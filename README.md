import subprocess
import time
import ctypes
from ctypes import wintypes

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# --------------------------------------------------
# 1. OUVERTURE DES 4 FENÊTRES
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

# Laisse Edge finir de charger
time.sleep(5)


# --------------------------------------------------
# 2. RÉCUPÉRATION DES FENÊTRES EDGE
# --------------------------------------------------

user32 = ctypes.windll.user32

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    wintypes.HWND,
    wintypes.LPARAM
)

GetWindowTextLength = user32.GetWindowTextLengthW
GetWindowText = user32.GetWindowTextW
IsWindowVisible = user32.IsWindowVisible

windows = []

def callback(hwnd, lParam):

    if IsWindowVisible(hwnd):

        length = GetWindowTextLength(hwnd)

        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buffer, length + 1)

            title = buffer.value

            if "Microsoft Edge" in title:
                windows.append((hwnd, title))

    return True

EnumWindows(EnumWindowsProc(callback), 0)

print("\nFenêtres Edge trouvées :")

for hwnd, title in windows:
    print(hwnd, title)
