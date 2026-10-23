@echo off
cd /d "%~dp0"
echo =========================================================
echo LR4 AR.js - local testing on your computer
 echo.
echo Open in browser: http://localhost:8000/
echo 3D preview:      http://localhost:8000/preview.html
echo Camera on a PHONE requires HTTPS (for example GitHub Pages).
echo Stop server: Ctrl+C
 echo.
echo =========================================================
where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3 serve.py
) else (
    python serve.py
)
pause
