#!/usr/bin/env python3
"""Nikon Z-series firmware container tool (legacy packaging).

Layout (per WonderLantern/nikon-fw-key-tool):
  file 0x00 : [20B SHA-1 digest][12B unidentified]
  file 0x20 : body
  body 0x00 : 32 ASCII spaces, plaintext (space label)
  body 0x20 : BE32 module count | BE32 directory size | 8 zero bytes
  body 0x30 : count * [16B name | BE32 body offset | BE32 length | 8 zero]
  ...       : modules back to back, each ending in BE16 CRC
  ...       : BE16 package CRC | 14 zero bytes

XOR keystream over body bytes at body offset i >= 0x20:
  plain[i] = cipher[i] ^ T1[i & 0xFF] ^ T2[(i>>8)&0xFF] ^ T3[(i>>16)&0xFF]

Usage:
  python zf.py info    --input Z_fc_0181.bin
  python zf.py unpack  --input Z_fc_0181.bin --outdir extracted
  python zf.py roundtrip --input Z_fc_0181.bin
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

import numpy as np

HEADER_LEN = 0x20
BODY_DIR_OFF = 0x20
DIR_ENTRY = 32
DIR_BASE = 48
TRAILER = 16

# ---------------------------------------------------------------------------
# XOR tables (legacy Nikon scheme, three 256-byte tables)
#
# Fetched from the public NikonHacker decoder rather than transcribed by hand,
# so a typo cannot silently corrupt every decode. Cached in tables.json.
# ---------------------------------------------------------------------------
TABLES_URL = ("https://raw.githubusercontent.com/simeonpilgrim/nikon-firmware-tools/"
              "master/firmware%20decode/firmware%20decode/Firmware.cs")
TABLES_CACHE = pathlib.Path(__file__).with_name("tables.json")


def _download_tables() -> dict:
    import re
    import urllib.request

    req = urllib.request.Request(TABLES_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        src = resp.read().decode("utf-8", "replace")

    out = {}
    for key in ("Xor_Ord1", "Xor_Ord2", "Xor_Ord3"):
        m = re.search(rf"{key}\s*=\s*\{{(.*?)\}};", src, re.S)
        if not m:
            raise RuntimeError(f"{key} not found in {TABLES_URL}")
        raw = [int(tok.strip().rstrip(","), 16) & 0xFF
               for tok in m.group(1).replace("\n", " ").split(",") if tok.strip()]
        if len(raw) != 256:
            raise RuntimeError(f"{key}: expected 256 entries, got {len(raw)}")
        out[key] = raw
    return out


def _load_tables() -> dict:
    if TABLES_CACHE.exists():
        return json.loads(TABLES_CACHE.read_text(encoding="utf-8"))
    data = _download_tables()
    TABLES_CACHE.write_text(json.dumps(data, indent=0), encoding="utf-8")
    return data


_TABLES = _load_tables()
T1 = np.array(_TABLES["Xor_Ord1"], dtype=np.uint8)
T2 = np.array(_TABLES["Xor_Ord2"], dtype=np.uint8)
T3 = np.array(_TABLES["Xor_Ord3"], dtype=np.uint8)
assert T1.size == T2.size == T3.size == 256, "XOR tables must be 256 bytes"


# ---------------------------------------------------------------------------
# CRC-16/CCITT-FALSE: poly 0x1021, init 0, no reflection, no final xor
# ---------------------------------------------------------------------------
def _crc_table() -> np.ndarray:
    tbl = np.zeros(256, dtype=np.uint16)
    for i in range(256):
        crc = i << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
        tbl[i] = crc
    return tbl


_CRC_TBL = _crc_table()


def crc16(data: bytes) -> int:
    crc = 0
    tbl = _CRC_TBL
    for byte in data:
        crc = ((crc << 8) & 0xFFFF) ^ int(tbl[((crc >> 8) ^ byte) & 0xFF])
    return crc


# ---------------------------------------------------------------------------
# XOR keystream
# ---------------------------------------------------------------------------
def xor_keystream(length: int) -> np.ndarray:
    """Keystream for body offsets 0 .. length-1 (index starts at 0 == body start)."""
    idx = np.arange(length, dtype=np.uint32)
    return (T1[idx & 0xFF] ^ T2[(idx >> 8) & 0xFF] ^ T3[(idx >> 16) & 0xFF]).astype(np.uint8)


def crypt_body(body: bytes, label_plain: bool = True) -> bytes:
    """Symmetric: decrypt or encrypt the body (same operation).

    The keystream index is the absolute body offset, so the first encrypted
    byte (body 0x20) uses T1[0x20]. The 32-byte space label stays plaintext.
    """
    arr = np.frombuffer(body, dtype=np.uint8).copy()
    start = HEADER_LEN if label_plain else 0
    if start < arr.size:
        ks = xor_keystream(arr.size)
        arr[start:] ^= ks[start:]
    return arr.tobytes()


# ---------------------------------------------------------------------------
# Container parsing
# ---------------------------------------------------------------------------
def u32(buf: bytes, off: int) -> int:
    return int.from_bytes(buf[off:off + 4], "big")


def u16(buf: bytes, off: int) -> int:
    return int.from_bytes(buf[off:off + 2], "big")


class Module:
    def __init__(self, name: str, offset: int, length: int):
        self.name = name
        self.offset = offset
        self.length = length
        self.payload = b""
        self.stored_crc = 0
        self.calc_crc = 0

    @property
    def crc_ok(self) -> bool:
        return self.stored_crc == self.calc_crc


def parse_directory(body: bytes) -> list[Module]:
    count = u32(body, BODY_DIR_OFF)
    dir_size = u32(body, BODY_DIR_OFF + 4)
    if not 0 < count <= 64:
        raise ValueError(f"implausible module count {count}")
    if dir_size != DIR_BASE + DIR_ENTRY * count:
        raise ValueError(f"directory size {dir_size} != 48+32*{count}")
    if body[BODY_DIR_OFF + 8:BODY_DIR_OFF + 16] != b"\0" * 8:
        raise ValueError("directory reserved bytes are not zero")

    modules = []
    for i in range(count):
        base = BODY_DIR_OFF + 16 + i * DIR_ENTRY
        raw_name = body[base:base + 16]
        name = raw_name.split(b"\0")[0].decode("ascii", "replace")
        if not name or any(not (32 <= ord(c) < 127) for c in name):
            raise ValueError(f"bad module name at index {i}: {raw_name!r}")
        offset = u32(body, base + 16)
        length = u32(body, base + 20)
        if body[base + 24:base + 32] != b"\0" * 8:
            raise ValueError(f"module {name}: reserved bytes not zero")
        if offset + length > len(body) - TRAILER:
            raise ValueError(f"module {name}: extent outside body")
        modules.append(Module(name, offset, length))
    return modules


def load_container(path: pathlib.Path) -> dict:
    data = path.read_bytes()
    if len(data) < HEADER_LEN + BODY_DIR_OFF + 16:
        raise ValueError("file too small")
    body = data[HEADER_LEN:]
    if body[:0x20] != b" " * 0x20:
        raise ValueError("space label missing (not a legacy container?)")

    candidates = []
    for label_plain, desc in ((True, "label plaintext, key starts at 0x20"),
                              (False, "key starts at 0")):
        plain = crypt_body(body, label_plain=label_plain)
        try:
            modules = parse_directory(plain)
        except ValueError as exc:
            candidates.append((desc, None, str(exc)))
            continue
        candidates.append((desc, plain, "ok"))

    good = [(d, p) for d, p, s in candidates if p is not None]
    if not good:
        detail = "; ".join(f"{d}: {s}" for d, _, s in candidates)
        raise ValueError(f"no XOR variant produced a valid directory ({detail})")

    desc, plain = good[0]
    modules = parse_directory(plain)

    # DIR_BASE already counts the 0x20 space label, so the first module begins
    # at body offset 48 + 32*count.
    expected = DIR_BASE + DIR_ENTRY * len(modules)
    for m in modules:
        if m.offset != expected:
            raise ValueError(f"{m.name}: offset {m.offset} != expected {expected}")
        expected = m.offset + m.length

    for m in modules:
        blob = plain[m.offset:m.offset + m.length]
        m.payload = blob[:-2]
        m.stored_crc = u16(blob, m.length - 2)
        m.calc_crc = crc16(m.payload)

    trailer = plain[-TRAILER:]
    pkg_stored = u16(trailer, 0)
    pkg_calc = crc16(plain[:-TRAILER])

    return {
        "data": data,
        "body": body,
        "plain": plain,
        "modules": modules,
        "variant": desc,
        "package_crc_stored": pkg_stored,
        "package_crc_calc": pkg_calc,
        "trailer_zeros_ok": trailer[2:] == b"\0" * 14,
    }


def summarize(info: dict, path: pathlib.Path) -> dict:
    plain = info["plain"]
    return {
        "file": str(path),
        "size": len(info["data"]),
        "sha256": hashlib.sha256(info["data"]).hexdigest(),
        "xor_variant": info["variant"],
        "space_label_ok": plain[:0x20] == b" " * 0x20,
        "module_count": len(info["modules"]),
        "directory_size": u32(plain, BODY_DIR_OFF + 4),
        "package_crc": {"stored": f"{info['package_crc_stored']:04X}",
                        "calculated": f"{info['package_crc_calc']:04X}",
                        "ok": info["package_crc_stored"] == info["package_crc_calc"]},
        "trailer_padding_zero": info["trailer_zeros_ok"],
        "body_sha1": hashlib.sha1(plain).hexdigest(),
        "header_digest": info["data"][:20].hex(),
        "modules": [
            {
                "name": m.name,
                "offset": m.offset,
                "offset_hex": f"0x{m.offset:X}",
                "length": m.length,
                "payload_length": m.length - 2,
                "crc_stored": f"{m.stored_crc:04X}",
                "crc_calculated": f"{m.calc_crc:04X}",
                "crc_ok": m.crc_ok,
            }
            for m in info["modules"]
        ],
    }


def cmd_info(args) -> int:
    path = pathlib.Path(args.input)
    info = load_container(path)
    print(json.dumps(summarize(info, path), indent=2, ensure_ascii=False))
    return 0 if all(m.crc_ok for m in info["modules"]) else 2


def cmd_unpack(args) -> int:
    path = pathlib.Path(args.input)
    info = load_container(path)
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for m in info["modules"]:
        (outdir / m.name).write_bytes(m.payload)

    (outdir / "body.bin").write_bytes(info["plain"])
    report = summarize(info, path)
    (outdir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                        encoding="utf-8")

    print(json.dumps({k: report[k] for k in
                      ("size", "sha256", "module_count", "package_crc", "space_label_ok")},
                     indent=2, ensure_ascii=False))
    print("\nmodules:")
    for m in info["modules"]:
        print(f"  {m.name:<24} off=0x{m.offset:08X} len={m.length:>10} "
              f"crc={m.stored_crc:04X} {'OK' if m.crc_ok else 'MISMATCH'}")
    print(f"\nwrote {len(info['modules'])} modules + body.bin + report.json to {outdir}")
    return 0 if all(m.crc_ok for m in info["modules"]) else 2


def cmd_roundtrip(args) -> int:
    path = pathlib.Path(args.input)
    info = load_container(path)
    reencoded = info["data"][:HEADER_LEN] + crypt_body(info["plain"], label_plain=True)
    original = info["data"]
    same = reencoded == original
    print(f"original  sha256={hashlib.sha256(original).hexdigest()}")
    print(f"reencoded sha256={hashlib.sha256(reencoded).hexdigest()}")
    print(f"byte-identical: {same}")
    if not same:
        for i, (a, b) in enumerate(zip(original, reencoded)):
            if a != b:
                print(f"first difference at file offset 0x{i:X}: {a:02X} != {b:02X}")
                break
    return 0 if same else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("info")
    p.add_argument("--input", required=True)
    p.set_defaults(func=cmd_info)

    p = sub.add_parser("unpack")
    p.add_argument("--input", required=True)
    p.add_argument("--outdir", default="extracted")
    p.set_defaults(func=cmd_unpack)

    p = sub.add_parser("roundtrip")
    p.add_argument("--input", required=True)
    p.set_defaults(func=cmd_roundtrip)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
