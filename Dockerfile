# Dockerfile : Kali avec SSH, Outils, SecLists, nmap fonctionnel
FROM kalilinux/kali-rolling

ARG SSH_ROOT_PASSWORD=toor
ENV DEBIAN_FRONTEND=noninteractive

# 1) Mise à jour + installation de paquets (dont libcap2-bin pour setcap)
RUN apt-get update && \
    apt-get install -y \
        kali-linux-default \
        openssh-server \
        nmap \
        net-tools \
        lsb-release \
        git \
        wget \
        libcap2-bin && \
    rm -rf /var/lib/apt/lists/*

# 2) Autoriser SSH (root)
RUN mkdir -p /var/run/sshd
RUN echo "root:${SSH_ROOT_PASSWORD}" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# 3) Donner la capacité raw à nmap (pour éviter "Operation not permitted")
# Selon la version de Kali, nmap peut être dans /usr/bin/nmap ou /usr/lib/nmap/nmap
RUN setcap cap_net_raw+eip /usr/bin/nmap || true
RUN setcap cap_net_raw+eip /usr/lib/nmap/nmap || true

# 4) Installer SecLists
RUN git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
RUN chmod -R 755 /usr/share/seclists

# 5) Exposer le port 22
EXPOSE 22

# 6) Lancer SSH en foreground
CMD ["/usr/sbin/sshd", "-D"]
