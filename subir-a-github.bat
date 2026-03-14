@echo off
echo ========================================
echo   SUBIR CAMBIOS A GITHUB
echo ========================================
echo.
echo Este script subira los cambios al repositorio:
echo   https://github.com/01Jarabo/cambio-de-caras.git
echo.
echo IMPORTANTE: Necesitas tener permisos en el repositorio.
echo.
echo PASOS:
echo 1. Asegurate de tener permisos en el repositorio de GitHub
echo 2. Cuando se solicite, introduce tu usuario y contrasena de GitHub
echo    (o usa un token de acceso personal)
echo.
pause

cd /d "%~dp0"

echo.
echo Subiendo cambios a GitHub...
echo.

git add .
git commit -m "Actualizacion: Face Swap Etico con multiples caras"
git push -u origin main

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo   ¡EXITO! Cambios subidos correctamente
    echo   Visita: https://github.com/01Jarabo/cambio-de-caras
) else (
    echo   ERROR: No se pudieron subir los cambios
    echo.
    echo   Posibles soluciones:
    echo   1. Verifica que tienes permisos en el repositorio
    echo   2. Usa un token de GitHub en lugar de contrasena
    echo   3. Crea tu propio repositorio en GitHub
)
echo ========================================
echo.
pause
