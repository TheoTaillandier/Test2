import subprocess
import time
import ctypes
from ctypes import wintypes


# ============================================================
# CONFIGURATION
# ============================================================

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

URLS = {
    "tradingview": "https://www.tradingview.com/chart/",
    "reuters": "https://www.reuters.com/business/energy/",
    "calendar": "https://tradingeconomics.com/calendar",
    "eia": "https://www.eia.gov/petroleum/supply/weekly/"
}


# ============================================================
# COORDONNÉES DES ÉCRANS
# ============================================================

# ÉCRAN 1 = Teams
# LEFT = -1920 / TOP = 993 / 1280x720
# >>> LE SCRIPT N'Y TOUCHE PAS <<<

# ÉCRAN 2 = Intelligence commodities
SCREEN_2_X = 0
SCREEN_2_Y = 0
SCREEN_2_W = 1920
SCREEN_2_H = 1080

# ÉCRAN 3 = TradingView
SCREEN_3_X = 1920
SCREEN_3_Y = 0
SCREEN_3_W = 1920
SCREEN_3_H = 1080


# ============================================================
# WINDOWS API
# ============================================================

user32 = ctypes.WinDLL("user32", use_last_error=True)

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


# ============================================================
# RÉCUPÉRER LES FENÊTRES VISIBLES
# ============================================================

def get_windows():

    windows = []

    def callback(hwnd, lparam):

        if not user32.IsWindowVisible(hwnd):
            return True

        length = user32.GetWindowTextLengthW(hwnd)

        if length > 0:

            title = ctypes.create_unicode_buffer(length + 1)

            user32.GetWindowTextW(
                hwnd,
                title,
                length + 1
            )

            windows.append(
                (hwnd, title.value)
            )

        return True

    user32.EnumWindows(
        WNDENUMPROC(callback),
        0
    )

    return windows


# ============================================================
# DÉPLACER UNE FENÊTRE
# ============================================================

def move_window(hwnd, x, y, width, height):

    # Restaure la fenêtre si elle est maximisée
    user32.ShowWindow(hwnd, 9)

    time.sleep(0.3)

    result = user32.SetWindowPos(
        hwnd,
        None,
        x,
        y,
        width,
        height,
        0
    )

    return result


# ============================================================
# OUVERTURE DES 4 FENÊTRES EDGE
# ============================================================

print("\n====================================")
print("   MORNING COMMODITY COCKPIT")
print("====================================\n")

print("Ouverture des marchés...")

for name, url in URLS.items():

    print("Ouverture :", name)

    subprocess.Popen(
        [
            EDGE,
            "--new-window",
            url
        ]
    )

    # Important pour laisser Edge créer une vraie fenêtre
    time.sleep(2)


print("\nAttente du chargement des pages...")

time.sleep(6)


# ============================================================
# DÉTECTION + PLACEMENT
# ============================================================

windows = get_windows()

found = {
    "tradingview": False,
    "reuters": False,
    "calendar": False,
    "eia": False
}


for hwnd, title in windows:

    t = title.lower()


    # --------------------------------------------------------
    # TRADINGVIEW
    # ÉCRAN 3 COMPLET
    # --------------------------------------------------------

    if "tradingview" in t:

        print("\nTradingView trouvé")
        print(title)

        move_window(
            hwnd,
            SCREEN_3_X,
            SCREEN_3_Y,
            SCREEN_3_W,
            SCREEN_3_H
        )

        found["tradingview"] = True


    # --------------------------------------------------------
    # REUTERS
    # ÉCRAN 2 - HAUT GAUCHE
    # --------------------------------------------------------

    elif "reuters" in t:

        print("\nReuters trouvé")
        print(title)

        move_window(
            hwnd,
            0,
            0,
            960,
            540
        )

        found["reuters"] = True


    # --------------------------------------------------------
    # TRADING ECONOMICS
    # ÉCRAN 2 - HAUT DROITE
    # --------------------------------------------------------

    elif (
        "trading economics" in t
        or "economic calendar" in t
    ):

        print("\nTrading Economics trouvé")
        print(title)

        move_window(
            hwnd,
            960,
            0,
            960,
            540
        )

        found["calendar"] = True


    # --------------------------------------------------------
    # EIA
    # ÉCRAN 2 - BAS GAUCHE
    # --------------------------------------------------------

    elif (
        "energy information administration" in t
        or "eia" in t
    ):

        print("\nEIA trouvé")
        print(title)

        move_window(
            hwnd,
            0,
            540,
            960,
            540
        )

        found["eia"] = True


# ============================================================
# RÉSULTAT
# ============================================================

print("\n\n====================================")
print("        RÉSULTAT DU COCKPIT")
print("====================================")

for name, status in found.items():

    if status:
        print(f"[OK] {name}")
    else:
        print(f"[NON TROUVÉ] {name}")


print("\nDisposition :")
print("")
print("ÉCRAN 2")
print("+----------------+----------------+")
print("| Reuters        | Calendar       |")
print("+----------------+----------------+")
print("| EIA            | Python futur   |")
print("+----------------+----------------+")
print("")
print("ÉCRAN 3")
print("+---------------------------------+")
print("|          TRADINGVIEW            |")
print("+---------------------------------+")
print("")
print("ÉCRAN 1 : Teams - non modifié")
print("")
print("====================================")
print("       COCKPIT PRÊT")
print("====================================")
