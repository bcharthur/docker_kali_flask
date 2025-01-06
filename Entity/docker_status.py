# Entity/docker_status.py
class DockerStatus:
    def __init__(self, installed=False, version=None):
        self.installed = installed
        self.version = version

    def __repr__(self):
        return f"DockerStatus(installed={self.installed}, version={self.version})"
