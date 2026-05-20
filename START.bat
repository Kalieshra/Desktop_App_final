@echo off
chcp 65001 > nul
title Django Management System

REM ============================================
REM Fix working directory (any drive)
REM ============================================
cd /d "%~dp0"

REM ============================================
REM Self-elevate to Administrator if needed
REM ============================================
net session >nul 2>&1
if %ERRORLEVEL% neq 0 (
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs -WorkingDirectory '%~dp0'"
    exit /b
)

REM ============================================
REM First Time Setup - install if no venv
REM ============================================
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo.
    echo ============================================
    echo    First Time Setup
    echo ============================================
    echo.
    echo Installing Python and required packages...
    echo This takes about 5-10 minutes.
    echo.
    pause

    echo.
    echo [1/2] Installing Python 3.13...
    powershell -ExecutionPolicy Bypass -File "%~dp0install_dependencies.ps1"
    if %ERRORLEVEL% neq 0 (
        echo.
        echo ERROR: Failed to install Python. See messages above.
        echo Check setup.log for details.
        pause
        exit /b 1
    )

    echo.
    echo [2/2] Setting up project environment...
    powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
    if %ERRORLEVEL% neq 0 (
        echo.
        echo ERROR: Setup failed. See messages above.
        echo Check setup.log for details.
        pause
        exit /b 1
    )

    echo.
    echo ============================================
    echo    Setup Complete! Starting server...
    echo ============================================
    echo.
)

REM ============================================
REM Start the server
REM ============================================
echo.
echo Starting Django server...
echo Chrome will open automatically.
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0run.ps1"

echo.
echo Server has stopped.
pause
exit /b 0
