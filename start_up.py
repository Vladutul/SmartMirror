import time
from camera import CameraModule
from model import FaceModel
import cv2 # Ai nevoie de OpenCV pentru a întoarce imaginea cum e în diagramă

def run_mirror():
    print("=== START: Pregătire Unelte ===")
    
    # 1. Init Camera
    my_camera = CameraModule()
    my_camera.start()
    
    # 2. Load YOLO Model
    my_model = FaceModel()
    
    print("=== RUNTIME: Sistemul rulează ===")
    try:
        while True:
            # Capture Frame
            frame = my_camera.get_frame()
            
            # Valid Frame?
            if frame is None:
                print("Eroare: Cadru nevalid!")
                break
                
            # Mirror Effect (Flip) - Opțional deocamdată, dar util dacă ai o oglindă
            frame_inversat = cv2.flip(frame, 1)

            # YOLO Inference
            results = my_model.detect(frame_inversat)
            
            # (Show on Display) - Deocamdată doar printăm în consolă ce a găsit
            obiecte_pe_ecran = False
            for r in results:
                if len(r.boxes) > 0:
                    for c in r.boxes.cls:
                        nume = r.names[int(c)]
                        print(f"Am detectat: {nume}")
                        obiecte_pe_ecran = True
            
            if not obiecte_pe_ecran:
                print("Nu văd nimic.")
            
            # Evităm să blocăm procesorul la 100%
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print("\nSistemul a fost oprit manual (Check Exit Condition).")
    finally:
        my_camera.stop()
        print("Cameră închisă.")

if __name__ == "__main__":
    run_mirror()