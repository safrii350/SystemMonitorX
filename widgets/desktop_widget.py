"""
Desktop-Widget-Klasse für SystemMonitorX
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Dict, Any, Optional
from PIL import Image, ImageTk, ImageDraw
import os
from pathlib import Path

class RoundedWidgetFrame(tk.Frame):
    """Frame mit abgerundeten Ecken ohne Transparenz"""
    
    def __init__(self, parent, bg_color="#1a1a1a", corner_radius=15, **kwargs):
        super().__init__(parent, **kwargs)
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        
        # Widget-Größe
        self.width = 280
        self.height = 80
        
        # Hintergrundbild mit abgerundeten Ecken erstellen
        self._create_rounded_background()
        
    def _create_rounded_background(self):
        """Erstellt ein Hintergrundbild mit abgerundeten Ecken"""
        try:
            # Bild mit abgerundeten Ecken erstellen
            image = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Farbe in RGB konvertieren
            if self.bg_color.startswith('#'):
                bg_rgb = tuple(int(self.bg_color[i:i+2], 16) for i in (1, 3, 5))
            else:
                bg_rgb = (26, 26, 26)  # Standard dunkelgrau
            
            # Abgerundetes Rechteck ohne Transparenz
            draw.rounded_rectangle(
                [0, 0, self.width-1, self.height-1],
                radius=self.corner_radius,
                fill=bg_rgb
            )
            
            # Bild als PhotoImage konvertieren
            self.bg_image = ImageTk.PhotoImage(image)
            
            # Hintergrundbild setzen
            bg_label = tk.Label(self, image=self.bg_image, bg=self.bg_color)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()  # Hintergrund nach hinten
            
        except Exception as e:
            print(f"Fehler beim Erstellen des abgerundeten Hintergrunds: {e}")
            # Fallback: Normaler Frame
            self.configure(bg=self.bg_color)
    
    def configure(self, **kwargs):
        """Konfiguriert das Widget und aktualisiert den Hintergrund"""
        if 'bg' in kwargs:
            self.bg_color = kwargs['bg']
            self._create_rounded_background()
        super().configure(**kwargs)

class DesktopWidget:
    """Eigenständiges Desktop-Widget mit transparentem Design"""
    
    def __init__(self, widget_type: str, data: Dict[str, Any], parent_window=None, config_manager=None, theme_manager=None):
        """Initialisiert das Desktop-Widget"""
        self.widget_type = widget_type
        self.data = data
        self.parent_window = parent_window
        self.config_manager = config_manager
        self.theme_manager = theme_manager
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
        self.window.geometry("280x80")
        
        # Fenster-Eigenschaften für Desktop-Widget
        self.window.overrideredirect(True)  # Entfernt Fensterrahmen
        self.window.attributes('-topmost', True)  # Immer im Vordergrund
        
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
        """Erstellt den Widget-Inhalt mit strukturiertem Layout"""
        # Theme-Farben bestimmen
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            bg_color = theme.get("card_bg", "#1a1a1a")
            text_color = theme.get("text_color", "#ffffff")
            accent_color = theme.get("accent_color", "#00ff00")
        else:
            bg_color = "#1a1a1a"
            text_color = "#ffffff"
            accent_color = "#00ff00"
        
        # Hauptframe mit abgerundeten Ecken
        main_frame = RoundedWidgetFrame(self.window, bg_color=bg_color, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Lila Close-Button (oben rechts)
        close_button = tk.Button(
            main_frame,
            text="×",
            font=('Consolas', 14, 'bold'),
            fg='#ffffff',
            bg='#8b5cf6',  # Lila Farbe
            relief='flat',
            bd=0,
            command=self.destroy,
            cursor='hand2'
        )
        close_button.pack(side="top", anchor="ne", padx=8, pady=4)
        
        # Hauptinhalt
        content_frame = tk.Frame(main_frame, bg=bg_color)
        content_frame.pack(expand=True, fill="both", padx=15, pady=10)
        
        # Linke Seite: Icon und Name
        left_frame = tk.Frame(content_frame, bg=bg_color)
        left_frame.pack(side="left", fill="y", padx=(0, 15))
        
        # Icon laden und anzeigen (oben links)
        icon = self._load_widget_icon()
        if icon:
            icon_label = tk.Label(left_frame, image=icon, bg=bg_color)
            icon_label.pack(pady=(0, 8))
            # Icon referenzieren
            icon_label._icon = icon
        
        # Widget-Name (unter dem Icon)
        title_label = tk.Label(
            left_frame,
            text=f"{self.widget_type.upper()}",
            font=('Consolas', 10, 'bold'),
            fg=text_color,
            bg=bg_color
        )
        title_label.pack()
        
        # Rechte Seite: Detaillierte Informationen
        right_frame = tk.Frame(content_frame, bg=bg_color)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Widget-spezifische Informationen
        if self.widget_type == "cpu":
            self._setup_cpu_info(right_frame, bg_color, text_color, accent_color)
        elif self.widget_type == "memory":
            self._setup_memory_info(right_frame, bg_color, text_color, accent_color)
        elif self.widget_type == "disk":
            self._setup_disk_info(right_frame, bg_color, text_color, accent_color)
        elif self.widget_type == "system":
            self._setup_system_info(right_frame, bg_color, text_color, accent_color)
        else:
            # Fallback für unbekannte Widget-Typen
            self.value_label = tk.Label(
                right_frame,
                text="Lade...",
                font=('Consolas', 16, 'bold'),
                fg=accent_color,
                bg=bg_color
            )
            self.value_label.pack(expand=True)
    
    def _setup_cpu_info(self, parent, bg_color, text_color, accent_color):
        """Setup für CPU-Widget mit detaillierten Informationen"""
        # CPU-Name Label (erste Zeile)
        self.cpu_name_label = tk.Label(
            parent,
            text="CPU: Intel i7-1355U",
            font=('Consolas', 10),
            fg=text_color,
            bg=bg_color,
            anchor="w"
        )
        self.cpu_name_label.pack(anchor="w", pady=(0, 5))
        
        # CPU-Auslastung Label (zweite Zeile)
        self.value_label = tk.Label(
            parent,
            text="USAGE: 5%",
            font=('Consolas', 10),
            fg=accent_color,
            bg=bg_color,
            anchor="w"
        )
        self.value_label.pack(anchor="w")
    
    def _setup_memory_info(self, parent, bg_color, text_color, accent_color):
        """Setup für Memory-Widget"""
        # Memory-Info Label (erste Zeile)
        self.memory_info_label = tk.Label(
            parent,
            text="RAM: 16GB DDR4",
            font=('Consolas', 10),
            fg=text_color,
            bg=bg_color,
            anchor="w"
        )
        self.memory_info_label.pack(anchor="w", pady=(0, 5))
        
        # Memory-Auslastung Label (zweite Zeile)
        self.value_label = tk.Label(
            parent,
            text="USAGE: 59.1%",
            font=('Consolas', 10),
            fg=accent_color,
            bg=bg_color,
            anchor="w"
        )
        self.value_label.pack(anchor="w")
    
    def _setup_disk_info(self, parent, bg_color, text_color, accent_color):
        """Setup für Disk-Widget"""
        # Disk-Info Label (erste Zeile)
        self.disk_info_label = tk.Label(
            parent,
            text="DISK: 1TB SSD",
            font=('Consolas', 10),
            fg=text_color,
            bg=bg_color,
            anchor="w"
        )
        self.disk_info_label.pack(anchor="w", pady=(0, 5))
        
        # Disk-Auslastung Label (zweite Zeile)
        self.value_label = tk.Label(
            parent,
            text="USAGE: 45.2%",
            font=('Consolas', 10),
            fg=accent_color,
            bg=bg_color,
            anchor="w"
        )
        self.value_label.pack(anchor="w")
    
    def _setup_system_info(self, parent, bg_color, text_color, accent_color):
        """Setup für System-Widget"""
        # System-Info Label (erste Zeile)
        self.system_info_label = tk.Label(
            parent,
            text="OS: Windows 11",
            font=('Consolas', 10),
            fg=text_color,
            bg=bg_color,
            anchor="w"
        )
        self.system_info_label.pack(anchor="w", pady=(0, 5))
        
        # System-Status Label (zweite Zeile)
        self.value_label = tk.Label(
            parent,
            text="STATUS: Online",
            font=('Consolas', 10),
            fg=accent_color,
            bg=bg_color,
            anchor="w"
        )
        self.value_label.pack(anchor="w")
        
    def _load_widget_icon(self) -> Optional[ImageTk.PhotoImage]:
        """Lädt das Widget-Icon basierend auf Theme"""
        try:
            # Theme-Suffix bestimmen
            theme_suffix = "dark"
            if self.theme_manager:
                theme_suffix = self.theme_manager.current_theme
            
            # Icon-Pfad bestimmen
            icons_path = Path("assets/icons")
            icon_name = f"widget_{self.widget_type}"
            icon_path = icons_path / f"{icon_name}_{theme_suffix}.png"
            
            if not icon_path.exists():
                # Fallback auf generisches Icon
                icon_path = icons_path / f"{icon_name}.png"
            
            if icon_path.exists():
                # Icon laden und resizen
                image = Image.open(icon_path)
                image = image.resize((24, 24), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
                
        except Exception as e:
            print(f"Fehler beim Laden des Widget-Icons {self.widget_type}: {e}")
        
        return None
        
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