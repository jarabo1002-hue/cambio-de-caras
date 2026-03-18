#!/bin/bash

# ========================================
#   INICIAR FACE SWAP ÉTICO - MAC/LINUX
# ========================================

echo "========================================"
echo "   FACE SWAP ÉTICO - Inicio Local"
echo "========================================"
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Verificar Python
echo "[1/4] Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python no está instalado"
    echo "Instala Python 3.10+ desde: https://www.python.org/downloads/"
    exit 1
fi
echo "OK: Python encontrado ($($PYTHON_CMD --version))"

# Verificar Node.js
echo ""
echo "[2/4] Verificando Node.js..."
if command -v node &> /dev/null; then
    echo "OK: Node.js encontrado ($(node --version))"
else
    echo "ERROR: Node.js no está instalado"
    echo "Instala Node.js 18+ desde: https://nodejs.org/"
    exit 1
fi

# Verificar modelo
echo ""
echo "[3/4] Verificando modelo..."
if [ ! -f "inswapper_128.onnx" ]; then
    echo ""
    echo "El modelo no existe. Descargando..."
    $PYTHON_CMD download_model.py
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo descargar el modelo"
        exit 1
    fi
else
    echo "OK: Modelo encontrado"
fi

# Verificar dependencias
echo ""
echo "[4/4] Verificando dependencias..."
if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias de Node.js..."
    npm install
fi

echo ""
echo "========================================"
echo "   INICIANDO SERVIDOR..."
echo "========================================"
echo ""
echo "Servidor disponible en: http://localhost:3000"
echo ""
echo "Presiona CTRL+C para detener el servidor."
echo ""

node server.js
