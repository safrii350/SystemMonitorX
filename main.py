#!/usr/bin/env python3
"""
SystemMonitorX - Ein modernes System-Monitoring-Tool
Hauptanwendung mit CustomTkinter GUI und Desktop-Widgets
"""

import sys
import os
from pathlib import Path

# Projektpfade hinzufügen
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.app import SystemMonitorX

def main():
    """Hauptfunktion der Anwendung"""
    try:
        app = SystemMonitorX()
        app.run()
    except Exception as e:
        print(f"Fehler beim Starten der Anwendung: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 