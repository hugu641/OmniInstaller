"""
Boîte de dialogue de recherche et d'ajout d'applications personnalisées.
Permet d'interroger les dépôts en ligne (Flathub / Winget)
ou d'ajouter directement un identifiant de paquet avec un design moderne.
"""

from typing import Dict, List
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTabWidget,
    QWidget,
    QScrollArea,
    QFrame,
    QProgressBar,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from src.installer_backend import is_windows, is_linux
from src.search_service import SearchWorker
from src.ui.icon_manager import IconManager
from src.i18n import tr


class SearchResultItem(QFrame):
    """Ligne représentant un résultat de recherche en ligne avec rendu moderne."""

    sig_add = pyqtSignal(dict)

    def __init__(self, data: Dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #475569;
                background-color: #24334D;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(14)

        # Conteneur logo officiel ou monogramme
        logo_container = QFrame(self)
        logo_container.setFixedSize(42, 42)
        logo_container.setStyleSheet("""
            background-color: #0F172A;
            border: 1px solid #334155;
            border-radius: 8px;
        """)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel(logo_container)
        icon_lbl.setPixmap(IconManager.get_app_pixmap(data, size=32))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(icon_lbl)
        layout.addWidget(logo_container)

        # Infos
        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)

        name_lbl = QLabel(data.get("name", "Application"), self)
        name_lbl.setStyleSheet("color: #F1F5F9; font-size: 13.5px; font-weight: 600; background: transparent;")
        info_layout.addWidget(name_lbl)

        desc_lbl = QLabel(data.get("summary", ""), self)
        desc_lbl.setStyleSheet("color: #94A3B8; font-size: 11px; background: transparent;")
        desc_lbl.setWordWrap(True)
        info_layout.addWidget(desc_lbl)

        id_lbl = QLabel(f"{data.get('source', 'dépôt')} • {data.get('id')}", self)
        id_lbl.setStyleSheet("color: #64748B; font-size: 10px; font-family: 'Consolas', monospace; background: transparent;")
        info_layout.addWidget(id_lbl)

        layout.addLayout(info_layout, 1)

        # Bouton Ajouter
        btn_add = QPushButton(f"  {tr('add')}", self)
        btn_add.setIcon(IconManager.get_ui_icon("plus", 14))
        btn_add.setIconSize(QSize(14, 14))
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: #06281E;
                border: none;
                border-radius: 6px;
                padding: 7px 16px;
                font-weight: 700;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #059669;
                color: #FFFFFF;
            }
        """)
        btn_add.clicked.connect(self._on_add)
        layout.addWidget(btn_add)

    def _on_add(self):
        self.sig_add.emit(self.data)


class SearchAddDialog(QDialog):
    """Dialogue modal permettant de chercher et ajouter des applications."""

    sig_app_added = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("store_title"))
        self.resize(700, 560)
        self.setModal(True)

        self._search_worker = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        tabs = QTabWidget(self)
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #1E293B;
                background-color: #0F172A;
                border-radius: 8px;
                padding: 8px;
            }
            QTabBar::tab {
                background-color: transparent;
                color: #64748B;
                padding: 9px 18px;
                margin-right: 6px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: 600;
                font-size: 12.5px;
            }
            QTabBar::tab:selected {
                background-color: #1E293B;
                color: #F1F5F9;
                border-bottom: 2px solid #10B981;
            }
        """)

        # Onglet 1 : Recherche en ligne
        tab_online = QWidget()
        self._setup_online_tab(tab_online)
        source_name = "Flathub" if is_linux() else "Winget"
        tabs.addTab(tab_online, tr("tab_online", source=source_name))
        tabs.setTabIcon(0, IconManager.get_ui_icon("globe", 16))

        # Onglet 2 : Ajout manuel
        tab_manual = QWidget()
        self._setup_manual_tab(tab_manual)
        tabs.addTab(tab_manual, tr("tab_manual"))
        tabs.setTabIcon(1, IconManager.get_ui_icon("code", 16))

        layout.addWidget(tabs)

        # Bouton Fermer
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        btn_close = QPushButton(tr("close"), self)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1E293B;
                color: #F1F5F9;
            }
        """)
        btn_close.clicked.connect(self.accept)
        bottom_row.addWidget(btn_close)
        layout.addLayout(bottom_row)

    def _setup_online_tab(self, parent_widget: QWidget):
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        # Barre de recherche
        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText(tr("search_ph"))
        self.search_input.addAction(IconManager.get_ui_icon("search", 16), QLineEdit.ActionPosition.LeadingPosition)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 7px;
                padding: 7px 12px;
                color: #F1F5F9;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #10B981;
                background-color: #1A2742;
            }
        """)
        self.search_input.returnPressed.connect(self._start_search)
        search_row.addWidget(self.search_input, 1)

        btn_search = QPushButton(f"  {tr('search_btn')}", self)
        btn_search.setIcon(IconManager.get_ui_icon("search", 15))
        btn_search.setIconSize(QSize(15, 15))
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: #06281E;
                border: none;
                border-radius: 7px;
                padding: 8px 18px;
                font-weight: 700;
                font-size: 12.5px;
            }
            QPushButton:hover {
                background-color: #059669;
                color: #FFFFFF;
            }
        """)
        btn_search.clicked.connect(self._start_search)
        search_row.addWidget(btn_search)
        layout.addLayout(search_row)

        # Indicateur de chargement
        self.loading_bar = QProgressBar(self)
        self.loading_bar.setRange(0, 0)
        self.loading_bar.setFixedHeight(4)
        self.loading_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1E293B;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #10B981;
                border-radius: 2px;
            }
        """)
        self.loading_bar.setVisible(False)
        layout.addWidget(self.loading_bar)

        self.status_lbl = QLabel(tr("status_hint"), self)
        self.status_lbl.setStyleSheet("color: #64748B; font-size: 11.5px;")
        layout.addWidget(self.status_lbl)

        # Zone de défilement des résultats
        self.results_scroll = QScrollArea(self)
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setStyleSheet("border: none; background-color: transparent;")

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(8)
        self.results_layout.addStretch()

        self.results_scroll.setWidget(self.results_container)
        layout.addWidget(self.results_scroll, 1)

    def _setup_manual_tab(self, parent_widget: QWidget):
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        info_lbl = QLabel(tr("manual_info"), self)
        info_lbl.setStyleSheet("color: #94A3B8; font-size: 11.5px;")
        layout.addWidget(info_lbl)

        input_style = """
            QLineEdit {
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 7px 12px;
                color: #F1F5F9;
                font-size: 12.5px;
            }
            QLineEdit:focus {
                border-color: #10B981;
                background-color: #1A2742;
            }
        """

        # Nom
        lbl1 = QLabel(tr("f_name"), self)
        lbl1.setStyleSheet("color: #F1F5F9; font-weight: 600; font-size: 12px;")
        layout.addWidget(lbl1)
        self.manual_name = QLineEdit(self)
        self.manual_name.setPlaceholderText(tr("f_name_ph"))
        self.manual_name.setStyleSheet(input_style)
        layout.addWidget(self.manual_name)

        # Identifiant
        lbl2 = QLabel(tr("f_id"), self)
        lbl2.setStyleSheet("color: #F1F5F9; font-weight: 600; font-size: 12px;")
        layout.addWidget(lbl2)
        self.manual_id = QLineEdit(self)
        self.manual_id.setPlaceholderText(tr("f_id_ph"))
        self.manual_id.setStyleSheet(input_style)
        layout.addWidget(self.manual_id)

        # Catégorie
        lbl3 = QLabel(tr("f_cat"), self)
        lbl3.setStyleSheet("color: #F1F5F9; font-weight: 600; font-size: 12px;")
        layout.addWidget(lbl3)
        self.manual_cat = QLineEdit(self)
        self.manual_cat.setText(tr("custom_cat"))
        self.manual_cat.setStyleSheet(input_style)
        layout.addWidget(self.manual_cat)

        # Description
        lbl4 = QLabel(tr("f_desc"), self)
        lbl4.setStyleSheet("color: #F1F5F9; font-weight: 600; font-size: 12px;")
        layout.addWidget(lbl4)
        self.manual_desc = QLineEdit(self)
        self.manual_desc.setPlaceholderText(tr("f_desc_ph"))
        self.manual_desc.setStyleSheet(input_style)
        layout.addWidget(self.manual_desc)

        # Bouton Ajouter
        btn_add_manual = QPushButton(f"  {tr('add_catalog_btn')}", self)
        btn_add_manual.setIcon(IconManager.get_ui_icon("plus", 16))
        btn_add_manual.setIconSize(QSize(16, 16))
        btn_add_manual.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_manual.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: #06281E;
                border: none;
                border-radius: 7px;
                padding: 10px 20px;
                font-weight: 700;
                font-size: 13px;
                margin-top: 8px;
            }
            QPushButton:hover {
                background-color: #059669;
                color: #FFFFFF;
            }
        """)
        btn_add_manual.clicked.connect(self._add_manual_app)
        layout.addWidget(btn_add_manual)
        layout.addStretch()

    def _start_search(self):
        query = self.search_input.text().strip()
        if not query:
            return

        self.loading_bar.setVisible(True)
        self.status_lbl.setText(tr("searching", q=query))

        # Nettoyer les anciens résultats
        self._clear_results()

        self._search_worker = SearchWorker(query)
        self._search_worker.sig_results.connect(self._on_search_results)
        self._search_worker.sig_error.connect(self._on_search_error)
        self._search_worker.start()

    def _on_search_results(self, results: List[Dict]):
        self.loading_bar.setVisible(False)
        if not results:
            self.status_lbl.setText(tr("no_result"))
            return

        self.status_lbl.setText(tr("results_found", n=len(results)))
        for item_data in results:
            item_widget = SearchResultItem(item_data, self.results_container)
            item_widget.sig_add.connect(self._on_app_selected)
            self.results_layout.insertWidget(self.results_layout.count() - 1, item_widget)

    def _on_search_error(self, err_msg: str):
        self.loading_bar.setVisible(False)
        self.status_lbl.setText(tr("search_error", err=err_msg))

    def _clear_results(self):
        while self.results_layout.count() > 1:
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _on_app_selected(self, app_data: Dict):
        new_app = {
            "id": app_data.get("id").replace(".", "_").lower(),
            "name": app_data.get("name"),
            "category": tr("custom_cat"),
            "desc": app_data.get("summary", ""),
            "icon": app_data.get("icon", "📦"),
            "windows_id": app_data.get("windows_id") or app_data.get("id"),
            "linux_id": app_data.get("linux_id") or app_data.get("id"),
            "linux_type": "flatpak",
            "recommended": True,
        }
        self.sig_app_added.emit(new_app)
        QMessageBox.information(
            self,
            tr("added_t"),
            tr("added_m", name=new_app['name']),
        )

    def _add_manual_app(self):
        name = self.manual_name.text().strip()
        pkg_id = self.manual_id.text().strip()
        cat = self.manual_cat.text().strip() or tr("custom_cat")
        desc = self.manual_desc.text().strip() or tr("pkg_word", pkg=pkg_id)

        if not name or not pkg_id:
            QMessageBox.warning(self, tr("required_t"), tr("required_m"))
            return

        new_app = {
            "id": pkg_id.replace(".", "_").lower(),
            "name": name,
            "category": cat,
            "desc": desc,
            "icon": "📦",
            "windows_id": pkg_id,
            "linux_id": pkg_id,
            "linux_type": "flatpak",
            "recommended": True,
        }
        self.sig_app_added.emit(new_app)
        QMessageBox.information(
            self,
            tr("added_t"),
            tr("added_m", name=name),
        )
        self.manual_name.clear()
        self.manual_id.clear()
        self.manual_desc.clear()
