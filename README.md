# 🤖 Face Swap Ético

Aplicación web para intercambio de caras con **salvaguardas éticas incorporadas**. Diseñada para uso responsable con consentimiento explícito.

## 🚀 Características

### Alta Resolución
- ✅ **Upscaling 2x** para mejor calidad
- ✅ **Detección de caras mejorada** (640x640)
- ✅ **PNG sin compresión** para máxima calidad
- ✅ **Marca de agua escalable** según resolución

### Salvaguardas Éticas
- ✅ **Verificación de edad** (mayor de 18 años)
- ✅ **Confirmación de consentimiento** obligatoria
- ✅ **Marca de agua** en todas las imágenes generadas
- ✅ **Términos de servicio** con usos prohibidos
- ✅ **Sin almacenamiento** de imágenes (se eliminan tras el procesamiento)

### Usos Prohibidos

- ❌ Contenido para adultos no consensuado
- ❌ Acoso o bullying
- ❌ Difamación o daño a la reputación
- ❌ Noticias falsas o desinformación
- ❌ Suplantación de identidad
- ❌ Cualquier propósito ilegal

---

## 📋 Requisitos

### Node.js
- Node.js 18 o superior
- npm o yarn

### Python
- Python 3.8 o superior
- pip

### Modelo de Face Swap
Debes descargar el modelo `inswapper_128.onnx`:
- [Descargar desde GitHub Releases](https://github.com/face-hunter/inswapper_128.onnx/releases)
- Colócalo en una ubicación accesible (insightface lo buscará automáticamente)

---

## 🚀 Instalación

### 1. Clonar o descargarar el proyecto

```bash
cd face-swap-ethical
```

### 2. Instalar dependencias de Node.js

```bash
npm install
```

### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

El archivo `.env` ya está creado con la configuración por defecto.

---

## ▶️ Ejecutar la Aplicación

```bash
npm start
```

La aplicación estará disponible en: **http://localhost:3000**

---

## 📁 Estructura del Proyecto

```
face-swap-ethical/
├── public/
│   └── index.html          # Frontend (HTML + Bootstrap + JS)
├── uploads/                 # Archivos temporales (auto-generado)
├── results/                 # Resultados procesados (auto-generado)
├── server.js               # Backend (Node.js + Express)
├── face_swap.py            # Script de procesamiento (Python)
├── requirements.txt        # Dependencias de Python
├── package.json            # Dependencias de Node.js
├── .env                    # Variables de entorno
└── README.md               # Esta documentación
```

---

## 🔧 Características Técnicas

### Frontend
- HTML5 + CSS3 + JavaScript vanilla
- Bootstrap 5 para el diseño
- Drag & drop para subir imágenes
- Verificación de edad con localStorage
- Preview de imágenes antes de procesar

### Backend
- Node.js con Express
- Multer para manejo de archivos
- Validación de tipos y tamaño de archivos
- CORS habilitado
- Eliminación automática de archivos temporales

### Procesamiento de Imágenes
- Python con insightface
- OpenCV para manipulación de imágenes
- Pillow para marcas de agua
- Modelo inswapper_128 para face swapping

---

## 🛡️ Salvaguardas Éticas Implementadas

| Salvaguarda | Descripción |
|-------------|-------------|
| **Edad** | Verificación de mayor de 18 años |
| **Consentimiento** | Checkbox obligatorio confirmando consentimiento |
| **Marca de Agua** | Texto visible en todas las imágenes generadas |
| **Términos** | Sección completa con usos prohibidos |
| **Privacidad** | No se almacenan imágenes |
| **Límite de Tamaño** | Máximo 10MB por imagen |
| **Tipos de Archivo** | Solo JPEG, PNG, WebP |

---

## 📸 Uso

1. **Verifica tu edad** (solo la primera vez)
2. **Sube la imagen de origen** (la cara que quieres usar)
3. **Sube la imagen de destino** (donde se aplicará el cambio)
4. **Marca la casilla de consentimiento**
5. **Haz clic en "Intercambiar Caras"**
6. **Descarga el resultado** con marca de agua

---

## 🔍 Solución de Problemas

### Error: "insightface no está instalado"
```bash
pip install -r requirements.txt
```

### Error: "No se pudo cargar el modelo inswapper_128.onnx"
Descarga el modelo desde [GitHub Releases](https://github.com/face-hunter/inswapper_128.onnx/releases)

### Error: "No se detectó ninguna cara"
- Asegúrate de que las imágenes tengan caras claramente visibles
- Usa imágenes con buena iluminación
- Las caras deben estar de frente o ligeramente de lado

### Error: "Archivo demasiado grande"
Las imágenes no pueden superar los 10MB. Comprime la imagen antes de subirla.

---

## 📝 Consideraciones Legales

Las leyes sobre deepfakes y face swap varían por país:

- **España**: Ley contra deepfakes no consensuados (2024)
- **UE**: AI Act regula el uso de IA para manipulación de imágenes
- **EE.UU.**: Varios estados tienen leyes específicas
- **México**: Ley Olimpia protege contra difusión de contenido íntimo sin consentimiento

**Siempre consulta las leyes locales antes de usar esta tecnología.**

---

## 🤝 Contribuciones

Si quieres contribuir, por favor asegúrate de mantener las salvaguardas éticas. No aceptaremos cambios que:

- Eliminen la verificación de edad
- Remuevan la marca de agua
- Permitan uso sin consentimiento
- Habiliten procesamiento masivo

---

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles.

---

## 🙏 Agradecimientos

- [insightface](https://github.com/deepinsight/insightface) - Librería de reconocimiento facial
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- Comunidad de IA ética

---

## 📞 Contacto

Para preguntas sobre uso ético de esta tecnología, consulta recursos como:
- [Partnership on AI](https://partnershiponai.org/)
- [AI Ethics Guidelines](https://ec.europa.eu/digital-strategy/our-technologies/ethics-artificial-intelligence_en)

---

**Hecho con responsabilidad ❤️**

*La tecnología debe usarse para el bien, no para el daño.*
