# v2.0 发布审查清单 / v2.0 Release Review Checklist

Scope: Nikon Z fc C 1.81 · **v2.0 正式发布（2026-11-27）**（`zfc-v2` / `zfc_all1b`）。

## Review Items

- [x] **Declared identity & author local reproduction log (`a199576`)**: `patches/zfc-v2.json` declares target size `35,060,342` B and SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`. Author local reproduction log for `a199576` is archived at [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md) (**作者本地报告**).
- [ ] **Independent third-party verification of `a199576`（延后）**: Maintainer decided to ship v2.0 based on on-camera testing and author local reproduction; independent third-party verification remains open for community follow-up.
- [x] **Classification of 27 warnings in saved offline report**: Applies strictly to the previously reviewed offline gate report (`zfc_all1b-finalbin-gate.json`, 0 violations, 27 warnings); all 27 are 2-byte zero-padding entries.
- [x] **Owner test scope & historical video reports separated**: Documented in [README.md](README.md), [CHANGELOG.md](CHANGELOG.md), and [docs/V2-ARCHITECTURE.md](docs/V2-ARCHITECTURE.md) (>30 min video and per-quality bitrates untested on `zfc_all1b`; `slowmo25` 10-min result archived; historical `34:32` & 5-MP4 summary image attribution noted as unconfirmed).
- [x] **Rollback observations & recovery limitations**: Removed any "flash stock to recover" guarantee; documented observed normal-menu rollback conditions separately from the lack of reliable recovery evidence when the camera cannot boot or open the update menu.
- [x] **来源与参考声明已确认 (Provenance & reference attribution confirmed by maintainer)**: All 48 `replacement` records, 213 `write` records, and `tools/tables.json` are catalogued in [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md). Maintainer confirmed reference attribution for `P1–P9` / `W3–W5`, accepted the current `a199576` recipe (`W1`/`W2`/`W6` `<12 B` gaps), and left `tools/tables.json` unchanged from v1.
- [x] **维护者签署发布决定 (Maintainer release sign-off — 2026-11-27)**: Repo hygiene verified (`*.bin`/`*.BIN` = 0, absolute paths = 0); maintainer approved formal `v2.0` release on `main` + GitHub Release (no `.BIN` assets uploaded).
