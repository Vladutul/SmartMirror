from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

print("Pornesc feed-ul video pe monitor...")
picam2.start()

# Lăsăm imaginea pe ecran 10 secunde
time.sleep(10)

picam2.stop()
print("S-a închis.")