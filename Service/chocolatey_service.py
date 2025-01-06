# Service/chocolatey_service.py
import subprocess
import shlex
import platform
from Entity.chocolatey_status import ChocolateyStatus

class ChocolateyService:
    def __init__(self):
        self.logs = []

    def check_chocolatey(self) -> ChocolateyStatus:
        status = ChocolateyStatus()
        if platform.system() == 'Windows':
            try:
                result = subprocess.run(["choco", "--version"], capture_output=True, text=True, check=True)
                status.installed = True
                status.version = result.stdout.strip()
            except:
                status.installed = False
        else:
            status.installed = False
        return status

    def install_chocolatey(self):
        self.add_log("Installation de Chocolatey... (exemple)")

    def uninstall_chocolatey(self):
        self.add_log("Désinstallation de Chocolatey... (exemple)")

    def add_log(self, msg):
        print(msg)
        self.logs.append(msg)

    def get_logs(self):
        return self.logs
