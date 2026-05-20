# Set UTF-8 encoding
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

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Refresh-Path {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("Path","User")
}

function Test-RealPython {
    # Returns true only if a real Python 3.x is installed (not Windows Store stub)
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $cmd) { return $false }
    $ver = & python --version 2>&1
    $verStr = "$ver"
    if ($verStr -match "Python 3\.\d+") {
        return $true
    }
    return $false
}

if (-not (Test-Administrator)) {
    Write-Log "This script requires administrator privileges." "ERROR"
    exit 1
}

Write-Log "=== Dependency Installation Started ===" "INFO"

# -----------------------------------------------
# Check if real Python 3 is already installed
# -----------------------------------------------
Refresh-Path

$hasRealPython = Test-RealPython

if ($hasRealPython) {
    $ver = & python --version 2>&1
    Write-Log "Python already installed: $ver" "SUCCESS"
} else {
    Write-Log "Python not found (Windows Store stub does not count). Installing Python 3.13..." "INFO"

    # --- Try winget first (built into Windows 10/11) ---
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Log "Using winget to install Python..." "INFO"
        winget install --id Python.Python.3.13 --silent --accept-package-agreements --accept-source-agreements
        Refresh-Path
    }

    # --- Check if winget install worked ---
    $hasRealPython = Test-RealPython
    if (-not $hasRealPython) {
        Write-Log "winget unavailable or failed. Trying Chocolatey..." "WARNING"

        # Install Chocolatey if missing
        if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
            Write-Log "Installing Chocolatey..." "INFO"
            try {
                Set-ExecutionPolicy Bypass -Scope Process -Force
                [System.Net.ServicePointManager]::SecurityProtocol = `
                    [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
                Invoke-Expression ((New-Object System.Net.WebClient).DownloadString(
                    'https://community.chocolatey.org/install.ps1'))
                Refresh-Path
                Write-Log "Chocolatey installed" "SUCCESS"
            } catch {
                Write-Log "Failed to install Chocolatey: $_" "ERROR"
                exit 1
            }
        }

        choco install python --version=3.13.7 -y --no-progress
        Refresh-Path
    }

    # --- Final check ---
    Refresh-Path
    $hasRealPython = Test-RealPython
    if (-not $hasRealPython) {
        Write-Log "Python installation failed. Please install Python 3.13 manually from:" "ERROR"
        Write-Log "  https://www.python.org/downloads/" "ERROR"
        Write-Log "Make sure to check 'Add Python to PATH' during install." "ERROR"
        Write-Log "Also disable App Execution Aliases: Settings > Apps > Advanced app settings > App execution aliases > turn off python.exe" "ERROR"
        exit 1
    }

    $ver = & python --version 2>&1
    Write-Log "Python installed: $ver" "SUCCESS"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   Python Ready!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Log "=== Dependency Installation Complete ===" "SUCCESS"
exit 0
