# SystemMonitorX v1.0.0

Ein modernes System-Monitoring-Tool mit Desktop-Widgets, inspiriert von Rainmeter und BeWidgets.

## 🎨 Design-Features

### Farbpalette
- **Dark Mode**: `#141414` (Hintergrund), `#4a307d` (Accent), `#f2ecfa` (Text)
- **Light Mode**: `#ffffff` (Hintergrund), `#6c3dd9` (Accent), `#141414` (Text)

### Moderne UI-Elemente
- **Glasmorphismus-Effekte**: Transparente Karten mit Blur-Effekt
- **Gradient-Buttons**: Moderne Buttons mit deinen Farben
- **Progress-Bars**: Visuelle Darstellung der System-Auslastung
- **Emoji-Icons**: 🎨 🖥️ 💾 📊 📈 ⚙️ für bessere UX
- **Responsive Layout**: Anpassungsfähiges Grid-System

## ✨ Features

### 🖥️ System-Monitoring
- **CPU-Auslastung**: Echtzeit-Überwachung mit Frequenz-Anzeige
- **RAM-Verbrauch**: Arbeitsspeicher-Nutzung in GB und Prozent
- **Festplatten-Auslastung**: Speicherplatz-Überwachung
- **System-Informationen**: Plattform, Version, Architektur

### 📊 Desktop-Widgets
- **Unabhängige Widgets**: CPU, RAM, Disk als separate Fenster
- **Drag & Drop**: Widgets frei positionierbar
- **Transparente Overlays**: Immer im Vordergrund
- **Konfigurierbar**: Größe, Position, Transparenz

### 📈 Daten-Logging
- **CSV/JSON Export**: Automatische Datenspeicherung
- **Matplotlib-Graphen**: Interaktive Visualisierungen
- **Verlaufsdaten**: System-Performance über Zeit
- **Buffer-System**: Effiziente Speicherung

### 🎯 System-Tray
- **Tray-Integration**: Minimierung in System-Tray
- **Dynamische Icons**: CPU/RAM-Auslastung im Icon
- **Kontext-Menü**: Schnellzugriff auf Funktionen
- **Hintergrund-Betrieb**: Läuft im Hintergrund

### 🔧 Konfiguration
- **JSON-basiert**: Vollständig konfigurierbar
- **Widget-Positionen**: Automatisch gespeichert
- **Theme-Einstellungen**: Persistent gespeichert
- **Export/Import**: Konfigurationen übertragbar

## 🛠️ Technologie-Stack

- **Python 3.12+**: Core-Programmiersprache
- **CustomTkinter**: Moderne GUI-Bibliothek
- **psutil**: System-Monitoring
- **tkinter + overrideredirect**: Desktop-Widgets
- **threading**: Hintergrund-Updates
- **pyinstaller**: Portable .exe-Erstellung
- **pystray**: System-Tray-Integration
- **Pillow (PIL)**: Icon-Erstellung
- **matplotlib**: Datenvisualisierung
- **JSON/CSV**: Datenpersistierung

## 📁 Projektstruktur

```
SystemMonitorX/
├── main.py                     # Hauptanwendung
├── build_exe.py               # Build-Script
├── requirements.txt            # Python-Dependencies
├── README.md                  # Dokumentation
├── core/                      # Core-Module
│   ├── __init__.py
│   ├── app.py                 # Hauptanwendungsklasse
│   ├── system_monitor.py      # System-Monitoring
│   ├── widget_manager.py      # Widget-Verwaltung
│   ├── tray_manager.py        # System-Tray
│   ├── theme_manager.py       # Theme-Management
│   ├── data_logger.py         # Daten-Logging
│   ├── config_manager.py      # Konfiguration
│   ├── graph_viewer.py        # Graphen-Viewer
│   └── gui/                   # GUI-Module
│       ├── __init__.py
│       ├── dashboard.py       # Haupt-Dashboard
│       └── custom_widgets.py  # Custom-Widgets
├── widgets/                   # Desktop-Widgets
│   ├── __init__.py
│   └── desktop_widget.py      # Widget-Implementierung
├── assets/                    # Ressourcen
│   └── icons/
│       └── tray_icon.py       # Tray-Icon-Generator
├── config/                    # Konfiguration
│   ├── app_config.json        # App-Einstellungen
│   └── widgets_config.json    # Widget-Konfiguration
├── logs/                      # Log-Dateien (wird erstellt)
├── tests/                     # Tests (geplant)
└── docs/                      # Dokumentation (geplant)
```

## 🚀 Installation

### Option 1: Python-Entwicklungsumgebung
```bash
# Repository klonen
git clone https://github.com/your-username/SystemMonitorX.git
cd SystemMonitorX

# Dependencies installieren
pip install -r requirements.txt

# Anwendung starten
python main.py
```

### Option 2: Portable .exe
1. Download der neuesten Release
2. `SystemMonitorX.exe` ausführen
3. Keine Installation erforderlich

## 📖 Verwendung

### Dashboard
- **Systemdaten**: Automatische Anzeige von CPU, RAM, Disk
- **Theme-Wechsel**: Klick auf "🎨 Theme wechseln"
- **Progress-Bars**: Visuelle Darstellung der Auslastung

### Desktop-Widgets
- **Widget erstellen**: Klick auf "🖥️ CPU Widget" oder "💾 RAM Widget"
- **Positionieren**: Drag & Drop der Widgets
- **Schließen**: Klick auf "×" Button

### Daten-Logging
- **Logging starten**: Klick auf "▶️ Logging starten"
- **Graphen anzeigen**: Klick auf Graph-Buttons
- **Daten exportieren**: Automatisch in `logs/` Ordner

### System-Tray
- **Minimieren**: Klick auf "📌 Minimieren"
- **Tray-Icon**: Rechtsklick für Kontext-Menü
- **Wiederherstellen**: Über Tray-Icon

## 🔧 Konfiguration

### Theme-Einstellungen
```json
{
  "dark": {
    "background": "#141414",
    "accent": "#4a307d",
    "text": "#f2ecfa"
  },
  "light": {
    "background": "#ffffff",
    "accent": "#6c3dd9",
    "text": "#141414"
  }
}
```

### Widget-Konfiguration
```json
{
  "widgets": {
    "cpu": {
      "enabled": false,
      "position": "top_right",
      "size": "200x100",
      "transparency": 0.9
    }
  }
}
```

## 🐛 Fehlerbehebung

### Anwendung startet nicht
- Python 3.12+ installiert?
- Dependencies installiert? (`pip install -r requirements.txt`)
- Als Administrator ausführen

### Widgets werden nicht angezeigt
- Konfigurationsdateien prüfen
- Anwendung neu starten
- Widget-Konfiguration zurücksetzen

### Logging funktioniert nicht
- Schreibrechte im `logs/` Ordner prüfen
- Speicherplatz verfügbar?
- Logging neu starten

## 🤝 Beitragen

1. Fork das Repository
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## 📝 Changelog

### v1.0.0 (2024-07-31)
- ✨ **Erste Release**
- 🎨 Moderne CustomTkinter GUI mit Glasmorphismus
- 🖥️ Desktop-Widgets mit Drag & Drop
- 📊 System-Monitoring (CPU, RAM, Disk)
- 📈 Daten-Logging mit Matplotlib-Graphen
- 🎯 System-Tray-Integration
- ⚙️ JSON-basierte Konfiguration
- 🎨 Dark/Light Mode mit benutzerdefinierten Farben
- 📦 Portable .exe-Distribution
- 🔧 Modulare Architektur

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## 👥 Autoren

- **SystemMonitorX Team** - *Initiale Entwicklung*

## 🙏 Danksagungen

- **CustomTkinter** - Moderne GUI-Bibliothek
- **psutil** - System-Monitoring
- **matplotlib** - Datenvisualisierung
- **PyInstaller** - Portable Distribution

---

**SystemMonitorX v1.0.0** - Ein modernes System-Monitoring-Tool mit Desktop-Widgets 🚀
