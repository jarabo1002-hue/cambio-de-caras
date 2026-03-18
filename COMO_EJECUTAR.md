# 🚀 Guía Completa - Ejecución Local

## ⚡ Inicio Rápido

### **Windows**
```bash
iniciar-local.bat
```

### **Mac/Linux**
```bash
chmod +x iniciar.sh
./iniciar.sh
```

### **Docker (Cualquier SO)**
```bash
docker-compose up --build
```

---

## 📋 Métodos Disponibles

### **Método 1: Script Automático (Recomendado)**

#### Windows:
```bash
cd g:\curros\qwen\face-swap-ethical
iniciar-local.bat
```

#### Mac/Linux:
```bash
cd /path/to/cambio-de-caras
chmod +x iniciar.sh
./iniciar.sh
```

**✅ Ventajas:**
- Un solo comando
- Verifica dependencias automáticamente
- Descarga el modelo si falta

---

### **Método 2: Docker (Aislado)**

#### Requisito: Tener Docker instalado

**Paso 1: Construir y ejecutar**
```bash
cd g:\curros\qwen\face-swap-ethical
docker-compose up --build
```

**Paso 2: Detener**
```bash
docker-compose down
```

**Paso 3: Limpiar todo (opcional)**
```bash
docker-compose down -v --rmi all
```

**✅ Ventajas:**
- Entorno completamente aislado
- Sin instalar Python ni Node.js
- Funciona igual en todos los sistemas

---

### **Método 3: Manual (Desarrolladores)**

#### Paso 1: Entorno virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Paso 2: Instalar dependencias

```bash
# Python
pip install -r requirements.txt

# Node.js
npm install
```

#### Paso 3: Descargar modelo

```bash
python download_model.py
```

#### Paso 4: Iniciar servidor

```bash
node server.js
```

---

## 🔧 Comandos Útiles

### **Verificar instalación**

```bash
# Python
python --version  # Debe ser 3.10+

# Node.js
node --version  # Debe ser 18+

# npm
npm --version
```

### **Limpiar archivos temporales**

```bash
# Windows
del /Q uploads\* results\*

# Mac/Linux
rm -f uploads/* results/*
```

### **Reinstalar dependencias**

```bash
# Python
pip install -r requirements.txt --force-reinstall

# Node.js
rm -rf node_modules package-lock.json
npm install
```

---

## 🛠️ Solución de Problemas

### **Error: "Port 3000 already in use"**

**Windows:**
```bash
# Encontrar proceso
netstat -ano | findstr :3000

# Matar proceso (reemplaza PID con el número)
taskkill /PID 12345 /F
```

**Mac/Linux:**
```bash
# Encontrar y matar proceso
lsof -ti:3000 | xargs kill -9
```

---

### **Error: "No module named 'insightface'"**

```bash
pip install -r requirements.txt --force-reinstall
```

---

### **Error: "Cannot find module 'express'"**

```bash
rm -rf node_modules package-lock.json
npm install
```

---

### **Error: "Model not found"**

```bash
python download_model.py
```

---

### **Error: Docker - "Cannot start service"**

```bash
# Reiniciar Docker
docker-compose down
docker system prune -a
docker-compose up --build
```

---

### **Error: Memoria insuficiente**

El modelo requiere ~1GB RAM. Cierra otras aplicaciones o usa Docker con límites:

```bash
# docker-compose.yml ya tiene límites configurados (2GB máx)
```

---

## 📊 Comparación de Métodos

| Método | Velocidad | Facilidad | Aislamiento | RAM |
|--------|-----------|-----------|-------------|-----|
| **Script (.bat/.sh)** | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | ~1.5GB |
| **Docker** | ⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ~2GB |
| **Manual** | ⚡⚡⚡ | ⭐⭐ | ❌ | ~1.5GB |

---

## 🎯 Recomendaciones

| Tu Caso | Método |
|---------|--------|
| **Usuario Windows** | `iniciar-local.bat` |
| **Usuario Mac/Linux** | `./iniciar.sh` |
| **Problemas de dependencias** | Docker |
| **Desarrollador** | Manual con venv |
| **Compartir con equipo** | Docker |

---

## 📞 Más Ayuda

- **README.md:** Documentación completa
- **GitHub Issues:** https://github.com/jarabo1002-hue/cambio-de-caras/issues

---

**Versión:** Local-only
**Última actualización:** 2026-03-16
