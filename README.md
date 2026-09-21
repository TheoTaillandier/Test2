import subprocess
import time

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

pages = [
    "https://www.tradingview.com/chart/",
    "https://www.reuters.com/business/energy/",
    "https://tradingeconomics.com/calendar",
    "https://www.eia.gov/petroleum/supply/weekly/"
]

for page in pages:
    subprocess.Popen([EDGE, "--new-window", page])
    time.sleep(1)
