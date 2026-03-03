import threading
import queue
import time
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# ==========================================
# 1. Variabile Globale (Pentru comunicare între thread-uri)
# ==========================================
# O coadă cu mărimea 1. Păstrăm doar CEL MAI RECENT cadru pentru YOLO.
cadru_pentru_yolo = queue.Queue(maxsize=1) 
# Aici Thread-ul YOLO va salva ce a găsit, ca Thread-ul principal să poată desena
detectii_curente = [] 
sistem_pornit = True

# ==========================================
# 2. Thread-ul Secundar (Analiza YOLO)
# ==========================================
def worker_yolo():
    global detectii_curente, sistem_pornit
    print("[YOLO] Încarc modelul pe nucleele hardware...")
    model = YOLO("yolov8n.pt")
    print("[YOLO] Pregătit pentru analiză!")

    while sistem_pornit:
        try:
            # Așteptăm până primim un cadru din coadă (timeout de 1 sec)
            cadru = cadru_pentru_yolo.get(timeout=1)
            
            # YOLO folosește automat toate nucleele aici
            rezultate = model(cadru, verbose=False) 
            
            noile_detectii = []
            for r in rezultate:
                for box in r.boxes:
                    # Salvăm coordonatele cutiei [x1, y1, x2, y2] și clasa
                    noile_detectii.append({
                        "nume": r.names[int(box.cls[0])],
                        "coord": box.xyxy[0].cpu().numpy().astype(int)
                    })
            
            # Actualizăm variabila globală cu noile date
            detectii_curente = noile_detectii
            
        except queue.Empty:
            continue # Dacă nu am primit un cadru nou, reluăm bucla

# ==========================================
# 3. Thread-ul Principal (Camera & Afișare)
# ==========================================
def main_loop():
    global sistem_pornit
    print("--- START: Pregătire Unelte ---")
    
    # Pornim thread-ul YOLO în fundal
    thread_analiza = threading.Thread(target=worker_yolo)
    thread_analiza.start()

    # Inițializăm Camera
    picam2 = Picamera2()
    # Folosim o rezoluție mai mică pt procesare rapidă (640x480)
    config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    # Așteptăm să se încarce modelul YOLO
    time.sleep(3) 
    print("--- RUNTIME: Sistemul rulează (Apasă ESC pe fereastră pentru a ieși) ---")

    try:
        while True:
            # 1. Achiziție date (Capture Frame)
            cadru = picam2.capture_array("main")
            
            # Transformăm din RGB (Picamera) în BGR (cum îi place lui OpenCV)
            cadru_bgr = cv2.cvtColor(cadru, cv2.COLOR_RGB2BGR)
            
            # (Opțional) Mirror Effect - Răsturnăm imaginea pe orizontală pt efect de oglindă
            cadru_bgr = cv2.flip(cadru_bgr, 1)

            # 2. Trimitem cadrul către YOLO (doar dacă e liber să primească altul)
            if cadru_pentru_yolo.empty():
                # Trimitem o copie a cadrului pentru a nu bloca desenul
                cadru_pentru_yolo.put(cadru_bgr.copy())

            # 3. Desenăm datele pe ecran (Draw Annotations)
            for obiect in detectii_curente:
                x1, y1, x2, y2 = obiect["coord"]
                nume = obiect["nume"]
                # Desenăm un dreptunghi verde și punem text
                cv2.rectangle(cadru_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(cadru_bgr, nume, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 4. Afișăm pe ecran (Show on Display)
            cv2.imshow("Smart Mirror", cadru_bgr)

            # 5. Check Exit Condition (Așteptăm tasta ESC)
            if cv2.waitKey(1) & 0xFF == 27:
                print("Se închide...")
                break

    finally:
        # Curățenie generală
        sistem_pornit = False
        picam2.stop()
        thread_analiza.join() # Așteptăm ca YOLO să se oprească
        cv2.destroyAllWindows()
        print("Sistem oprit cu succes.")

if __name__ == "__main__":
    main_loop()