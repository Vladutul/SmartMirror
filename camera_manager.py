import cv2
import numpy as np # Adăugat opțional, doar pentru type hinting (vezi get_frame)
from picamera2 import Picamera2

# 1. Nume clar și specific pentru implementarea hardware
class PiCamera:
    def __init__(self, width: int = 640, height: int = 480):
        print(f"[PiCamera] Inițializare la {width}x{height}...")
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"size": (width, height), "format": "RGB888"}
        )
        self.picam2.configure(config)

    # 3. Type hints (-> None) pentru a indica faptul că nu returnează nimic
    def start(self) -> None:
        self.picam2.start()

    def stop(self) -> None:
        self.picam2.stop()

    # 2. Nume standardizat. Orice cameră vom adăuga pe viitor va avea metoda "get_frame"
    def get_frame(self) -> np.ndarray:
        """Returnează un cadru gata de afișat (convertit în BGR și efect de oglindă)."""
        cadru_rgb = self.picam2.capture_array("main")
        
        # Procesarea internă (specifică acestei camere) rămâne ascunsă aici
        cadru_bgr = cv2.cvtColor(cadru_rgb, cv2.COLOR_RGB2BGR)
        cadru_inversat = cv2.flip(cadru_bgr, 1)
        
        return cadru_inversat