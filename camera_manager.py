from picamera2 import Picamera2

class CameraManager:
    def __init__(self, width=640, height=480):
        print(f"[CameraManager] Inițializare cameră ({width}x{height})...")
        self.picam2 = Picamera2()
        
        # Configurăm formatul optim pentru procesare rapidă
        config = self.picam2.create_preview_configuration(
            main={"size": (width, height), "format": "RGB888"}
        )
        self.picam2.configure(config)
        self.is_running = False

    def start(self):
        print("[CameraManager] Pornire flux video...")
        self.picam2.start()
        self.is_running = True

    def opreste(self):
        print("[CameraManager] Oprire sistem de captură...")
        if self.is_running:
            self.picam2.stop()
            self.is_running = False

    def ia_cadru(self):
        """Returnează un array (matrice) din stream-ul curent."""
        if not self.is_running:
            return None
        return self.picam2.capture_array("main")