# Service/console_service.py
import subprocess
import shlex

class ConsoleService:
    def __init__(self):
        self.logs = []

    def execute_command_in_container(self, container_name: str, command: str):
        if not command:
            self.logs.append("[Aucune commande saisie]")
            return
        full_cmd = f"docker exec {container_name} {command}"
        self.logs.append(f"Exécution: {full_cmd}")
        try:
            result = subprocess.run(shlex.split(full_cmd), capture_output=True, text=True, check=True)
            out = result.stdout.strip()
            err = result.stderr.strip()
            if out:
                self.logs.append(out)
            if err:
                self.logs.append(f"Erreur: {err}")
        except subprocess.CalledProcessError as e:
            self.logs.append(f"Erreur d'exécution: {e.stderr.strip()}")

    def get_logs(self):
        return self.logs
