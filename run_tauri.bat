@echo off
setlocal
set "ROOT=%~dp0"

echo Starting backend (http://localhost:8000)...
start "Backend" /D "%ROOT%backend" cmd /k "call .venv\Scripts\activate.bat && uvicorn app.main:app --reload --reload-dir app"

echo Starting Tauri desktop app...
start "Tauri" /D "%ROOT%frontend" cmd /k "npm run tauri:dev"

echo.
echo Backend is running in a separate window.
echo The Tauri desktop window will open after it finishes building.
endlocal
