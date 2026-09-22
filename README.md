import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)

MONITORENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HMONITOR,
    wintypes.HDC,
    ctypes.POINTER(wintypes.RECT),
    wintypes.LPARAM
)

def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):

    r = lprcMonitor.contents

    print(
        "ECRAN :",
        "LEFT =", r.left,
        "TOP =", r.top,
        "RIGHT =", r.right,
        "BOTTOM =", r.bottom,
        "|",
        "TAILLE =", r.right - r.left, "x", r.bottom - r.top
    )

    return True


user32.EnumDisplayMonitors(
    None,
    None,
    MONITORENUMPROC(callback),
    0
)
