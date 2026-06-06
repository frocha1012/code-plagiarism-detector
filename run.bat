@echo off
setlocal
set "ROOT=%~dp0"

echo Starting backend (http://localhost:8000)...
start "Backend" /D "%ROOT%backend" cmd /k "call .venv\Scripts\activate.bat && uvicorn app.main:app --reload --reload-dir app"

echo Starting frontend (http://localhost:5173)...
start "Frontend" /D "%ROOT%frontend" cmd /k "npm run dev"

echo Opening browser...
timeout /t 4 /nobreak >nul
start "" http://localhost:5173

echo.
echo Backend and frontend are running in separate windows.
echo Close those windows (or press Ctrl+C in them) to stop.
endlocal
