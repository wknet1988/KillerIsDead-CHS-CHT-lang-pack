# -*- coding: utf-8 -*-
"""回滚 v1.5.2 的「整套简体化」，恢复 JPN 槽繁体：
   - 菜单 *.jpn / 关卡 *_LOC_JPN.upk / HUD 标签  <- backup_traditional（繁体状态）
   - HUD.int                                    <- backup_original（原补丁标签）
   - Movies\\*_JPN.txt 保持简体（= *_INT.txt），因为过场字幕字库只有简体字形
   最后同步整合包目录并重写 readme。
"""
import os, glob, shutil

GAME = r'E:\Game\Steam\steamapps\common\KillerIsDead\KidGame'
TRAD = r'E:\Temp\kid\backup_traditional'
ORIG = r'E:\Temp\kid\backup_original'
OUT  = r'E:\Temp\kid\out\KID_v1.5.2'

changed = []          # 相对 GAME 的路径
def sync_from(src, dst):
    shutil.copy2(src, dst)
    changed.append(os.path.relpath(dst, GAME))

# --- 1. 菜单 / UI 文本：恢复繁体 ---
n = 0
for p in sorted(glob.glob(os.path.join(TRAD, 'Localization', 'JPN', '*.jpn'))):
    sync_from(p, os.path.join(GAME, os.path.relpath(p, TRAD)))
    n += 1
print('1. 菜单 *.jpn 恢复繁体：%d 个' % n)

# --- 2. 关卡字幕 UPK：恢复繁体 ---
n = 0
for p in sorted(glob.glob(os.path.join(TRAD, r'CookedPC\Maps\**\*_LOC_JPN.upk'), recursive=True)):
    sync_from(p, os.path.join(GAME, os.path.relpath(p, TRAD)))
    n += 1
print('2. 关卡字幕 *_LOC_JPN.upk 恢复繁体：%d 个' % n)

# --- 3. HUD.int 恢复原补丁标签（语音 英语/日语，字幕语言 简体/繁体中文） ---
p = os.path.join(ORIG, 'Localization', 'INT', 'HUD.int')
sync_from(p, os.path.join(GAME, 'Localization', 'INT', 'HUD.int'))
print('3. HUD.int 恢复原版标签')

# --- 4. 过场动画字幕：JPN 继续保持与 INT 相同的简体（唯一受字库限制的部分） ---
n = same = 0
for p in sorted(glob.glob(os.path.join(GAME, 'Movies', '*_INT.txt'))):
    q = p.replace('_INT.txt', '_JPN.txt')
    n += 1
    if open(p, 'rb').read() == open(q, 'rb').read():
        same += 1
    else:
        shutil.copy2(p, q)
        changed.append(os.path.relpath(q, GAME))
print('4. 过场字幕：%d 组，其中 %d 组已是简体一致，补同步 %d 组' % (n, same, n - same))

# --- 5. 同步到整合包 ---
synced = 0
for rel in changed:
    dst = os.path.join(OUT, 'KidGame', rel)
    if os.path.isfile(dst):
        shutil.copy2(os.path.join(GAME, rel), dst)
        synced += 1
print('5. 同步到整合包：%d / %d' % (synced, len(changed)))

# --- 6. 重写 readme（GBK / CRLF） ---
readme = '''杀手已死：噩梦版（Killer is Dead Nightmare Edition）
起源汉化组 v1.5.1 简/繁补丁整合 · v1.5.2

────────────────────────────────
两个语言槽
────────────────────────────────
INT 槽 = 简体中文（选项里语音为「英语」）
JPN 槽 = 繁体中文（选项里语音为「日语」）

菜单、界面、章节文字、关卡内对话与字幕，两个槽各自简/繁分开，显示正常
（这部分使用 CookedPC\\UI\\FontLib_INT.upk 的完整 CJK 字表）。

语音选项标签保持游戏原样「英语 / 日语」，没有改动。

────────────────────────────────
唯一限制：过场动画字幕
────────────────────────────────
过场动画字幕（KidGame\\Movies\\*.txt）不走上面的 UI 字体，而是使用
CookedPC\\Startup_LOC_INT.upk 内的 SubtitleFont 字库。全盘扫描确认游戏里
只有这一套字幕字库，两张映射表各 1728 个字，全部是简体字形，繁体字形
一个也没有，也不存在按语言槽分开的第二份字体包。

所以繁体文本里的繁体特有字会被字体引擎统一渲染成同一个「专」字。
由于无法在游戏层面补字形（需重烘焙字体包，要 UE3 工具链与字体源文件），
本整合版让「过场动画画面内的字幕」在两槽都使用简体中文文本：
Movies\\*_JPN.txt 与 Movies\\*_INT.txt 内容完全一致。

也就是说：切到日语语音后，菜单和关卡字幕仍是繁体，只有过场动画那一小段
字幕是简体。这是为避免满屏「专」字做的唯一妥协。

────────────────────────────────
过场字幕缺字换字修复
────────────────────────────────
按「换字」方式把字库外的生僻字改成字库内的同义词，共改写 19 行，例如：
左撇子→用左手、诱拐案件→（繁体槽对应句）拐走案件、纵横南北→走遍南北、
时光流逝→时光流去、抹杀→消除、闇暗→黑暗、蒙德·扎帕→蒙德·札帕。
最终过场字幕按 1746 项字库表扫描，表外字 0 行。

────────────────────────────────
安装方法
────────────────────────────────
把本补丁内的 KidGame 文件夹整个覆盖到游戏根目录
（例：E:\\Game\\Steam\\steamapps\\common\\KillerIsDead）
提示覆盖文件时选「是」。存档不受影响，可以直接沿用。

文字语言由 KidGame\\Config\\KidEngine.ini 的 Language=INT/JPN 在启动时读取。
若改了选项文字不跟着变，把 SwitchLanguage.bat 放到游戏根目录双击运行，
或直接改这一行，然后重开游戏即可。

影院（Theater）→ 字幕语言：INT=简体中文 / JPN=繁体中文，标签保持原补丁原样。
注意在影院回放过场动画时，画面内字幕同样受上面字库限制，两槽均为简体。

────────────────────────────────
这个整合版做了什么
────────────────────────────────
1. 补齐上一版整合遗漏：KidGame\\Localization\\JPN\\*.jpn、
   KidGame\\CookedPC\\Maps 下全部 193 个 *_LOC_JPN.upk、
   KidGame\\Movies 下 39 组 *_JPN.txt，三处同步为繁体，
   解决「只有第一顺位语言能正常显示」的问题。
2. UPK 内字符串用 UTF-16LE 单字符 1:1 映射转换，文件大小与偏移不变。
3. 过场动画字幕换字修复缺字，并因字库限制在两槽统一为简体文本。
4. 语音选项标签保持原样（英语 / 日语）。

────────────────────────────────
备份 / 还原
────────────────────────────────
E:\\Temp\\kid\\backup_original                  整合前状态（简体补丁原样）
E:\\Temp\\kid\\backup_traditional               v1.5.2 完整繁体槽状态（含繁体过场字幕）
E:\\Temp\\kid\\backup_movies_before_glyphfix    换字前的过场动画字幕
把对应备份覆盖回游戏目录即可还原。日后若能拿到含繁体字形的字幕字体包，
可从 backup_traditional 恢复繁体过场字幕文本再试。

────────────────────────────────
原补丁说明（起源汉化组 v1.5）
────────────────────────────────
文本来源为 PS3 官方日文版，在此基础上进行了汉化。
仅对基于日文版文本的文件追加了翻译。
理论上还原了 PS3 官方日文版的感觉。
转载请注明出处，请勿用于商业用途。
'''
open(os.path.join(OUT, 'readme.txt'), 'wb').write(readme.replace('\n', '\r\n').encode('gbk'))
print('6. readme.txt 已重写（GBK/CRLF）')
