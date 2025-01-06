# Service/docker_service.py
import ctypes
import subprocess
import shlex
import platform
import sys

from Entity.docker_status import DockerStatus


class DockerService:
    def __init__(self):
        self.logs = []

    def check_and_ask_admin_rights(self):
        """
        Sous Windows, si pas admin, on relance le script en mode admin.
        Approche rudimentaire : usage de ctypes + ShellExecute.
        """
        if platform.system() == 'Windows':
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                if not is_admin:
                    self.add_log("Élévation de privilèges requise. Relancement en mode admin...")
                    # Relancer le script Python actuel avec "runas"
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                    sys.exit(0)
            except Exception as e:
                self.add_log(f"Impossible de vérifier/obtenir les droits admin : {e}")

    def check_docker(self) -> DockerStatus:
        """
        Vérifie si Docker est installé et si le service Docker est démarré (Windows ou Linux).
        """
        status = DockerStatus()
        # 1) Vérifier si Docker est installé
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
            status.installed = True
            status.version = result.stdout.strip()
        except (FileNotFoundError, subprocess.CalledProcessError):
            status.installed = False

        # 2) Vérifier si Docker est démarré (très simplifié)
        # Sous Windows, on pourrait checker un process "Docker Desktop", sur Linux "systemctl is-active docker"
        if status.installed:
            if platform.system() == "Windows":
                # Heuristique simplifiée : on ping docker ps
                try:
                    subprocess.run(["docker", "ps"], capture_output=True, text=True, check=True)
                    status.running = True
                except subprocess.CalledProcessError:
                    status.running = False
            else:
                # Sur Linux, on peut faire systemctl is-active docker
                try:
                    r = subprocess.run(["systemctl", "is-active", "docker"], capture_output=True, text=True)
                    if r.stdout.strip() == "active":
                        status.running = True
                    else:
                        status.running = False
                except:
                    # Si systemctl n'existe pas, on tente juste un docker ps
                    try:
                        subprocess.run(["docker", "ps"], capture_output=True, text=True, check=True)
                        status.running = True
                    except:
                        status.running = False
        return status

    def install_docker(self):
        """
        Exemples :
          - Sous Windows, installer Docker Desktop avec choco
          - Sous Linux, apt-get install docker.io
        """
        self.add_log("Installation de Docker... (exemple)")
        # ... implémentez la logique réelle

    def uninstall_docker(self):
        self.add_log("Désinstallation de Docker... (exemple)")

    def start_docker(self):
        """
        Sur Windows, on lance Docker Desktop. Sur Linux : systemctl start docker
        """
        self.add_log("Démarrage de Docker... (exemple)")

    def stop_docker(self):
        """
        Sur Windows, on arrête Docker Desktop, sur Linux : systemctl stop docker
        """
        self.add_log("Arrêt de Docker... (exemple)")

    # Logs
    def add_log(self, msg):
        print(msg)
        self.logs.append(msg)

    def get_logs(self):
        return self.logs
