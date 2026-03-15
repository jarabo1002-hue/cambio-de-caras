import os
import urllib.request

def download_model():
    model_path = 'inswapper_128.onnx'
    # URL de descarga del modelo
    url = "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx"
    
    if os.path.exists(model_path):
        print(f"El modelo {model_path} ya existe.")
        return

    print(f"Descargando {model_path} desde {url}...")
    try:
        # Descargar con barra de progreso simple o solo log
        urllib.request.urlretrieve(url, model_path)
        print("Descarga completada exitosamente.")
    except Exception as e:
        print(f"Error descargando el modelo: {e}")
        # Intentar servidor secundario si falla
        url_secundaria = "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx"
        print(f"Intentando servidor secundario: {url_secundaria}")
        try:
            urllib.request.urlretrieve(url_secundaria, model_path)
            print("Descarga completada (Servidor secundario).")
        except Exception as e2:
            print(f"Fallo total en la descarga: {e2}")

if __name__ == "__main__":
    download_model()
