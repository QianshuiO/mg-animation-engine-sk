param(
    [switch]$SkipSmokeTest,
    [switch]$NoDependencyInstall
)

$ErrorActionPreference = "Stop"

function TextFromCodePoints([int[]]$Codes) {
    return -join ($Codes | ForEach-Object { [char]$_ })
}

function RepeatCodePoint([int]$Code, [int]$Count) {
    return -join (1..$Count | ForEach-Object { [char]$Code })
}

try {
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
} catch {
    # Older hosts may not allow changing console encoding. Installation can continue.
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetRoot = Join-Path $env:USERPROFILE ".codex\skills"
$target = Join-Path $targetRoot "mg-animation-engine-sk"

$requiredPaths = @(
    "SKILL.md",
    "key.auth",
    "db",
    "scripts\search_obsidian_mg.py",
    "scripts\write_mg_excel.py"
)

foreach ($item in $requiredPaths) {
    $path = Join-Path $repoRoot $item
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Repository is incomplete. Missing required path: $item"
    }
}

New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
}

New-Item -ItemType Directory -Path $target -Force | Out-Null

Get-ChildItem -LiteralPath $repoRoot -Force |
    Where-Object { $_.Name -notin @(".git", ".github", "test_output", "mg-animation-engine-sk.zip") } |
    ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force
    }

$pythonCommand = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCommand = @("python")
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCommand = @("py", "-3")
}

function RunPython([string[]]$PythonArgs) {
    if ($script:pythonCommand.Count -gt 1) {
        & $script:pythonCommand[0] $script:pythonCommand[1] @PythonArgs
    } else {
        & $script:pythonCommand[0] @PythonArgs
    }
}

if ($pythonCommand -eq $null) {
    Write-Warning "Python was not found. The skill files were installed, but Excel generation needs Python."
} else {
    RunPython @("-c", "import openpyxl, cryptography") | Out-Null
    if ($LASTEXITCODE -ne 0) {
        if ($NoDependencyInstall) {
            throw "Missing Python packages: openpyxl and/or cryptography."
        }
        Write-Host "Installing Python dependencies..."
        RunPython @("-m", "pip", "install", "-r", (Join-Path $target "requirements.txt"))
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install Python dependencies."
        }
    }

    if (-not $SkipSmokeTest) {
        $smokeRoot = Join-Path ([System.IO.Path]::GetTempPath()) "mg-animation-engine-sk-smoke"
        if (Test-Path -LiteralPath $smokeRoot) {
            Remove-Item -LiteralPath $smokeRoot -Recurse -Force
        }
        New-Item -ItemType Directory -Path $smokeRoot -Force | Out-Null

        $rowsPath = Join-Path $smokeRoot "rows.json"
        $rowJson = '[{"\u6587\u6848":"smoke copy","\u5206\u955c":"smoke shot","AI\u63d0\u793a\u8bcd":"smoke prompt"}]'
        [System.IO.File]::WriteAllText($rowsPath, $rowJson, (New-Object System.Text.UTF8Encoding($false)))

        RunPython @((Join-Path $target "scripts\write_mg_excel.py"), "--rows-json", $rowsPath, "--title-source", "smoke-test", "--project", $smokeRoot) | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Smoke test failed while writing Excel."
        }

        RunPython @((Join-Path $target "scripts\search_obsidian_mg.py"), "--query", "MG", "--top", "1") | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Smoke test failed while searching the bundled MG library."
        }
    }
}

$defaultProject = Join-Path (Join-Path $env:USERPROFILE "Desktop") ("MG" + (TextFromCodePoints @(21160, 30011, 33050, 26412, 36755, 20986)))
$defaultOutput = Join-Path $defaultProject (TextFromCodePoints @(33050, 26412, 22312, 36825, 37324))

Write-Host ""
Write-Host "MG Animation Engine Skill installed:"
Write-Host $target
Write-Host ""
Write-Host "Default Excel output:"
Write-Host $defaultOutput
Write-Host ""
Write-Host "Launch reply:"
Write-Host ((TextFromCodePoints @(9627)) + (RepeatCodePoint 9600 21) + (TextFromCodePoints @(9628)))
Write-Host ("   " + (TextFromCodePoints @(5465, 40, 8640, 8248, 8636, 8246, 41, 5463)) + "  MG MODE")
Write-Host ((TextFromCodePoints @(9625)) + (RepeatCodePoint 9604 21) + (TextFromCodePoints @(9631)))
Write-Host ""
Write-Host ((TextFromCodePoints @(5478, 40, 242, 95, 243, 711, 41, 5476)) + "  MG" + (TextFromCodePoints @(21160, 30011, 24341, 25806, 21551, 21160)))
Write-Host ((TextFromCodePoints @(20316, 32773, 65306)) + "Qianshui")
Write-Host ""
Write-Host (TextFromCodePoints @(25226, 20320, 30340, 25991, 26696, 21457, 25105))
