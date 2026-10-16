@echo off
title Push GponMonitorSystem to GitHub
cd /d "%~dp0"
echo ===================================================
echo   DANG DAY TOAN BO DU AN LEN GITHUB (hai-crypto2026)
echo ===================================================
echo Repo: https://github.com/hai-crypto2026/GponMonitorSystem.git
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ===================================================
    echo [THANH CONG] Du an da duoc day len GitHub!
    echo Link repo: https://github.com/hai-crypto2026/GponMonitorSystem
    echo ===================================================
) else (
    echo ===================================================
    echo [LUU Y] Neu chua tao repo tren web GitHub, vui long:
    echo 1. Mo trinh duyet vao: https://github.com/new
    echo 2. Dat ten Repository name: GponMonitorSystem
    echo 3. Bam "Create repository" roi chay lai file bat nay!
    echo ===================================================
)
pause
