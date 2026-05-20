@echo off
chcp 65001 > nul
title Create Desktop Shortcut

set SCRIPT_DIR=%~dp0
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT_NAME=Django Travel System

echo.
echo Creating desktop shortcut...
echo.

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%.lnk'); $s.TargetPath = '%SCRIPT_DIR%START.bat'; $s.IconLocation = 'imageres.dll,14'; $s.Description = 'Django Travel Management System - Smart Launcher'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Save()"

if %errorlevel% equ 0 (
    echo Success! Shortcut created on desktop!
    echo.
    echo Right-click the shortcut and select
    echo "Run as administrator" to start the application.
) else (
    echo Failed to create shortcut
)

echo.
pause
