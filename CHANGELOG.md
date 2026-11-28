# Changelog

## [2.0] - 2026-11-27

Official v2.0 release (`zfc-v2` / `zfc_all1b_bi` auto-bilingual, target size `35,060,966` B,
SHA-256 `cfaf2e4848ffe96757aef71ca1f9eaaf58482c351d57250d4fa7f35208e38d5a`; supersedes initial `zfc_all1b` `b5c6e75e...` with live Simplified Chinese / clean English auto-switching via `PROP_GET(0x1400)`).

### Added
- **Complete Custom Aspect Ratio suite + EVF Burst Speedup + Movie Auto-Hide**: 5 custom ratios (`2.35:1`, `1.85:1`, `4:3`, `2:1`, `65:24 XPAN`; `5:4` removed, all 8 items on Page 1), LCD + EVF pure-black Live View masks with EVF UI preservation and 4-pixel `ldmia`/`stmia` burst speedup, no-reboot playback zoom repair, and automatic mask hide in Movie mode / restore in Photo mode.
- **Unified Setup Menu entry & Independent Photo Zebra**: Setup Menu Page 394 entry with cold-boot text initialization and independent Photo-mode highlight display toggle.
- **Silent-mode Custom Shutter Sound**: 5 fixed WAV slots (`ZFC\SHUTTER.WAV`, `1.WAV`..`4.WAV`; uncompressed 8 kHz 16-bit mono PCM WAV <= 17,280 B / ~1.08 s) with automatic preview on select.
- **Unified Configuration & Cold-Boot Auto-Restore**: Single `A:\ZFCEXT.CFG` file restored automatically on power-on without opening any menu.
- **Video Suite**: 125-minute recording duration entries + engine gate (`unlock2`), 25-minute slow-motion (`slowmo25`), and Movie Quality menu + `qmenu_rates` (`qs8`).
- **Tooling**: `tools/patch.py` extended to support `expected_sha256` target checks and `append_recipe` (`copy_stock` + `write`) builds with zero external dependencies.

### Test & Verification Boundaries
- **Owner on-camera test (`zfc_all1b`, photo-focused)**: power cycling, still photography, aspect-ratio masks (including Movie-mode auto-hide / Photo-mode restore), unified Setup menu, independent photo zebra, custom shutter sound, cold-boot config restoration, and short video clips reported no issues. Owner also confirmed custom shutter sound on `extsnd1` and `extboot1`. Recordings > 30 minutes and bitrate across quality modes were **not** tested on `zfc_all1b`.
- **Historical video measurements**: a 10-minute slow-motion recording is documented for `slowmo25`. A historical summary reports a `34:32` / `3.1 GB` recording and 5 MP4 quality modes (specific test images unconfirmed). Full 125 min, 4 GiB boundary, long 4K recording, full 25 min slow-motion, and MOV remain untested.
- **Verification**: Author local reproduction log archived in [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md) (7/7 MATCH); previously reviewed offline report recorded 0 violations and 27 two-byte zero-padding warnings; independent third-party verification is deferred. See [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) and [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md).

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
- The 30-minute recording limit was addressed in v2.0 (`unlock2`).
