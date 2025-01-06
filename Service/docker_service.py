# Service/docker_service.py
import subprocess
import shlex
import platform
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
        Exemple d'installation, à adapter :
         - Sous Windows : choco install docker-desktop
         - Sous Linux : apt-get install docker.io
        """
        self.logs.append("Installation Docker... (à implémenter)")

    def get_logs(self):
        return self.logs
