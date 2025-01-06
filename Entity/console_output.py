# Entity/console_output.py

class ConsoleOutput:
    """
    Stocke le résultat d'une commande ou logs de console
    """
    def __init__(self, output="", error=""):
        self.output = output
        self.error = error

    def __repr__(self):
        return f"ConsoleOutput(output={self.output}, error={self.error})"
