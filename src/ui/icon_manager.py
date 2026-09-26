"""
Gestionnaire d'icônes et logos réels pour OmniInstaller.
Supporte le chargement depuis les assets locaux, l'environnement PyInstaller (sys._MEIPASS),
la mise en cache haute performance, le rendu vectoriel SVG et la génération de visuels élégants.
"""

import os
import sys
from typing import Dict, Optional
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QColor, QFont, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QByteArray
from PyQt6.QtSvg import QSvgRenderer

# Résolution du dossier racine (compatible script direct et package PyInstaller)
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOGOS_DIR = os.path.join(BASE_DIR, "assets", "logos")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")

# Monogrammes de secours : tons ardoise sobres, unis (pas de dégradés, pas de néon)
FALLBACK_COLORS = [
    ("#334155", "#334155"),  # Slate-700
    ("#475569", "#475569"),  # Slate-600
    ("#1E3A5F", "#1E3A5F"),  # Bleu ardoise profond
    ("#0F766E", "#0F766E"),  # Sarcelle discrète
    ("#4C5A71", "#4C5A71"),  # Gris-bleu
    ("#2B3A55", "#2B3A55"),  # Slate nuit
    ("#3F4C63", "#3F4C63"),  # Gris acier
]


class IconManager:
    """Fournisseur d'icônes, logos et glyphes vectoriels SVG avec cache mémoire."""

    _pixmap_cache: Dict[str, QPixmap] = {}
    _svg_cache: Dict[str, str] = {}

    @classmethod
    def get_logo_path(cls, app_id: str) -> Optional[str]:
        """Retourne le chemin local du fichier logo s'il existe."""
        if not app_id:
            return None
        candidate = os.path.join(LOGOS_DIR, f"{app_id}.png")
        if os.path.exists(candidate):
            return candidate
        return None

    @classmethod
    def get_ui_pixmap(cls, name: str, size: int = 20, color: Optional[str] = None) -> QPixmap:
        """
        Charge une icône vectorielle SVG depuis assets/icons/<name>.svg
        avec taille exacte, lissage antialiasing et coloration optionnelle.
        """
        cache_key = f"ui_{name}_{size}_{color}"
        if cache_key in cls._pixmap_cache:
            return cls._pixmap_cache[cache_key]

        svg_path = os.path.join(ICONS_DIR, f"{name}.svg")
        if not os.path.exists(svg_path):
            # Fallback pixmap transparent
            pm = QPixmap(size, size)
            pm.fill(Qt.GlobalColor.transparent)
            cls._pixmap_cache[cache_key] = pm
            return pm

        renderer = None
        if color:
            # Coloration dynamique du SVG
            if name not in cls._svg_cache:
                try:
                    with open(svg_path, "r", encoding="utf-8") as f:
                        cls._svg_cache[name] = f.read()
                except Exception:
                    cls._svg_cache[name] = ""

            svg_content = cls._svg_cache.get(name, "")
            if svg_content:
                # Remplacer les couleurs de stroke ou fill courantes
                modified = svg_content.replace('stroke="white"', f'stroke="{color}"')
                modified = modified.replace('stroke="#94a3b8"', f'stroke="{color}"')
                modified = modified.replace('stroke="#818cf8"', f'stroke="{color}"')
                modified = modified.replace('stroke="#38bdf8"', f'stroke="{color}"')
                modified = modified.replace('fill="white"', f'fill="{color}"')
                renderer = QSvgRenderer(QByteArray(modified.encode("utf-8")))

        if renderer is None or not renderer.isValid():
            renderer = QSvgRenderer(svg_path)

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        renderer.render(painter, QRectF(0, 0, size, size))
        painter.end()

        cls._pixmap_cache[cache_key] = pixmap
        return pixmap

    @classmethod
    def get_ui_icon(cls, name: str, size: int = 20, color: Optional[str] = None) -> QIcon:
        """Retourne un QIcon à partir du pixmap vectoriel."""
        return QIcon(cls.get_ui_pixmap(name, size, color))

    @classmethod
    def get_app_pixmap(cls, app_data: Dict, size: int = 48) -> QPixmap:
        """
        Retourne un QPixmap haute résolution pour l'application.
        Si le logo officiel existe, il est chargé et mis à l'échelle en douceur.
        Sinon, un monogramme moderne et soigné est généré.
        """
        app_id = app_data.get("id", "")
        cache_key = f"app_{app_id}_{size}"

        if cache_key in cls._pixmap_cache:
            return cls._pixmap_cache[cache_key]

        logo_path = cls.get_logo_path(app_id)
        if logo_path:
            original = QPixmap(logo_path)
            if not original.isNull():
                # Redimensionnement haute qualité
                scaled = original.scaled(
                    size,
                    size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                # Centrer dans un canvas carré transparent
                final_pixmap = QPixmap(size, size)
                final_pixmap.fill(Qt.GlobalColor.transparent)

                painter = QPainter(final_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

                x = (size - scaled.width()) // 2
                y = (size - scaled.height()) // 2
                painter.drawPixmap(x, y, scaled)
                painter.end()

                cls._pixmap_cache[cache_key] = final_pixmap
                return final_pixmap

        # Repli élégant : Monogramme avec fond arrondi
        fallback_pixmap = cls._generate_monogram(app_data, size)
        cls._pixmap_cache[cache_key] = fallback_pixmap
        return fallback_pixmap

    @classmethod
    def get_app_icon(cls, app_data: Dict, size: int = 48) -> QIcon:
        """Retourne un QIcon à partir du pixmap généré."""
        return QIcon(cls.get_app_pixmap(app_data, size))

    @classmethod
    def _generate_monogram(cls, app_data: Dict, size: int) -> QPixmap:
        """Génère un avatar graphique moderne pour les applications sans logo PNG."""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Choix d'une couleur basée sur le nom
        name = app_data.get("name", "App")
        color_idx = sum(ord(c) for c in name) % len(FALLBACK_COLORS)
        c_start, c_end = FALLBACK_COLORS[color_idx]

        # Rectangle arrondi
        path = QPainterPath()
        rect = QRectF(1, 1, size - 2, size - 2)
        radius = size * 0.22
        path.addRoundedRect(rect, radius, radius)

        painter.fillPath(path, QColor(c_start))

        # Texte (Monogramme 1 à 2 lettres)
        initials = "".join([part[0].upper() for part in name.split()[:2] if part])
        if not initials:
            initials = name[:1].upper() if name else "?"

        painter.setPen(QColor("#ffffff"))
        font = QFont("Segoe UI", int(size * 0.42), QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, initials)

        painter.end()
        return pixmap

