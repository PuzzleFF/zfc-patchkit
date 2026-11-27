# Changelog

## [2.0] — candidate

The owner reports an initial camera test on Nikon Z fc C 1.81 with no issues observed. The local candidate matches the declared SHA-256. The reports record a 34:32 ordinary recording and a 10-minute slow-motion recording. The longer menu settings remain outside the recorded test durations.

See [README](README.md) for the evidence scope and [release review checklist](RELEASE-CHECKLIST.md) for outstanding items.

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
