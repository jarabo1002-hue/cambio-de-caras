@echo off
chcp 65001 >nul
echo ========================================
echo   FORZAR REDESPIEGUE EN RENDER
echo ========================================
echo.
echo Este script intentara forzar un redepliegue del backend en Render.
echo.
echo OPCIONES:
echo.
echo 1. IR A RENDER DASHBOARD (Recomendado)
echo    - Ve a: https://dashboard.render.com
echo    - Inicia sesion
echo    - Busca tu servicio "face-swap-ethical-backend" o "face-swap-app-9dz7"
echo    - Click en "Manual Deploy" -" "Deploy latest commit"
echo.
echo 2. USAR LA API DE RENDER (Requiere API Key)
echo    - Consigue tu API Key en: https://dashboard.render.com/u/api
echo    - Ejecuta: render-api-trigger.bat con tu API Key
echo.
echo 3. CAMBIO DE TRUCO (Workaround)
echo    - Haz un pequeno cambio en cualquier archivo
echo    - Subelo a GitHub con: subir-a-github.bat
echo    - Esto deberia triggerar un nuevo despliegue automatico
echo.
pause

echo.
echo Abriendo Render Dashboard...
start https://dashboard.render.com

echo.
echo ========================================
echo   Siguientes pasos:
echo ========================================
echo.
echo 1. Inicia sesion en Render
echo 2. Busca tu servicio de backend
echo 3. Click en "Manual Deploy"
echo 4. Selecciona "Deploy latest commit"
echo 5. Espera 5-10 minutos a que complete
echo.
echo Mientras tanto, puedes monitorear el estado en:
echo   https://caras-frontend.vercel.app/deploy-status.html
echo.
pause
