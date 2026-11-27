#!/usr/bin/env python3
"""Guarded patcher for the Z fc EG module (v1 equal-length & v2 code-cave).

Every safety gate that can be checked offline is enforced here, and the build
aborts if any of them fails:

  R2  equal-length replacement for every in-place patch window
  R3  directory bytes and other modules untouched (v1 equal-length mode)
  R7  only the requested bytes may differ in the original module payload
  R8  input must match the pinned official C 1.81 SHA-256
  --  v1: package CRC must remain 0xC023 after module CRC repair
      v2: appended code-cave payload matches pinned append_sha256 & module CRC residue == 0

The output is the standalone EG module, the same artifact shape the Wonder
Lantern project installs. Nothing here writes to a camera.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import zf

ROOT = pathlib.Path(__file__).resolve().parent
EXPECTED_SHA256 = "e4cd838a215c113659416983b31dbdba8896591caacf7309170d4cc3c60bd1b6"
EXPECTED_PACKAGE_CRC = 0xC023
TRAILER = 16


class BuildError(RuntimeError):
    pass


def load_spec(path: pathlib.Path) -> tuple[list[dict], bytes, str | None]:
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    append_bytes = b""
    append_sha256 = None
    if isinstance(raw, dict):
        spec = raw.get("patches", [])
        if raw.get("append_hex"):
            append_bytes = bytes.fromhex(raw["append_hex"])
            append_sha256 = raw.get("append_sha256")
            if append_sha256:
                got = hashlib.sha256(append_bytes).hexdigest()
                if got != append_sha256:
                    raise BuildError(f"append_hex sha256 mismatch: {got} != {append_sha256}")
    else:
        spec = raw
    for i, p in enumerate(spec):
        for key in ("offset", "expected", "replacement"):
            if key not in p:
                raise BuildError(f"patch #{i}: missing '{key}'")
        p.setdefault("note", "")
    return spec, append_bytes, append_sha256


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="official Z_fc_0181.bin")
    ap.add_argument("--spec", required=True, help="JSON patch spec")
    ap.add_argument("--output", required=True, help="output EG module path")
    ap.add_argument("--report", help="output JSON report path")
    args = ap.parse_args()

    src = pathlib.Path(args.input)
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    print(f"input  {src.name}  {len(data):,} bytes")
    print(f"sha256 {digest}")

    if digest != EXPECTED_SHA256:
        raise BuildError("input hash is not the pinned official image (R8)")

    info = zf.load_container(src)
    eg = next((m for m in info["modules"] if m.name.startswith("eg")), None)
    if eg is None:
        raise BuildError("no eg module in container")

    print(f"module {eg.name}  offset=0x{eg.offset:X} len={eg.length:,}")
    if not eg.crc_ok:
        raise BuildError("input module CRC is wrong; refusing to build")

    original = bytes(eg.payload)
    payload = bytearray(original)

    spec, append_bytes, append_sha256 = load_spec(pathlib.Path(args.spec))
    print(f"patches: {len(spec)}" + (f"  append: {len(append_bytes):,} B" if append_bytes else ""))

    touched: set[int] = set()
    applied = []
    for i, p in enumerate(spec):
        off = int(p["offset"])
        exp = bytes.fromhex(p["expected"])
        rep = bytes.fromhex(p["replacement"])
        if len(exp) != len(rep):
            raise BuildError(f"patch #{i}: expected/replacement length differ (R2)")
        if off < 0 or off + len(rep) > len(payload):
            raise BuildError(f"patch #{i}: offset 0x{off:X} outside module")
        if payload[off:off + len(exp)] != exp:
            raise BuildError(
                f"patch #{i}: bytes at 0x{off:X} are {payload[off:off+len(exp)].hex()}, "
                f"expected {exp.hex()}")
        payload[off:off + len(rep)] = rep
        touched.update(range(off, off + len(rep)))
        applied.append({"index": i, "offset": off, "offset_hex": f"0x{off:X}",
                        "expected": exp.hex(), "replacement": rep.hex(),
                        "note": p["note"]})
        if len(spec) <= 30:
            print(f"  #{i} 0x{off:X}  {exp.hex()} -> {rep.hex()}  {p['note']}")

    # R7: diff inside original payload must be strictly within declared patches
    changed = [i for i in range(len(original)) if original[i] != payload[i]]
    escaped = [i for i in changed if i not in touched]
    if escaped:
        raise BuildError(f"{len(escaped)} unexpected byte(s) changed, first at 0x{escaped[0]:X}")
    print(f"changed bytes: {len(changed)} (all within requested ranges)")

    final_payload = bytes(payload) + append_bytes
    new_crc = zf.crc16(final_payload)
    if zf.crc16(final_payload + new_crc.to_bytes(2, "big")) != 0:
        raise BuildError("module CRC residual is not zero (CRC chain broken)")

    pkg_crc_actual = None
    if not append_bytes:
        body = bytearray(info["plain"])
        body[eg.offset:eg.offset + eg.length] = final_payload + new_crc.to_bytes(2, "big")
        if body[0x20:eg.offset] != info["plain"][0x20:eg.offset]:
            raise BuildError("directory bytes changed (R3)")
        for m in info["modules"]:
            if m is eg:
                continue
            if body[m.offset:m.offset + m.length] != info["plain"][m.offset:m.offset + m.length]:
                raise BuildError(f"module {m.name} changed unexpectedly (R3)")
        pkg_crc_actual = zf.crc16(bytes(body[:-TRAILER]))
        print(f"package CRC 0x{pkg_crc_actual:04X} (expected 0x{EXPECTED_PACKAGE_CRC:04X})")
        if pkg_crc_actual != EXPECTED_PACKAGE_CRC:
            raise BuildError("package CRC changed; the edit escaped the module (invariant)")

    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(final_payload + new_crc.to_bytes(2, "big"))

    report = {
        "input": {"file": src.name, "size": len(data), "sha256": digest},
        "module": {"name": eg.name, "offset": eg.offset, "length": eg.length},
        "patches": applied,
        "appended_bytes": len(append_bytes),
        "append_sha256": append_sha256,
        "module_crc": {"old": f"{eg.stored_crc:04X}", "new": f"{new_crc:04X}"},
        "package_crc": None if pkg_crc_actual is None else {
            "expected": f"{EXPECTED_PACKAGE_CRC:04X}",
            "actual": f"{pkg_crc_actual:04X}",
        },
        "changed_bytes": len(changed),
        "output": {"file": out.name, "size": out.stat().st_size,
                   "sha256": hashlib.sha256(out.read_bytes()).hexdigest()},
        "camera_verified": False,
    }
    rp = pathlib.Path(args.report) if args.report else out.with_suffix(".json")
    rp.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nwrote {out}  ({out.stat().st_size:,} bytes)")
    print(f"wrote {rp}")
    print("RESULT PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as exc:
        print(f"\nBUILD REFUSED: {exc}", file=sys.stderr)
        sys.exit(2)
