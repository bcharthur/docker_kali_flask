# Service/kali_service.py
import subprocess
import shlex
import json
import time
import paramiko

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
        1) docker build
        2) docker run
        3) connexion SSH (sshpass)
        """
        self.logs.append("=== Installation de Kali ===")

        # 1) Docker build
        try:
            cmd_build = "docker build -t my_kali_image ."
            print(f"Exécution de la commande : {cmd_build}\n")

            # Lance le process en mode “streaming”
            process = subprocess.Popen(
                shlex.split(cmd_build),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # on mélange stdout/stderr
                text=True,  # strings plutôt que bytes
                bufsize=1  # unbuffered ou ligne par ligne
            )

            # Lire les sorties ligne par ligne
            for line in process.stdout:
                print(line, end='')  # 'end' pour éviter un double \n

            # Attendre la fin du process, récupérer le code retour
            returncode = process.wait()
            if returncode != 0:
                print(f"\nLe build a échoué avec un code de retour {returncode}")
            else:
                print("\nBuild terminé avec succès !")
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur build: {e.stderr}")
            return

        # 2) Docker run
        try:
            cmd_run = "docker run -d --name my_kali_container -p 2222:22 my_kali_image"
            self.logs.append(f"Run cmd: {cmd_run}")
            run_result = subprocess.run(shlex.split(cmd_run), capture_output=True, text=True, check=True)
            container_id = run_result.stdout.strip()
            self.logs.append(f"Conteneur lancé : {container_id}")
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur run: {e.stderr}")
            return

        # Attendre quelques secondes que le service SSH soit opérationnel
        time.sleep(5)
        # 3) Connexion SSH via sshpass
        #    On suppose user = kaliuser, pass = kali, port 2222
        try:
            cmd_ssh = (
                "sshpass -p kali ssh -o StrictHostKeyChecking=no "
                "-p 2222 kaliuser@127.0.0.1 whoami"
            )
            self.logs.append(f"SSH cmd: {cmd_ssh}")
            ssh_result = subprocess.run(shlex.split(cmd_ssh), capture_output=True, text=True, check=True)
            out = ssh_result.stdout.strip()
            self.logs.append(f"Connexion SSH OK. Sortie: {out}")
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur SSH: {e.stderr}")

            # 4) Essayer la connexion SSH via Paramiko
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    hostname="127.0.0.1",
                    port=2222,
                    username="kaliuser",
                    password="kali"
                )
                stdin, stdout, stderr = client.exec_command("whoami")
                output = stdout.read().decode().strip()
                print("Connexion SSH OK, whoami =>", output)
                client.close()
            except Exception as e:
                print("Erreur SSH Paramiko :", e)

    # --------------- Méthodes internes ---------------
    def _image_exists(self, image_name) -> bool:
        try:
            cmd = f"docker images -q {image_name}"
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            # Si la commande renvoie quelque chose sur stdout, l'image existe
            if r.stdout.strip():
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
