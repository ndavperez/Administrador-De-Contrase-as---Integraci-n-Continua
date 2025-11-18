FROM jenkins/jenkins:lts-jdk17

USER root

# Instalamos solo el cliente de Docker desde los repos de Debian
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# (Opcional pero recomendado) Dar permisos al usuario jenkins para usar docker
RUN groupadd -f docker && usermod -aG docker jenkins

USER jenkins
