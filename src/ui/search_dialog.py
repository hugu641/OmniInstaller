"""
Boîte de dialogue de recherche et d'ajout d'applications personnalisées.
Permet d'interroger les dépôts en ligne (Flathub / Winget)
ou d'ajouter directement un identifiant de paquet.
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
from PyQt6.QtCore import pyqtSignal, Qt
from src.installer_backend import is_windows, is_linux
from src.search_service import SearchWorker


class SearchResultItem(QFrame):
    """Ligne représentant un résultat de recherche en ligne."""

    sig_add = pyqtSignal(dict)

    def __init__(self, data: Dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px 10px;
            }
            QFrame:hover {
                border-color: #6366f1;
                background-color: #24324a;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(10)

        # Icône
        icon_lbl = QLabel(data.get("icon", "📦"), self)
        icon_lbl.setStyleSheet("font-size: 18px;")
        layout.addWidget(icon_lbl)

        # Infos
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_lbl = QLabel(f"<b>{data.get('name')}</b>", self)
        name_lbl.setStyleSheet("color: #f8fafc; font-size: 13px;")
        info_layout.addWidget(name_lbl)

        desc_lbl = QLabel(data.get("summary", ""), self)
        desc_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        desc_lbl.setWordWrap(True)
        info_layout.addWidget(desc_lbl)

        id_lbl = QLabel(f"ID : {data.get('id')}  •  Source : {data.get('source')}", self)
        id_lbl.setStyleSheet("color: #64748b; font-size: 10px; font-family: monospace;")
        info_layout.addWidget(id_lbl)

        layout.addLayout(info_layout, 1)

        # Bouton Ajouter
        btn_add = QPushButton("➕ Ajouter", self)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
        """)
        btn_add.clicked.connect(self._on_add)
        layout.addWidget(btn_add)

    def _on_add(self):
        self.sig_add.emit(self.data)


class SearchAddDialog(QDialog):
    """Dialogue modal permettant de chercher et ajouter des applications."""

    sig_app_added = pyqtSignal(dict)  # Émis quand une nouvelle application est ajoutée

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rechercher ou Ajouter une Application")
        self.resize(650, 520)
        self.setModal(True)

        self._search_worker = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        tabs = QTabWidget(self)
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #334155;
                background-color: #0f172a;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: #94a3b8;
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #6366f1;
                color: #ffffff;
                font-weight: bold;
            }
        """)

        # Onglet 1 : Recherche en ligne
        tab_online = QWidget()
        self._setup_online_tab(tab_online)
        source_name = "Flathub" if is_linux() else "Winget"
        tabs.addTab(tab_online, f"🔍 Recherche en ligne ({source_name})")

        # Onglet 2 : Ajout manuel
        tab_manual = QWidget()
        self._setup_manual_tab(tab_manual)
        tabs.addTab(tab_manual, "✏️ Ajout manuel par ID")

        layout.addWidget(tabs)

        # Bouton Fermer
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        btn_close = QPushButton("Fermer", self)
        btn_close.setProperty("class", "ActionButton")
        btn_close.clicked.connect(self.accept)
        bottom_row.addWidget(btn_close)
        layout.addLayout(bottom_row)

    def _setup_online_tab(self, parent_widget: QWidget):
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Barre de recherche
        search_row = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Ex: blender, vlc, discord, steam, code...")
        self.search_input.setProperty("class", "SearchBar")
        self.search_input.returnPressed.connect(self._start_search)
        search_row.addWidget(self.search_input, 1)

        btn_search = QPushButton("Rechercher", self)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        btn_search.clicked.connect(self._start_search)
        search_row.addWidget(btn_search)
        layout.addLayout(search_row)

        # Indicateur de chargement
        self.loading_bar = QProgressBar(self)
        self.loading_bar.setRange(0, 0)
        self.loading_bar.setFixedHeight(4)
        self.loading_bar.setVisible(False)
        layout.addWidget(self.loading_bar)

        self.status_lbl = QLabel("Entrez un nom ou mot-clé pour lancer la recherche.", self)
        self.status_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        layout.addWidget(self.status_lbl)

        # Zone de défilement des résultats
        self.results_scroll = QScrollArea(self)
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setStyleSheet("border: none; background-color: transparent;")

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(6)
        self.results_layout.addStretch()

        self.results_scroll.setWidget(self.results_container)
        layout.addWidget(self.results_scroll, 1)

    def _setup_manual_tab(self, parent_widget: QWidget):
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        info_lbl = QLabel(
            "Ajoutez manuellement une application en fournissant son nom et son identifiant officiel :\n"
            "• Sur Windows : Identifiant Winget (ex: '7zip.7zip', 'Valve.Steam')\n"
            "• Sur Linux : Identifiant Flatpak (ex: 'org.videolan.VLC', 'com.brave.Browser')",
            self
        )
        info_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; line-height: 1.4;")
        layout.addWidget(info_lbl)

        # Nom
        layout.addWidget(QLabel("Nom de l'application :", self))
        self.manual_name = QLineEdit(self)
        self.manual_name.setPlaceholderText("Ex: Blender 3D")
        self.manual_name.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 6px;")
        layout.addWidget(self.manual_name)

        # Identifiant
        layout.addWidget(QLabel("Identifiant du paquet (Winget / Flatpak) :", self))
        self.manual_id = QLineEdit(self)
        self.manual_id.setPlaceholderText("Ex: BlenderFoundation.Blender ou org.blender.Blender")
        self.manual_id.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 6px;")
        layout.addWidget(self.manual_id)

        # Catégorie
        layout.addWidget(QLabel("Catégorie :", self))
        self.manual_cat = QLineEdit(self)
        self.manual_cat.setText("Personnalisé")
        self.manual_cat.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 6px;")
        layout.addWidget(self.manual_cat)

        # Description
        layout.addWidget(QLabel("Description (optionnel) :", self))
        self.manual_desc = QLineEdit(self)
        self.manual_desc.setPlaceholderText("Description courte de l'application")
        self.manual_desc.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 6px;")
        layout.addWidget(self.manual_desc)

        # Bouton Ajouter
        btn_add_manual = QPushButton("➕ Ajouter cette application", self)
        btn_add_manual.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 18px;
                font-weight: 700;
                font-size: 13px;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #059669; }
        """)
        btn_add_manual.clicked.connect(self._add_manual_app)
        layout.addWidget(btn_add_manual)
        layout.addStretch()

    def _start_search(self):
        query = self.search_input.text().strip()
        if not query:
            return

        self.loading_bar.setVisible(True)
        self.status_lbl.setText(f"Recherche de '{query}' en cours...")

        # Nettoyer les anciens résultats
        self._clear_results()

        self._search_worker = SearchWorker(query)
        self._search_worker.sig_results.connect(self._on_search_results)
        self._search_worker.sig_error.connect(self._on_search_error)
        self._search_worker.start()

    def _on_search_results(self, results: List[Dict]):
        self.loading_bar.setVisible(False)
        if not results:
            self.status_lbl.setText("Aucun résultat trouvé.")
            return

        self.status_lbl.setText(f"{len(results)} résultat(s) trouvé(s) :")
        for item_data in results:
            item_widget = SearchResultItem(item_data, self.results_container)
            item_widget.sig_add.connect(self._on_app_selected)
            self.results_layout.insertWidget(self.results_layout.count() - 1, item_widget)

    def _on_search_error(self, err_msg: str):
        self.loading_bar.setVisible(False)
        self.status_lbl.setText(f"Erreur : {err_msg}")

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
            "category": "Personnalisé",
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
            "Application Ajoutée",
            f"L'application '{new_app['name']}' a été ajoutée avec succès à votre sélection !"
        )

    def _add_manual_app(self):
        name = self.manual_name.text().strip()
        pkg_id = self.manual_id.text().strip()
        cat = self.manual_cat.text().strip() or "Personnalisé"
        desc = self.manual_desc.text().strip() or f"Paquet {pkg_id}"

        if not name or not pkg_id:
            QMessageBox.warning(self, "Champs requis", "Veuillez renseigner le nom et l'identifiant du paquet.")
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
            "Application Ajoutée",
            f"L'application '{name}' a été ajoutée avec succès à votre sélection !"
        )
        self.manual_name.clear()
        self.manual_id.clear()
        self.manual_desc.clear()
