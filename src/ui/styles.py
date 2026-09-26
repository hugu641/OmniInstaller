"""
Design System OmniInstaller — Thème "Pro / Slate Nordic" v4.
Palette : gris-bleu profonds, sans dégradés, sans néon, sans ombres floues.
Inspiré de Raycast, GitHub Desktop, VS Code.
"""

# Tokens de couleurs
C_BG         = "#0F172A"  # Fond principal (slate-900)
C_SIDEBAR    = "#1E293B"  # Barre latérale (slate-800) — voir note : on assombrit légèrement via stylesheet pour contraste
C_SURFACE    = "#1E293B"  # Cartes (slate-800)
C_SURFACE_H  = "#273449"  # Hover carte / bouton
C_BORDER     = "#334155"  # Bordures subtiles (slate-700)
C_BORDER_H   = "#475569"  # Bordures hover (slate-600)
C_TEXT       = "#F1F5F9"  # Texte principal (slate-100)
C_TEXT2      = "#94A3B8"  # Texte secondaire (slate-400)
C_TEXT3      = "#64748B"  # Texte discret (slate-500)
C_ACCENT     = "#10B981"  # Vert émeraude — CTA principal uniquement
C_ACCENT_H   = "#059669"  # Émeraude hover
C_ACCENT_P   = "#047857"  # Émeraude pressed
C_ACCENT_TX  = "#06281E"  # Texte sur fond émeraude (contraste élevé)
C_SUCCESS    = "#10B981"
C_WARN       = "#F59E0B"
C_DANGER     = "#EF4444"

MAIN_STYLESHEET = """
/* ============================================================
   BASE
   ============================================================ */
QWidget {
    background-color: #0F172A;
    color: #F1F5F9;
    font-family: 'Inter', 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
    outline: none;
    selection-background-color: #10B981;
    selection-color: #06281E;
}

QMainWindow {
    background-color: #0F172A;
}

QToolTip {
    background-color: #1E293B;
    color: #F1F5F9;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 9px;
    font-size: 11px;
}

/* ============================================================
   SIDEBAR — compacte, outil technique
   ============================================================ */
QFrame#Sidebar {
    background-color: #16213A;
    border-right: 1px solid #334155;
    min-width: 200px;
    max-width: 200px;
}

QLabel#BrandTitle {
    font-size: 14px;
    font-weight: 700;
    color: #F1F5F9;
    background: transparent;
}

QLabel#BrandSubtitle {
    font-size: 10px;
    font-weight: 400;
    color: #64748B;
    background: transparent;
}

QLabel#SidebarSectionHeader {
    color: #64748B;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
    background: transparent;
    padding: 14px 14px 4px 14px;
}

QPushButton[navbtn="1"] {
    text-align: left;
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-left: 2px solid transparent;
    border-radius: 0px;
    padding: 6px 10px 6px 12px;
    font-size: 12px;
    font-weight: 400;
    margin: 0 6px;
}

QPushButton[navbtn="1"]:hover {
    background-color: #1E293B;
    color: #F1F5F9;
    border-radius: 6px;
}

QPushButton[navbtn="1"][active="true"] {
    background-color: #1E293B;
    color: #F1F5F9;
    font-weight: 600;
    border-left: 2px solid #10B981;
    border-radius: 0 6px 6px 0;
}

QPushButton[navbtn="1"]:pressed {
    background-color: #0F172A;
}

QFrame#SidebarSystemBox {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
    margin: 6px 10px 12px 10px;
}

QLabel#SystemStatusLabel {
    font-size: 11px;
    font-weight: 500;
    color: #94A3B8;
    background: transparent;
}

QLabel#SystemStatusBadgeReady {
    background-color: transparent;
    color: #10B981;
    border: 1px solid #134E3A;
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 9px;
    font-weight: 600;
}

QLabel#SystemStatusBadgeWarn {
    background-color: transparent;
    color: #F59E0B;
    border: 1px solid #4A3410;
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 9px;
    font-weight: 600;
}

QPushButton#SearchOnlineBtn {
    background-color: #1E293B;
    color: #94A3B8;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 11.5px;
    font-weight: 500;
    text-align: left;
}

QPushButton#SearchOnlineBtn:hover {
    background-color: #273449;
    color: #F1F5F9;
    border-color: #475569;
}

/* ============================================================
   HEADER CONTENU
   ============================================================ */
QFrame#ContentHeader {
    background-color: #0F172A;
    border-bottom: 1px solid #1E293B;
}

QLabel#PageTitle {
    font-size: 17px;
    font-weight: 700;
    color: #F1F5F9;
    background: transparent;
}

QLabel#PageSubtitle {
    font-size: 12px;
    font-weight: 400;
    color: #64748B;
    background: transparent;
}

QLineEdit#SearchBar {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 7px;
    padding: 7px 12px;
    color: #F1F5F9;
    font-size: 13px;
    font-weight: 400;
    min-height: 16px;
}

QLineEdit#SearchBar:hover {
    border-color: #475569;
}

QLineEdit#SearchBar:focus {
    border-color: #10B981;
    background-color: #1A2742;
}

QPushButton[quickbtn="1"] {
    background-color: transparent;
    color: #94A3B8;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton[quickbtn="1"]:hover {
    background-color: #1E293B;
    color: #F1F5F9;
    border-color: #475569;
}

QPushButton[quickbtn="1"]:pressed {
    background-color: #16213A;
}

QPushButton#BtnRecommended {
    background-color: transparent;
    color: #94A3B8;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton#BtnRecommended:hover {
    background-color: #1E293B;
    color: #F59E0B;
    border-color: #475569;
}

QLabel#ResultsCountLabel {
    color: #64748B;
    font-size: 11px;
    font-weight: 500;
    background: transparent;
}

/* ============================================================
   CARTES APPLICATION — plates, 8px, 1px #334155, sans ombre
   ============================================================ */
QFrame#AppCard {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    min-height: 96px;
}

QFrame#AppCard:hover {
    background-color: #24334D;
    border-color: #475569;
}

QFrame#AppCard[selected="true"] {
    background-color: #1E293B;
    border-color: #10B981;
    border-width: 1px;
}

QFrame#LogoContainer {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
}

QLabel#CardAppTitle {
    font-size: 13.5px;
    font-weight: 600;
    color: #F1F5F9;
    background: transparent;
}

QLabel#CardCategoryBadge {
    background-color: transparent;
    color: #64748B;
    border: none;
    padding: 0;
    font-size: 11px;
    font-weight: 400;
}

QLabel#CardRecommendedBadge {
    background-color: transparent;
    color: #F59E0B;
    border: none;
    padding: 0;
    font-size: 11px;
    font-weight: 500;
}

QLabel#CardAppDesc {
    font-size: 12px;
    font-weight: 400;
    color: #94A3B8;
    background: transparent;
}

QLabel#CardPkgId {
    font-size: 10px;
    color: #64748B;
    background: transparent;
    border: none;
    font-family: 'Cascadia Code', 'Consolas', monospace;
}

/* Bouton d'action directe par carte */
QPushButton#CardActionButton {
    background-color: transparent;
    color: #94A3B8;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    min-width: 86px;
}

QPushButton#CardActionButton:hover {
    background-color: #273449;
    color: #F1F5F9;
    border-color: #475569;
}

QPushButton#CardActionButton[selected="true"] {
    background-color: rgba(16, 185, 129, 0.14);
    color: #10B981;
    border: 1px solid #10B981;
}

QPushButton#CardActionButton[selected="true"]:hover {
    background-color: rgba(16, 185, 129, 0.22);
}

QLabel#CardInstalledBadge {
    background-color: rgba(16, 185, 129, 0.12);
    color: #10B981;
    border: 1px solid #134E3A;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 11.5px;
    font-weight: 600;
}

/* ============================================================
   DOCK INSTALLATION
   ============================================================ */
QFrame#InstallDock {
    background-color: #0F172A;
    border-top: 1px solid #1E293B;
}

QLabel#DockSummaryTitle {
    font-size: 13px;
    font-weight: 600;
    color: #F1F5F9;
    background: transparent;
}

QLabel#DockSummarySubtitle {
    font-size: 11px;
    font-weight: 400;
    color: #64748B;
    background: transparent;
}

QPushButton#InstallButton {
    background-color: #10B981;
    color: #06281E;
    border: none;
    border-radius: 7px;
    padding: 9px 22px;
    font-size: 13px;
    font-weight: 700;
    min-width: 160px;
}

QPushButton#InstallButton:hover {
    background-color: #059669;
    color: #FFFFFF;
}

QPushButton#InstallButton:pressed {
    background-color: #047857;
    color: #FFFFFF;
}

QPushButton#InstallButton:disabled {
    background-color: #1E293B;
    color: #475569;
    border: 1px solid #1E293B;
}

QPushButton#CancelButton {
    background-color: transparent;
    color: #94A3B8;
    border: 1px solid #334155;
    border-radius: 7px;
    padding: 9px 16px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton#CancelButton:hover {
    background-color: #2A1A1A;
    color: #EF4444;
    border-color: #4A2A2A;
}

QPushButton#CancelButton:disabled {
    color: #475569;
    border-color: #1E293B;
}

QPushButton#ToggleLogButton {
    background-color: transparent;
    color: #94A3B8;
    border: 1px solid #334155;
    border-radius: 7px;
    padding: 9px 14px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton#ToggleLogButton:hover {
    background-color: #1E293B;
    color: #F1F5F9;
}

QProgressBar#InstallProgressBar {
    background-color: #1E293B;
    border: none;
    border-radius: 2px;
    min-height: 4px;
    max-height: 4px;
    text-align: center;
    color: transparent;
}

QProgressBar#InstallProgressBar::chunk {
    background-color: #10B981;
    border-radius: 2px;
}

QTextEdit#LogConsole {
    background-color: #0B1220;
    border: 1px solid #1E293B;
    border-radius: 6px;
    color: #94A3B8;
    font-family: 'Cascadia Code', 'Consolas', monospace;
    font-size: 11px;
    padding: 8px;
}

/* ============================================================
   SCROLLBAR — fine et discrète
   ============================================================ */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 6px;
    margin: 2px 1px 2px 0;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 24px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
    height: 0;
}

QScrollBar:horizontal {
    height: 0;
    background: transparent;
}

/* ============================================================
   DIALOGUES & ONGLETS
   ============================================================ */
QDialog {
    background-color: #0F172A;
}

QTabWidget::pane {
    border: 1px solid #1E293B;
    background-color: #0F172A;
    border-radius: 7px;
    top: -1px;
}

QTabBar::tab {
    background-color: transparent;
    color: #64748B;
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 500;
    font-size: 12px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #1E293B;
    color: #F1F5F9;
    font-weight: 600;
    border-bottom: 2px solid #10B981;
}

QTabBar::tab:hover:!selected {
    color: #94A3B8;
    background-color: #16213A;
}

QLineEdit {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 7px 10px;
    color: #F1F5F9;
    font-size: 12.5px;
}

QLineEdit:focus {
    border-color: #10B981;
}

QLineEdit:hover {
    border-color: #475569;
}
"""
