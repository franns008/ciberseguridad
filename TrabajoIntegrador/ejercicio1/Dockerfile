FROM ubuntu:22.04 

# Configurar instalación no interactiva
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Preconfigurar postfix para instalación no interactiva
RUN echo "postfix postfix/mailname string localhost" | debconf-set-selections
RUN echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections

# Instalación de herramientas básicas (incluyendo git para Lynis) - solo un apt update inicial
RUN apt-get update && apt-get install -y \
    openssh-server \
    net-tools \
    vim \
    ufw \
    rsyslog \
    cron \
    postfix \
    telnetd \
    xinetd \
    redis-server \
    sudo \
    debconf-utils \
    wget \
    curl \
    gnupg \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Lynis desde Git (versión más reciente) - NO hacer apt update para mantener paquetes vulnerables
RUN git clone https://github.com/CISOfy/lynis /opt/lynis \
    && chmod +x /opt/lynis/lynis \
    && echo '#!/bin/bash\ncd /opt/lynis && ./lynis "$@"' > /usr/local/bin/lynis \
    && chmod +x /usr/local/bin/lynis

# Configurar SSH para permitir el servicio
RUN mkdir /var/run/sshd
RUN mkdir -p /root/.ssh



# Configurar Redis de manera insegura
RUN sed -i 's/bind 127.0.0.1 ::1/bind 0.0.0.0/' /etc/redis/redis.conf \
    && sed -i 's/protected-mode yes/protected-mode no/' /etc/redis/redis.conf \
    && sed -i 's/# requirepass foobared/# requirepass/' /etc/redis/redis.conf \
    && echo "timeout 0" >> /etc/redis/redis.conf \
    && echo "tcp-keepalive 0" >> /etc/redis/redis.conf

# Copiar el binario precompilado (sin exponer el código fuente)
COPY vulnerabilizar /usr/local/bin/vulnerabilizar
RUN chmod +x /usr/local/bin/vulnerabilizar

# Crear directorios necesarios para el laboratorio
RUN mkdir -p /var/vulnerable
RUN mkdir -p /tmp/vulnerable

EXPOSE 22

# Script de inicio que ejecuta las vulnerabilidades y mantiene servicios activos
RUN echo '#!/bin/bash\n\
echo "Iniciando servicios del laboratorio..."\n\
/usr/local/bin/vulnerabilizar\n\
echo "Iniciando servicios de red..."\n\
service ssh start\n\
service rsyslog start\n\
service cron start\n\
service postfix start || true\n\
service redis-server start || true\n\
service xinetd start || true\n\
echo "Servicios iniciados. Sistema listo para auditoría."\n\
tail -f /var/log/auth.log /var/log/syslog 2>/dev/null || tail -f /dev/null' > /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]