# MG Animation Engine Skill

A portable Codex skill for generating director-level MG animation storyboard Excel files.

The intended user test prompt is:

```text
Clone this repository and run the code inside it: https://github.com/QianshuiO/mg-animation-engine-sk
```

## Quick Start For AI Agents

After cloning or otherwise materializing this repository, run this from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

Do not stop after `git clone`. The installer is the project entry point.

If `git clone` hangs or fails because of HTTPS credentials, TLS, or pack download timeouts, do not retry indefinitely. Use the GitHub file/content API, an available GitHub connector, or a repository archive fallback to materialize the files, then run the same installer command.

## What The Installer Does

- Copies the skill to `%USERPROFILE%\.codex\skills\mg-animation-engine-sk`
- Verifies the required repository paths exist
- Checks Python availability
- Installs missing Python packages from `requirements.txt` unless `-NoDependencyInstall` is passed
- Runs an Excel writer smoke test in the temp directory
- Runs an encrypted library search smoke test
- Prints the launch screen

## Output

By default, generated Excel files go to the user's Desktop under the Chinese MG animation output folder. The workbook is an 8-column production storyboard:

```text
shot no. | duration | narration | RAG reference | visual design | camera/transition | screen text | AI prompt
```

The actual Excel file uses Chinese column names.

The skill is tuned for production-ready director storyboards:

- 60-90 second policy videos usually use 12-22 shots.
- 2-3 minute training/explainer videos usually use 24-36 shots.
- Each main shot should bind to a reusable RAG visual pattern when possible.
- The Excel writer still accepts the old three-column smoke-test JSON and maps it into the new 8-column schema.

## Useful Installer Flags

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -SkipSmokeTest
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -NoDependencyInstall
```
