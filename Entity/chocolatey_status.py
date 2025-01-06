# Entity/chocolatey_status.py
class ChocolateyStatus:
    def __init__(self, installed=False, version=None):
        self.installed = installed
        self.version = version

    def __repr__(self):
        return f"ChocolateyStatus(installed={self.installed}, version={self.version})"
