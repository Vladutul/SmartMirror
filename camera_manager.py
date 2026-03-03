from picamera2 import Picamera2

class CameraModule:
    def __init__(self, width=640, height=480):
        # This covers "Init Camera"
        print(f"[Camera] Inițializare cameră la {width}x{height}...")
        self.cam = Picamera2()
        config = self.cam.create_preview_configuration(
            main={"size": (width, height), "format": "RGB888"}
        )
        self.cam.configure(config)
        self.running = False

    def start(self):
        self.cam.start()
        self.running = True
        print("[Camera] Cameră pornită.")

    def get_frame(self):
        # This covers "Capture Frame"
        if not self.running:
            return None
        return self.cam.capture_array("main")

    def stop(self):
        self.cam.stop()
        self.running = False