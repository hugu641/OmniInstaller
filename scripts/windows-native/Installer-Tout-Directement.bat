@echo off
chcp 65001 >nul
title Installation Automatique de Toutes tes Applications (Mode Direct)

:: Elevation Administrateur
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Demande des privileges administrateur...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo ================================================================
echo ⚡ INSTALLATION AUTOMATIQUE DES APPLICATIONS WINDOWS (WINGET)
echo ================================================================
echo.
echo Les applications suivantes vont etre installees :
echo - Brave Browser
echo - Discord
echo - Telegram Desktop
echo - Steam
echo - Epic Games Launcher
echo - Deezer
echo - VLC Media Player
echo - Visual Studio Code
echo - Git for Windows
echo - Node.js LTS
echo - 7-Zip
echo.
echo ================================================================
echo.

set APPS=Brave.Brave Discord.Discord Telegram.TelegramDesktop Valve.Steam EpicGames.EpicGamesLauncher Deezer.Deezer VideoLAN.VLC Microsoft.VisualStudioCode Git.Git OpenJS.NodeJS.LTS 7zip.7zip

for %%A in (%APPS%) do (
    echo [WINGET] Installation de %%A en cours...
    winget install --id "%%A" --exact --silent --accept-source-agreements --accept-package-agreements --disable-interactivity
    echo.
)

echo.
echo ================================================================
echo 🎉 Toutes les applications ont ete traitees !
echo ================================================================
echo.
pause
