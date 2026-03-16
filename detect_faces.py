"""
Detección de caras para Face Swap Ético
========================================
Detecta caras usando OpenCV DNN (SSD Caffe) - ultra ligero (~10MB RAM).
Mucho más eficiente que InsightFace para detección en Render Free.
"""

import sys
import cv2
import numpy as np
import os
import json
import urllib.request
import warnings

# Silenciar warnings
warnings.filterwarnings('ignore')

# Rutas de los modelos DNN (se descargan automáticamente si no existen)
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models_dnn')
PROTO_URL = 'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt'
MODEL_URL = 'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel'
PROTO_PATH = os.path.join(MODELS_DIR, 'deploy.prototxt')
MODEL_PATH = os.path.join(MODELS_DIR, 'res10_300x300_ssd.caffemodel')

def ensure_models():
    """Descarga los modelos DNN ligeros si no existen."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    if not os.path.exists(PROTO_PATH):
        sys.stderr.write("Descargando prototxt...\n")
        urllib.request.urlretrieve(PROTO_URL, PROTO_PATH)
    if not os.path.exists(MODEL_PATH):
        sys.stderr.write("Descargando caffemodel (~10MB)...\n")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

def detect_faces(image_path):
    """Detecta caras en una imagen usando OpenCV DNN SSD."""

    sys.stderr.write(f"--- Iniciando detección para {image_path} ---\n")

    # Asegurar modelos DNN
    ensure_models()

    # Leer imagen
    sys.stderr.write("Leyendo imagen...\n")
    img = cv2.imread(image_path)
    if img is None:
        print(json.dumps({"error": "No se pudo leer la imagen"}))
        sys.exit(1)

    orig_height, orig_width = img.shape[:2]

    # Reescalar si es muy grande
    MAX_DIM = 800
    if orig_height > MAX_DIM or orig_width > MAX_DIM:
        scale = MAX_DIM / max(orig_height, orig_width)
        img = cv2.resize(img, (int(orig_width * scale), int(orig_height * scale)))
        sys.stderr.write(f"Imagen reescalada a {img.shape[1]}x{img.shape[0]}\n")

    height, width = img.shape[:2]

    # Cargar red DNN
    sys.stderr.write("Cargando red DNN SSD...\n")
    net = cv2.dnn.readNetFromCaffe(PROTO_PATH, MODEL_PATH)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Crear blob (300x300 es el tamaño nativo del modelo SSD)
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)

    sys.stderr.write("Ejecutando detección...\n")
    detections = net.forward()
    sys.stderr.write(f"Detección finalizada.\n")

    # Calcular factor de escala para volver a coordenadas originales
    scale_x = orig_width / width
    scale_y = orig_height / height

    # Procesar detecciones
    faces_info = []
    for i in range(detections.shape[2]):
        confidence = float(detections[0, 0, i, 2])
        if confidence < 0.5:
            continue

        box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
        x1, y1, x2, y2 = box.astype(int)

        # Ajustar a imagen original
        x1_orig = max(0, int(x1 * scale_x))
        y1_orig = max(0, int(y1 * scale_y))
        x2_orig = min(orig_width, int(x2 * scale_x))
        y2_orig = min(orig_height, int(y2 * scale_y))

        w = x2_orig - x1_orig
        h = y2_orig - y1_orig

        if w <= 0 or h <= 0:
            continue

        # Generar landmarks aproximados (centro, puntos ojos, nariz, boca)
        cx, cy = x1_orig + w // 2, y1_orig + h // 2
        landmarks = [
            [cx - w * 0.25, cy - h * 0.15],  # ojo izq
            [cx + w * 0.25, cy - h * 0.15],  # ojo der
            [cx,            cy             ],  # nariz
            [cx - w * 0.15, cy + h * 0.20],  # boca izq
            [cx + w * 0.15, cy + h * 0.20],  # boca der
        ]

        faces_info.append({
            "index": len(faces_info),
            "bbox": {
                "x": x1_orig,
                "y": y1_orig,
                "width": w,
                "height": h
            },
            "confidence": confidence,
            "landmarks": landmarks,
            "gender": 0,
            "age": 0
        })

    # Ordenar de izquierda a derecha, luego de arriba a abajo
    faces_info.sort(key=lambda f: (f['bbox']['y'] // 100 * 100, f['bbox']['x']))

    # Re-indexar
    for i, face in enumerate(faces_info):
        face['index'] = i
        face['displayIndex'] = i

    result = {
        "faces": faces_info,
        "width": orig_width,
        "height": orig_height,
        "facesCount": len(faces_info)
    }

    sys.stderr.write(f"Caras detectadas: {len(faces_info)}\n")
    print(json.dumps(result))
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Se requiere ruta de imagen"}))
        sys.exit(1)

    image_path = sys.argv[1]
    detect_faces(image_path)
