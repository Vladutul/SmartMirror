from ultralytics import YOLO

class ModelYOLO:
    def __init__(self, model_name="yolov8n.pt"):
        print(f"[ModelYOLO] Inițializare model {model_name}...")
        self.model = YOLO(model_name)
        print("[ModelYOLO] Încărcare completă!")

    def analizeaza_cadru(self, frame):
        """Trimite imaginea către model și returnează clasele detectate."""
        # rulăm detecția fără a umple terminalul
        rezultate = self.model(frame, verbose=False) 
        obiecte_detectate = []
        
        for r in rezultate:
            for c in r.boxes.cls:
                nume_clasa = r.names[int(c)]
                obiecte_detectate.append(nume_clasa)
                
        return obiecte_detectate