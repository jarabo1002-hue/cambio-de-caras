# 🚀 GUÍA DE DESPLIEGUE - HUGGING FACE SPACES

## ✅ Paso a paso para desplegar GRATIS

---

## 📋 PASO 1: Inicia sesión en Hugging Face

1. Ve a: https://huggingface.co/spaces
2. Click en **"Sign In"** (arriba derecha)
3. Click en **"Log in with GitHub"**
4. Autoriza Hugging Face a acceder a tu cuenta

---

## 📋 PASO 2: Crea un nuevo Space

1. Click en tu **avatar** (esquina superior derecha)
2. Click en **"New Space"**

---

## 📋 PASO 3: Rellena el formulario

| Campo | Valor |
|-------|-------|
| **Space name** | `face-swap-ethical` |
| **License** | `MIT` |
| **SDK** | `Docker` ⚠️ **IMPORTANTE** |
| **Visibility** | `Public` |

**Screenshot del formulario:**
```
┌────────────────────────────────────────┐
│ Space name                             │
│ face-swap-ethical                      │
├────────────────────────────────────────┤
│ License                                │
│ MIT                                    │
├────────────────────────────────────────┤
│ SDK                              ▼     │
│ Docker                                 │
├────────────────────────────────────────┤
│ Visibility                             │
│ ● Public  ○ Private                    │
└────────────────────────────────────────┘
```

---

## 📋 PASO 4: Click en "Create Space"

Hugging Face creará el espacio.

---

## 📋 PASO 5: Conecta tu repositorio de GitHub

1. En la página del Space, verás opciones de despliegue
2. Click en **"Import from GitHub"**
3. Selecciona: `jarabo1002-hue/cambio-de-caras`
4. Click en **"Import"**

---

## 📋 PASO 6: Configura las variables de entorno

1. En tu Space, ve a la pestaña **"Settings"**
2. Busca **"Variables"** o **"Environment Variables"**
3. Añade:

| Variable | Valor |
|----------|-------|
| `NODE_ENV` | `production` |
| `PORT` | `3000` |

---

## 📋 PASO 7: ¡Espera el despliegue!

1. Hugging Face comenzará a construir tu Docker
2. Verás los logs en tiempo real en la pestaña **"Logs"**
3. **Tiempo estimado:** 15-20 minutos (descarga el modelo ~500MB)
4. Cuando diga **"Running"** o **"Live"**, ¡está listo!

---

## 📊 Estado del despliegue

| Estado | Significado |
|--------|-------------|
| `Building` | Construyendo imagen Docker |
| `Starting` | Iniciando contenedor |
| `Running` | ✅ ¡Listo para usar! |
| `Error` | Algo falló (revisa logs) |

---

## 🔗 URLs importantes

| Recurso | URL |
|---------|-----|
| Tu Space | `https://huggingface.co/spaces/TU_USUARIO/face-swap-ethical` |
| API | `https://TU_USUARIO-face-swap-ethical.hf.space/api/health` |
| Logs | Pestaña "Logs" en tu Space |

---

## ⚠️ Problemas comunes

### Error: "Build failed"
**Causa:** Error en Dockerfile o dependencias

**Solución:**
1. Ve a pestaña "Logs"
2. Busca la línea con error
3. Verifica que `requirements.txt` y `package.json` estén correctos

### Error: "Timeout"
**Causa:** El modelo tarda en descargar

**Solución:**
- Espera, puede tardar 15-20 minutos
- El modelo inswapper_128.onnx es ~500MB

### Error: "Out of memory"
**Causa:** Pocas RAM disponible

**Solución:**
- Hugging Face da recursos generosos para Docker
- Si persiste, considera upgrade a GPU (pago)

---

## ✅ Después del despliegue

### 1. Actualiza el frontend en Vercel

1. Ve a: https://vercel.com/dashboard
2. Busca tu proyecto `caras-frontend`
3. Ve a Settings → Environment Variables
4. Actualiza `BACKEND_URL` con la URL de Hugging Face:
   ```
   https://TU_USUARIO-face-swap-ethical.hf.space
   ```
5. Redeploy en Vercel

### 2. Prueba el backend

```
https://TU_USUARIO-face-swap-ethical.hf.space/api/health
```

Debe responder: `{"status":"ok","version":"1.0.0"}`

### 3. Prueba el frontend

```
https://caras-frontend.vercel.app
```

¡Debería funcionar sin error 502!

---

## 💰 Costo

| Servicio | Costo |
|----------|-------|
| Hugging Face Spaces | **GRATIS** (CPU básico) |
| Hugging Face GPU | Pago (opcional, ~$5-10/mes) |

**Recomendación:** Empieza con CPU gratis. Si necesitas más velocidad, upgrade a GPU.

---

## 📞 Soporte

- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Discord: https://discord.gg/huggingface
- GitHub Issues: https://github.com/jarabo1002-hue/cambio-de-caras/issues

---

**Última actualización:** 2026-03-16
**Autor:** Face Swap Ético Team
