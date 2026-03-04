import cv2
from picamera2 import Picamera2

class CameraManager:
    def __init__(self, width=640, height=480):
        print(f"[Camera] Inițializare la {width}x{height}...")
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"size": (width, height), "format": "RGB888"}
        )
        self.picam2.configure(config)

    def start(self):
        self.picam2.start()

    def stop(self):
        self.picam2.stop()

    def get_frame_bgr_flipped(self):
        """Returnează un cadru gata de afișat cu OpenCV (BGR și inversat)."""
        cadru_rgb = self.picam2.capture_array("main")
        cadru_bgr = cv2.cvtColor(cadru_rgb, cv2.COLOR_RGB2BGR)
        return cv2.flip(cadru_bgr, 1)