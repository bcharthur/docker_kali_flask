# --------------------------------
#  Dockerfile : Kali avec SSH, Outils et SecLists
# --------------------------------
FROM kalilinux/kali-rolling

# Éviter les interactions apt
ENV DEBIAN_FRONTEND=noninteractive

# Variables d'arguments
ARG SSH_ROOT_PASSWORD=toor
ARG SSH_USER=kaliuser
ARG SSH_PASSWORD=kali

# Mise à jour & installation d'outils
RUN apt-get update && \
    apt-get install -y \
        kali-linux-default \
        openssh-server \
        nmap \
        net-tools \
        lsb-release \
        git \
        wget \
        sudo && \
    rm -rf /var/lib/apt/lists/*

# Dossier run/sshd
RUN mkdir -p /var/run/sshd

# Mot de passe root
RUN echo "root:${SSH_ROOT_PASSWORD}" | chpasswd

# Création d'un user normal
RUN useradd -ms /bin/bash --uid 1000 --gid 0 "${SSH_USER}" \
    && usermod -aG sudo "${SSH_USER}" \
    && echo "${SSH_USER}:${SSH_PASSWORD}" | chpasswd

# Autoriser le root login en SSH
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# Autoriser l’authentification par mot de passe
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose port 22
EXPOSE 22

# Installer SecLists
RUN git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists && \
    chmod -R 755 /usr/share/seclists

# Lancer SSH en mode "foreground"
CMD ["/usr/sbin/sshd", "-D"]
