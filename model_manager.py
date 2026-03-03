from ultralytics import YOLO

class FaceModel:
    def __init__(self, model_path="yolov8n.pt"):
        # This covers "Load YOLO Model" from your flowchart
        print(f"[Model] Încărcare model {model_path} în memorie...")
        self.model = YOLO(model_path)
        print("[Model] Model încărcat.")

    def detect(self, frame):
        # This covers "YOLO Inference"
        results = self.model(frame, verbose=False) # verbose=False ca să nu facă spam în terminal
        return results