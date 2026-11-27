# Nikon Z fc 固件补丁包 / Nikon Z fc Patchkit

[简体中文](#简体中文) · [English](#english)

---

# 简体中文

给 Nikon Z fc（C 1.81，EXPEED 6）做**自制固件功能扩展与补丁**的工具集与已实机验证规格。

**路线只有一条**：基于官方固件提取主模块 `eg` → 打补丁/追加代码 → 重算模块 CRC16 → 命名 `EG198581.BIN` → 放 SD 卡根目录 → 相机「设定菜单 → 固件版本 → 版本升级」。
**不需要 K8、不需要重新签名整包、不需要服务模式、不需要任何第三方 Python 依赖库。**

> 这个仓库**不包含任何尼康固件**。官方升级文件请自行从尼康官网获取，脚本会严格校验它的 SHA-256。

## 适用与状态

| 项 | 值 |
|---|---|
| 机型 | Nikon Z fc |
| 固件 | C 1.81（容器 `Z_fc_0181.bin`，35,578,974 字节，sha256 `e4cd838a…bd1b6`） |
| 最新正式版 | **`zfc-v2`（v2.0 全功能版）** — SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`（35,060,342 字节） |
| 回滚 | ✅ 刷 `stock` 镜像即回到原厂（`cd47efc1…`） |

## v2.0 已实机验证功能（`zfc-v2` 七合一）

| 功能 | 说明 | 实机结果 |
|---|---|---|
| **125 分钟视频解锁** | 解锁 29:59 录制上限（84 项时长表 + 引擎门限 `0x1029E088`） | ✅ 菜单显示 `125:00`，实录 34:32 / 3.1 GB 通过（4 GiB 与 4K 长录边界未测满） |
| **慢动作上限 3 → 25 分钟** | `0x102A0470`（`180000` → `1500000` ms） | ✅ 菜单显示 `25:00`，实录 10 分钟正常（25 分钟满程未测） |
| **4K / 1080p 品质菜单与可调码率** | 解锁视频品质菜单（高 / 标准）+ `qmenu_rates`（4K 高 144/120 Mbps、标准 72/60 Mbps；1080p 高/标准可选） | ✅ MP4 五模式实测通过（MOV 未测） |
| **统一设定菜单入口 + 独立拍照斑马纹** | 设定菜单底部新增统一扩展入口（冷启动直显文字），拍照斑马纹与视频斑马纹完全独立 | ✅ 实机通过 |
| **静音模式自定义快门声** | 5 个固定 WAV 槽位（`A:\ZFC\SHUTTER.WAV`、`1.WAV`~`4.WAV`，8 kHz 16-bit 单声道，≤1.08 秒），菜单选中自动试听 | ✅ 实机通过 |
| **完整自定义画幅套件** | 新增 `2.35:1` / `1.85:1` / `4:3` / `2:1` / `65:24 XPAN`（去 5:4，单页 8 项）；LCD+EVF 双屏纯黑实时取景遮罩（保留 EVF UI、4 像素突发加速切换约 1 秒）；免重启回放 1/2/3 级放大修复；**视频档自动隐藏遮罩、切回拍照档立刻恢复** | ✅ 实机全面通过 |
| **单文件持久化 + 开机即生效** | 画幅、拍照斑马纹、自定义快门声统一保存于 `A:\ZFCEXT.CFG`，**开机自动恢复，无需进任何菜单** | ✅ 实机通过 |

> 保留全部 v1 等长补丁（`stock`、`slowmo25`、`bitrate-a`、`bitrate-b`、`zebra-photo`、`zfc-v1`），随时可按需构建。

## 快速开始

```bash
# 1) 放好官方固件 Z_fc_0181.bin（同名或 --firmware 指定）
#    sha256 = e4cd838a215c113659416983b31dbdba8896591caacf7309170d4cc3c60bd1b6

# 2) 一键复现全部镜像（含 stock、v1、zfc-v2）并逐一校验 SHA-256
python tools/verify_release.py --firmware Z_fc_0181.bin

# 3) 或单独构建 v2.0 全功能版
python tools/patch.py --input Z_fc_0181.bin --spec patches/zfc-v2.json \
                      --output out/EG198581.BIN --report out/report.json
```

自定义快门声使用方法与架构详见 [docs/V2-ARCHITECTURE.md](docs/V2-ARCHITECTURE.md)。

## 参考与致谢

本项目的核心方法（独立 EG 模块安装路径、`CAPACITY` 代码停放、`ldr.w pc` 跳板、SD 卡配置持久化等）深受 [Wonder Lantern（Nikon Z30 固件扩展项目）](https://github.com/WonderLantern/wonder-lantern-z30) 启发。Z fc 与 Z30 同属 EXPEED 6 平台，但函数地址与结构体布局均存在差异，本仓库中 Z fc 的全部地址、表格、门控与实机结果均为独立逆向定位并实测验证。

其他参考：[NikonUnlock](https://github.com/summershrimp/NikonUnlock)、[nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools)。

## 免责声明

改固件有风险。**升级过程中断电可能导致相机无法开机**，且本机型没有已知的 USB 救援路径。请确保电量 ≥ 50%、切勿中断升级。本工具与作者不对任何设备损坏、保修失效或数据丢失负责。仅供研究与个人使用。

---

# English

Pure-Python (zero external dependencies) tools and **camera-verified** firmware patches for the Nikon Z fc (firmware C 1.81, EXPEED 6).

One installation route only: patch the `eg` module from your own official `Z_fc_0181.bin` → recompute its CRC16 → copy `EG198581.BIN` to the SD card root → *Setup → Firmware version → Update*. No K8, no full-package re-signing, no service mode.

> This repository ships **no Nikon firmware**. Obtain the official update yourself; the scripts verify its SHA-256 before doing anything.

## v2.0 Camera-Verified Features (`zfc-v2`)

- **125-minute video unlock** (`unlock2`: verified to 34:32 / 3.1 GB; 4 GiB & 4K long-recording bounds untested)
- **Slow-motion 3 → 25 min** (`slowmo25`: verified to 10 min; full 25 min untested)
- **Movie Quality menu + 4K / 1080p adjustable bitrate** (`qs8`: 4K Normal 72/60 Mbps vs High 144/120 Mbps, 1080p Normal/High; verified in MP4)
- **Unified Setup Menu entry + Independent Photo Zebra** (cold-boot text rendering; Movie zebra stays 100% stock)
- **Silent-mode Custom Shutter Sound** (5 WAV slots in `A:\ZFC\SHUTTER.WAV`, `1.WAV..4.WAV`, auto-preview on select)
- **Complete Custom Aspect Ratio suite** (`2.35:1`, `1.85:1`, `4:3`, `2:1`, `65:24 XPAN`; `5:4` removed, 8 items on Page 1; pure-black LCD + EVF masks with EVF UI preserved & 4-pixel burst speedup; no-reboot playback zoom fix; automatic hide in Movie mode)
- **Single unified config (`A:\ZFCEXT.CFG`) + Cold-boot Auto-Restore** (works immediately on power-on without opening any menu)

All v1 equal-length specs (`stock`, `slowmo25`, `bitrate-a`, `bitrate-b`, `zebra-photo`, `zfc-v1`) remain supported.

## Quick start

```bash
python tools/verify_release.py --firmware Z_fc_0181.bin
python tools/patch.py --input Z_fc_0181.bin --spec patches/zfc-v2.json \
                      --output out/EG198581.BIN --report out/report.json
```

See [docs/V2-ARCHITECTURE.md](docs/V2-ARCHITECTURE.md) for SD card WAV format, architecture details, and honest verification boundaries.

## Credits & Disclaimer

Method inspired by [Wonder Lantern (Nikon Z30)](https://github.com/WonderLantern/wonder-lantern-z30); also referencing [NikonUnlock](https://github.com/summershrimp/NikonUnlock) and [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools). Every Z fc address, table, and verification result here was located and verified independently.

Firmware modification carries brick risk and Z fc has no known USB recovery path. Use >= 50% battery and do not interrupt updates. Research and personal use only.

## License

MIT — see `LICENSE`.
