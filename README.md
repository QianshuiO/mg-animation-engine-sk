# MG Animation Engine Skill

一个可迁移的 MG 动画脚本生成 Skill。用户只需要复制一句固定提示词，就可以让 AI 克隆仓库、安装 Skill、启动 MG 动画引擎，然后等待文案，并输出只包含三列的 Excel：

```text
文案 | 分镜 | AI提示词
```

默认 Excel 会生成到桌面：

```text
桌面\MG动画脚本输出\脚本在这里
```

## 无脑提示词

复制下面这一句话发给 AI：

```text
请克隆并安装这个 MG 动画引擎仓库 https://github.com/QianshuiO/mg-animation-engine-sk ，安装完成后直接启动 MG 动画引擎，不要问我要文件夹路径，Excel 默认输出到桌面 MG动画脚本输出 文件夹，先回复启动界面并让我发文案。
```

## 手动安装

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
启动MG动画引擎
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
