# Nikon Z fc 固件补丁包 / Nikon Z fc Patchkit

[简体中文](#简体中文) · [English](#english)

---

# 简体中文

**`v2.0`（`zfc-v2` / 研究代号 `zfc_all1b`）是 Nikon Z fc（C 1.81，EXPEED 6）的正式发布版本。**

路线：基于用户自行提供的官方 `Z_fc_0181.bin` 提取主模块 `eg` → 应用补丁与扩展配方 → 重算模块 CRC16 → 命名 `EG198581.BIN` → 放 SD 卡根目录 → 相机「设定菜单 → 固件版本 → 版本升级」。**纯 Python 标准库，零第三方依赖。**

> 本仓库**不包含任何完整的尼康固件镜像**。官方升级文件请自行从尼康官网获取，脚本会严格校验其 SHA-256。  
> **关于 `patches/zfc-v2.json` 的内嵌范围说明**：48 处目标窗口校验全部使用 `expected_sha256`（不含原厂 `expected` 字节），扩展区中 239 段 ≥12 B 原厂菜单/画幅表及原指令段（9,433 B）在构建时通过 `copy_stock` 从用户本地固件读取；剩余 213 条直接写入记录（`write`）与 48 条替换记录（`replacement`）的来源台账与维护者确认记录见 [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md)。本仓库 MIT 许可仅覆盖项目原创代码与文档，不授予任何 Nikon 固件、资源或商标权利。

## v2.0 更新内容

相比 `v1`（仅含慢动作 25 分钟、1080p 码率提升与复用视频开关的拍照斑马纹），**`v2.0`（`zfc-v2`）是一次完整大版本升级**：

1. **完整自定义画幅套件 + EVF 加速 + 视频档自动隐藏**：新增 `2.35:1`、`1.85:1`、`4:3`、`2:1`、`65:24 XPAN`（移除 `5:4`，全部 8 项单页显示）；LCD + EVF 双屏纯黑实时取景遮罩（保留 EVF UI，4 像素 `ldmia`/`stmia` 突发加速切换约 1 秒）；免重启回放 1/2/3 级放大修复；**切到视频档自动隐藏遮罩，切回拍照档立刻恢复**。
2. **设定菜单底部统一扩展入口 + 独立拍照斑马纹**：冷启动直显文字，拍照模式高亮显示（斑马纹）与视频模式斑马纹完全独立。
3. **静音模式自定义快门声**：支持 5 个固定 WAV 槽位（`ZFC\SHUTTER.WAV`、`1.WAV`~`4.WAV`），菜单选中即自动试听。
4. **全项目单一配置文件 + 开机自动恢复**：画幅、拍照斑马纹、自定义快门声统一保存于 `A:\ZFCEXT.CFG`，开机自动恢复，无需先进菜单。
5. **视频功能整合**：125 分钟视频录制时长解锁（`unlock2`，不含慢动作）、慢动作 3 → 25 分钟（`slowmo25`）、视频品质菜单解锁 + 4K / 1080p 可调码率（`qs8`）。
6. **纯 Python 配方补丁器**：`tools/patch.py` 新增 `expected_sha256` 校验与 `append_recipe`（`copy_stock` + `write`），继续完整兼容全部 `v1` 等长补丁。

## 适用与版本标识

| 项 | 值 |
|---|---|
| 机型 / 固件 | Nikon Z fc · C 1.81（官方容器 `Z_fc_0181.bin`，35,578,974 B，SHA-256 `e4cd838a…bd1b6`） |
| 当前正式版 | **`v2.0`（`zfc-v2` / `zfc_all1b`）**，目标大小 `35,060,342` B，SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8` |
| 上一版本 | `v1`（`zfc-v1`，SHA-256 `2c9cc3a9…ec161`），仓库继续保留全部 v1 规格 |

## 实测范围与未测边界

- **机主在 `zfc_all1b` 上已实机确认**：开关机、拍照、自定义画幅遮罩（含切到视频档自动隐藏 / 切回拍照档恢复）、统一设定菜单入口、独立拍照斑马纹、自定义快门声、开机配置自恢复、以及短时间录像均未报告异常；机主亦补充确认早期 `extsnd1` / `extboot1` 的自定义快门声已实机测试。
- **在 `zfc_all1b` 上未测试的项目**：**超过 30 分钟的长录像**、**不同视频画质档位的码率实测**。

| 功能 | v2.0 行为 | 实测归因与未测边界 |
|---|---|---|
| **125 分钟视频解锁** | 菜单时长上限设为 `125:00`（84 项时长表 + 引擎门限 `0x1029E088`） | `zfc_all1b` 仅测短录像，**未测超过 30 分钟录像**。历史汇总报告记录了普通录像 `34:32` / `3.1 GB`，所测镜像尚未确认（见 `zfc-research@e77cb5c` 与 `CFW@b6d4d04`）；`125` 分钟满程、`4 GiB` 边界与 `4K` 长录均未验证 |
| **慢动作上限 3 → 25 分钟** | 菜单时长上限设为 `25:00`（`0x102A0470`） | 更早的 `10` 分钟录像记录来自 `slowmo25`（`zfc-patchkit@10d619b:CHANGELOG.md`、`docs/MILESTONE-2026-10-25.md`）；`25` 分钟满程未验证 |
| **4K / 1080p 品质与码率菜单** | 解锁视频品质菜单（高 / 标准）+ `qmenu_rates` | **`zfc_all1b` 未测不同画质档位的码率**。历史汇总报告记录了 5 种 MP4 模式，所测镜像尚未确认；MOV 未测 |
| **自定义画幅套件 + EVF 加速 + 视频档自动隐藏** | 新增 5 档画幅（去 5:4，单页 8 项）、LCD/EVF 纯黑遮罩（保留 EVF UI、4 像素突发加速）、免重启回放放大、视频档自动隐藏遮罩 | 机主在 `zfc_all1b` 上实测拍照、画幅遮罩及**切到视频档自动隐藏 / 切回拍照档恢复**未报告异常 |
| **静音模式自定义快门声** | 5 个固定 WAV 槽位（选中自动试听） | 机主在 `zfc_all1b` 上实测自定义快门声未报告异常，并确认早期 `extsnd1` / `extboot1` 已实机测试（早期逐项原始日志未归档） |
| **统一设定菜单入口 + 独立拍照斑马纹** | 设定菜单底部扩展入口（冷启动直显文字）+ 独立拍照斑马纹 | 机主确认在 `zfc_all1b` 上实机测试通过 |
| **单文件配置与开机自恢复** | 统一保存于 `A:\ZFCEXT.CFG`，开机自动恢复 | 机主确认在 `zfc_all1b` 上单独实机测试开机配置自恢复通过 |

## 快速开始

```bash
# 1) 放好官方固件 Z_fc_0181.bin（sha256 = e4cd838a215c113659416983b31dbdba8896591caacf7309170d4cc3c60bd1b6）
# 2) 本地复现全部镜像并核对 pins.json 声明的 SHA-256
python tools/verify_release.py --firmware Z_fc_0181.bin

# 3) 或单独构建 v2.0 正式版
python tools/patch.py --input Z_fc_0181.bin --spec patches/zfc-v2.json \
                      --output out/EG198581.BIN --report out/report.json
```

### 自定义快门声 WAV 文件要求

- **存放路径与文件名**（SD 卡根目录 `ZFC` 文件夹，最多 5 个槽位）：
  - 槽位 1：`ZFC\SHUTTER.WAV`
  - 槽位 2~5：`ZFC\1.WAV`、`ZFC\2.WAV`、`ZFC\3.WAV`、`ZFC\4.WAV`
- **音频格式要求**（不满足条件的文件会被跳过）：
  - 格式：**未压缩 PCM WAV**（RIFF/WAVE，`pcm_s16le`）
  - 采样率：**8,000 Hz（8 kHz）** · 位深：**16-bit** · 声道：**单声道（Mono，1 ch）**
  - 时长 / 大小：PCM 数据区 **≤ 17,280 字节（约 1.08 秒）**，建议裁剪在 **1.0 秒以内**
- **使用 `ffmpeg` 转换示例**：
  ```bash
  ffmpeg -i input.wav -ar 8000 -ac 1 -c:a pcm_s16le -t 1.0 SHUTTER.WAV
  ```
- **使用方式**：在「设定菜单 → 静音拍摄」开启静音模式，并在「设定菜单 → 扩展功能 → 自定义快门声」启用并选择槽位（选中自动试听）。请仅使用你有权使用的音频文件。

## 验证记录与回退边界

- **验证记录**：`a199576` 的作者本地 `verify_release.py` 7/7 复现日志归档于 [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md)（作者本地报告）；既有离线门禁报告记录 0 项违规、27 项 2 字节零填充警告（仅归属该旧报告）。`a199576` 的第三方独立验证暂延后。
- **回退观察与救援边界**：在相机**能够正常开机、电池电量充足（≥ 50%）且能够正常进入「设定菜单 → 固件版本 → 版本升级」**的条件下，先前测试观察到可通过 SD 卡重刷原厂 `EG198581.BIN` 回退。原厂镜像的存在**不能保证一定能够回退成功**；**如果相机无法启动或无法进入升级菜单，目前缺少可靠的 USB 或硬件救援证据**（USB 协议栈位于被替换的 `eg` 模块内）。升级过程中切勿断电或中断。

## 参考与致谢

本项目在扩展方法、菜单与遮罩思路上参考了 [Wonder Lantern（Nikon Z30）](https://github.com/WonderLantern/wonder-lantern-z30)，同时参考了 [NikonUnlock](https://github.com/summershrimp/NikonUnlock) 与 [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools)。完整来源台账详见 [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md)。

---

# English

**`v2.0` (`zfc-v2` / research build `zfc_all1b`) is the official v2.0 release for Nikon Z fc (firmware C 1.81, EXPEED 6).**

Pure Python standard library (zero third-party dependencies). Patch `eg` from your own official `Z_fc_0181.bin`, recompute CRC16, copy `EG198581.BIN` to SD card root, and install via *Setup → Firmware version → Update*.

> This repository ships **no complete Nikon firmware image**. Obtain the official `Z_fc_0181.bin` yourself; the scripts verify its SHA-256 before building. In `patches/zfc-v2.json`, all 48 target checks use `expected_sha256` and 239 contiguous runs >= 12 B (9,433 B) of stock data are read locally via `copy_stock`. See [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md) for the full provenance ledger. The MIT license covers only original project code and documentation and grants no rights to Nikon firmware, resources, or trademarks.

## What's New in v2.0 (`zfc-v2`)

1. **Complete Custom Aspect Ratio Suite + EVF Burst Speedup + Movie Auto-Hide**: adds `2.35:1`, `1.85:1`, `4:3`, `2:1`, `65:24 XPAN` (removes `5:4`, all 8 items on Page 1); pure-black LCD + EVF masks (EVF UI preserved, 4-pixel `ldmia`/`stmia` burst speedup ~1 s switch); no-reboot playback zoom fix; **auto-hides in Movie mode and restores in Photo mode**.
2. **Unified Setup Menu Entry + Independent Photo Zebra**: cold-boot text rendering; Photo-mode highlight display is fully independent of Movie zebra.
3. **Silent-Mode Custom Shutter Sound**: 5 fixed WAV slots (`ZFC\SHUTTER.WAV`, `1.WAV`..`4.WAV`) with auto-preview on select.
4. **Unified Config (`A:\ZFCEXT.CFG`) + Cold-Boot Auto-Restore**: stores Aspect Ratio, Photo Zebra, and Shutter Sound in one file and restores automatically on power-on.
5. **Video Suite**: 125-minute recording unlock (`unlock2`), 3 → 25 min slow-motion (`slowmo25`), and Movie Quality menu + 4K/1080p adjustable bitrate (`qs8`).
6. **Pure-Python Recipe Patcher**: `tools/patch.py` adds `expected_sha256` and `append_recipe` (`copy_stock` + `write`) while keeping all v1 equal-length specs compatible.

## Test Scope & Boundaries

- **Owner confirmed on `zfc_all1b`**: power cycling, still photography, custom aspect-ratio masks (including Movie-mode auto-hide / Photo-mode restore), unified Setup menu, independent photo zebra, custom shutter sound, cold-boot config auto-restore, and short video clips reported no issues (owner also confirmed custom shutter sound on earlier `extsnd1` / `extboot1`).
- **Untested on `zfc_all1b`**: recordings > 30 minutes and bitrate measurements across quality modes.
- **Historical video measurements**: `10`-minute slow-motion documented for `slowmo25` (`zfc-patchkit@10d619b:CHANGELOG.md`); historical summaries report `34:32` / `3.1 GB` and 5 MP4 quality modes (specific test images unconfirmed). Full 125 min, 4 GiB boundary, long 4K, full 25 min slow-motion, and MOV remain untested.

## Quick start

```bash
python tools/verify_release.py --firmware Z_fc_0181.bin
python tools/patch.py --input Z_fc_0181.bin --spec patches/zfc-v2.json \
                      --output out/EG198581.BIN --report out/report.json
```

### Custom Shutter Sound WAV Requirements

- **SD card paths** (`ZFC\` in SD card root, 5 fixed slots): `ZFC\SHUTTER.WAV`, `ZFC\1.WAV` .. `ZFC\4.WAV`.
- **Format**: uncompressed PCM WAV (`pcm_s16le`), **8,000 Hz**, **16-bit**, **Mono**, PCM payload **<= 17,280 bytes (~1.08 s)** (`<= 1.0 s` recommended).
- **Conversion**: `ffmpeg -i input.wav -ar 8000 -ac 1 -c:a pcm_s16le -t 1.0 SHUTTER.WAV`
- Use only audio you have rights to use.

## Verification & Rollback Boundaries

- **Verification**: Author local `verify_release.py` log for `a199576` is archived at [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md) (7/7 MATCH, target `b5c6e75e…61f8`); saved offline gate report recorded 0 violations and 27 two-byte zero-padding warnings. Independent third-party verification is deferred.
- **Rollback limits**: Re-flashing stock `EG198581.BIN` has been observed to work **only when the camera boots normally and can enter the firmware update menu** (battery >= 50%). Having a stock file does **not** guarantee recovery; **there is no reliable recovery evidence if the camera fails to boot or cannot open the update menu**.

## Credits & License

Inspired by [Wonder Lantern (Nikon Z30)](https://github.com/WonderLantern/wonder-lantern-z30); also referencing [NikonUnlock](https://github.com/summershrimp/NikonUnlock) and [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools). See [LICENSE](LICENSE), [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md), [docs/V2-ARCHITECTURE.md](docs/V2-ARCHITECTURE.md), and [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md).
