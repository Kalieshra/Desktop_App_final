# Windows Installation Guide

## Quick Start (One-Time Setup)

1. Copy the project folder to your Desktop
2. Right-click `setup_windows.bat` → **Run as administrator**
3. Wait for installation to complete (5-10 minutes)
4. Server will start automatically
5. **Chrome will open automatically** to http://localhost:8000

## For Subsequent Runs

Double-click `run.bat` to start the server - Chrome will open automatically!

## System Requirements

- Windows 10/11
- 2GB free disk space
- Internet connection (for initial setup only)
- Administrator privileges

## What Gets Installed

The setup script will automatically install:

- **Python 3.13** - Programming language
- **Tesseract OCR** - Text recognition engine (with Arabic support)
- **pytesseract** - Windows-compatible OCR library
- **Poppler** - PDF processing utilities
- **Chocolatey** - Package manager for Windows

## OCR Library

This project now uses **pytesseract** - a Windows-compatible OCR library that works seamlessly on all Windows versions:

- ✅ **Easy to install** - No compilation required
- ✅ **Fully compatible** with Windows 10/11
- ✅ **Automatic setup** - Installed via setup_windows.bat
- ✅ **Arabic + English** support included

The installation automatically:
1. Installs Tesseract OCR engine via Chocolatey
2. Installs pytesseract Python library
3. Configures everything to work together

## New Features

- 🌐 **Auto-open Chrome** - Browser opens automatically when server starts
- 📝 **OCR Support** - Extract text from PDFs and images (Arabic + English)
- 🚀 **One-click startup** - Just double-click run.bat

## Troubleshooting

### "Access Denied" or "Permission Error"
→ Run `setup_windows.bat` as administrator (right-click → Run as administrator)

### Port 8000 already in use
→ Close any program using port 8000 or change the port in run.ps1

### Python not found after installation
→ Close and reopen PowerShell/Command Prompt to refresh PATH

### OCR not working
→ Check that tessdata folder contains ara.traineddata and eng.traineddata

### Installation fails
→ Check setup.log for detailed error messages

## Manual Installation (if automated setup fails)

1. **Install Python 3.13**
   - Download from https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **Install Tesseract OCR**
   - Download from https://github.com/UB-Mannheim/tesseract/wiki
   - ✅ Select Arabic language pack during installation
   - Default path: `C:\Program Files\Tesseract-OCR\`

3. **Install Poppler** (for PDF processing)
   - Download from https://github.com/oschwartz10612/poppler-windows/releases
   - Extract and add to PATH

4. **Run setup commands**:
   ```cmd
   python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   .venv\Scripts\python manage.py migrate
   .venv\Scripts\python manage.py runserver
   ```

5. **Open browser**:
   - Navigate to http://localhost:8000

## Features

- **Travel Management** - Track training courses and travel
- **License Management** - Manage facility licenses and inspections
- **Supply Management** - Track purchases and service orders
- **OCR Processing** - Extract text from PDFs and images (Arabic + English)

## Support

For issues, check the log file: `setup.log`
