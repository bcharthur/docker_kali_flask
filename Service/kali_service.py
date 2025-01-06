# Service/kali_service.py
import subprocess
import shlex
import json
from Entity.kali_status import KaliStatus

class KaliService:
    def __init__(self):
        self.logs = []

    def check_kali(self) -> KaliStatus:
        """Vérifie si l'image my_kali_image existe et si le conteneur my_kali_container tourne."""
        status = KaliStatus()

        # Vérifier l'image
        if self._image_exists("my_kali_image"):
            status.image_exists = True

        # Vérifier si conteneur 'my_kali_container' est running
        info = self._get_container_info("my_kali_container")
        if info and info["State"].lower() == "running":
            status.container_running = True

        return status

    def install_kali(self):
        """
        Exécute docker build + docker run
        """
        self.logs.append("Installation de Kali : docker build + run")

        # Docker build
        try:
            cmd_build = "docker build -t my_kali_image ."
            build_result = subprocess.run(shlex.split(cmd_build), capture_output=True, text=True, check=True)
            self.logs.append(build_result.stdout)
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur build: {e.stderr}")

        # Docker run
        try:
            cmd_run = "docker run -d --name my_kali_container -p 2222:22 my_kali_image"
            run_result = subprocess.run(shlex.split(cmd_run), capture_output=True, text=True, check=True)
            self.logs.append(run_result.stdout)
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur run: {e.stderr}")

    # --------------- Internes ---------------
    def _image_exists(self, image_name) -> bool:
        try:
            cmd = "docker images --format '{{.Repository}}'"
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if image_name in r.stdout.split():
                return True
        except:
            pass
        return False

    def _get_container_info(self, container_name):
        try:
            cmd = "docker ps -a --format '{{json .}}'"
            r = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
            for line in r.stdout.strip().split('\n'):
                data = json.loads(line)
                if data["Names"] == container_name:
                    return data
        except:
            pass
        return None

    def get_logs(self):
        return self.logs
