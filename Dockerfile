# Usar una imagen de Python como base (la necesitamos para el AI)
FROM python:3.10-slim

# Instalar Node.js y dependencias del sistema para OpenCV
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la app
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./
COPY requirements.txt ./

# Instalar dependencias de Node y Python
RUN npm install --production
RUN pip install --no-cache-dir -r requirements.txt

# Descargar el modelo ONNX (usamos un script de python para esto)
COPY download_model.py .
RUN python download_model.py

# Copiar el resto del código
COPY . .

# Asegurar que los directorios de trabajo existen y tienen permisos
RUN mkdir -p uploads results && chmod 777 uploads results

# Exponer el puerto
EXPOSE 3000

# Comando para arrancar
CMD ["npm", "start"]
