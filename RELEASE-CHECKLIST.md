# v2.0 候选版发布审查清单 / v2.0 Candidate Release Review Checklist

Scope: Nikon Z fc C 1.81. **v2.0 remains a candidate (v2.0 候选版)** on the public review branch (`release/v2.0`, recipe commit `a199576`). Formal Release status is governed by GitHub Releases (currently `v1`).

## Review Items

- [x] **Declared identity & author local reproduction log (`a199576`)**: `patches/zfc-v2.json` declares target size `35,060,342` B and SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`. Author local reproduction log for `a199576` is archived at [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md) (**作者本地报告**).
- [ ] **Independent verification of current commit (`a199576`) — 待验证**: Independent re-run of `verify_release.py` and independent gate verification against commit `a199576` remain pending.
- [x] **Classification of 27 warnings in saved offline report**: Applies strictly to the previously reviewed offline gate report (`zfc_all1b-finalbin-gate.json`, 0 violations, 27 warnings); all 27 are 2-byte zero-padding entries. This classification does not add runtime or new-commit verification.
- [x] **Owner initial test scope & earlier video reports separated**: Documented in [README.md](README.md), [CHANGELOG.md](CHANGELOG.md), and [docs/V2-ARCHITECTURE.md](docs/V2-ARCHITECTURE.md) (>30 min video and per-quality bitrates untested on `zfc_all1b`; the historical 34:32 recording and five MP4 modes are recorded with the tested image unconfirmed).
- [x] **Rollback observations & recovery limitations**: Removed any "flash stock to recover" guarantee; documented observed normal-menu rollback conditions separately from the lack of reliable recovery evidence when the camera cannot boot or open the update menu.
- [ ] **来源和再分发依据已确认 (Provenance & redistribution basis confirmed)**: All 48 `replacement` records, 213 `write` records, and `tools/tables.json` are catalogued in [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md), where items pending verification (`W1`/`W2`/`W6` `<12 B` fragments, `W3`/`W4` author confirmation, `tools/tables.json` upstream commit & license) are marked **「待确认」**. Must be resolved before any formal release.
- [ ] **维护者签署发布决定 (Maintainer release sign-off)**: Confirm repo hygiene (zero `*.bin`/`*.BIN`, zero absolute paths) and record explicit maintainer sign-off before creating a GitHub Release or pushing a `v2.0` tag.

A completed local hash check establishes file identity only; it does not establish hardware behavior, independent verification, or brick recovery.
