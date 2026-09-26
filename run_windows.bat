@echo off
cd /d "%~dp0"
if exist "dist\OmniInstaller.exe" (
    start "" "dist\OmniInstaller.exe"
) else (
    .venv\Scripts\python.exe main.py
)
