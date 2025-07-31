@echo off
echo SystemMonitorX Autostart Setup
echo ===============================

REM Prüfe ob SystemMonitorX installiert ist
set "INSTALL_DIR=%PROGRAMFILES%\SystemMonitorX"
if not exist "%INSTALL_DIR%\SystemMonitorX.exe" (
    echo Fehler: SystemMonitorX ist nicht installiert!
    pause
    exit /b 1
)

REM Erstelle Autostart-Verknüpfung
echo Erstelle Autostart-Verknüpfung...
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP%\SystemMonitorX.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\SystemMonitorX.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"

echo.
echo Autostart-Verknüpfung erstellt!
echo SystemMonitorX wird beim nächsten Systemstart automatisch gestartet.
echo.
pause
