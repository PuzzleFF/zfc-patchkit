#!/usr/bin/env python3
"""Reproduce this kit's images from the official firmware and verify them.

The kit deliberately does NOT ship any Nikon firmware.  You supply the official
`Z_fc_0181.bin` yourself; this script then rebuilds every patched image from the
patch specs and compares the SHA-256 of each result against the pinned value
recorded when the images were verified on a real camera.

Usage
    python tools/verify_release.py                 # expects ./Z_fc_0181.bin
    python tools/verify_release.py --firmware D:/fw/Z_fc_0181.bin

Exit code 0 means every artifact matched its pinned hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

KIT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = KIT / "tools"
OUT = KIT / "build" / "verify"

OFFICIAL_SHA256 = "e4cd838a215c113659416983b31dbdba8896591caacf7309170d4cc3c60bd1b6"
OFFICIAL_SIZE = 35_578_974


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--firmware", default=str(KIT / "Z_fc_0181.bin"),
                    help="official Nikon Z fc C 1.81 firmware container")
    args = ap.parse_args()

    fw = pathlib.Path(args.firmware)
    if not fw.exists():
        print(f"!! firmware not found: {fw}\n"
              f"   Put the official Z fc C 1.81 update file there (or pass --firmware).\n"
              f"   This kit does not redistribute firmware.", file=sys.stderr)
        return 2

    digest = sha256(fw)
    size_ok = fw.stat().st_size == OFFICIAL_SIZE
    print(f"firmware  {fw.name}")
    print(f"  size    {fw.stat().st_size:,} (expected {OFFICIAL_SIZE:,}) {'OK' if size_ok else 'MISMATCH'}")
    print(f"  sha256  {digest}")
    print(f"          {'OK' if digest == OFFICIAL_SHA256 else 'MISMATCH -- this is not the pinned image'}")
    if digest != OFFICIAL_SHA256:
        return 2

    pins = json.loads((TOOLS / "pins.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    failures = 0
    print(f"\n{'label':<14}{'size':>12}  {'sha256':<18}result")
    print("-" * 62)
    for pin in pins:
        label = pin["label"]
        spec = KIT / pin["spec"]
        dest = OUT / label
        dest.mkdir(parents=True, exist_ok=True)
        out_file = dest / "EG198581.BIN"
        report = dest / "report.json"

        cmd = [sys.executable, str(TOOLS / "patch.py"),
               "--input", str(fw), "--spec", str(spec),
               "--output", str(out_file), "--report", str(report)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"{label:<14}{'--':>12}  {'--':<18}BUILD FAILED (exit {res.returncode})")
            tail = (res.stderr or res.stdout).strip().splitlines()[-3:]
            for line in tail:
                print(f"    {line}")
            failures += 1
            continue

        got = sha256(out_file)
        ok = got == pin["sha256"]
        failures += not ok
        print(f"{label:<14}{out_file.stat().st_size:>12,}  {got[:16]}...  "
              f"{'MATCH' if ok else 'MISMATCH vs ' + pin['sha256'][:16] + '...'}")

    print("-" * 62)
    if failures:
        print(f"{failures} artifact(s) did not match the pinned hashes", file=sys.stderr)
        print("If the specs were edited this is expected; otherwise the official "
              "firmware or the toolchain changed.", file=sys.stderr)
        return 1
    print("all artifacts reproduced and matched -- RESULT PASS")
    print(f"images are in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
