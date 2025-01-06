# Service/kali_service.py
import subprocess
import shlex
import json
import time
import paramiko

from Entity.kali_status import KaliStatus

class KaliService:
    IMAGE_NAME = "my_kali_image"
    CONTAINER_NAME = "my_kali_container"
    SSH_PORT = 2222
    SSH_USERNAME = "kaliuser"
    SSH_PASSWORD = "kali"

    def __init__(self):
        self.logs = []

    def check_kali(self) -> KaliStatus:
        """Vérifie si l'image my_kali_image existe et si le conteneur my_kali_container tourne."""
        status = KaliStatus(
            image_name=self.IMAGE_NAME,
            container_name=self.CONTAINER_NAME
        )

        # Vérifier l'image
        if self._image_exists(self.IMAGE_NAME):
            status.image_exists = True

        # Vérifier si conteneur 'my_kali_container' est running
        info = self._get_container_info(self.CONTAINER_NAME)
        if info and info["State"].lower() == "running":
            status.container_running = True

        return status

    def install_kali(self):
        """
        1) docker build
        2) docker run
        3) connexion SSH via Paramiko
        """
        self.logs.append("=== Installation de Kali ===")

        # 1) Docker build
        try:
            cmd_build = f"docker build -t {self.IMAGE_NAME} ."
            print(f"Exécution de la commande : {cmd_build}\n")

            # Lance le process en mode “streaming”
            process = subprocess.Popen(
                shlex.split(cmd_build),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # on mélange stdout/stderr
                text=True,                 # strings plutôt que bytes
                bufsize=1                  # unbuffered ou ligne par ligne
            )

            # Lire les sorties ligne par ligne
            for line in process.stdout:
                print(line, end='')  # 'end' pour éviter un double \n
                self.logs.append(line.strip())

            # Attendre la fin du process, récupérer le code retour
            returncode = process.wait()
            if returncode != 0:
                error_msg = f"\nLe build a échoué avec un code de retour {returncode}"
                print(error_msg)
                self.logs.append(error_msg)
                return
            else:
                success_msg = "\nBuild terminé avec succès !"
                print(success_msg)
                self.logs.append(success_msg)
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur build: {e.stderr}")
            return

        # 2) Docker run
        try:
            cmd_run = f"docker run -d --name {self.CONTAINER_NAME} -p {self.SSH_PORT}:22 {self.IMAGE_NAME}"
            self.logs.append(f"Run cmd: {cmd_run}")
            print(f"Exécution de la commande : {cmd_run}")
            run_result = subprocess.run(shlex.split(cmd_run), capture_output=True, text=True, check=True)
            container_id = run_result.stdout.strip()
            self.logs.append(f"Conteneur lancé : {container_id}")
            print(f"Conteneur lancé : {container_id}")
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur run: {e.stderr}")
            print(f"Erreur run: {e.stderr}")
            return

        # Attendre quelques secondes que le service SSH soit opérationnel
        time.sleep(10)  # Augmenté pour laisser plus de temps à SSHD de démarrer

        # 3) Connexion SSH via Paramiko
        try:
            print("Tentative de connexion SSH via Paramiko...")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname="127.0.0.1",
                port=self.SSH_PORT,
                username=self.SSH_USERNAME,
                password=self.SSH_PASSWORD,
                timeout=10  # Timeout pour éviter de bloquer trop longtemps
            )
            stdin, stdout, stderr = client.exec_command("whoami")
            output = stdout.read().decode().strip()
            print("Connexion SSH OK, whoami =>", output)
            self.logs.append(f"Connexion SSH OK. Sortie: {output}")
            client.close()
        except Exception as e:
            error_msg = f"Erreur SSH Paramiko : {e}"
            print(error_msg)
            self.logs.append(error_msg)

    def execute_command(self, command: str) -> str:
        """
        Exécute une commande SSH sur le conteneur Kali et retourne la sortie.
        """
        self.logs.append(f"=== Exécution de la commande : {command} ===")
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname="127.0.0.1",
                port=self.SSH_PORT,
                username=self.SSH_USERNAME,
                password=self.SSH_PASSWORD,
                timeout=10
            )
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            client.close()

            if output:
                self.logs.append(f"Sortie de la commande :\n{output}")
                return output
            if error:
                self.logs.append(f"Erreur de la commande :\n{error}")
                return error
            return "Commande exécutée sans sortie."
        except Exception as e:
            error_msg = f"Erreur lors de l'exécution de la commande SSH : {e}"
            self.logs.append(error_msg)
            return error_msg

    # --------------- Méthodes internes ---------------
    def _image_exists(self, image_name) -> bool:
        try:
            cmd = f"docker images -q {image_name}"
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            # Si la commande renvoie quelque chose sur stdout, l'image existe
            if r.stdout.strip():
                return True
        except Exception as e:
            self.logs.append(f"Erreur dans _image_exists: {e}")
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
        except Exception as e:
            self.logs.append(f"Erreur dans _get_container_info: {e}")
            pass
        return None

    def get_logs(self):
        return self.logs
