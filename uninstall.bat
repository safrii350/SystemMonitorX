@echo off
echo SystemMonitorX Uninstaller
echo ==========================

REM Prüfe ob SystemMonitorX installiert ist
set "INSTALL_DIR=%PROGRAMFILES%\SystemMonitorX"
if not exist "%INSTALL_DIR%" (
    echo SystemMonitorX ist nicht installiert.
    pause
    exit /b 0
)

echo Entferne SystemMonitorX...
echo.

REM Lösche Desktop-Verknüpfung
set "DESKTOP=%USERPROFILE%\Desktop"
if exist "%DESKTOP%\SystemMonitorX.lnk" del "%DESKTOP%\SystemMonitorX.lnk"

REM Lösche Startmenü-Verknüpfung
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
if exist "%STARTMENU%\SystemMonitorX" rmdir /S /Q "%STARTMENU%\SystemMonitorX"

REM Lösche Installationsverzeichnis
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR%"

echo.
echo SystemMonitorX wurde erfolgreich entfernt!
echo.
pause
