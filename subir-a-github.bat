@echo off
chcp 65001 >nul
echo ========================================
echo   SUBIR CAMBIOS A GITHUB - FACE SWAP
echo ========================================
echo.
echo Este script subira los cambios al repositorio:
echo   https://github.com/01Jarabo/cambio-de-caras.git
echo.
echo Render se actualizara automaticamente despues del push.
echo.
pause

cd /d "%~dp0"

echo.
echo [1/4] Verificando Git...
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git no esta instalado o no esta en el PATH
    pause
    exit /b 1
)
echo OK: Git encontrado

echo.
echo [2/4] Preparando archivos...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo ejecutar git add
    pause
    exit /b 1
)
echo OK: Archivos preparados

echo.
echo [3/4] Confirmando cambios...
git diff --cached --quiet
if %ERRORLEVEL% EQU 0 (
    echo INFO: No hay cambios nuevos para subir
) else (
    git commit -m "Actualizacion: Face Swap Etico - endpoint face-swap-multi"
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: No se pudo hacer commit
        pause
        exit /b 1
    )
    echo OK: Cambios confirmados
)

echo.
echo [4/4] Subiendo a GitHub...
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo   ERROR: No se pudo subir a GitHub
    echo ========================================
    echo.
    echo Posibles soluciones:
    echo 1. Verifica que tienes permisos en el repositorio
    echo 2. Usa un token de GitHub en lugar de contrasena
    echo    - Ve a: https://github.com/settings/tokens
    echo    - Crea un token con permisos 'repo'
    echo    - Usalo como contrasena al hacer push
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ¡EXITO! Cambios subidos correctamente
echo ========================================
echo.
echo Render deberia actualizarse automaticamente en 2-5 minutos.
echo.
echo Links utiles:
echo   - GitHub: https://github.com/01Jarabo/cambio-de-caras
echo   - Render Dashboard: https://dashboard.render.com
echo   - Backend Health: https://face-swap-app-9dz7.onrender.com/api/health
echo.
echo Para verificar el despliegue:
echo   1. Ve a Render Dashboard
echo   2. Busca tu servicio 'face-swap-app-9dz7'
echo   3. Revisa los logs de despliegue
echo.
pause
