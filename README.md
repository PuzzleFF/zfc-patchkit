# Nikon Z fc 固件补丁包 / Nikon Z fc Patchkit

[简体中文](#简体中文) · [English](#english)

---

# 简体中文

**v2.0 目前是 Nikon Z fc（C 1.81，EXPEED 6）的候选版本（candidate），用于公开审查。GitHub 上的正式 Release 仍以 Releases 页面为准（当前为 v1）。**

路线：基于用户自行提供的官方 `Z_fc_0181.bin` 提取主模块 `eg` → 应用补丁与扩展配方 → 重算模块 CRC16 → 命名 `EG198581.BIN` → 放 SD 卡根目录 → 相机「设定菜单 → 固件版本 → 版本升级」。

> 本仓库**不包含任何完整的尼康固件镜像**。官方升级文件请自行从尼康官网获取，脚本会严格校验其 SHA-256。  
> **关于 `patches/zfc-v2.json` 的内嵌范围限定**：在提交 `a199576` 中，48 处目标窗口校验已改为 `expected_sha256`（不再内嵌原厂 `expected` 字节），且扩展区中 239 段（9,433 B，≥12 B 连续段）原厂菜单/画幅表及原指令数据已改为构建时通过 `copy_stock` 从用户本地固件读取；但**剩余 213 条直接写入记录（`write`）与 48 条替换记录（`replacement`）的来源尚未全部完成核验**（原厂派生表与短原指令重放中仍可能残留 `<12 B` 原厂片段），详见 [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md)。本仓库 MIT 许可仅覆盖项目原创代码与文档，不授予任何 Nikon 固件、资源或商标权利。

## 适用与版本状态

| 项 | 值 |
|---|---|
| 机型 / 固件 | Nikon Z fc · C 1.81（官方容器 `Z_fc_0181.bin`，35,578,974 B，SHA-256 `e4cd838a…bd1b6`） |
| 正式 Release（GitHub） | `v1`（`zfc-v1`）— 正式发布状态以 GitHub Releases 页面为准 |
| 当前分支候选版 | **`v2.0 候选版`（`zfc-v2` / 研究代号 `zfc_all1b`）**，声明目标大小为 `35,060,342` B、目标 SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8` |

## v2.0 候选版功能范围与实测边界

### 1. 机主在 `zfc_all1b` 上的初测范围
- 机主确认已刷入并实测 **`zfc_all1b`**（主要测试拍照场景）：**开关机、拍照、自定义画幅遮罩（含视频档自动隐藏 / 切回拍照档恢复）、自定义快门声、以及短录像未报告异常**。
- **在 `zfc_all1b` 上未测试的项目**：**超过 30 分钟的长录像**、**不同视频画质档位的码率实测**。

### 2. 各模块功能与历史实测来源对照

| 功能 | 候选版声明行为 | 历史来源报告与未测边界 |
|---|---|---|
| **125 分钟视频解锁** | 菜单时长上限设为 `125:00`（84 项时长表 + 引擎门限 `0x1029E088`） | 更早的录像结果来自早期单功能/组件版本（`unlock2` / `VIDEO1` 研究记录）：记录到普通录像 `34:32` / `3.1 GB`。`zfc_all1b` 未测 >30 分钟录像；`125` 分钟满程、`4 GiB` 边界与 `4K` 长录均未验证 |
| **慢动作上限 3 → 25 分钟** | 菜单时长上限设为 `25:00`（`0x102A0470`） | 更早的录像结果来自 `slowmo25`（v1 / `VIDEO1` 研究记录）：记录到 `10` 分钟正常。`25` 分钟满程未验证 |
| **4K / 1080p 品质与码率菜单** | 解锁视频品质菜单（高 / 标准）+ `qmenu_rates`（4K 高/标准、1080p 高/标准可选） | 更早的码率结果来自 `qs8` 组件研究记录（覆盖 5 种 MP4 模式）。`zfc_all1b` 未测不同画质码率；MOV 未测 |
| **统一设定菜单入口 + 独立拍照斑马纹** | 设定菜单底部扩展入口（冷启动直显文字）+ 独立拍照斑马纹 | 机主在 `extmenu1b` / `extsnd1` / `extboot1` / `zfc_all1b` 上初测未报告异常；仍需逐项归档独立测试记录 |
| **静音模式自定义快门声** | 5 个固定 WAV 槽位（选中自动试听） | 机主在 `extsnd1` / `extboot1` / `zfc_all1b` 上初测未报告异常 |
| **自定义画幅套件 + EVF 加速 + 视频档隐藏** | 新增 5 档画幅（去 5:4，单页 8 项）、LCD/EVF 纯黑遮罩（保留 EVF UI、4 像素突发加速）、免重启回放放大修复、视频档自动隐藏遮罩 | 机主在 `zfc_all1b` 上初测拍照、遮罩与视频档切换未报告异常 |
| **单文件配置 + 开机自恢复** | 统一保存于 `A:\ZFCEXT.CFG`，开机自动恢复 | 机主在 `extboot1` / `zfc_all1b` 上初测开关机未报告异常；未覆盖全部显示模式与无卡/慢挂载边界 |

## 快速开始

```bash
# 1) 放好官方固件 Z_fc_0181.bin（sha256 = e4cd838a215c113659416983b31dbdba8896591caacf7309170d4cc3c60bd1b6）
# 2) 本地复现全部镜像并核对 pins.json 声明的 SHA-256
python tools/verify_release.py --firmware Z_fc_0181.bin

# 3) 或单独构建 v2.0 候选版
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

## 验证记录与审查状态

- **已有旧离线报告**：早期研究仓库与本地构建保存了 `zfc_all1b` 的离线检查报告（`gate_zfc_all1b_final` 记录 0 项违规、27 项警告——经复核全部 27 项均为 2 字节零填充提示，仅归属于该旧报告，不代表新的运行时验证）。
- **当前提交 `a199576`**：作者本地执行 `verify_release.py` 的复现日志已归档于 [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md)（**作者本地报告**，7/7 匹配声明目标 SHA-256 `b5c6e75e…61f8`）；**当前提交尚缺少独立第三方复现与独立审查验证记录（状态：待验证）**。详见 [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) 与 [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md)。

## 回退观察与救援边界

- **已有回退观察**：在相机**能够正常开机、电池电量充足且能够正常进入「设定菜单 → 固件版本 → 版本升级」**的条件下，先前测试中观察到可以通过 SD 卡重刷原厂 `EG198581.BIN` 回到原厂固件。
- **重要限制（不构成恢复保证）**：原厂镜像的存在**不能保证一定能够回退成功**。**如果相机无法启动或无法进入升级菜单，目前缺少可靠的 USB 或硬件救援证据**（USB 协议栈本身位于被替换的 `eg` 模块内）。请务必满电（≥ 50%）操作、升级过程中切勿断电或中断。

## 参考与致谢

相关研究参考：[Wonder Lantern（Nikon Z30）](https://github.com/WonderLantern/wonder-lantern-z30)、[NikonUnlock](https://github.com/summershrimp/NikonUnlock)、[nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools)。内嵌字节的来源与授权审查状态详见 [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md)。

---

# English

**v2.0 is currently a project candidate for Nikon Z fc (firmware C 1.81, EXPEED 6) open for review. Formal release status is governed by GitHub Releases (currently v1).**

> This repository ships **no complete Nikon firmware image**. Obtain the official `Z_fc_0181.bin` yourself; the scripts verify its SHA-256 before building.  
> **Scope limit on `patches/zfc-v2.json`**: In commit `a199576`, all 48 target-window checks use `expected_sha256` (no raw stock `expected` bytes), and 239 contiguous runs >= 12 B (9,433 B) of stock menu/profile data are read locally from the user's firmware via `copy_stock`. However, **provenance for all remaining 213 `write` records and 48 `replacement` records is not yet fully closed** (`<12 B` stock fragments may still exist inside stock-derived table gaps). See [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md). The repository's MIT license covers only original project code and documentation and grants no rights to Nikon firmware, resources, or trademarks.

## Owner Initial Test Scope & Earlier Video Reports

- **Owner initial test on `zfc_all1b`** (photo-focused): power cycling, still photography, custom aspect-ratio masks (including Movie-mode auto-hide / Photo-mode restore), custom shutter sound, and short video clips reported no issues.
- **Untested on `zfc_all1b`**: recordings longer than 30 minutes and bitrate measurements across different quality levels.
- **Earlier video measurements (separate earlier builds)**: the `34:32` / `3.1 GB` recording (`unlock2` / `VIDEO1`), `10`-minute slow-motion clip (`slowmo25`), and 5 MP4 quality modes (`qs8`) belong to earlier component/video research builds, not full-duration runs on `zfc_all1b`. Full 125 min, 4 GiB boundary, long 4K recording, full 25 min slow-motion, and MOV remain untested.

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

- **Saved offline reports vs current commit**: The previously reviewed offline gate report for `zfc_all1b` recorded 0 violations and 27 warnings (all 27 classified as 2-byte zero-padding entries in that saved report only). The author's local `verify_release.py` log on `a199576` is archived in [docs/V2-LOCAL-VERIFY-a199576.md](docs/V2-LOCAL-VERIFY-a199576.md) (author local report); **independent verification of commit `a199576` is pending (`待验证`)**.
- **Rollback observations & limits**: Re-flashing stock `EG198581.BIN` has been observed to work **only when the camera boots normally and can enter the firmware update menu** (battery >= 50%). Having a stock file does **not** guarantee recovery; **there is no reliable recovery evidence if the camera fails to boot or cannot open the update menu**.

## Credits & License

References: [Wonder Lantern (Nikon Z30)](https://github.com/WonderLantern/wonder-lantern-z30), [NikonUnlock](https://github.com/summershrimp/NikonUnlock), [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools). See [LICENSE](LICENSE), [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md), [docs/V2-ARCHITECTURE.md](docs/V2-ARCHITECTURE.md), and [docs/V2-PROVENANCE.md](docs/V2-PROVENANCE.md).
