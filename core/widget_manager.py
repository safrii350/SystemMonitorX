"""
Widget-Manager für Desktop-Widgets
"""

import threading
from typing import Dict, Any, List
from widgets.desktop_widget import DesktopWidget

class WidgetManager:
    """Verwaltet Desktop-Widgets"""
    
    def __init__(self, config_manager=None):
        """Initialisiert den Widget-Manager"""
        self.config_manager = config_manager
        self.active_widgets: List[DesktopWidget] = []
        self.widget_lock = threading.Lock()
        
    def create_widget(self, widget_type: str, data: Dict[str, Any], parent_window=None) -> DesktopWidget:
        """Erstellt ein neues Desktop-Widget"""
        try:
            widget = DesktopWidget(widget_type, data, parent_window, self.config_manager)
            
            with self.widget_lock:
                self.active_widgets.append(widget)
                
            # Widget als aktiviert markieren
            if self.config_manager:
                self.config_manager.set_widget_enabled(widget_type, True)
                
            print(f"Widget erstellt: {widget_type}")
            return widget
            
        except Exception as e:
            print(f"Fehler beim Erstellen des Widgets {widget_type}: {e}")
            return None
            
    def stop_widget(self, widget: DesktopWidget):
        """Stoppt ein spezifisches Widget"""
        try:
            with self.widget_lock:
                if widget in self.active_widgets:
                    widget.destroy()
                    self.active_widgets.remove(widget)
                    
                    # Widget als deaktiviert markieren
                    if self.config_manager:
                        self.config_manager.set_widget_enabled(widget.widget_type, False)
                        
                    print(f"Widget gestoppt: {widget.widget_type}")
                    
        except Exception as e:
            print(f"Fehler beim Stoppen des Widgets: {e}")
            
    def stop_all_widgets(self):
        """Stoppt alle aktiven Widgets"""
        try:
            with self.widget_lock:
                for widget in self.active_widgets[:]:  # Kopie der Liste verwenden
                    try:
                        widget.destroy()
                    except Exception as e:
                        print(f"Fehler beim Zerstören des Widgets: {e}")
                        
                self.active_widgets.clear()
                print("Alle Widgets gestoppt")
                
        except Exception as e:
            print(f"Fehler beim Stoppen aller Widgets: {e}")
            
    def get_active_widgets(self) -> List[DesktopWidget]:
        """Gibt alle aktiven Widgets zurück"""
        with self.widget_lock:
            return self.active_widgets.copy()
            
    def update_widget_data(self, data: Dict[str, Any]):
        """Aktualisiert alle Widgets mit neuen Daten"""
        try:
            with self.widget_lock:
                for widget in self.active_widgets:
                    try:
                        widget.update_data(data)
                    except Exception as e:
                        print(f"Fehler beim Aktualisieren des Widgets: {e}")
                        
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Widget-Daten: {e}")
            
    def cleanup(self):
        """Bereinigt alle Ressourcen"""
        self.stop_all_widgets() 