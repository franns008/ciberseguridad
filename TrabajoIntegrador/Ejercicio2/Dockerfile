FROM python:3.12-slim

# Primero asegurarnos de que bash esté instalado
RUN apt-get update && apt-get install -y \
    bash curl git wget unzip tar rpm \
    && rm -rf /var/lib/apt/lists/*

# Instalar TRIVY
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Instalar TRUFFLEHOG 
RUN curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin

WORKDIR /app

CMD ["/bin/bash"]