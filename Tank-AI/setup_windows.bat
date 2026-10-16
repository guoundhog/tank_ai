@echo off
setlocal
cd /d "%~dp0"
py -m venv .venv
if errorlevel 1 (
    echo [ERROR] Cannot create Python virtual environment.
    echo Please install Python 3.11+ with the Windows Python Launcher.
    pause
    exit /b 1
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)
echo Installation complete. Double-click play_windows.bat to play!
pause
