# Nikon Z fc 固件补丁包 / Nikon Z fc Patchkit

[简体中文](#简体中文) · [English](#english)

---

# 简体中文

给 Nikon Z fc（C 1.81，EXPEED 6）做**自制固件功能补丁**的一组工具与已实测补丁。

**路线只有一条**：改主模块 `eg` 的字节 → 重算模块 CRC16 → 命名 `EG198581.BIN` →
放 SD 卡根目录 → 相机自己的「设置 → 固件版本 → 版本升级」。
**不需要 K8、不需要重新签名整包、不需要服务模式。**

> 这个仓库**不包含任何尼康固件**。官方升级文件请自行从尼康官网获取，脚本会校验它的 SHA-256。

## 适用与状态

| 项 | 值 |
|---|---|
| 机型 | Nikon Z fc |
| 固件 | C 1.81（容器 `Z_fc_0181.bin`，35,578,974 字节，sha256 `e4cd838a…bd1b6`） |
| 已验证的安装链路 | ✅ 实机（原厂模块重刷、真实补丁刷入、断电重启后功能正常） |
| 回滚 | ✅ 刷 `stock` 镜像即回到原厂 |

## 已实测的功能

| 功能 | 改动 | 实机结果 |
|---|---|---|
| **慢动作上限 3 → 25 分钟** | `0x102A0470` 4 字节（`180000` → `1500000` ms） | 已录 10 分钟正常（原厂 3 分钟）；25 分钟满程未验 |
| **1080p 码率提升** | 模式表 `0x10717144` 的 6 条记录（高档 84/70 与 56/48，标准档 56/48 与 28/24） | 8 个格式实测符合目标；4K 未动 |
| **照片取景斑马纹** | `0x101765DE` / `0x1017670A` 各 2 字节（`cbz r5,reject` → `nop`） | 照片取景出条纹，**原厂视频菜单「加亮显示」可直接开关** |

**正式版 = `zfc-v1`**（三项合一，23 处改动、88 字节写入、实际变化 74 字节）。

## 快速开始

```bash
# 1) 放好官方固件（同名或 --firmware 指定）
#    Z_fc_0181.bin  sha256 = e4cd838a215c113659416983b31dbdba8896591caacf7309170d4cc3c60bd1b6

# 2) 复现全部镜像并逐一对哈希（推荐先做这一步）
python tools/verify_release.py

# 3) 或者自己构建某一版
python tools/patch.py --input Z_fc_0181.bin --spec patches/combo.json \
                      --output out/EG198581.BIN --report out/report.json
```

`verify_release.py` 会把 `pins.json` 里每个镜像重建一遍并与实测时的哈希对比 ——
**如果全部 MATCH，说明你的固件和工具链与当初完全一致。**

## 目录

| 路径 | 内容 |
|---|---|
| `patches/*.json` | 补丁规格：`{offset, expected, replacement}` 列表 |
| `tools/zf.py` | 容器解析 / 模块提取 / CRC16（XOR 表缓存在 `tables.json`） |
| `tools/patch.py` | 等长补丁器（五道闸门，见下） |
| `tools/make_update.py` | 生成 SD 卡可用的 `EG198581.BIN` + 刷机说明 + 回滚镜像 |
| `tools/verify_release.py` | 复现并核对哈希 |
| `docs/` | 技术报告：模式表结构、斑马纹门、码率实测、注入空间分析、阶段小结 |

## 安全闸门（`patch.py` 强制执行，任一条不过就中止）

1. **R2 等长**：只做等长替换，模块长度永不变
2. **R3 边界**：目录区与其他模块一字不动
3. **R7 改动范围**：除声明的字节与模块 CRC 外，任何字节变化都中止
4. **R8 输入固定**：输入必须是钉死 SHA-256 的官方镜像
5. **整包 CRC 不变式**：重算模块 CRC 后，整包 CRC 必须仍是 `0xC023`

## 参考与致谢

本项目的**方法**来自 [Wonder Lantern（Nikon Z30 固件扩展项目）](https://github.com/WonderLantern/wonder-lantern-z30)。
它把"往固件模块里停放新代码 + 把既有调用重定向过去"这条路走通了（项目里叫 `CAPACITY`），
并在此之上做出了一整套功能：自定义菜单、画幅遮罩、全信息页、快门音、机内码率档位、
照片取景斑马纹、模块宿主等。本仓库的三个功能里有几个直接受益于它的结论：

- **独立 EG 模块的安装路径**（改模块 → 重算 CRC16 → `EG1985??.BIN` → SD 卡 → 相机自身升级）
- **`ldr.w pc` 跳板**这句写法（把 N 字节窗口换成"远跳 + 字面量"）
- **把配置存到 SD 卡**而不是写进固件的思路

Z30 与 Z fc 是同一代 EXPEED 6 平台，但**函数级地址不能照搬** —— 同一处代码在两个机型上的
位移都不是常数（我们实测同一处 `bl` 的目标位移与门本身的位移相差 `0xDC`）。所以本仓库里
Z fc 的每一个地址、数据表与验证结果都是重新定位、独立实测的。

其他参考：[NikonUnlock](https://github.com/summershrimp/NikonUnlock)（服务模式语言解锁协议）、
[nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools)（容器解包的 XOR 表）。

## 免责声明

改固件有风险。**升级过程中断电可能让相机无法开机**，且本机型没有已知的 USB 救援路径
（USB 栈就在被替换的 `eg` 模块里）。请满电操作、不要中断。
本工具与作者不对任何设备损坏、保修失效或数据丢失负责。仅供研究与个人使用。

---

# English

Tools and **camera-verified** feature patches for the Nikon Z fc (firmware C 1.81, EXPEED 6).

One installation route only: patch bytes in the `eg` module → recompute its CRC16 →
name it `EG198581.BIN` → put it in the SD card root → use the camera's own
*Setup → Firmware version → Update*. No K8, no re-signing of the full package, no service mode.

> This repository ships **no Nikon firmware**. Obtain the official update yourself;
> the scripts verify its SHA-256 before doing anything.

## Verified features

| Feature | Patch | Camera result |
|---|---|---|
| Slow-motion limit 3 → 25 min | 4 bytes at `0x102A0470` | 10-minute clip recorded fine; full 25 min untested |
| 1080p bitrate boost | 6 records in the mode table at `0x10717144` | 8 formats measured on target; 4K untouched |
| Photo-mode zebra | 2 bytes at `0x101765DE` / `0x1017670A` | Stripes in photo live view, toggled by the native *Highlight display* menu item |

`zfc-v1` combines all three (23 edits, 88 bytes written, 74 bytes actually changed).

## Quick start

```bash
python tools/verify_release.py        # rebuild everything and check the pinned hashes
python tools/patch.py --input Z_fc_0181.bin --spec patches/combo.json \
                      --output out/EG198581.BIN --report out/report.json
```

## Safety gates

Equal-length replacement only; module boundary and directory untouched; nothing but the
declared bytes and the module CRC may change; input pinned by SHA-256; the container CRC
invariant (`0xC023`) must still hold.

## Prior art and credits

The *method* comes from [Wonder Lantern](https://github.com/WonderLantern/wonder-lantern-z30),
a Nikon Z30 firmware-extension project. It established the technique of parking new code in
the firmware module and redirecting existing calls into it (called `CAPACITY` there), and
built a whole feature set on top: custom menus, aspect masks, a full-info display, shutter
sounds, in-camera bitrate profiles, photo-mode zebra and a module host. Several pieces here
follow directly from its findings:

- the **standalone EG-module install path** (patch the module → recompute CRC16 →
  `EG1985??.BIN` → SD card → the camera's own updater)
- the **`ldr.w pc` trampoline** that turns an N-byte window into a far jump plus a literal
- the idea of **keeping configuration on the SD card** instead of inside the firmware

The Z30 and the Z fc share the EXPEED 6 generation, but **function-level addresses cannot be
transplanted**: the same code site shifts by a different amount in each model (we measured a
`bl` target offset differing from the gate offset by `0xDC`). Every Z fc address, table and
verification result in this repository was re-located and measured independently.

Also referenced: [NikonUnlock](https://github.com/summershrimp/NikonUnlock) for the
service-mode language-unlock protocol, and
[nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools) for the
container XOR tables.

## Disclaimer

Firmware modification is risky. A power loss during the update can leave the camera
unbootable, and this model has no known USB recovery path (the USB stack lives in the very
module being replaced). Use a full battery, do not interrupt. The author is not responsible
for damaged hardware, voided warranty or lost data. Research and personal use only.

## License

MIT — see `LICENSE`.
