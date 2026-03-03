from picamera import PiCamera
from time import sleep

# Inițializăm camera
camera = PiCamera()

# Opțional: Dacă imaginea este cu susul în jos, poți roti camera
# camera.rotation = 180

print("Pornesc camera...")

# Pornim previzualizarea pe ecran
camera.start_preview()

# Lăsăm previzualizarea activă timp de 10 secunde
# În acest timp vei vedea live pe monitor ce vede camera
sleep(10)

# Oprim previzualizarea
camera.stop_preview()
print("Camera a fost oprită.")