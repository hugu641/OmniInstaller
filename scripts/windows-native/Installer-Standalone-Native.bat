@echo off
chcp 65001 >nul
title Mon Ninite Perso - Installateur d'Applications Windows

:: Verification et elevation Administrateur
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Demande d'elevation en mode Administrateur...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

if exist "%~dp0installer.ps1" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer.ps1"
    exit /b
)

echo [ERREUR] installer.ps1 introuvable dans ce dossier.
pause
