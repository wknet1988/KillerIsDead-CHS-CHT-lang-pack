# Killer is Dead: Nightmare Edition — 简繁中文整合语言包

把起源汉化组 **v1.5.1** 的「简体中文汉化补丁」和「繁体中文汉化补丁」整合进同一份游戏安装，
用游戏自带的 **INT / JPN 语言槽**切换简繁，不必再反复覆盖文件、也不会出现「只有第一顺位语言正常显示」。

---

## 下载

| 版本 | 文件 | 大小 | SHA-256 |
| --- | --- | --- | --- |
| **v1.5.2** | [KillerIsDead_CHS_CHT_v1.5.2.7z](https://github.com/wknet1988/KillerIsDead-CHS-CHT-lang-pack/releases/tag/v1.5.2) | 135,290,198 字节（129.02 MiB） | `53cc5a013d842bf76ce33e07f87855ce0c541d11901ab4a779272a862e169dc8` |

MD5：`51d990deee1fa1d774e27b9bbe9e71e7`

压缩包内是 `KID_v1.5.2/`，含 `KidGame/`（539 个补丁文件）、`readme.txt`、`SwitchLanguage.bat`，共 541 个文件。
因为单文件超过 GitHub 仓库的 100 MB 限制，**补丁本体放在 Release 附件里**，仓库只保留文档、切换脚本和构建参考代码。

---

## 安装

1. 备份游戏目录（至少备份 `KidGame\Config` 与 `KidGame\Localization`）。
2. 解压 `KillerIsDead_CHS_CHT_v1.5.2.7z`。
3. 把 `KID_v1.5.2\KidGame` **整个覆盖**到游戏根目录，例如
   `E:\Game\Steam\steamapps\common\KillerIsDead`，提示覆盖时选「是」。
4. 存档不受影响，可直接沿用。

## 切换简繁

游戏内的「语音 / 语言」选项**不会把选择写进配置**（PC 版已知问题，PCGamingWiki 也记为
「Japanese voice language plays some sounds in English」）。实际生效的是配置文件：

```
KidGame\Config\KidEngine.ini  →  Language=INT 或 Language=JPN
```

**推荐做法**：完全退出游戏 → 双击本仓库的 [`SwitchLanguage.bat`](SwitchLanguage.bat)
（把它放在游戏根目录，与 `KidGame` 同级）→ 重开游戏。脚本会在 INT / JPN 之间来回切换。

若游戏启动时又把值改回去，可手动编辑该行并把 `KidEngine.ini` 设为只读。

| 语言槽 | 界面 / 菜单 / 章节 | 关卡内对话与字幕 | 游戏内语音 | 过场动画字幕 |
| --- | --- | --- | --- | --- |
| `Language=INT` | 简体中文 | 简体中文 | 英语 | **简体中文** |
| `Language=JPN` | 繁体中文 | 繁体中文 | 日语（游戏内对话） | **简体中文** |

> 语音选项标签保持游戏原样「英语 / 日语」，没有改成「简体中文 / 繁体中文」——那一项本来就是语音。

---

## 已知限制

1. **过场动画字幕两槽都用简体**。`KidGame\Movies\*.txt` 不走 UI 字体，而走
   `CookedPC\Startup_LOC_INT.upk` 里的 `SubtitleFont`。全盘扫描确认游戏只有这一套字幕字库，
   两张映射表各 1728 个字，**全部是简体字形，繁体字形一个也没有**，也没有按语言槽分开的第二份字体包。
   繁体特有字会被字体引擎统一渲染成同一个「专」字。要在游戏层面补字形必须重烘焙字体包
   （需 UE3 工具链与字体源文件），因此本整合让画面内字幕在两槽统一使用简体文本，
   `Movies\*_JPN.txt` 与 `Movies\*_INT.txt` 完全一致。**菜单与关卡字幕不受影响，仍是正常繁体。**
2. **过场动画永远是英语音轨**。`Movies` 下 96 个视频全是 `_EN.bik`，没有日语版，切 JPN 也一样。
3. **语音与文字绑定同一个语言槽**，所以「简体文字 + 日语语音」目前做不到，只能二选一。
4. **影院（Theater）回放**过场动画时，画面内字幕同样受第 1 条限制。

详见 [docs/TECHNICAL.md](docs/TECHNICAL.md)。

---

## 这个整合版修了什么

- 补齐上一版整合的三处遗漏，解决「只有第一顺位语言能正常显示」：
  - `KidGame\Localization\JPN\*.jpn`（34 个）
  - `KidGame\CookedPC\Maps\**\*_LOC_JPN.upk`（193 个）
  - `KidGame\Movies\*_JPN.txt`（39 组）
- UPK 内的 UTF-16LE 字符串做**单字符 1:1 映射**，文件大小与偏移完全不变，不破坏包结构。
- 过场字幕按字库表做**词级换字**修掉缺字（如「左撇子 → 用左手」「纵横南北 → 走遍南北」），
  最终按 1746 项字库表扫描，表外字 0 行。替换清单见 [docs/TECHNICAL.md](docs/TECHNICAL.md#缺字换字清单)。
- 语音选项标签恢复为游戏原样。

---

## 仓库内容

| 路径 | 说明 |
| --- | --- |
| [README.md](README.md) | 本页 |
| [SwitchLanguage.bat](SwitchLanguage.bat) | INT / JPN 切换脚本（GBK / CRLF，放游戏根目录双击） |
| [docs/patch-readme.md](docs/patch-readme.md) | 补丁包内 `readme.txt` 的 UTF-8 版 |
| [docs/TECHNICAL.md](docs/TECHNICAL.md) | 槽位机制、UPK 结构、字体作用域、语音资源、换字清单 |
| [tools/](tools/) | 构建时用到的参考脚本与依赖说明 |

补丁包本体请在 [Releases](https://github.com/wknet1988/KillerIsDead-CHS-CHT-lang-pack/releases) 下载。
