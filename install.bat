@echo off
echo SystemMonitorX Installer
echo ========================

REM Prüfe ob .exe existiert
if not exist "SystemMonitorX.exe" (
    echo Fehler: SystemMonitorX.exe nicht gefunden!
    pause
    exit /b 1
)

REM Erstelle Programm-Ordner
set "INSTALL_DIR=%PROGRAMFILES%\SystemMonitorX"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Kopiere Dateien
echo Installiere SystemMonitorX...
copy "SystemMonitorX.exe" "%INSTALL_DIR%\"
if exist "config" xcopy "config" "%INSTALL_DIR%\config\" /E /I /Y
if exist "assets" xcopy "assets" "%INSTALL_DIR%\assets\" /E /I /Y
if exist "README.md" copy "README.md" "%INSTALL_DIR%\"

REM Erstelle Desktop-Verknüpfung
echo Erstelle Desktop-Verknüpfung...
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\SystemMonitorX.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\SystemMonitorX.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

REM Erstelle Startmenü-Verknüpfung
echo Erstelle Startmenü-Verknüpfung...
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if not exist "%STARTMENU%\SystemMonitorX" mkdir "%STARTMENU%\SystemMonitorX"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\SystemMonitorX\SystemMonitorX.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\SystemMonitorX.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

echo.
echo Installation abgeschlossen!
echo SystemMonitorX wurde installiert in: %INSTALL_DIR%
echo Desktop-Verknüpfung erstellt
echo Startmenü-Verknüpfung erstellt
echo.
pause
