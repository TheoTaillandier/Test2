import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

# --------------------------------------------------
# CONFIG WINDOWS API
# --------------------------------------------------

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM
)

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


# --------------------------------------------------
# TROUVER LES FENÊTRES
# --------------------------------------------------

windows = []

def callback(hwnd, lparam):

    if not user32.IsWindowVisible(hwnd):
        return True

    length = user32.GetWindowTextLengthW(hwnd)

    if length > 0:

        title = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title, length + 1)

        windows.append((hwnd, title.value))

    return True


user32.EnumWindows(WNDENUMPROC(callback), 0)


# --------------------------------------------------
# PLACEMENT
# --------------------------------------------------

for hwnd, title in windows:

    title_lower = title.lower()

    # TRADINGVIEW → écran commodity DROIT
    if "tradingview" in title_lower:

        print("TradingView trouvé :", title)

        user32.ShowWindow(hwnd, 9)
        time.sleep(0.5)

        user32.SetWindowPos(
            hwnd,
            None,
            0, 0,
            1920, 1080,
            0
        )

    # REUTERS → écran commodity GAUCHE / haut gauche
    elif "reuters" in title_lower:

        print("Reuters trouvé :", title)

        user32.ShowWindow(hwnd, 9)
        time.sleep(0.5)

        user32.SetWindowPos(
            hwnd,
            None,
            -1920, 0,
            960, 540,
            0
        )

print("Placement terminé.")
