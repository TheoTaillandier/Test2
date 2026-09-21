import requests

sites = [
    "https://www.google.com",
    "https://www.tradingview.com",
    "https://tradingeconomics.com",
]

for site in sites:
    try:
        r = requests.get(site, timeout=5)
        print(site, "->", r.status_code)
    except Exception as e:
        print(site, "-> BLOQUÉ")
        print(type(e).__name__)
