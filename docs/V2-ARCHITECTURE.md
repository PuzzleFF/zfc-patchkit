# zfc-patchkit v2.0 Architecture & Usage Guide

`zfc-v2` (`patches/zfc-v2.json`, output SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`,
`35,060,342` bytes, CRC16 residue `0x0000`) extends the Nikon Z fc C 1.81 `eg` module
using appended Thumb-2 code-cave blocks (`+38,652` B) and 135 guarded native hook/table
windows.

## SD Card Layout

All user configuration and custom audio assets live on the SD card (`A:\`):

| Path on SD Card | Purpose | Format |
|---|---|---|
| `A:\ZFCEXT.CFG` | Unified settings file (Aspect Ratio + Photo Zebra + Shutter Sound) | Auto-created by camera (32 B `'ZFE1'` v1 + CRC32) |
| `A:\ZFC\SHUTTER.WAV` | Custom shutter sound — Slot 1 | Uncompressed PCM WAV, 8 kHz 16-bit mono, <= 17,280 B (~1.08 s) |
| `A:\ZFC\1.WAV` .. `4.WAV` | Custom shutter sound — Slots 2..5 | Same PCM WAV format |

> Tip: Converting any shutter clip with `ffmpeg`:
> ```bash
> ffmpeg -i input.wav -ar 8000 -ac 1 -sample_fmt s16 -t 1.05 SHUTTER.WAV
> ```

## Key Technical Subsystems

1. **Video Suite (`unlock2` + `slowmo25` + `qs8`)**
   - Unlocks the 30-minute recording cap (`0x1029E088` engine gate + 84 duration table entries at `0x116DB8A4..0x116DBA60` -> `7,500,000` ms / 125 min).
   - Raises slow-motion cap (`0x102A0470`) from 3 min to 25 min.
   - Enables the hidden Movie Quality menu (Page 205 + condition `0x49`) and redirects `0x103544C4` to `qmenu_rates` so 4K and 1080p MP4 offer selectable **Normal** (4K 72/60 Mbps) and **High** (4K 144/120 Mbps) bitrates.
2. **Unified Setup Menu & Independent Photo Zebra**
   - Appends one entry at the bottom of Setup Menu Page 394 (`36 -> 37` rows) leading to a unified hub (`Pages 964 / 962 / 961 / 963`) with cold-boot text style lazy initialization (`style_tbl[2] = 0x02642413`).
   - Dual zebra hooks (`0x101765DA`, `0x10176706`) gate Photo mode (`r5 == 0`) on the custom toggle while keeping Movie-mode zebra 100% stock.
3. **Silent-Mode Custom Shutter Sound**
   - Hooks the silent-shutter audio dispatch path (`0x100725C4` with Thumb-aligned `A_ARG = 0x04190004`, `0x1006BE18`, `0x1006BE54`), pre-loads the selected WAV slot, and auto-previews when switching slots in the menu.
4. **Custom Aspect Ratio Suite + EVF Burst Speedup + Movie Auto-Hide**
   - Adds `2.35:1`, `1.85:1`, `4:3`, `2:1`, and `65:24 XPAN` (removes `5:4`; all 8 items fit on Page 1).
   - Repairs JPEG/EXIF metadata and no-reboot playback zoom (Site A `0x1033FF50` + Site B `0x102B0850`).
   - Draws pure-black Live View masks on both LCD (`0xD0959600`) and EVF (`0xD045F200`, preserving all non-zero-alpha EVF UI pixels) using 4-pixel `ldmia`/`stmia` bursts + 32:1 steady-state EVF throttle (~1 s switch).
   - Automatically retires the Photo mask when switching to Movie mode (`EXT_IS_MOVIE` published by `0x101765DA`/`0x10176706`) and restores it immediately on return to Photo mode.
5. **Cold-Boot Auto-Restore**
   - One-shot `ext_boot_restore` runs on the GUI task (`0x104B4E0A`) with a re-entry guard and 4-retry SD mount cap so Aspect Ratio, Photo Zebra, and Custom Shutter Sound all work immediately on power-on without opening any menu.

## Known Unverified Bounds (Honest Disclosures)
- `125 min` recording was hardware-verified to `34:32` / `3.1 GB`; the `4 GiB` boundary (~47:34) and 4K long-recording segment math have not been run to completion.
- Slow-motion `25 min` was hardware-verified to `10 min` (full 25 min run untested).
- Movie Quality (`qs8`) was verified in MP4 (MOV untested); unlocking Page 205 globally may expose stock-hidden options in some modes.
- No hardware/USB brick recovery path exists on Z fc; always flash with battery >= 50% and keep the stock rollback image (`build/verify/stock/EG198581.BIN`) handy.
