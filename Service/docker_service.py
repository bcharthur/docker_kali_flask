# Service/docker_service.py
import subprocess
import shlex
import platform
import time
from Entity.docker_status import DockerStatus


class DockerService:
    def __init__(self):
        self.logs = []

    def check_docker(self) -> DockerStatus:
        """Vérifie si Docker est installé (docker --version) et renvoie le statut."""
        status = DockerStatus()
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
            status.installed = True
            status.version = result.stdout.strip()
        except (FileNotFoundError, subprocess.CalledProcessError):
            status.installed = False
        return status

    def install_docker(self):
        """
        Installe Docker en fonction du système d'exploitation :
         - Sous Windows : Utilise Chocolatey pour installer Docker Desktop.
         - Sous Linux (Ubuntu/Debian) : Utilise apt-get pour installer docker.io.
        """
        self.logs.append("=== Début de l'installation de Docker ===")
        os_type = platform.system()
        self.logs.append(f"Système d'exploitation détecté : {os_type}")

        if os_type == "Windows":
            self.logs.append("Installation de Docker Desktop via Chocolatey...")
            try:
                # Vérifier si Chocolatey est installé
                result = subprocess.run(["choco", "--version"], capture_output=True, text=True)
                if result.returncode != 0:
                    self.logs.append("Chocolatey n'est pas installé. Installation de Chocolatey...")
                    # Installer Chocolatey
                    install_cmd = "Set-ExecutionPolicy Bypass -Scope Process -Force; " \
                                  "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
                    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", install_cmd],
                                   check=True)
                    self.logs.append("Chocolatey installé avec succès.")
                else:
                    self.logs.append("Chocolatey est déjà installé.")

                # Installer Docker Desktop
                install_docker_cmd = ["choco", "install", "docker-desktop", "-y"]
                process = subprocess.Popen(install_docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           text=True)

                for line in process.stdout:
                    self.logs.append(line.strip())
                    print(line, end='')  # Afficher les logs en temps réel

                process.wait()
                if process.returncode == 0:
                    self.logs.append("Docker Desktop installé avec succès.")
                else:
                    self.logs.append(
                        f"Échec de l'installation de Docker Desktop avec le code de retour {process.returncode}.")
            except subprocess.CalledProcessError as e:
                self.logs.append(f"Erreur lors de l'installation de Docker Desktop : {e}")
        elif os_type == "Linux":
            # Note : platform.linux_distribution() est déprécié depuis Python 3.5 et supprimé dans Python 3.8
            # Utilisez distro à la place si nécessaire
            distro = platform.platform().lower()
            self.logs.append(f"Distribution Linux détectée : {distro}")
            if "ubuntu" in distro or "debian" in distro:
                self.logs.append("Installation de Docker via apt-get...")
                try:
                    subprocess.run(["sudo", "apt-get", "update"], check=True)
                    subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"], check=True)
                    subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
                    subprocess.run(["sudo", "systemctl", "enable", "docker"], check=True)
                    self.logs.append("Docker installé et démarré avec succès.")
                except subprocess.CalledProcessError as e:
                    self.logs.append(f"Erreur lors de l'installation de Docker : {e}")
            else:
                self.logs.append(f"Distribution Linux non supportée pour l'installation automatique : {distro}")
        else:
            self.logs.append(f"Système d'exploitation non supporté pour l'installation automatique : {os_type}")

        self.logs.append("=== Fin de l'installation de Docker ===")

    def get_logs(self):
        current_logs = self.logs.copy()
        self.logs = []  # Réinitialiser les logs après les avoir récupérés
        return current_logs
