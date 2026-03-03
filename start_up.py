import time
from model_manager import ModelYOLO
from camera_manager import CameraManager

class SmartMirrorApp:
    def __init__(self):
        print("--- Pornire Sistem Smart Mirror ---")
        # Inițializăm uneltele independent
        self.yolo = ModelYOLO()
        self.camera = CameraManager()

    def ruleaza(self):
        self.camera.start()
        
        print("--- Începe bucla de analiză ---")
        try:
            # Main loop-ul va rula la nesfârșit (ideal pentru un serviciu)
            while True:
                cadru = self.camera.ia_cadru()
                
                if cadru is not None:
                    # Pasăm imaginea la Model
                    detecții = self.yolo.analizeaza_cadru(cadru)
                    
                    if detecții:
                        print(f"Am găsit pe cadru: {', '.join(detecții)}")
                    else:
                        print("Nu văd nimic pe acest cadru.")
                
                # Pentru un SmartMirror care rulează 24/7, nu vrem să topim procesorul
                # O mică pauză de ex: 0.1 secunde (10 cadre pe secundă e destul)
                time.sleep(0.1) 
                
        except KeyboardInterrupt:
            print("\nSemnal de închidere primit.")
        finally:
            self.curatare()

    def curatare(self):
        self.camera.opreste()
        print("Sistem închis în siguranță.")

if __name__ == "__main__":
    app = SmartMirrorApp()
    app.ruleaza()