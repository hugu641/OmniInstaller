#!/usr/bin/env python3
"""
OmniInstaller - Installateur d'Applications Moderne & Multi-plateforme (Windows & Linux).
Point d'entrée principal de l'application.
"""

import sys
import os

# S'assurer que le répertoire racine est dans sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from src.ui.main_window import MainWindow


def main():
    # Optimisation affichage haute résolution (High DPI)
    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("OmniInstaller")
    app.setApplicationDisplayName("OmniInstaller")
    app.setOrganizationName("OmniInstaller")
    app.setApplicationVersion("1.0.0")

    icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
