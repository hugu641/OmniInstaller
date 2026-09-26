"""
Système multilingue d'OmniInstaller.

- 6 langues : Français, English, Español, Deutsch, Italiano, Português.
- Mémoire du choix via QSettings (registre Windows / .ini Linux) :
  la langue est demandée une seule fois au premier lancement.
- Les données du catalogue (noms, descriptions) restent en langue
  d'origine ; seule l'interface est traduite.

Utilisation :
    from src.i18n import tr, tr_category, get_language, set_language
    btn.setText(tr("install_n", n=3))
"""

from typing import Dict, Optional

# Code langue -> nom affiché (chaque langue dans sa propre langue)
LANGUAGES: Dict[str, str] = {
    "fr": "Français",
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
}

DEFAULT_LANG = "fr"
_SETTINGS_KEY = "language"

_current: str = DEFAULT_LANG


def _settings():
    """QSettings lazily (nécessite un QApplication existant)."""
    from PyQt6.QtCore import QSettings
    return QSettings("OmniInstaller", "OmniInstaller")


def detect_system_language() -> str:
    """Devine la langue depuis le système (pour présélectionner)."""
    try:
        from PyQt6.QtCore import QLocale
        code = QLocale.system().name().split("_")[0].lower()
        if code in LANGUAGES:
            return code
    except Exception:
        pass
    return DEFAULT_LANG


def get_saved_language() -> Optional[str]:
    """Langue mémorisée, ou None si premier lancement."""
    try:
        code = _settings().value(_SETTINGS_KEY, None)
        if code in LANGUAGES:
            return code
    except Exception:
        pass
    return None


def get_language() -> str:
    return _current


def set_language(code: str) -> str:
    """Mémorise la langue et l'active. Retourne le code effectif."""
    global _current
    if code not in LANGUAGES:
        code = DEFAULT_LANG
    _current = code
    try:
        _settings().setValue(_SETTINGS_KEY, code)
    except Exception:
        pass
    return _current


def init_language() -> str:
    """Charge la langue mémorisée (ou défaut). À appeler après QApplication."""
    global _current
    saved = get_saved_language()
    _current = saved if saved else DEFAULT_LANG
    return _current


def tr(key: str, **kwargs) -> str:
    """Traduit une clé dans la langue courante (repli : français, puis clé)."""
    lang = _current if _current in STRINGS else DEFAULT_LANG
    text = STRINGS.get(lang, {}).get(key)
    if text is None:
        text = STRINGS[DEFAULT_LANG].get(key, key)
    try:
        return text.format(**kwargs) if kwargs else text
    except Exception:
        return text


# ──────────────────────────────────────────────
# Noms de catégories (clés internes = français)
# ──────────────────────────────────────────────

CATEGORY_NAMES: Dict[str, Dict[str, str]] = {
    "Navigateurs": {
        "fr": "Navigateurs", "en": "Browsers", "es": "Navegadores",
        "de": "Browser", "it": "Browser", "pt": "Navegadores",
    },
    "Communication": {
        "fr": "Communication", "en": "Communication", "es": "Comunicación",
        "de": "Kommunikation", "it": "Comunicazione", "pt": "Comunicação",
    },
    "Gaming": {
        "fr": "Gaming", "en": "Gaming", "es": "Juegos",
        "de": "Spiele", "it": "Giochi", "pt": "Jogos",
    },
    "Musique & Médias": {
        "fr": "Musique & Médias", "en": "Music & Media", "es": "Música y medios",
        "de": "Musik & Medien", "it": "Musica e media", "pt": "Música e mídia",
    },
    "Développement": {
        "fr": "Développement", "en": "Development", "es": "Desarrollo",
        "de": "Entwicklung", "it": "Sviluppo", "pt": "Desenvolvimento",
    },
    "Utilitaires & Sécurité": {
        "fr": "Utilitaires & Sécurité", "en": "Utilities & Security",
        "es": "Utilidades y seguridad", "de": "Dienstprogramme & Sicherheit",
        "it": "Utilità e sicurezza", "pt": "Utilitários e segurança",
    },
    "Graphisme & Création": {
        "fr": "Graphisme & Création", "en": "Graphics & Design",
        "es": "Gráficos y creación", "de": "Grafik & Design",
        "it": "Grafica e creazione", "pt": "Gráficos e criação",
    },
    "Bureautique": {
        "fr": "Bureautique", "en": "Office", "es": "Ofimática",
        "de": "Büro", "it": "Ufficio", "pt": "Escritório",
    },
}


def tr_category(fr_name: str) -> str:
    """Nom de catégorie traduit (repli : nom français d'origine)."""
    lang = _current if _current in LANGUAGES else DEFAULT_LANG
    return CATEGORY_NAMES.get(fr_name, {}).get(lang, fr_name)


# ──────────────────────────────────────────────
# Tables de traduction de l'interface
# ──────────────────────────────────────────────

STRINGS: Dict[str, Dict[str, str]] = {
    # ════════════ FRANÇAIS ════════════
    "fr": {
        "brand_subtitle": "Gestionnaire d'applications",
        "nav_section": "NAVIGATION",
        "nav_recommended": "Recommandées",
        "nav_all": "Toutes les applications",
        "nav_selected": "Sélectionnées ({n})",
        "cat_section": "CATÉGORIES",
        "add_app": "Ajouter une application",
        "page_title": "Catalogue",
        "page_subtitle": "Parcourez, sélectionnez puis installez vos applications en un clic.",
        "search_placeholder": "Rechercher une application…  (nom, catégorie, identifiant)",
        "select_all": "Tout sélectionner",
        "clear": "Effacer",
        "recommended": "Recommandées",
        "results_vs": "{v} application(s)  ·  {s} sélectionnée(s)",
        "empty_title": "Aucune application trouvée",
        "empty_desc": "Essayez un autre terme ou ajoutez une application manuellement.",
        "dock_ready": "Prêt à installer",
        "dock_none": "Aucune application sélectionnée",
        "dock_one": "1 application sélectionnée",
        "dock_many": "{n} applications sélectionnées",
        "console": "Console",
        "hide_console": "Masquer la console",
        "stop": "Arrêter",
        "install_n": "Installer ({n})",
        "installing_ct": "Installation en cours… ({c}/{t})",
        "installing_name": "Installation : {name}",
        "stopping": "Arrêt en cours…",
        "backend_missing": "ABSENT",
        "no_selection_t": "Aucune sélection",
        "no_selection_m": "Sélectionnez au moins une application.",
        "confirm_t": "Confirmer",
        "confirm_m": "Interrompre l'installation en cours ?",
        "done_ok_t": "Terminé",
        "done_ok_m": "{ok} application(s) installée(s) avec succès.",
        "done_err_t": "Terminé avec erreurs",
        "done_err_m": "{ok} réussie(s), {fail} échec(s).\nConsultez la console pour les détails.",
        "done_dock_ok": "{ok}/{t} installations réussies en {d}s",
        "done_dock_err": "{ok} réussie(s), {fail} échec(s)",
        "app_added_t": "Application ajoutée",
        "app_added_m": "'{name}' a été ajoutée à la liste.",
        "settings": "Paramètres",
        "settings_title": "Paramètres",
        "language": "Langue",
        "language_hint": "La langue est appliquée immédiatement.",
        "save": "Enregistrer",
        "cancel": "Annuler",
        "card_install": "Installer",
        "card_selected": "✓ Sélectionné",
        "card_installed": "✓ Installé",
        "card_recommended": "★ Recommandé",
        "store_title": "Explorer le Store & Ajouter des Applications",
        "tab_online": "Recherche en ligne ({source})",
        "tab_manual": "Ajout manuel par ID",
        "close": "Fermer",
        "add": "Ajouter",
        "search_ph": "Ex: blender, vlc, discord, steam, code, obsidian...",
        "search_btn": "Rechercher",
        "status_hint": "Entrez un nom ou mot-clé pour lancer la recherche en direct.",
        "searching": "Recherche de '{q}' en cours...",
        "no_result": "Aucun résultat trouvé.",
        "results_found": "{n} résultat(s) trouvé(s) :",
        "search_error": "Erreur : {err}",
        "manual_info": (
            "Ajoutez n'importe quel paquet en spécifiant son identifiant officiel :\n"
            "• Windows : ID Winget officiel (ex: 'Valve.Steam', '7zip.7zip', 'Spotify.Spotify')\n"
            "• Linux : ID Flatpak ou nom APT (ex: 'org.videolan.VLC', 'com.brave.Browser')"
        ),
        "f_name": "Nom affiché de l'application :",
        "f_name_ph": "Ex: Steam, Blender, Docker Desktop...",
        "f_id": "Identifiant du paquet (Winget / Flatpak) :",
        "f_id_ph": "Ex: Valve.Steam ou org.videolan.VLC",
        "f_cat": "Catégorie :",
        "f_desc": "Description courte (optionnel) :",
        "f_desc_ph": "Ex: Plateforme de jeux vidéo",
        "add_catalog_btn": "Ajouter cette application au catalogue",
        "required_t": "Champs requis",
        "required_m": "Veuillez renseigner le nom et l'identifiant du paquet.",
        "added_t": "Application Ajoutée",
        "added_m": "L'application '{name}' a été ajoutée avec succès à votre catalogue !",
        "pkg_word": "Paquet {pkg}",
        "custom_cat": "Personnalisé",
        "lang_title": "Bienvenue sur OmniInstaller",
        "lang_subtitle": "Choisissez votre langue / Choose your language",
        "lang_continue": "Continuer",
    },
    # ════════════ ENGLISH ════════════
    "en": {
        "brand_subtitle": "Application manager",
        "nav_section": "NAVIGATION",
        "nav_recommended": "Recommended",
        "nav_all": "All applications",
        "nav_selected": "Selected ({n})",
        "cat_section": "CATEGORIES",
        "add_app": "Add an application",
        "page_title": "Catalog",
        "page_subtitle": "Browse, select and install your apps in one click.",
        "search_placeholder": "Search for an application…  (name, category, ID)",
        "select_all": "Select all",
        "clear": "Clear",
        "recommended": "Recommended",
        "results_vs": "{v} app(s)  ·  {s} selected",
        "empty_title": "No application found",
        "empty_desc": "Try another term or add an application manually.",
        "dock_ready": "Ready to install",
        "dock_none": "No application selected",
        "dock_one": "1 application selected",
        "dock_many": "{n} applications selected",
        "console": "Console",
        "hide_console": "Hide console",
        "stop": "Stop",
        "install_n": "Install ({n})",
        "installing_ct": "Installing… ({c}/{t})",
        "installing_name": "Installing: {name}",
        "stopping": "Stopping…",
        "backend_missing": "MISSING",
        "no_selection_t": "No selection",
        "no_selection_m": "Please select at least one application.",
        "confirm_t": "Confirm",
        "confirm_m": "Interrupt the ongoing installation?",
        "done_ok_t": "Done",
        "done_ok_m": "{ok} application(s) installed successfully.",
        "done_err_t": "Completed with errors",
        "done_err_m": "{ok} succeeded, {fail} failed.\nSee the console for details.",
        "done_dock_ok": "{ok}/{t} installations completed in {d}s",
        "done_dock_err": "{ok} succeeded, {fail} failed",
        "app_added_t": "Application added",
        "app_added_m": "'{name}' has been added to the list.",
        "settings": "Settings",
        "settings_title": "Settings",
        "language": "Language",
        "language_hint": "The language is applied immediately.",
        "save": "Save",
        "cancel": "Cancel",
        "card_install": "Install",
        "card_selected": "✓ Selected",
        "card_installed": "✓ Installed",
        "card_recommended": "★ Recommended",
        "store_title": "Browse the Store & Add Applications",
        "tab_online": "Online search ({source})",
        "tab_manual": "Manual add by ID",
        "close": "Close",
        "add": "Add",
        "search_ph": "E.g.: blender, vlc, discord, steam, code, obsidian...",
        "search_btn": "Search",
        "status_hint": "Enter a name or keyword to start the live search.",
        "searching": "Searching for '{q}'...",
        "no_result": "No results found.",
        "results_found": "{n} result(s) found:",
        "search_error": "Error: {err}",
        "manual_info": (
            "Add any package by providing its official identifier:\n"
            "• Windows: official Winget ID (e.g. 'Valve.Steam', '7zip.7zip', 'Spotify.Spotify')\n"
            "• Linux: Flatpak ID or APT name (e.g. 'org.videolan.VLC', 'com.brave.Browser')"
        ),
        "f_name": "Application display name:",
        "f_name_ph": "E.g.: Steam, Blender, Docker Desktop...",
        "f_id": "Package ID (Winget / Flatpak):",
        "f_id_ph": "E.g.: Valve.Steam or org.videolan.VLC",
        "f_cat": "Category:",
        "f_desc": "Short description (optional):",
        "f_desc_ph": "E.g.: Video game platform",
        "add_catalog_btn": "Add this application to the catalog",
        "required_t": "Required fields",
        "required_m": "Please fill in the name and package ID.",
        "added_t": "Application Added",
        "added_m": "'{name}' has been successfully added to your catalog!",
        "pkg_word": "Package {pkg}",
        "custom_cat": "Custom",
        "lang_title": "Welcome to OmniInstaller",
        "lang_subtitle": "Choose your language / Choisissez votre langue",
        "lang_continue": "Continue",
    },
    # ════════════ ESPAÑOL ════════════
    "es": {
        "brand_subtitle": "Gestor de aplicaciones",
        "nav_section": "NAVEGACIÓN",
        "nav_recommended": "Recomendadas",
        "nav_all": "Todas las aplicaciones",
        "nav_selected": "Seleccionadas ({n})",
        "cat_section": "CATEGORÍAS",
        "add_app": "Añadir una aplicación",
        "page_title": "Catálogo",
        "page_subtitle": "Explora, selecciona e instala tus aplicaciones en un clic.",
        "search_placeholder": "Buscar una aplicación…  (nombre, categoría, ID)",
        "select_all": "Seleccionar todo",
        "clear": "Borrar",
        "recommended": "Recomendadas",
        "results_vs": "{v} aplicación(es)  ·  {s} seleccionada(s)",
        "empty_title": "Ninguna aplicación encontrada",
        "empty_desc": "Prueba con otro término o añade una aplicación manualmente.",
        "dock_ready": "Listo para instalar",
        "dock_none": "Ninguna aplicación seleccionada",
        "dock_one": "1 aplicación seleccionada",
        "dock_many": "{n} aplicaciones seleccionadas",
        "console": "Consola",
        "hide_console": "Ocultar la consola",
        "stop": "Detener",
        "install_n": "Instalar ({n})",
        "installing_ct": "Instalando… ({c}/{t})",
        "installing_name": "Instalando: {name}",
        "stopping": "Deteniendo…",
        "backend_missing": "AUSENTE",
        "no_selection_t": "Sin selección",
        "no_selection_m": "Selecciona al menos una aplicación.",
        "confirm_t": "Confirmar",
        "confirm_m": "¿Interrumpir la instalación en curso?",
        "done_ok_t": "Terminado",
        "done_ok_m": "{ok} aplicación(es) instalada(s) con éxito.",
        "done_err_t": "Terminado con errores",
        "done_err_m": "{ok} correctas, {fail} fallidas.\nConsulta la consola para más detalles.",
        "done_dock_ok": "{ok}/{t} instalaciones correctas en {d}s",
        "done_dock_err": "{ok} correctas, {fail} fallidas",
        "app_added_t": "Aplicación añadida",
        "app_added_m": "'{name}' se ha añadido a la lista.",
        "settings": "Ajustes",
        "settings_title": "Ajustes",
        "language": "Idioma",
        "language_hint": "El idioma se aplica inmediatamente.",
        "save": "Guardar",
        "cancel": "Cancelar",
        "card_install": "Instalar",
        "card_selected": "✓ Seleccionada",
        "card_installed": "✓ Instalada",
        "card_recommended": "★ Recomendada",
        "store_title": "Explorar la tienda y añadir aplicaciones",
        "tab_online": "Búsqueda en línea ({source})",
        "tab_manual": "Añadir manualmente por ID",
        "close": "Cerrar",
        "add": "Añadir",
        "search_ph": "Ej.: blender, vlc, discord, steam, code, obsidian...",
        "search_btn": "Buscar",
        "status_hint": "Escribe un nombre o palabra clave para iniciar la búsqueda en directo.",
        "searching": "Buscando '{q}'...",
        "no_result": "Sin resultados.",
        "results_found": "{n} resultado(s) encontrado(s):",
        "search_error": "Error: {err}",
        "manual_info": (
            "Añade cualquier paquete con su identificador oficial:\n"
            "• Windows: ID oficial de Winget (ej.: 'Valve.Steam', '7zip.7zip', 'Spotify.Spotify')\n"
            "• Linux: ID de Flatpak o nombre APT (ej.: 'org.videolan.VLC', 'com.brave.Browser')"
        ),
        "f_name": "Nombre visible de la aplicación:",
        "f_name_ph": "Ej.: Steam, Blender, Docker Desktop...",
        "f_id": "Identificador del paquete (Winget / Flatpak):",
        "f_id_ph": "Ej.: Valve.Steam o org.videolan.VLC",
        "f_cat": "Categoría:",
        "f_desc": "Descripción breve (opcional):",
        "f_desc_ph": "Ej.: Plataforma de videojuegos",
        "add_catalog_btn": "Añadir esta aplicación al catálogo",
        "required_t": "Campos obligatorios",
        "required_m": "Completa el nombre y el identificador del paquete.",
        "added_t": "Aplicación añadida",
        "added_m": "¡'{name}' se ha añadido correctamente a tu catálogo!",
        "pkg_word": "Paquete {pkg}",
        "custom_cat": "Personalizado",
        "lang_title": "Bienvenido a OmniInstaller",
        "lang_subtitle": "Elige tu idioma / Choose your language",
        "lang_continue": "Continuar",
    },
    # ════════════ DEUTSCH ════════════
    "de": {
        "brand_subtitle": "Anwendungsverwaltung",
        "nav_section": "NAVIGATION",
        "nav_recommended": "Empfohlen",
        "nav_all": "Alle Anwendungen",
        "nav_selected": "Ausgewählt ({n})",
        "cat_section": "KATEGORIEN",
        "add_app": "Anwendung hinzufügen",
        "page_title": "Katalog",
        "page_subtitle": "Durchsuchen, auswählen und mit einem Klick installieren.",
        "search_placeholder": "Anwendung suchen…  (Name, Kategorie, ID)",
        "select_all": "Alle auswählen",
        "clear": "Zurücksetzen",
        "recommended": "Empfohlen",
        "results_vs": "{v} App(s)  ·  {s} ausgewählt",
        "empty_title": "Keine Anwendung gefunden",
        "empty_desc": "Versuche einen anderen Begriff oder füge eine Anwendung manuell hinzu.",
        "dock_ready": "Bereit zur Installation",
        "dock_none": "Keine Anwendung ausgewählt",
        "dock_one": "1 Anwendung ausgewählt",
        "dock_many": "{n} Anwendungen ausgewählt",
        "console": "Konsole",
        "hide_console": "Konsole ausblenden",
        "stop": "Stoppen",
        "install_n": "Installieren ({n})",
        "installing_ct": "Installation läuft… ({c}/{t})",
        "installing_name": "Installiert: {name}",
        "stopping": "Wird gestoppt…",
        "backend_missing": "FEHLT",
        "no_selection_t": "Keine Auswahl",
        "no_selection_m": "Bitte wähle mindestens eine Anwendung aus.",
        "confirm_t": "Bestätigen",
        "confirm_m": "Die laufende Installation abbrechen?",
        "done_ok_t": "Fertig",
        "done_ok_m": "{ok} Anwendung(en) erfolgreich installiert.",
        "done_err_t": "Mit Fehlern abgeschlossen",
        "done_err_m": "{ok} erfolgreich, {fail} fehlgeschlagen.\nDetails findest du in der Konsole.",
        "done_dock_ok": "{ok}/{t} Installationen erfolgreich in {d}s",
        "done_dock_err": "{ok} erfolgreich, {fail} fehlgeschlagen",
        "app_added_t": "Anwendung hinzugefügt",
        "app_added_m": "'{name}' wurde zur Liste hinzugefügt.",
        "settings": "Einstellungen",
        "settings_title": "Einstellungen",
        "language": "Sprache",
        "language_hint": "Die Sprache wird sofort angewendet.",
        "save": "Speichern",
        "cancel": "Abbrechen",
        "card_install": "Installieren",
        "card_selected": "✓ Ausgewählt",
        "card_installed": "✓ Installiert",
        "card_recommended": "★ Empfohlen",
        "store_title": "Store durchsuchen & Anwendungen hinzufügen",
        "tab_online": "Online-Suche ({source})",
        "tab_manual": "Manuell per ID hinzufügen",
        "close": "Schließen",
        "add": "Hinzufügen",
        "search_ph": "Z. B.: blender, vlc, discord, steam, code, obsidian...",
        "search_btn": "Suchen",
        "status_hint": "Name oder Stichwort eingeben, um die Live-Suche zu starten.",
        "searching": "Suche nach '{q}' läuft...",
        "no_result": "Keine Ergebnisse gefunden.",
        "results_found": "{n} Ergebnis(se) gefunden:",
        "search_error": "Fehler: {err}",
        "manual_info": (
            "Füge ein beliebiges Paket über seine offizielle Kennung hinzu:\n"
            "• Windows: offizielle Winget-ID (z. B. 'Valve.Steam', '7zip.7zip', 'Spotify.Spotify')\n"
            "• Linux: Flatpak-ID oder APT-Name (z. B. 'org.videolan.VLC', 'com.brave.Browser')"
        ),
        "f_name": "Anzeigename der Anwendung:",
        "f_name_ph": "Z. B.: Steam, Blender, Docker Desktop...",
        "f_id": "Paket-ID (Winget / Flatpak):",
        "f_id_ph": "Z. B.: Valve.Steam oder org.videolan.VLC",
        "f_cat": "Kategorie:",
        "f_desc": "Kurzbeschreibung (optional):",
        "f_desc_ph": "Z. B.: Videospiel-Plattform",
        "add_catalog_btn": "Diese Anwendung zum Katalog hinzufügen",
        "required_t": "Pflichtfelder",
        "required_m": "Bitte Name und Paket-ID ausfüllen.",
        "added_t": "Anwendung hinzugefügt",
        "added_m": "'{name}' wurde erfolgreich zu deinem Katalog hinzugefügt!",
        "pkg_word": "Paket {pkg}",
        "custom_cat": "Benutzerdefiniert",
        "lang_title": "Willkommen bei OmniInstaller",
        "lang_subtitle": "Wähle deine Sprache / Choose your language",
        "lang_continue": "Weiter",
    },
    # ════════════ ITALIANO ════════════
    "it": {
        "brand_subtitle": "Gestore di applicazioni",
        "nav_section": "NAVIGAZIONE",
        "nav_recommended": "Consigliate",
        "nav_all": "Tutte le applicazioni",
        "nav_selected": "Selezionate ({n})",
        "cat_section": "CATEGORIE",
        "add_app": "Aggiungi un'applicazione",
        "page_title": "Catalogo",
        "page_subtitle": "Sfoglia, seleziona e installa le tue app con un clic.",
        "search_placeholder": "Cerca un'applicazione…  (nome, categoria, ID)",
        "select_all": "Seleziona tutto",
        "clear": "Cancella",
        "recommended": "Consigliate",
        "results_vs": "{v} app  ·  {s} selezionate",
        "empty_title": "Nessuna applicazione trovata",
        "empty_desc": "Prova un altro termine o aggiungi un'applicazione manualmente.",
        "dock_ready": "Pronto per l'installazione",
        "dock_none": "Nessuna applicazione selezionata",
        "dock_one": "1 applicazione selezionata",
        "dock_many": "{n} applicazioni selezionate",
        "console": "Console",
        "hide_console": "Nascondi console",
        "stop": "Interrompi",
        "install_n": "Installa ({n})",
        "installing_ct": "Installazione in corso… ({c}/{t})",
        "installing_name": "Installazione: {name}",
        "stopping": "Interruzione in corso…",
        "backend_missing": "MANCANTE",
        "no_selection_t": "Nessuna selezione",
        "no_selection_m": "Seleziona almeno un'applicazione.",
        "confirm_t": "Conferma",
        "confirm_m": "Interrompere l'installazione in corso?",
        "done_ok_t": "Completato",
        "done_ok_m": "{ok} app installate con successo.",
        "done_err_t": "Completato con errori",
        "done_err_m": "{ok} riuscite, {fail} fallite.\nConsulta la console per i dettagli.",
        "done_dock_ok": "{ok}/{t} installazioni riuscite in {d}s",
        "done_dock_err": "{ok} riuscite, {fail} fallite",
        "app_added_t": "Applicazione aggiunta",
        "app_added_m": "'{name}' è stata aggiunta all'elenco.",
        "settings": "Impostazioni",
        "settings_title": "Impostazioni",
        "language": "Lingua",
        "language_hint": "La lingua viene applicata immediatamente.",
        "save": "Salva",
        "cancel": "Annulla",
        "card_install": "Installa",
        "card_selected": "✓ Selezionata",
        "card_installed": "✓ Installata",
        "card_recommended": "★ Consigliata",
        "store_title": "Esplora lo Store e aggiungi applicazioni",
        "tab_online": "Ricerca online ({source})",
        "tab_manual": "Aggiunta manuale per ID",
        "close": "Chiudi",
        "add": "Aggiungi",
        "search_ph": "Es.: blender, vlc, discord, steam, code, obsidian...",
        "search_btn": "Cerca",
        "status_hint": "Inserisci un nome o una parola chiave per avviare la ricerca live.",
        "searching": "Ricerca di '{q}' in corso...",
        "no_result": "Nessun risultato trovato.",
        "results_found": "{n} risultato(i) trovato(i):",
        "search_error": "Errore: {err}",
        "manual_info": (
            "Aggiungi qualsiasi pacchetto con il suo identificativo ufficiale:\n"
            "• Windows: ID Winget ufficiale (es. 'Valve.Steam', '7zip.7zip', 'Spotify.Spotify')\n"
            "• Linux: ID Flatpak o nome APT (es. 'org.videolan.VLC', 'com.brave.Browser')"
        ),
        "f_name": "Nome visualizzato dell'applicazione:",
        "f_name_ph": "Es.: Steam, Blender, Docker Desktop...",
        "f_id": "Identificativo del pacchetto (Winget / Flatpak):",
        "f_id_ph": "Es.: Valve.Steam o org.videolan.VLC",
        "f_cat": "Categoria:",
        "f_desc": "Breve descrizione (facoltativo):",
        "f_desc_ph": "Es.: Piattaforma di videogiochi",
        "add_catalog_btn": "Aggiungi questa applicazione al catalogo",
        "required_t": "Campi obbligatori",
        "required_m": "Inserisci il nome e l'identificativo del pacchetto.",
        "added_t": "Applicazione aggiunta",
        "added_m": "'{name}' è stata aggiunta con successo al tuo catalogo!",
        "pkg_word": "Pacchetto {pkg}",
        "custom_cat": "Personalizzato",
        "lang_title": "Benvenuto in OmniInstaller",
        "lang_subtitle": "Scegli la tua lingua / Choose your language",
        "lang_continue": "Continua",
    },
    # ════════════ PORTUGUÊS ════════════
    "pt": {
        "brand_subtitle": "Gestor de aplicações",
        "nav_section": "NAVEGAÇÃO",
        "nav_recommended": "Recomendados",
        "nav_all": "Todos os aplicativos",
        "nav_selected": "Selecionados ({n})",
        "cat_section": "CATEGORIAS",
        "add_app": "Adicionar um aplicativo",
        "page_title": "Catálogo",
        "page_subtitle": "Navegue, selecione e instale seus apps em um clique.",
        "search_placeholder": "Pesquisar um aplicativo…  (nome, categoria, ID)",
        "select_all": "Selecionar tudo",
        "clear": "Limpar",
        "recommended": "Recomendados",
        "results_vs": "{v} aplicativo(s)  ·  {s} selecionado(s)",
        "empty_title": "Nenhum aplicativo encontrado",
        "empty_desc": "Tente outro termo ou adicione um aplicativo manualmente.",
        "dock_ready": "Pronto para instalar",
        "dock_none": "Nenhum aplicativo selecionado",
        "dock_one": "1 aplicativo selecionado",
        "dock_many": "{n} aplicativos selecionados",
        "console": "Console",
        "hide_console": "Ocultar console",
        "stop": "Parar",
        "install_n": "Instalar ({n})",
        "installing_ct": "Instalando… ({c}/{t})",
        "installing_name": "Instalando: {name}",
        "stopping": "Parando…",
        "backend_missing": "AUSENTE",
        "no_selection_t": "Sem seleção",
        "no_selection_m": "Selecione pelo menos um aplicativo.",
        "confirm_t": "Confirmar",
        "confirm_m": "Interromper a instalação em curso?",
        "done_ok_t": "Concluído",
        "done_ok_m": "{ok} aplicativo(s) instalado(s) com sucesso.",
        "done_err_t": "Concluído com erros",
        "done_err_m": "{ok} com êxito, {fail} com falha.\nConsulte o console para detalhes.",
        "done_dock_ok": "{ok}/{t} instalações concluídas em {d}s",
        "done_dock_err": "{ok} com êxito, {fail} com falha",
        "app_added_t": "Aplicativo adicionado",
        "app_added_m": "'{name}' foi adicionado à lista.",
        "settings": "Configurações",
        "settings_title": "Configurações",
        "language": "Idioma",
        "language_hint": "O idioma é aplicado imediatamente.",
        "save": "Salvar",
        "cancel": "Cancelar",
        "card_install": "Instalar",
        "card_selected": "✓ Selecionado",
        "card_installed": "✓ Instalado",
        "card_recommended": "★ Recomendado",
        "store_title": "Explorar a loja e adicionar aplicativos",
        "tab_online": "Pesquisa online ({source})",
        "tab_manual": "Adição manual por ID",
        "close": "Fechar",
        "add": "Adicionar",
        "search_ph": "Ex.: blender, vlc, discord, steam, code, obsidian...",
        "search_btn": "Pesquisar",
        "status_hint": "Digite um nome ou palavra-chave para iniciar a pesquisa ao vivo.",
        "searching": "Pesquisando '{q}'...",
        "no_result": "Nenhum resultado encontrado.",
        "results_found": "{n} resultado(s) encontrado(s):",
        "search_error": "Erro: {err}",
        "manual_info": (
            "Adicione qualquer pacote com seu identificador oficial:\n"
            "• Windows: ID oficial do Winget (ex.: 'Valve.Steam', '7zip.7zip', 'Spotify.Spotify')\n"
            "• Linux: ID Flatpak ou nome APT (ex.: 'org.videolan.VLC', 'com.brave.Browser')"
        ),
        "f_name": "Nome de exibição do aplicativo:",
        "f_name_ph": "Ex.: Steam, Blender, Docker Desktop...",
        "f_id": "Identificador do pacote (Winget / Flatpak):",
        "f_id_ph": "Ex.: Valve.Steam ou org.videolan.VLC",
        "f_cat": "Categoria:",
        "f_desc": "Descrição curta (opcional):",
        "f_desc_ph": "Ex.: Plataforma de jogos",
        "add_catalog_btn": "Adicionar este aplicativo ao catálogo",
        "required_t": "Campos obrigatórios",
        "required_m": "Preencha o nome e o identificador do pacote.",
        "added_t": "Aplicativo adicionado",
        "added_m": "'{name}' foi adicionado ao seu catálogo com sucesso!",
        "pkg_word": "Pacote {pkg}",
        "custom_cat": "Personalizado",
        "lang_title": "Bem-vindo ao OmniInstaller",
        "lang_subtitle": "Escolha seu idioma / Choose your language",
        "lang_continue": "Continuar",
    },
}
