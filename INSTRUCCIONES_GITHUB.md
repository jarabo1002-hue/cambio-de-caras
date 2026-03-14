# 📤 Instrucciones para Subir a GitHub

## Opción 1: Usar el script automático (Recomendado)

1. **Ejecuta el script:**
   ```
   doble_clic_en_subir-a-github.bat
   ```

2. **Cuando se solicite autenticación:**
   - Introduce tu usuario de GitHub
   - Introduce tu contraseña o token de acceso personal

3. **¡Listo!** Los cambios se subirán automáticamente

---

## Opción 2: Comandos manuales

Si prefieres hacerlo manualmente, abre una terminal en la carpeta del proyecto y ejecuta:

```bash
cd g:\curros\qwen\face-swap-ethical
git push -u origin main
```

---

## 🔑 Si no tienes permisos en el repositorio

### Opción A: Crear tu propio repositorio

1. Ve a https://github.com/new
2. Crea un repositorio llamado `cambio-de-caras`
3. Ejecuta estos comandos:

```bash
cd g:\curros\qwen\face-swap-ethical
git remote set-url origin https://github.com/TU_USUARIO/cambio-de-caras.git
git push -u origin main
```

### Opción B: Pedir acceso

Contacta al dueño del repositorio (`01Jarabo`) y pide que te añada como colaborador.

---

## 🎫 Crear token de GitHub (Recomendado para autenticación)

1. Ve a: https://github.com/settings/tokens
2. Haz clic en "Generate new token (classic)"
3. Pon un nombre (ej: "Face Swap Project")
4. Marca el permiso `repo` (Full control of private repositories)
5. Haz clic en "Generate token"
6. **Copia el token** (solo se muestra una vez)
7. Úsalo como contraseña cuando git te la solicite

---

## ✅ Verificar que se subió correctamente

Después de hacer push, visita:
```
https://github.com/01Jarabo/cambio-de-caras
```

Deberías ver todos los archivos del proyecto.

---

## 📁 Archivos que se subirán

- ✅ `README.md` - Documentación del proyecto
- ✅ `package.json` - Dependencias de Node.js
- ✅ `server.js` - Backend (Node.js + Express)
- ✅ `face_swap.py` - Script de face swap (Python)
- ✅ `detect_faces.py` - Detección de caras (Python)
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `public/index.html` - Frontend (HTML + JS)
- ✅ `.gitignore` - Archivos ignorados
- ✅ `.env` - Variables de entorno (si existe)

---

## 🚫 Archivos que NO se suben (privacidad)

- ❌ `node_modules/` - Dependencias instaladas
- ❌ `uploads/` - Imágenes temporales
- ❌ `results/` - Resultados generados
- ❌ `.env` - Variables sensibles
- ❌ `inswapper_128.onnx` - Modelo (500MB, demasiado grande)

---

## 💡 Consejo

Si el repositorio es privado, solo tú y los colaboradores podrán verlo.
Si es público, cualquiera podrá ver el código.
