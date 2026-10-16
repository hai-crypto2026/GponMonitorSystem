@echo off
title VTVcab GPON Monitor & PRTG 10G Portal
color 0a
echo ======================================================================
echo           VTVCAB GPON & PRTG 10G NETWORK MONITOR SYSTEM
echo ======================================================================
echo.
echo [*] Dang khoi dong Web Server tren port 8765...
echo [*] Local:   http://localhost:8765
echo [*] LAN:     http://192.168.100.71:8765
echo [*] WAN:     http://116.104.90.25:8765
echo.
python server.py
pause
