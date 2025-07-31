"""
Dashboard-Klasse für die Hauptbenutzeroberfläche
"""

import customtkinter as ctk
from typing import Dict, Any
import threading
import time
from .custom_widgets import ModernFrame, GradientButton, ModernLabel, SystemInfoCard, AnimatedProgressBar, GlassmorphismFrame
from ..graph_viewer import GraphViewer
from ..icon_manager import IconManager

class Dashboard:
    """Hauptdashboard der SystemMonitorX Anwendung"""
    
    def __init__(self, root, system_monitor, widget_manager, tray_manager=None, theme_manager=None, data_logger=None, config_manager=None):
        """Initialisiert das Dashboard"""
        self.root = root
        self.system_monitor = system_monitor
        self.widget_manager = widget_manager
        self.tray_manager = tray_manager
        self.theme_manager = theme_manager
        self.data_logger = data_logger
        self.config_manager = config_manager
        self.graph_viewer = GraphViewer(theme_manager)
        self.icon_manager = IconManager(theme_manager)
        self.data = {}
        
        # GUI-Elemente
        self.cpu_card = None
        self.memory_card = None
        self.disk_card = None
        self.system_card = None
        
        self._setup_ui()
        self._start_monitoring()
        
    def _setup_ui(self):
        """Erstellt die moderne, responsive Benutzeroberfläche"""
        # Hauptcontainer mit Gradient-Hintergrund
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header-Bereich
        header_frame = GlassmorphismFrame(main_container, self.theme_manager)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Titel mit modernem Design
        title_label = ModernLabel(
            header_frame, 
            self.theme_manager,
            text="SYSTEMMONITORX", 
            font_size=32,
            font_weight="bold"
        )
        title_label.pack(pady=20)
        
        # Untertitel
        subtitle_label = ModernLabel(
            header_frame,
            self.theme_manager,
            text="Modernes System-Monitoring mit Desktop-Widgets",
            font_size=14,
            font_weight="normal"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Systemdaten-Grid mit modernem Layout
        data_container = ctk.CTkFrame(main_container, fg_color="transparent")
        data_container.pack(fill="both", expand=True, pady=(0, 20))
        
        # Responsive Grid-Layout
        data_container.grid_columnconfigure(0, weight=1)
        data_container.grid_columnconfigure(1, weight=1)
        data_container.grid_rowconfigure(0, weight=1)
        data_container.grid_rowconfigure(1, weight=1)
        
        # CPU-Karte mit erweiterten Informationen
        self.cpu_card = SystemInfoCard(data_container, self.theme_manager, "CPU", self.icon_manager)
        self.cpu_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # RAM-Karte
        self.memory_card = SystemInfoCard(data_container, self.theme_manager, "Arbeitsspeicher", self.icon_manager)
        self.memory_card.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        # Festplatten-Karte
        self.disk_card = SystemInfoCard(data_container, self.theme_manager, "Festplatte", self.icon_manager)
        self.disk_card.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")
        
        # System-Info-Karte
        self.system_card = SystemInfoCard(data_container, self.theme_manager, "System", self.icon_manager)
        self.system_card.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="nsew")
        
        # Control-Bereiche mit modernem Design
        controls_container = ctk.CTkFrame(main_container, fg_color="transparent")
        controls_container.pack(fill="x", pady=(0, 20))
        
        # Widget-Controls
        widget_section = GlassmorphismFrame(controls_container, self.theme_manager)
        widget_section.pack(fill="x", pady=(0, 15))
        
        # Widget-Titel
        widget_title = ModernLabel(
            widget_section, 
            self.theme_manager,
            text="DESKTOP-WIDGETS", 
            font_size=16,
            font_weight="bold"
        )
        widget_title.pack(pady=(15, 10))
        
        # Widget-Buttons mit modernem Design
        widget_buttons_frame = ctk.CTkFrame(widget_section, fg_color="transparent")
        widget_buttons_frame.pack(pady=(0, 15))
        
        # Erste Button-Reihe
        button_row1 = ctk.CTkFrame(widget_buttons_frame, fg_color="transparent")
        button_row1.pack(pady=5)
        
        # Theme-Toggle Button
        theme_button = GradientButton(
            button_row1,
            self.theme_manager,
            self.icon_manager,
            "theme_dark" if self.theme_manager.current_theme == "dark" else "theme_light",
            text="Theme wechseln",
            command=self._toggle_theme
        )
        theme_button.pack(side="left", padx=5)
        
        # CPU Widget Button
        cpu_button = GradientButton(
            button_row1,
            self.theme_manager,
            self.icon_manager,
            "widget_cpu",
            text="CPU Widget",
            command=lambda: self._create_widget("cpu")
        )
        cpu_button.pack(side="left", padx=5)
        
        # RAM Widget Button
        ram_button = GradientButton(
            button_row1,
            self.theme_manager,
            self.icon_manager,
            "widget_ram",
            text="RAM Widget",
            command=lambda: self._create_widget("memory")
        )
        ram_button.pack(side="left", padx=5)
        
        # Zweite Button-Reihe
        button_row2 = ctk.CTkFrame(widget_buttons_frame, fg_color="transparent")
        button_row2.pack(pady=5)
        
        # Disk Widget Button
        disk_button = GradientButton(
            button_row2,
            self.theme_manager,
            self.icon_manager,
            "widget_disk",
            text="Disk Widget",
            command=lambda: self._create_widget("disk")
        )
        disk_button.pack(side="left", padx=5)
        
        # System Widget Button
        system_button = GradientButton(
            button_row2,
            self.theme_manager,
            self.icon_manager,
            "widget_system",
            text="System Widget",
            command=lambda: self._create_widget("system")
        )
        system_button.pack(side="left", padx=5)
        
        # Dritte Button-Reihe
        button_row3 = ctk.CTkFrame(widget_buttons_frame, fg_color="transparent")
        button_row3.pack(pady=5)
        
        # Stop Button
        stop_button = GradientButton(
            button_row3,
            self.theme_manager,
            text="⏹️ Alle Widgets stoppen",
            command=self._stop_all_widgets
        )
        stop_button.pack(side="left", padx=5)
        
        # Minimieren Button
        minimize_button = GradientButton(
            button_row2,
            self.theme_manager,
            text="📌 Minimieren",
            command=self._minimize_to_tray
        )
        minimize_button.pack(side="left", padx=5)
        
        # Logging-Sektion
        logging_section = GlassmorphismFrame(controls_container, self.theme_manager)
        logging_section.pack(fill="x", pady=(0, 15))
        
        logging_title = ModernLabel(
            logging_section,
            self.theme_manager,
            text="📊 DATEN-LOGGING", 
            font_size=16,
            font_weight="bold"
        )
        logging_title.pack(pady=(15, 10))
        
        logging_buttons_frame = ctk.CTkFrame(logging_section, fg_color="transparent")
        logging_buttons_frame.pack(pady=(0, 15))
        
        # Logging-Buttons
        start_logging_button = GradientButton(
            logging_buttons_frame,
            self.theme_manager,
            self.icon_manager,
            "logging_start",
            text="Logging starten",
            command=self._start_logging
        )
        start_logging_button.pack(side="left", padx=5)
        
        stop_logging_button = GradientButton(
            logging_buttons_frame,
            self.theme_manager,
            self.icon_manager,
            "logging_stop",
            text="Logging stoppen",
            command=self._stop_logging
        )
        stop_logging_button.pack(side="left", padx=5)
        
        # Graph-Sektion
        graph_section = GlassmorphismFrame(controls_container, self.theme_manager)
        graph_section.pack(fill="x", pady=(0, 15))
        
        graph_title = ModernLabel(
            graph_section,
            self.theme_manager,
            text="📈 GRAPHEN", 
            font_size=16,
            font_weight="bold"
        )
        graph_title.pack(pady=(15, 10))
        
        graph_buttons_frame = ctk.CTkFrame(graph_section, fg_color="transparent")
        graph_buttons_frame.pack(pady=(0, 15))
        
        # Graph-Buttons in Reihen
        graph_row1 = ctk.CTkFrame(graph_buttons_frame, fg_color="transparent")
        graph_row1.pack(pady=5)
        
        overview_graph_button = GradientButton(
            graph_row1,
            self.theme_manager,
            self.icon_manager,
            "graph_icon",
            text="System-Übersicht",
            command=lambda: self._show_graph("overview")
        )
        overview_graph_button.pack(side="left", padx=5)
        
        cpu_graph_button = GradientButton(
            graph_row1,
            self.theme_manager,
            self.icon_manager,
            "graph_icon",
            text="CPU-Graph",
            command=lambda: self._show_graph("cpu")
        )
        cpu_graph_button.pack(side="left", padx=5)
        
        graph_row2 = ctk.CTkFrame(graph_buttons_frame, fg_color="transparent")
        graph_row2.pack(pady=5)
        
        memory_graph_button = GradientButton(
            graph_row2,
            self.theme_manager,
            self.icon_manager,
            "graph_icon",
            text="RAM-Graph",
            command=lambda: self._show_graph("memory")
        )
        memory_graph_button.pack(side="left", padx=5)
        
        disk_graph_button = GradientButton(
            graph_row2,
            self.theme_manager,
            self.icon_manager,
            "graph_icon",
            text="Disk-Graph",
            command=lambda: self._show_graph("disk")
        )
        disk_graph_button.pack(side="left", padx=5)
        
        # Konfigurations-Sektion
        config_section = GlassmorphismFrame(controls_container, self.theme_manager)
        config_section.pack(fill="x")
        
        config_title = ModernLabel(
            config_section,
            self.theme_manager,
            text="⚙️ KONFIGURATION", 
            font_size=16,
            font_weight="bold"
        )
        config_title.pack(pady=(15, 10))
        
        config_buttons_frame = ctk.CTkFrame(config_section, fg_color="transparent")
        config_buttons_frame.pack(pady=(0, 15))
        
        # Konfigurations-Buttons in Reihen
        config_row1 = ctk.CTkFrame(config_buttons_frame, fg_color="transparent")
        config_row1.pack(pady=5)
        
        save_config_button = GradientButton(
            config_row1,
            self.theme_manager,
            self.icon_manager,
            "save_config",
            text="Konfiguration speichern",
            command=self._save_config
        )
        save_config_button.pack(side="left", padx=5)
        
        reset_config_button = GradientButton(
            config_row1,
            self.theme_manager,
            self.icon_manager,
            "reset_config",
            text="Konfiguration zurücksetzen",
            command=self._reset_config
        )
        reset_config_button.pack(side="left", padx=5)
        
        config_row2 = ctk.CTkFrame(config_buttons_frame, fg_color="transparent")
        config_row2.pack(pady=5)
        
        export_config_button = GradientButton(
            config_row2,
            self.theme_manager,
            self.icon_manager,
            "export_config",
            text="Konfiguration exportieren",
            command=self._export_config
        )
        export_config_button.pack(side="left", padx=5)
        
    def _start_monitoring(self):
        """Startet das System-Monitoring"""
        self.system_monitor.add_callback(self._update_ui)
        self.system_monitor.start()
        
    def _update_ui(self, data: Dict[str, Any]):
        """Aktualisiert die Benutzeroberfläche mit neuen Daten"""
        self.data = data
        
        # Daten loggen
        if self.data_logger:
            self.data_logger.log_data(data)
        
        # Widgets mit neuen Daten aktualisieren
        if self.widget_manager:
            self.widget_manager.update_widget_data(data)
        
        # UI-Updates im Hauptthread ausführen
        self.root.after(0, self._update_labels)
        
    def _update_labels(self):
        """Aktualisiert die Karten mit aktuellen Daten und Progress-Bars"""
        if not self.data:
            return
            
        # CPU-Informationen
        if 'cpu' in self.data:
            cpu_info = self.data['cpu']
            cpu_percent = cpu_info['percent']
            cpu_text = f"{cpu_percent:.1f}%"
            
            if cpu_info.get('freq'):
                freq = cpu_info['freq']['current'] / 1000  # MHz zu GHz
                cpu_text += f" | {freq:.1f} GHz"
                
            self.cpu_card.update_value(cpu_text, cpu_percent / 100.0)
            self.cpu_card.update_info(f"Kerne: {cpu_info['count']}")
            
            # Tray-Icon aktualisieren (CPU)
            if self.tray_manager:
                self.tray_manager.update_icon(cpu_percent=cpu_percent)
            
        # RAM-Informationen
        if 'memory' in self.data:
            mem_info = self.data['memory']
            mem_percent = mem_info['percent']
            used_gb = mem_info['used'] / (1024**3)
            total_gb = mem_info['total'] / (1024**3)
            mem_text = f"{mem_percent:.1f}% | {used_gb:.1f} GB"
            
            self.memory_card.update_value(mem_text, mem_percent / 100.0)
            self.memory_card.update_info(f"Gesamt: {total_gb:.1f} GB")
            
            # Tray-Icon aktualisieren (RAM)
            if self.tray_manager:
                self.tray_manager.update_icon(memory_percent=mem_percent)
            
        # Festplatten-Informationen
        if 'disk' in self.data:
            disk_info = self.data['disk']
            disk_percent = disk_info['percent']
            used_gb = disk_info['used'] / (1024**3)
            total_gb = disk_info['total'] / (1024**3)
            disk_text = f"{disk_percent:.1f}% | {used_gb:.1f} GB"
            
            self.disk_card.update_value(disk_text, disk_percent / 100.0)
            self.disk_card.update_info(f"Gesamt: {total_gb:.1f} GB")
            
        # System-Informationen
        if 'system' in self.data:
            sys_info = self.data['system']
            username = sys_info.get('username', 'Unknown')
            sys_text = f"{sys_info['platform']} {sys_info['platform_version']}"
            self.system_card.update_value(sys_text)
            self.system_card.update_info(f"Online: {username}")
            
    def _create_widget(self, widget_type: str):
        """Erstellt ein Desktop-Widget"""
        try:
            self.widget_manager.create_widget(widget_type, self.data, self.root)
        except Exception as e:
            print(f"Fehler beim Erstellen des Widgets: {e}")
            
    def _stop_all_widgets(self):
        """Stoppt alle Desktop-Widgets"""
        try:
            self.widget_manager.stop_all_widgets()
        except Exception as e:
            print(f"Fehler beim Stoppen der Widgets: {e}")
            
    def _minimize_to_tray(self):
        """Minimiert das Fenster in den System-Tray"""
        try:
            if self.root:
                self.root.withdraw()
        except Exception as e:
            print(f"Fehler beim Minimieren: {e}")
            
    def _toggle_theme(self):
        """Wechselt zwischen Dark und Light Mode"""
        try:
            if self.theme_manager:
                current_theme = self.theme_manager.current_theme
                new_theme = "light" if current_theme == "dark" else "dark"
                self.theme_manager.set_theme(new_theme)
                
                # Icon-Manager aktualisieren
                if self.icon_manager:
                    self.icon_manager.update_theme()
                
                # Fenster-Transparenz aktualisieren
                transparency = self.theme_manager.get_transparency()
                self.root.attributes('-alpha', transparency)
                
                print(f"Theme gewechselt zu: {new_theme}")
        except Exception as e:
            print(f"Fehler beim Theme-Wechsel: {e}")
            
    def _start_logging(self):
        """Startet das Daten-Logging"""
        try:
            if self.data_logger:
                self.data_logger.start_logging("both")  # CSV und JSON
                print("Daten-Logging gestartet")
        except Exception as e:
            print(f"Fehler beim Starten des Loggings: {e}")
            
    def _stop_logging(self):
        """Stoppt das Daten-Logging"""
        try:
            if self.data_logger:
                self.data_logger.stop_logging()
                print("Daten-Logging gestoppt")
        except Exception as e:
            print(f"Fehler beim Stoppen des Loggings: {e}")
            
    def _show_graph(self, graph_type: str):
        """Zeigt einen Graphen an"""
        try:
            if self.data_logger:
                # Neueste Log-Daten laden
                data = self.data_logger.get_latest_log_data("csv")
                if data:
                    # Graph-Fenster erstellen
                    self.graph_viewer.create_tkinter_window(data, graph_type)
                else:
                    print("Keine Log-Daten verfügbar. Starten Sie zuerst das Logging.")
        except Exception as e:
            print(f"Fehler beim Anzeigen des Graphen: {e}")
            
    def _save_config(self):
        """Speichert die aktuelle Konfiguration"""
        try:
            if self.config_manager:
                # Aktuelle Einstellungen speichern
                self.config_manager.set_config("app.theme", self.theme_manager.current_theme)
                self.config_manager.set_config("app.transparency", self.theme_manager.get_transparency())
                self.config_manager.set_config("app.window_size", self.root.geometry())
                
                print("Konfiguration gespeichert")
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
            
    def _reset_config(self):
        """Setzt die Konfiguration auf Standardwerte zurück"""
        try:
            if self.config_manager:
                self.config_manager.reset_config()
                print("Konfiguration auf Standardwerte zurückgesetzt")
        except Exception as e:
            print(f"Fehler beim Zurücksetzen der Konfiguration: {e}")
            
    def _export_config(self):
        """Exportiert die Konfiguration"""
        try:
            if self.config_manager:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_path = f"config/export_config_{timestamp}.json"
                
                self.config_manager.export_config(export_path)
                print(f"Konfiguration exportiert nach: {export_path}")
        except Exception as e:
            print(f"Fehler beim Exportieren der Konfiguration: {e}") 