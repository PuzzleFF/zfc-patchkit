# v2.0 候选版发布审查清单 / v2.0 Candidate Release Review Checklist

Scope: Nikon Z fc C 1.81. **v2.0 remains a candidate (v2.0 候选版)** on the public review branch (`release/v2.0`, recipe commit `a199576`). Formal Release status is governed by GitHub Releases (currently `v1`).

## Review Items

- [x] **Declared identity vs local reproduction (`a199576`)**: `patches/zfc-v2.json` declares target size `35,060,342` B and SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`; local `verify_release.py` on `a199576` reproduced all 7 pinned artifacts (`stock`, v1 specs, `zfc-v2`).
- [ ] **Independent verification of current commit (`a199576`) — 待验证**: Independent re-run of `verify_release.py` and offline gate review against commit `a199576` is not yet recorded.
- [x] **Classification of 27 warnings in saved offline report**: Applies strictly to the previously reviewed offline gate report (`zfc_all1b-finalbin-gate.json`, 0 violations, 27 warnings); all 27 are 2-byte zero-padding entries. This classification does not add runtime or new-commit verification.
- [x] **Separate menu settings, owner initial test scope, and earlier video reports**: Documented in [README.md](README.md), [CHANGELOG.md](CHANGELOG.md), and [docs/V2-ARCHITECTURE.md](docs/V2-ARCHITECTURE.md). Owner tested `zfc_all1b` primarily for photography (power cycle, stills, aspect masks, custom shutter sound, short video — no issues reported); >30 min video and per-quality bitrates were not tested on `zfc_all1b`. Earlier video results (34:32 / 3.1 GB, 10 min slow-mo, 5 MP4 modes) are attributed to their earlier builds.
- [x] **Rollback observations & recovery limitations**: Removed any "flash stock to recover" guarantee; documented observed normal-menu rollback conditions separately from the lack of reliable recovery evidence when the camera cannot boot or open the update menu.
- [ ] **Embedded-byte provenance & clean separation (`a199576`)**: Commit `a199576` moved 48 `expected` checks to `expected_sha256` and 239 runs >= 12 B (9,433 B) to local `copy_stock`. All remaining 213 `write` records and 48 `replacement` records are catalogued in [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md), where `W1`/`W2`/`W6` (`<12 B` stock-table gaps and short prologue replays) remain marked **「待核实」**. Resolve or record maintainer sign-off before any formal release.
- [ ] **Repo hygiene & maintainer decision**: Confirm zero `*.bin`/`*.BIN` files, zero absolute paths, and record maintainer sign-off before creating a GitHub Release or pushing a `v2.0` tag.

A completed local hash check establishes file identity only; it does not establish hardware behavior, independent verification, or brick recovery.
