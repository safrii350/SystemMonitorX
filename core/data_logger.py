"""
Data-Logger für SystemMonitorX
"""

import csv
import json
import os
import time
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

class DataLogger:
    """Loggt Systemdaten in CSV und JSON Format"""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialisiert den Data-Logger"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.csv_file = None
        self.json_file = None
        self.logging_enabled = False
        self.data_buffer = []
        self.max_buffer_size = 1000  # Maximale Anzahl Einträge im Buffer
        
    def start_logging(self, format_type: str = "csv"):
        """Startet das Logging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format_type == "csv":
                self.csv_file = self.log_dir / f"system_data_{timestamp}.csv"
                self._create_csv_header()
            elif format_type == "json":
                self.json_file = self.log_dir / f"system_data_{timestamp}.json"
                self._create_json_header()
            else:
                # Beide Formate
                self.csv_file = self.log_dir / f"system_data_{timestamp}.csv"
                self.json_file = self.log_dir / f"system_data_{timestamp}.json"
                self._create_csv_header()
                self._create_json_header()
                
            self.logging_enabled = True
            print(f"Logging gestartet: {format_type.upper()}")
            
        except Exception as e:
            print(f"Fehler beim Starten des Loggings: {e}")
            
    def stop_logging(self):
        """Stoppt das Logging"""
        try:
            self.logging_enabled = False
            
            # Verbleibende Daten schreiben
            if self.data_buffer:
                self._flush_buffer()
                
            print("Logging gestoppt")
            
        except Exception as e:
            print(f"Fehler beim Stoppen des Loggings: {e}")
            
    def log_data(self, data: Dict[str, Any]):
        """Loggt Systemdaten"""
        if not self.logging_enabled:
            return
            
        try:
            # Timestamp hinzufügen
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': data.get('cpu', {}).get('percent', 0),
                'cpu_count': data.get('cpu', {}).get('count', 0),
                'memory_percent': data.get('memory', {}).get('percent', 0),
                'memory_used_gb': data.get('memory', {}).get('used', 0) / (1024**3),
                'memory_total_gb': data.get('memory', {}).get('total', 0) / (1024**3),
                'disk_percent': data.get('disk', {}).get('percent', 0),
                'disk_used_gb': data.get('disk', {}).get('used', 0) / (1024**3),
                'disk_total_gb': data.get('disk', {}).get('total', 0) / (1024**3),
                'platform': data.get('system', {}).get('platform', ''),
                'machine': data.get('system', {}).get('machine', '')
            }
            
            # Daten zum Buffer hinzufügen
            self.data_buffer.append(log_entry)
            
            # Buffer schreiben wenn voll
            if len(self.data_buffer) >= self.max_buffer_size:
                self._flush_buffer()
                
        except Exception as e:
            print(f"Fehler beim Loggen der Daten: {e}")
            
    def _create_csv_header(self):
        """Erstellt CSV-Header"""
        if self.csv_file:
            fieldnames = [
                'timestamp', 'cpu_percent', 'cpu_count', 'memory_percent',
                'memory_used_gb', 'memory_total_gb', 'disk_percent',
                'disk_used_gb', 'disk_total_gb', 'platform', 'machine'
            ]
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
    def _create_json_header(self):
        """Erstellt JSON-Header"""
        if self.json_file:
            header = {
                'metadata': {
                    'created': datetime.now().isoformat(),
                    'version': '1.0',
                    'description': 'SystemMonitorX Log Data'
                },
                'data': []
            }
            
            with open(self.json_file, 'w', encoding='utf-8') as jsonfile:
                json.dump(header, jsonfile, indent=2)
                
    def _flush_buffer(self):
        """Schreibt Buffer-Daten in Dateien"""
        if not self.data_buffer:
            return
            
        try:
            # CSV schreiben
            if self.csv_file:
                fieldnames = [
                    'timestamp', 'cpu_percent', 'cpu_count', 'memory_percent',
                    'memory_used_gb', 'memory_total_gb', 'disk_percent',
                    'disk_used_gb', 'disk_total_gb', 'platform', 'machine'
                ]
                
                with open(self.csv_file, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerows(self.data_buffer)
                    
            # JSON schreiben
            if self.json_file:
                # JSON-Datei lesen und erweitern
                try:
                    with open(self.json_file, 'r', encoding='utf-8') as jsonfile:
                        json_data = json.load(jsonfile)
                except FileNotFoundError:
                    json_data = {
                        'metadata': {
                            'created': datetime.now().isoformat(),
                            'version': '1.0',
                            'description': 'SystemMonitorX Log Data'
                        },
                        'data': []
                    }
                
                # Neue Daten hinzufügen
                json_data['data'].extend(self.data_buffer)
                
                # Zurück schreiben
                with open(self.json_file, 'w', encoding='utf-8') as jsonfile:
                    json.dump(json_data, jsonfile, indent=2)
                    
            # Buffer leeren
            self.data_buffer.clear()
            
        except Exception as e:
            print(f"Fehler beim Schreiben der Log-Daten: {e}")
            
    def get_log_files(self) -> List[Path]:
        """Gibt alle Log-Dateien zurück"""
        return list(self.log_dir.glob("*.csv")) + list(self.log_dir.glob("*.json"))
        
    def get_latest_log_data(self, format_type: str = "csv") -> List[Dict[str, Any]]:
        """Gibt die neuesten Log-Daten zurück"""
        try:
            if format_type == "csv":
                files = list(self.log_dir.glob("*.csv"))
            else:
                files = list(self.log_dir.glob("*.json"))
                
            if not files:
                return []
                
            # Neueste Datei
            latest_file = max(files, key=os.path.getctime)
            
            if format_type == "csv":
                return self._read_csv_data(latest_file)
            else:
                return self._read_json_data(latest_file)
                
        except Exception as e:
            print(f"Fehler beim Lesen der Log-Daten: {e}")
            return []
            
    def _read_csv_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """Liest CSV-Daten"""
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Fehler beim Lesen der CSV-Datei: {e}")
        return data
        
    def _read_json_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """Liest JSON-Daten"""
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                json_data = json.load(jsonfile)
                return json_data.get('data', [])
        except Exception as e:
            print(f"Fehler beim Lesen der JSON-Datei: {e}")
            return [] 