@echo off
chcp 65001 >nul
echo ========================================
echo   MANTENER BACKEND DESPIERTO - RENDER
echo ========================================
echo.
echo Este script mantiene el backend despierto haciendo peticiones
echo cada 14 minutos a la API de Render.
echo.
echo El backend de Render se duerme despues de 15 min de inactividad.
echo.
echo Presiona Ctrl+C para detener.
echo.
echo Logs utiles:
echo   - Backend Health: https://face-swap-app-9dz7.onrender.com/api/health
echo   - Render Dashboard: https://dashboard.render.com
echo.

:loop
echo [%DATE% %TIME%] Enviando heartbeat al backend...

curl -s "https://face-swap-app-9dz7.onrender.com/api/health" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] Backend respondio correctamente
) else (
    echo [ERROR] Backend no respondio - posiblemente en sleep mode o caido
)

echo.
echo Esperando 14 minutos antes del proximo heartbeat...
echo.

timeout /t 840 /nobreak >nul

goto loop
