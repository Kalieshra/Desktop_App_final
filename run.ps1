[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location $PSScriptRoot
$env:DJANGO_DEBUG = "1"

$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host ""
    Write-Host "ERROR: Virtual environment not found." -ForegroundColor Red
    Write-Host "Please run START.bat again to set up the project." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Run any pending migrations
Write-Host "Checking database..." -ForegroundColor Gray
& $venvPython manage.py migrate --noinput 2>&1 | Out-Null

# Create backup directory if missing
$backupDir = Join-Path $PSScriptRoot "backup"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}

# Show server info
Clear-Host
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   Django Management System" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "   URL: http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Open browser after 3 seconds (in background)
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 3
    $chromePaths = @(
        "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    )
    $opened = $false
    foreach ($p in $chromePaths) {
        if (Test-Path $p) {
            Start-Process -FilePath $p -ArgumentList "http://localhost:8000"
            $opened = $true
            break
        }
    }
    if (-not $opened) {
        Start-Process "http://localhost:8000"
    }
} | Out-Null

# Run Django in foreground (keeps window open)
& $venvPython manage.py runserver 0.0.0.0:8000
