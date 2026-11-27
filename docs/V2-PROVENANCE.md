# Nikon Z fc Patchkit v2.0：内嵌内容来源与授权台账

- **对应版本**：`PuzzleFF/zfc-patchkit` `v2.0`（配方提交 `a1995765343359c69b6bf327068f660343e51851`）
- **维护者声明（2026-11-27）**：本项目除在 v1 与 v2 中明确致谢的第三方思路参考（Wonder Lantern Z30、NikonUnlock、nikon-firmware-tools）及沿用自 v1 的 `tools/tables.json` 外，全部代码、文档与补丁内容均为项目原创并适用仓库 [MIT 许可](../LICENSE)。`a199576` 已将全部 48 处 `expected` 校验改为 SHA-256，并将 239 段 ≥12 B 原厂表/原指令段（9,433 B）改为构建时从用户本地固件 `copy_stock`；`W1`/`W2`/`W6` 中低于 12 B 的结构短间隙与短原指令重放维持当前配方形态。
- **目标文件**：`patches/zfc-v2.json`（SHA-256 `9c1d5e34d55e89baaf5ac437c4959e750da0d4007db66a33d73517d25c8bf172`）
- **覆盖范围**：全部 **48 条 `patches[]` 替换记录（索引 `0–47`）**、全部 **213 条 `append_recipe` 直接写入记录（按 `op == "write"` 顺序编号 `0–212`）**，以及沿用自 v1 的 **`tools/tables.json`**；另含 239 条 `copy_stock` 指令（9,433 B，构建时从用户本地 `Z_fc_0181.bin` 读取，不内嵌字节）。
- **私有对照提交**：`PuzzleFF/zfc-research` 分支 `research/zfc-v2-complete`（`e77cb5ccbf70942c54b946174023cad62884acd3`）与 `PuzzleFF/CFW` 分支 `research/zfc-v2-findings`（`b6d4d041954d6bc335d96579808f73151bbc2083`）。
- **说明**：本表仅包含标识、来源类别、可核查依据与授权状态，**不包含任何十六进制载荷、固件、提取文件、密钥或设备标识**。

---

## 一、48 条 `patches[]` 替换记录（`0–47`，合计 48 条 / 709 B）

> 所有 48 条记录的原厂预期值均已改为 `expected_sha256` + `length` 校验，不包含原厂 `expected` 字节。下表覆盖每条记录的 `replacement` 内容：

| 组别 | 覆盖索引（`patches[]`） | 条数 / 字节 | 材料内容标识 | 来源类别 | 可核查依据（固定提交 / 文件） | 授权与致谢 |
|---|---:|---:|---|---|---|---|
| **P1** | `0, 1` | 2 / 2 B | 启动 RW 拷贝长度与 8 B 状态锚点预留修改 | 项目原创 | `zfc-research@e77cb5c`: `patches/zfc_all1b.json` | 仓库 MIT（项目原创） |
| **P2** | `2, 3, 4` | 3 / 32 B | 静音自定义快门声 3 个钩子跳板（`ext_snd_a_hook` / `data_hook` / `cfg_hook`） | 项目原创（跳板思路参考 Wonder Lantern） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`, `scripts/v2/audit_a_hook_arg.py` | 仓库 MIT（项目原创）；README 已向 Wonder Lantern 致谢 |
| **P3** | `5–21, 29–35` | 24 / 220 B | 自定义画幅生命周期 / 采集 / EXIF / 回放缩放钩子跳板 | 项目原创（跳板思路参考 Wonder Lantern） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json` | 仓库 MIT（项目原创）；README 已向 Wonder Lantern 致谢 |
| **P4** | `22, 23, 26, 37, 39, 40` | 6 / 54 B | 画幅菜单与扩展菜单 / 选择钩子跳板（`frame_*` / `select_*`） | 项目原创（跳板思路参考 Wonder Lantern） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`, `scripts/v2/make_extboot1.py` | 仓库 MIT（项目原创）；README 已向 Wonder Lantern 致谢 |
| **P5** | `24, 25` | 2 / 24 B | 独立拍照斑马纹双门控跳板（`ext_zebra_gate_a/b`） | 项目原创（跳板思路参考 Wonder Lantern） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`, `scripts/v2/make_zfc_all1b.py` | 仓库 MIT（项目原创）；README 已向 Wonder Lantern 致谢 |
| **P6** | `27, 28, 43, 44, 45` | 5 / 339 B | 125 分钟时长表（84 项合并为 3 段）+ 引擎门限 + 慢动作 25 分钟时长值 | 项目原创（125 分钟数值参考 Nikon Z30 固件观测） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`, `notes/ZFC-V2-ARCHITECTURE-AND-RESULTS-2026-11-27.md` | 仓库 MIT（项目原创） |
| **P7** | `36, 38, 42` | 3 / 15 B | 视频品质菜单 Page 205 谓词、条件列表 `0x49` 计数与 `qmenu_rates` 跳板 | 项目原创 | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`, `scripts/v2/make_zfc_all1.py` | 仓库 MIT（项目原创） |
| **P8** | `41` | 1 / 10 B | 实时取景画幅遮罩钩子跳板（`p2bmask2_fast`） | 项目原创（跳板思路参考 Wonder Lantern） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`, `scripts/v2/make_extboot1.py` | 仓库 MIT（项目原创）；README 已向 Wonder Lantern 致谢 |
| **P9** | `46, 47` | 2 / 13 B | 设定菜单 Page 394 与拍照菜单 Page 39 控件/分发指针改写 | 项目原创（指向项目自建扩展表地址） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json` | 仓库 MIT（项目原创） |

> **核对合计**：`2 + 3 + 24 + 6 + 2 + 5 + 3 + 1 + 2 = 48` 条（覆盖索引 `0–47`，无遗漏、无重叠）。

---

## 二、213 条 `append_recipe` 直接写入记录（`0–212`，合计 213 条 / 22,514 B）

> 编号按 `patches/zfc-v2.json` 中 `append_recipe` 数组内 `op == "write"` 的出现顺序从 `0` 到 `212` 计数。

| 组别 | 覆盖 `write` 编号 | 条数 / 字节 | 对应块与内容标识 | 来源类别 | 可核查依据（固定提交 / 文件） | 授权与说明 |
|---|---:|---:|---|---|---|---|
| **W1** | `0–49, 51–106, 108–112, 170–182, 188, 192, 199, 203` | 128 / 2,732 B | `profile_3..8`、`frame_template`、`frame_parent_*`、`ext_p394_*`、`ext_hub_events`、`ext_sub_events`、`ext_p961..964_layout/boxes` 内的项目修改字段及 `<12 B` 结构短间隙 | 项目原创修改（≥12 B 原厂段已通过 `copy_stock` 从用户本地固件读取；余下 `<12 B` 结构短间隙） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json` | 项目修改部分适用仓库 MIT；维护者确认维持当前 `copy_stock` 配方形态 |
| **W2** | `50` | 1 / 6,573 B | 跨块写入：`profile_pointers`、`slot30_capacity`、`life_*`、`capture_*`、`direct_*`、`jpeg_metadata_dimensions`、`exif_*`、`file_preview_after_release` 及 `frame_template` 开头字节 | 项目原创汇编（尾端含 `frame_template` 开头短字节） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json` | 原创汇编部分适用仓库 MIT；维护者确认维持当前配方形态 |
| **W3** | `155–159` | 5 / 1,374 B | 静音自定义快门声汇编：`ext_snd_cb`、`ext_snd_load_slot`、`ext_snd_trigger`、`ext_snd_a_hook`、`ext_snd_data_hook`、`ext_snd_cfg_hook` | 项目原创独立重写（思路参考 Wonder Lantern） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`、`notes/ZFC-V2-ARCHITECTURE-AND-RESULTS-2026-11-27.md`（与 WL 逐指令比对：6-gram 重合度 0.0%、最长精确连续 3 条） | 仓库 MIT（项目原创）；README 已向 Wonder Lantern 致谢 |
| **W4** | `144, 212` | 2 / 4,610 B | `p2bmask2`（旧留位）、`p2e4_zoom_after_release`、`siteb_preserve_custom`、`ext_page_templates`、`ext_boot_restore`、`p2bmask2_fast`、`qmenu_rates` | 项目原创独立重写（思路参考 Wonder Lantern） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`、`scripts/v2/make_extboot1.py`、`scripts/v2/make_zfc_all1b.py`（与 WL 逐指令比对：6-gram 重合度 0.0%、最长精确连续 2 条） | 仓库 MIT（项目原创）；README 已向 Wonder Lantern 致谢 |
| **W5** | `107, 160–169, 183–187, 189–191, 193–198, 200–202, 204–211` | 36 / 951 B | 项目原创常量与元表：`ext_str_blob`（UTF-16LE 菜单文字）、`ext_cfg_path`、`ext_wav_path_0..4`、`ext_wav_table`、`ext_str_table`、`ext_callbacks`、`frame_relocs`、`ext_p961..964_ctrls/disp/labels/vals/geom/meta` | 项目原创 | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`（原厂 16 B 分片覆盖率 0%） | 仓库 MIT（项目原创） |
| **W6** | `113–143, 145–154` | 41 / 6,274 B | 画幅选择、菜单运行时、统一配置与独立拍照斑马纹汇编：`select_*`、`frame_*`、`cfg_*`、`ext_cfg_*`、`ext_ensure`、`ext_enter`、`ext_confirm`、`ext_back`、`ext_zebra_gate_a/b`、`ext_snd_ccb` | 项目原创汇编（部分钩子尾部含 `<12 B` 被覆盖原指令重放） | `zfc-research@e77cb5c`: `patches/zfc_all1b.json`、`scripts/v2/make_extboot1.py`、`scripts/v2/make_zfc_all1b.py` | 原创汇编部分适用仓库 MIT；维护者确认维持当前配方形态 |

> **核对合计**：`128 + 1 + 5 + 2 + 36 + 41 = 213` 条（覆盖 `write` 编号 `0–212`，无遗漏、无重叠）。

---

## 三、沿用自 v1 的第三方数据文件

| 标识 | 来源类别 | 可核查依据 | 说明 |
|---|---|---|---|
| `tools/tables.json`（3,560 B，SHA-256 `C14BDE9F…0B1C`） | 第三方容器解码 XOR 表缓存（沿用自 `v1`） | `tools/zf.py` 指向 `simeonpilgrim/nikon-firmware-tools` | 非本项目原创，已在 README 致谢 `nikon-firmware-tools`；不适用本仓库 MIT 再授权 |
