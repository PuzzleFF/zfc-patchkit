# Changelog

## [2.0] - 2026-11-27

Major release (`zfc-v2`, hardware-verified on a physical Nikon Z fc running C 1.81,
SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`).
Introduces appended code-cave (`CAPACITY`-style) extensions while keeping all v1
equal-length specs and pure-Python stdlib tooling intact.

### Added
- **125-minute video recording unlock** (`unlock2`) — 84 duration-table entries
  (`0x116DB8A4..0x116DBA60`, `1,799,000` -> `7,500,000` ms) + 1 engine-gate literal
  (`0x1029E088`). Verified on hardware to 34:32 / 3.1 GB (menu displays `125:00`;
  4 GiB boundary & 4K long-recording segment math remain untested).
- **Movie Quality menu unlock + 4K / 1080p adjustable bitrate (`qs8`)** — unlocks
  Movie Quality page 205 + condition `0x49` and hooks `0x103544C4` (`qmenu_rates`):
  4K Normal `72/60 Mbps` vs 4K High `144/120 Mbps`, 1080p Normal vs High selectable
  in-camera (verified on 5 MP4 modes; MOV untested).
- **Unified Setup Menu entry + Independent Photo Zebra** — appends a single custom
  entry to Setup Menu Page 394 (`36 -> 37` rows) with cold-boot text rendering
  (`style_tbl[2]` lazy initialization) and an independent Photo-mode highlight display
  toggle that leaves Movie-mode zebra 100% stock.
- **Silent-mode Custom Shutter Sound** — 5 fixed WAV slots in `A:\ZFC\`
  (`SHUTTER.WAV`, `1.WAV`..`4.WAV`, max 17,280 B / ~1.08 s @ 8 kHz 16-bit mono) with
  automatic preview playback on menu selection.
- **Complete Custom Aspect Ratio suite + EVF Burst Speedup + Movie Auto-Hide** —
  adds `2.35:1`, `1.85:1`, `4:3`, `2:1`, and `65:24 XPAN` (removes `5:4`, all 8 items
  on Page 1), pure-black Live View masks on both LCD (`0xD0959600`) and EVF
  (`0xD045F200`) with EVF UI intact, 4-pixel `ldmia`/`stmia` EVF burst speedup (~1 s
  LCD/EVF switch), no-reboot playback zoom fix (Site A + Site B), and automatic mask
  hide when switching to Movie mode.
- **Single unified config file (`A:\ZFCEXT.CFG`) + Cold-boot Auto-Restore** — stores
  Aspect Ratio, Photo Zebra, and Custom Shutter Sound in one 32 B CRC32-protected file
  and restores all settings automatically on power-on without opening any menu.
- `tools/patch.py` extended to support both v1 equal-length specs and v2 code-cave
  specs (`append_hex` + `append_sha256` verification) with zero external dependencies.
- `docs/V2-ARCHITECTURE.md` documenting the v2.0 architecture, SD card layout, and
  verified boundaries.

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
- The 30-minute recording limit was solved in v2.0 (`unlock2` engine gate at `0x1029E088`).
