#!/usr/bin/env python3
"""
Build-Script für SystemMonitorX .exe
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def create_spec_file():
    """Erstellt eine optimierte .spec Datei für pyinstaller"""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('assets', 'assets'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'psutil',
        'pystray',
        'PIL',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure',
        'matplotlib.dates',
        'numpy',
        'tkinter',
        'tkinter.ttk',
        'threading',
        'json',
        'csv',
        'datetime',
        'pathlib',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter.test',
        'matplotlib.tests',
        'numpy.tests',
        'PIL.tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SystemMonitorX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Keine Konsole für GUI-App
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/app_icon.ico' if os.path.exists('assets/icons/app_icon.ico') else None,
    version_file=None,
)
'''
    
    with open('SystemMonitorX.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ SystemMonitorX.spec Datei erstellt")

def install_pyinstaller():
    """Installiert pyinstaller falls nicht vorhanden"""
    try:
        import PyInstaller
        print("✅ PyInstaller bereits installiert")
    except ImportError:
        print("📦 Installiere PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller>=5.13.0'])
        print("✅ PyInstaller installiert")

def clean_build_dirs():
    """Bereinigt alte Build-Verzeichnisse"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                print(f"🧹 Lösche {dir_name}/...")
                shutil.rmtree(dir_name)
            except PermissionError:
                print(f"⚠️ Konnte {dir_name}/ nicht löschen (Datei in Verwendung)")
                continue
    
    # .spec Dateien löschen (außer der aktuellen)
    for file in Path('.').glob('*.spec'):
        if file.name != 'SystemMonitorX.spec':
            try:
                file.unlink()
                print(f"🧹 Lösche {file.name}")
            except PermissionError:
                print(f"⚠️ Konnte {file.name} nicht löschen")
                continue

def build_executable():
    """Baut die .exe Datei"""
    print("🔨 Baue SystemMonitorX.exe...")
    
    try:
        # PyInstaller mit .spec Datei ausführen
        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller',
            'SystemMonitorX.spec',
            '--clean',
            '--noconfirm'
        ])
        
        print("✅ Build erfolgreich!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build fehlgeschlagen: {e}")
        return False
    
    return True

def create_distribution():
    """Erstellt ein Distribution-Paket"""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ dist/ Verzeichnis nicht gefunden")
        return False
    
    # Distribution-Ordner erstellen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dist_name = f"SystemMonitorX_v1.0.0_{timestamp}"
    dist_path = Path(dist_name)
    
    if dist_path.exists():
        shutil.rmtree(dist_path)
    
    # Dateien kopieren
    shutil.copytree('dist', dist_path)
    
    # Zusätzliche Dateien hinzufügen
    additional_files = [
        'README.md',
        'requirements.txt',
        'LICENSE' if os.path.exists('LICENSE') else None
    ]
    
    for file in additional_files:
        if file and os.path.exists(file):
            shutil.copy2(file, dist_path)
    
    # ZIP erstellen
    shutil.make_archive(dist_name, 'zip', dist_path)
    
    # Temporären Ordner löschen
    shutil.rmtree(dist_path)
    
    print(f"✅ Distribution erstellt: {dist_name}.zip")
    return True

def create_installer_script():
    """Erstellt ein Installer-Script"""
    
    installer_content = '''@echo off
echo SystemMonitorX Installer
echo ========================

REM Prüfe ob .exe existiert
if not exist "SystemMonitorX.exe" (
    echo Fehler: SystemMonitorX.exe nicht gefunden!
    pause
    exit /b 1
)

REM Erstelle Programm-Ordner
set "INSTALL_DIR=%PROGRAMFILES%\\SystemMonitorX"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Kopiere Dateien
echo Installiere SystemMonitorX...
copy "SystemMonitorX.exe" "%INSTALL_DIR%\\"
if exist "config" xcopy "config" "%INSTALL_DIR%\\config\\" /E /I /Y
if exist "assets" xcopy "assets" "%INSTALL_DIR%\\assets\\" /E /I /Y
if exist "README.md" copy "README.md" "%INSTALL_DIR%\\"

REM Erstelle Desktop-Verknüpfung
echo Erstelle Desktop-Verknüpfung...
set "DESKTOP=%USERPROFILE%\\Desktop"
set "SHORTCUT=%DESKTOP%\\SystemMonitorX.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\SystemMonitorX.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

REM Erstelle Startmenü-Verknüpfung
echo Erstelle Startmenü-Verknüpfung...
set "STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
if not exist "%STARTMENU%\\SystemMonitorX" mkdir "%STARTMENU%\\SystemMonitorX"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\\SystemMonitorX\\SystemMonitorX.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\SystemMonitorX.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

echo.
echo Installation abgeschlossen!
echo SystemMonitorX wurde installiert in: %INSTALL_DIR%
echo Desktop-Verknüpfung erstellt
echo Startmenü-Verknüpfung erstellt
echo.
pause
'''
    
    with open('install.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("✅ install.bat erstellt")

def create_uninstaller_script():
    """Erstellt ein Uninstaller-Script"""
    
    uninstaller_content = '''@echo off
echo SystemMonitorX Uninstaller
echo ==========================

REM Prüfe ob SystemMonitorX installiert ist
set "INSTALL_DIR=%PROGRAMFILES%\\SystemMonitorX"
if not exist "%INSTALL_DIR%" (
    echo SystemMonitorX ist nicht installiert.
    pause
    exit /b 0
)

echo Entferne SystemMonitorX...
echo.

REM Lösche Desktop-Verknüpfung
set "DESKTOP=%USERPROFILE%\\Desktop"
if exist "%DESKTOP%\\SystemMonitorX.lnk" del "%DESKTOP%\\SystemMonitorX.lnk"

REM Lösche Startmenü-Verknüpfung
set "STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
if exist "%STARTMENU%\\SystemMonitorX" rmdir /S /Q "%STARTMENU%\\SystemMonitorX"

REM Lösche Installationsverzeichnis
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR%"

echo.
echo SystemMonitorX wurde erfolgreich entfernt!
echo.
pause
'''
    
    with open('uninstall.bat', 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    
    print("✅ uninstall.bat erstellt")

def create_autostart_script():
    """Erstellt ein Autostart-Script"""
    
    autostart_content = '''@echo off
echo SystemMonitorX Autostart Setup
echo ===============================

REM Prüfe ob SystemMonitorX installiert ist
set "INSTALL_DIR=%PROGRAMFILES%\\SystemMonitorX"
if not exist "%INSTALL_DIR%\\SystemMonitorX.exe" (
    echo Fehler: SystemMonitorX ist nicht installiert!
    pause
    exit /b 1
)

REM Erstelle Autostart-Verknüpfung
echo Erstelle Autostart-Verknüpfung...
set "STARTUP=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
set "SHORTCUT=%STARTUP%\\SystemMonitorX.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\SystemMonitorX.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

echo.
echo Autostart-Verknüpfung erstellt!
echo SystemMonitorX wird beim nächsten Systemstart automatisch gestartet.
echo.
pause
'''
    
    with open('setup_autostart.bat', 'w', encoding='utf-8') as f:
        f.write(autostart_content)
    
    print("✅ setup_autostart.bat erstellt")

def main():
    """Hauptfunktion für den Build-Prozess"""
    print("🚀 SystemMonitorX Build-Prozess")
    print("=" * 40)
    
    # 1. PyInstaller installieren
    install_pyinstaller()
    
    # 2. Alte Build-Dateien bereinigen
    clean_build_dirs()
    
    # 3. .spec Datei erstellen
    create_spec_file()
    
    # 4. .exe bauen
    if not build_executable():
        print("❌ Build fehlgeschlagen!")
        return False
    
    # 5. Distribution erstellen
    create_distribution()
    
    # 6. Installer-Scripts erstellen
    create_installer_script()
    create_uninstaller_script()
    create_autostart_script()
    
    print("\n🎉 Build-Prozess abgeschlossen!")
    print("\n📁 Erstellte Dateien:")
    print("   - dist/SystemMonitorX.exe")
    print("   - SystemMonitorX_v1.0.0_*.zip")
    print("   - install.bat")
    print("   - uninstall.bat")
    print("   - setup_autostart.bat")
    
    return True

if __name__ == "__main__":
    main() 