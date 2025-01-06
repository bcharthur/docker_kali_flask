# Entity/kali_status.py
class KaliStatus:
    def __init__(self, image_exists=False, container_running=False, image_name=None, container_name=None):
        self.image_exists = image_exists
        self.container_running = container_running
        self.image_name = image_name
        self.container_name = container_name

    def __repr__(self):
        return (f"KaliStatus(image_exists={self.image_exists}, "
                f"container_running={self.container_running}, "
                f"image_name={self.image_name}, "
                f"container_name={self.container_name})")
