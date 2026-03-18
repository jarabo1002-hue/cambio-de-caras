# ⚡ Inicio Rápido - Face Swap Ético Local

## 🚀 Instalación y Uso en 5 Pasos

### **Paso 1: Instalar Python**
Descarga e instala Python 3.10+:
- https://www.python.org/downloads/

✅ **Verifica:** Abre PowerShell y escribe `python --version`

---

### **Paso 2: Instalar Node.js**
Descarga e instala Node.js 18+:
- https://nodejs.org/

✅ **Verifica:** Abre PowerShell y escribe `node --version`

---

### **Paso 3: Clonar el repositorio**
```bash
git clone https://github.com/jarabo1002-hue/cambio-de-caras.git
cd cambio-de-caras
```

---

### **Paso 4: Instalar dependencias**
```bash
# Dependencias de Python
pip install -r requirements.txt

# Dependencias de Node.js
npm install

# Descargar modelo (~500MB)
python download_model.py
```

---

### **Paso 5: Iniciar**
```bash
# Opción A: Usar script automático (Windows)
iniciar-local.bat

# Opción B: Manual
node server.js
```

**Abrir en el navegador:**
```
http://localhost:3000
```

---

## ✅ ¡Listo!

Ahora puedes:
1. Subir imágenes de origen y destino
2. Confirmar consentimiento
3. Click en "Procesar"
4. ¡Descargar resultado!

---

## 🛠️ Problemas Comunes

| Error | Solución |
|-------|----------|
| `pip no se reconoce` | Python no está en PATH. Reinstala Python y marca "Add to PATH" |
| `npm no se reconoce` | Node.js no está en PATH. Reinstala Node.js |
| `ModuleNotFoundError` | Ejecuta: `pip install -r requirements.txt` |
| `Cannot find module 'express'` | Ejecuta: `npm install` |
| `Model not found` | Ejecuta: `python download_model.py` |
| `Port 3000 in use` | Cierra otros servidores o cambia el puerto en `.env` |

---

## 📞 Más Ayuda

- Lee el `README.md` para documentación completa
- GitHub Issues: https://github.com/jarabo1002-hue/cambio-de-caras/issues

---

**Versión:** Local-only (sin despliegue en la nube)
**Última actualización:** 2026-03-16
