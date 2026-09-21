import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

user32.SetWindowPos.argtypes = [
    wintypes.HWND,
    wintypes.HWND,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.UINT
]
user32.SetWindowPos.restype = wintypes.BOOL

# Handle Edge vu dans ton test précédent
hwnd = 133032

print("Déplacement dans 3 secondes...")
time.sleep(3)

# Restaure la fenêtre
user32.ShowWindow(hwnd, 9)
time.sleep(1)

ctypes.set_last_error(0)

result = user32.SetWindowPos(
    hwnd,
    None,
    200,
    150,
    800,
    600,
    0
)

print("Résultat :", result)
print("Erreur Windows :", ctypes.get_last_error())
