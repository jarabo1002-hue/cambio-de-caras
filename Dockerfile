FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    curl \
        gnupg \
            libgl1 \
                libglib2.0-0 \
                    libsm6 \
                        libxext6 \
                            && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
                                && apt-get install -y nodejs \
                                    && rm -rf /var/lib/apt/lists/*

                                    WORKDIR /app

                                    COPY package*.json ./
                                    COPY requirements.txt ./

                                    RUN npm install --production
                                    RUN pip install --no-cache-dir -r requirements.txt

                                    COPY download_model.py .
                                    RUN python download_model.py

                                    COPY . .

                                    RUN mkdir -p uploads results && chmod 777 uploads results

                                    EXPOSE 3000

                                    CMD ["npm", "start"]
                                    
