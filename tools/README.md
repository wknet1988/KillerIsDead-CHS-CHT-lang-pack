# tools

本目录是**构建参考**，不是可直接运行的安装工具。

- `requirements.txt`：Python 依赖（OpenCC 简繁转换）。
- `reference/`：v1.5.2 整合过程中实际用过的一次性脚本。

## 使用前必读

1. `reference/` 下的脚本把游戏目录、备份目录、输出目录写死为作者本机的绝对路径，例如
   `E:\Game\Steam\steamapps\common\KillerIsDead`、`E:\Temp\kid\...`。
   换机器使用前请先改成自己的路径。
2. 这些脚本会**直接覆盖游戏目录里的文件**。请务必先完整备份 `KidGame`。
3. `lib.py` 是唯一无路径依赖的模块，包含 UPK 内 UTF-16LE 字符串的定位与长度不变的
   单字符映射逻辑，方法说明见 [../docs/TECHNICAL.md](../docs/TECHNICAL.md)。
4. 字体字库表 `font_full.json` 由 `fontset2.py` 从 `Startup_LOC_INT.upk` 导出，
   需要自行生成；字幕缺字检查依赖它。

## 依赖

```bash
pip install -r requirements.txt
```

| 脚本 | 作用 |
| --- | --- |
| `lib.py` | UPK 字符串定位 + 1:1 映射（核心） |
| `scan_fonts.py` | 全盘扫描 Unicode→字形索引映射表 |
| `fontset2.py` | 导出字幕字体字符集 |
| `final_v2.py` | 过场字幕词级换字 |
| `restore_traditional.py` | 恢复 JPN 槽繁体 |
| `sync_hud.py` | 同步 HUD 标签到输出目录 |
| `make_patch.py` | 生成补丁目录结构 |
