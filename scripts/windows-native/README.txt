==============================================================================
⚡ MON NINITE PERSO - INSTALLATEUR D'APPLICATIONS WINDOWS
==============================================================================

Ce dossier contient des scripts prêts à l'emploi pour installer automatiquement
toutes tes applications sur Windows 10 et Windows 11 en un simple double-clic !

------------------------------------------------------------------------------
📦 DEUX MODES D'UTILISATION :
------------------------------------------------------------------------------

1. Mode Graphique (Type Ninite) - RECOMMANDÉ :
   👉 Fichier : Installer-Apps-Windows.bat
   - Fais simplement un DOUBLE-CLIC sur ce fichier sous Windows.
   - Il demande automatiquement les droits Administrateur (invite Windows UAC).
   - Une belle fenêtre s'ouvre avec tes applications classées par catégorie.
   - Par défaut, tes applications préférées sont déjà pré-cochées :
     * VS Code
     * Steam
     * Discord
     * Epic Games Launcher
     * Deezer
     * Brave
     * Telegram
     * 7-Zip, Git, Node.js, VLC, etc.
   - Tu peux cocher / décocher ce que tu veux, puis cliquer sur :
     "🚀 Lancer l'installation".

2. Mode Direct & Silencieux (Invite de commande) :
   👉 Fichier : Installer-Tout-Directement.bat
   - Double-clique dessus pour installer directement toute la liste
     sans aucune fenêtre de confirmation.

------------------------------------------------------------------------------
⚙️ COMMENT ÇA FONCTIONNE SOUS LE CAPOT ?
------------------------------------------------------------------------------
Les scripts utilisent "Winget" (Windows Package Manager), l'outil officiel
de Microsoft intégré nativement dans Windows 10 et Windows 11.

Avantages majeurs par rapport aux installateurs manuels :
- 100% Officiel et sans logiciels publicitaires / adwares
- Téléchargement direct depuis les serveurs officiels des éditeurs
- Installation silencieuse en arrière-plan sans avoir à cliquer sur "Suivant, Suivant..."
- Mises à jour faciles plus tard avec la commande Windows : "winget upgrade --all"

------------------------------------------------------------------------------
🔧 COMMENT PERSONNALISER LA LISTE ?
------------------------------------------------------------------------------
Tu peux ouvrir `Installer-Apps-Windows.bat` avec le Bloc-notes (Clic droit > Modifier)
et ajouter n'importe quelle application du catalogue Winget en ajoutant une ligne :
@{ Name = "Nom"; Id = "Identifiant.Winget"; Category = "..."; Checked = $true; Desc = "..." }
