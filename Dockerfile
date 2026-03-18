# Face Swap Ético - Docker Optimizado
# Versión: Local-only

FROM python:3.10-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Establecer directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias de Node
COPY package*.json ./
RUN npm install --production

# Copiar e instalar dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelo
COPY download_model.py .
RUN python download_model.py

# Copiar el resto del código
COPY . .

# Crear directorios para archivos temporales
RUN mkdir -p uploads results && chmod 777 uploads results

# Exponer puerto
EXPOSE 3000

# Variables de entorno
ENV NODE_ENV=production
ENV PORT=3000

# Comando de inicio
CMD ["node", "server.js"]
