# Entity/kali_status.py
class KaliStatus:
    def __init__(self, image_exists=False, container_running=False):
        self.image_exists = image_exists
        self.container_running = container_running

    def __repr__(self):
        return f"KaliStatus(image_exists={self.image_exists}, container_running={self.container_running})"
