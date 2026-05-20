[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location $PSScriptRoot

$LogFile = Join-Path $PSScriptRoot "setup.log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$Timestamp [$Level] $Message" | Out-File -FilePath $LogFile -Append -Encoding UTF8
    switch ($Level) {
        "ERROR"   { Write-Host $Message -ForegroundColor Red }
        "WARNING" { Write-Host $Message -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $Message -ForegroundColor Green }
        default   { Write-Host $Message }
    }
}

function Refresh-Path {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("Path","User")
}

Write-Log "=== Project Setup Started ===" "INFO"
Refresh-Path

# -----------------------------------------------
# Locate real Python (skip Windows Store stubs)
# -----------------------------------------------
$pythonExe = $null

# Check PATH but verify it is a real Python, not a Windows Store stub
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pyCmd) {
    $ver = & python --version 2>&1
    $verStr = "$ver"
    if ($verStr -match "Python 3\.\d+") {
        $pythonExe = $pyCmd.Source
    }
}

# Common manual install locations as fallback
if (-not $pythonExe) {
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "${env:ProgramFiles}\Python313\python.exe",
        "${env:ProgramFiles}\Python312\python.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) {
            $ver = & "$c" --version 2>&1
            if ("$ver" -match "Python 3\.\d+") {
                $pythonExe = $c
                break
            }
        }
    }
}

if (-not $pythonExe) {
    Write-Log "Python not found. Please run START.bat again to install Python first." "ERROR"
    Write-Log "Tip: Disable App Execution Aliases in Settings > Apps > Advanced app settings." "WARNING"
    exit 1
}

Write-Log "Using Python: $pythonExe" "INFO"

# -----------------------------------------------
# Create virtual environment
# -----------------------------------------------
$venvPath   = Join-Path $PSScriptRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$venvPip    = Join-Path $venvPath "Scripts\pip.exe"

if (-not (Test-Path $venvPython)) {
    Write-Log "Creating virtual environment..." "INFO"
    & $pythonExe -m venv "$venvPath"
    if ($LASTEXITCODE -ne 0) {
        Write-Log "Failed to create virtual environment." "ERROR"
        exit 1
    }
    Write-Log "Virtual environment created" "SUCCESS"
} else {
    Write-Log "Virtual environment already exists" "SUCCESS"
}

# -----------------------------------------------
# Upgrade pip
# -----------------------------------------------
Write-Log "Upgrading pip..." "INFO"
& $venvPython -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Log "Warning: Could not upgrade pip" "WARNING"
}

# -----------------------------------------------
# Install packages from requirements.txt
# -----------------------------------------------
$requirementsPath = Join-Path $PSScriptRoot "requirements.txt"
if (-not (Test-Path $requirementsPath)) {
    Write-Log "requirements.txt not found!" "ERROR"
    exit 1
}

Write-Log "Installing packages from requirements.txt..." "INFO"

# Filter out psycopg2 (only needed for PostgreSQL, we use SQLite on Windows)
$filtered = (Get-Content $requirementsPath) | Where-Object {
    $_ -notmatch "psycopg2" -and $_.Trim() -ne "" -and $_ -notmatch "^\s*#"
} | ForEach-Object { ($_ -replace "#.*","").Trim() } | Where-Object { $_ -ne "" }

foreach ($pkg in $filtered) {
    Write-Log "  Installing $pkg..." "INFO"
    & $venvPip install $pkg --quiet 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "  Failed to install: $pkg" "ERROR"
        exit 1
    }
}
Write-Log "All packages installed" "SUCCESS"

# -----------------------------------------------
# Run database migrations
# -----------------------------------------------
Write-Log "Running database migrations..." "INFO"
& $venvPython manage.py migrate --noinput 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Log "Migration failed" "ERROR"
    exit 1
}
Write-Log "Migrations complete" "SUCCESS"

# -----------------------------------------------
# Create backup directory
# -----------------------------------------------
$backupDir = Join-Path $PSScriptRoot "backup"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Write-Log "Backup directory created" "SUCCESS"
}

# -----------------------------------------------
# Collect static files
# -----------------------------------------------
Write-Log "Collecting static files..." "INFO"
& $venvPython manage.py collectstatic --noinput 2>&1 | Out-Null
Write-Log "Static files ready" "SUCCESS"

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Log "=== Project Setup Complete ===" "INFO"
exit 0
