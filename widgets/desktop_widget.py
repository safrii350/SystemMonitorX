"""
Desktop-Widget-Klasse für SystemMonitorX
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Dict, Any, Optional

class DesktopWidget:
    """Eigenständiges Desktop-Widget mit transparentem Design"""
    
    def __init__(self, widget_type: str, data: Dict[str, Any], parent_window=None, config_manager=None):
        """Initialisiert das Desktop-Widget"""
        self.widget_type = widget_type
        self.data = data
        self.parent_window = parent_window
        self.config_manager = config_manager
        self.window = None
        self.running = False
        self.update_thread = None
        
        self._create_window()
        self._start_updates()
        
    def _create_window(self):
        """Erstellt das Widget-Fenster"""
        if self.parent_window:
            # Verwende Toplevel mit Parent-Fenster
            self.window = tk.Toplevel(self.parent_window)
        else:
            # Fallback: Erstelle eigenes Tk-Fenster
            self.window = tk.Tk()
            
        self.window.title(f"SystemMonitorX - {self.widget_type.upper()}")
        self.window.geometry("200x100")
        
        # Fenster-Eigenschaften für Desktop-Widget
        self.window.overrideredirect(True)  # Entfernt Fensterrahmen
        self.window.attributes('-topmost', True)  # Immer im Vordergrund
        self.window.attributes('-alpha', 0.9)  # Transparenz
        
        # Position aus Konfiguration laden oder Standard verwenden
        if self.config_manager:
            position = self.config_manager.get_widget_position(self.widget_type)
            x = position.get('x', -220)
            y = position.get('y', 20)
            
            # Relative Positionen berechnen
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            if x < 0:  # Relative Position von rechts
                x = screen_width + x
            if y < 0:  # Relative Position von unten
                y = screen_height + y
                
            # Widget-Größe aus Konfiguration
            widget_config = self.config_manager.get_widget_config(self.widget_type)
            size = widget_config.get('size', '200x100')
            self.window.geometry(f"{size}+{x}+{y}")
        else:
            # Standard-Position
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            x = screen_width - 220
            y = 20
            self.window.geometry(f"200x100+{x}+{y}")
        
        # Widget-Inhalt
        self._setup_widget_content()
        
        # Drag-and-Drop-Funktionalität
        self._setup_drag_drop()
        
    def _setup_widget_content(self):
        """Erstellt den Widget-Inhalt"""
        # Hauptframe mit modernem Design
        main_frame = tk.Frame(self.window, bg='#1a1a1a', relief='flat', bd=0)
        main_frame.pack(fill="both", expand=True)
        
        # Titel mit Consolas Font
        title_label = tk.Label(
            main_frame,
            text=f"{self.widget_type.upper()}",
            font=('Consolas', 12, 'bold'),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        title_label.pack(pady=8)
        
        # Wert-Label mit modernem Design
        self.value_label = tk.Label(
            main_frame,
            text="Lade...",
            font=('Consolas', 18, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        self.value_label.pack(pady=8)
        
        # Schließen-Button mit modernem Design
        close_button = tk.Button(
            main_frame,
            text="×",
            font=('Consolas', 10, 'bold'),
            fg='#ffffff',
            bg='#ff4444',
            relief='flat',
            bd=0,
            command=self.destroy
        )
        close_button.pack(side="top", anchor="ne", padx=8, pady=8)
        
    def _setup_drag_drop(self):
        """Richtet Drag-and-Drop-Funktionalität ein"""
        self.window.bind('<Button-1>', self._on_click)
        self.window.bind('<B1-Motion>', self._on_drag)
        
    def _on_click(self, event):
        """Behandelt Mausklicks"""
        self.window.x = event.x
        self.window.y = event.y
        
    def _on_drag(self, event):
        """Behandelt Drag-Operationen"""
        deltax = event.x - self.window.x
        deltay = event.y - self.window.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")
        
        # Position in Konfiguration speichern
        if self.config_manager:
            self.config_manager.save_widget_position(self.widget_type, x, y)
        
    def _start_updates(self):
        """Startet die Aktualisierungsschleife"""
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        
    def _update_loop(self):
        """Hauptschleife für Widget-Updates"""
        while self.running:
            try:
                # UI-Updates im Hauptthread ausführen
                if self.window and self.window.winfo_exists():
                    self.window.after(0, self._update_display)
                time.sleep(1.0)  # Aktualisierung jede Sekunde
            except Exception as e:
                print(f"Fehler im Widget-Update-Loop: {e}")
                break
                
    def _update_display(self):
        """Aktualisiert die Widget-Anzeige"""
        try:
            if not self.data:
                return
                
            if self.widget_type == "cpu" and 'cpu' in self.data:
                cpu_info = self.data['cpu']
                value = f"{cpu_info['percent']:.1f}%"
                self.value_label.configure(text=value)
                
            elif self.widget_type == "memory" and 'memory' in self.data:
                mem_info = self.data['memory']
                value = f"{mem_info['percent']:.1f}%"
                self.value_label.configure(text=value)
                
            elif self.widget_type == "disk" and 'disk' in self.data:
                disk_info = self.data['disk']
                value = f"{disk_info['percent']:.1f}%"
                self.value_label.configure(text=value)
                
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Widgets: {e}")
            
    def update_data(self, data: Dict[str, Any]):
        """Aktualisiert die Widget-Daten"""
        self.data = data
        
    def destroy(self):
        """Zerstört das Widget"""
        self.running = False
        if self.window:
            try:
                self.window.destroy()
            except:
                pass
                
    def show(self):
        """Zeigt das Widget an"""
        if self.window:
            self.window.deiconify()
            
    def hide(self):
        """Versteckt das Widget"""
        if self.window:
            self.window.withdraw() 