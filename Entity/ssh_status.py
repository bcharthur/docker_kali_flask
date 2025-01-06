# Entity/ssh_status.py
class SSHStatus:
    def __init__(self, connected=False, port=22):
        self.connected = connected
        self.port = port

    def __repr__(self):
        return f"SSHStatus(connected={self.connected}, port={self.port})"
