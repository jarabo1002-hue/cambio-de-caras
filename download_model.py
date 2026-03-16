"""
Script de pre-descarga de modelos de IA durante el build de Docker.
Se ejecuta en el Dockerfile para evitar descargas en runtime.
"""

import os
import urllib.request
import sys


def download_file(url, path, description):
    if os.path.exists(path):
        print(f"✓ {description} ya existe.")
        return True
    print(f"⏳ Descargando {description}...")
    try:
        urllib.request.urlretrieve(url, path)
        print(f"✓ {description} descargado OK.")
        return True
    except Exception as e:
        print(f"✗ Error descargando {description}: {e}")
        return False


def download_dnn_models():
    """Pre-descarga los modelos DNN ligeros de OpenCV (SSD Caffe, ~10MB)."""
    models_dir = os.path.join(os.path.dirname(__file__), 'models_dnn')
    os.makedirs(models_dir, exist_ok=True)

    proto_path = os.path.join(models_dir, 'deploy.prototxt')
    model_path = os.path.join(models_dir, 'res10_300x300_ssd.caffemodel')

    ok1 = download_file(
        'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt',
        proto_path,
        'deploy.prototxt (DNN)'
    )
    ok2 = download_file(
        'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel',
        model_path,
        'SSD Caffemodel (~10MB)'
    )
    return ok1 and ok2


def download_inswapper_model():
    """Pre-descarga el modelo ONNX de face swap."""
    model_path = 'inswapper_128.onnx'

    urls = [
        "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx",
        "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx"
    ]

    if os.path.exists(model_path):
        print(f"✓ {model_path} ya existe.")
        return True

    for url in urls:
        try:
            print(f"⏳ Descargando inswapper_128.onnx desde {url}...")
            urllib.request.urlretrieve(url, model_path)
            print(f"✓ inswapper_128.onnx descargado OK.")
            return True
        except Exception as e:
            print(f"✗ Fallo en {url}: {e}")

    print("✗ No se pudo descargar inswapper_128.onnx")
    return False


def download_insightface_models():
    """Pre-descarga los modelos de InsightFace buffalo_s (solo para swap)."""
    print("⏳ Descargando InsightFace buffalo_s (para swap)...")
    try:
        from insightface.app import FaceAnalysis
        app_s = FaceAnalysis(
            name='buffalo_s',
            providers=['CPUExecutionProvider'],
            allowed_modules=['detection', 'recognition']
        )
        app_s.prepare(ctx_id=0, det_size=(320, 320))
        print("✓ InsightFace buffalo_s descargado OK.")
        return True
    except Exception as e:
        print(f"✗ Error preparando InsightFace buffalo_s: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Iniciando pre-descarga de modelos de IA")
    print("=" * 50)

    ok1 = download_dnn_models()
    ok2 = download_inswapper_model()
    ok3 = download_insightface_models()

    print("=" * 50)
    if ok1 and ok2 and ok3:
        print("✓ Todos los modelos pre-descargados correctamente.")
    else:
        print("⚠ Algunos modelos no se descargaron. Se intentarán descargar en runtime.")
    print("=" * 50)
