#!/usr/bin/env python3
"""Build a flashable EG1985??.BIN from a patch spec, and verify module files.

This wraps patch.py (the guarded patcher: R2/R3/R7/R8 + package-CRC invariant)
and adds the SD-card packaging, the rollback image and a verification pass.

Usage
-----
  python make_update.py stock
        Build/refresh the stock rollback image at build/sd/stock/EG198581.BIN

  python make_update.py build --spec patches/xxx.json --label test2
        Build build/sd/test2/EG198581.BIN (+ report.json + FLASH.txt)

  python make_update.py verify build/sd/test2/EG198581.BIN
        Check size / CRC residue / version string / diff vs stock

  python make_update.py list
        List existing builds under build/sd/

Every produced file is named EG198581.BIN because the camera only recognises
the pattern EG1985??.BIN (type 2 = main EG module).  Put exactly ONE of them
in the SD card root; the camera reports "There is many update files." for more.
"""
from __future__ import annotations

import argparse
import binascii
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SD = ROOT / "build" / "sd"
CONTAINER = ROOT / "Z_fc_0181.bin"
UPDATE_NAME = "EG198581.BIN"          # must match EG1985??.BIN
MODULE_SIZE = 35_021_690
STOCK_SHA256 = "cd47efc126ce5e4ce98fe95bcfe30089a07e86d7f256a4eb0df2f6bc6e9233e3"
STOCK_SPEC = ROOT / "patches" / "stock.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify(path: pathlib.Path, stock: bytes | None = None) -> dict:
    data = path.read_bytes()
    info = {
        "file": str(path),
        "size": len(data),
        "crc_residue": binascii.crc_hqx(data, 0),
        "sha256": sha256(data),
        "version": data[0x20:0x30].split(b"\0")[0].decode("ascii", "replace"),
        "size_ok": len(data) == MODULE_SIZE,
        "crc_ok": binascii.crc_hqx(data, 0) == 0,
    }
    if stock is not None:
        if len(stock) != len(data):
            info["changed_bytes"] = None
        else:
            info["changed_bytes"] = sum(1 for a, b in zip(stock, data) if a != b)
    return info


def run_patch(spec: pathlib.Path, output: pathlib.Path, report: pathlib.Path) -> None:
    cmd = [sys.executable, str(ROOT / "patch.py"),
           "--input", str(CONTAINER),
           "--spec", str(spec),
           "--output", str(output),
           "--report", str(report)]
    print("$ " + " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    if res.returncode != 0:
        raise SystemExit(f"patch.py failed (exit {res.returncode})")


def write_flash_txt(folder: pathlib.Path, label: str, info: dict, report: dict | None) -> None:
    patches = []
    if report:
        for p in report.get("patches", []):
            patches.append(f"  {p['offset_hex']}  {p['expected']} -> {p['replacement']}  {p['note']}")
    lines = [
        f"刷机说明 —— {label}",
        "=" * 40,
        f"文件      {UPDATE_NAME}",
        f"大小      {info['size']:,} 字节",
        f"CRC 残差  0x{info['crc_residue']:04X}  ({'OK' if info['crc_ok'] else 'FAIL'})",
        f"SHA-256   {info['sha256']}",
        f"版本串    {info['version']}",
        f"改动字节  {info.get('changed_bytes', '?')}",
        "",
        "改动明细",
    ] + (patches or ["  （无：这是原厂模块）"]) + [
        "",
        "步骤",
        "  1. 电池充满（或接电源适配器）",
        "  2. SD 卡根目录只放这一个文件，文件名必须是 " + UPDATE_NAME,
        "  3. 相机：设置 → 固件版本 → 版本升级 → A → 确认",
        "  4. 等进度条走完，提示“更新成功，请关闭相机”后断电重启",
        "",
        "回滚",
        f"  把 {SD / 'stock' / UPDATE_NAME} 再刷一次",
        "",
        "风险",
        "  与官方固件升级同级；写入过程中断电有风险，满电、别碰相机。",
    ]
    (folder / "FLASH.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def stock_bytes() -> bytes:
    p = SD / "stock" / UPDATE_NAME
    return p.read_bytes() if p.exists() else b""


def cmd_stock(args) -> int:
    folder = SD / "stock"
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / UPDATE_NAME
    report = folder / "report.json"
    run_patch(STOCK_SPEC, out, report)
    info = verify(out)
    write_flash_txt(folder, "stock（原厂回滚）", info, None)
    print(f"\nstock image: {out}")
    print(f"  size={info['size']:,}  crc=0x{info['crc_residue']:04X}  "
          f"sha={info['sha256'][:16]}…  version={info['version']}")
    if info["sha256"] != STOCK_SHA256:
        print("!! stock image hash differs from the verified one "
              f"({STOCK_SHA256})", file=sys.stderr)
        return 3
    return 0


def cmd_build(args) -> int:
    spec = pathlib.Path(args.spec).resolve()
    if not spec.exists():
        raise SystemExit(f"spec not found: {spec}")
    label = args.label.strip()
    if not label or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in label):
        raise SystemExit("label must be simple ascii (a-z, 0-9, -, _)")

    folder = SD / label
    out = folder / UPDATE_NAME
    if out.exists() and not args.force:
        raise SystemExit(f"{out} exists; use --force to overwrite")
    folder.mkdir(parents=True, exist_ok=True)

    report_path = folder / "report.json"
    run_patch(spec, out, report_path)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    info = verify(out, stock_bytes() or None)
    write_flash_txt(folder, label, info, report)

    print(f"\nbuild: {out}")
    print(f"  size={info['size']:,}  crc=0x{info['crc_residue']:04X}  "
          f"changed={info.get('changed_bytes')}  version={info['version']}")
    print(f"  sha256={info['sha256']}")
    if not info["crc_ok"] or not info["size_ok"]:
        print("!! verification failed", file=sys.stderr)
        return 3
    print(f"  instructions: {folder / 'FLASH.txt'}")
    print(f"  rollback:     {SD / 'stock' / UPDATE_NAME}")
    return 0


def cmd_verify(args) -> int:
    path = pathlib.Path(args.file).resolve()
    info = verify(path, stock_bytes() or None)
    for k, v in info.items():
        print(f"  {k:14} {v}")
    ok = info["size_ok"] and info["crc_ok"]
    print("RESULT " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 3


def cmd_list(args) -> int:
    if not SD.exists():
        print("no builds yet")
        return 0
    for folder in sorted(p for p in SD.iterdir() if p.is_dir()):
        f = folder / UPDATE_NAME
        if not f.exists():
            continue
        info = verify(f, stock_bytes() or None)
        print(f"  {folder.name:16} {info['size']:>10,}  crc=0x{info['crc_residue']:04X}  "
              f"changed={info.get('changed_bytes')}  {info['sha256'][:12]}…")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("stock", help="build the stock rollback image")
    s.set_defaults(func=cmd_stock)

    b = sub.add_parser("build", help="build a patched update file")
    b.add_argument("--spec", required=True)
    b.add_argument("--label", required=True)
    b.add_argument("--force", action="store_true")
    b.set_defaults(func=cmd_build)

    v = sub.add_parser("verify", help="verify a module file")
    v.add_argument("file")
    v.set_defaults(func=cmd_verify)

    l = sub.add_parser("list", help="list builds")
    l.set_defaults(func=cmd_list)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
