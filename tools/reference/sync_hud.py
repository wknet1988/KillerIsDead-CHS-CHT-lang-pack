# -*- coding: utf-8 -*-
import os, shutil

G = r"E:\Game\Steam\steamapps\common\KillerIsDead\KidGame\Localization"
O = r"E:\Temp\kid\out\KID_v1.5.2\KidGame\Localization"
for rel in [r"INT\HUD.int", r"JPN\HUD.jpn"]:
    shutil.copy2(os.path.join(G, rel), os.path.join(O, rel))
    print("同步", rel)

README = """杀手已死：噩梦版（Killer is Dead Nightmare Edition）
简繁中文汉化补丁 v1.5.2 整合版
基于 起源汉化组 v1.5.1 简体版 + v1.5.1 繁体版 整合制作

────────────────────────────────
安装方法
────────────────────────────────
把本补丁内的 KidGame 文件夹整个覆盖到游戏根目录
（例：E:\\Game\\Steam\\steamapps\\common\\KillerIsDead）
提示覆盖文件时选“是”。

────────────────────────────────
简繁怎么切
────────────────────────────────
本作的文字内容和语音内容是绑在同一个语言槽上的，游戏里只有“语音”选项：

  选项 → 语言（Voice）→ 英语 ：文字为简体中文，语音为英语
  选项 → 语言（Voice）→ 日语 ：文字为繁体中文，语音为日语

也就是说，选英语＝简体版，选日语＝繁体版。游戏自带的语音选项没有改动，
还是原来的“英语 / 日语”。

如果切了语音发现界面文字没跟着变（个别情况下要重开游戏才生效），
把 SwitchLanguage.bat 放到游戏根目录双击运行，它会直接改
KidGame\\Config\\KidEngine.ini 里的 Language=INT / JPN，然后重开游戏即可。
（Language=INT → 简体，Language=JPN → 繁体）

过场动画字幕另有单独设置：影院（Theater）→ 字幕语言 → 简体中文 / 繁体中文。

────────────────────────────────
这个整合版做了什么
────────────────────────────────
1. INT 语言槽 = 简体内容（Localization\\INT\\*.int、Movies\\*_INT.txt、
   CookedPC\\Maps 下全部 *_LOC_INT.upk）
2. JPN 语言槽 = 繁体内容（Localization\\JPN\\*.jpn、Movies\\*_JPN.txt、
   CookedPC\\Maps 下全部 *_LOC_JPN.upk）
3. 原繁体补丁里漏翻的两章文本（第 6 章 VICTOR、第 10 章 THOMAS）仍是简体，
   现已全部转为繁体。
4. 影院字幕语言列表里的 INT / JPN 标签显示为“简体中文 / 繁体中文”。

────────────────────────────────
说明
────────────────────────────────
- 字体库 CookedPC\\UI\\FontLib_INT.upk 内含完整 CJK 字表（两万余字形），
  简繁共用同一套字体，不会出现缺字方框。
- 存档不受影响，可以直接沿用。

────────────────────────────────
原补丁说明（起源汉化组 v1.5）
────────────────────────────────
文本来源为 PS3 官方日文版，在此基础上进行了汉化。
仅对基于日文版文本的文件追加了翻译。
理论上还原了 PS3 官方日文版的感觉。
转载请注明出处，请勿用于商业用途。
"""

p = os.path.join(r"E:\Temp\kid\out\KID_v1.5.2", "readme.txt")
open(p, "wb").write(README.replace("\n", "\r\n").encode("gbk"))
print("readme 已更新")
