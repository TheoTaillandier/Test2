import subprocess
import time
import ctypes
from ctypes import wintypes

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

user32 = ctypes.windll.user32

SW_RESTORE = 9
SW_MAXIMIZE = 3

# --------------------------------------------------
# Récupère toutes les fenêtres visibles
# --------------------------------------------------

def get_windows():

    result = set()

    CALLBACK = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        wintypes.HWND,
        wintypes.LPARAM
    )

    def callback(hwnd, lParam):

        if user32.IsWindowVisible(hwnd):
            result.add(hwnd)

        return True

    user32.EnumWindows(CALLBACK(callback), 0)

    return result


# --------------------------------------------------
# Ouvre une NOUVELLE fenêtre Edge et récupère son HWND
# --------------------------------------------------

def open_edge(url):

    before = get_windows()

    subprocess.Popen([
        EDGE,
        "--new-window",
        url
    ])

    # Attend que la nouvelle fenêtre apparaisse
    for _ in range(30):

        time.sleep(0.5)

        after = get_windows()

        new_windows = after - before

        for hwnd in new_windows:

            length = user32.GetWindowTextLengthW(hwnd)

            if length > 0:

                buffer = ctypes.create_unicode_buffer(length + 1)

                user32.GetWindowTextW(
                    hwnd,
                    buffer,
                    length + 1
                )

                title = buffer.value

                if "Microsoft Edge" in title:
                    print("Trouvé :", title)
                    return hwnd

    print("Fenêtre Edge non trouvée")
    return None


# --------------------------------------------------
# Déplacement
# --------------------------------------------------

def place(hwnd, x, y, width, height, maximize=False):

    if hwnd is None:
        return

    user32.ShowWindow(hwnd, SW_RESTORE)

    time.sleep(0.5)

    user32.SetWindowPos(
        hwnd,
        0,
        x,
        y,
        width,
        height,
        0x0040
    )

    if maximize:
        user32.ShowWindow(hwnd, SW_MAXIMIZE)


# ==================================================
# TRADINGVIEW
# écran DROIT
# ==================================================

tv = open_edge(
    "https://www.tradingview.com/chart/"
)

place(
    tv,
    0, 0,
    1920, 1080,
    maximize=True
)


# ==================================================
# REUTERS
# écran GAUCHE — haut gauche
# ==================================================

reuters = open_edge(
    "https://www.reuters.com/business/energy/"
)

place(
    reuters,
    -1920, 0,
    960, 540
)


# ==================================================
# CALENDAR
# écran GAUCHE — haut droite
# ==================================================

calendar = open_edge(
    "https://tradingeconomics.com/calendar"
)

place(
    calendar,
    -960, 0,
    960, 540
)


# ==================================================
# FUNDAMENTALS / EIA
# écran GAUCHE — bas gauche
# ==================================================

eia = open_edge(
    "https://www.eia.gov/petroleum/supply/weekly/"
)

place(
    eia,
    -1920, 540,
    960, 540
)


print("Morning Markets prêt.")
