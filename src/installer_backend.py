"""
Gestionnaire d'installation multi-plateforme (Windows & Linux).
Détecte l'environnement, prépare les commandes d'installation et exécute
l'installation en arrière-plan avec reporting en temps réel via signaux Qt.
"""

import sys
import os
import shutil
import subprocess
import time
from typing import List, Dict, Optional
from PyQt6.QtCore import QThread, pyqtSignal


def is_windows() -> bool:
    return sys.platform == "win32"


def is_linux() -> bool:
    return sys.platform.startswith("linux")


def get_current_os_name() -> str:
    if is_windows():
        return "Windows"
    elif is_linux():
        return "Linux"
    return "Inconnu"


class SystemDetector:
    """Détecte les outils d'installation disponibles sur la machine."""

    @staticmethod
    def check_winget() -> bool:
        if not is_windows():
            return False
        return shutil.which("winget") is not None

    @staticmethod
    def check_flatpak() -> bool:
        if not is_linux():
            return False
        return shutil.which("flatpak") is not None

    @staticmethod
    def check_apt() -> bool:
        if not is_linux():
            return False
        return shutil.which("apt-get") is not None or shutil.which("apt") is not None

    @staticmethod
    def check_pacman() -> bool:
        if not is_linux():
            return False
        return shutil.which("pacman") is not None

    @staticmethod
    def check_dnf() -> bool:
        if not is_linux():
            return False
        return shutil.which("dnf") is not None

    @classmethod
    def get_preferred_backend(cls) -> str:
        """Retourne le gestionnaire principal recommandé."""
        if is_windows():
            return "winget" if cls.check_winget() else "missing_winget"
        elif is_linux():
            if cls.check_flatpak():
                return "flatpak"
            elif cls.check_apt():
                return "apt"
            elif cls.check_pacman():
                return "pacman"
            elif cls.check_dnf():
                return "dnf"
            return "missing_linux_pm"
        return "unsupported"

    @classmethod
    def get_status_info(cls) -> Dict[str, str]:
        """Retourne un dictionnaire informatif sur l'état du système."""
        os_name = get_current_os_name()
        backend = cls.get_preferred_backend()

        if is_windows():
            if backend == "winget":
                return {
                    "os": "Windows",
                    "backend": "winget",
                    "status": "ready",
                    "message": "Windows Package Manager (Winget) détecté et prêt.",
                }
            else:
                return {
                    "os": "Windows",
                    "backend": "none",
                    "status": "warning",
                    "message": "Winget introuvable. Installez 'App Installer' depuis le Microsoft Store.",
                }
        elif is_linux():
            if backend == "flatpak":
                return {
                    "os": "Linux",
                    "backend": "flatpak",
                    "status": "ready",
                    "message": "Flatpak (Flathub) détecté et prêt.",
                }
            elif backend in ("apt", "pacman", "dnf"):
                return {
                    "os": "Linux",
                    "backend": backend,
                    "status": "ready",
                    "message": f"Gestionnaire système ({backend.upper()}) détecté.",
                }
            else:
                return {
                    "os": "Linux",
                    "backend": "none",
                    "status": "warning",
                    "message": "Aucun gestionnaire (flatpak/apt/pacman/dnf) détecté.",
                }
        return {
            "os": os_name,
            "backend": "unknown",
            "status": "error",
            "message": "Système d'exploitation non pris en charge.",
        }

    @classmethod
    def ensure_flathub_user_remote(cls) -> bool:
        """S'assure que le remote flathub est configuré en mode user."""
        if not cls.check_flatpak():
            return False
        try:
            # Vérifie si flathub est présent
            res = subprocess.run(
                ["flatpak", "remotes", "--user"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            if "flathub" not in res.stdout:
                subprocess.run(
                    [
                        "flatpak",
                        "remote-add",
                        "--user",
                        "--if-not-exists",
                        "flathub",
                        "https://dl.flathub.org/repo/flathub.flatpakrepo",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                )
            return True
        except Exception:
            return False


class InstallationWorker(QThread):
    """
    Thread en arrière-plan pour exécuter les commandes d'installation
    sans bloquer l'interface graphique.
    """

    sig_log = pyqtSignal(str, str)         # (message, level: 'info', 'success', 'warning', 'error')
    sig_progress = pyqtSignal(int, int)    # (current_count, total_count)
    sig_current_app = pyqtSignal(str)      # nom de l'application en cours
    sig_finished = pyqtSignal(dict)        # {total, succeeded, failed, duration}

    def __init__(self, selected_apps: List[Dict]):
        super().__init__()
        self.selected_apps = selected_apps
        self._is_cancelled = False
        self._current_process: Optional[subprocess.Popen] = None

    def cancel(self):
        """Demande l'annulation de l'installation en cours."""
        self._is_cancelled = True
        if self._current_process:
            try:
                self._current_process.terminate()
            except Exception:
                pass

    def run(self):
        start_time = time.time()
        total = len(self.selected_apps)
        succeeded = 0
        failed = 0
        failed_apps = []

        self.sig_log.emit(
            f"🚀 Démarrage de l'installation de {total} application(s)...",
            "info"
        )

        # Préparation Linux (configuration user remote Flathub si applicable)
        if is_linux():
            SystemDetector.ensure_flathub_user_remote()

        for index, app in enumerate(self.selected_apps, 1):
            if self._is_cancelled:
                self.sig_log.emit("🛑 Installation interrompue par l'utilisateur.", "warning")
                break

            app_name = app.get("name", "Application")
            self.sig_current_app.emit(app_name)
            self.sig_progress.emit(index, total)

            self.sig_log.emit(
                f"[{index}/{total}] Préparation de l'installation de {app_name}...",
                "info"
            )

            cmd = self._build_install_command(app)
            if not cmd:
                self.sig_log.emit(
                    f"⚠️ Aucune commande disponible pour {app_name} sur ce système ({get_current_os_name()}).",
                    "warning"
                )
                failed += 1
                failed_apps.append(app_name)
                continue

            # Exécution de la commande
            ok = self._run_command(cmd, app_name)
            if ok:
                succeeded += 1
                self.sig_log.emit(f"✔ {app_name} installé avec succès !", "success")
            else:
                failed += 1
                failed_apps.append(app_name)
                self.sig_log.emit(f"❌ Échec de l'installation de {app_name}.", "error")

        duration = round(time.time() - start_time, 1)
        self.sig_finished.emit({
            "total": total,
            "succeeded": succeeded,
            "failed": failed,
            "failed_apps": failed_apps,
            "cancelled": self._is_cancelled,
            "duration": duration,
        })

    def _build_install_command(self, app: Dict) -> Optional[List[str]]:
        """Génère la liste d'arguments de commande selon l'OS et l'application."""
        if is_windows():
            pkg_id = app.get("windows_id")
            if not pkg_id:
                return None
            return [
                "winget",
                "install",
                "--id",
                pkg_id,
                "--exact",
                "--silent",
                "--accept-source-agreements",
                "--accept-package-agreements",
                "--disable-interactivity",
            ]
        elif is_linux():
            pkg_id = app.get("linux_id")
            if not pkg_id:
                return None

            linux_type = app.get("linux_type", "flatpak")

            if linux_type == "flatpak" or SystemDetector.check_flatpak():
                # Installation Flatpak non-interactive en mode --user (pas besoin de mot de passe sudo)
                return [
                    "flatpak",
                    "install",
                    "-y",
                    "--user",
                    "flathub",
                    pkg_id,
                    "--noninteractive",
                ]
            elif SystemDetector.check_apt():
                # APT système
                return ["apt-get", "install", "-y", pkg_id]
            elif SystemDetector.check_pacman():
                return ["pacman", "-S", "--noconfirm", pkg_id]
            elif SystemDetector.check_dnf():
                return ["dnf", "install", "-y", pkg_id]

        return None

    def _run_command(self, cmd: List[str], app_name: str) -> bool:
        """Exécute une commande de manière sûre avec streaming des logs."""
        try:
            self.sig_log.emit(f"⚙️ Commande : {' '.join(cmd)}", "info")

            self._current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            # Lecture ligne par ligne pour logs en temps réel
            if self._current_process.stdout:
                for line in iter(self._current_process.stdout.readline, ""):
                    if self._is_cancelled:
                        self._current_process.terminate()
                        return False
                    cleaned = line.strip()
                    if cleaned:
                        self.sig_log.emit(f"   {cleaned}", "info")

            self._current_process.wait()
            code = self._current_process.returncode

            # Codes de succès Winget & Flatpak
            # Winget 0 = succès, 2316632107 = déjà installé
            # Flatpak 0 = succès
            if code == 0 or code == 2316632107:
                return True
            else:
                self.sig_log.emit(f"Code retour commande : {code}", "warning")
                # Certains codes Winget bénins (redémarrage nécessaire, déjà installé etc.)
                if is_windows() and code in (-1978335189, 2316632107, 3010):
                    return True
                return False
        except Exception as e:
            self.sig_log.emit(f"Erreur d'exécution pour {app_name}: {str(e)}", "error")
            return False
        finally:
            self._current_process = None
