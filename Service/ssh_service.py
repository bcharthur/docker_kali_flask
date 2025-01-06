# Service/ssh_service.py

from Entity.ssh_status import SSHStatus

class SSHService:
    def __init__(self):
        self.logs = []

    def enable_ssh_in_kali(self):
        self.add_log("Activation SSH dans Kali - (non implémenté)")

    def disable_ssh_in_kali(self):
        self.add_log("Désactivation SSH dans Kali - (non implémenté)")

    def check_ssh(self) -> SSHStatus:
        # ex. on considère qu'on est "connected" si le conteneur est running et qu'on a un port ?
        return SSHStatus(connected=False, port=2222)

    def add_log(self, msg):
        print(msg)
        self.logs.append(msg)

    def get_logs(self):
        return self.logs
