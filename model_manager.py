import threading
import queue
import numpy as np
from typing import List, Dict, Any
from ultralytics import YOLO

# 1. Nume bazat pe "ce face" (domeniu), nu pe "cum face" (tehnic)
class YoloObjectDetector:
    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model_path = model_path
        self.frame_queue = queue.Queue(maxsize=1)
        self.current_detections: List[Dict[str, Any]] = []
        self.running_state = False
        self.thread: threading.Thread | None = None

    # 3. Type hints pentru o curățenie impecabilă
    def start(self) -> None:
        """Pornește analiza în fundal, ascunzând complexitatea de thread-uri."""
        self.change_running_state(True)
        self.thread = threading.Thread(target=self._worker_loop, daemon=True) # daemon=True ajută la închiderea curată
        self.thread.start()

    def stop(self) -> None:
        """Oprește thread-ul curat."""
        self.change_running_state(False)
        if self.thread is not None:
            self.thread.join()

    def _worker_loop(self) -> None:
        """Această funcție rămâne privată (are '_' în față) pentru că aparține doar de implementarea curentă."""
        print("[YOLO] Încarc modelul pe nucleele hardware...")
        model = YOLO(self.model_path)
        print("[YOLO] Pregătit pentru analiză!")

        while self.running_state:
            try:
                # Așteptăm o imagine nouă (timeout 1 sec ca să putem verifica if running_state)
                cadru = self.frame_queue.get(timeout=1)
                rezultate = model(cadru, verbose=False)

                noile_detectii = []
                for r in rezultate:
                    for box in r.boxes:
                        noile_detectii.append({
                            "nume": r.names[int(box.cls[0])],
                            "coord": box.xyxy[0].cpu().numpy().astype(int)
                        })
                
                # Actualizăm starea internă cu ultimele detecții
                self.current_detections = noile_detectii
                
            except queue.Empty:
                continue

    def push_frame(self, frame: np.ndarray) -> None:
        """Primește un cadru. Dacă modelul este ocupat, cadrul este ignorat pentru a evita latența."""
        # 2. Modul Pythonic (și sigur pe thread-uri) de a gestiona o coadă de mărime 1
        try:
            self.frame_queue.put_nowait(frame)
        except queue.Full:
            pass # Coada e plină, modelul e ocupat, ignorăm cadrul vechi

    def get_detections(self) -> List[Dict[str, Any]]:
        """Returnează ce a găsit ultima dată pe ecran."""
        return self.current_detections
    
    def change_running_state(self, state: bool):
        self.running_state = state