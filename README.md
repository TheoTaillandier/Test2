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

# PETIT ÉCRAN
# Teams uniquement
# >>> LE SCRIPT N'Y TOUCHE JAMAIS <<<


# GRAND ÉCRAN GAUCHE
# TradingView
TRADINGVIEW_X = 0
TRADINGVIEW_Y = 0
TRADINGVIEW_W = 1920
TRADINGVIEW_H = 1080


# GRAND ÉCRAN DROITE
# Intelligence commodities
INTEL_X = 1920
INTEL_Y = 0
INTEL_W = 1920
INTEL_H = 1080


# Chaque quadrant fait 960 x 540

REUTERS_POSITION = (
    1920,   # x
    0,      # y
    960,    # largeur
    540     # hauteur
)

CALENDAR_POSITION = (
    2880,   # 1920 + 960
    0,
    960,
    540
)

EIA_POSITION = (
    1920,
    540,
    960,
    540
)

# Bas droite :
# x = 2880
# y = 540
# 960 x 540
#
# Réservé au futur dashboard Python


# ============================================================
# WINDOWS API
# ============================================================

user32 = ctypes.WinDLL(
    "user32",
    use_last_error=True
)

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

            title = ctypes.create_unicode_buffer(
                length + 1
            )

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
    user32.ShowWindow(
        hwnd,
        9
    )

    time.sleep(0.3)

    ctypes.set_last_error(0)

    result = user32.SetWindowPos(
        hwnd,
        None,
        x,
        y,
        width,
        height,
        0
    )

    if result:
        print("Déplacement OK")
    else:
        print(
            "Erreur déplacement :",
            ctypes.get_last_error()
        )


# ============================================================
# OUVERTURE DU COCKPIT
# ============================================================

print()
print("========================================")
print("       MORNING COMMODITY COCKPIT")
print("========================================")
print()

print("Ouverture des pages...")
print()


for name, url in URLS.items():

    print("Ouverture :", name)

    subprocess.Popen(
        [
            EDGE,
            "--new-window",
            url
        ]
    )

    # Laisse Edge créer la fenêtre
    time.sleep(2)


# ============================================================
# ATTENTE CHARGEMENT
# ============================================================

print()
print("Chargement des pages...")

time.sleep(6)


# ============================================================
# DÉTECTION DES FENÊTRES
# ============================================================

windows = get_windows()


found = {
    "tradingview": False,
    "reuters": False,
    "calendar": False,
    "eia": False
}


# ============================================================
# PLACEMENT
# ============================================================

for hwnd, title in windows:

    t = title.lower()


    # --------------------------------------------------------
    # TRADINGVIEW
    # GRAND ÉCRAN GAUCHE COMPLET
    # --------------------------------------------------------

    if "tradingview" in t:

        print()
        print("TRADINGVIEW TROUVÉ")
        print(title)

        move_window(
            hwnd,
            TRADINGVIEW_X,
            TRADINGVIEW_Y,
            TRADINGVIEW_W,
            TRADINGVIEW_H
        )

        found["tradingview"] = True


    # --------------------------------------------------------
    # REUTERS
    # GRAND ÉCRAN DROITE
    # HAUT GAUCHE
    # --------------------------------------------------------

    elif "reuters" in t:

        print()
        print("REUTERS TROUVÉ")
        print(title)

        move_window(
            hwnd,
            *REUTERS_POSITION
        )

        found["reuters"] = True


    # --------------------------------------------------------
    # TRADING ECONOMICS
    # GRAND ÉCRAN DROITE
    # HAUT DROITE
    # --------------------------------------------------------

    elif (
        "trading economics" in t
        or "economic calendar" in t
    ):

        print()
        print("CALENDAR TROUVÉ")
        print(title)

        move_window(
            hwnd,
            *CALENDAR_POSITION
        )

        found["calendar"] = True


    # --------------------------------------------------------
    # EIA
    # GRAND ÉCRAN DROITE
    # BAS GAUCHE
    # --------------------------------------------------------

    elif (
        "energy information administration" in t
        or "eia" in t
    ):

        print()
        print("EIA TROUVÉ")
        print(title)

        move_window(
            hwnd,
            *EIA_POSITION
        )

        found["eia"] = True


# ============================================================
# RÉSULTAT
# ============================================================

print()
print()
print("========================================")
print("              RÉSULTAT")
print("========================================")
print()


for name, status in found.items():

    if status:
        print("[OK]", name)

    else:
        print("[NON TROUVÉ]", name)


print()
print("----------------------------------------")
print()
print("GRAND ÉCRAN GAUCHE")
print()
print("+--------------------------------------+")
print("|                                      |")
print("|             TRADINGVIEW              |")
print("|                                      |")
print("+--------------------------------------+")
print()
print("GRAND ÉCRAN DROITE")
print()
print("+------------------+-------------------+")
print("| Reuters          | Calendar          |")
print("|                  |                   |")
print("+------------------+-------------------+")
print("| EIA              | Python Dashboard  |")
print("|                  | futur             |")
print("+------------------+-------------------+")
print()
print("PETIT ÉCRAN : TEAMS")
print("Aucune modification.")
print()
print("========================================")
print("             COCKPIT PRÊT")
print("========================================")
