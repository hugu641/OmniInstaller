"""
Fenetre principale OmniInstaller — style "Pro / Slate Nordic" v4.
Sobre, industriel, inspire de Raycast / GitHub Desktop / VS Code.
Palette #0F172A / #1E293B / #334155, accent emeraude #10B981 (CTA uniquement).
"""

import os
from typing import List, Dict

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QFrame,
    QProgressBar,
    QTextEdit,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon, QPixmap, QResizeEvent

from src.catalog import get_catalog, CATEGORIES
from src.installer_backend import (
    SystemDetector,
    InstallationWorker,
    is_windows,
    get_current_os_name,
)
from src.ui.app_card import AppCard
from src.ui.search_dialog import SearchAddDialog
from src.ui.language_dialog import LanguageDialog
from src.ui.styles import MAIN_STYLESHEET
from src.ui.icon_manager import BASE_DIR, IconManager
from src.i18n import tr, tr_category, set_language, get_language


CATEGORY_ICONS = {
    "Navigateurs":            "globe",
    "Communication":          "message",
    "Gaming":                 "gamepad",
    "Musique & Medias":       "music",
    "Musique & Médias":       "music",
    "Developpement":          "code",
    "Développement":          "code",
    "Utilitaires & Securite": "shield",
    "Utilitaires & Sécurité": "shield",
    "Graphisme & Creation":   "palette",
    "Graphisme & Création":   "palette",
    "Bureautique":            "file_text",
}

SIDEBAR_WIDTH = 200
CARD_MIN_WIDTH = 300


def _mk_nav(text: str, parent, icon: str) -> QPushButton:
    btn = QPushButton(text, parent)
    btn.setProperty("navbtn", "1")
    btn.setProperty("active", "false")
    # Icones fines type Feather/Tabler, ton discret
    btn.setIcon(IconManager.get_ui_icon(icon, 15, "#94A3B8"))
    btn.setIconSize(QSize(15, 15))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn


def _mk_quick(text: str, parent, icon: str) -> QPushButton:
    btn = QPushButton(text, parent)
    btn.setProperty("quickbtn", "1")
    btn.setIcon(IconManager.get_ui_icon(icon, 13, "#94A3B8"))
    btn.setIconSize(QSize(13, 13))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn


def _activate(btn: QPushButton, active: bool):
    btn.setProperty("active", "true" if active else "false")
    btn.style().unpolish(btn)
    btn.style().polish(btn)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OmniInstaller")
        self.resize(1240, 840)
        self.setMinimumSize(980, 680)

        icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet(MAIN_STYLESHEET)

        self.apps_data: List[Dict] = get_catalog()
        self.app_cards: List[AppCard] = []
        self.current_category = "Toutes"
        self.active_worker = None
        self.nav_buttons: Dict[str, QPushButton] = {}
        self.installed_ids: set = set()
        self._cols = 3

        self._build_ui()
        self._populate_cards()
        self._update_counts()
        QTimer.singleShot(300, self._check_backend)

    # ──────────────────────────────────────────────
    # Construction
    # ──────────────────────────────────────────────

    def _build_ui(self):
        root_w = QWidget(self)
        self.setCentralWidget(root_w)
        root = QHBoxLayout(root_w)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())

        right_w = QWidget(self)
        right = QVBoxLayout(right_w)
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(0)

        right.addWidget(self._build_header())
        right.addWidget(self._build_grid_area(), 1)
        right.addWidget(self._build_dock())

        root.addWidget(right_w, 1)

    # ── Sidebar compacte ──────────────────────────

    def _build_sidebar(self) -> QFrame:
        sb = QFrame(self)
        sb.setObjectName("Sidebar")
        lay = QVBoxLayout(sb)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Marque
        brand_w = QWidget(sb)
        brand_l = QHBoxLayout(brand_w)
        brand_l.setContentsMargins(14, 16, 14, 12)
        brand_l.setSpacing(10)

        logo_path = os.path.join(BASE_DIR, "assets", "icon.png")
        if os.path.exists(logo_path):
            logo = QLabel(brand_w)
            logo.setPixmap(
                QPixmap(logo_path).scaled(
                    28, 28,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            brand_l.addWidget(logo)

        txt = QVBoxLayout()
        txt.setSpacing(1)
        t = QLabel("OmniInstaller", brand_w)
        t.setObjectName("BrandTitle")
        txt.addWidget(t)
        self.lbl_brand_sub = QLabel(tr("brand_subtitle"), brand_w)
        self.lbl_brand_sub.setObjectName("BrandSubtitle")
        txt.addWidget(self.lbl_brand_sub)
        brand_l.addLayout(txt, 1)
        lay.addWidget(brand_w)

        # Separateur fin
        sep = QFrame(sb)
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #1E293B; max-height: 1px; border: none;")
        sep.setFixedHeight(1)
        lay.addWidget(sep)

        # Section Navigation
        self.lbl_nav_section = self._sec_lbl(tr("nav_section"), sb)
        lay.addWidget(self.lbl_nav_section)

        for key, icon in [
            ("Recommandes",   "star"),
            ("Toutes",        "apps"),
            ("Selectionnes",  "check_circle"),
        ]:
            btn = _mk_nav(self._nav_text(key), sb, icon)
            btn.clicked.connect(lambda _c, k=key: self._on_cat(k))
            if key == "Toutes":
                _activate(btn, True)
            if key == "Selectionnes":
                self.btn_sel_view = btn
            self.nav_buttons[key] = btn
            lay.addWidget(btn)

        # Section Categories
        self.lbl_cat_section = self._sec_lbl(tr("cat_section"), sb)
        lay.addWidget(self.lbl_cat_section)

        cs = QScrollArea(sb)
        cs.setWidgetResizable(True)
        cs.setStyleSheet(
            "QScrollArea{border:none;background:transparent;}"
            "QWidget{background:transparent;}"
        )
        cs.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        cc = QWidget()
        cc.setStyleSheet("background:transparent;")
        cl = QVBoxLayout(cc)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(1)

        for cat in CATEGORIES[1:]:
            icon_key = CATEGORY_ICONS.get(cat, "apps")
            count = sum(1 for a in self.apps_data if a.get("category") == cat)
            btn = _mk_nav(self._nav_text(cat, count), cc, icon_key)
            btn.clicked.connect(lambda _c, c=cat: self._on_cat(c))
            self.nav_buttons[cat] = btn
            cl.addWidget(btn)

        cl.addStretch()
        cs.setWidget(cc)
        lay.addWidget(cs, 1)

        # Boite systeme
        lay.addWidget(self._build_sys_box(sb))

        # Bouton Paramètres (langue) — pied de sidebar
        self.btn_settings = _mk_nav(f"  {tr('settings')}", sb, "settings")
        self.btn_settings.clicked.connect(self._open_settings)
        lay.addWidget(self.btn_settings)

        return sb

    def _nav_text(self, key: str, count: int = 0) -> str:
        """Libellé traduit d'un bouton de navigation (clé interne inchangée)."""
        if key == "Recommandes":
            label = tr("nav_recommended")
        elif key == "Toutes":
            label = tr("nav_all")
        elif key == "Selectionnes":
            sel = sum(1 for c in self.app_cards if c.is_selected())
            label = tr("nav_selected", n=sel)
        else:
            # Clé = nom de catégorie français du catalogue
            label = tr_category(key).replace("&", "&&")
            return f"  {label}  ({count})"
        return f"  {label}"

    def _sec_lbl(self, text: str, parent) -> QLabel:
        lbl = QLabel(text, parent)
        lbl.setObjectName("SidebarSectionHeader")
        return lbl

    def _build_sys_box(self, parent) -> QFrame:
        box = QFrame(parent)
        box.setObjectName("SidebarSystemBox")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(10, 9, 10, 9)
        lay.setSpacing(8)

        row = QHBoxLayout()
        row.setSpacing(7)

        os_key = "windows" if is_windows() else "linux"
        ico = QLabel(box)
        ico.setPixmap(IconManager.get_ui_pixmap(os_key, 14))
        ico.setFixedSize(14, 14)
        row.addWidget(ico)

        self.lbl_os = QLabel(get_current_os_name(), box)
        self.lbl_os.setObjectName("SystemStatusLabel")
        row.addWidget(self.lbl_os, 1)

        self.lbl_badge = QLabel("···", box)
        self.lbl_badge.setObjectName("SystemStatusBadgeReady")
        row.addWidget(self.lbl_badge)
        lay.addLayout(row)

        self.btn_store = QPushButton(f"  {tr('add_app')}", box)
        self.btn_store.setObjectName("SearchOnlineBtn")
        self.btn_store.setIcon(IconManager.get_ui_icon("plus", 13, "#94A3B8"))
        self.btn_store.setIconSize(QSize(13, 13))
        self.btn_store.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_store.clicked.connect(self._open_store)
        lay.addWidget(self.btn_store)

        return box

    # ── Header : titre + recherche fine + actions ──

    def _build_header(self) -> QFrame:
        h = QFrame(self)
        h.setObjectName("ContentHeader")

        lay = QVBoxLayout(h)
        lay.setContentsMargins(24, 18, 24, 14)
        lay.setSpacing(10)

        # Titre de page (hiérarchie VS Code / GitHub Desktop)
        self.lbl_page_title = QLabel(tr("page_title"), h)
        self.lbl_page_title.setObjectName("PageTitle")
        lay.addWidget(self.lbl_page_title)

        self.lbl_page_sub = QLabel(tr("page_subtitle"), h)
        self.lbl_page_sub.setObjectName("PageSubtitle")
        lay.addWidget(self.lbl_page_sub)

        # Barre de recherche — fine, longue, bordure #334155, loupe discrète
        self.search_bar = QLineEdit(h)
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setPlaceholderText(tr("search_placeholder"))
        self.search_bar.addAction(
            IconManager.get_ui_icon("search", 14, "#64748B"),
            QLineEdit.ActionPosition.LeadingPosition,
        )
        self.search_bar.textChanged.connect(self._filter)
        lay.addWidget(self.search_bar)

        # Ligne actions secondaires
        row = QHBoxLayout()
        row.setSpacing(8)

        self.btn_all = _mk_quick(f"  {tr('select_all')}", h, "check_all")
        self.btn_all.clicked.connect(self._check_all)
        row.addWidget(self.btn_all)

        self.btn_none = _mk_quick(f"  {tr('clear')}", h, "uncheck_all")
        self.btn_none.clicked.connect(self._uncheck_all)
        row.addWidget(self.btn_none)

        self.btn_rec = QPushButton(f"  {tr('recommended')}", h)
        self.btn_rec.setObjectName("BtnRecommended")
        self.btn_rec.setIcon(IconManager.get_ui_icon("star", 13, "#94A3B8"))
        self.btn_rec.setIconSize(QSize(13, 13))
        self.btn_rec.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_rec.clicked.connect(self._select_recommended)
        row.addWidget(self.btn_rec)

        row.addStretch()

        self.lbl_results = QLabel("", h)
        self.lbl_results.setObjectName("ResultsCountLabel")
        row.addWidget(self.lbl_results)

        lay.addLayout(row)

        return h

    # ── Zone cartes — espaces négatifs généreux ───

    def _build_grid_area(self) -> QWidget:
        wrapper = QWidget(self)
        wrapper.setStyleSheet("background-color: #0F172A;")
        wlay = QVBoxLayout(wrapper)
        wlay.setContentsMargins(0, 0, 0, 0)
        wlay.setSpacing(0)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.cards_w = QWidget()
        self.cards_w.setStyleSheet("background-color: #0F172A;")
        self.grid = QGridLayout(self.cards_w)
        self.grid.setContentsMargins(24, 20, 24, 24)
        self.grid.setSpacing(12)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll.setWidget(self.cards_w)
        wlay.addWidget(self.scroll, 1)

        self.empty_w = self._build_empty()
        self.empty_w.hide()
        wlay.addWidget(self.empty_w)

        return wrapper

    def _build_empty(self) -> QWidget:
        w = QWidget(self)
        w.setStyleSheet("background-color: #0F172A;")
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(40, 64, 40, 64)
        lay.setSpacing(10)

        ico = QLabel(w)
        ico.setPixmap(IconManager.get_ui_pixmap("search", 36, "#334155"))
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(ico)

        self.lbl_empty_title = QLabel(tr("empty_title"), w)
        self.lbl_empty_title.setStyleSheet("font-size: 14px; font-weight: 600; color: #94A3B8; background: transparent;")
        self.lbl_empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.lbl_empty_title)

        self.lbl_empty_desc = QLabel(tr("empty_desc"), w)
        self.lbl_empty_desc.setStyleSheet("font-size: 12px; color: #64748B; background: transparent;")
        self.lbl_empty_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.lbl_empty_desc)

        self.btn_empty_add = QPushButton(f"  {tr('add_app')}", w)
        self.btn_empty_add.setObjectName("SearchOnlineBtn")
        self.btn_empty_add.setIcon(IconManager.get_ui_icon("plus", 13, "#94A3B8"))
        self.btn_empty_add.setIconSize(QSize(13, 13))
        self.btn_empty_add.setFixedWidth(230)
        self.btn_empty_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_empty_add.clicked.connect(self._open_store)
        lay.addWidget(self.btn_empty_add, alignment=Qt.AlignmentFlag.AlignCenter)

        return w

    # ── Dock installation ─────────────────────────

    def _build_dock(self) -> QFrame:
        dock = QFrame(self)
        dock.setObjectName("InstallDock")

        lay = QVBoxLayout(dock)
        lay.setContentsMargins(24, 14, 24, 14)
        lay.setSpacing(10)

        row = QHBoxLayout()
        row.setSpacing(10)
        row.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        info = QVBoxLayout()
        info.setSpacing(2)

        self.lbl_dock_title = QLabel(tr("dock_ready"), dock)
        self.lbl_dock_title.setObjectName("DockSummaryTitle")
        info.addWidget(self.lbl_dock_title)

        self.lbl_dock_sub = QLabel(tr("dock_none"), dock)
        self.lbl_dock_sub.setObjectName("DockSummarySubtitle")
        info.addWidget(self.lbl_dock_sub)

        row.addLayout(info, 1)

        self.btn_log = QPushButton(f"  {tr('console')}", dock)
        self.btn_log.setObjectName("ToggleLogButton")
        self.btn_log.setIcon(IconManager.get_ui_icon("terminal", 13, "#94A3B8"))
        self.btn_log.setIconSize(QSize(13, 13))
        self.btn_log.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_log.clicked.connect(self._toggle_log)
        row.addWidget(self.btn_log)

        self.btn_cancel = QPushButton(f"  {tr('stop')}", dock)
        self.btn_cancel.setObjectName("CancelButton")
        self.btn_cancel.setIcon(IconManager.get_ui_icon("stop", 13, "#94A3B8"))
        self.btn_cancel.setIconSize(QSize(13, 13))
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self._cancel)
        row.addWidget(self.btn_cancel)

        self.btn_install = QPushButton(tr("install_n", n=0), dock)
        self.btn_install.setObjectName("InstallButton")
        self.btn_install.setIcon(IconManager.get_ui_icon("rocket", 15, "#06281E"))
        self.btn_install.setIconSize(QSize(15, 15))
        self.btn_install.setEnabled(False)
        self.btn_install.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_install.clicked.connect(self._install)
        row.addWidget(self.btn_install)

        lay.addLayout(row)

        self.progress = QProgressBar(dock)
        self.progress.setObjectName("InstallProgressBar")
        self.progress.setValue(0)
        self.progress.setVisible(False)
        lay.addWidget(self.progress)

        self.log_console = QTextEdit(dock)
        self.log_console.setObjectName("LogConsole")
        self.log_console.setReadOnly(True)
        self.log_console.setFixedHeight(120)
        self.log_console.setVisible(False)
        lay.addWidget(self.log_console)

        return dock

    # ──────────────────────────────────────────────
    # Logique
    # ──────────────────────────────────────────────

    def _populate_cards(self):
        for c in self.app_cards:
            self.grid.removeWidget(c)
            c.deleteLater()
        self.app_cards.clear()

        for app in self.apps_data:
            card = AppCard(app, self.cards_w)
            if app.get("id") in self.installed_ids:
                card.set_installed(True)
            card.sig_toggled.connect(self._on_toggled)
            self.app_cards.append(card)

        self._filter()

    def _filter(self):
        query = self.search_bar.text().strip().lower()

        for c in self.app_cards:
            self.grid.removeWidget(c)
            c.setParent(None)

        cols = max(1, self._cols)
        visible: List[AppCard] = [
            c for c in self.app_cards
            if c.matches_category(self.current_category) and c.matches_query(query)
        ]

        for i, c in enumerate(visible):
            c.setParent(self.cards_w)
            c.show()
            self.grid.addWidget(c, i // cols, i % cols)

        for c in set(self.app_cards) - set(visible):
            c.hide()

        if visible:
            self.empty_w.hide()
            self.scroll.show()
        else:
            self.scroll.hide()
            self.empty_w.show()

        sel = sum(1 for c in self.app_cards if c.is_selected())
        self.lbl_results.setText(tr("results_vs", v=len(visible), s=sel))

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        available = self.width() - SIDEBAR_WIDTH - 48
        cols = max(1, available // CARD_MIN_WIDTH)
        cols = min(cols, 4)
        if cols != self._cols:
            self._cols = cols
            self._filter()

    def _check_backend(self):
        info = SystemDetector.get_status_info()
        status = info.get("status")
        backend = info.get("backend", "").upper()
        msg = info.get("message", "")

        if status == "ready":
            self.lbl_badge.setText(f"● {backend}")
            self.lbl_badge.setObjectName("SystemStatusBadgeReady")
        else:
            self.lbl_badge.setText(f"● {backend} {tr('backend_missing')}")
            self.lbl_badge.setObjectName("SystemStatusBadgeWarn")
        self.lbl_badge.setToolTip(msg)
        self.lbl_badge.style().unpolish(self.lbl_badge)
        self.lbl_badge.style().polish(self.lbl_badge)

    def _on_cat(self, cat: str):
        self.current_category = cat
        for name, btn in self.nav_buttons.items():
            _activate(btn, name == cat)
        self._filter()

    def _check_all(self):
        q = self.search_bar.text().strip().lower()
        for c in self.app_cards:
            if c.matches_category(self.current_category) and c.matches_query(q):
                if not c.is_installed():
                    c.set_selected(True)
        self._update_counts()

    def _uncheck_all(self):
        q = self.search_bar.text().strip().lower()
        for c in self.app_cards:
            if c.matches_category(self.current_category) and c.matches_query(q):
                c.set_selected(False)
        self._update_counts()

    def _select_recommended(self):
        for c in self.app_cards:
            if not c.is_installed():
                c.set_selected(bool(c.app_data.get("recommended", False)))
        self._update_counts()

    def _on_toggled(self, _app: Dict, _checked: bool):
        self._update_counts()
        if self.current_category == "Selectionnes":
            self._filter()

    def _update_counts(self):
        sel = sum(1 for c in self.app_cards if c.is_selected())
        self.btn_sel_view.setText(self._nav_text("Selectionnes"))
        self.btn_install.setText(f"  {tr('install_n', n=sel)}")
        self.btn_install.setEnabled(sel > 0)

        if sel == 0:
            self.lbl_dock_sub.setText(tr("dock_none"))
        elif sel == 1:
            self.lbl_dock_sub.setText(tr("dock_one"))
        else:
            self.lbl_dock_sub.setText(tr("dock_many", n=sel))

        q = self.search_bar.text().strip().lower() if hasattr(self, "search_bar") else ""
        vis = sum(
            1 for c in self.app_cards
            if c.matches_category(self.current_category) and c.matches_query(q)
        )
        self.lbl_results.setText(tr("results_vs", v=vis, s=sel))

    def _mark_installed_by_name(self, name: str):
        for c in self.app_cards:
            if c.app_data.get("name") == name and not c.is_installed():
                c.set_installed(True)
                self.installed_ids.add(c.app_data.get("id", ""))
        self._update_counts()

    def _toggle_log(self):
        v = self.log_console.isVisible()
        self.log_console.setVisible(not v)
        self.btn_log.setText(f"  {tr('hide_console')}" if not v else f"  {tr('console')}")

    def _install(self):
        selected = [c.app_data for c in self.app_cards if c.is_selected()]
        if not selected:
            QMessageBox.information(self, tr("no_selection_t"), tr("no_selection_m"))
            return

        self.log_console.setVisible(True)
        self.btn_log.setText(f"  {tr('hide_console')}")
        self.log_console.clear()
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.progress.setMaximum(len(selected))
        self.btn_install.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.lbl_dock_title.setText(tr("installing_ct", c=0, t=len(selected)))

        self.active_worker = InstallationWorker(selected)
        self.active_worker.sig_log.connect(self._on_log)
        self.active_worker.sig_progress.connect(self._on_progress)
        self.active_worker.sig_current_app.connect(
            lambda name: self.lbl_dock_title.setText(tr("installing_name", name=name))
        )
        self.active_worker.sig_finished.connect(self._on_done)
        self.active_worker.start()

    def _cancel(self):
        if self.active_worker and self.active_worker.isRunning():
            reply = QMessageBox.question(
                self, tr("confirm_t"), tr("confirm_m"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.active_worker.cancel()
                self.btn_cancel.setEnabled(False)
                self.lbl_dock_title.setText(tr("stopping"))

    def _on_log(self, msg: str, level: str):
        colors = {"info": "#94A3B8", "success": "#10B981", "warning": "#F59E0B", "error": "#EF4444"}
        col = colors.get(level, "#94A3B8")
        self.log_console.append(f'<span style="color:{col};">{msg}</span>')
        # Marquage progressif des succès : "✔ <Nom> installé avec succès !"
        if level == "success" and "installé avec succès" in msg:
            try:
                name = msg.split("✔", 1)[1].split("installé avec succès")[0].strip()
                if name:
                    self._mark_installed_by_name(name)
            except Exception:
                pass

    def _on_progress(self, cur: int, total: int):
        self.progress.setMaximum(total)
        self.progress.setValue(cur)

    def _on_done(self, summary: Dict):
        total = summary.get("total", 0)
        ok = summary.get("succeeded", 0)
        fail = summary.get("failed", 0)
        dur = summary.get("duration", 0.0)

        self.btn_install.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.progress.setValue(total)

        if fail == 0:
            self.lbl_dock_title.setText(tr("done_dock_ok", ok=ok, t=total, d=f"{dur:.0f}"))
            QMessageBox.information(self, tr("done_ok_t"), tr("done_ok_m", ok=ok))
        else:
            self.lbl_dock_title.setText(tr("done_dock_err", ok=ok, fail=fail))
            QMessageBox.warning(self, tr("done_err_t"),
                tr("done_err_m", ok=ok, fail=fail))
        self._update_counts()

    def _open_store(self):
        dialog = SearchAddDialog(self)
        dialog.sig_app_added.connect(self._on_app_added)
        dialog.exec()

    def _on_app_added(self, new_app: Dict):
        new_app["recommended"] = False
        self.apps_data.insert(0, new_app)
        self._populate_cards()
        self._update_counts()
        QMessageBox.information(self, tr("app_added_t"),
            tr("app_added_m", name=new_app.get('name')))

    # ── Paramètres / langue ───────────────────────

    def _open_settings(self):
        dialog = LanguageDialog(self, mode="settings", current=get_language())
        if dialog.exec():
            set_language(dialog.selected_lang)
            self._retranslate_ui()

    def _retranslate_ui(self):
        """Réapplique la langue à toute l'interface, sans redémarrage."""
        self.lbl_brand_sub.setText(tr("brand_subtitle"))
        self.lbl_nav_section.setText(tr("nav_section"))
        self.lbl_cat_section.setText(tr("cat_section"))
        for key, btn in self.nav_buttons.items():
            if key in ("Recommandes", "Toutes", "Selectionnes"):
                btn.setText(self._nav_text(key))
            else:
                count = sum(1 for a in self.apps_data if a.get("category") == key)
                btn.setText(self._nav_text(key, count))
        self.btn_settings.setText(f"  {tr('settings')}")
        self.btn_store.setText(f"  {tr('add_app')}")
        self.lbl_page_title.setText(tr("page_title"))
        self.lbl_page_sub.setText(tr("page_subtitle"))
        self.search_bar.setPlaceholderText(tr("search_placeholder"))
        self.btn_all.setText(f"  {tr('select_all')}")
        self.btn_none.setText(f"  {tr('clear')}")
        self.btn_rec.setText(f"  {tr('recommended')}")
        self.lbl_empty_title.setText(tr("empty_title"))
        self.lbl_empty_desc.setText(tr("empty_desc"))
        self.btn_empty_add.setText(f"  {tr('add_app')}")
        if not (self.active_worker and self.active_worker.isRunning()):
            self.lbl_dock_title.setText(tr("dock_ready"))
        self.btn_log.setText(
            f"  {tr('hide_console')}" if self.log_console.isVisible()
            else f"  {tr('console')}"
        )
        self.btn_cancel.setText(f"  {tr('stop')}")
        self._populate_cards()
        self._update_counts()
        self._check_backend()
