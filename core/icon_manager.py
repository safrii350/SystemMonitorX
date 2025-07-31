"""
Icon-Manager für SystemMonitorX
Verwaltet Icons basierend auf dem aktuellen Theme
"""

import os
from pathlib import Path
from PIL import Image, ImageTk
import customtkinter as ctk

class IconManager:
    """Verwaltet Icons basierend auf dem aktuellen Theme"""
    
    def __init__(self, theme_manager=None):
        """Initialisiert den Icon-Manager"""
        self.theme_manager = theme_manager
        self.icons_path = Path("assets/icons")
        self._icon_cache = {}
        
    def get_theme_suffix(self) -> str:
        """Gibt das Theme-Suffix zurück (dark/light)"""
        if self.theme_manager:
            return self.theme_manager.current_theme
        return "dark"  # Standard
        
    def get_icon_path(self, icon_name: str) -> str:
        """Gibt den Pfad zu einem Icon zurück"""
        theme_suffix = self.get_theme_suffix()
        
        # Versuche zuerst theme-spezifisches Icon
        theme_specific_path = self.icons_path / f"{icon_name}_{theme_suffix}.png"
        if theme_specific_path.exists():
            return str(theme_specific_path)
            
        # Fallback auf generisches Icon
        generic_path = self.icons_path / f"{icon_name}.png"
        if generic_path.exists():
            return str(generic_path)
            
        return None
        
    def load_icon(self, icon_name: str, size: tuple = (24, 24)) -> ImageTk.PhotoImage:
        """Lädt ein Icon und cached es"""
        theme_suffix = self.get_theme_suffix()
        cache_key = f"{icon_name}_{theme_suffix}_{size[0]}x{size[1]}"
        
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]
            
        icon_path = self.get_icon_path(icon_name)
        if not icon_path or not os.path.exists(icon_path):
            return None
            
        try:
            # Icon laden und resizen
            image = Image.open(icon_path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Cache das Icon
            self._icon_cache[cache_key] = photo
            return photo
            
        except Exception as e:
            print(f"Fehler beim Laden des Icons {icon_name}: {e}")
            return None
            
    def get_widget_icon(self, widget_type: str) -> ImageTk.PhotoImage:
        """Lädt ein Widget-Icon"""
        if widget_type == "cpu":
            return self.load_icon("widget_cpu", (32, 32))
        elif widget_type == "memory":
            return self.load_icon("widget_ram", (32, 32))
        elif widget_type == "disk":
            return self.load_icon("widget_disk", (32, 32))
        elif widget_type == "system":
            return self.load_icon("widget_system", (32, 32))
        return None
        
    def get_theme_icon(self) -> ImageTk.PhotoImage:
        """Lädt das Theme-Icon"""
        theme_suffix = self.get_theme_suffix()
        return self.load_icon(f"theme_{theme_suffix}", (24, 24))
        
    def clear_cache(self):
        """Löscht den Icon-Cache"""
        self._icon_cache.clear()
        
    def update_theme(self):
        """Aktualisiert Icons basierend auf neuem Theme"""
        self.clear_cache() 