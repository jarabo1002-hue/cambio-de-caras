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

    # Inicializar detector
    app = FaceAnalysis(providers=['CPUExecutionProvider'], verbose=False)
    app.prepare(ctx_id=0, det_size=(640, 640))

    # Leer imagen
    img = cv2.imread(image_path)
    if img is None:
        print(json.dumps({"error": "No se pudo leer la imagen"}))
        sys.exit(1)

    height, width = img.shape[:2]

    # Detectar caras
    faces = app.get(img)

    # Preparar resultado
    faces_info = []
    for i, face in enumerate(faces):
        bbox = face.bbox.astype(int)
        faces_info.append({
            "index": i,
            "bbox": {
                "x": int(bbox[0]),
                "y": int(bbox[1]),
                "width": int(bbox[2] - bbox[0]),
                "height": int(bbox[3] - bbox[1])
            },
            "confidence": float(face.det_score),
            "landmarks": face.kps.tolist() if hasattr(face, 'kps') else [],
            "gender": int(face.gender) if hasattr(face, 'gender') else 0,
            "age": int(face.age) if hasattr(face, 'age') else 0
        })

    # Ordenar caras: de izquierda a derecha, luego de arriba a abajo
    faces_info.sort(key=lambda f: (f['bbox']['y'] // 50 * 50, f['bbox']['x']))

    # Re-indexar después de ordenar
    for i, face in enumerate(faces_info):
        face['displayIndex'] = i

    result = {
        "faces": faces_info,
        "width": width,
        "height": height,
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
