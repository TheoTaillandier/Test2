import subprocess
import time
import ctypes
from ctypes import wintypes

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# --------------------------------------------------
# 1. OUVRIR LES FENÊTRES
# --------------------------------------------------

pages = [
    "https://www.tradingview.com/chart/",
    "https://www.reuters.com/business/energy/",
    "https://tradingeconomics.com/calendar",
    "https://www.eia.gov/petroleum/supply/weekly/"
]

for page in pages:
    subprocess.Popen([EDGE, "--new-window", page])
    time.sleep(2)

time.sleep(5)

# --------------------------------------------------
# 2. OUTILS WINDOWS
# --------------------------------------------------

user32 = ctypes.windll.user32

SW_RESTORE = 9
SW_MAXIMIZE = 3

def get_title(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)

    if length == 0:
        return ""

    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)

    return buffer.value


def move_window(hwnd, x, y, width, height):
    # Important si Edge est actuellement maximisé
    user32.ShowWindow(hwnd, SW_RESTORE)
    time.sleep(0.3)

    user32.MoveWindow(
        hwnd,
        x,
        y,
        width,
        height,
        True
    )


# --------------------------------------------------
# 3. TROUVER ET POSITIONNER LES FENÊTRES
# --------------------------------------------------

EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    wintypes.HWND,
    wintypes.LPARAM
)

def callback(hwnd, lParam):

    if not user32.IsWindowVisible(hwnd):
        return True

    title = get_title(hwnd)

    if "Microsoft Edge" not in title:
        return True

    title_lower = title.lower()

    print("Trouvé :", title)

    # TRADINGVIEW -> ÉCRAN DROIT COMPLET
    if "tradingview" in title_lower:
        move_window(hwnd, 0, 0, 1920, 1080)
        user32.ShowWindow(hwnd, SW_MAXIMIZE)

    # REUTERS -> HAUT GAUCHE
    elif "reuters" in title_lower or "energy" in title_lower:
        move_window(hwnd, -1920, 0, 960, 540)

    # CALENDRIER -> HAUT DROIT DE L'ÉCRAN GAUCHE
    elif "economic calendar" in title_lower or "trading economics" in title_lower:
        move_window(hwnd, -960, 0, 960, 540)

    # EIA -> BAS GAUCHE
    elif (
        "petroleum" in title_lower
        or "eia" in title_lower
        or "energy information" in title_lower
    ):
        move_window(hwnd, -1920, 540, 960, 540)

    return True


user32.EnumWindows(
    EnumWindowsProc(callback),
    0
)

print("\n✅ Morning Markets lancé")
