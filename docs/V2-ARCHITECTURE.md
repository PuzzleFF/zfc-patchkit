# Nikon Z fc v2.0 候选版：功能范围、SD 卡格式与证据边界

- **候选版标识**：公开名 `zfc-v2`（研究代号 `zfc_all1b`），面向 Nikon Z fc C 1.81。
- **状态**：**v2.0 候选版（candidate）**；正式 Release 状态以 GitHub Releases 为准（当前正式版为 `v1`）。
- **配方提交**：`release/v2.0` @ `a1995765343359c69b6bf327068f660343e51851`（声明目标大小 `35,060,342` B，目标 SHA-256 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`）。

## 1. 功能范围与验证边界对照

| 领域 | 候选版行为 | 实测归因与审查边界 |
|---|---|---|
| **普通录像（125 分钟）** | 菜单上限 `125:00`（`unlock2`） | 机主在 `zfc_all1b` 上仅测短录像（未报告异常），**未测超过 30 分钟录像**。历史汇总报告记录了普通录像 `34:32` / `3.1 GB`，所测镜像尚未确认（总述见 `zfc-research@e77cb5c:notes/ZFC-V2-ARCHITECTURE-AND-RESULTS-2026-11-27.md` 与 `CFW@b6d4d04:research/nikon_zfc/snapshots/zfc-v2-20261127/README.md`，公开仓未附单组件原始日志）；125 分钟满程、4 GiB 边界与 4K 长录均未验证 |
| **慢动作（25 分钟）** | 菜单上限 `25:00`（`slowmo25`） | 更早的 `10` 分钟记录来自 `slowmo25`（固定出处：`zfc-patchkit@10d619b:CHANGELOG.md`、`docs/MILESTONE-2026-10-25.md`）；25 分钟满程未验证 |
| **视频品质与码率（`qs8`）** | 解锁品质菜单（高 / 标准）+ `qmenu_rates` | **`zfc_all1b` 未测不同画质档位的码率**。历史汇总报告记录了 5 种 MP4 模式，所测镜像尚未确认（总述见 `zfc-research@e77cb5c:notes/ZFC-V2-ARCHITECTURE-AND-RESULTS-2026-11-27.md`，公开仓未附单组件原始日志）；MOV 未测；全局解锁可能暴露原厂隐藏项 |
| **自定义画幅与遮罩** | 5 档新增画幅（去 5:4，单页 8 项）、LCD/EVF 纯黑遮罩（EVF UI 保留 + 4 像素突发加速）、免重启回放放大、视频档自动隐藏遮罩 | 机主在 `zfc_all1b` 上实测拍照、画幅遮罩及**切到视频档自动隐藏 / 切回拍照档恢复**未报告异常 |
| **静音模式自定义快门声** | 5 槽固定 WAV，选中自动试听 | 机主在 `zfc_all1b` 上实测自定义快门声未报告异常（限于机主测试环境）；早期 `extsnd1` / `extboot1` 缺少对应独立实机测试报告（该部分历史归因：**尚未确认**） |
| **扩展菜单与独立拍照斑马纹** | 设定菜单底部统一入口（冷启动直显文字）+ 独立拍照斑马纹 | **尚未确认**：`zfc_all1b` 本轮初测记录未单独涵盖这两项；早期 `extmenu1b` / `extsnd1` / `extboot1` 仅在 `zfc-research@e77cb5c:notes/ZFC-V2-ARCHITECTURE-AND-RESULTS-2026-11-27.md` 有总述，缺少独立实机测试报告文件 |
| **统一配置与开机自恢复** | 单文件 `A:\ZFCEXT.CFG`，冷启动自动恢复 | **尚未确认**：`zfc_all1b` 的「开关机正常」观察仅覆盖开关机本身，不等价于配置自恢复实测；`zfc-research@e77cb5c:notes/EXTBOOT1-REPORT.md` 为刷前离线报告（`camera_verified: false`），缺少 `extboot1` / `zfc_all1b` 的配置恢复独立实机报告 |

## 2. SD 卡目录与自定义快门声 WAV 要求

| SD 卡路径 | 用途 | 格式要求 |
|---|---|---|
| `A:\ZFCEXT.CFG` | 统一配置文件（画幅 + 拍照斑马纹 + 快门声） | 相机自动生成（32 B `'ZFE1'` v1 + CRC32） |
| `A:\ZFC\SHUTTER.WAV` | 自定义快门声 — 槽位 1 | 未压缩 PCM WAV（`pcm_s16le`），**8,000 Hz、16-bit、单声道**，PCM 数据 **≤ 17,280 B（~1.08 秒）** |
| `A:\ZFC\1.WAV` .. `4.WAV` | 自定义快门声 — 槽位 2~5 | 同上（建议 ≤ 1.0 秒） |

转换示例：
```bash
ffmpeg -i input.wav -ar 8000 -ac 1 -c:a pcm_s16le -t 1.0 SHUTTER.WAV
```

## 3. 验证记录与提交绑定

| 证据类别 | 对应提交 / 来源 | 状态 |
|---|---|---|
| 既有离线构建与门禁报告（`zfc_all1b`） | 私有 `zfc-research@e77cb5c`（`notes/ZFC-ALL1B-REPORT.md`）与本地 `zfc_all1b-finalbin-gate.json` | 已归档（记录 0 项违规、27 项警告——经复核全部 27 项均为 2 B 零填充提示，仅针对该旧报告） |
| 当前公开配方声明的目标哈希与作者本地复现 | `release/v2.0` @ `a199576`（`patches/zfc-v2.json`） | **作者本地报告**：[V2-LOCAL-VERIFY-a199576.md](V2-LOCAL-VERIFY-a199576.md)（7/7 匹配 `b5c6e75e…61f8`） |
| 当前提交 `a199576` 的独立复核与门禁验证 | `release/v2.0` @ `a199576` | **待验证** |

## 4. 回退观察与救援限制

- **已有观察**：在相机正常启动、电量 ≥ 50%、且能正常进入「设定菜单 → 固件版本 → 版本升级」的条件下，先前测试观察到可通过 SD 卡重刷原厂 `EG198581.BIN` 回退。
- **救援缺口**：上述观察不构成回退保证。若相机无法启动或无法进入升级菜单，目前缺少可靠的 USB 或硬件救援证据。

更多发布审查项与内嵌字节来源见 [RELEASE-CHECKLIST.md](../RELEASE-CHECKLIST.md) 与 [V2-PROVENANCE.md](V2-PROVENANCE.md)。
