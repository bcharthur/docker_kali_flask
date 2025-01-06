# Service/kali_service.py
import subprocess
import shlex
import json
from Entity.kali_status import KaliStatus

class KaliService:
    def __init__(self):
        self.logs = []

    def check_kali(self) -> KaliStatus:
        status = KaliStatus()

        # 1) Vérifier si l'image my_kali_image existe
        if self._image_exists("my_kali_image"):
            status.image_exists = True

        # 2) Vérifier si conteneur my_kali_container est running
        info = self._get_container_info("my_kali_container")
        if info:
            if info["State"].lower() == "running":
                status.container_running = True

        return status

    def build_kali_image(self):
        self.add_log("Construction de l'image Kali (docker build -t my_kali_image .)")
        try:
            cmd = "docker build -t my_kali_image ."
            subprocess.run(shlex.split(cmd), check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.add_log(f"Erreur: {e.stderr}")

    def run_kali_container(self):
        self.add_log("Démarrage du conteneur Kali (docker run...)")
        try:
            cmd = "docker run -d --name my_kali_container -p 2222:22 my_kali_image"
            r = subprocess.run(shlex.split(cmd), check=True, capture_output=True, text=True)
            self.add_log(r.stdout.strip())
        except subprocess.CalledProcessError as e:
            self.add_log(f"Erreur: {e.stderr}")

    def stop_kali_container(self):
        self.add_log("Arrêt du conteneur Kali (docker stop my_kali_container)")
        try:
            subprocess.run(["docker", "stop", "my_kali_container"], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.add_log(f"Erreur: {e.stderr}")

    def uninstall_kali(self):
        """
        Stop + rm conteneur, rmi image
        """
        self.add_log("Désinstallation de Kali (stop + rm + rmi)")
        try:
            subprocess.run(["docker", "stop", "my_kali_container"], check=False, capture_output=True, text=True)
            subprocess.run(["docker", "rm", "my_kali_container"], check=False, capture_output=True, text=True)
            subprocess.run(["docker", "rmi", "my_kali_image"], check=False, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.add_log(f"Erreur: {e.stderr}")

    # ---------------------
    # MÉTHODES INTERNES
    # ---------------------
    def _image_exists(self, image_name):
        try:
            cmd = f"docker images --format '{{{{.Repository}}}}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if image_name in result.stdout.splitlines():
                return True
        except:
            pass
        return False

    def _get_container_info(self, container_name):
        try:
            cmd = "docker ps -a --format '{{json .}}'"
            r = subprocess.run(shlex.split(cmd), check=True, capture_output=True, text=True)
            for line in r.stdout.strip().split('\n'):
                data = json.loads(line)
                if data["Names"] == container_name:
                    return data
        except:
            pass
        return None

    def add_log(self, msg):
        print(msg)
        self.logs.append(msg)

    def get_logs(self):
        return self.logs
