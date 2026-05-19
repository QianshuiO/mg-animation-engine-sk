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

After the user sends copy, use this skill and the bundled encrypted `db` folder to generate an Excel file with only these three columns:

```text
copy | storyboard | AI prompt
```

The actual Excel writer uses the Chinese column names.

After writing the Excel file, tell the user the clickable Excel path and ask them to send the next piece of copy.
