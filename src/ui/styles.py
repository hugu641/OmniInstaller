"""
Feuilles de style modernes QSS (Thème Sombre Premium 'Midnight Slate').
Palette inspirée de Tailwind CSS (Slate, Indigo, Emerald, Amber).
"""

MAIN_STYLESHEET = """
/* === Styles Généraux === */
QWidget {
    background-color: #0f172a;
    color: #f1f5f9;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', 'Ubuntu', sans-serif;
    font-size: 13px;
    selection-background-color: #6366f1;
    selection-color: #ffffff;
}

/* === Fenêtre Principale === */
QMainWindow {
    background-color: #0b0f19;
}

/* === En-tête (Header) === */
QFrame#HeaderFrame {
    background-color: #111827;
    border-bottom: 1px solid #1f2937;
    padding: 10px 16px;
}

QLabel#AppTitle {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
}

QLabel#AppSubtitle {
    font-size: 12px;
    color: #94a3b8;
}

QLabel#OSBadge {
    background-color: #1e293b;
    color: #38bdf8;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 4px 10px;
    font-weight: 600;
    font-size: 11px;
}

QLabel#StatusBadgeReady {
    background-color: #064e3b;
    color: #34d399;
    border: 1px solid #059669;
    border-radius: 12px;
    padding: 4px 10px;
    font-weight: 600;
    font-size: 11px;
}

QLabel#StatusBadgeWarn {
    background-color: #78350f;
    color: #fbbf24;
    border: 1px solid #d97706;
    border-radius: 12px;
    padding: 4px 10px;
    font-weight: 600;
    font-size: 11px;
}

/* === Barre de recherche et filtres === */
QLineEdit#SearchBar {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 14px;
    color: #f8fafc;
    font-size: 13px;
}

QLineEdit#SearchBar:focus {
    border: 1.5px solid #6366f1;
    background-color: #24324a;
}

/* === Boutons de Catégories (Chips) === */
QPushButton.CategoryChip {
    background-color: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton.CategoryChip:hover {
    background-color: #334155;
    color: #f8fafc;
}

QPushButton.CategoryChip[active="true"] {
    background-color: #6366f1;
    color: #ffffff;
    border: 1px solid #818cf8;
    font-weight: 600;
}

/* === Boutons d'Action Rapide === */
QPushButton.ActionButton {
    background-color: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton.ActionButton:hover {
    background-color: #334155;
    color: #ffffff;
    border-color: #475569;
}

QPushButton.ActionButton:pressed {
    background-color: #0f172a;
}

QPushButton#SearchOnlineBtn {
    background-color: #4f46e5;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
}

QPushButton#SearchOnlineBtn:hover {
    background-color: #4338ca;
}

/* === Cartes d'application (AppCard) === */
QFrame.AppCard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 8px;
}

QFrame.AppCard:hover {
    border-color: #6366f1;
    background-color: #24324a;
}

QFrame.AppCard[checked="true"] {
    background-color: #1e1b4b;
    border: 1.5px solid #818cf8;
}

QLabel.AppCardTitle {
    font-size: 14px;
    font-weight: 700;
    color: #f8fafc;
}

QLabel.AppCardDesc {
    font-size: 11px;
    color: #94a3b8;
}

QLabel.AppCardCategory {
    font-size: 10px;
    color: #a78bfa;
    background-color: #2e1065;
    border-radius: 4px;
    padding: 2px 6px;
    font-weight: 600;
}

QLabel.AppCardPkgId {
    font-size: 10px;
    color: #64748b;
    font-family: 'Consolas', monospace;
}

/* === CheckBox Moderne === */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1.5px solid #64748b;
    border-radius: 5px;
    background-color: #0f172a;
}

QCheckBox::indicator:hover {
    border-color: #818cf8;
}

QCheckBox::indicator:checked {
    background-color: #6366f1;
    border-color: #6366f1;
    image: none; /* Le dessin est géré via le style ou texte */
}

/* === Barre de Défilement (ScrollBar) === */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 25px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* === Tiroir d'Installation & Logs (Bottom Drawer) === */
QFrame#InstallDrawer {
    background-color: #111827;
    border-top: 1px solid #1f2937;
    padding: 12px 18px;
}

QProgressBar#InstallProgressBar {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    height: 14px;
    text-align: center;
    color: #ffffff;
    font-size: 10px;
    font-weight: bold;
}

QProgressBar#InstallProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #a855f7);
    border-radius: 5px;
}

QTextEdit#LogConsole {
    background-color: #090d16;
    border: 1px solid #1f2937;
    border-radius: 8px;
    color: #4ade80;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    padding: 8px;
}

QPushButton#InstallButton {
    background-color: #6366f1;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton#InstallButton:hover {
    background-color: #4f46e5;
}

QPushButton#InstallButton:pressed {
    background-color: #4338ca;
}

QPushButton#InstallButton:disabled {
    background-color: #334155;
    color: #64748b;
}

QPushButton#CancelButton {
    background-color: #dc2626;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#CancelButton:hover {
    background-color: #b91c1c;
}

QPushButton#ToggleLogButton {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    font-size: 12px;
}

QPushButton#ToggleLogButton:hover {
    color: #f1f5f9;
}
"""
