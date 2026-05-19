---
name: mg-animation-engine
description: Use when the user asks to install/start the MG animation engine from the GitHub repository, says "启动MG动画引擎", "我要做MG动画", or asks to turn Chinese copy into an MG animation Excel storyboard. The skill uses the bundled encrypted db folder next to this SKILL.md and outputs an Excel file with only 文案、分镜、AI提示词.
---

# MG Animation Engine

把用户文案转成可制作的 MG 动画 Excel 脚本。必须使用本 Skill 同目录下的 `db` 资料库；不要使用任何写死的电脑绝对路径。

## 启动方式

当用户输入以下任意意思时启动：

```text
启动MG动画引擎
我要做MG动画
请克隆并安装 https://github.com/QianshuiO/mg-animation-engine-sk，然后启动 MG 动画引擎
以 https://github.com/QianshuiO/mg-animation-engine-sk 为源，解封、部署、点燃 Qianshui 的 MG 动画引擎；路径归于桌面星图，脚本自入“MG动画脚本输出”，仪式完成后显现启动界面，静候我的文案。
```

先回复下面这段，不要生成 Excel：

```text
▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
   ᕙ(⇀‸↼‶)ᕗ  MG MODE
▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟

ᕦ(ò_óˇ)ᕤ  MG动画引擎启动
作者：Qianshui

把你的文案发我
```

用户随后发来文案后，再开始生成脚本。不要要求用户提供项目文件夹路径；如果用户没有明确指定路径，使用默认输出目录。

## 路径规则

- RAG 资料库固定从当前 Skill 目录解析：`SKILL.md 所在目录/db`。
- 授权密钥固定从当前 Skill 目录解析：`SKILL.md 所在目录/key.auth`。
- Excel 默认输出到：`用户桌面/MG动画脚本输出/脚本在这里`。
- 如果用户明确指定项目文件夹，则输出到：`用户给出的文件夹路径/脚本在这里`。
- 如果 `脚本在这里` 不存在，生成 Excel 时自动创建。
- 任何地方都不要写死 `C:\Users\XU\...` 这类绝对路径，保证复制整个 `sk` 文件夹到另一台电脑后仍可使用。

## RAG 检索

使用：

```bash
python scripts/search_obsidian_mg.py --query "用户文案里的核心词 视觉词" --top 12
```

检索脚本会自动读取同目录授权文件并解密 `db` 内资料。不要直接假设资料库路径。

建议至少检索：

- 文案核心概念词：政策、绩效、薪酬、项目、责任、审批、数据、服务、平台、航空、直升机等。
- 视觉结构词：开场、会议、阶梯、金字塔、数据看板、结构讲解、标题、转场、结尾等。
- 风格约束词：企业培训、MG风格、蓝白、扁平矢量、提示词、负面提示词。

## Excel 输出要求

最终 Excel 只能有三列，列名和顺序固定为：

```text
文案 | 分镜 | AI提示词
```

不得输出镜号、时长、RAG参考、屏幕文字、备注、音效、角色、场景等其它列。

每一行对应一个可制作镜头或画面段落：

- `文案`：保留用户原意，可按镜头轻分段，不要随意改写。
- `分镜`：写清画面元素、人物/图标、构图、运动、转场和节奏。
- `AI提示词`：中文，适合图像或视频生成，包含 16:9、企业培训 MG、蓝白干净背景、扁平矢量商务人物、构图、短标签、负面约束。

## Excel 生成

整理出三列数据后，调用：

```bash
python scripts/write_mg_excel.py --title-source "用户文案开头或主题" --rows-json "rows.json"
```

如果用户明确指定了项目文件夹，再使用：

```bash
python scripts/write_mg_excel.py --project "用户给出的文件夹路径" --title-source "用户文案开头或主题" --rows-json "rows.json"
```

其中 `rows.json` 是数组，每项只包含：

```json
{"文案": "...", "分镜": "...", "AI提示词": "..."}
```

文件名由脚本根据文案自动生成；如果重名，会自动加 `_2`、`_3`。


## 生成完成后的回复

Excel 写入成功后，必须在对话里告诉用户脚本 Excel 的完整路径，并使用可点击文件链接格式。回复要简洁，例如：

```text
脚本 Excel 已生成：C:\示例路径\脚本在这里\标题.xlsx

把你的文案发我
```

最后一句必须固定为：

```text
把你的文案发我
```

这表示本次 MG 动画引擎保持开启状态。用户之后只需要直接发送新的文案，就继续使用默认输出目录或上一次明确指定的项目文件夹生成新的 Excel 脚本；不要要求用户重新输入启动语或文件夹路径，除非用户明确想切换输出文件夹。

## 质量检查

生成前确认：

- 每个抽象概念都有明确视觉载体。
- 分镜不是简单复述文案，而是能指导制作。
- AI提示词不堆长段文字，不要求画面出现大段屏幕字。
- 风格统一为企业 MG、干净蓝白、扁平矢量，除非用户明确要求别的风格。
- Excel 只有 `文案`、`分镜`、`AI提示词` 三列。



