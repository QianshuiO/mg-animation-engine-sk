# Agent Instructions

If the user asks you to clone and run this repository, do not stop after cloning.

Run this command from the repository root on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

The installer copies the skill into `%USERPROFILE%\.codex\skills\mg-animation-engine-sk`, checks Python dependencies, runs a small Excel smoke test, searches the bundled encrypted MG library, and prints the launch screen.

If the installer succeeds, treat the MG animation engine as started and reply with this launch screen:

```text
▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
   ᕙ(⇀‸↼‶)ᕗ  MG MODE
▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟

ᕦ(ò_óˇ)ᕤ  MG动画引擎启动
作者：Qianshui

把你的文案发我
```

Do not ask the user for an output folder. Excel files default to:

```text
Desktop\MG动画脚本输出\脚本在这里
```

After the user sends copy, use this skill and the bundled encrypted `db` folder to generate an Excel file with only these three columns:

```text
文案 | 分镜 | AI提示词
```

After writing the Excel file, tell the user the clickable Excel path and end with:

```text
把你的文案发我
```
