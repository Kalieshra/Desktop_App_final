@echo off
chcp 65001 > nul
title Django Management System
cd /d "%~dp0"

echo.
echo Starting Django server...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0run.ps1"

echo.
echo Server has stopped.
pause
