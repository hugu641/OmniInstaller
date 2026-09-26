"""
Carte d'application (AppCard) — style "Pro / Slate Nordic" v4.
Sans case à cocher : logo, titre, description courte, badge catégorie,
et bouton d'action directe (Installer / Sélectionné / Installé).
Bords 8px, bordure 1px #334155, sans ombre portée.
"""

from typing import Dict

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QMouseEvent

from src.installer_backend import is_windows
from src.ui.icon_manager import IconManager
from src.i18n import tr, tr_category


class AppCard(QFrame):
    """Carte d'application cliquable avec action directe."""

    sig_toggled = pyqtSignal(dict, bool)

    def __init__(self, app_data: Dict, parent=None):
        super().__init__(parent)
        self.app_data = app_data
        self._selected: bool = bool(app_data.get("recommended", False))
        self._installed: bool = False
        self.setObjectName("AppCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._build()
        self._refresh()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(8)

        # ── Ligne principale : logo + titre/meta + action ──
        top = QHBoxLayout()
        top.setSpacing(12)
        top.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Logo — conteneur 44x44, fond #0F172A, bordure #334155
        logo_f = QFrame(self)
        logo_f.setObjectName("LogoContainer")
        logo_f.setFixedSize(44, 44)
        logo_inner = QVBoxLayout(logo_f)
        logo_inner.setContentsMargins(0, 0, 0, 0)
        logo_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_lbl = QLabel(logo_f)
        self.logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_lbl.setPixmap(IconManager.get_app_pixmap(self.app_data, size=32))
        logo_inner.addWidget(self.logo_lbl)
        top.addWidget(logo_f)

        # Titre + catégorie
        meta = QVBoxLayout()
        meta.setSpacing(3)
        meta.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.title_lbl = QLabel(self.app_data.get("name", ""), self)
        self.title_lbl.setObjectName("CardAppTitle")
        meta.addWidget(self.title_lbl)

        cat_text = tr_category(self.app_data.get("category", ""))
        self.cat_lbl = QLabel(cat_text, self)
        self.cat_lbl.setObjectName("CardCategoryBadge")
        meta.addWidget(self.cat_lbl)

        top.addLayout(meta, 1)

        # Action directe — bouton ou badge installé
        self.action_btn = QPushButton(tr("card_install"), self)
        self.action_btn.setObjectName("CardActionButton")
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.action_btn.clicked.connect(self._on_action_clicked)
        top.addWidget(self.action_btn)

        self.installed_badge = QLabel(tr("card_installed"), self)
        self.installed_badge.setObjectName("CardInstalledBadge")
        self.installed_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.installed_badge.hide()
        top.addWidget(self.installed_badge)

        lay.addLayout(top)

        # ── Description courte (2 lignes max, ton secondaire) ──
        desc = (self.app_data.get("desc", "") or "").strip()
        if desc:
            self.desc_lbl = QLabel(desc, self)
            self.desc_lbl.setObjectName("CardAppDesc")
            self.desc_lbl.setWordWrap(True)
            self.desc_lbl.setMaximumHeight(38)
            lay.addWidget(self.desc_lbl)

        # ── Ligne basse : package ID mono + recommandation discrète ──
        bottom = QHBoxLayout()
        bottom.setSpacing(8)

        pkg = (
            self.app_data.get("windows_id") if is_windows()
            else self.app_data.get("linux_id")
        ) or self.app_data.get("windows_id") or self.app_data.get("linux_id") or ""

        if pkg:
            self.pkg_lbl = QLabel(pkg, self)
            self.pkg_lbl.setObjectName("CardPkgId")
            self.pkg_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            bottom.addWidget(self.pkg_lbl, 1)

        if self.app_data.get("recommended"):
            rec = QLabel(tr("card_recommended"), self)
            rec.setObjectName("CardRecommendedBadge")
            bottom.addWidget(rec)

        if pkg or self.app_data.get("recommended"):
            lay.addLayout(bottom)

    # ── Interactions ──────────────────────────────

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and not self._installed:
            self.set_selected(not self._selected)
            event.accept()
        else:
            super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return) and not self._installed:
            self.set_selected(not self._selected)
            event.accept()
        else:
            super().keyPressEvent(event)

    def _on_action_clicked(self):
        if self._installed:
            return
        self.set_selected(not self._selected)

    def _refresh(self):
        self.setProperty("selected", "true" if self._selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

        if self._installed:
            self.action_btn.hide()
            self.installed_badge.show()
            return

        self.installed_badge.hide()
        self.action_btn.show()
        if self._selected:
            self.action_btn.setText(tr("card_selected"))
        else:
            self.action_btn.setText(tr("card_install"))
        self.action_btn.setProperty("selected", "true" if self._selected else "false")
        self.style().unpolish(self.action_btn)
        self.style().polish(self.action_btn)

    # ── API ───────────────────────────────────────

    def is_selected(self) -> bool:
        return self._selected

    def set_selected(self, v: bool):
        v = bool(v)
        if self._installed:
            return
        if v == self._selected:
            self._refresh()
            return
        self._selected = v
        self._refresh()
        self.sig_toggled.emit(self.app_data, self._selected)

    def set_installed(self, v: bool = True):
        """Marque la carte comme installée : badge discret, action désactivée."""
        self._installed = bool(v)
        if self._installed:
            self._selected = False
        self._refresh()

    def is_installed(self) -> bool:
        return self._installed

    # Compatibilité avec l'ancien modèle à cases à cocher
    def is_checked(self) -> bool:
        return self.is_selected()

    def set_checked(self, v: bool):
        self.set_selected(v)

    def matches_query(self, q: str) -> bool:
        if not q:
            return True
        return any(
            q in (self.app_data.get(k) or "").lower()
            for k in ("name", "desc", "category", "windows_id", "linux_id")
        )

    def matches_category(self, cat: str) -> bool:
        if not cat or cat in ("Toutes", "Toutes les applications"):
            return True
        if cat == "Recommandes":
            return bool(self.app_data.get("recommended"))
        if cat == "Selectionnes":
            return self.is_selected()
        return self.app_data.get("category", "") == cat
