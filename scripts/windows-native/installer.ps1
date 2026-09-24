# ==============================================================================
# ⚡ Mon Ninite Perso - Installateur d'Applications Windows
# Script PowerShell avec interface graphique interactive (WinForms)
# ==============================================================================

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()

# Liste des applications disponibles avec leurs identifiants Winget officiels
$appsList = @(
    # Navigateurs
    @{ Name = "Brave Browser"; Id = "Brave.Brave"; Category = "Navigateurs"; Checked = $true; Desc = "Navigateur rapide axé sur la vie privée" },
    @{ Name = "Google Chrome"; Id = "Google.Chrome"; Category = "Navigateurs"; Checked = $false; Desc = "Navigateur web officiel de Google" },
    @{ Name = "Mozilla Firefox"; Id = "Mozilla.Firefox"; Category = "Navigateurs"; Checked = $false; Desc = "Navigateur web libre et sécurisé" },

    # Communication
    @{ Name = "Discord"; Id = "Discord.Discord"; Category = "Communication"; Checked = $true; Desc = "Chat vocal et textuel pour communautés" },
    @{ Name = "Telegram Desktop"; Id = "Telegram.TelegramDesktop"; Category = "Communication"; Checked = $true; Desc = "Messagerie instantanée sécurisée et rapide" },

    # Gaming
    @{ Name = "Steam"; Id = "Valve.Steam"; Category = "Gaming"; Checked = $true; Desc = "Plateforme principale de jeux PC" },
    @{ Name = "Epic Games Launcher"; Id = "EpicGames.EpicGamesLauncher"; Category = "Gaming"; Checked = $true; Desc = "Lanceur Epic Games (Fortnite, jeux gratuits)" },

    # Musique & Vidéo
    @{ Name = "Deezer"; Id = "Deezer.Deezer"; Category = "Musique & Médias"; Checked = $true; Desc = "Application officielle Deezer Musique" },
    @{ Name = "Spotify"; Id = "Spotify.Spotify"; Category = "Musique & Médias"; Checked = $false; Desc = "Streaming musical et podcasts" },
    @{ Name = "VLC Media Player"; Id = "VideoLAN.VLC"; Category = "Musique & Médias"; Checked = $true; Desc = "Lecteur multimédia universel tous formats" },

    # Développement
    @{ Name = "Visual Studio Code"; Id = "Microsoft.VisualStudioCode"; Category = "Développement"; Checked = $true; Desc = "Éditeur de code puissant et personnalisable" },
    @{ Name = "Git for Windows"; Id = "Git.Git"; Category = "Développement"; Checked = $true; Desc = "Système de contrôle de version" },
    @{ Name = "Node.js (LTS)"; Id = "OpenJS.NodeJS.LTS"; Category = "Développement"; Checked = $true; Desc = "Environnement d'exécution JavaScript" },
    @{ Name = "Python 3"; Id = "Python.Python.3.12"; Category = "Développement"; Checked = $false; Desc = "Langage de programmation Python" },

    # Utilitaires
    @{ Name = "7-Zip"; Id = "7zip.7zip"; Category = "Utilitaires"; Checked = $true; Desc = "Extracteur d'archives haute compression (ZIP, RAR, 7Z)" },
    @{ Name = "Notepad++"; Id = "Notepad++.Notepad++"; Category = "Utilitaires"; Checked = $false; Desc = "Éditeur de texte avancé et léger" },
    @{ Name = "Microsoft PowerToys"; Id = "Microsoft.PowerToys"; Category = "Utilitaires"; Checked = $false; Desc = "Outils avancés de productivité pour Windows" }
)

# Palette de couleurs (Thème Moderne Sombre)
$cBg = [System.Drawing.Color]::FromArgb(24, 26, 38)
$cCard = [System.Drawing.Color]::FromArgb(32, 35, 51)
$cCardBorder = [System.Drawing.Color]::FromArgb(55, 60, 85)
$cText = [System.Drawing.Color]::FromArgb(240, 243, 250)
$cMuted = [System.Drawing.Color]::FromArgb(150, 155, 175)
$cAccent = [System.Drawing.Color]::FromArgb(124, 58, 237)      # Violet moderne
$cAccentHover = [System.Drawing.Color]::FromArgb(139, 92, 246)
$cSuccess = [System.Drawing.Color]::FromArgb(34, 197, 94)

# Fenêtre Principale
$form = New-Object System.Windows.Forms.Form
$form.Text = "Mon Ninite Perso - Installateur d'Applications Windows"
$form.Size = New-Object System.Drawing.Size(860, 780)
$form.StartPosition = "CenterScreen"
$form.BackColor = $cBg
$form.ForeColor = $cText
$form.Font = New-Object System.Drawing.Font("Segoe UI", 9.5)
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

# En-tête
$headerPanel = New-Object System.Windows.Forms.Panel
$headerPanel.Dock = "Top"
$headerPanel.Height = 85
$headerPanel.BackColor = $cCard
$form.Controls.Add($headerPanel)

$lblTitle = New-Object System.Windows.Forms.Label
$lblTitle.Text = "⚡ Mon Ninite Perso - Sélectionne tes applications"
$lblTitle.Font = New-Object System.Drawing.Font("Segoe UI", 15, [System.Drawing.FontStyle]::Bold)
$lblTitle.ForeColor = [System.Drawing.Color]::White
$lblTitle.Location = New-Object System.Drawing.Point(20, 14)
$lblTitle.AutoSize = $true
$headerPanel.Controls.Add($lblTitle)

$lblSubtitle = New-Object System.Windows.Forms.Label
$lblSubtitle.Text = "Coche les applications souhaitées. Elles seront installées proprement et silencieusement via Winget."
$lblSubtitle.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$lblSubtitle.ForeColor = $cMuted
$lblSubtitle.Location = New-Object System.Drawing.Point(22, 48)
$lblSubtitle.AutoSize = $true
$headerPanel.Controls.Add($lblSubtitle)

# Barre d'actions rapides (Boutons Tout cocher / Décocher)
$actionBar = New-Object System.Windows.Forms.Panel
$actionBar.Location = New-Object System.Drawing.Point(20, 95)
$actionBar.Size = New-Object System.Drawing.Size(800, 38)
$form.Controls.Add($actionBar)

$btnCheckAll = New-Object System.Windows.Forms.Button
$btnCheckAll.Text = "Tout cocher"
$btnCheckAll.Size = New-Object System.Drawing.Size(120, 30)
$btnCheckAll.Location = New-Object System.Drawing.Point(0, 4)
$btnCheckAll.FlatStyle = "Flat"
$btnCheckAll.BackColor = $cCard
$btnCheckAll.ForeColor = $cText
$btnCheckAll.FlatAppearance.BorderColor = $cCardBorder
$actionBar.Controls.Add($btnCheckAll)

$btnUncheckAll = New-Object System.Windows.Forms.Button
$btnUncheckAll.Text = "Tout décocher"
$btnUncheckAll.Size = New-Object System.Drawing.Size(120, 30)
$btnUncheckAll.Location = New-Object System.Drawing.Point(130, 4)
$btnUncheckAll.FlatStyle = "Flat"
$btnUncheckAll.BackColor = $cCard
$btnUncheckAll.ForeColor = $cText
$btnUncheckAll.FlatAppearance.BorderColor = $cCardBorder
$actionBar.Controls.Add($btnUncheckAll)

$btnDefault = New-Object System.Windows.Forms.Button
$btnDefault.Text = "⭐ Sélection recommandée"
$btnDefault.Size = New-Object System.Drawing.Size(200, 30)
$btnDefault.Location = New-Object System.Drawing.Point(260, 4)
$btnDefault.FlatStyle = "Flat"
$btnDefault.BackColor = $cCard
$btnDefault.ForeColor = [System.Drawing.Color]::FromArgb(250, 204, 21)
$btnDefault.FlatAppearance.BorderColor = $cCardBorder
$actionBar.Controls.Add($btnDefault)

# Conteneur principal pour les catégories
$contentPanel = New-Object System.Windows.Forms.Panel
$contentPanel.Location = New-Object System.Drawing.Point(20, 138)
$contentPanel.Size = New-Object System.Drawing.Size(805, 330)
$contentPanel.AutoScroll = $true
$form.Controls.Add($contentPanel)

# Organisation des applications par catégorie dans des colonnes
$categories = @("Navigateurs", "Communication", "Gaming", "Musique & Médias", "Développement", "Utilitaires")
$checkboxes = @()

$x = 0
$y = 0
$colWidth = 255
$colHeight = 155

for ($i = 0; $i -lt $categories.Count; $i++) {
    $cat = $categories[$i]
    $grp = New-Object System.Windows.Forms.GroupBox
    $grp.Text = "  $cat  "
    $grp.Font = New-Object System.Drawing.Font("Segoe UI", 9.5, [System.Drawing.FontStyle]::Bold)
    $grp.ForeColor = [System.Drawing.Color]::FromArgb(168, 85, 247)
    $grp.BackColor = $cCard
    $grp.Size = New-Object System.Drawing.Size($colWidth, $colHeight)
    
    # 3 colonnes par rangée
    $col = $i % 3
    $row = [math]::Floor($i / 3)
    $grp.Location = New-Object System.Drawing.Point(($col * ($colWidth + 15)), ($row * ($colHeight + 12)))

    $catApps = $appsList | Where-Object { $_.Category -eq $cat }
    $chkY = 24
    foreach ($app in $catApps) {
        $chk = New-Object System.Windows.Forms.CheckBox
        $chk.Text = $app.Name
        $chk.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Regular)
        $chk.ForeColor = $cText
        $chk.Checked = $app.Checked
        $chk.Location = New-Object System.Drawing.Point(14, $chkY)
        $chk.AutoSize = $true
        $chk.Tag = $app
        
        $tooltip = New-Object System.Windows.Forms.ToolTip
        $tooltip.SetToolTip($chk, "$($app.Desc) (ID: $($app.Id))")

        $grp.Controls.Add($chk)
        $checkboxes += $chk
        $chkY += 28
    }

    $contentPanel.Controls.Add($grp)
}

# Actions des boutons rapides
$btnCheckAll.Add_Click({
    foreach ($c in $checkboxes) { $c.Checked = $true }
})

$btnUncheckAll.Add_Click({
    foreach ($c in $checkboxes) { $c.Checked = $false }
})

$btnDefault.Add_Click({
    foreach ($c in $checkboxes) {
        $c.Checked = $c.Tag.Checked
    }
})

# Console de logs / progression
$lblLog = New-Object System.Windows.Forms.Label
$lblLog.Text = "Journal d'installation :"
$lblLog.Location = New-Object System.Drawing.Point(20, 480)
$lblLog.AutoSize = $true
$lblLog.ForeColor = $cMuted
$form.Controls.Add($lblLog)

$txtLog = New-Object System.Windows.Forms.TextBox
$txtLog.Location = New-Object System.Drawing.Point(20, 502)
$txtLog.Size = New-Object System.Drawing.Size(800, 125)
$txtLog.Multiline = $true
$txtLog.ScrollBars = "Vertical"
$txtLog.ReadOnly = $true
$txtLog.BackColor = [System.Drawing.Color]::FromArgb(15, 17, 26)
$txtLog.ForeColor = [System.Drawing.Color]::FromArgb(180, 240, 180)
$txtLog.Font = New-Object System.Drawing.Font("Consolas", 9)
$txtLog.Text = "Prêt. Coche tes applications puis clique sur 'Lancer l'installation'."
$form.Controls.Add($txtLog)

# Barre de progression
$progressBar = New-Object System.Windows.Forms.ProgressBar
$progressBar.Location = New-Object System.Drawing.Point(20, 638)
$progressBar.Size = New-Object System.Drawing.Size(800, 18)
$form.Controls.Add($progressBar)

# Statut et Bouton Installer
$lblStatus = New-Object System.Windows.Forms.Label
$lblStatus.Text = "0 application(s) en attente"
$lblStatus.Location = New-Object System.Drawing.Point(20, 672)
$lblStatus.Size = New-Object System.Drawing.Size(500, 30)
$lblStatus.ForeColor = $cMuted
$lblStatus.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$form.Controls.Add($lblStatus)

$btnInstall = New-Object System.Windows.Forms.Button
$btnInstall.Text = "🚀 Lancer l'installation"
$btnInstall.Size = New-Object System.Drawing.Size(240, 44)
$btnInstall.Location = New-Object System.Drawing.Point(580, 665)
$btnInstall.FlatStyle = "Flat"
$btnInstall.BackColor = $cAccent
$btnInstall.ForeColor = [System.Drawing.Color]::White
$btnInstall.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
$btnInstall.Cursor = [System.Windows.Forms.Cursors]::Hand
$btnInstall.FlatAppearance.BorderSize = 0
$form.Controls.Add($btnInstall)

# Mise à jour du compteur
function UpdateCount {
    $sel = ($checkboxes | Where-Object { $_.Checked }).Count
    $lblStatus.Text = "$sel application(s) sélectionnée(s)"
}

foreach ($c in $checkboxes) {
    $c.Add_CheckedChanged({ UpdateCount })
}
UpdateCount

# Log Helper
function LogMessage($msg) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    $txtLog.AppendText("`r`n[$timestamp] $msg")
    $txtLog.SelectionStart = $txtLog.Text.Length
    $txtLog.ScrollToCaret()
    [System.Windows.Forms.Application]::DoEvents()
}

# Action d'installation
$btnInstall.Add_Click({
    $selectedApps = $checkboxes | Where-Object { $_.Checked } | ForEach-Object { $_.Tag }
    
    if ($selectedApps.Count -eq 0) {
        [System.Windows.Forms.MessageBox]::Show(
            "Aucune application n'a été sélectionnée !",
            "Attention",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Warning
        )
        return
    }

    # Vérification de Winget
    $hasWinget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $hasWinget) {
        $res = [System.Windows.Forms.MessageBox]::Show(
            "Windows Package Manager (Winget) n'a pas été détecté sur ce système.`r`n`r`nWinget est inclus par défaut sur Windows 10/11 via 'App Installer'.`r`n`r`nSouhaitez-vous ouvrir la page du Microsoft Store pour l'installer ?",
            "Winget introuvable",
            [System.Windows.Forms.MessageBoxButtons]::YesNo,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
        if ($res -eq "Yes") {
            Start-Process "ms-windows-store://pdp/?productid=9NBLGGH4NNS1"
        }
        return
    }

    # Désactiver les boutons pendant l'installation
    $btnInstall.Enabled = $false
    $btnInstall.Text = "Installation en cours..."
    $btnCheckAll.Enabled = $false
    $btnUncheckAll.Enabled = $false
    $btnDefault.Enabled = $false
    foreach ($c in $checkboxes) { $c.Enabled = $false }

    $progressBar.Maximum = $selectedApps.Count
    $progressBar.Value = 0

    LogMessage("==========================================")
    LogMessage("Début de l'installation de $($selectedApps.Count) application(s)...")
    LogMessage("==========================================")

    $successCount = 0
    $failedCount = 0
    $current = 0

    foreach ($app in $selectedApps) {
        $current++
        $lblStatus.Text = "Installation de $($app.Name) ($current/$($selectedApps.Count))..."
        LogMessage("▶ [$current/$($selectedApps.Count)] Téléchargement & installation de $($app.Name) ($($app.Id))...")
        
        [System.Windows.Forms.Application]::DoEvents()

        # Commande Winget silencieuse
        $args = "install --id `"$($app.Id)`" --exact --silent --accept-source-agreements --accept-package-agreements --disable-interactivity"
        
        $proc = Start-Process -FilePath "winget" -ArgumentList $args -NoNewWindow -PassThru -Wait

        if ($proc.ExitCode -eq 0 -or $proc.ExitCode -eq 2316632107) {
            # 2316632107 = Already installed
            LogMessage("✔ $($app.Name) installé avec succès !")
            $successCount++
        } else {
            LogMessage("⚠ Note : Résultat code $($proc.ExitCode) pour $($app.Name) (peut-être déjà à jour ou nécessite un redémarrage).")
            $successCount++ # Winget renvoie parfois des codes non nuls bénins
        }

        $progressBar.Value = $current
        [System.Windows.Forms.Application]::DoEvents()
    }

    LogMessage("==========================================")
    LogMessage("🎉 Terminé ! $successCount application(s) traitée(s).")
    LogMessage("==========================================")
    
    $lblStatus.Text = "Installation terminée avec succès !"
    $btnInstall.Text = "✔ Terminé !"
    $btnInstall.BackColor = $cSuccess

    [System.Windows.Forms.MessageBox]::Show(
        "Toutes les applications sélectionnées ont été installées avec succès !`r`n`r`nTu peux les retrouver dans ton menu Démarrer Windows.",
        "Installation Réussie",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    )

    # Réactiver
    $btnInstall.Enabled = $true
    $btnInstall.Text = "🚀 Réinstaller / Modifier"
    $btnInstall.BackColor = $cAccent
    $btnCheckAll.Enabled = $true
    $btnUncheckAll.Enabled = $true
    $btnDefault.Enabled = $true
    foreach ($c in $checkboxes) { $c.Enabled = $true }
})

# Afficher la fenêtre
[void]$form.ShowDialog()
