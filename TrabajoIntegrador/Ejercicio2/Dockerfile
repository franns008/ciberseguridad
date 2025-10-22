# Imagen base ligera con Python y utilidades
FROM python:3.12-slim

# Instalar dependencias básicas y herramientas
RUN apt-get update && apt-get install -y \
    curl git wget unzip tar rpm \
    && rm -rf /var/lib/apt/lists/*

# Instalar TRIVY
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh && \
    mv ./bin/trivy /usr/local/bin/ && rm -rf ./bin

# Instalar TRUFFLEHOG (versión Linux x86_64)
RUN wget -O /usr/local/bin/trufflehog \
    https://github.com/trufflesecurity/trufflehog/releases/latest/download/trufflehog_linux_amd64 && \
    chmod +x /usr/local/bin/trufflehog

# Crear directorio de trabajo
WORKDIR /app

# Declarar el volumen donde se montará tu código
VOLUME ["/app/webapp"]

# Comando por defecto
CMD ["/bin/bash"]
