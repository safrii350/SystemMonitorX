"""
Tray-Manager für SystemMonitorX
"""

import pystray
from PIL import Image, ImageDraw
import threading
from typing import Callable, Optional
from assets.icons.tray_icon import create_detailed_tray_icon, create_simple_tray_icon

class TrayManager:
    """Verwaltet die System-Tray-Integration"""
    
    def __init__(self, show_callback: Callable, hide_callback: Callable, quit_callback: Callable):
        """Initialisiert den Tray-Manager"""
        self.show_callback = show_callback
        self.hide_callback = hide_callback
        self.quit_callback = quit_callback
        self.icon = None
        self.menu = None
        
    def create_icon(self) -> Image.Image:
        """Erstellt das Tray-Icon"""
        return create_simple_tray_icon()
        
    def create_menu(self) -> pystray.Menu:
        """Erstellt das Tray-Menü"""
        return pystray.Menu(
            pystray.MenuItem("SystemMonitorX", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Dashboard anzeigen", self._show_window),
            pystray.MenuItem("Dashboard verstecken", self._hide_window),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Beenden", self._quit_app)
        )
        
    def start(self):
        """Startet die Tray-Integration"""
        try:
            # Icon und Menü erstellen
            icon_image = self.create_icon()
            self.menu = self.create_menu()
            
            # Tray-Icon erstellen
            self.icon = pystray.Icon(
                "SystemMonitorX",
                icon_image,
                "SystemMonitorX",
                self.menu
            )
            
            # Icon im Hintergrund starten
            self.icon.run_detached()
            print("Tray-Integration gestartet")
            
        except Exception as e:
            print(f"Fehler beim Starten der Tray-Integration: {e}")
            
    def stop(self):
        """Stoppt die Tray-Integration"""
        try:
            if self.icon:
                self.icon.stop()
                print("Tray-Integration gestoppt")
        except Exception as e:
            print(f"Fehler beim Stoppen der Tray-Integration: {e}")
            
    def _show_window(self, icon, item):
        """Zeigt das Hauptfenster an"""
        try:
            self.show_callback()
        except Exception as e:
            print(f"Fehler beim Anzeigen des Fensters: {e}")
            
    def _hide_window(self, icon, item):
        """Versteckt das Hauptfenster"""
        try:
            self.hide_callback()
        except Exception as e:
            print(f"Fehler beim Verstecken des Fensters: {e}")
            
    def _quit_app(self, icon, item):
        """Beendet die Anwendung"""
        try:
            self.quit_callback()
        except Exception as e:
            print(f"Fehler beim Beenden der Anwendung: {e}")
            
    def update_icon(self, cpu_percent: float = None, memory_percent: float = None):
        """Aktualisiert das Tray-Icon basierend auf CPU und RAM-Auslastung"""
        try:
            if self.icon and (cpu_percent is not None or memory_percent is not None):
                # Icon mit aktuellen Systemdaten erstellen
                icon_image = create_detailed_tray_icon(
                    cpu_percent or 0, 
                    memory_percent or 0
                )
                self.icon.icon = icon_image
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Tray-Icons: {e}") 