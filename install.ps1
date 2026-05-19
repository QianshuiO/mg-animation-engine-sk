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
Write-Host "MG animation engine is ready. Default Excel output:"
Write-Host "$env:USERPROFILE\Desktop\MG动画脚本输出\脚本在这里"
Write-Host ""
Write-Host "Launch reply:"
Write-Host "▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜"
Write-Host "   ᕙ(⇀‸↼‶)ᕗ  MG MODE"
Write-Host "▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟"
Write-Host ""
Write-Host "ᕦ(ò_óˇ)ᕤ  MG动画引擎启动"
Write-Host "作者：Qianshui"
Write-Host ""
Write-Host "把你的文案发我"
