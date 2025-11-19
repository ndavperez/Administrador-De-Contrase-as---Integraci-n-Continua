FROM jenkins/jenkins:lts-jdk17

USER root


RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh && \
    sh /tmp/get-docker.sh && \
    rm -rf /var/lib/apt/lists/* /tmp/get-docker.sh


RUN groupadd -f docker && usermod -aG docker jenkins

USER jenkins