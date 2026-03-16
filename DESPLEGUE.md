# Guía de Despliegue - Face Swap Ético

## Problema Actual
El endpoint `/api/face-swap-multi` no está disponible en el backend de Render.

## Solución Paso a Paso

### Opción 1: Despliegue Automático (Recomendada)

1. **Los cambios ya están en GitHub**
   - Repositorio: https://github.com/jarabo1002-hue/cambio-de-caras
   - Últimos commits subidos correctamente

2. **Esperar a que Render despliegue**
   - Render detecta cambios en GitHub automáticamente
   - Tiempo estimado: 5-10 minutos
   - Ver estado: https://dashboard.render.com

3. **Verificar el despliegue**
   ```
   https://face-swap-app-9dz7.onrender.com/api/health
   ```

4. **Probar el endpoint**
   ```
   https://face-swap-app-9dz7.onrender.com/api/face-swap-multi
   ```
   Debería devolver 405 Method Not Allowed (porque requiere POST)

### Opción 2: Despliegue Manual en Render

1. Ir a https://dashboard.render.com
2. Iniciar sesión
3. Buscar el servicio `face-swap-ethical-backend` o `face-swap-app-9dz7`
4. Click en "Manual Deploy" → "Deploy latest commit"
5. Esperar a que complete
6. Ver logs en tiempo real

### Opción 3: Verificar Logs de Error

Si el despliegue falla:

1. Ir a Render Dashboard
2. Seleccionar el servicio
3. Click en "Logs"
4. Buscar errores como:
   - Error en `npm install`
   - Error en `pip install`
   - Error en `download_model.py`
   - Error en `server.js`

### Posibles Problemas y Soluciones

#### Problema 1: Error en requirements.txt
```bash
# Verificar que requirements.txt existe y es válido
cat requirements.txt
```

#### Problema 2: Error en download_model.py
El modelo inswapper_128.onnx es grande (~500MB) y puede fallar la descarga.

**Solución:**
- Verificar que `download_model.py` está en el repositorio
- Revisar logs de Render para ver si la descarga completó

#### Problema 3: Error en server.js
El servidor puede tener errores de sintaxis.

**Solución:**
```bash
# Probar localmente antes de subir
node server.js
```

#### Problema 4: Puerto incorrecto
Render asigna el puerto automáticamente mediante la variable `PORT`.

**Verificar en server.js:**
```javascript
const PORT = process.env.PORT || 3000;
```

### Comandos Útiles

#### Probar backend localmente
```bash
cd g:\curros\qwen\face-swap-ethical
npm start
```

#### Ver logs de Render (CLI)
```bash
render logs -f
```

#### Forzar redepliegue
1. Ir a Render Dashboard
2. Servicio → Manual Deploy → Deploy latest commit

### URLs Importantes

| Recurso | URL |
|---------|-----|
| Frontend (Vercel) | https://caras-frontend.vercel.app |
| Backend (Render) | https://face-swap-app-9dz7.onrender.com |
| Health Check | https://face-swap-app-9dz7.onrender.com/api/health |
| Test Backend | https://caras-frontend.vercel.app/test-backend.html |
| GitHub Repo | https://github.com/jarabo1002-hue/cambio-de-caras |
| Render Dashboard | https://dashboard.render.com |
| Vercel Dashboard | https://vercel.com/dashboard |

### Endpoints del Backend

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/health | Verificar estado |
| GET | /api/terms | Términos de servicio |
| POST | /api/face-swap | Face swap simple (1 cara) |
| POST | /api/face-swap-multi | Face swap múltiple |
| POST | /api/detect-faces | Detectar caras |
| GET | /api/job-status/:jobId | Estado de job asíncrono |

### Mantenimiento

#### Mantener backend despierto
Render duerme los servicios free después de 15 min de inactividad.

**Opción A:** Usar script local
```bash
keep-alive.bat
```

**Opción B:** Usar servicio externo como UptimeRobot
- URL a monitorear: https://face-swap-app-9dz7.onrender.com/api/health
- Intervalo: 14 minutos

### Contacto y Soporte

- GitHub Issues: https://github.com/jarabo1002-hue/cambio-de-caras/issues
- Render Support: https://render.com/support
