import webbrowser
import time

sites = [
    "https://www.tradingview.com/chart/",
    "https://www.reuters.com/business/energy/",
    "https://tradingeconomics.com/calendar",
    "https://www.eia.gov/petroleum/supply/weekly/"
]

for site in sites:
    webbrowser.open_new(site)
    time.sleep(1)
