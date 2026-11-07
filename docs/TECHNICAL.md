# 技术说明

记录整合过程中查清的游戏机制，以及各次修复的依据。供后续维护或制作类似整合参考。

## 1. 语言槽机制

`KidGame\Config\KidEngine.ini` 第 40 行左右：

```ini
Language=INT
```

启动时读取，决定加载哪一套资源。游戏内选项里的「英语 / 日语」实际上是**语音标识**，与槽位绑定，
且该选项不会把选择写回 ini（PC 版已知问题）。PCGamingWiki 记为
「Japanese voice language plays some sounds in English」，给出的解法正是手改 `Language=` 为 `JPN`。

存档 `KID.sav` 里搜不到语言标志，说明设置只落在这个 ini 上。

游戏存在 `INT / JPN / CHN / DEU / ESN / FRA / ITA` 等本地化槽，本整合只改 **INT**（简体）与 **JPN**（繁体）。

## 2. 文本资源分布在三处

| 位置 | 内容 | 数量 |
| --- | --- | --- |
| `KidGame\Localization\INT\*.int`、`JPN\*.jpn` | UI / 菜单 / 章节文字 | 每槽 34 个 |
| `KidGame\CookedPC\Maps\**\*_LOC_INT.upk`、`*_LOC_JPN.upk` | 关卡内对话、字幕 | 每槽 193 个 |
| `KidGame\Movies\*_INT.txt`、`*_JPN.txt` | 过场动画画面内字幕 | 每槽 39 组 |

**之前整合失败的根因**：只替换了 `Localization\JPN\*.jpn`，没同步改 193 个 `*_LOC_JPN.upk`
和 39 个 `*_JPN.txt`，切到第二槽时大部分内容仍是简体，看起来像「只有第一顺位语言正常」。

`.int` / `.jpn` / `Movies\*.txt` 均为 **UTF-16LE**，部分带 `FF FE` BOM、CRLF 行尾；
改写时必须保留 BOM 状态与行尾，否则游戏读取异常。

## 3. UPK 内字符串与长度不变的转换

UE3 的 `FString` 用**负长度前缀**表示 UTF-16LE 字符串。`tools/reference/lib.py` 的做法：

```python
PAT = re.compile(rb'[\x00-\xff][\xF8-\xff]\xff\xff')  # 定位负长度字段

def iter_strings(d):
    # 校验长度在 -4000..-2，解码 utf-16-le，
    # 只保留含 >=2 个 CJK 且字符全在白名单内的串
    ...

def convert(d):
    for s, e, body, nul in iter_strings(d):
        new = ''.join(chr(MAP.get(ord(ch), ord(ch))) for ch in body)
        nb = (new + ('\x00' if nul else '')).encode('utf-16-le')
        if len(nb) == e - s:      # 长度必须严格相等
            d[s:e] = nb
```

关键点：**只做单字符 1:1 映射**（`MAP` 由 OpenCC `s2tw` 对 CJK 逐字生成），
绝不改变字符串字节长度，因此 UPK 的所有内部偏移、导入表、对象名都保持有效。
质检脚本会比对备份，确认每一处字节差异都落在 `iter_strings` 给出的区间内，且文件大小不变。

音频数据（OGG 流）也在这些 UPK 内，但文本替换从不触碰它们。

## 4. 两套字体，作用域不同（最容易搞混的地方）

| 字体包 | 用途 | 字表 |
| --- | --- | --- |
| `CookedPC\UI\FontLib_INT.upk` | UI / 菜单 / 关卡内字幕 | 完整 CJK 码表，简繁字形齐全 → **繁体显示正常** |
| `CookedPC\Startup_LOC_INT.upk` → `SubtitleFont.SubtitleFont` | **过场动画画面内字幕** | 两张完全相同的「Unicode → 字形索引」表，各 1860 项，含 1728 个汉字，全部是简体字形 |

`DefaultEngine.ini` / `KidEngine.ini` 中的相关配置：

```ini
SubtitleFontName=SubtitleFont.SubtitleFont
+AdditionalFontNames=SubtitleFont.SubtitleFont
+AdditionalFontNames=KidFonts00.KidFonts00
```

全盘扫描（`tools/reference/scan_fonts.py`）结论：

- 整个游戏**只有** `Startup_LOC_INT.upk` 里有字幕字形映射表，表偏移 `2583508` 与 `2630112`，内容完全相同。
- 不存在 `Startup_LOC_JPN.upk`，也不存在按语言槽分开的第二份字幕字体包。
- 繁体样例字（館 發 說 誘 闆 隻 週 歷 歸 懷 巔 闖）命中数为 **0**。
- 表外字不会被画成方框，而是被字体引擎统一 fallback 到**同一个字形「专」**——这是判断字库缺字的关键现象。

因此繁体过场字幕里的约 400 个特有字（共 2856 处）全部会变成「专」，游戏层面无法补字形。
**结论只适用于 `Movies\*.txt`；菜单与关卡字幕走 UI 字体库，繁体完全正常，不需要简体化。**

## 5. 过场字幕的缺字换字

用户点名的两处：第一章「左撇子」的 `撇`（简繁都缺）、`誘拐` 的 `誘`（繁体缺）。
采用**词级换字**而非补字库，且不使用逐字替换（逐字会把 `抹殺` 变「消殺」、`闇暗` 变「暗暗」、
`忽略` 变「略略」、`深♂入♀瞭解你` 变「深男入女瞭解你」，造成破句）。

### 缺字换字清单

简体侧（19 行）：

| 原词 | 改为 |
| --- | --- |
| 左撇子 | 用左手 |
| 纵横南北 | 走遍南北 |
| 成为了历史 | 成为了过去 |
| 时光流逝 | 时光流去 |
| 抹杀 | 消除 |
| 搞砸了 | 搞坏了 |
| 蒙德·扎帕 | 蒙德·札帕 |
| 阁下 | 先生 |
| 臆测 | 猜测 |
| 恶徒 | 恶人 |
| 难以忘怀 | 难以忘记 |
| 闇暗 | 黑暗 |
| 吃饱了撑的慌 | 吃饱了没事做 |
| 虎已逝 | 虎已不在 |
| 龙犹存 | 龙还在 |
| 忽略这么个东西 | 无视这么个东西 |
| `深♂入♀了解你` | 深入了解你 |

繁体侧（20 行，当时仍是繁体字幕时）：誘拐→拐走、時光流逝→時光流去、抹殺→消除、
左撇子→用左手、縱橫南北→走遍南北、成為了歷史→成為了過去、`♀`→女 / `♂`→男 等。

第一章结果：

```
INT: 少女诱拐案件频发 据说犯人是用左手?
JPN: 少女拐走案件頻發 據說犯人是用左手?     ← 繁体版曾用的文本
```

**最终状态**：因第 4 节的字库限制，两槽过场字幕统一采用已换字、零表外字的简体文本
（`*_JPN.txt` 与 `*_INT.txt` 内容完全一致）。按 1746 项字库表扫描，表外字 0 行。

> 完整繁体槽状态（含繁体过场字幕）保留在构建机的 `E:\Temp\kid\backup_traditional`
> （34 个 `.jpn` + 39 个字幕 + 193 个 UPK，共 266 个文件）。
> 日后若能拿到含繁体字形的字幕字体包，可从该备份恢复文本再试。

## 6. 语音资源

- 全盘没有独立的 `.bnk` / `.wem` / `.ogg` 音频文件；**OGG 语音流内嵌在**
  `CookedPC\Maps\**\*_LOC_<LANG>.upk` 里。
- 比对 39 对大包，前 12 对里 11 对的 JPN 与 INT 音频流页数与内容都不同 → JPN 槽确实是另一套录音。
- 补丁只改 UPK 里的 UTF-16 文本字节，从未改写 OGG 数据。
- `Movies` 下 96 个过场视频全是 `_EN.bik`（`KID_EP*_EN.bik`、`Gigolo_*_EN.bik`），
  **没有日语版**，所以过场动画永远是英语音轨，这是游戏本体如此。

## 7. 质检方法

| 检查 | 手段 |
| --- | --- |
| 二进制改动范围 | 比对备份，所有差异字节必须落在 `iter_strings` 区间内；文件大小不变 |
| 简繁残留 | OpenCC `t2s` / `s2t` 逐文件比对，JPN 侧不应残留简体，INT 侧不应残留繁体 |
| 字幕缺字 | 从 `Startup_LOC_INT.upk` 提取字库表 → `font_full.json`，逐行扫描表外字 |
| 整合包一致性 | 遍历输出目录与游戏目录逐字节比对（538 个补丁文件应全部一致，`KidEngine.ini` 例外） |
| 交付校验 | 从 7z 内直接抽取 `HUD.jpn` 与第一章字幕复核内容 |

## 8. 构建脚本

`tools/reference/` 下是构建时的一次性脚本，**路径写死为作者本机的绝对路径**
（`E:\Game\Steam\steamapps\common\KillerIsDead` 等），仅供方法参考，直接运行前需自行改路径。
依赖见 `tools/requirements.txt`。

| 脚本 | 作用 |
| --- | --- |
| `lib.py` | UPK 字符串定位与 1:1 映射（核心逻辑，无路径依赖） |
| `scan_fonts.py` | 全盘扫描 Unicode→字形索引映射表 |
| `fontset2.py` | 导出 `Startup_LOC_INT.upk` 的字符集 |
| `final_v2.py` | 过场字幕纯词级换字 |
| `restore_traditional.py` | 恢复 JPN 槽繁体（回滚过度简体化） |
| `sync_hud.py` / `make_patch.py` | 同步输出目录、生成补丁目录结构 |
