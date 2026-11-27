# Nikon Z fc 固件补丁包 / Nikon Z fc Patchkit

## 简体中文

**v2.0 是 Nikon Z fc C 1.81 的项目候选版本，已由用户初测。** GitHub 正式发布版仍为 v1。v2.0 的公开分支用于审查。

| 项目 | 来源报告记录的范围 |
|---|---|
| 普通录像 | 菜单显示 125:00，记录到 34:32、3.1 GB。125 分钟满程、4 GiB 和 4K 长录边界未验证。 |
| 慢动作 | 菜单显示 25:00，记录到 10 分钟。25 分钟满程未验证。 |
| 视频品质与码率 | 来源报告记录了五种 MP4 模式。MOV 未测。 |
| 其他功能 | 来源报告记录了扩展菜单、独立拍照斑马纹、自定义快门声、画幅与配置恢复的观察。后续仍需逐项绑定最终镜像及测试记录。 |

本地候选镜像大小为 35,060,342 字节，SHA-256 为 `b5c6e75ee6cbb09a98226e7bc928cdc4b4d05bd9d80df6fb1b180b26ea8161f8`。已计算本地镜像哈希，并核对它与版本声明及既有离线报告一致。已有检查记录为 0 项违规、27 项警告，尚需逐项分级。

原厂文件存在并不能保证回退成功。已有资料没有给出相机无法启动或无法进入升级菜单时的可靠救援办法。详见[发布审查清单](RELEASE-CHECKLIST.md)。

## English

**v2.0 is a project candidate for Nikon Z fc C 1.81. The owner reports an initial camera test without observed issues.** The latest formal GitHub Release is v1.

The source reports record a 125-minute menu setting and a clip of 34:32 (3.1 GB), and a 25-minute slow-motion setting and a 10-minute clip. Full-duration runs, the 4 GiB boundary, long 4K recording, and MOV remain untested in the reviewed evidence. The reported movie quality checks covered five MP4 modes. The source reports also describe observations for menu, zebra, sound, aspect ratio, and configuration restoration features.

The local candidate's SHA-256 was checked against the declared identity and saved offline report. The saved report lists zero violations and 27 warnings pending review. Recovery from a camera that cannot boot or enter its update menu remains unverified. See the [release review checklist](RELEASE-CHECKLIST.md).

## Credits and license

Related research includes [Wonder Lantern](https://github.com/WonderLantern/wonder-lantern-z30), [NikonUnlock](https://github.com/summershrimp/NikonUnlock), and [nikon-firmware-tools](https://github.com/simeonpilgrim/nikon-firmware-tools). See [LICENSE](LICENSE) for the repository's project license. The source and redistribution status of embedded bytes are part of release review.
