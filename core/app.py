"""
Hauptanwendungsklasse für SystemMonitorX
"""

import customtkinter as ctk
from .system_monitor import SystemMonitor
from .gui.dashboard import Dashboard
from .widget_manager import WidgetManager
from .tray_manager import TrayManager
from .theme_manager import ThemeManager
from .data_logger import DataLogger
from .config_manager import ConfigManager

class SystemMonitorX:
    """Hauptklasse der SystemMonitorX Anwendung"""
    
    def __init__(self):
        """Initialisiert die Anwendung"""
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager()
        self.system_monitor = SystemMonitor()
        self.widget_manager = WidgetManager(self.config_manager, self.theme_manager)
        self.data_logger = DataLogger()
        self.tray_manager = None
        self.dashboard = None
        self.root = None
        
    def run(self):
        """Startet die Anwendung"""
        # Konfiguration laden
        theme = self.config_manager.get_config("app.theme") or "dark"
        window_size = self.config_manager.get_config("app.window_size") or "900x700"
        transparency = self.config_manager.get_config("app.transparency") or 0.9
        
        # Theme-Manager konfigurieren
        self.theme_manager.set_theme(theme)
        
        # CustomTkinter konfigurieren
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")
        
        # Hauptfenster erstellen
        self.root = ctk.CTk()
        self.root.title("SystemMonitorX")
        self.root.geometry(window_size)
        self.root.resizable(True, True)
        
        # Fenster-Transparenz anwenden
        self.root.attributes('-alpha', transparency)
        
        # Tray-Integration starten
        self._setup_tray()
        
        # Dashboard erstellen
        self.dashboard = Dashboard(self.root, self.system_monitor, self.widget_manager, self.tray_manager, self.theme_manager, self.data_logger, self.config_manager)
        
        # Fenster-Schließen-Event behandeln
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Anwendung starten
        self.root.mainloop()
        
    def cleanup(self):
        """Bereinigt Ressourcen beim Beenden"""
        if self.widget_manager:
            self.widget_manager.stop_all_widgets()
        if self.system_monitor:
            self.system_monitor.stop()
        if self.tray_manager:
            self.tray_manager.stop()
        if self.data_logger:
            self.data_logger.stop_logging()
            
    def _setup_tray(self):
        """Richtet die Tray-Integration ein"""
        try:
            self.tray_manager = TrayManager(
                show_callback=self._show_window,
                hide_callback=self._hide_window,
                quit_callback=self._quit_app
            )
            self.tray_manager.start()
        except Exception as e:
            print(f"Fehler beim Einrichten der Tray-Integration: {e}")
            
    def _show_window(self):
        """Zeigt das Hauptfenster an"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
    def _hide_window(self):
        """Versteckt das Hauptfenster"""
        if self.root:
            self.root.withdraw()
            
    def _on_closing(self):
        """Behandelt das Schließen des Hauptfensters"""
        # Fenster verstecken statt beenden
        self._hide_window()
        
    def _quit_app(self):
        """Beendet die Anwendung vollständig"""
        try:
            self.cleanup()
            if self.root:
                self.root.quit()
        except Exception as e:
            print(f"Fehler beim Beenden der Anwendung: {e}") 