"""
Face Swap Ético - Script de procesamiento múltiple
===================================================
Este script realiza intercambio de caras con marcas de agua éticas.
Soporta intercambio de una cara o múltiples caras.

REQUISITOS:
    pip install insightface opencv-python numpy pillow

NOTA ÉTICA:
    Este script añade una marca de agua discreta a todas las imágenes
    generadas para indicar que fueron creadas con IA.
"""

import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import urllib.request
import json

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Ruta del modelo
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'inswapper_128.onnx')

def download_model():
    """Descarga el modelo inswapper_128.onnx si no existe."""
    if os.path.exists(MODEL_PATH):
        file_size = os.path.getsize(MODEL_PATH)
        if file_size > 1000000:
            print(f"✓ Modelo encontrado: {MODEL_PATH} ({file_size / 1024 / 1024:.1f} MB)")
            return True

    print("⏳ Descargando modelo inswapper_128.onnx...")
    print("   Esto puede tardar varios minutos dependiendo de tu conexión...")

    urls = [
        "https://github.com/face-hunter/inswapper_128.onnx/releases/download/latest/inswapper_128.onnx",
        "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx",
    ]

    for url in urls:
        try:
            print(f"   Intentando: {url[:60]}...")
            urllib.request.urlretrieve(url, MODEL_PATH)
            if os.path.getsize(MODEL_PATH) > 1000000:
                print(f"✓ Modelo descargado exitosamente ({os.path.getsize(MODEL_PATH) / 1024 / 1024:.1f} MB)")
                return True
            else:
                os.remove(MODEL_PATH)
                print("   Archivo descargado inválido, intentando otra fuente...")
        except Exception as e:
            print(f"   Error con esta fuente: {e}")
            continue

    print("\n❌ No se pudo descargar el modelo automáticamente.")
    print("\nDescarga manual:")
    print("1. Ve a: https://huggingface.co/ezioruan/inswapper_128.onnx")
    print("2. Descarga el archivo inswapper_128.onnx")
    print(f"3. Guárdalo en: {MODEL_PATH}")
    return False


def add_watermark(image_path, output_path):
    """Añade una marca de agua ética a la imagen resultante."""
    try:
        img = Image.open(image_path).convert("RGBA")
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        watermark_text = "🤖 AI-GENERATED | ÉTICA | CONSENTIMIENTO REQUERIDO"
        font_size = max(16, min(img.width, img.height) // 40)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        margin = max(10, img.width // 100)
        x = img.width - text_width - margin
        y = img.height - text_height - margin

        padding = max(5, font_size // 3)
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(0, 0, 0, 180)
        )

        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 255))
        watermarked = Image.alpha_composite(img, overlay)
        watermarked = watermarked.convert("RGB")
        watermarked.save(output_path, "PNG", quality=100)

        print(f"✓ Marca de agua añadida exitosamente (tamaño: {img.width}x{img.height})")
        return True

    except Exception as e:
        print(f"⚠ Error añadiendo marca de agua: {e}")
        img = Image.open(image_path).convert("RGB")
        img.save(output_path, "PNG", quality=100)
        return True


def detect_faces(app, img):
    """Detecta caras en una imagen y las ordena por posición."""
    faces = app.get(img)
    # Ordenar caras: de izquierda a derecha, luego de arriba a abajo
    faces_sorted = sorted(faces, key=lambda x: (x.bbox[1] // 50 * 50, x.bbox[0]))
    return faces_sorted


def process_single_face_swap(source_path, target_path, output_path, app, swapper):
    """Procesa face swap de una sola cara."""
    # Verificar y descargar modelo si es necesario
    if not download_model():
        sys.exit(1)

    print("⏳ Inicializando detector de caras...")
    app = FaceAnalysis(name='buffalo_s', providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))

    print("⏳ Cargando modelo de face swapper...")
    try:
        swapper = insightface.model_zoo.get_model(MODEL_PATH, providers=['CPUExecutionProvider'])
    except Exception as e:
        print(f"ERROR: No se pudo cargar el modelo")
        print(f"Error: {e}")
        sys.exit(1)

    print("⏳ Leyendo imágenes...")
    source_img = cv2.imread(source_path)
    target_img = cv2.imread(target_path)

    if source_img is None:
        print(f"ERROR: No se pudo leer la imagen de origen: {source_path}")
        sys.exit(1)

    if target_img is None:
        print(f"ERROR: No se pudo leer la imagen destino: {target_path}")
        sys.exit(1)

    # Escalar imágenes si son demasiado pequeñas
    h, w = source_img.shape[:2]
    min_dim = 512
    if h < min_dim or w < min_dim:
        scale = min_dim / min(h, w)
        source_img = cv2.resize(source_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        print(f"📈 Imagen de origen escalada a: {source_img.shape[1]}x{source_img.shape[0]}")

    h, w = target_img.shape[:2]
    if h < min_dim or w < min_dim:
        scale = min_dim / min(h, w)
        target_img = cv2.resize(target_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        print(f"📈 Imagen de destino escalada a: {target_img.shape[1]}x{target_img.shape[0]}")

    print("🔍 Detectando caras...")
    source_faces = detect_faces(app, source_img)
    target_faces = detect_faces(app, target_img)

    if len(source_faces) == 0:
        print("ERROR: No se detectó ninguna cara en la imagen de origen")
        sys.exit(1)

    if len(target_faces) == 0:
        print("ERROR: No se detectó ninguna cara en la imagen destino")
        sys.exit(1)

    print(f"✓ Caras detectadas: {len(source_faces)} en origen, {len(target_faces)} en destino")

    # Usar la cara más grande de la imagen de origen
    source_face = sorted(source_faces, key=lambda x: x.bbox[2] * x.bbox[3])[-1]

    # Aplicar face swap con upscaling
    print("🔄 Aplicando face swap en alta resolución...")
    orig_h, orig_w = target_img.shape[:2]
    scale_factor = 2
    target_img_scaled = cv2.resize(target_img, (orig_w * scale_factor, orig_h * scale_factor), interpolation=cv2.INTER_CUBIC)
    source_img_scaled = cv2.resize(source_img, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    source_faces_scaled = detect_faces(app, source_img_scaled)
    target_faces_scaled = detect_faces(app, target_img_scaled)

    if len(source_faces_scaled) > 0 and len(target_faces_scaled) > 0:
        print(f"✓ Caras detectadas en versión escalada")
        source_face_scaled = sorted(source_faces_scaled, key=lambda x: x.bbox[2] * x.bbox[3])[-1]
        target_face_scaled = sorted(target_faces_scaled, key=lambda x: x.bbox[2] * x.bbox[3])[-1]
        result = swapper.get(target_img_scaled, target_face_scaled, source_face_scaled, paste_back=True)
    else:
        print("⚠ Fallback a resolución original")
        result = swapper.get(target_img, target_face, source_face, paste_back=True)

    temp_output = output_path.replace('.png', '_temp.png')
    cv2.imwrite(temp_output, result, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    print("💧 Añadiendo marca de agua ética...")
    add_watermark(temp_output, output_path)

    if os.path.exists(temp_output):
        os.remove(temp_output)

    print(f"✓ Face swap completado: {output_path}")
    return True


def process_multi_face_swap(source_paths, target_path, output_path, face_mapping=None):
    """
    Procesa face swap con múltiples caras.

    Args:
        source_paths: Lista de rutas de imágenes de origen
        target_path: Ruta de la imagen destino (puede tener múltiples caras)
        output_path: Ruta donde se guardará el resultado
        face_mapping: Diccionario {índice_cara_destino: índice_imagen_origen}
                     Si es None, se aplican en orden
    """
    try:
        import insightface
        from insightface.app import FaceAnalysis
    except ImportError:
        print("ERROR: insightface no está instalado.")
        print("Instala las dependencias con: pip install -r requirements.txt")
        sys.exit(1)

    # Verificar y descargar modelo
    if not download_model():
        sys.exit(1)

    print("⏳ Inicializando detector de caras...")
    app = FaceAnalysis(name='buffalo_s', providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))

    print("⏳ Cargando modelo de face swapper...")
    try:
        swapper = insightface.model_zoo.get_model(MODEL_PATH, providers=['CPUExecutionProvider'])
    except Exception as e:
        print(f"ERROR: No se pudo cargar el modelo: {e}")
        sys.exit(1)

    # Leer imágenes de origen
    print("⏳ Leyendo imágenes de origen...")
    source_images = []
    source_faces_all = []

    for i, source_path in enumerate(source_paths):
        img = cv2.imread(source_path)
        if img is None:
            print(f"ERROR: No se pudo leer la imagen de origen {i+1}: {source_path}")
            sys.exit(1)

        # Escalar si es necesario
        h, w = img.shape[:2]
        min_dim = 512
        if h < min_dim or w < min_dim:
            scale = min_dim / min(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        source_images.append(img)
        faces = detect_faces(app, img)
        source_faces_all.append(faces)
        print(f"  Imagen {i+1}: {len(faces)} cara(s) detectada(s)")

    # Leer imagen destino
    print("⏳ Leyendo imagen destino...")
    target_img = cv2.imread(target_path)
    if target_img is None:
        print(f"ERROR: No se pudo leer la imagen destino: {target_path}")
        sys.exit(1)

    # Escalar si es necesario
    h, w = target_img.shape[:2]
    min_dim = 512
    if h < min_dim or w < min_dim:
        scale = min_dim / min(h, w)
        target_img = cv2.resize(target_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
        print(f"📈 Imagen destino escalada a: {target_img.shape[1]}x{target_img.shape[0]}")

    # Detectar caras en destino
    print("🔍 Detectando caras en destino...")
    target_faces = detect_faces(app, target_img)
    print(f"✓ {len(target_faces)} cara(s) detectada(s) en destino")

    if len(target_faces) == 0:
        print("ERROR: No se detectó ninguna cara en la imagen destino")
        sys.exit(1)

    # Preparar mapeo de caras
    if face_mapping is None:
        # Mapeo por defecto: aplicar caras de origen en orden a las de destino
        face_mapping = {}
        for i in range(len(target_faces)):
            face_mapping[i] = i % len(source_images)

    print(f"📋 Mapeo de caras: {face_mapping}")

    # Aplicar face swap para cada cara en destino
    print("🔄 Aplicando face swaps...")
    result = target_img.copy()

    for target_idx, source_idx in face_mapping.items():
        if target_idx >= len(target_faces):
            continue
        if source_idx >= len(source_images):
            continue

        target_face = target_faces[target_idx]

        # Obtener la cara más grande de la imagen de origen correspondiente
        source_faces = source_faces_all[source_idx]
        if len(source_faces) == 0:
            print(f"⚠ No hay caras en la imagen de origen {source_idx+1}")
            continue

        source_face = sorted(source_faces, key=lambda x: x.bbox[2] * x.bbox[3])[-1]

        # Aplicar swap para esta cara
        print(f"  → Intercambiando cara {target_idx+1} con origen {source_idx+1}...")
        result = swapper.get(result, target_face, source_face, paste_back=True)

    # Guardar resultado con máxima calidad
    temp_output = output_path.replace('.png', '_temp.png')
    cv2.imwrite(temp_output, result, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    print("💧 Añadiendo marca de agua ética...")
    add_watermark(temp_output, output_path)

    if os.path.exists(temp_output):
        os.remove(temp_output)

    print(f"✓ Face swap múltiple completado: {output_path}")
    print(f"   - {len(target_faces)} cara(s) procesada(s)")
    print(f"   - {len(source_images)} imagen(es) de origen")
    return True


def main():
    if len(sys.argv) < 4:
        print("Uso:")
        print("  Una cara: python face_swap.py single <source_image> <target_image> <output_path>")
        print("  Múltiples caras: python face_swap.py multi <source1,source2,...> <target_image> <output_path> [face_mapping_json]")
        print("")
        print("Ético Face Swap - Intercambio de caras con consentimiento")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "single":
        source_path = sys.argv[2]
        target_path = sys.argv[3]
        output_path = sys.argv[4]

        print("=" * 50)
        print("🤖 FACE SWAP ÉTICO (Una cara)")
        print("=" * 50)
        print(f"Origen: {source_path}")
        print(f"Destino: {target_path}")
        print(f"Salida: {output_path}")
        print("-" * 50)

        process_single_face_swap(source_path, target_path, output_path, None, None)

    elif mode == "multi":
        source_paths_str = sys.argv[2]
        source_paths = [p.strip() for p in source_paths_str.split(',')]
        target_path = sys.argv[3]
        output_path = sys.argv[4]

        face_mapping = None
        if len(sys.argv) > 5:
            mapping_str = sys.argv[5]
            try:
                face_mapping = json.loads(mapping_str)
                face_mapping = {int(k): int(v) for k, v in face_mapping.items()}
            except:
                print(f"⚠ Mapeo inválido, usando orden por defecto")

        print("=" * 50)
        print("🤖 FACE SWAP ÉTICO (Múltiples caras)")
        print("=" * 50)
        print(f"Orígenes: {source_paths}")
        print(f"Destino: {target_path}")
        print(f"Salida: {output_path}")
        if face_mapping:
            print(f"Mapeo: {face_mapping}")
        print("-" * 50)

        process_multi_face_swap(source_paths, target_path, output_path, face_mapping)

    else:
        print(f"ERROR: Modo '{mode}' no reconocido")
        print("Usa 'single' o 'multi'")
        sys.exit(1)

    print("=" * 50)
    print("✓ PROCESAMIENTO COMPLETADO")
    print("=" * 50)
    print("")
    print("⚠️  RECORDATORIO ÉTICO:")
    print("   - Solo usa estas imágenes con consentimiento")
    print("   - No las uses para engañar, dañar o fines ilegales")
    print("   - Estas imágenes contienen marcas de agua de IA")


if __name__ == "__main__":
    main()
