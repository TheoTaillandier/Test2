import requests

url = "https://www.eia.gov"

try:

    response = requests.get(url, timeout=10)

    print("Connexion EIA :", response.status_code)

    if response.ok:

        print("✅ Python peut accéder aux données externes")

    else:

        print("⚠️ EIA accessible mais réponse :", response.status_code)

except Exception as e:

    print("❌ Connexion impossible")

    print(e)
