# Troubleshooting Guide

## Error: "Virtual environment not found" or "Requirements.txt not found"

### Symptoms:
```
The term 'C:\Users\...\Scripts\pip.exe' is not recognized
Cannot find path 'C:\Windows\system32\requirements.txt'
```

### Cause:
The PowerShell script is not running in the correct directory.

### Solution 1: Use Full Setup (Recommended)
1. **Close all PowerShell windows**
2. **Right-click `setup_windows.bat`** → **Run as administrator**
3. Wait for the complete installation

### Solution 2: Manual Directory Fix
If you tried running the PowerShell scripts directly:

1. Open PowerShell as Administrator
2. Navigate to the project folder:
   ```powershell
   cd "C:\Users\dell\Desktop\desktop_2-main"
   ```
3. Run the scripts in order:
   ```powershell
   .\install_dependencies.ps1
   .\setup.ps1
   .\run.ps1
   ```

### Solution 3: Clean Reinstall
If virtual environment is corrupted:

1. Delete the `.venv` folder (if it exists)
2. Delete `setup.log` (if it exists)
3. Right-click `setup_windows.bat` → Run as administrator

## Error: "Python is not installed or not in PATH"

### Solution:
After Chocolatey installs Python, you may need to:

1. **Close and reopen PowerShell** (or restart computer)
2. Verify Python is installed:
   ```powershell
   python --version
   ```
3. If not found, manually add Python to PATH:
   - Search Windows for "Environment Variables"
   - Add `C:\Python313` and `C:\Python313\Scripts` to PATH
   - Restart PowerShell

## Error: "Access Denied" or "Execution Policy"

### Solution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run `setup_windows.bat` as administrator again.

## Error: Port 8000 already in use

### Solution:
1. Find what's using port 8000:
   ```powershell
   netstat -ano | findstr :8000
   ```
2. Kill the process (replace XXXX with PID):
   ```powershell
   taskkill /PID XXXX /F
   ```
3. Or change port in `run.ps1` (line with `runserver 0.0.0.0:8000`)

## Error: Chocolatey installation fails

### Solution 1: Manual Chocolatey Install
Open PowerShell as Administrator:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Solution 2: Manual Software Installation
Skip Chocolatey and install manually:
1. Python 3.13: https://www.python.org/downloads/
2. Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
3. Poppler: https://github.com/oschwartz10612/poppler-windows/releases

## Error: OCR not working

### Check 1: Verify Tesseract installation
```powershell
tesseract --version
```

### Check 2: Verify language files
The `tessdata` folder should contain:
- `ara.traineddata` (Arabic)
- `eng.traineddata` (English)

### Check 3: Test Tesseract
```powershell
tesseract --list-langs
```
Should show: `ara` and `eng`

## Error: Database migrations fail

### Solution:
```powershell
cd "C:\Users\dell\Desktop\desktop_2-main"
.\.venv\Scripts\python manage.py migrate --run-syncdb
```

## Still Having Issues?

### Check the log file:
Open `setup.log` in the project folder for detailed error messages.

### Verify your setup:
```powershell
# Check Python
python --version

# Check virtual environment
Test-Path .venv\Scripts\python.exe

# Check requirements file
Test-Path requirements.txt

# Check Django
.\.venv\Scripts\python -m django --version
```

### Clean slate approach:
1. Delete these if they exist:
   - `.venv` folder
   - `db.sqlite3` file
   - `setup.log` file
   - `.ocr_fallback` file

2. Restart computer (to refresh PATH)

3. Run `setup_windows.bat` as administrator

## Getting Help

When reporting issues, please include:
1. Contents of `setup.log`
2. Output of `python --version`
3. Output of `Get-Location` (your current directory)
4. The exact error message
