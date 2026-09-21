import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL("user32", use_last_error=True)

# --------------------------------------------------
# TYPES WINDOWS
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
# TROUVER LES FENÊTRES EDGE PAR LEUR TITRE
# (sans dépendre de "Microsoft Edge")
# --------------------------------------------------

windows = []

def callback(hwnd, lparam):

    if not user32.IsWindowVisible(hwnd):
        return True

    length = user32.GetWindowTextLengthW(hwnd)

    if length > 0:

        title = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title, length + 1)

        text = title.value

        # On exclut PyCharm et les fenêtres système
        if (
            text
            and "morning_markets" not in text
            and "Explorateur de fichiers" not in text
            and "Excel" not in text
            and "Paramètres" not in text
        ):
            windows.append((hwnd, text))

    return True


user32.EnumWindows(WNDENUMPROC(callback), 0)

print("Fenêtres candidates :")

for i, (hwnd, title) in enumerate(windows):
    print(i, "|", hwnd, "|", title)


# --------------------------------------------------
# TEST
# --------------------------------------------------

if windows:

    hwnd = windows[0][0]

    print("\nTest déplacement :", windows[0][1])
    time.sleep(3)

    user32.ShowWindow(hwnd, 9)

    user32.SetWindowPos(
        hwnd,
        None,
        200,
        150,
        800,
        600,
        0
    )
