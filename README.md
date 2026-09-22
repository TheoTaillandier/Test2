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
# TROUVER TOUTES LES FENÊTRES
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
# PLACER TRADINGVIEW + REUTERS
# --------------------------------------------------

for hwnd, title in windows:

    title_lower = title.lower()

    # ==============================
    # TRADINGVIEW
    # ÉCRAN DROIT COMPLET
    # ==============================

    if "tradingview" in title_lower:

        print("\nTRADINGVIEW TROUVÉ")
        print("HWND :", hwnd)
        print("Titre :", title)

        user32.ShowWindow(hwnd, 9)
        time.sleep(1)

        ctypes.set_last_error(0)

        result = user32.SetWindowPos(
            hwnd,
            None,
            0, 0,
            1920, 1080,
            0
        )

        print("Résultat TradingView :", result)
        print("Erreur Windows :", ctypes.get_last_error())


    # ==============================
    # REUTERS
    # ÉCRAN GAUCHE / HAUT GAUCHE
    # ==============================

    elif "reuters" in title_lower:

        print("\nREUTERS TROUVÉ")
        print("HWND :", hwnd)
        print("Titre :", title)

        user32.ShowWindow(hwnd, 9)
        time.sleep(1)

        ctypes.set_last_error(0)

        result = user32.SetWindowPos(
            hwnd,
            None,
            -1920, 0,
            960, 540,
            0
        )

        print("Résultat Reuters :", result)
        print("Erreur Windows :", ctypes.get_last_error())


print("\n--------------------------")
print("PLACEMENT TERMINÉ")
print("--------------------------")
