"""
Graph-Viewer für SystemMonitorX
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
from typing import List, Dict, Any, Optional
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GraphViewer:
    """Erstellt Graphen aus Systemdaten"""
    
    def __init__(self, theme_manager=None):
        """Initialisiert den Graph-Viewer"""
        self.theme_manager = theme_manager
        self.setup_matplotlib_style()
        
    def setup_matplotlib_style(self):
        """Konfiguriert das matplotlib-Styling"""
        plt.style.use('dark_background' if self.theme_manager and 
                     self.theme_manager.current_theme == "dark" else 'default')
        
        # Custom Styling
        plt.rcParams['figure.facecolor'] = '#1a1a1a' if self.theme_manager and \
            self.theme_manager.current_theme == "dark" else '#f0f0f0'
        plt.rcParams['axes.facecolor'] = '#2b2b2b' if self.theme_manager and \
            self.theme_manager.current_theme == "dark" else '#ffffff'
        plt.rcParams['text.color'] = '#ffffff' if self.theme_manager and \
            self.theme_manager.current_theme == "dark" else '#000000'
        plt.rcParams['axes.labelcolor'] = '#ffffff' if self.theme_manager and \
            self.theme_manager.current_theme == "dark" else '#000000'
        plt.rcParams['xtick.color'] = '#ffffff' if self.theme_manager and \
            self.theme_manager.current_theme == "dark" else '#000000'
        plt.rcParams['ytick.color'] = '#ffffff' if self.theme_manager and \
            self.theme_manager.current_theme == "dark" else '#000000'
        
    def create_system_overview_graph(self, data: List[Dict[str, Any]], 
                                   save_path: Optional[str] = None) -> Figure:
        """Erstellt einen Überblicksgraphen für alle Systemdaten"""
        
        if not data:
            return self._create_empty_figure("Keine Daten verfügbar")
            
        # Daten vorbereiten
        timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in data]
        cpu_percent = [float(entry['cpu_percent']) for entry in data]
        memory_percent = [float(entry['memory_percent']) for entry in data]
        disk_percent = [float(entry['disk_percent']) for entry in data]
        
        # Figure erstellen
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), 
                                            sharex=True, height_ratios=[1, 1, 1])
        fig.suptitle('SystemMonitorX - Systemübersicht', fontsize=16, fontweight='bold')
        
        # CPU-Graph
        ax1.plot(timestamps, cpu_percent, color='#00ff00', linewidth=2, label='CPU')
        ax1.fill_between(timestamps, cpu_percent, alpha=0.3, color='#00ff00')
        ax1.set_ylabel('CPU (%)', fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Memory-Graph
        ax2.plot(timestamps, memory_percent, color='#007acc', linewidth=2, label='RAM')
        ax2.fill_between(timestamps, memory_percent, alpha=0.3, color='#007acc')
        ax2.set_ylabel('RAM (%)', fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Disk-Graph
        ax3.plot(timestamps, disk_percent, color='#ff6600', linewidth=2, label='Festplatte')
        ax3.fill_between(timestamps, disk_percent, alpha=0.3, color='#ff6600')
        ax3.set_ylabel('Festplatte (%)', fontweight='bold')
        ax3.set_xlabel('Zeit', fontweight='bold')
        ax3.set_ylim(0, 100)
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # X-Achse formatieren
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax3.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            
        return fig
        
    def create_cpu_graph(self, data: List[Dict[str, Any]], 
                        save_path: Optional[str] = None) -> Figure:
        """Erstellt einen detaillierten CPU-Graphen"""
        
        if not data:
            return self._create_empty_figure("Keine CPU-Daten verfügbar")
            
        timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in data]
        cpu_percent = [float(entry['cpu_percent']) for entry in data]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(timestamps, cpu_percent, color='#00ff00', linewidth=3, label='CPU-Auslastung')
        ax.fill_between(timestamps, cpu_percent, alpha=0.4, color='#00ff00')
        
        ax.set_title('CPU-Auslastung über Zeit', fontsize=16, fontweight='bold')
        ax.set_ylabel('CPU (%)', fontweight='bold')
        ax.set_xlabel('Zeit', fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # X-Achse formatieren
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            
        return fig
        
    def create_memory_graph(self, data: List[Dict[str, Any]], 
                           save_path: Optional[str] = None) -> Figure:
        """Erstellt einen detaillierten Memory-Graphen"""
        
        if not data:
            return self._create_empty_figure("Keine Memory-Daten verfügbar")
            
        timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in data]
        memory_percent = [float(entry['memory_percent']) for entry in data]
        memory_used = [float(entry['memory_used_gb']) for entry in data]
        memory_total = [float(entry['memory_total_gb']) for entry in data]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Prozent-Graph
        ax1.plot(timestamps, memory_percent, color='#007acc', linewidth=3, label='RAM-Auslastung')
        ax1.fill_between(timestamps, memory_percent, alpha=0.4, color='#007acc')
        ax1.set_title('RAM-Auslastung über Zeit', fontsize=16, fontweight='bold')
        ax1.set_ylabel('RAM (%)', fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # GB-Graph
        ax2.plot(timestamps, memory_used, color='#ff6600', linewidth=3, label='Verwendet')
        ax2.plot(timestamps, memory_total, color='#00ff00', linewidth=3, label='Gesamt')
        ax2.fill_between(timestamps, memory_used, alpha=0.4, color='#ff6600')
        ax2.set_ylabel('RAM (GB)', fontweight='bold')
        ax2.set_xlabel('Zeit', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # X-Achse formatieren
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            
        return fig
        
    def create_disk_graph(self, data: List[Dict[str, Any]], 
                         save_path: Optional[str] = None) -> Figure:
        """Erstellt einen detaillierten Disk-Graphen"""
        
        if not data:
            return self._create_empty_figure("Keine Disk-Daten verfügbar")
            
        timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in data]
        disk_percent = [float(entry['disk_percent']) for entry in data]
        disk_used = [float(entry['disk_used_gb']) for entry in data]
        disk_total = [float(entry['disk_total_gb']) for entry in data]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Prozent-Graph
        ax1.plot(timestamps, disk_percent, color='#ff6600', linewidth=3, label='Festplatten-Auslastung')
        ax1.fill_between(timestamps, disk_percent, alpha=0.4, color='#ff6600')
        ax1.set_title('Festplatten-Auslastung über Zeit', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Festplatte (%)', fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # GB-Graph
        ax2.plot(timestamps, disk_used, color='#ff4444', linewidth=3, label='Verwendet')
        ax2.plot(timestamps, disk_total, color='#00ff00', linewidth=3, label='Gesamt')
        ax2.fill_between(timestamps, disk_used, alpha=0.4, color='#ff4444')
        ax2.set_ylabel('Festplatte (GB)', fontweight='bold')
        ax2.set_xlabel('Zeit', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # X-Achse formatieren
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor=fig.get_facecolor())
            
        return fig
        
    def _create_empty_figure(self, message: str) -> Figure:
        """Erstellt eine leere Figure mit Nachricht"""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, message, ha='center', va='center', 
                transform=ax.transAxes, fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return fig
        
    def create_tkinter_window(self, data: List[Dict[str, Any]], 
                             graph_type: str = "overview") -> tk.Toplevel:
        """Erstellt ein Tkinter-Fenster mit Graphen"""
        
        window = tk.Toplevel()
        window.title(f"SystemMonitorX - {graph_type.title()} Graph")
        window.geometry("1000x700")
        
        # Graph erstellen
        if graph_type == "overview":
            fig = self.create_system_overview_graph(data)
        elif graph_type == "cpu":
            fig = self.create_cpu_graph(data)
        elif graph_type == "memory":
            fig = self.create_memory_graph(data)
        elif graph_type == "disk":
            fig = self.create_disk_graph(data)
        else:
            fig = self._create_empty_figure("Unbekannter Graph-Typ")
            
        # Canvas erstellen
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        
        return window 