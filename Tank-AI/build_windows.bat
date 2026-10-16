@echo off
setlocal
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe
if not exist "%PY%" (
    echo [ERROR] Python environment not found.
    echo First run setup_windows.bat
    pause
    exit /b 1
)
"%PY%" -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)
"%PY%" -m PyInstaller --noconfirm --clean --onedir --windowed --name TankAI main.py
if errorlevel 1 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)
echo.
echo SUCCESS: dist\TankAI\TankAI.exe
echo Zip the WHOLE dist\TankAI folder for GitHub Releases.
pause
