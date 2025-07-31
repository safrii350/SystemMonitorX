"""
Config-Manager für SystemMonitorX
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

class ConfigManager:
    """Verwaltet die JSON-Konfiguration der Anwendung"""
    
    def __init__(self, config_dir: str = "config"):
        """Initialisiert den Config-Manager"""
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / "app_config.json"
        self.widget_config_file = self.config_dir / "widgets_config.json"
        self.default_config = self._get_default_config()
        self.default_widget_config = self._get_default_widget_config()
        
        # Konfiguration laden oder erstellen
        self.config = self._load_config()
        self.widget_config = self._load_widget_config()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Gibt die Standard-Konfiguration zurück"""
        return {
            "app": {
                "name": "SystemMonitorX",
                "version": "1.0.0",
                "theme": "dark",
                "update_interval": 1.0,
                "window_size": "800x600",
                "window_position": "center",
                "transparency": 0.9,
                "always_on_top": False,
                "minimize_to_tray": True
            },
            "dashboard": {
                "show_system_info": True,
                "show_widget_controls": True,
                "show_logging_controls": True,
                "show_graph_controls": True,
                "auto_start_logging": False,
                "log_format": "both"  # csv, json, both
            },
            "monitoring": {
                "cpu_enabled": True,
                "memory_enabled": True,
                "disk_enabled": True,
                "network_enabled": False,
                "gpu_enabled": False,
                "update_frequency": 1.0
            },
            "logging": {
                "enabled": False,
                "auto_start": False,
                "buffer_size": 1000,
                "save_interval": 60,  # Sekunden
                "max_log_files": 10
            },
            "tray": {
                "enabled": True,
                "show_icon": True,
                "update_icon": True,
                "minimize_to_tray": True
            }
        }
        
    def _get_default_widget_config(self) -> Dict[str, Any]:
        """Gibt die Standard-Widget-Konfiguration zurück"""
        return {
            "widgets": {
                "cpu": {
                    "enabled": False,
                    "position": "top_right",
                    "size": "200x100",
                    "transparency": 0.9,
                    "always_on_top": True,
                    "auto_start": False
                },
                "memory": {
                    "enabled": False,
                    "position": "top_right",
                    "size": "200x100",
                    "transparency": 0.9,
                    "always_on_top": True,
                    "auto_start": False
                },
                "disk": {
                    "enabled": False,
                    "position": "top_right",
                    "size": "200x100",
                    "transparency": 0.9,
                    "always_on_top": True,
                    "auto_start": False
                }
            },
            "positions": {
                "top_left": {"x": 20, "y": 20},
                "top_right": {"x": -220, "y": 20},
                "bottom_left": {"x": 20, "y": -120},
                "bottom_right": {"x": -220, "y": -120},
                "center": {"x": "center", "y": "center"}
            },
            "sizes": {
                "small": "150x80",
                "medium": "200x100",
                "large": "250x120"
            }
        }
        
    def _load_config(self) -> Dict[str, Any]:
        """Lädt die Hauptkonfiguration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Standardwerte für fehlende Einträge hinzufügen
                    return self._merge_configs(self.default_config, config)
            else:
                # Standardkonfiguration erstellen
                self._save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")
            return self.default_config
            
    def _load_widget_config(self) -> Dict[str, Any]:
        """Lädt die Widget-Konfiguration"""
        try:
            if self.widget_config_file.exists():
                with open(self.widget_config_file, 'r', encoding='utf-8') as f:
                    widget_config = json.load(f)
                    # Standardwerte für fehlende Einträge hinzufügen
                    return self._merge_configs(self.default_widget_config, widget_config)
            else:
                # Standard-Widget-Konfiguration erstellen
                self._save_widget_config(self.default_widget_config)
                return self.default_widget_config
        except Exception as e:
            print(f"Fehler beim Laden der Widget-Konfiguration: {e}")
            return self.default_widget_config
            
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Führt Standard- und Benutzer-Konfiguration zusammen"""
        result = default.copy()
        
        def merge_dicts(base: Dict[str, Any], update: Dict[str, Any]):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dicts(base[key], value)
                else:
                    base[key] = value
                    
        merge_dicts(result, user)
        return result
        
    def _save_config(self, config: Dict[str, Any]):
        """Speichert die Hauptkonfiguration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
            
    def _save_widget_config(self, widget_config: Dict[str, Any]):
        """Speichert die Widget-Konfiguration"""
        try:
            with open(self.widget_config_file, 'w', encoding='utf-8') as f:
                json.dump(widget_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Widget-Konfiguration: {e}")
            
    def get_config(self, key_path: str = None) -> Any:
        """Gibt einen Konfigurationswert zurück"""
        try:
            if key_path is None:
                return self.config
                
            keys = key_path.split('.')
            value = self.config
            
            for key in keys:
                value = value[key]
                
            return value
        except (KeyError, TypeError):
            return None
            
    def set_config(self, key_path: str, value: Any):
        """Setzt einen Konfigurationswert"""
        try:
            keys = key_path.split('.')
            config = self.config
            
            # Zum letzten Key navigieren
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
                
            # Wert setzen
            config[keys[-1]] = value
            
            # Speichern
            self._save_config(self.config)
            
        except Exception as e:
            print(f"Fehler beim Setzen der Konfiguration: {e}")
            
    def get_widget_config(self, widget_type: str = None) -> Any:
        """Gibt Widget-Konfiguration zurück"""
        try:
            if widget_type is None:
                return self.widget_config
                
            return self.widget_config.get('widgets', {}).get(widget_type, {})
        except Exception as e:
            print(f"Fehler beim Laden der Widget-Konfiguration: {e}")
            return {}
            
    def set_widget_config(self, widget_type: str, config: Dict[str, Any]):
        """Setzt Widget-Konfiguration"""
        try:
            if 'widgets' not in self.widget_config:
                self.widget_config['widgets'] = {}
                
            self.widget_config['widgets'][widget_type] = config
            self._save_widget_config(self.widget_config)
            
        except Exception as e:
            print(f"Fehler beim Setzen der Widget-Konfiguration: {e}")
            
    def save_widget_position(self, widget_type: str, x: int, y: int):
        """Speichert die Position eines Widgets"""
        try:
            widget_config = self.get_widget_config(widget_type)
            widget_config['position'] = f"custom_{x}_{y}"
            widget_config['custom_position'] = {"x": x, "y": y}
            self.set_widget_config(widget_type, widget_config)
            
        except Exception as e:
            print(f"Fehler beim Speichern der Widget-Position: {e}")
            
    def get_widget_position(self, widget_type: str) -> Dict[str, int]:
        """Gibt die gespeicherte Position eines Widgets zurück"""
        try:
            widget_config = self.get_widget_config(widget_type)
            position = widget_config.get('position', 'top_right')
            
            if position.startswith('custom_'):
                # Custom Position
                custom_pos = widget_config.get('custom_position', {})
                return custom_pos
            else:
                # Vordefinierte Position
                positions = self.widget_config.get('positions', {})
                return positions.get(position, {"x": -220, "y": 20})
                
        except Exception as e:
            print(f"Fehler beim Laden der Widget-Position: {e}")
            return {"x": -220, "y": 20}
            
    def set_widget_enabled(self, widget_type: str, enabled: bool):
        """Aktiviert/Deaktiviert ein Widget"""
        try:
            widget_config = self.get_widget_config(widget_type)
            widget_config['enabled'] = enabled
            self.set_widget_config(widget_type, widget_config)
            
        except Exception as e:
            print(f"Fehler beim Setzen des Widget-Status: {e}")
            
    def get_widget_enabled(self, widget_type: str) -> bool:
        """Gibt zurück, ob ein Widget aktiviert ist"""
        try:
            widget_config = self.get_widget_config(widget_type)
            return widget_config.get('enabled', False)
        except Exception as e:
            print(f"Fehler beim Laden des Widget-Status: {e}")
            return False
            
    def get_all_widget_configs(self) -> Dict[str, Dict[str, Any]]:
        """Gibt alle Widget-Konfigurationen zurück"""
        return self.widget_config.get('widgets', {})
        
    def reset_config(self):
        """Setzt die Konfiguration auf Standardwerte zurück"""
        try:
            self.config = self.default_config.copy()
            self.widget_config = self.default_widget_config.copy()
            self._save_config(self.config)
            self._save_widget_config(self.widget_config)
            print("Konfiguration auf Standardwerte zurückgesetzt")
            
        except Exception as e:
            print(f"Fehler beim Zurücksetzen der Konfiguration: {e}")
            
    def export_config(self, file_path: str):
        """Exportiert die Konfiguration"""
        try:
            export_data = {
                "app_config": self.config,
                "widget_config": self.widget_config,
                "export_date": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
                
            print(f"Konfiguration exportiert nach: {file_path}")
            
        except Exception as e:
            print(f"Fehler beim Exportieren der Konfiguration: {e}")
            
    def import_config(self, file_path: str):
        """Importiert eine Konfiguration"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
                
            if 'app_config' in import_data:
                self.config = self._merge_configs(self.default_config, import_data['app_config'])
                self._save_config(self.config)
                
            if 'widget_config' in import_data:
                self.widget_config = self._merge_configs(self.default_widget_config, import_data['widget_config'])
                self._save_widget_config(self.widget_config)
                
            print(f"Konfiguration importiert von: {file_path}")
            
        except Exception as e:
            print(f"Fehler beim Importieren der Konfiguration: {e}") 