# 🚨 SOLUCIÓN URGENTE - Backend no se despliega en Render

## Problema Actual
El endpoint `/api/face-swap-multi` no está disponible en Render aunque el código está en GitHub.

**Estado:**
- ✅ Código en GitHub: https://github.com/jarabo1002-hue/cambio-de-caras (27 commits)
- ✅ Backend responde: https://face-swap-app-9dz7.onrender.com/api/health
- ❌ Endpoint multi: 404 Not Found (código antiguo desplegado)

---

## ✅ SOLUCIÓN RÁPIDA (5 minutos)

### Paso 1: Ir a Render Dashboard
1. Abre: https://dashboard.render.com
2. Inicia sesión con tu cuenta de GitHub

### Paso 2: Buscar tu servicio
1. En la lista de servicios, busca: `face-swap-ethical-backend` o `face-swap-app-9dz7`
2. Click en el servicio

### Paso 3: Forzar despliegue manual
1. En la página del servicio, busca el botón **"Manual"** o **"Deploy"**
2. Click en **"Deploy latest commit"**
3. Esto forzará a Render a usar el código más reciente de GitHub

### Paso 4: Monitorear logs
1. Click en **"Logs"** en el menú lateral
2. Verás el despliegue en tiempo real
3. Debería decir algo como:
   ```
   Deploying...
   Building...
   Installing dependencies...
   Starting server...
   Deployed successfully!
   ```

### Paso 5: Verificar
Una vez que diga "Deployed successfully!":
1. Ve a: https://face-swap-app-9dz7.onrender.com/api/health
2. Debería responder: `{"status":"ok","version":"1.0.0"}`
3. Ve a: https://face-swap-app-9dz7.onrender.com/api/face-swap-multi
4. Debería responder: `405 Method Not Allowed` (esto es CORRECTO porque requiere POST)

---

## 🔧 SI EL DESPLIEGUE FALLA

### Error Común 1: "Build failed"
**Causa:** Error al instalar dependencias

**Solución:**
1. En los logs, busca la línea que dice "error"
2. Verifica que `requirements.txt` y `package.json` estén correctos
3. Revisa que `download_model.py` no esté fallando

### Error Común 2: "Health check failed"
**Causa:** El servidor no inicia correctamente

**Solución:**
1. Revisa los logs después de "Starting server"
2. Busca errores de Python o Node.js
3. Verifica que `server.js` no tenga errores de sintaxis

### Error Común 3: "Timeout"
**Causa:** El despliegue tarda demasiado

**Solución:**
1. El modelo inswapper_128.onnx es grande (~500MB)
2. Puede tardar 10-15 minutos en descargar
3. Espera pacientemente, no canceles

---

## 🎯 VERIFICACIÓN FINAL

Una vez desplegado, prueba en este orden:

### 1. Health Check
```
GET https://face-swap-app-9dz7.onrender.com/api/health
```
**Respuesta esperada:** `{"status":"ok","version":"1.0.0"}`

### 2. Face Swap Multi (debe existir)
```
GET https://face-swap-app-9dz7.onrender.com/api/face-swap-multi
```
**Respuesta esperada:** `405 Method Not Allowed` (porque requiere POST)

### 3. Frontend
```
https://caras-frontend.vercel.app
```
**Debe funcionar:** Sin errores 502

---

## 📞 SI NADA FUNCIONA

### Opción A: Crear nuevo servicio en Render
1. Dashboard → New → Web Service
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Name:** face-swap-backend-v2
   - **Region:** Oregon (us-west-2)
   - **Branch:** main
   - **Root Directory:** (déjalo vacío)
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt && npm install --production && python download_model.py`
   - **Start Command:** `node server.js`
4. Click en "Create Web Service"

### Opción B: Usar alternativa (Railway, Fly.io)
1. Railway: https://railway.app
2. Fly.io: https://fly.io
3. Sigue procesos similares de despliegue

---

## 📊 Estado Actual

| Componente | Estado | URL |
|------------|--------|-----|
| GitHub Repo | ✅ OK | https://github.com/jarabo1002-hue/cambio-de-caras |
| Render Backend | ⚠️ Desactualizado | https://face-swap-app-9dz7.onrender.com |
| Vercel Frontend | ✅ OK | https://caras-frontend.vercel.app |
| Health Check | ✅ OK | /api/health |
| Face Swap Multi | ❌ No disponible | /api/face-swap-multi |

---

## 🔄 Después de Solucionar

Una vez que funcione:

1. **Ejecuta keep-alive.bat** para mantener el backend despierto
   ```
   cd g:\curros\qwen\face-swap-ethical
   keep-alive.bat
   ```

2. **O configura UptimeRobot** (gratis):
   - URL: https://face-swap-app-9dz7.onrender.com/api/health
   - Intervalo: 14 minutos

3. **Prueba el frontend:**
   - Abre: https://caras-frontend.vercel.app
   - Sube imágenes
   - ¡Debería funcionar sin error 502!

---

**Última actualización:** 2026-03-16
**Commit más reciente:** 7d7f74b
