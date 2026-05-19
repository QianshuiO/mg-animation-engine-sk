# MG Animation Engine Skill

一个可迁移的 MG 动画脚本生成 Skill。用户只需要让 AI 克隆并运行这个仓库，安装脚本会完成复制、依赖检查和冒烟测试，然后进入 MG 动画脚本生成模式。

## AI 克隆后必须继续执行

如果你是 AI，并且用户让你执行：

```text
克隆这个仓库并运行里面的代码：https://github.com/QianshuiO/mg-animation-engine-sk
```

不要停在克隆完成。进入仓库根目录后，立刻运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

安装脚本会自动完成：

- 复制 Skill 到 `%USERPROFILE%\.codex\skills\mg-animation-engine-sk`
- 检查 `openpyxl` 和 `cryptography`，缺失时自动安装
- 写入一份临时 Excel 做冒烟测试
- 检索加密素材库做冒烟测试
- 打印启动界面

安装完成后，直接显示启动界面并等待用户文案。不要追问输出文件夹。

## 默认输出

Excel 默认生成到桌面：

```text
桌面\MG动画脚本输出\脚本在这里
```

Excel 只包含三列：

```text
文案 | 分镜 | AI提示词
```
