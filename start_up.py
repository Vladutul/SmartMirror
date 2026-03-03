from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(config)

print("Trimit fluxul video direct pe hardware-ul ecranului (DRM)...")

# Aici e magia: folosim DRM în loc de QTGL
picam2.start_preview(Preview.DRM)

picam2.start()

# Lăsăm pe ecran 10 secunde
time.sleep(10)

picam2.stop_preview()
picam2.stop()
print("S-a închis.")