import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

# Déclaration correcte de SetWindowPos
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

user32.ShowWindow.argtypes = [
    wintypes.HWND,
    ctypes.c_int
]
user32.ShowWindow.restype = wintypes.BOOL

# Trouver Edge
edge_hwnd = None

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM
)

def callback(hwnd, lparam):
    global edge_hwnd

    length = user32.GetWindowTextLengthW(hwnd)

    if length > 0:
        title = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title, length + 1)

        if "Microsoft Edge" in title.value:
            edge_hwnd = hwnd
            print("Edge trouvé :", hwnd)
            print(title.value)

    return True

user32.EnumWindows(WNDENUMPROC(callback), 0)

if edge_hwnd:

    print("Déplacement dans 3 secondes...")
    time.sleep(3)

    # Restaurer Edge s'il est maximisé
    user32.ShowWindow(edge_hwnd, 9)
    time.sleep(1)

    ctypes.set_last_error(0)

    result = user32.SetWindowPos(
        edge_hwnd,
        None,
        200,
        150,
        800,
        600,
        0x0040
    )

    print("Résultat :", result)
    print("Erreur Windows :", ctypes.get_last_error())

else:
    print("Edge non trouvé")
