# Quick Fix for Your Current Error

## What Happened?
The PowerShell scripts ran from the wrong directory (`C:\Windows\system32` instead of your project folder). This has been fixed in the updated scripts.

## How to Fix It Now

### Option 1: Simple Clean Restart (Recommended)

1. **Delete the broken virtual environment folder:**
   - Go to: `C:\Users\dell\Desktop\desktop_2-main`
   - Delete the `.venv` folder (if it exists)
   - Delete `setup.log` (if it exists)

2. **Close ALL PowerShell windows**

3. **Run setup again:**
   - Right-click `setup_windows.bat`
   - Select **"Run as administrator"**
   - Wait for completion

### Option 2: Manual Fix (If Option 1 doesn't work)

Open PowerShell **as Administrator** and run these commands one by one:

```powershell
# Navigate to project directory
cd "C:\Users\dell\Desktop\desktop_2-main"

# Verify you're in the right place
Get-Location
# Should show: C:\Users\dell\Desktop\desktop_2-main

# Check if Python is installed
python --version
# Should show: Python 3.13.x

# If Python not found, install it:
choco install python --version=3.13.7 -y

# Close and reopen PowerShell as Administrator, then continue:
cd "C:\Users\dell\Desktop\desktop_2-main"

# Delete old venv if exists
Remove-Item -Path .venv -Recurse -Force -ErrorAction SilentlyContinue

# Create new virtual environment
python -m venv .venv

# Verify it was created
Test-Path .venv\Scripts\python.exe
# Should show: True

# Install packages
.\.venv\Scripts\pip install --upgrade pip
.\.venv\Scripts\pip install Django==5.1.5
.\.venv\Scripts\pip install django-bootstrap5
.\.venv\Scripts\pip install openpyxl
.\.venv\Scripts\pip install Pillow
.\.venv\Scripts\pip install pdf2image
.\.venv\Scripts\pip install pytesseract
.\.venv\Scripts\pip install whitenoise

# Run migrations
.\.venv\Scripts\python manage.py migrate

# Start server
.\.venv\Scripts\python manage.py runserver 0.0.0.0:8000
```

## What Was Fixed?

The scripts now include `Set-Location $PSScriptRoot` at the beginning, which ensures they always run in the correct directory (where the script file is located), not where PowerShell was started from.

## Files Updated:
- ✅ `setup.ps1` - Fixed directory issue
- ✅ `install_dependencies.ps1` - Fixed directory issue
- ✅ `run.ps1` - Fixed directory issue + better error messages

## After Fix is Complete

Once working, you can simply double-click `run.bat` to start the server.

## Need More Help?

See `TROUBLESHOOTING.md` for detailed solutions to common problems.
