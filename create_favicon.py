from PIL import Image, ImageDraw

# Create 32x32 icon
img = Image.new('RGB', (32, 32), color='#6366f1')
draw = ImageDraw.Draw(img)

# White circle for face
draw.ellipse([4, 4, 28, 28], fill='white')

# Purple eyes
draw.ellipse([10, 10, 14, 14], fill='#6366f1')
draw.ellipse([18, 10, 22, 14], fill='#6366f1')

# Smile
draw.arc([10, 12, 22, 22], 0, 180, fill='white', width=2)

# Save as ICO
img.save('public/favicon.ico', format='ICO')
print('✓ Favicon created: public/favicon.ico')
