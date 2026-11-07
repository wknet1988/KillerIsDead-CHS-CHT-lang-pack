# -*- coding: utf-8 -*-
import os, shutil, glob

G = r"E:\Game\Steam\steamapps\common\KillerIsDead"
OUT = r"E:\Temp\kid\out\KID_v1.5.2"

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)

patch = [l.strip().replace("/", "\\") for l in open(r"E:\Temp\kid\patch_list.txt", encoding="utf-8") if l.strip()]
n = 0
for rel in patch:
    if rel.endswith("说明.txt"):
        continue
    src = os.path.join(G, rel)
    dst = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    n += 1

for p in sorted(glob.glob(os.path.join(G, r"KidGame\Movies\*_JPN.txt"))):
    dst = os.path.join(OUT, r"KidGame\Movies", os.path.basename(p))
    shutil.copy2(p, dst)
    n += 1

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
游戏内切换简繁
────────────────────────────────
主菜单 → 选项 → 语言 → 简体中文 / 繁体中文
影院（Theater）→ 字幕语言 → 简体中文 / 繁体中文

选“简体中文”：文字为简体（INT 语言槽）
选“繁体中文”：文字为繁体（JPN 语言槽）
语音跟随语言槽一起切换（INT 槽为英语语音，JPN 槽为日语语音）。

如果选单里的切换没有立即生效，可以手动改配置：
用记事本打开 KidGame\\Config\\KidEngine.ini，
把 Language=INT 改成 Language=JPN（繁体），或改回 INT（简体），存盘后重开游戏。

────────────────────────────────
这个整合版做了什么
────────────────────────────────
1. INT 语言槽 = 简体内容（Localization\\INT\\*.int、Movies\\*_INT.txt、
   CookedPC\\Maps 下全部 *_LOC_INT.upk）
2. JPN 语言槽 = 繁体内容（Localization\\JPN\\*.jpn、Movies\\*_JPN.txt、
   CookedPC\\Maps 下全部 *_LOC_JPN.upk）
3. 原繁体补丁里漏翻的两章文本（第 6 章 VICTOR、第 10 章 THOMAS）仍是简体，
   现已全部转为繁体。
4. 标题选单的语言标签由“英语/日语”改为“简体中文/繁体中文”，一眼能认。

────────────────────────────────
说明
────────────────────────────────
- 字体库 CookedPC\\UI\\FontLib_INT.upk 内含完整 CJK 字表（两万余字形），
  简繁共用同一套字体，不会出现缺字方框。
- 过场动画字幕（Movies\\*.txt）跟随影院字幕语言设置。
- 存档不受影响，可以直接沿用。

────────────────────────────────
原补丁说明（起源汉化组 v1.5）
────────────────────────────────
文本来源为 PS3 官方日文版，在此基础上进行了汉化。
仅对基于日文版文本的文件追加了翻译。
理论上还原了 PS3 官方日文版的感觉。
转载请注明出处，请勿用于商业用途。
"""

with open(os.path.join(OUT, "readme.txt"), "wb") as f:
    f.write(README.replace("\n", "\r\n").encode("gbk"))

print("生成文件", n, "+ readme.txt")
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print("总体积 %.1f MB" % (tot / 1048576))
