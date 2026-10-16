@echo off
title Auto Push GponMonitorSystem to GitHub
cd /d "c:\Users\ByActive\Desktop\Jb\GponMonitorSystem"

echo ===================================================
echo   DANG DONG BO VA DAY CODE LEN GITHUB
echo ===================================================
echo Repo: https://github.com/hai-crypto2026/GponMonitorSystem
echo.

:: 1. Kiem tra file thay doi
git status -s

:: 2. Them tat ca file da sua
git add .

:: 3. Nhap ghi chu commit (neu Enter bo qua se tu dong dat ghi chu mac dinh theo gio)
echo.
set "commit_msg="
set /p commit_msg="Nhap noi dung thay doi (hoac Enter de tu dong): "

if "%commit_msg%"=="" (
    for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set mydate=%%a-%%b-%%c
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a:%%b
    set commit_msg=update: cap nhat ma nguon luc %mydate% %mytime%
)

:: 4. Commit thay doi
git commit -m "%commit_msg%"

:: 5. Day len GitHub
echo.
echo Dang day len GitHub (origin main)...
git push origin main

echo.
if %errorlevel% equ 0 (
    echo ===================================================
    echo [THANH CONG] Toan bo thay doi da duoc day len GitHub!
    echo Link repo: https://github.com/hai-crypto2026/GponMonitorSystem
    echo ===================================================
) else (
    echo ===================================================
    echo [LOI] Co loi xay ra khi push, vui long kiem tra ket noi mang.
    echo ===================================================
)

echo.
pause
