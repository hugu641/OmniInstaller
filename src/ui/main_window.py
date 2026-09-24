"""
Fenêtre principale d'OmniInstaller.
Interface moderne avec grille d'applications dynamique, recherche instantanée,
filtres par catégories, et console de déploiement en temps réel.
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
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

from src.catalog import get_catalog, CATEGORIES
from src.installer_backend import (
    SystemDetector,
    InstallationWorker,
    is_windows,
    is_linux,
    get_current_os_name,
)
from src.ui.app_card import AppCard
from src.ui.search_dialog import SearchAddDialog
from src.ui.styles import MAIN_STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OmniInstaller - Installateur Universel d'Applications")
        self.resize(1080, 840)
        self.setMinimumSize(880, 620)

        # Définir l'icône de la fenêtre
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet(MAIN_STYLESHEET)

        self.apps_data = get_catalog()
        self.app_cards: List[AppCard] = []
        self.current_category = "Toutes"
        self.active_worker = None

        self._setup_ui()
        self._populate_apps()
        self._update_selection_count()
        self._check_system_status()

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. En-tête (Header)
        header = self._create_header()
        main_layout.addWidget(header)

        # 2. Barre d'outils et recherche
        tools_panel = self._create_tools_panel()
        main_layout.addWidget(tools_panel)

        # 3. Zone de défilement des cartes d'applications
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: #0b0f19;")

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setContentsMargins(18, 14, 18, 14)
        self.cards_layout.setSpacing(12)

        self.scroll_area.setWidget(self.cards_container)
        main_layout.addWidget(self.scroll_area, 1)

        # 4. Tiroir d'installation et console de logs
        self.install_drawer = self._create_install_drawer()
        main_layout.addWidget(self.install_drawer)

    def _create_header(self) -> QFrame:
        frame = QFrame(self)
        frame.setObjectName("HeaderFrame")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 12, 20, 12)

        # Gauche : Titre et sous-titre
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title = QLabel("⚡ OmniInstaller", self)
        title.setObjectName("AppTitle")
        title_box.addWidget(title)

        subtitle = QLabel("Installateur silencieux d'applications pour Windows et Linux", self)
        subtitle.setObjectName("AppSubtitle")
        title_box.addWidget(subtitle)

        layout.addLayout(title_box, 1)

        # Droite : Badges OS & Gestionnaire
        badges_box = QHBoxLayout()
        badges_box.setSpacing(8)

        os_name = get_current_os_name()
        os_icon = "🪟" if is_windows() else "🐧"
        self.os_badge = QLabel(f"{os_icon} {os_name}", self)
        self.os_badge.setObjectName("OSBadge")
        badges_box.addWidget(self.os_badge)

        self.status_badge = QLabel("Vérification...", self)
        self.status_badge.setObjectName("StatusBadgeReady")
        badges_box.addWidget(self.status_badge)

        layout.addLayout(badges_box)
        return frame

    def _create_tools_panel(self) -> QFrame:
        panel = QFrame(self)
        panel.setStyleSheet("background-color: #111827; border-bottom: 1px solid #1f2937; padding: 10px 18px;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Rangée 1 : Barre de recherche + Bouton recherche en ligne + Boutons d'action
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        self.search_bar = QLineEdit(self)
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setPlaceholderText("🔍 Rechercher une application (nom, description, ID, mot-clé)...")
        self.search_bar.textChanged.connect(self._filter_apps)
        row1.addWidget(self.search_bar, 1)

        btn_search_online = QPushButton("🌐 Chercher sur le Store / Dépôt", self)
        btn_search_online.setObjectName("SearchOnlineBtn")
        btn_search_online.clicked.connect(self._open_search_dialog)
        row1.addWidget(btn_search_online)

        layout.addLayout(row1)

        # Rangée 2 : Boutons de catégories (Chips)
        self.category_buttons = {}
        row_cat = QHBoxLayout()
        row_cat.setSpacing(6)

        for cat in CATEGORIES:
            btn = QPushButton(cat, self)
            btn.setProperty("class", "CategoryChip")
            btn.setProperty("active", "true" if cat == "Toutes" else "false")
            btn.clicked.connect(lambda checked, c=cat: self._on_category_clicked(c))
            self.category_buttons[cat] = btn
            row_cat.addWidget(btn)

        row_cat.addStretch()
        layout.addLayout(row_cat)

        # Rangée 3 : Actions rapides (Tout cocher, Décocher, Recommandé, Compteur)
        row_actions = QHBoxLayout()
        row_actions.setSpacing(8)

        btn_check_all = QPushButton("Tout cocher", self)
        btn_check_all.setProperty("class", "ActionButton")
        btn_check_all.clicked.connect(self._check_all)
        row_actions.addWidget(btn_check_all)

        btn_uncheck_all = QPushButton("Tout décocher", self)
        btn_uncheck_all.setProperty("class", "ActionButton")
        btn_uncheck_all.clicked.connect(self._uncheck_all)
        row_actions.addWidget(btn_uncheck_all)

        btn_recommended = QPushButton("⭐ Sélection recommandée", self)
        btn_recommended.setProperty("class", "ActionButton")
        btn_recommended.setStyleSheet("color: #facc15; font-weight: 600;")
        btn_recommended.clicked.connect(self._select_recommended)
        row_actions.addWidget(btn_recommended)

        row_actions.addStretch()

        self.lbl_counter = QLabel("0 application(s) sélectionnée(s)", self)
        self.lbl_counter.setStyleSheet("color: #cbd5e1; font-weight: 600; font-size: 12px;")
        row_actions.addWidget(self.lbl_counter)

        layout.addLayout(row_actions)

        return panel

    def _create_install_drawer(self) -> QFrame:
        drawer = QFrame(self)
        drawer.setObjectName("InstallDrawer")

        layout = QVBoxLayout(drawer)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(10)

        # Ligne d'action : Statut texte + Bouton Dérouler Console + Boutons Lancer/Annuler
        action_row = QHBoxLayout()
        action_row.setSpacing(12)

        status_box = QVBoxLayout()
        status_box.setSpacing(2)

        self.lbl_install_status = QLabel("Prêt pour l'installation", self)
        self.lbl_install_status.setStyleSheet("color: #f8fafc; font-size: 13px; font-weight: 700;")
        status_box.addWidget(self.lbl_install_status)

        self.lbl_current_step = QLabel("Cochez les applications souhaitées puis cliquez sur Lancer.", self)
        self.lbl_current_step.setStyleSheet("color: #94a3b8; font-size: 11px;")
        status_box.addWidget(self.lbl_current_step)

        action_row.addLayout(status_box, 1)

        self.btn_toggle_log = QPushButton("📜 Afficher les logs", self)
        self.btn_toggle_log.setObjectName("ToggleLogButton")
        self.btn_toggle_log.clicked.connect(self._toggle_logs)
        action_row.addWidget(self.btn_toggle_log)

        self.btn_cancel = QPushButton("🛑 Annuler", self)
        self.btn_cancel.setObjectName("CancelButton")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self._cancel_installation)
        action_row.addWidget(self.btn_cancel)

        self.btn_install = QPushButton("🚀 Lancer l'installation", self)
        self.btn_install.setObjectName("InstallButton")
        self.btn_install.clicked.connect(self._start_installation)
        action_row.addWidget(self.btn_install)

        layout.addLayout(action_row)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("InstallProgressBar")
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Console de logs (repliable)
        self.log_console = QTextEdit(self)
        self.log_console.setObjectName("LogConsole")
        self.log_console.setReadOnly(True)
        self.log_console.setFixedHeight(140)
        self.log_console.setVisible(False)
        layout.addWidget(self.log_console)

        return drawer

    def _populate_apps(self):
        """Instancie et place les cartes d'applications dans la grille."""
        # Vider la grille
        for card in self.app_cards:
            card.deleteLater()
        self.app_cards.clear()

        # Remplir avec 3 colonnes
        cols = 3
        for idx, app in enumerate(self.apps_data):
            card = AppCard(app, self.cards_container)
            card.sig_toggled.connect(self._on_card_toggled)
            self.app_cards.append(card)

            row = idx // cols
            col = idx % cols
            self.cards_layout.addWidget(card, row, col)

    def _check_system_status(self):
        """Vérifie et affiche l'état du gestionnaire de paquets de la machine."""
        info = SystemDetector.get_status_info()
        status = info.get("status")
        msg = info.get("message")
        backend = info.get("backend")

        if status == "ready":
            self.status_badge.setText(f"✔ Prêt ({backend.upper()})")
            self.status_badge.setObjectName("StatusBadgeReady")
            self.status_badge.setToolTip(msg)
        else:
            self.status_badge.setText(f"⚠️ {backend.upper()} manquant")
            self.status_badge.setObjectName("StatusBadgeWarn")
            self.status_badge.setToolTip(msg)

        self.status_badge.style().unpolish(self.status_badge)
        self.status_badge.style().polish(self.status_badge)

    def _on_category_clicked(self, category: str):
        self.current_category = category
        for cat, btn in self.category_buttons.items():
            active = "true" if cat == category else "false"
            btn.setProperty("active", active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._filter_apps()

    def _filter_apps(self):
        """Applique les filtres de recherche textuelle et de catégorie."""
        query = self.search_bar.text().strip().lower()
        visible_count = 0

        # Réorganisation dans la grille des cartes visibles
        cols = 3
        col = 0
        row = 0

        for card in self.app_cards:
            matches_cat = card.matches_category(self.current_category)
            matches_txt = card.matches_query(query)
            should_show = matches_cat and matches_txt

            card.setVisible(should_show)
            if should_show:
                self.cards_layout.removeWidget(card)
                self.cards_layout.addWidget(card, row, col)
                col += 1
                if col >= cols:
                    col = 0
                    row += 1
                visible_count += 1

        self._update_selection_count(visible_count)

    def _on_card_toggled(self, app_data: Dict, checked: bool):
        self._update_selection_count()

    def _update_selection_count(self, visible_count=None):
        selected = [c for c in self.app_cards if c.is_checked()]
        total_visible = visible_count if visible_count is not None else len([c for c in self.app_cards if c.isVisible()])

        self.lbl_counter.setText(
            f"{len(selected)} application(s) sélectionnée(s) / {total_visible} affichée(s)"
        )
        self.btn_install.setText(f"🚀 Lancer l'installation ({len(selected)})")
        self.btn_install.setEnabled(len(selected) > 0 and self.active_worker is None)

    def _check_all(self):
        for card in self.app_cards:
            if card.isVisible():
                card.set_checked(True)
        self._update_selection_count()

    def _uncheck_all(self):
        for card in self.app_cards:
            card.set_checked(False)
        self._update_selection_count()

    def _select_recommended(self):
        for card in self.app_cards:
            is_rec = card.app_data.get("recommended", False)
            card.set_checked(is_rec)
        self._update_selection_count()

    def _toggle_logs(self):
        is_visible = self.log_console.isVisible()
        self.log_console.setVisible(not is_visible)
        self.btn_toggle_log.setText("📜 Masquer les logs" if not is_visible else "📜 Afficher les logs")

    def _open_search_dialog(self):
        dialog = SearchAddDialog(self)
        dialog.sig_app_added.connect(self._add_custom_app)
        dialog.exec()

    def _add_custom_app(self, new_app: Dict):
        # Ajouter à la liste et créer une nouvelle carte
        self.apps_data.append(new_app)
        card = AppCard(new_app, self.cards_container)
        card.set_checked(True)
        card.sig_toggled.connect(self._on_card_toggled)
        self.app_cards.append(card)

        self._filter_apps()
        self._update_selection_count()

    def _start_installation(self):
        selected_apps = [c.app_data for c in self.app_cards if c.is_checked()]
        if not selected_apps:
            QMessageBox.warning(self, "Attention", "Aucune application n'est sélectionnée.")
            return

        # Afficher la console de log et la barre de progression
        self.log_console.setVisible(True)
        self.btn_toggle_log.setText("📜 Masquer les logs")
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected_apps))
        self.progress_bar.setValue(0)

        self.log_console.clear()
        self.lbl_install_status.setText("Installation en cours...")
        self.btn_install.setEnabled(False)
        self.btn_cancel.setEnabled(True)

        # Lancer le worker en arrière-plan
        self.active_worker = InstallationWorker(selected_apps)
        self.active_worker.sig_log.connect(self._on_worker_log)
        self.active_worker.sig_progress.connect(self._on_worker_progress)
        self.active_worker.sig_current_app.connect(self._on_worker_current_app)
        self.active_worker.sig_finished.connect(self._on_worker_finished)
        self.active_worker.start()

    def _cancel_installation(self):
        if self.active_worker:
            self.lbl_install_status.setText("Arrêt de l'installation en cours...")
            self.btn_cancel.setEnabled(False)
            self.active_worker.cancel()

    def _on_worker_log(self, message: str, level: str):
        color_map = {
            "info": "#94a3b8",
            "success": "#4ade80",
            "warning": "#facc15",
            "error": "#f87171",
        }
        color = color_map.get(level, "#f1f5f9")
        html_line = f"<span style='color: {color};'>{message}</span>"
        self.log_console.append(html_line)

        # Auto-scroll vers le bas
        sb = self.log_console.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _on_worker_progress(self, current: int, total: int):
        self.progress_bar.setValue(current)
        percent = int((current / total) * 100) if total > 0 else 0
        self.lbl_current_step.setText(f"Progression : {current}/{total} ({percent}%)")

    def _on_worker_current_app(self, app_name: str):
        self.lbl_install_status.setText(f"Installation de {app_name} en cours...")

    def _on_worker_finished(self, report: dict):
        self.active_worker = None
        self.btn_cancel.setEnabled(False)
        self.btn_install.setEnabled(True)

        succeeded = report.get("succeeded", 0)
        total = report.get("total", 0)
        failed = report.get("failed", 0)
        cancelled = report.get("cancelled", False)
        duration = report.get("duration", 0)

        if cancelled:
            self.lbl_install_status.setText("Installation annulée.")
            self.lbl_current_step.setText(f"{succeeded}/{total} application(s) installée(s) avant arrêt.")
            QMessageBox.information(
                self,
                "Installation Annulée",
                f"L'opération a été interrompue.\n{succeeded} application(s) ont été installées."
            )
        elif failed == 0:
            self.lbl_install_status.setText("✔ Toutes les applications ont été installées avec succès !")
            self.lbl_current_step.setText(f"{succeeded} paquet(s) traités en {duration}s.")
            QMessageBox.information(
                self,
                "Succès !",
                f"🎉 Toutes les {succeeded} applications ont été installées avec succès !\n"
                f"Elles sont maintenant disponibles dans votre menu d'applications."
            )
        else:
            self.lbl_install_status.setText(f"Terminé : {succeeded} réussie(s), {failed} échec(s).")
            failed_apps = ", ".join(report.get("failed_apps", []))
            QMessageBox.warning(
                self,
                "Installation terminée avec des remarques",
                f"{succeeded} application(s) installée(s) avec succès.\n"
                f"{failed} échec(s) : {failed_apps}\n\n"
                "Consultez les logs détaillés ci-dessous pour plus de précisions."
            )

        self._update_selection_count()
