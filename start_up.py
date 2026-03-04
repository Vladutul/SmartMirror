import cv2
import time
from camera_manager import CameraManager
from model_manager import YoloWorker

class SmartMirrorApp:
    def __init__(self):
        self.camera = CameraManager()
        self.yolo = YoloWorker()
        self.is_running = False

    def run(self):
        print("--- START: Pregătire Unelte ---")
        
        # Pornim componentele
        self.yolo.start()
        self.camera.start()
        self.is_running = True

        time.sleep(3) # Dăm timp modelului să se încarce
        print("--- RUNTIME: Sistemul rulează (Apasă ESC pe fereastră pentru a ieși) ---")

        try:
            while self.is_running:
                # 1. Luăm cadrul gata procesat de la cameră
                cadru = self.camera.get_frame_bgr_flipped()

                # 2. Îl trimitem la YOLO (YoloWorker își face o copie intern dacă e liber)
                self.yolo.push_frame(cadru.copy())

                # 3. Cerem detecțiile curente și desenăm
                detectii = self.yolo.get_detections()
                for obiect in detectii:
                    x1, y1, x2, y2 = obiect["coord"]
                    nume = obiect["nume"]
                    cv2.rectangle(cadru, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(cadru, nume, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # 4. Afișăm pe ecran
                cv2.imshow("Smart Mirror", cadru)

                # 5. Verificăm ieșirea
                if cv2.waitKey(1) & 0xFF == 27:
                    print("Se închide...")
                    self.is_running = False
                    break
                    
        finally:
            self.cleanup()

    def cleanup(self):
        print("Încep oprirea componentelor...")
        self.camera.stop()
        self.yolo.stop()
        cv2.destroyAllWindows()
        print("Sistem oprit cu succes.")

if __name__ == "__main__":
    app = SmartMirrorApp()
    app.run()