#!/bin/bash
# Lancement direct d'OmniInstaller sous Linux
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if [ -f "dist/OmniInstaller-Linux" ]; then
    ./dist/OmniInstaller-Linux "$@"
else
    python3 main.py "$@"
fi
