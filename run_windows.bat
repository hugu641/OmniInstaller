@echo off
cd /d "%~dp0"
if exist "dist\OmniInstaller.exe" (
    start "" "dist\OmniInstaller.exe"
) else (
    python main.py
)
