import ctypes

user32 = ctypes.windll.user32

print("Largeur écran principal :", user32.GetSystemMetrics(0))
print("Hauteur écran principal :", user32.GetSystemMetrics(1))

print("Largeur totale bureau :", user32.GetSystemMetrics(78))
print("Hauteur totale bureau :", user32.GetSystemMetrics(79))

print("Position gauche bureau :", user32.GetSystemMetrics(76))
print("Position haute bureau :", user32.GetSystemMetrics(77))
