const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const { exec } = require('child_process');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Configuración de multer para uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

// Filtro para solo permitir imágenes
const fileFilter = (req, file, cb) => {
  const allowedTypes = /jpeg|jpg|png|webp/;
  const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
  const mimetype = allowedTypes.test(file.mimetype);

  if (extname && mimetype) {
    cb(null, true);
  } else {
    cb(new Error('Solo se permiten imágenes (JPEG, PNG, WebP)'));
  }
};

const upload = multer({
  storage,
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB máximo
  fileFilter
});

// Directorio para resultados
const resultsDir = path.join(__dirname, 'results');
if (!fs.existsSync(resultsDir)) {
  fs.mkdirSync(resultsDir, { recursive: true });
}

// Endpoint principal de face swap (una cara)
app.post('/api/face-swap', upload.fields([
  { name: 'sourceImage', maxCount: 1 },
  { name: 'targetImage', maxCount: 1 }
]), async (req, res) => {
  try {
    // Validar que se subieron ambas imágenes
    if (!req.files.sourceImage || !req.files.targetImage) {
      return res.status(400).json({
        error: 'Se requieren ambas imágenes: origen y destino'
      });
    }

    const sourceImagePath = req.files.sourceImage[0].path;
    const targetImagePath = req.files.targetImage[0].path;
    const resultFilename = `${uuidv4()}_result.png`;
    const resultPath = path.join(resultsDir, resultFilename);

    // Verificar consentimiento (declaración del usuario)
    const { consentConfirmed } = req.body;
    if (!consentConfirmed) {
      // Limpiar archivos subidos
      fs.unlinkSync(sourceImagePath);
      fs.unlinkSync(targetImagePath);
      return res.status(400).json({
        error: 'Debes confirmar que tienes consentimiento para usar estas imágenes'
      });
    }

    // Ejecutar script de Python para face swap
    const pythonScript = path.join(__dirname, 'face_swap.py');
    const command = `python3 "${pythonScript}" single "${sourceImagePath}" "${targetImagePath}" "${resultPath}"`;

    exec(command, (error, stdout, stderr) => {
      // Limpiar archivos temporales de upload
      try {
        fs.unlinkSync(sourceImagePath);
        fs.unlinkSync(targetImagePath);
      } catch (e) {
        console.error('Error limpiando archivos:', e);
      }

      if (error) {
        console.error('Error en face swap:', error);
        console.error('STDERR:', stderr);
        return res.status(500).json({
          error: 'Error procesando las imágenes. Asegúrate de tener Python y las dependencias instaladas.',
          details: stderr || error.message
        });
      }

      // Verificar que el resultado existe
      if (!fs.existsSync(resultPath)) {
        return res.status(500).json({
          error: 'No se generó el resultado'
        });
      }

      // URL para descargar el resultado
      const resultUrl = `/results/${resultFilename}`;

      res.json({
        success: true,
        message: 'Face swap completado exitosamente',
        resultUrl,
        watermark: 'Esta imagen contiene una marca de agua ética',
        disclaimer: 'Esta imagen fue generada con IA. No la uses para engañar o dañar a otros.'
      });
    });

  } catch (error) {
    console.error('Error general:', error);
    res.status(500).json({
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// Endpoint para face swap múltiple
app.post('/api/face-swap-multi', upload.fields([
  { name: 'sourceImages', maxCount: 10 },
  { name: 'targetImage', maxCount: 1 }
]), async (req, res) => {
  try {
    // Validar que se subieron las imágenes
    if (!req.files.sourceImages || !req.files.targetImage) {
      return res.status(400).json({
        error: 'Se requieren al menos una imagen de origen y una de destino'
      });
    }

    if (req.files.sourceImages.length === 0) {
      return res.status(400).json({
        error: 'Se requiere al menos una imagen de origen'
      });
    }

    const sourceImagePaths = req.files.sourceImages.map(f => f.path);
    const targetImagePath = req.files.targetImage[0].path;
    const resultFilename = `${uuidv4()}_result.png`;
    const resultPath = path.join(resultsDir, resultFilename);

    // Verificar consentimiento
    const { consentConfirmed, faceMapping } = req.body;
    if (!consentConfirmed) {
      // Limpiar archivos subidos
      sourceImagePaths.forEach(p => fs.unlinkSync(p));
      fs.unlinkSync(targetImagePath);
      return res.status(400).json({
        error: 'Debes confirmar que tienes consentimiento para usar estas imágenes'
      });
    }

    // Preparar mapeo de caras si se proporcionó
    let mappingArg = '';
    if (faceMapping) {
      try {
        const mapping = typeof faceMapping === 'string' ? JSON.parse(faceMapping) : faceMapping;
        mappingArg = `"${JSON.stringify(mapping)}"`;
      } catch (e) {
        console.error('Error parseando faceMapping:', e);
      }
    }

    // Ejecutar script de Python para face swap múltiple
    const pythonScript = path.join(__dirname, 'face_swap.py');
    const sourcesArg = sourceImagePaths.join(',');
    const command = `python3 "${pythonScript}" multi "${sourcesArg}" "${targetImagePath}" "${resultPath}" ${mappingArg}`;

    exec(command, (error, stdout, stderr) => {
      // Limpiar archivos temporales de upload
      try {
        sourceImagePaths.forEach(p => fs.unlinkSync(p));
        fs.unlinkSync(targetImagePath);
      } catch (e) {
        console.error('Error limpiando archivos:', e);
      }

      if (error) {
        console.error('Error en face swap múltiple:', error);
        console.error('STDERR:', stderr);
        return res.status(500).json({
          error: 'Error procesando las imágenes.',
          details: stderr || error.message
        });
      }

      // Verificar que el resultado existe
      if (!fs.existsSync(resultPath)) {
        return res.status(500).json({
          error: 'No se generó el resultado'
        });
      }

      const resultUrl = `/results/${resultFilename}`;

      res.json({
        success: true,
        message: `Face swap múltiple completado con ${req.files.sourceImages.length} imagen(es) de origen`,
        resultUrl,
        watermark: 'Esta imagen contiene una marca de agua ética',
        disclaimer: 'Esta imagen fue generada con IA. No la uses para engañar o dañar a otros.',
        facesCount: req.files.sourceImages.length
      });
    });

  } catch (error) {
    console.error('Error general:', error);
    res.status(500).json({
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// Servir resultados
app.use('/results', express.static(resultsDir));

// Endpoint para términos de servicio
app.get('/api/terms', (req, res) => {
  res.json({
    terms: {
      title: 'Términos de Servicio - Face Swap Ético',
      version: '1.0.0',
      lastUpdated: '2026-03-14',
      sections: [
        {
          title: '1. Consentimiento Obligatorio',
          content: 'Debes tener el consentimiento explícito de todas las personas cuyas imágenes uses en esta aplicación.'
        },
        {
          title: '2. Uso Prohibido',
          content: 'Queda estrictamente prohibido usar esta aplicación para: contenido pornográfico no consensuado, acoso, difamación, noticias falsas, suplantación de identidad, o cualquier propósito ilegal.'
        },
        {
          title: '3. Marca de Agua',
          content: 'Todas las imágenes generadas incluyen una marca de agua que indica que fueron creadas con IA.'
        },
        {
          title: '4. Responsabilidad del Usuario',
          content: 'El usuario es único responsable del uso que dé a las imágenes generadas. Esta aplicación es solo para fines legítimos como entretenimiento personal, educación, o proyectos artísticos con consentimiento.'
        },
        {
          title: '5. Retención de Datos',
          content: 'Las imágenes se eliminan automáticamente después del procesamiento. No almacenamos tus datos.'
        },
        {
          title: '6. Edad Mínima',
          content: 'Debes ser mayor de 18 años para usar esta aplicación.'
        }
      ],
      acceptanceRequired: true
    }
  });
});

// Endpoint de verificación de edad
app.post('/api/verify-age', (req, res) => {
  const { isOver18 } = req.body;
  if (isOver18 !== true) {
    return res.status(403).json({
      error: 'Debes ser mayor de 18 años para usar esta aplicación'
    });
  }
  res.json({ success: true, message: 'Edad verificada' });
});

// Endpoint de salud
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', version: '1.0.0' });
});

// Endpoint para detectar caras en una imagen
app.post('/api/detect-faces', upload.single('image'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'Se requiere una imagen' });
    }

    const imagePath = req.file.path;
    const { exec } = require('child_process');
    const pythonScript = path.join(__dirname, 'detect_faces.py');

    exec(`python3 "${pythonScript}" "${imagePath}"`, {
      maxBuffer: 1024 * 1024 * 10,
      windowsHide: true
    }, (error, stdout, stderr) => {
      // Limpiar archivo temporal
      try {
        fs.unlinkSync(imagePath);
      } catch (e) {
        console.error('Error limpiando archivo:', e);
      }

      if (error) {
        console.error('Error detectando caras:', error);
        console.error('STDERR:', stderr);
        return res.status(500).json({
          error: 'Error detectando caras',
          details: stderr || error.message
        });
      }

      if (!stdout || stdout.trim() === '') {
        return res.status(500).json({
          error: 'El script de detección no devolvió ningún resultado',
          details: stderr
        });
      }

      // Buscar solo el JSON en el output (última línea válida)
      try {
        const trimmedStdout = stdout.trim();
        const lines = trimmedStdout.split('\n');
        let jsonLine = lines[lines.length - 1]; // Tomar última línea

        // Intentar parsear
        const facesData = JSON.parse(jsonLine);

        if (facesData.error) {
          return res.status(500).json({ error: facesData.error });
        }

        res.json({
          success: true,
          facesCount: facesData.faces ? facesData.faces.length : 0,
          faces: facesData.faces || [],
          imageWidth: facesData.width || 0,
          imageHeight: facesData.height || 0
        });
      } catch (e) {
        console.error('Error parseando JSON:', e);
        console.error('STDOUT:', stdout);
        res.status(500).json({
          error: 'Error procesando resultado',
          details: 'No se pudo parsear la respuesta de Python: ' + e.message,
          output: stdout.substring(0, 500)
        });
      }
    });

  } catch (error) {
    console.error('Error general:', error);
    res.status(500).json({
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// Manejo de errores de multer
app.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        error: 'Archivo demasiado grande. Máximo 10MB'
      });
    }
    return res.status(400).json({ error: error.message });
  }
  next(error);
});

app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║         FACE SWAP ÉTICO - Servidor Iniciado               ║
╠═══════════════════════════════════════════════════════════╣
║  Puerto: ${PORT}                                          
║  URL: http://localhost:${PORT}                             
║                                                           
║  ⚠️  RECORDATORIO ÉTICO:                                  
║  - Solo usa imágenes con consentimiento                   
║  - Prohibido contenido ilegal o dañino                    
║  - Todas las imágenes tienen marca de agua                
║  - Mayor de 18 años requerido                             
╚═══════════════════════════════════════════════════════════╝
  `);
});
