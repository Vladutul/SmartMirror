import cv2
import time
from typing import Protocol, List, Dict, Any

# 1. Definim "Contractele" (Interfețele)
# Orice cameră viitoare va trebui să respecte această structură
class ICamera(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def get_frame(self) -> Any: ... # Returnează cadrul (ex: BGR flipped)

# Orice model de AI viitor va trebui să respecte această structură
class IModelWorker(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def push_frame(self, frame: Any) -> None: ...
    def get_detections(self) -> List[Dict[str, Any]]: ...

# 2. Clasa principală devine complet independentă de device-uri
class SmartMirrorApp:
    # Injectăm dependințele prin constructor
    def __init__(self, camera: ICamera, model: IModelWorker):
        self.camera = camera
        self.model = model
        self.is_running = False

    def run(self):
        print("--- START: Pregătire Unelte ---")
        self.start_components()
        self.set_running_state(True)
        
        time.sleep(3)
        print("--- RUNTIME: Sistemul rulează (Apasă ESC pentru ieșire) ---")

        try:
            while self.is_running:
                cadru = self.camera.get_frame()
                
                if cadru is not None:
                    self.model.push_frame(cadru.copy())
                    detectii = self.model.get_detections()
                    self._draw_detections(cadru, detectii)
                    cv2.imshow("Smart Mirror", cadru)

                if cv2.waitKey(1) & 0xFF == 27:
                    self.set_running_state(False)
                    break
        finally:
            self.cleanup()

    def _draw_detections(self, frame, detections):
        """O metodă separată doar pentru desenare (Single Responsibility)"""
        for obiect in detections:
            x1, y1, x2, y2 = obiect["coord"]
            nume = obiect["nume"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, nume, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def start_components(self):
        self.model.start()
        self.camera.start()

    def set_running_state(self, state: bool):
        self.is_running = state

    def cleanup(self):
        print("Încep oprirea componentelor...")
        self.camera.stop()
        self.model.stop()
        cv2.destroyAllWindows()
        print("Sistem oprit cu succes.")

# 3. Asamblarea aplicației se face la exterior (Compozitie)
if __name__ == "__main__":
    from camera_manager import PiCamera # Implementarea concretă
    from model_manager import YoloObjectDetector     # Implementarea concretă
    
    # Aici poți schimba ușor cu: 
    # camera = IpCameraManager("192.168.1.100")
    # model = MediaPipeWorker()
    
    my_camera = PiCamera()
    my_model = YoloObjectDetector()
    
    app = SmartMirrorApp(camera=my_camera, model=my_model)
    app.run()