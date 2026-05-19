$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetRoot = Join-Path $env:USERPROFILE ".codex\skills"
$target = Join-Path $targetRoot "mg-animation-engine-sk"

New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
}

New-Item -ItemType Directory -Path $target -Force | Out-Null

Get-ChildItem -LiteralPath $repoRoot -Force |
    Where-Object { $_.Name -notin @(".git", ".github") } |
    ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force
    }

Write-Host ""
Write-Host "MG Animation Engine Skill installed:"
Write-Host $target
Write-Host ""
Write-Host "Start in Codex with:"
Write-Host "我要做MG动画！你的项目文件夹路径"

