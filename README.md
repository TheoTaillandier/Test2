import ctypes
from ctypes import wintypes
import time

# Important : rendre Python DPI-aware
ctypes.windll.shcore.SetProcessDpiAwareness(2)

user32 = ctypes.windll.user32

CALLBACK = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    wintypes.HWND,
    wintypes.LPARAM
)

edge_windows = []

def callback(hwnd, lParam):
    if user32.IsWindowVisible(hwnd):

        length = user32.GetWindowTextLengthW(hwnd)

        if length > 0:
            title = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, title, length + 1)

            if "Microsoft Edge" in title.value:
                edge_windows.append(hwnd)
                print("EDGE :", hwnd, title.value)

    return True

user32.EnumWindows(CALLBACK(callback), 0)

if edge_windows:

    hwnd = edge_windows[0]

    print("Je déplace la fenêtre dans 3 secondes...")
    time.sleep(3)

    # Enlève maximisation éventuelle
    user32.ShowWindow(hwnd, 9)

    time.sleep(1)

    # TEST :
    # écran DROIT, petite fenêtre très visible
    result = user32.SetWindowPos(
        hwnd,
        0,
        200,     # x
        150,     # y
        800,     # largeur
        600,     # hauteur
        0x0040
    )

    print("Résultat SetWindowPos :", result)

else:
    print("Aucune fenêtre Edge trouvée")
