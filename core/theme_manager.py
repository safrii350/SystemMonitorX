"""
Theme-Manager für SystemMonitorX
"""

import customtkinter as ctk
from typing import Dict, Any
import json
import os

class ThemeManager:
    """Verwaltet Themes und Design-Einstellungen"""
    
    def __init__(self):
        """Initialisiert den Theme-Manager"""
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "bg_color": "#141414",
                "fg_color": "#1a1a1a",
                "text_color": "#f2ecfa",
                "accent_color": "#4a307d",
                "secondary_color": "#6c3dd9",
                "primary_color": "#8b5cf6",
                "border_color": "#2d1b69",
                "card_bg": "#1e1e1e",
                "hover_color": "#5a3a8d",
                "transparency": 0.9,
                "blur_effect": True,
                "glass_effect": True,
                "gradient_start": "#141414",
                "gradient_end": "#1a1a1a"
            },
            "light": {
                "bg_color": "#ffffff",
                "fg_color": "#f8f9fa",
                "text_color": "#141414",
                "accent_color": "#6c3dd9",
                "secondary_color": "#8b5cf6",
                "primary_color": "#a855f7",
                "border_color": "#e5e7eb",
                "card_bg": "#ffffff",
                "hover_color": "#7c4de9",
                "transparency": 0.95,
                "blur_effect": False,
                "glass_effect": True,
                "gradient_start": "#ffffff",
                "gradient_end": "#f8f9fa"
            }
        }
        
    def get_theme(self, theme_name: str = None) -> Dict[str, Any]:
        """Gibt das aktuelle Theme zurück"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes["dark"])
        
    def set_theme(self, theme_name: str):
        """Setzt das aktuelle Theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self._apply_theme()
            
    def _apply_theme(self):
        """Wendet das aktuelle Theme an"""
        theme = self.get_theme()
        
        # CustomTkinter Theme-Einstellungen
        if self.current_theme == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
            
    def get_color(self, color_name: str) -> str:
        """Gibt eine Farbe aus dem aktuellen Theme zurück"""
        theme = self.get_theme()
        return theme.get(color_name, "#000000")
        
    def get_transparency(self) -> float:
        """Gibt die Transparenz des aktuellen Themes zurück"""
        theme = self.get_theme()
        return theme.get("transparency", 1.0)
        
    def has_blur_effect(self) -> bool:
        """Gibt zurück, ob Blur-Effekt aktiv ist"""
        theme = self.get_theme()
        return theme.get("blur_effect", False)
        
    def has_glass_effect(self) -> bool:
        """Gibt zurück, ob Glass-Effekt aktiv ist"""
        theme = self.get_theme()
        return theme.get("glass_effect", False) 