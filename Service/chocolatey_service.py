# Service/chocolatey_service.py
import subprocess
import platform
from Entity.chocolatey_status import ChocolateyStatus

class ChocolateyService:
    def __init__(self):
        self.logs = []

    def check_chocolatey(self) -> ChocolateyStatus:
        """Vérifie si Chocolatey est installé (choco --version)"""
        status = ChocolateyStatus()
        if platform.system() == 'Windows':
            try:
                result = subprocess.run(["choco", "--version"], capture_output=True, text=True, check=True)
                status.installed = True
                status.version = result.stdout.strip()
            except (FileNotFoundError, subprocess.CalledProcessError):
                status.installed = False
        else:
            # Hors Windows, on considère que non pertinent
            status.installed = False
        return status

    def install_chocolatey(self):
        """
        Exemple:
          - Windows : via script d'installation powershell
        """
        self.logs.append("Installation de Chocolatey... (à implémenter)")

    def get_logs(self):
        return self.logs
