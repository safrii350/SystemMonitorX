import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Dict, Any, Optional
from PIL import Image, ImageTk, ImageDraw
import os
from pathlib import Path

class RoundedWidgetFrame(tk.Frame):
    def __init__(self, parent, bg_color="#1a1a1a", corner_radius=20, **kwargs):
        super().__init__(parent, **kwargs)
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.width = 320  # Breiter für längere Texte
        self.height = 110  # Höher für bessere Darstellung
        self._create_rounded_background()

    def _create_rounded_background(self):
        try:
            # Transparenter Hintergrund für saubere abgerundete Ecken
            image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            if self.bg_color.startswith('#'):
                bg_rgb = tuple(int(self.bg_color[i:i+2], 16) for i in (1, 3, 5))
            else:
                bg_rgb = (26, 26, 26)
            # Abgerundetes Rechteck mit Theme-Farbe
            draw.rounded_rectangle([0, 0, self.width-1, self.height-1], radius=self.corner_radius, fill=bg_rgb + (255,))
            self.bg_image = ImageTk.PhotoImage(image)
            # Transparenter Hintergrund für saubere Ränder
            bg_label = tk.Label(self, image=self.bg_image, bg=self.bg_color)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception as e:
            print(f"Fehler beim Erstellen des abgerundeten Hintergrunds: {e}")
            self.configure(bg=self.bg_color)

    def configure(self, **kwargs):
        if 'bg' in kwargs:
            self.bg_color = kwargs['bg']
            self._create_rounded_background()
        super().configure(**kwargs)

class DesktopWidget:
    def __init__(self, widget_type: str, data: Dict[str, Any], parent_window=None, config_manager=None, theme_manager=None):
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
        self.window = tk.Toplevel(self.parent_window) if self.parent_window else tk.Tk()
        self.window.title(f"SystemMonitorX - {self.widget_type.upper()}")
        self.window.geometry("320x110")
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)

        if self.config_manager:
            position = self.config_manager.get_widget_position(self.widget_type)
            x = position.get('x', -220)
            y = position.get('y', 20)
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            if x < 0:
                x = screen_width + x
            if y < 0:
                y = screen_height + y
            size = self.config_manager.get_widget_config(self.widget_type).get('size', '320x110')
            self.window.geometry(f"{size}+{x}+{y}")
        else:
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            x = screen_width - 260
            y = 20
            self.window.geometry(f"320x110+{x}+{y}")

        self._setup_widget_content()
        self._setup_drag_drop()

    def _setup_widget_content(self):
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            bg_color = theme.get("card_bg", "#1a1a1a")
            text_color = theme.get("text_color", "#ffffff")
            accent_color = theme.get("accent_color", "#00ff00")
        else:
            bg_color = "#1a1a1a"
            text_color = "#ffffff"
            accent_color = "#00ff00"

        main_frame = RoundedWidgetFrame(self.window, bg_color=bg_color, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Einfacher lila Close-Button (ohne Bild)
        close_button = tk.Button(
            main_frame,
            text="×",
            font=('Consolas', 12, 'bold'),
            fg='#ffffff',
            bg='#8b5cf6',
            relief='flat',
            bd=0,
            width=2,
            height=1,
            highlightthickness=0,
            command=self.destroy,
            cursor='hand2'
        )
        close_button.place(relx=1.0, x=-15, y=10, anchor="ne")

        content_frame = tk.Frame(main_frame, bg=bg_color)
        content_frame.pack(expand=True, fill="both", padx=15, pady=10)

        top_line = tk.Frame(content_frame, bg=bg_color)
        top_line.pack(side="top", fill="x", pady=(0, 5))

        icon = self._load_widget_icon()
        if icon:
            icon_label = tk.Label(top_line, image=icon, bg=bg_color)
            icon_label.pack(side="left", padx=(0, 10))
            icon_label._icon = icon

        self.title_label = tk.Label(
            top_line,
            text="",
            font=('Consolas', 10, 'bold'),
            fg=text_color,
            bg=bg_color,
            anchor="w",
            justify="left"
        )
        self.title_label.pack(side="left", fill="x", expand=True)

        # Usage-Wert Label (oben)
        self.value_label = tk.Label(
            content_frame,
            text="",
            font=('Consolas', 9),
            fg=accent_color,
            bg=bg_color,
            anchor="w"
        )
        self.value_label.pack(side="top", anchor="w", pady=(0, 3))
        
        # Progress Bar für Usage-Werte (mitten)
        self.progress_frame = tk.Frame(content_frame, bg=bg_color, height=8)
        self.progress_frame.pack(side="top", fill="x", pady=(0, 3))
        self.progress_frame.pack_propagate(False)
        
        # Progress Bar Hintergrund (dunkelgrau)
        self.progress_bg = tk.Frame(self.progress_frame, bg='#2a2a2a', height=6)
        self.progress_bg.pack(fill="x", pady=1)
        
        # Progress Bar Füllung (lila/blau)
        self.progress_fill = tk.Frame(self.progress_bg, bg=accent_color, height=6)
        self.progress_fill.pack(side="left", fill="y")
        
        # Info Label (unten) - für Kerne, Gesamt, etc.
        self.info_label = tk.Label(
            content_frame,
            text="",
            font=('Consolas', 8),
            fg=text_color,
            bg=bg_color,
            anchor="w"
        )
        self.info_label.pack(side="top", anchor="w")

        if self.widget_type == "cpu":
            self._setup_cpu_info()
        elif self.widget_type == "memory":
            self._setup_memory_info()
        elif self.widget_type == "disk":
            self._setup_disk_info()
        elif self.widget_type == "system":
            self._setup_system_info()
            # System-Widget braucht keine Progress Bar
            self.progress_frame.pack_forget()
        else:
            self.title_label.configure(text=f"{self.widget_type.upper()}")
            self.value_label.configure(text="Lade...")

    def _setup_cpu_info(self):
        self.title_label.configure(text="CPU: Intel i7-1355U")
        self.value_label.configure(text="9.5%")
        self.info_label.configure(text="Kerne: 12")

    def _setup_memory_info(self):
        self.title_label.configure(text="RAM: 16GB DDR4")
        self.value_label.configure(text="59.1%")
        self.info_label.configure(text="Gesamt: 31.7 GB")

    def _setup_disk_info(self):
        self.title_label.configure(text="DISK: 1TB SSD")
        self.value_label.configure(text="45.2%")
        self.info_label.configure(text="Gesamt: 475.7 GB")

    def _setup_system_info(self):
        self.title_label.configure(text="OS: Windows 11")
        self.value_label.configure(text="Online")
        self.info_label.configure(text="Online: Unknown")

    def _load_widget_icon(self) -> Optional[ImageTk.PhotoImage]:
        try:
            theme_suffix = self.theme_manager.current_theme if self.theme_manager else "dark"
            icons_path = Path("assets/icons")
            icon_name = f"widget_{self.widget_type}"
            icon_path = icons_path / f"{icon_name}_{theme_suffix}.png"
            if not icon_path.exists():
                icon_path = icons_path / f"{icon_name}.png"
            if icon_path.exists():
                image = Image.open(icon_path)
                image = image.resize((24, 24), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Fehler beim Laden des Widget-Icons {self.widget_type}: {e}")
        return None

    def _setup_drag_drop(self):
        self.window.bind('<Button-1>', self._on_click)
        self.window.bind('<B1-Motion>', self._on_drag)

    def _on_click(self, event):
        self.window.x = event.x
        self.window.y = event.y

    def _on_drag(self, event):
        deltax = event.x - self.window.x
        deltay = event.y - self.window.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")
        if self.config_manager:
            self.config_manager.save_widget_position(self.widget_type, x, y)

    def _start_updates(self):
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

    def _update_loop(self):
        while self.running:
            try:
                if self.window and self.window.winfo_exists():
                    self.window.after(0, self._update_display)
                time.sleep(1.0)
            except Exception as e:
                print(f"Fehler im Widget-Update-Loop: {e}")
                break

    def _update_display(self):
        try:
            if not self.data:
                return
                
            if self.widget_type == "cpu" and 'cpu' in self.data:
                cpu_info = self.data['cpu']
                usage_percent = cpu_info['percent']
                self.value_label.configure(text=f"{usage_percent:.1f}%")
                self._update_progress_bar(usage_percent)
                
            elif self.widget_type == "memory" and 'memory' in self.data:
                mem_info = self.data['memory']
                usage_percent = mem_info['percent']
                used_gb = mem_info['used'] / (1024**3)  # Bytes zu GB
                total_gb = mem_info['total'] / (1024**3)  # Bytes zu GB
                self.value_label.configure(text=f"{usage_percent:.1f}%")
                self.info_label.configure(text=f"Gesamt: {total_gb:.1f} GB")
                self._update_progress_bar(usage_percent)
                
            elif self.widget_type == "disk" and 'disk' in self.data:
                disk_info = self.data['disk']
                usage_percent = disk_info['percent']
                used_gb = disk_info['used'] / (1024**3)  # Bytes zu GB
                total_gb = disk_info['total'] / (1024**3)  # Bytes zu GB
                self.value_label.configure(text=f"{usage_percent:.1f}%")
                self.info_label.configure(text=f"Gesamt: {total_gb:.1f} GB")
                self._update_progress_bar(usage_percent)
                
            elif self.widget_type == "system" and 'system' in self.data:
                sys_info = self.data['system']
                username = sys_info.get('username', 'Unknown')
                self.value_label.configure(text="Online")
                self.info_label.configure(text=f"Online: {username}")
                
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Widgets: {e}")
    
    def _update_progress_bar(self, percent):
        """Aktualisiert die Progress Bar basierend auf dem Prozentwert"""
        try:
            # Prozentwert auf 0-100 begrenzen
            percent = max(0, min(100, percent))
            
            # Progress Bar Breite berechnen (0-1 als relwidth)
            progress_width = percent / 100.0
            
            # Progress Bar aktualisieren
            self.progress_fill.pack_forget()
            self.progress_fill.pack(side="left", fill="y", ipadx=0)
            
            # Breite der Progress Bar setzen
            self.progress_bg.update_idletasks()
            bar_width = self.progress_bg.winfo_width()
            fill_width = int(bar_width * progress_width)
            
            if fill_width > 0:
                self.progress_fill.configure(width=fill_width)
            else:
                self.progress_fill.configure(width=1)
                
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Progress Bar: {e}")

    def update_data(self, data: Dict[str, Any]):
        self.data = data

    def destroy(self):
        self.running = False
        if self.window:
            try:
                self.window.destroy()
            except:
                pass

    def show(self):
        if self.window:
            self.window.deiconify()

    def hide(self):
        if self.window:
            self.window.withdraw()
