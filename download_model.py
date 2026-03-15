import os
import urllib.request
import sys

def download_model():
    model_path = 'inswapper_128.onnx'
    # URL de descarga del modelo
    url = "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx"
    
    if os.path.exists(model_path):
        print(f"El modelo {model_path} ya existe.")
    else:
        print(f"Descargando {model_path} desde {url}...")
        try:
            urllib.request.urlretrieve(url, model_path)
            print("Descarga completada exitosamente.")
        except Exception as e:
            print(f"Error descargando el modelo: {e}")
            url_secundaria = "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx"
            print(f"Intentando servidor secundario: {url_secundaria}")
            try:
                urllib.request.urlretrieve(url_secundaria, model_path)
                print("Descarga completada (Servidor secundario).")
            except Exception as e2:
                print(f"Fallo total en la descarga: {e2}")

    # Descargar modelos de InsightFace (DETECCION)
    print("⏳ Descargando modelos de detección de InsightFace...")
    try:
        from insightface.app import FaceAnalysis
        # Intentamos descargar buffalo_s (ligero para detección) y buffalo_l
        app_s = FaceAnalysis(name='buffalo_s', providers=['CPUExecutionProvider'])
        app_s.prepare(ctx_id=0, det_size=(640, 640))
        
        app_l = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        app_l.prepare(ctx_id=0, det_size=(640, 640))
        print("✓ Modelos de InsightFace (S y L) descargados y preparados.")
    except Exception as e:
        print(f"Error preparando InsightFace: {e}")

if __name__ == "__main__":
    download_model()
