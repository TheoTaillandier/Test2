import ctypes

from ctypes import wintypes

user32 = ctypes.windll.user32

MONITORENUMPROC = ctypes.WINFUNCTYPE(

    ctypes.c_int,

    wintypes.HMONITOR,

    wintypes.HDC,

    ctypes.POINTER(wintypes.RECT),

    wintypes.LPARAM

)

def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):

    r = lprcMonitor.contents

    print(

        f"Écran : "

        f"left={r.left}, top={r.top}, "

        f"right={r.right}, bottom={r.bottom}, "

        f"largeur={r.right-r.left}, "

        f"hauteur={r.bottom-r.top}"

    )

    return 1

callback_func = MONITORENUMPROC(callback)

user32.EnumDisplayMonitors(

    0,

    None,

    callback_func,

    0

)
