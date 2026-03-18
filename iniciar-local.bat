@echo off
chcp 65001 >nul
echo ========================================
echo   INICIAR FACE SWAP ÉTICO - LOCAL
echo ========================================
echo.
echo Este script iniciara el servidor en tu maquina local.
echo.
echo Requisitos:
echo   - Python 3.10+ instalado
echo   - Node.js 18+ instalado
echo   - Dependencias instaladas (pip install -r requirements.txt)
echo   - npm install ejecutado
echo   - Modelo descargado (python download_model.py)
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Verificando Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Instala Python 3.10+ desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK: Python encontrado

echo.
echo [2/3] Verificando Node.js...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js no esta instalado
    echo Instala Node.js 18+ desde: https://nodejs.org/
    pause
    exit /b 1
)
echo OK: Node.js encontrado

echo.
echo [3/3] Verificando modelo...
if not exist "inswapper_128.onnx" (
    echo.
    echo El modelo no existe. Descargando...
    python download_model.py
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: No se pudo descargar el modelo
        pause
        exit /b 1
    )
) else (
    echo OK: Modelo encontrado
)

echo.
echo ========================================
echo   INICIANDO SERVIDOR...
echo ========================================
echo.
echo Servidor disponible en: http://localhost:3000
echo.
echo Presiona CTRL+C para detener el servidor.
echo.

node server.js
