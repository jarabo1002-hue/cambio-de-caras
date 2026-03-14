from PIL import Image, ImageDraw, ImageFilter
import os

def create_face_image(width, height, output_path, skin_color=(200, 150, 100)):
    """Crear una imagen de cara realista simple"""
    img = Image.new('RGB', (width, height), color=(50, 50, 80))
    draw = ImageDraw.Draw(img)
    
    cx, cy = width // 2, height // 2
    face_radius_x = width // 3
    face_radius_y = height // 3
    
    # Cara
    draw.ellipse([cx - face_radius_x, cy - face_radius_y, 
                  cx + face_radius_x, cy + face_radius_y], 
                 fill=skin_color)
    
    # Ojos
    eye_y = cy - face_radius_y // 3
    eye_offset_x = face_radius_x // 2
    eye_size = 15
    
    draw.ellipse([cx - eye_offset_x - eye_size, eye_y - eye_size,
                  cx - eye_offset_x + eye_size, eye_y + eye_size], fill=(255, 255, 255))
    draw.ellipse([cx + eye_offset_x - eye_size, eye_y - eye_size,
                  cx + eye_offset_x + eye_size, eye_y + eye_size], fill=(255, 255, 255))
    
    # Pupilas
    draw.ellipse([cx - eye_offset_x - 5, eye_y - 5,
                  cx - eye_offset_x + 5, eye_y + 5], fill=(0, 0, 0))
    draw.ellipse([cx + eye_offset_x - 5, eye_y - 5,
                  cx + eye_offset_x + 5, eye_y + 5], fill=(0, 0, 0))
    
    # Nariz
    nose_y = cy + 20
    draw.polygon([(cx, nose_y - 20), (cx - 15, nose_y + 10), (cx + 15, nose_y + 10)], 
                 fill=tuple(max(0, c - 30) for c in skin_color))
    
    # Boca
    mouth_y = cy + face_radius_y // 2
    draw.arc([cx - 40, mouth_y - 20, cx + 40, mouth_y + 40], 0, 180, fill=(180, 80, 80), width=8)
    
    # Cejas
    brow_y = eye_y - 25
    draw.line([(cx - eye_offset_x - 20, brow_y), (cx - eye_offset_x + 20, brow_y - 10)], 
              fill=(100, 80, 60), width=4)
    draw.line([(cx + eye_offset_x - 20, brow_y - 10), (cx + eye_offset_x + 20, brow_y)], 
              fill=(100, 80, 60), width=4)
    
    # Cabello
    draw.arc([cx - face_radius_x - 10, cy - face_radius_y - 40, 
              cx + face_radius_x + 10, cy + face_radius_y - 20], 
             180, 0, fill=(50, 30, 20), width=50)
    
    img = img.filter(ImageFilter.GaussianBlur(2))
    img.save(output_path, 'PNG', quality=100)
    print(f'Imagen creada: {output_path} ({width}x{height})')

os.makedirs('g:/curros/qwen/face-swap-ethical/test_images', exist_ok=True)
create_face_image(1024, 1024, 'g:/curros/qwen/face-swap-ethical/test_images/person1.png', skin_color=(220, 180, 140))
create_face_image(1024, 1024, 'g:/curros/qwen/face-swap-ethical/test_images/person2.png', skin_color=(150, 110, 80))
print('Imágenes creadas')
