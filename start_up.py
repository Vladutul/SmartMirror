from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

# Setăm configurația
config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(config)

print("Deschid fereastra video pe ecran...")

# ASTA E LINIA MAGICĂ CARE LIPSEA:
picam2.start_preview(Preview.QTGL)

# Pornim captura
picam2.start()

# Lăsăm fereastra pe ecran 10 secunde
time.sleep(10)

# Oprim totul curat
picam2.stop_preview()
picam2.stop()
print("S-a închis.")