# ⚡ OmniInstaller

<div align="center">

![OmniInstaller Logo](assets/icon.png)

### L'installateur d'applications moderne et tout-en-un pour **Windows** & **Linux**
*Une alternative moderne, élégante et open-source à Ninite avec recherche dynamique et catalogue extensible.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-brightgreen.svg)]()
[![Backend Windows](https://img.shields.io/badge/Windows-Winget%20Official-0078D6.svg?logo=windows&logoColor=white)]()
[![Backend Linux](https://img.shields.io/badge/Linux-Flatpak%20%2F%20Flathub-4A90E2.svg?logo=flatpak&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Actions](https://img.shields.io/badge/Build-Automated%20CI%2FCD-purple.svg?logo=github-actions&logoColor=white)]()

[Fonctionnalités](#-fonctionnalités) •
[Téléchargement & Utilisation](#-téléchargement--utilisation) •
[Recherche d'Applications](#-recherche--catalogue-extensible) •
[Compilation (.exe & Linux)](#-compilation-locale) •
[Publication GitHub](#-publier-sur-votre-compte-github)

---

</div>

## 🌟 Fonctionnalités

- 🪟 **Support Windows Natif (Winget)** : Utilise l'outil officiel Microsoft Windows Package Manager. Téléchargements directs depuis les serveurs officiels, sans adwares ni malwares.
- 🐧 **Support Linux Universel (Flatpak / Flathub & APT)** : Compatible avec toutes les distributions modernes (Ubuntu, Debian, Fedora, Arch, etc.). Installation sans mot de passe root en mode `--user`.
- 🎨 **Interface Graphique Moderne (PyQt6)** : Thème sombre soigné (*Midnight Slate & Indigo*), cartes interactives avec sélection au clic, animations et badges colorés.
- 🔍 **Système de Recherche Puissant** :
  - **Filtre instantané** : Recherche en direct parmi plus de 40 applications prédéfinies.
  - **Filtre par catégories** : *Navigateurs, Communication, Gaming, Médias, Développement, Utilitaires, Graphisme, Bureautique*.
  - **Recherche en ligne dans les Stores** : Interroge en direct le catalogue Flathub (Linux) et Winget (Windows) pour ajouter n'importe quelle application du web !
  - **Ajout personnalisé** : Saisie libre d'identifiants de paquets pour vos besoins spécifiques.
- 🚀 **Installation Silencieuse & Asynchrone** :
  - Exécution en arrière-plan sans bloquer l'interface.
  - Console de logs en temps réel avec coloration syntaxique.
  - Barre de progression dynamique avec pourcentage et compteur.
  - Bouton d'annulation sécurisée en cours de route.
- 📦 **Exécutables Autonomes** :
  - Fichier `.exe` autonome pour Windows (aucun besoin d'installer Python).
  - Binaire autonome pour Linux (64 bits).
  - Intégration GitHub Actions : compilation et releases automatisées dans le cloud.
- 🛡️ **Zero-install Legacy inclus** : Les scripts PowerShell & Batch originaux restent conservés dans `scripts/windows-native/` pour une utilisation immédiate sans interface.

---

## 📸 Aperçu de l'Interface

```
+-------------------------------------------------------------------------------+
| ⚡ OmniInstaller                    [ 🐧 Linux (FLATPAK) ] [ ✔ Prêt (FLATPAK) ]|
+-------------------------------------------------------------------------------+
| [ 🔍 Rechercher une application...               ] [ 🌐 Chercher sur le Store ]|
| [ Toutes ] [ Navigateurs ] [ Communication ] [ Gaming ] [ Dév ] [ Utilitaires ]|
| [ Tout cocher ] [ Tout décocher ] [ ⭐ Recommandé ]   •   7 sélectionnée(s)    |
+-------------------------------------------------------------------------------+
|  +--------------------+  +--------------------+  +--------------------+       |
|  | [✔] 🦁 Brave        |  | [✔] 💬 Discord     |  | [✔] 🎮 Steam       |       |
|  | Navigateur privé   |  | Chat vocal & texte |  | Plateforme jeux PC |       |
|  | ID: com.brave...   |  | ID: com.discord... |  | ID: com.valveso... |       |
|  +--------------------+  +--------------------+  +--------------------+       |
+-------------------------------------------------------------------------------+
|  Progression : 3/7 (42%) [====================>                  ]            |
|  [📜 Afficher les logs]      [🛑 Annuler]       [🚀 Lancer l'installation (7)]|
+-------------------------------------------------------------------------------+
```

---

## 📥 Téléchargement & Utilisation

### Option 1 : Télécharger l'exécutable (Recommandé)

Rendez-vous dans la section **[Releases](../../releases)** du dépôt GitHub :
- **Sous Windows** : Téléchargez `OmniInstaller.exe` et double-cliquez dessus.
- **Sous Linux** : Téléchargez `OmniInstaller-Linux`, rendez-le exécutable (`chmod +x OmniInstaller-Linux`) puis lancez-le.

### Option 2 : Lancement direct avec Python

Si Python 3.10+ est installé sur votre ordinateur :

```bash
# 1. Cloner le dépôt
git clone https://github.com/VOTRE_PSEUDO/Installer-Apps-Windows.git
cd Installer-Apps-Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python main.py
```

Sous Windows, vous pouvez aussi simplement double-cliquer sur `Installer-Apps-Windows.bat`.

---

## 🔍 Recherche & Catalogue Extensible

OmniInstaller ne se limite pas à sa liste par défaut ! Vous pouvez :
1. Cliquer sur **🌐 Chercher sur le Store / Dépôt**.
2. Taper le nom d'un logiciel (ex: `blender`, `kdenlive`, `lutris`, `gimp`).
3. L'application interroge immédiatement les dépôts en ligne (Flathub sur Linux, Winget sur Windows).
4. Cliquer sur **➕ Ajouter** : la nouvelle carte apparaît instantanément dans votre fenêtre avec sa case cochée, prête à être installée !

---

## 📂 Structure du Projet

```text
Installer-Apps-Windows/
├── .github/
│   └── workflows/
│       └── build-and-release.yml    # CI/CD automatique (compile .exe et binaire Linux)
├── assets/
│   ├── icon.png                     # Icône de l'application
│   └── icon.ico                     # Icône Windows
├── src/
│   ├── catalog.py                   # Catalogue complet d'applications prédéfinies
│   ├── installer_backend.py         # Moteur multi-plateforme (Winget, Flatpak, APT)
│   ├── search_service.py            # API de recherche Flathub & Winget
│   └── ui/
│       ├── styles.py                # Thème sombre QSS moderne
│       ├── app_card.py              # Composant carte d'application
│       ├── search_dialog.py         # Fenêtre modale de recherche en ligne
│       └── main_window.py           # Fenêtre principale
├── scripts/
│   └── windows-native/              # Scripts Batch / PowerShell autonomes d'origine
│       ├── installer.ps1
│       ├── Installer-Tout-Directement.bat
│       └── Installer-Standalone-Native.bat
├── build.py                         # Script universel PyInstaller
├── build_windows.bat                # Script de compilation 1-clic pour Windows
├── build_linux.sh                   # Script de compilation 1-clic pour Linux
├── run_windows.bat                  # Lanceur rapide Windows
├── run_linux.sh                     # Lanceur rapide Linux
├── main.py                          # Point d'entrée de l'application
├── requirements.txt                 # Dépendances Python (PyQt6, PyInstaller)
├── .gitignore                       # Fichiers ignorés par Git
├── LICENSE                          # Licence MIT
└── README.md                        # Documentation officielle
```

---

## 🛠️ Compilation Locale

### Sous Windows (générer `OmniInstaller.exe`)
Double-cliquez sur `build_windows.bat` ou lancez :
```cmd
pip install -r requirements.txt
python build.py
```
L'exécutable standalone `.exe` est généré dans `dist\OmniInstaller.exe`.

### Sous Linux (générer `OmniInstaller-Linux`)
Exécutez :
```bash
chmod +x build_linux.sh
./build_linux.sh
```
L'exécutable autonome est généré dans `dist/OmniInstaller-Linux`.

---

## 🚀 Publier sur votre compte GitHub

Pour publier ce projet en public sur votre propre compte GitHub :

### 1. Créez un nouveau dépôt sur GitHub
1. Connectez-vous sur [github.com](https://github.com).
2. Cliquez sur le bouton vert **"New"** (Nouveau dépôt).
3. Nommez le dépôt (ex: `OmniInstaller` ou `Installer-Apps-Windows`).
4. Choisissez la visibilité **Public**.
5. **Ne cochez pas** "Add a README" ni "Add .gitignore" (ils sont déjà prêts dans votre projet !).
6. Cliquez sur **"Create repository"**.

### 2. Liez et envoyez vos fichiers depuis le terminal
Exécutez simplement les commandes suivantes dans ce dossier :

```bash
# 1. Configurer votre identité Git (si ce n'est pas déjà fait)
git config --global user.name "Votre Nom ou Pseudo"
git config --global user.email "votre-email@example.com"

# 2. Relier à votre dépôt GitHub distant (remplacez VOTRE_PSEUDO et VOTRE_DEPOT)
git remote add origin https://github.com/VOTRE_PSEUDO/Installer-Apps-Windows.git

# 3. Envoyer votre code sur GitHub
git branch -M main
git push -u origin main
```

### 3. Activer la compilation automatique des fichiers `.exe`
Dès que vous envoyez votre code ou créez un tag (ex: `git tag v1.0.0 && git push origin v1.0.0`), **GitHub Actions** va automatiquement compiler l'application sous Windows et Linux et placer `OmniInstaller.exe` et `OmniInstaller-Linux` dans la section **Releases** de votre dépôt GitHub !

---

## 📜 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de l'utiliser, le modifier et le distribuer comme bon vous semble. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
