@echo off
chcp 65001 >nul
title OmniInstaller - Installateur d'Applications

cd /d "%~dp0"

:: 1. Si l'exécutable compilé est présent, le lancer directement
if exist "dist\OmniInstaller.exe" (
    start "" "dist\OmniInstaller.exe" %*
    exit /b
)

:: 2. Si Python est installé, tenter de lancer la version PyQt6
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python -c "import PyQt6" >nul 2>&1
    if %errorlevel% equ 0 (
        start "" pythonw main.py
        exit /b
    )
)

:: 3. Sinon, lancer le script PowerShell natif intégré (sans dépendances)
echo [INFO] Lancement de l'installateur Windows natif...
if exist "scripts\windows-native\Installer-Apps-Windows.bat" (
    call "scripts\windows-native\Installer-Apps-Windows.bat"
    exit /b
)
if exist "scripts\windows-native\installer.ps1" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\windows-native\installer.ps1"
    exit /b
)

echo [ERREUR] Impossible de trouver l'installateur.
pause
