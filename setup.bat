@echo off
setlocal
set "ROOT=%~dp0"

echo ============================================
echo  Code Plagiarism Detector - Setup
echo ============================================

echo.
echo [1/3] Backend virtual environment...
cd /d "%ROOT%backend"
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists. Skipping.
)

echo.
echo [2/3] Installing backend dependencies...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: backend dependency installation failed.
    goto :end
)

echo.
echo [3/3] Installing frontend dependencies...
cd /d "%ROOT%frontend"
call npm install
if errorlevel 1 (
    echo.
    echo ERROR: frontend dependency installation failed.
    goto :end
)

echo.
echo ============================================
echo  Setup complete!
echo  Next: run.bat (web)  or  run_tauri.bat (desktop)
echo ============================================

:end
echo.
pause
endlocal
