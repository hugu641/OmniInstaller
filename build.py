#!/usr/bin/env python3
"""
Script de compilation multi-plateforme avec PyInstaller.
Génère :
- Un fichier exécutable unique .exe sous Windows (dist/OmniInstaller.exe)
- Un fichier exécutable autonome sous Linux (dist/OmniInstaller-Linux)
"""

import os
import sys
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_WINDOWS = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")


def build():
    print("=" * 60)
    print("⚡ Compilation d'OmniInstaller avec PyInstaller")
    print(f"Plateforme cible : {'Windows' if IS_WINDOWS else 'Linux'}")
    print("=" * 60)

    # Vérification de PyInstaller
    try:
        import PyInstaller
        print(f"✔ PyInstaller détecté (version {PyInstaller.__version__})")
    except ImportError:
        print("❌ PyInstaller n'est pas installé. Exécutez : pip install pyinstaller")
        sys.exit(1)

    # Chemins
    main_script = os.path.join(BASE_DIR, "main.py")
    icon_png = os.path.join(BASE_DIR, "assets", "icon.png")
    icon_ico = os.path.join(BASE_DIR, "assets", "icon.ico")
    dist_dir = os.path.join(BASE_DIR, "dist")
    build_dir = os.path.join(BASE_DIR, "build")

    # Options PyInstaller
    sep = ";" if IS_WINDOWS else ":"
    data_arg = f"{icon_png}{sep}assets"

    target_name = "OmniInstaller" if IS_WINDOWS else "OmniInstaller-Linux"
    icon_file = icon_ico if (IS_WINDOWS and os.path.exists(icon_ico)) else icon_png

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name", target_name,
        "--add-data", data_arg,
    ]

    if os.path.exists(icon_file):
        cmd.extend(["--icon", icon_file])

    cmd.append(main_script)

    print("\nExécution de la commande PyInstaller :")
    print(" ".join(cmd))
    print("-" * 60)

    result = subprocess.run(cmd, cwd=BASE_DIR)
    if result.returncode == 0:
        print("\n" + "=" * 60)
        ext = ".exe" if IS_WINDOWS else ""
        output_file = os.path.join(dist_dir, f"{target_name}{ext}")
        print(f"🎉 SUCCÈS ! L'exécutable a été généré dans :")
        print(f"   👉 {output_file}")
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"   Taille : {size_mb:.2f} Mo")
        print("=" * 60)
    else:
        print("\n❌ Erreur lors de la compilation.")
        sys.exit(result.returncode)


if __name__ == "__main__":
    build()
