import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

# Types exacts des fonctions Windows
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

user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextLengthW.restype = ctypes.c_int

user32.GetWindowTextW.argtypes = [
    wintypes.HWND,
    wintypes.LPWSTR,
    ctypes.c_int
]
user32.GetWindowTextW.restype = ctypes.c_int

edge_windows = []

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM
)

def callback(hwnd, lparam):

    length = user32.GetWindowTextLengthW(hwnd)

    if length > 0:
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)

        if "Microsoft Edge" in buffer.value:
            edge_windows.append(hwnd)
            print("Trouvé :", hwnd, buffer.value)

    return True

user32.EnumWindows(WNDENUMPROC(callback), 0)

if edge_windows:

    hwnd = edge_windows[0]

    print("Déplacement dans 3 secondes...")
    time.sleep(3)

    # Restaurer la fenêtre
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

    error = ctypes.get_last_error()

    print("SetWindowPos =", result)
    print("Windows error =", error)

else:
    print("Aucune fenêtre Edge trouvée")
