"""
Script pour télécharger les vrais logos officiels (PNG haute résolution) de toutes les applications du catalogue.
"""
import os
import sys
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS_DIR = os.path.join(BASE_DIR, "assets", "logos")
os.makedirs(LOGOS_DIR, exist_ok=True)

# Mapping des apps vers les URLs potentielles d'icônes officielles de haute qualité
APPS_MAP = {
    "brave": ["brave.png"],
    "chrome": ["google-chrome.png", "chrome.png"],
    "firefox": ["firefox.png", "mozilla-firefox.png"],
    "edge": ["microsoft-edge.png", "edge.png"],
    "opera": ["opera.png"],
    "tor": ["tor.png", "tor-browser.png"],
    "discord": ["discord.png"],
    "telegram": ["telegram.png"],
    "signal": ["signal.png"],
    "whatsapp": ["whatsapp.png"],
    "slack": ["slack.png"],
    "zoom": ["zoom.png"],
    "steam": ["steam.png"],
    "epicgames": ["epic-games.png", "epicgames.png"],
    "heroic": ["heroic.png", "heroic-games-launcher.png"],
    "lutris": ["lutris.png"],
    "retroarch": ["retroarch.png"],
    "deezer": ["deezer.png"],
    "spotify": ["spotify.png"],
    "vlc": ["vlc.png"],
    "obs": ["obs.png", "obs-studio.png"],
    "audacity": ["audacity.png"],
    "handbrake": ["handbrake.png"],
    "vscode": ["visual-studio-code.png", "vscode.png"],
    "git": ["git.png"],
    "nodejs": ["nodejs.png", "node-js.png"],
    "python": ["python.png"],
    "postman": ["postman.png"],
    "dbeaver": ["dbeaver.png"],
    "sublimetext": ["sublime-text.png", "sublimetext.png"],
    "7zip": ["7-zip.png", "7zip.png"],
    "notepadplusplus": ["notepad-plus-plus.png", "notepad++.png", "notepad.png"],
    "powertoys": ["powertoys.png", "microsoft-powertoys.png", "microsoft.png"],
    "bitwarden": ["bitwarden.png"],
    "keepassxc": ["keepassxc.png"],
    "qbittorrent": ["qbittorrent.png"],
    "bleachbit": ["bleachbit.png"],
    "gimp": ["gimp.png"],
    "inkscape": ["inkscape.png"],
    "blender": ["blender.png"],
    "krita": ["krita.png"],
    "libreoffice": ["libreoffice.png"],
    "obsidian": ["obsidian.png"],
    "notion": ["notion.png"],
}

# Sources CDNs
CDNS = [
    "https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/{name}",
    "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/{name}",
    "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/{name}",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_logo(app_id, candidates):
    dest = os.path.join(LOGOS_DIR, f"{app_id}.png")
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"✔ {app_id} déjà présent ({os.path.getsize(dest)} octets)")
        return True

    for cand in candidates:
        for cdn in CDNS:
            url = cdn.format(name=cand)
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=7) as resp:
                    if resp.status == 200:
                        data = resp.read()
                        if len(data) > 500:
                            with open(dest, "wb") as f:
                                f.write(data)
                            print(f"✔ {app_id} téléchargé depuis {cand} ({len(data)} octets)")
                            return True
            except Exception:
                pass
    print(f"❌ Échec pour {app_id}")
    return False

def main():
    print(f"Téléchargement des logos dans {LOGOS_DIR}...")
    success = 0
    for app_id, cands in APPS_MAP.items():
        if download_logo(app_id, cands):
            success += 1
    print(f"\nRésultat: {success}/{len(APPS_MAP)} logos téléchargés avec succès.")

if __name__ == "__main__":
    main()
