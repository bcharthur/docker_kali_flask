# Entity/docker_status.py

class DockerStatus:
    def __init__(self, installed=False, version=None, running=False):
        self.installed = installed
        self.version = version
        self.running = running

    def __repr__(self):
        return f"DockerStatus(installed={self.installed}, version={self.version}, running={self.running})"
