"""
Erweiterte Tray-Icon-Generierung für SystemMonitorX
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_detailed_tray_icon(cpu_percent: float = 0, memory_percent: float = 0) -> Image.Image:
    """Erstellt ein detailliertes Tray-Icon mit CPU und RAM Informationen"""
    
    # Icon-Größe
    icon_size = 32
    
    # Neues Bild erstellen
    image = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Farbe basierend auf CPU-Auslastung
    if cpu_percent < 50:
        cpu_color = (0, 255, 0)  # Grün
    elif cpu_percent < 80:
        cpu_color = (255, 255, 0)  # Gelb
    else:
        cpu_color = (255, 0, 0)  # Rot
        
    # Farbe basierend auf RAM-Auslastung
    if memory_percent < 70:
        mem_color = (0, 150, 255)  # Blau
    elif memory_percent < 90:
        mem_color = (255, 165, 0)  # Orange
    else:
        mem_color = (255, 0, 0)  # Rot
    
    # Monitor-Rahmen
    draw.rectangle([4, 4, 27, 20], outline=(100, 100, 100), width=2)
    
    # CPU-Balken (oben)
    cpu_height = max(2, int((cpu_percent / 100) * 6))
    draw.rectangle([6, 18-cpu_height, 25, 18], fill=cpu_color)
    
    # RAM-Balken (unten)
    mem_height = max(2, int((memory_percent / 100) * 6))
    draw.rectangle([6, 26-mem_height, 25, 26], fill=mem_color)
    
    # Standfuß
    draw.rectangle([12, 20, 19, 28], fill=(100, 100, 100))
    
    return image

def create_simple_tray_icon() -> Image.Image:
    """Erstellt ein einfaches Tray-Icon"""
    
    icon_size = 16
    image = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Monitor-Symbol
    draw.rectangle([2, 2, 13, 11], outline=(0, 255, 0), width=1)
    draw.rectangle([3, 8, 12, 10], fill=(0, 255, 0))
    draw.rectangle([6, 11, 9, 13], fill=(0, 255, 0))
    
    return image 