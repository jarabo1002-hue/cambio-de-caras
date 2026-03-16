"""
Detección de caras para Face Swap Ético
========================================
Detecta caras en una imagen y devuelve información en formato JSON.
"""

import sys
import cv2
import numpy as np
import os
import json
import warnings

# Silenciar warnings
warnings.filterwarnings('ignore')

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def detect_faces(image_path):
    """Detecta caras en una imagen y devuelve información."""
    try:
        import insightface
        from insightface.app import FaceAnalysis
    except ImportError:
        sys.stderr.write("ERROR: insightface no está instalado\n")
        print(json.dumps({"error": "insightface no está instalado"}))
        sys.exit(1)

    # Inicializar detector (usamos buffalo_s por memoria)
    app = FaceAnalysis(name='buffalo_s', providers=['CPUExecutionProvider'], verbose=False)
    # Reducimos det_size a 320 para ahorrar mucha RAM
    app.prepare(ctx_id=0, det_size=(320, 320))

    # Leer imagen
    img = cv2.imread(image_path)
    if img is None:
        print(json.dumps({"error": "No se pudo leer la imagen"}))
        sys.exit(1)

    # REESCALADO PARA AHORRO DE MEMORIA
    # Si la imagen es muy grande, InsightFace consumirá demasiada RAM
    MAX_DIM = 1000
    height, width = img.shape[:2]
    orig_height, orig_width = height, width
    
    if height > MAX_DIM or width > MAX_DIM:
        scale = MAX_DIM / max(height, width)
        img = cv2.resize(img, (int(width * scale), int(height * scale)))
        height, width = img.shape[:2]
        # sys.stderr.write(f"Resized for detection to {width}x{height}\n")

    # Detectar caras
    faces = app.get(img)

    # Ajustar coordenadas si hubo reescalado
    scale_x = orig_width / width
    scale_y = orig_height / height

    # Preparar resultado
    faces_info = []
    for i, face in enumerate(faces):
        bbox = face.bbox.astype(int)
        faces_info.append({
            "index": i,
            "bbox": {
                "x": int(bbox[0] * scale_x),
                "y": int(bbox[1] * scale_y),
                "width": int((bbox[2] - bbox[0]) * scale_x),
                "height": int((bbox[3] - bbox[1]) * scale_y)
            },
            "confidence": float(face.det_score),
            "landmarks": (face.kps * [scale_x, scale_y]).tolist() if hasattr(face, 'kps') else [],
            "gender": int(face.gender) if hasattr(face, 'gender') else 0,
            "age": int(face.age) if hasattr(face, 'age') else 0
        })

    # Ordenar caras: de izquierda a derecha, luego de arriba a abajo
    faces_info.sort(key=lambda f: (f['bbox']['y'] // 100 * 100, f['bbox']['x']))

    # Re-indexar después de ordenar
    for i, face in enumerate(faces_info):
        face['displayIndex'] = i

    result = {
        "faces": faces_info,
        "width": orig_width,
        "height": orig_height,
        "facesCount": len(faces_info)
    }

    # Solo imprimir JSON puro
    print(json.dumps(result))
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Se requiere ruta de imagen"}))
        sys.exit(1)

    image_path = sys.argv[1]
    detect_faces(image_path)
