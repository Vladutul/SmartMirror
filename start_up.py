from picam2 import Picamera2
import time

# Inițializăm camera
picam2 = Picamera2()

# Configurăm camera pentru previzualizare
picam2.configure(picam2.create_preview_configuration())

print("Pornesc camera pe Trixie...")

# Pornim camera și previzualizarea pe ecran
picam2.start()
picam2.start_preview()

# Lăsăm previzualizarea 10 secunde
time.sleep(10)

# Oprim camera
picam2.stop_preview()
picam2.stop()
print("Camera a fost oprită.")