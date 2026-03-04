import threading
import queue
from ultralytics import YOLO

class YoloWorker:
    def __init__(self, model_path="yolov8n.pt"):
        self.model_path = model_path
        self.frame_queue = queue.Queue(maxsize=1)
        self.current_detections = []
        self.is_running = False
        self.thread = None

    def start(self):
        """Pornește thread-ul pentru analiză în fundal."""
        self.is_running = True
        self.thread = threading.Thread(target=self._worker_loop)
        self.thread.start()

    def stop(self):
        """Oprește thread-ul curat."""
        self.is_running = False
        if self.thread is not None:
            self.thread.join()

    def _worker_loop(self):
        """Această funcție rulează izolat pe thread-ul secundar."""
        print("[YOLO] Încarc modelul pe nucleele hardware...")
        model = YOLO(self.model_path)
        print("[YOLO] Pregătit pentru analiză!")

        while self.is_running:
            try:
                # Așteptăm o imagine nouă (timeout 1 sec ca să putem verifica if is_running)
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

    def push_frame(self, frame):
        """Primește un cadru de la programul principal (dacă e liber)."""
        if self.frame_queue.empty():
            self.frame_queue.put(frame)

    def get_detections(self):
        """Returnează ce a găsit ultima dată pe ecran."""
        return self.current_detections