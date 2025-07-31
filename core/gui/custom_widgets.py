"""
Moderne CustomTkinter-Widgets für SystemMonitorX
"""

import customtkinter as ctk
from typing import Optional, Callable
import tkinter as tk
import math

class ModernFrame(ctk.CTkFrame):
    """Moderner Frame mit Glasmorphismus-Effekt"""
    
    def __init__(self, master, theme_manager=None, **kwargs):
        super().__init__(master, **kwargs)
        self.theme_manager = theme_manager
        self._apply_theme()
        
    def _apply_theme(self):
        """Wendet das Theme an"""
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            self.configure(
                fg_color=theme.get("card_bg", "#1e1e1e"),
                border_color=theme.get("border_color", "#2d1b69"),
                border_width=1,
                corner_radius=12
            )

class GradientButton(ctk.CTkButton):
    """Moderner Button mit Gradient-Effekt und Icon-Unterstützung"""
    
    def __init__(self, master, theme_manager=None, icon_manager=None, icon_name=None, **kwargs):
        super().__init__(master, **kwargs)
        self.theme_manager = theme_manager
        self.icon_manager = icon_manager
        self.icon_name = icon_name
        self._apply_theme()
        self._apply_icon()
        
    def _apply_theme(self):
        """Wendet das Theme an"""
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            self.configure(
                fg_color=theme.get("accent_color", "#4a307d"),
                hover_color=theme.get("hover_color", "#5a3a8d"),
                text_color=theme.get("text_color", "#f2ecfa"),
                border_color=theme.get("border_color", "#2d1b69"),
                border_width=1,
                corner_radius=10,
                font=ctk.CTkFont(family="Consolas", size=12, weight="bold")
            )
            
    def _apply_icon(self):
        """Wendet das Icon an"""
        if self.icon_manager and self.icon_name:
            icon = self.icon_manager.load_icon(self.icon_name, (24, 24))
            if icon:
                self.configure(image=icon)
                # Icon referenzieren um Garbage Collection zu verhindern
                self._icon = icon

class ModernLabel(ctk.CTkLabel):
    """Moderne Label mit Theme-Unterstützung"""
    
    def __init__(self, master, theme_manager=None, font_size=14, font_weight="normal", **kwargs):
        super().__init__(master, **kwargs)
        self.theme_manager = theme_manager
        self.font_size = font_size
        self.font_weight = font_weight
        self._apply_theme()
        
    def _apply_theme(self):
        """Wendet das Theme an"""
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            self.configure(
                text_color=theme.get("text_color", "#f2ecfa"),
                font=ctk.CTkFont(family="Consolas", size=self.font_size, weight=self.font_weight)
            )

class SystemInfoCard(ModernFrame):
    """Moderne System-Info-Karte mit Glasmorphismus"""
    
    def __init__(self, master, theme_manager=None, title="", icon_manager=None, **kwargs):
        super().__init__(master, theme_manager, **kwargs)
        self.theme_manager = theme_manager
        self.icon_manager = icon_manager
        self.title = title
        self.value_label = None
        self.progress_bar = None
        self._setup_card()
        
    def _setup_card(self):
        """Erstellt die Karten-Struktur"""
        # Hauptcontainer
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Icon-Container mit Icon
        icon_frame = ctk.CTkFrame(main_container, fg_color="transparent", width=40, height=40)
        icon_frame.pack(anchor="nw", pady=(0, 10))
        
        # Icon laden und anzeigen
        if self.icon_manager:
            icon_name = self._get_icon_name()
            if icon_name:
                icon = self.icon_manager.load_icon(icon_name, (32, 32))
                if icon:
                    icon_label = ctk.CTkLabel(icon_frame, image=icon, text="")
                    icon_label.pack(expand=True)
                    # Icon referenzieren
                    icon_label._icon = icon
        
        # Titel mit modernem Design
        title_label = ModernLabel(
            main_container, 
            self.theme_manager,
            text=self.title.upper(),
            font_size=12,
            font_weight="bold"
        )
        title_label.pack(anchor="nw", pady=(0, 8))
        
        # Wert-Label mit größerer Schrift
        self.value_label = ModernLabel(
            main_container,
            self.theme_manager,
            text="Lade...",
            font_size=16,
            font_weight="bold"
        )
        self.value_label.pack(anchor="nw", pady=(0, 10))
        
        # Progress-Bar für visuelle Darstellung
        self.progress_bar = ctk.CTkProgressBar(main_container)
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_bar.set(0.0)
        
        # Zusätzliche Info-Label
        self.info_label = ModernLabel(
            main_container,
            self.theme_manager,
            text="",
            font_size=11
        )
        self.info_label.pack(anchor="nw")
        
    def update_value(self, value: str, progress: float = None):
        """Aktualisiert den Wert und Progress"""
        if self.value_label:
            self.value_label.configure(text=value)
            
        if self.progress_bar and progress is not None:
            self.progress_bar.set(progress)
            
    def update_info(self, info: str):
        """Aktualisiert zusätzliche Informationen"""
        if self.info_label:
            self.info_label.configure(text=info)
            
    def _get_icon_name(self) -> str:
        """Gibt den Icon-Namen basierend auf dem Titel zurück"""
        title_lower = self.title.lower()
        if "cpu" in title_lower:
            return "widget_cpu"
        elif "arbeitsspeicher" in title_lower or "ram" in title_lower:
            return "widget_ram"
        elif "festplatte" in title_lower or "disk" in title_lower:
            return "widget_disk"
        elif "system" in title_lower:
            return "widget_system"
        return None

class AnimatedProgressBar(ctk.CTkProgressBar):
    """Animierte Progress-Bar mit modernem Design"""
    
    def __init__(self, master, theme_manager=None, **kwargs):
        super().__init__(master, **kwargs)
        self.theme_manager = theme_manager
        self._apply_theme()
        
    def _apply_theme(self):
        """Wendet das Theme an"""
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            self.configure(
                progress_color=theme.get("accent_color", "#4a307d"),
                border_color=theme.get("border_color", "#2d1b69"),
                border_width=1
            )

class ModernSwitch(ctk.CTkSwitch):
    """Moderner Switch mit Theme-Unterstützung"""
    
    def __init__(self, master, theme_manager=None, **kwargs):
        super().__init__(master, **kwargs)
        self.theme_manager = theme_manager
        self._apply_theme()
        
    def _apply_theme(self):
        """Wendet das Theme an"""
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            self.configure(
                progress_color=theme.get("accent_color", "#4a307d"),
                button_color=theme.get("text_color", "#f2ecfa"),
                button_hover_color=theme.get("hover_color", "#5a3a8d")
            )

class GlassmorphismFrame(ctk.CTkFrame):
    """Glasmorphismus-Frame mit Blur-Effekt"""
    
    def __init__(self, master, theme_manager=None, **kwargs):
        super().__init__(master, **kwargs)
        self.theme_manager = theme_manager
        self._apply_theme()
        
    def _apply_theme(self):
        """Wendet das Theme an"""
        if self.theme_manager:
            theme = self.theme_manager.get_theme()
            self.configure(
                fg_color=theme.get("card_bg", "#1e1e1e"),
                border_color=theme.get("border_color", "#2d1b69"),
                border_width=1,
                corner_radius=15
            )

# Kompatibilitätsklassen für bestehenden Code
class TransparentFrame(ModernFrame):
    """Kompatibilitätsklasse für bestehenden Code"""
    pass

class GlassButton(GradientButton):
    """Kompatibilitätsklasse für bestehenden Code"""
    pass

class ProgressBar(AnimatedProgressBar):
    """Kompatibilitätsklasse für bestehenden Code"""
    pass 