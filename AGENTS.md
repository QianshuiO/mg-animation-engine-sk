# Agent Instructions

If the user asks you to clone and run this repository, do not stop after cloning.

## Required Run Command

Run this command from the repository root on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

The installer copies the skill into `%USERPROFILE%\.codex\skills\mg-animation-engine-sk`, checks Python dependencies, runs a small Excel smoke test, searches the bundled encrypted MG library, and prints the launch screen.

If `git clone` hangs or fails because of HTTPS credentials, TLS, or pack download timeouts, do not retry indefinitely. Use the GitHub file/content API, an available GitHub connector, or a repository archive fallback to materialize the repository contents, then run the same installer command from the materialized root. The installer validates that required paths are present before copying the skill.

## After Install

If the installer succeeds, treat the MG animation engine as started. Reply to the user with the launch screen printed by the installer, then wait for the user's copy.

Do not ask the user for an output folder. Excel files default to:

```text
Desktop\MG animation script output\scripts here
```

The actual installer uses the Chinese folder names for that default path.

After the user sends copy, use this skill and the bundled encrypted `db` folder to generate a director-level Excel storyboard with exactly these eight columns:

```text
shot no. | duration | narration | RAG reference | visual design | camera/transition | screen text | AI prompt
```

The actual Excel writer uses the Chinese column names:

```text
镜号 | 时长 | 原文/旁白 | RAG参考 | 画面设计 | 镜头运动/转场 | 屏幕文字 | AI提示词
```

For 2-3 minute training or explainer copy, split into about 24-36 producible shots. Use RAG references from the bundled library for the visual pattern column; write `基础推导` only when no suitable note exists.

After writing the Excel file, tell the user the clickable Excel path and ask them to send the next piece of copy.
