"""
Widget carte d'application interactive (AppCard).
Affiche les informations d'un logiciel avec case à cocher,
icône, tags et description.
"""

from typing import Dict
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QCheckBox,
)
from PyQt6.QtCore import pyqtSignal, Qt
from src.installer_backend import is_windows


class AppCard(QFrame):
    """Carte graphique représentant une application sélectionnable."""

    sig_toggled = pyqtSignal(dict, bool)  # (app_dict, is_checked)

    def __init__(self, app_data: Dict, parent=None):
        super().__init__(parent)
        self.app_data = app_data
        self.setProperty("class", "AppCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self._setup_ui()
        self._update_style()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Ligne supérieure : Checkbox + Icône + Nom + Badge Catégorie
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(self.app_data.get("recommended", False))
        self.checkbox.toggled.connect(self._on_toggled)
        top_row.addWidget(self.checkbox)

        # Icône / Emoji
        icon_label = QLabel(self.app_data.get("icon", "📦"), self)
        icon_label.setStyleSheet("font-size: 20px;")
        top_row.addWidget(icon_label)

        # Nom de l'application
        self.title_label = QLabel(self.app_data.get("name", ""), self)
        self.title_label.setProperty("class", "AppCardTitle")
        top_row.addWidget(self.title_label, 1)

        # Badge Catégorie
        cat_badge = QLabel(self.app_data.get("category", ""), self)
        cat_badge.setProperty("class", "AppCardCategory")
        top_row.addWidget(cat_badge)

        layout.addLayout(top_row)

        # Description
        desc_text = self.app_data.get("desc", "")
        self.desc_label = QLabel(desc_text, self)
        self.desc_label.setProperty("class", "AppCardDesc")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        # Identifiant du paquet
        pkg_id = self.app_data.get("windows_id") if is_windows() else self.app_data.get("linux_id")
        if not pkg_id:
            pkg_id = self.app_data.get("windows_id") or self.app_data.get("linux_id") or "N/A"
        self.pkg_label = QLabel(f"ID : {pkg_id}", self)
        self.pkg_label.setProperty("class", "AppCardPkgId")
        layout.addWidget(self.pkg_label)

    def mousePressEvent(self, event):
        """Un clic n'importe où sur la carte inverse la sélection."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.checkbox.setChecked(not self.checkbox.isChecked())
            event.accept()
        else:
            super().mousePressEvent(event)

    def _on_toggled(self, checked: bool):
        self._update_style()
        self.sig_toggled.emit(self.app_data, checked)

    def _update_style(self):
        checked = self.checkbox.isChecked()
        self.setProperty("checked", "true" if checked else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def is_checked(self) -> bool:
        return self.checkbox.isChecked()

    def set_checked(self, checked: bool):
        self.checkbox.setChecked(checked)

    def matches_query(self, query: str) -> bool:
        """Vérifie si la carte correspond à la recherche textuelle."""
        if not query:
            return True
        q = query.lower()
        name = self.app_data.get("name", "").lower()
        desc = self.app_data.get("desc", "").lower()
        cat = self.app_data.get("category", "").lower()
        win_id = self.app_data.get("windows_id", "").lower()
        lin_id = self.app_data.get("linux_id", "").lower()
        return (
            q in name
            or q in desc
            or q in cat
            or q in win_id
            or q in lin_id
        )

    def matches_category(self, category: str) -> bool:
        """Vérifie si la carte appartient à la catégorie sélectionnée."""
        if not category or category == "Toutes":
            return True
        return self.app_data.get("category", "") == category
