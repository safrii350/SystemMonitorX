"""
System-Monitoring-Klasse für SystemMonitorX
"""

import psutil
import platform
import threading
import time
from typing import Dict, Any, Callable

class SystemMonitor:
    """Überwacht Systemdaten wie CPU, RAM, Festplatte"""
    
    def __init__(self):
        """Initialisiert den System-Monitor"""
        self.running = False
        self.update_interval = 1.0  # Sekunden
        self.callbacks = []
        self.monitor_thread = None
        
    def start(self):
        """Startet das Monitoring"""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
    def stop(self):
        """Stoppt das Monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
            
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Fügt einen Callback für Datenaktualisierungen hinzu"""
        self.callbacks.append(callback)
        
    def get_system_info(self) -> Dict[str, Any]:
        """Sammelt aktuelle Systemdaten"""
        try:
            # CPU-Auslastung
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # RAM-Informationen
            memory = psutil.virtual_memory()
            
            # Festplatten-Informationen
            disk = psutil.disk_usage('/')
            
            # System-Informationen
            system_info = {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor()
            }
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used,
                    'free': memory.free
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                },
                'system': system_info,
                'timestamp': time.time()
            }
        except Exception as e:
            print(f"Fehler beim Sammeln der Systemdaten: {e}")
            return {}
            
    def _monitor_loop(self):
        """Hauptschleife für kontinuierliches Monitoring"""
        while self.running:
            try:
                data = self.get_system_info()
                if data:
                    # Callbacks aufrufen
                    for callback in self.callbacks:
                        try:
                            callback(data)
                        except Exception as e:
                            print(f"Fehler im Callback: {e}")
                            
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Fehler im Monitor-Loop: {e}")
                time.sleep(self.update_interval) 