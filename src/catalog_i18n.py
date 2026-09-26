"""
Traductions des descriptions du catalogue (44 applications x 5 langues).

Le français est la langue source (champ "desc" de src/catalog.py).
Ce module fournit les descriptions en English, Español, Deutsch,
Italiano et Português, avec repli automatique sur le français
si une traduction manque (ex : applications ajoutées par l'utilisateur).

Utilisation :
    from src.catalog_i18n import tr_desc
    label.setText(tr_desc(app_data))
"""

from typing import Dict

from src.i18n import get_language


# app_id -> {lang_code -> description traduite}
APP_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    # ── Navigateurs ──
    "brave": {
        "en": "Fast browser focused on privacy and ad blocking",
        "es": "Navegador rápido centrado en la privacidad y el bloqueo de anuncios",
        "de": "Schneller Browser mit Fokus auf Privatsphäre und Werbeblocker",
        "it": "Browser veloce incentrato sulla privacy e sul blocco degli annunci",
        "pt": "Navegador rápido focado em privacidade e bloqueio de anúncios",
    },
    "chrome": {
        "en": "Google's official web browser, fast and synced",
        "es": "Navegador web oficial de Google, rápido y sincronizado",
        "de": "Offizieller Webbrowser von Google, schnell und synchronisiert",
        "it": "Browser web ufficiale di Google, veloce e sincronizzato",
        "pt": "Navegador web oficial do Google, rápido e sincronizado",
    },
    "firefox": {
        "en": "Free web browser, privacy-friendly and customizable",
        "es": "Navegador web libre, respetuoso con la privacidad y personalizable",
        "de": "Freier Webbrowser, datenschutzfreundlich und anpassbar",
        "it": "Browser web libero, rispettoso della privacy e personalizzabile",
        "pt": "Navegador web livre, respeita a privacidade e personalizável",
    },
    "edge": {
        "en": "Optimized Microsoft browser with built-in Copilot tools",
        "es": "Navegador optimizado de Microsoft con herramientas Copilot integradas",
        "de": "Optimierter Microsoft-Browser mit integrierten Copilot-Tools",
        "it": "Browser Microsoft ottimizzato con strumenti Copilot integrati",
        "pt": "Navegador otimizado da Microsoft com ferramentas Copilot integradas",
    },
    "opera": {
        "en": "Innovative browser with VPN and built-in messengers",
        "es": "Navegador innovador con VPN y mensajería integrada",
        "de": "Innovativer Browser mit VPN und integrierten Messengern",
        "it": "Browser innovativo con VPN e messaggistica integrata",
        "pt": "Navegador inovador com VPN e mensagens integradas",
    },
    "tor": {
        "en": "Anonymous and secure browsing via the decentralized Tor network",
        "es": "Navegación anónima y segura a través de la red descentralizada Tor",
        "de": "Anonymes und sicheres Surfen über das dezentrale Tor-Netzwerk",
        "it": "Navigazione anonima e sicura tramite la rete decentralizzata Tor",
        "pt": "Navegação anônima e segura pela rede descentralizada Tor",
    },
    # ── Communication ──
    "discord": {
        "en": "Voice, video and text chat for communities and friends",
        "es": "Chat de voz, vídeo y texto para comunidades y amigos",
        "de": "Sprach-, Video- und Text-Chat für Communities und Freunde",
        "it": "Chat vocale, video e testuale per community e amici",
        "pt": "Chat de voz, vídeo e texto para comunidades e amigos",
    },
    "telegram": {
        "en": "Ultra-fast, encrypted and synced instant messaging",
        "es": "Mensajería instantánea ultrarrápida, cifrada y sincronizada",
        "de": "Blitzschnelles, verschlüsseltes und synchronisiertes Messaging",
        "it": "Messaggistica istantanea velocissima, crittografata e sincronizzata",
        "pt": "Mensagens instantâneas ultrarrápidas, criptografadas e sincronizadas",
    },
    "signal": {
        "en": "Secure messaging with strict end-to-end encryption",
        "es": "Mensajería segura con cifrado estricto de extremo a extremo",
        "de": "Sicheres Messaging mit strenger Ende-zu-Ende-Verschlüsselung",
        "it": "Messaggistica sicura con rigorosa crittografia end-to-end",
        "pt": "Mensagens seguras com criptografia rígida de ponta a ponta",
    },
    "whatsapp": {
        "en": "Official WhatsApp messaging and calls app",
        "es": "Aplicación oficial de mensajería y llamadas de WhatsApp",
        "de": "Offizielle WhatsApp-App für Nachrichten und Anrufe",
        "it": "App ufficiale di messaggistica e chiamate WhatsApp",
        "pt": "Aplicativo oficial de mensagens e chamadas do WhatsApp",
    },
    "slack": {
        "en": "Collaboration and communication platform for teams",
        "es": "Plataforma de colaboración y comunicación para equipos",
        "de": "Kollaborations- und Kommunikationsplattform für Teams",
        "it": "Piattaforma di collaborazione e comunicazione per i team",
        "pt": "Plataforma de colaboração e comunicação para equipes",
    },
    "zoom": {
        "en": "High-definition video conferencing and virtual meetings",
        "es": "Videoconferencias y reuniones virtuales en alta definición",
        "de": "Videokonferenzen und virtuelle Meetings in HD",
        "it": "Videoconferenze e riunioni virtuali in alta definizione",
        "pt": "Videoconferências e reuniões virtuais em alta definição",
    },
    # ── Gaming ──
    "steam": {
        "en": "The largest PC video game distribution platform",
        "es": "La mayor plataforma de distribución de videojuegos para PC",
        "de": "Die größte Vertriebsplattform für PC-Videospiele",
        "it": "La più grande piattaforma di distribuzione di videogiochi per PC",
        "pt": "A maior plataforma de distribuição de jogos para PC",
    },
    "epicgames": {
        "en": "Epic Games store (Fortnite, Unreal Engine, free games)",
        "es": "Tienda de Epic Games (Fortnite, Unreal Engine, juegos gratis)",
        "de": "Epic Games Store (Fortnite, Unreal Engine, Gratis-Spiele)",
        "it": "Negozio Epic Games (Fortnite, Unreal Engine, giochi gratuiti)",
        "pt": "Loja Epic Games (Fortnite, Unreal Engine, jogos grátis)",
    },
    "heroic": {
        "en": "Open-source launcher for Epic Games and GOG games",
        "es": "Lanzador de código abierto para juegos de Epic Games y GOG",
        "de": "Open-Source-Launcher für Epic-Games- und GOG-Spiele",
        "it": "Avviatore open-source per giochi Epic Games e GOG",
        "pt": "Lançador de código aberto para jogos Epic Games e GOG",
    },
    "lutris": {
        "en": "Universal open-source game manager for Linux",
        "es": "Gestor de juegos universal de código abierto para Linux",
        "de": "Universeller Open-Source-Spielemanager für Linux",
        "it": "Gestore di giochi universale open-source per Linux",
        "pt": "Gerenciador de jogos universal de código aberto para Linux",
    },
    "retroarch": {
        "en": "Powerful frontend for retro console emulators",
        "es": "Potente interfaz para emuladores de consolas retro",
        "de": "Leistungsstarkes Frontend für Retro-Konsolen-Emulatoren",
        "it": "Potente frontend per emulatori di console retrò",
        "pt": "Frontend poderoso para emuladores de consoles retrô",
    },
    # ── Musique & Médias ──
    "deezer": {
        "en": "Official Deezer music streaming app",
        "es": "Aplicación oficial de streaming musical Deezer",
        "de": "Offizielle Deezer-App für Musik-Streaming",
        "it": "App ufficiale di streaming musicale Deezer",
        "pt": "Aplicativo oficial de streaming de música Deezer",
    },
    "spotify": {
        "en": "World-leading music streaming and podcast service",
        "es": "Servicio líder mundial de streaming musical y pódcasts",
        "de": "Weltweit führender Musik-Streaming- und Podcast-Dienst",
        "it": "Servizio leader mondiale di streaming musicale e podcast",
        "pt": "Serviço líder mundial de streaming de música e podcasts",
    },
    "vlc": {
        "en": "Universal media player for all video and audio formats",
        "es": "Reproductor multimedia universal para todos los formatos de vídeo y audio",
        "de": "Universeller Mediaplayer für alle Video- und Audioformate",
        "it": "Lettore multimediale universale per tutti i formati video e audio",
        "pt": "Reprodutor de mídia universal para todos os formatos de vídeo e áudio",
    },
    "obs": {
        "en": "Reference software for video recording and live streaming",
        "es": "Software de referencia para grabación de vídeo y streaming en directo",
        "de": "Referenz-Software für Videoaufnahmen und Live-Streaming",
        "it": "Software di riferimento per registrazione video e live streaming",
        "pt": "Software de referência para gravação de vídeo e transmissão ao vivo",
    },
    "audacity": {
        "en": "Free multitrack audio editor and recorder",
        "es": "Editor y grabador de audio multipista libre y gratuito",
        "de": "Freier Mehrspur-Audioeditor und -rekorder",
        "it": "Editor e registratore audio multitraccia libero e gratuito",
        "pt": "Editor e gravador de áudio multipista livre e gratuito",
    },
    "handbrake": {
        "en": "Powerful open-source video converter for all formats",
        "es": "Potente conversor de vídeo de código abierto para todos los formatos",
        "de": "Leistungsstarker Open-Source-Videokonverter für alle Formate",
        "it": "Potente convertitore video open-source per tutti i formati",
        "pt": "Conversor de vídeo de código aberto e poderoso para todos os formatos",
    },
    # ── Développement ──
    "vscode": {
        "en": "Modern extensible code editor developed by Microsoft",
        "es": "Moderno editor de código extensible desarrollado por Microsoft",
        "de": "Moderner erweiterbarer Code-Editor von Microsoft",
        "it": "Moderno editor di codice estensibile sviluppato da Microsoft",
        "pt": "Editor de código moderno e extensível desenvolvido pela Microsoft",
    },
    "git": {
        "en": "Essential distributed version control system",
        "es": "Sistema de control de versiones distribuido imprescindible",
        "de": "Unverzichtbares verteiltes Versionskontrollsystem",
        "it": "Sistema di controllo versione distribuito indispensabile",
        "pt": "Sistema de controle de versão distribuído indispensável",
    },
    "nodejs": {
        "en": "Server-side JavaScript runtime environment",
        "es": "Entorno de ejecución JavaScript del lado del servidor",
        "de": "Serverseitige JavaScript-Laufzeitumgebung",
        "it": "Ambiente di esecuzione JavaScript lato server",
        "pt": "Ambiente de execução JavaScript do lado do servidor",
    },
    "python": {
        "en": "Versatile and popular programming language",
        "es": "Lenguaje de programación versátil y popular",
        "de": "Vielseitige und beliebte Programmiersprache",
        "it": "Linguaggio di programmazione versatile e popolare",
        "pt": "Linguagem de programação versátil e popular",
    },
    "postman": {
        "en": "Complete tool to design, test and document REST APIs",
        "es": "Herramienta completa para diseñar, probar y documentar API REST",
        "de": "Komplettes Tool zum Entwerfen, Testen und Dokumentieren von REST-APIs",
        "it": "Strumento completo per progettare, testare e documentare API REST",
        "pt": "Ferramenta completa para criar, testar e documentar APIs REST",
    },
    "dbeaver": {
        "en": "Universal database manager (SQL, NoSQL)",
        "es": "Gestor universal de bases de datos (SQL, NoSQL)",
        "de": "Universeller Datenbankmanager (SQL, NoSQL)",
        "it": "Gestore universale di database (SQL, NoSQL)",
        "pt": "Gerenciador universal de bancos de dados (SQL, NoSQL)",
    },
    "sublimetext": {
        "en": "Ultra-fast text editor for code and prose",
        "es": "Editor de texto ultrarrápido para código y prosa",
        "de": "Ultraschneller Texteditor für Code und Prosa",
        "it": "Editor di testo velocissimo per codice e prosa",
        "pt": "Editor de texto ultrarrápido para código e prosa",
    },
    # ── Utilitaires & Sécurité ──
    "7zip": {
        "en": "High-compression archive extractor (ZIP, 7z, RAR, TAR)",
        "es": "Extractor de archivos de alta compresión (ZIP, 7z, RAR, TAR)",
        "de": "Archiventpacker mit hoher Kompression (ZIP, 7z, RAR, TAR)",
        "it": "Estrattore di archivi ad alta compressione (ZIP, 7z, RAR, TAR)",
        "pt": "Extrator de arquivos de alta compressão (ZIP, 7z, RAR, TAR)",
    },
    "notepadplusplus": {
        "en": "Lightweight text editor with syntax highlighting",
        "es": "Editor de texto ligero con resaltado de sintaxis",
        "de": "Leichter Texteditor mit Syntaxhervorhebung",
        "it": "Editor di testo leggero con evidenziazione della sintassi",
        "pt": "Editor de texto leve com destaque de sintaxe",
    },
    "powertoys": {
        "en": "Essential set of system utilities for Windows",
        "es": "Conjunto esencial de utilidades del sistema para Windows",
        "de": "Unverzichtbare Sammlung von Systemdienstprogrammen für Windows",
        "it": "Set essenziale di utilità di sistema per Windows",
        "pt": "Conjunto essencial de utilitários de sistema para Windows",
    },
    "bitwarden": {
        "en": "Secure open-source password manager",
        "es": "Gestor de contraseñas seguro y de código abierto",
        "de": "Sicherer Open-Source-Passwortmanager",
        "it": "Gestore di password sicuro e open-source",
        "pt": "Gerenciador de senhas seguro e de código aberto",
    },
    "keepassxc": {
        "en": "Secure offline password vault",
        "es": "Caja fuerte de contraseñas segura sin conexión",
        "de": "Sicherer Offline-Passworttresor",
        "it": "Cassaforte di password sicura offline",
        "pt": "Cofre de senhas seguro offline",
    },
    "qbittorrent": {
        "en": "Free, fast torrent client with no ads",
        "es": "Cliente torrent libre, rápido y sin publicidad",
        "de": "Freier, schneller Torrent-Client ohne Werbung",
        "it": "Client torrent libero, veloce e senza pubblicità",
        "pt": "Cliente torrent livre, rápido e sem anúncios",
    },
    "bleachbit": {
        "en": "Cleaner for temporary files and system cache",
        "es": "Limpiador de archivos temporales y caché del sistema",
        "de": "Reiniger für temporäre Dateien und System-Cache",
        "it": "Pulitore di file temporanei e cache di sistema",
        "pt": "Limpador de arquivos temporários e cache do sistema",
    },
    # ── Graphisme & Création ──
    "gimp": {
        "en": "Complete raster image editor and photo retouching",
        "es": "Completo editor de imágenes y retoque fotográfico",
        "de": "Vollständiger Rasterbildeditor und Fotoretusche",
        "it": "Editor di immagini raster e fotoritocco completo",
        "pt": "Editor de imagens e retoque fotográfico completo",
    },
    "inkscape": {
        "en": "Professional vector graphics editor (SVG)",
        "es": "Editor profesional de gráficos vectoriales (SVG)",
        "de": "Professioneller Vektorgrafikeditor (SVG)",
        "it": "Editor professionale di grafica vettoriale (SVG)",
        "pt": "Editor profissional de gráficos vetoriais (SVG)",
    },
    "blender": {
        "en": "Complete suite for 3D creation, animation, rendering and effects",
        "es": "Suite completa de creación 3D, animación, renderizado y efectos",
        "de": "Komplettsuite für 3D-Erstellung, Animation, Rendering und Effekte",
        "it": "Suite completa per creazione 3D, animazione, rendering ed effetti",
        "pt": "Suíte completa de criação 3D, animação, renderização e efeitos",
    },
    "krita": {
        "en": "Professional digital painting and illustration studio",
        "es": "Estudio profesional de pintura digital e ilustración",
        "de": "Professionelles Studio für digitale Malerei und Illustration",
        "it": "Studio professionale di pittura digitale e illustrazione",
        "pt": "Estúdio profissional de pintura digital e ilustração",
    },
    # ── Bureautique ──
    "libreoffice": {
        "en": "Complete office suite (Writer, Calc, Impress)",
        "es": "Suite ofimática completa (Writer, Calc, Impress)",
        "de": "Vollständige Bürosuite (Writer, Calc, Impress)",
        "it": "Suite per ufficio completa (Writer, Calc, Impress)",
        "pt": "Suíte de escritório completa (Writer, Calc, Impress)",
    },
    "obsidian": {
        "en": "Personal knowledge base and Markdown note-taking",
        "es": "Base de conocimiento personal y notas en Markdown",
        "de": "Persönliche Wissensdatenbank und Markdown-Notizen",
        "it": "Base di conoscenza personale e note Markdown",
        "pt": "Base de conhecimento pessoal e notas em Markdown",
    },
    "notion": {
        "en": "Connected workspace for notes, wikis and project management",
        "es": "Espacio de trabajo conectado para notas, wikis y gestión de proyectos",
        "de": "Vernetzter Arbeitsbereich für Notizen, Wikis und Projektmanagement",
        "it": "Spazio di lavoro connesso per note, wiki e gestione progetti",
        "pt": "Espaço de trabalho conectado para notas, wikis e gestão de projetos",
    },
}


def tr_desc(app_data: Dict) -> str:
    """Description de l'app dans la langue courante (repli : français)."""
    fallback = app_data.get("desc", "") or ""
    lang = get_language()
    if lang == "fr":
        return fallback
    return APP_DESCRIPTIONS.get(app_data.get("id", ""), {}).get(lang, fallback)
