# SystemMonitorX v1.0.0 - Distribution

## 📦 Was ist enthalten?

Diese Distribution enthält eine vollständig portable Version von SystemMonitorX:

- **SystemMonitorX.exe** (40MB) - Die Hauptanwendung
- **install.bat** - Installer-Script
- **uninstall.bat** - Uninstaller-Script
- **setup_autostart.bat** - Autostart-Setup
- **README.md** - Diese Dokumentation

## 🚀 Installation

### Option 1: Automatische Installation

1. Führen Sie `install.bat` als Administrator aus
2. SystemMonitorX wird in `%PROGRAMFILES%\SystemMonitorX` installiert
3. Desktop- und Startmenü-Verknüpfungen werden erstellt

### Option 2: Portable Nutzung

1. Kopieren Sie `SystemMonitorX.exe` in einen beliebigen Ordner
2. Starten Sie die .exe direkt - keine Installation erforderlich

## 🔧 Autostart einrichten

Führen Sie `setup_autostart.bat` aus, um SystemMonitorX beim Systemstart automatisch zu starten.

## 🗑️ Deinstallation

Führen Sie `uninstall.bat` als Administrator aus, um SystemMonitorX vollständig zu entfernen.

## ✨ Features

### 🖥️ System-Monitoring

- **CPU-Auslastung**: Echtzeit-Überwachung mit Frequenz-Anzeige
- **RAM-Verbrauch**: Arbeitsspeicher-Nutzung in GB und Prozent
- **Festplatten-Auslastung**: Speicherplatz-Überwachung
- **System-Informationen**: Plattform, Version, Architektur

### 🎨 Moderne GUI

- **CustomTkinter**: Moderne, ansprechende Benutzeroberfläche
- **Dark/Light Mode**: Vollständige Theme-Unterstützung
- **Transparenz-Effekte**: Glasmorphismus-Design
- **Consolas Font**: Professionelle Typografie

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

### 🔧 Konfiguration

- **JSON-basiert**: Vollständig konfigurierbar
- **Widget-Positionen**: Automatisch gespeichert
- **Theme-Einstellungen**: Persistent gespeichert
- **Export/Import**: Konfigurationen übertragbar

### 🎯 System-Tray

- **Tray-Integration**: Minimierung in System-Tray
- **Dynamische Icons**: CPU/RAM-Auslastung im Icon
- **Kontext-Menü**: Schnellzugriff auf Funktionen
- **Hintergrund-Betrieb**: Läuft im Hintergrund

## 🛠️ Systemanforderungen

- **Betriebssystem**: Windows 10/11 (64-bit)
- **RAM**: 100 MB verfügbar
- **Speicherplatz**: 50 MB
- **Python**: Nicht erforderlich (portable .exe)

## 📁 Verzeichnisstruktur

```
SystemMonitorX/
├── SystemMonitorX.exe          # Hauptanwendung
├── config/                     # Konfigurationsdateien
│   ├── app_config.json        # App-Einstellungen
│   └── widgets_config.json    # Widget-Konfiguration
├── logs/                      # Log-Dateien (wird erstellt)
├── assets/                    # Ressourcen (Icons, etc.)
└── README.md                  # Dokumentation
```

## 🔍 Erste Schritte

1. **Starten**: Doppelklick auf `SystemMonitorX.exe`
2. **Dashboard**: Systemdaten werden automatisch angezeigt
3. **Widgets**: Klicken Sie auf "CPU Widget" oder "RAM Widget"
4. **Logging**: Starten Sie das Logging für Verlaufsdaten
5. **Graphen**: Visualisieren Sie die gesammelten Daten

## ⚙️ Konfiguration

### Widget-Positionen

- Widgets werden automatisch an der letzten Position gespeichert
- Drag & Drop zum Verschieben
- Schließen-Button (×) zum Beenden

### Theme-Wechsel

- Klicken Sie auf "Theme wechseln" im Dashboard
- Dark/Light Mode wird persistent gespeichert
- Transparenz-Effekte passen sich automatisch an

### Logging-Einstellungen

- "Logging starten" beginnt die Datensammlung
- CSV und JSON werden automatisch erstellt
- "Graphen" zeigen die gesammelten Daten

## 🐛 Fehlerbehebung

### Anwendung startet nicht

- Führen Sie als Administrator aus
- Prüfen Sie Windows Defender/Antivirus
- Stellen Sie sicher, dass alle Dateien vorhanden sind

### Widgets werden nicht angezeigt

- Prüfen Sie die Konfigurationsdateien
- Starten Sie die Anwendung neu
- Löschen Sie die Widget-Konfiguration für Reset

### Logging funktioniert nicht

- Prüfen Sie Schreibrechte im logs/ Ordner
- Stellen Sie sicher, dass genügend Speicherplatz vorhanden ist
- Starten Sie das Logging neu

## 📞 Support

Bei Problemen oder Fragen:

1. Prüfen Sie die Log-Dateien im `logs/` Ordner
2. Starten Sie die Anwendung neu
3. Löschen Sie die Konfigurationsdateien für Reset

## 🎉 Changelog v1.0.0

### ✨ Neue Features

- Vollständige System-Monitoring-Integration
- Desktop-Widgets mit Drag & Drop
- Matplotlib-Graphen für Datenvisualisierung
- JSON-basierte Konfiguration
- System-Tray-Integration
- Dark/Light Mode mit Transparenz-Effekten

### 🔧 Verbesserungen

- Optimierte Performance
- Robuste Fehlerbehandlung
- Modulare Architektur
- Portable .exe-Distribution

---

**SystemMonitorX v1.0.0** - Ein modernes System-Monitoring-Tool mit Desktop-Widgets
