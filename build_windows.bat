@echo off
chcp 65001 >nul
title Compilation d'OmniInstaller pour Windows (.exe)

echo ==============================================================================
echo ⚡ Compilation d'OmniInstaller pour Windows (.exe)
echo ==============================================================================
echo.

cd /d "%~dp0"

echo [1/3] Verification de Python...
set "PYTHON_CMD="
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        py --version >nul 2>&1
        if %errorlevel% equ 0 (
            set "PYTHON_CMD=py"
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Installez Python depuis https://www.python.org/ ou via Winget :
    echo winget install Python.Python.3.12
    pause
    exit /b 1
)

echo [2/3] Installation des dependances...
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer les dependances.
    pause
    exit /b 1
)

echo [3/3] Creation de l'executable avec PyInstaller...
%PYTHON_CMD% build.py

echo.
echo ==============================================================================
echo 🎉 TERMINE ! L'executable est dans le dossier 'dist\OmniInstaller.exe'
echo ==============================================================================
echo.
pause
