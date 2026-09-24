"""
Service de recherche d'applications en ligne et en local.
- Sur Linux : Recherche Flathub via API REST
- Sur Windows : Recherche Winget via 'winget search'
- Recherche par mot-clé dans le catalogue intégré
"""

import json
import subprocess
import urllib.request
import urllib.parse
from typing import List, Dict
from PyQt6.QtCore import QThread, pyqtSignal
from src.installer_backend import is_windows, is_linux


class SearchWorker(QThread):
    """Thread de recherche en ligne asynchrone."""

    sig_results = pyqtSignal(list)   # Liste de résultats [{'name', 'id', 'summary', 'source'}]
    sig_error = pyqtSignal(str)      # Message d'erreur si la recherche échoue

    def __init__(self, query: str):
        super().__init__()
        self.query = query.strip()

    def run(self):
        if not self.query:
            self.sig_results.emit([])
            return

        try:
            if is_linux():
                results = self._search_flathub(self.query)
            elif is_windows():
                results = self._search_winget(self.query)
            else:
                results = []

            self.sig_results.emit(results)
        except Exception as e:
            self.sig_error.emit(f"Erreur de recherche : {str(e)}")

    def _search_flathub(self, query: str) -> List[Dict]:
        """Effectue une recherche sur Flathub via son API."""
        url = "https://flathub.org/api/v2/search"
        payload = json.dumps({"query": query}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "OmniInstaller/1.0"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        hits = data.get("hits", [])
        results = []
        for hit in hits[:25]:  # Limiter aux 25 meilleurs résultats
            app_id = hit.get("app_id") or hit.get("id") or ""
            name = hit.get("name") or app_id
            summary = hit.get("summary") or "Application Flathub"
            icon = hit.get("icon") or "📦"
            results.append({
                "name": name,
                "id": app_id,
                "summary": summary,
                "source": "Flathub (Linux)",
                "icon": "📦",
                "linux_id": app_id,
                "windows_id": "",
                "category": "Personnalisé",
            })
        return results

    def _search_winget(self, query: str) -> List[Dict]:
        """Effectue une recherche Winget en ligne de commande."""
        cmd = ["winget", "search", query, "--accept-source-agreements"]
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=15,
        )

        lines = proc.stdout.splitlines()
        results = []
        # Le format Winget a des colonnes fixes séparées par des tirets
        # Exemple:
        # Nom        ID                  Version  Source
        # -----------------------------------------------
        # Brave      Brave.Brave         1.65.1   winget
        dash_line_idx = -1
        for idx, line in enumerate(lines):
            if line.startswith("---") or "---" in line:
                dash_line_idx = idx
                break

        if dash_line_idx != -1 and dash_line_idx + 1 < len(lines):
            for line in lines[dash_line_idx + 1:]:
                parts = [p.strip() for p in line.split() if p.strip()]
                if len(parts) >= 2:
                    # Approximation raisonnable : ID est souvent le 2ème élément
                    name = parts[0]
                    pkg_id = parts[1]
                    results.append({
                        "name": name,
                        "id": pkg_id,
                        "summary": f"Paquet Winget ({pkg_id})",
                        "source": "Winget (Windows)",
                        "icon": "🪟",
                        "windows_id": pkg_id,
                        "linux_id": "",
                        "category": "Personnalisé",
                    })
                    if len(results) >= 25:
                        break

        return results
