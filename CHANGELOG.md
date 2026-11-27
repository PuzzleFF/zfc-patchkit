# Changelog

## [2.0] - candidate (unreleased)

**Status**: Project candidate on public review branch (`release/v2.0`, recipe commit `a199576`). Formal Release status is governed by GitHub Releases (currently `v1`).

### Summary of Candidate Changes (`zfc-v2` / research label `zfc_all1b`)
- **Video settings**: 125-minute recording duration entries + engine gate (`unlock2`), 25-minute slow-motion setting (`slowmo25`), and Movie Quality menu + `qmenu_rates` (`qs8`).
- **Setup menu, zebra & shutter sound**: Unified Setup Menu Page 394 entry with cold-boot text initialization, independent Photo-mode highlight display toggle, and 5-slot silent-mode custom shutter sound (`ZFC\SHUTTER.WAV`, `1.WAV`..`4.WAV`; 8 kHz 16-bit mono PCM WAV <= 17,280 B).
- **Custom aspect ratio suite**: 5 custom ratios (5:4 removed, 8 items on Page 1), LCD + EVF pure-black Live View masks with EVF UI preservation and 4-pixel `ldmia`/`stmia` burst speedup, no-reboot playback zoom repair, and automatic mask hide in Movie mode.
- **Unified configuration & boot auto-restore**: Single `A:\ZFCEXT.CFG` file restored automatically on cold boot.
- **Tooling**: `tools/patch.py` extended to support `expected_sha256` target checks and `append_recipe` (`copy_stock` + `write`) builds without external dependencies.

### Test & Verification Boundaries
- **Owner initial test (`zfc_all1b`, photo-focused)**: power cycling, still photography, aspect-ratio masks, custom shutter sound, and short video clips reported no issues. The owner later confirmed separate on-camera tests of the unified Setup menu, independent photo zebra, and cold-boot configuration restoration. The owner also confirmed testing custom shutter sound on `extsnd1` and `extboot1`. Recordings > 30 minutes and bitrate across quality modes were **not** tested on `zfc_all1b`.
- **Historical video measurements**: a 10-minute slow-motion recording is documented for `slowmo25`. A historical summary reports a `34:32` / `3.1 GB` recording and 5 MP4 quality modes. The image used for each of those two results has not been confirmed. Full 125 min, 4 GiB boundary, long 4K recording, full 25 min slow-motion, and MOV remain untested.
- **Verification**: Declared target SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`; author local reproduction log archived in [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md) (author local report); previously reviewed offline report recorded 0 violations and 27 two-byte zero-padding warnings; independent verification of current commit `a199576` is pending. See [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) and [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md).

## [1] - 2026-10-25

First published release. Three features, all verified on a physical Nikon Z fc
running firmware C 1.81, plus the tooling used to produce and reproduce them.

### Added
- **Slow-motion limit 3 -> 25 minutes** - 4 bytes at `0x102A0470`
  (`180000` -> `1500000` ms). A 10-minute clip recorded normally; the full
  25 minutes was not exercised.
- **1080p bitrate boost** - 6 records in the video mode table at `0x10717144`.
  1080p 60/50 high: 56/48 -> 84/70 Mbps; 1080p 60/50 standard: 28/24 -> 56/48;
  1080p 30/25/24 high: 28/24 -> 56/48; 1080p 30/25/24 standard: 14/12 -> 28/24.
  Eight formats measured with MediaInfo; 4K untouched.
- **Photo-mode zebra** - `0x101765DE` and `0x1017670A`, 2 bytes each
  (`cbz r5,reject` -> `nop`). Photo live view now shows the native highlight
  pattern, still toggled by the camera own "highlight display" menu item.
- `combo` spec combining all three (this is the `zfc-v1` image).
- Tooling: container parser and CRC, equal-length patcher with five gates,
  SD-card packaging, and `verify_release.py` which rebuilds every artifact and
  checks it against the pinned SHA-256.
- Technical reports in `docs/`.

### Notes
- 4K bitrate deliberately left at the stock 144/120 and 72/60.
- The 30-minute recording limit was later addressed in the v2.0 candidate (`unlock2`).
