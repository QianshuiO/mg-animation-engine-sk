# MG Animation Engine Skill

一个可迁移的 MG 动画脚本生成 Skill。用户输入 `我要做MG动画！文件夹路径` 后，Skill 会启动 MG 动画引擎，等待文案，并输出只包含三列的 Excel：

```text
文案 | 分镜 | AI提示词
```

Excel 会生成到用户给出的项目路径：

```text
项目路径\脚本在这里
```

## 一键安装

在 Windows PowerShell 中运行：

```powershell
.\install.ps1
```

安装脚本会把当前仓库复制到：

```text
$env:USERPROFILE\.codex\skills\mg-animation-engine-sk
```

安装完成后，在 Codex 中输入：

```text
我要做MG动画！你的项目文件夹路径
```

启动回复会显示：

```text
▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
   ᕙ(⇀‸↼‶)ᕗ  MG MODE
▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟

ᕦ(ò_óˇ)ᕤ  MG动画引擎启动
作者：Qianshui

把你的文案发我
```

之后直接发送文案即可生成 Excel。生成完成后，AI 会返回 Excel 路径，并以 `把你的文案发我` 结尾；下一次直接发新文案即可继续生成。

## 目录说明

```text
SKILL.md
key.auth
db/
scripts/
references/
agents/
```

- `SKILL.md`：最小可读启动说明。
- `db/`：加密后的 RAG 资料库。
- `key.auth`：同目录授权密钥。
- `scripts/search_obsidian_mg.py`：检索加密 RAG。
- `scripts/write_mg_excel.py`：写入三列 Excel。

## 安全说明

为了实现“克隆后直接可用”，仓库包含 `key.auth`。这意味着加密主要用于防止普通查看和误操作，不适合作为公开仓库里的强安全保护。

