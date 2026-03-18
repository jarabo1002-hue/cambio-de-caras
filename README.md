# 🚀 Face Swap Ético - Versión Local

Aplicación de intercambio de caras con consentimiento ético para uso **LOCAL**.

## ⚠️ Requisitos

- Python 3.10+
- Node.js 18+
- 8GB RAM mínimo (16GB recomendado)
- Espacio en disco: ~1GB (para el modelo)

---

## 📋 Instalación

### **Paso 1: Clonar el repositorio**

```bash
git clone https://github.com/jarabo1002-hue/cambio-de-caras.git
cd cambio-de-caras
```

### **Paso 2: Instalar dependencias de Python**

```bash
pip install -r requirements.txt
```

### **Paso 3: Instalar dependencias de Node.js**

```bash
npm install
```

### **Paso 4: Descargar el modelo**

```bash
python download_model.py
```

Esto descargará `inswapper_128.onnx` (~500MB).

---

## 🚀 Uso

### **Opción A: Usar el script batch (Windows)**

```bash
iniciar-local.bat
```

### **Opción B: Manual**

1. **Iniciar el servidor:**
   ```bash
   node server.js
   ```

2. **Abrir el navegador:**
   ```
   http://localhost:3000
   ```

---

## 📁 Estructura del proyecto

```
cambio-de-caras/
├── server.js           # Servidor backend (Node.js)
├── face_swap.py        # Script de face swap (Python)
├── detect_faces.py     # Detección de caras (Python)
├── download_model.py   # Descarga del modelo
├── requirements.txt    # Dependencias de Python
├── package.json        # Dependencias de Node.js
├── Dockerfile          # (Opcional) Para Docker
├── public/             # Frontend (HTML, CSS, JS)
│   └── index.html
├── uploads/            # (Temporal) Imágenes subidas
└── results/            # (Temporal) Resultados
```

---

## 🔧 Configuración

### **Variables de entorno (opcional)**

Crea un archivo `.env` en la raíz:

```env
PORT=3000
```

---

## ⚙️ Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Verificar estado |
| POST | `/api/face-swap` | Face swap simple (1 cara) |
| POST | `/api/face-swap-multi` | Face swap múltiple |
| POST | `/api/detect-faces` | Detectar caras |
| GET | `/api/terms` | Términos de servicio |

---

## 🛠️ Solución de problemas

### **Error: "No module named 'insightface'"**

```bash
pip install -r requirements.txt
```

### **Error: "Cannot find module 'express'"**

```bash
npm install
```

### **Error: "Model not found"**

```bash
python download_model.py
```

### **Error: "Port 3000 already in use"**

Cambia el puerto en `.env`:
```env
PORT=3001
```

O mata el proceso:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

---

## 📝 Notas importantes

1. **El modelo se descarga la primera vez** (~500MB)
2. **Las imágenes se eliminan automáticamente** después del procesamiento
3. **Requiere conexión a internet** solo para descargar el modelo
4. **Todo se ejecuta en tu máquina** - nada se sube a la nube

---

## 🛡️ Ética

Esta aplicación incluye salvaguardas:
- ✅ Verificación de edad (+18)
- ✅ Términos de servicio
- ✅ Consentimiento requerido
- ✅ Marca de agua en todas las imágenes

**No uses esta aplicación para:**
- ❌ Contenido ilegal o dañino
- ❌ Suplantación de identidad
- ❌ Engañar o manipular a otros

---

## 📄 Licencia

MIT

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero.

---

## 📞 Soporte

- GitHub Issues: https://github.com/jarabo1002-hue/cambio-de-caras/issues

---

**Última actualización:** 2026-03-16
