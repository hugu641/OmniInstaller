#!/bin/bash
# ==============================================================================
# Script de compilation OmniInstaller pour Linux
# ==============================================================================
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "⚡ Préparation de l'environnement de compilation..."
python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || python3 -m pip install -r requirements.txt || true

echo "🚀 Lancement de la compilation avec PyInstaller..."
python3 build.py

echo "✔ Terminé ! Votre exécutable est disponible dans le dossier 'dist/'."
