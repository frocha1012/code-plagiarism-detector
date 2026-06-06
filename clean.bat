@echo off
setlocal
set "ROOT=%~dp0"

echo ============================================
echo  Code Plagiarism Detector - Clean
echo ============================================

echo.
echo Removing Python cache (__pycache__, *.pyc)...
for /d /r "%ROOT%backend" %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)
del /s /q "%ROOT%backend\*.pyc" >nul 2>&1

if exist "%ROOT%backend\.pytest_cache" (
    echo Removing pytest cache...
    rd /s /q "%ROOT%backend\.pytest_cache"
)

echo.
set /p CONFIRM="Also clear uploaded files in backend\uploads? (y/N): "
if /i "%CONFIRM%"=="y" (
    echo Clearing uploads...
    for /d %%d in ("%ROOT%backend\uploads\*") do rd /s /q "%%d"
    echo Uploads cleared (.gitkeep preserved).
) else (
    echo Skipped clearing uploads.
)

echo.
echo Cleanup complete.
echo.
pause
endlocal
