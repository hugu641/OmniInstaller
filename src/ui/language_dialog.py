"""
Dialogue de choix de langue — style Slate Nordic.

Deux modes :
- mode="first"    : premier lancement, pas d'annulation, bouton Continuer.
- mode="settings" : depuis le bouton Paramètres, boutons Enregistrer/Annuler.

Chaque langue est affichée dans sa propre langue (Français, English,
Español, Deutsch, Italiano, Português) : pas besoin de traduction.
Le titre/sous-titre utilise la langue présélectionnée et se met à jour
en direct quand on clique sur une autre langue.
"""

from typing import Dict, Optional

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt, QSize

from src.i18n import LANGUAGES, tr, get_language
from src.ui.icon_manager import IconManager
from src.ui.styles import MAIN_STYLESHEET


class LanguageDialog(QDialog):
    """Sélecteur de langue (premier lancement ou paramètres)."""

    def __init__(self, parent=None, mode: str = "first",
                 current: Optional[str] = None):
        super().__init__(parent)
        self.mode = mode
        self.selected_lang: str = current or get_language()
        self._preview_lang: str = self.selected_lang
        self._lang_buttons: Dict[str, QPushButton] = {}

        self.setMinimumWidth(380)
        self.setModal(True)
        if mode == "first":
            # Pas de fermeture sans choix au premier lancement
            self.setWindowFlags(
                self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint
            )

        self._build()
        self._refresh_texts()

    # ── Construction ──────────────────────────────

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 22, 24, 22)
        lay.setSpacing(10)

        # Icône globe
        globe = QLabel(self)
        globe.setPixmap(IconManager.get_ui_pixmap("globe", 32, "#10B981"))
        globe.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(globe)

        self.lbl_title = QLabel(self)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet(
            "font-size: 16px; font-weight: 700; color: #F1F5F9; background: transparent;"
        )
        lay.addWidget(self.lbl_title)

        self.lbl_sub = QLabel(self)
        self.lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_sub.setWordWrap(True)
        self.lbl_sub.setStyleSheet(
            "font-size: 12px; color: #64748B; background: transparent;"
        )
        lay.addWidget(self.lbl_sub)

        lay.addSpacing(6)

        # Liste des langues (une par ligne, pleine largeur)
        for code, name in LANGUAGES.items():
            btn = QPushButton(f"  {name}", self)
            btn.setProperty("langbtn", "1")
            btn.setProperty("selected", "false")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(36)
            btn.clicked.connect(lambda _c, c=code: self._pick(c))
            self._lang_buttons[code] = btn
            lay.addWidget(btn)

        self.lbl_hint = QLabel(self)
        self.lbl_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_hint.setStyleSheet(
            "font-size: 11px; color: #64748B; background: transparent;"
        )
        lay.addWidget(self.lbl_hint)

        lay.addSpacing(4)

        # Boutons bas
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addStretch()

        if self.mode == "settings":
            self.btn_cancel = QPushButton(tr("cancel"), self)
            self.btn_cancel.setObjectName("SearchOnlineBtn")
            self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_cancel.clicked.connect(self.reject)
            row.addWidget(self.btn_cancel)

            self.btn_ok = QPushButton(tr("save"), self)
        else:
            self.btn_ok = QPushButton("Continuer", self)

        self.btn_ok.setObjectName("LangConfirmButton")
        self.btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ok.setStyleSheet("""
            QPushButton#LangConfirmButton {
                background-color: #10B981;
                color: #06281E;
                border: none;
                border-radius: 7px;
                padding: 9px 26px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton#LangConfirmButton:hover {
                background-color: #059669;
                color: #FFFFFF;
            }
        """)
        self.btn_ok.clicked.connect(self.accept)
        row.addWidget(self.btn_ok)
        lay.addLayout(row)

        self.setStyleSheet(MAIN_STYLESHEET + """
            QPushButton[langbtn="1"] {
                text-align: left;
                background-color: #1E293B;
                color: #CBD5E1;
                border: 1px solid #334155;
                border-radius: 7px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton[langbtn="1"]:hover {
                border-color: #475569;
                color: #FFFFFF;
            }
            QPushButton[langbtn="1"][selected="true"] {
                background-color: #10B981;
                color: #06281E;
                border: 1px solid #10B981;
                font-weight: 700;
            }
            QPushButton[langbtn="1"][selected="true"]:hover {
                background-color: #059669;
                color: #FFFFFF;
            }
        """)
        self._mark_selected()

    # ── Logique ───────────────────────────────────

    def _pick(self, code: str):
        """Sélection + aperçu immédiat du titre dans cette langue."""
        self.selected_lang = code
        self._preview_lang = code
        self._mark_selected()
        self._refresh_texts()

    def _mark_selected(self):
        for code, btn in self._lang_buttons.items():
            is_sel = code == self.selected_lang
            btn.setProperty("selected", "true" if is_sel else "false")
            # Pastille ✓ : repère visible même sans distinguer les teintes
            btn.setText(f"✓  {LANGUAGES[code]}" if is_sel else f"  {LANGUAGES[code]}")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _refresh_texts(self):
        """Titre/sous-titre affichés dans la langue d'aperçu."""
        import src.i18n as i18n_mod
        prev = i18n_mod.get_language()
        i18n_mod._current = self._preview_lang
        try:
            if self.mode == "settings":
                self.setWindowTitle(tr("settings_title"))
                self.lbl_title.setText(tr("settings_title"))
                self.lbl_sub.setText(f"{tr('language')} · {tr('language_hint')}")
                self.lbl_hint.setText("")
                self.btn_ok.setText(tr("save"))
                if hasattr(self, "btn_cancel"):
                    self.btn_cancel.setText(tr("cancel"))
            else:
                self.setWindowTitle(tr("lang_title"))
                self.lbl_title.setText(tr("lang_title"))
                self.lbl_sub.setText(tr("lang_subtitle"))
                self.lbl_hint.setText("")
                self.btn_ok.setText(tr("lang_continue"))
        finally:
            i18n_mod._current = prev
