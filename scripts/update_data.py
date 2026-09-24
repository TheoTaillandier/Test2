#!/usr/bin/env python3
"""Build a sourced, dated snapshot from public commodity publications.

Run with: python scripts/update_data.py
Only official, published values are included. A failed feed preserves its last
valid figures and records the error status; no values are estimated.
"""

from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from io import StringIO
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "snapshot.json"
HTML = ROOT / "index.html"
README = ROOT / "README.md"

OIL_URL = "https://ir.eia.gov/wpsr/table4.csv"
OIL_FLOW_URL = "https://ir.eia.gov/wpsr/table1.csv"
OIL_HISTORY_URL = "https://ir.eia.gov/wpsr/psw00.json"
OIL_REPORT_URL = "https://www.eia.gov/petroleum/supply/weekly/"
GAS_URL = "https://ir.eia.gov/ngs/wngsr.json"
GAS_REPORT_URL = "https://ir.eia.gov/ngs/ngs.html"
NEWS_URL = "https://www.eia.gov/rss/todayinenergy.xml"
GIE_URL = "https://agsi.gie.eu/api?country=EU&size=2"
GIE_REPORT_URL = "https://agsi.gie.eu/"


def fetch(url: str, headers: dict[str, str] | None = None) -> bytes:
    req = Request(url, headers={"User-Agent": "CommodityCockpit/1.0 (personal research)", **(headers or {})})
    with urlopen(req, timeout=36) as response:
        data = response.read(5_000_000)
        if not data or len(data) >= 5_000_000:
            raise ValueError("response empty or unexpectedly large")
        return data


def metric(id: str, sector: str, label: str, value: float, unit: str,
           change: float | None, comparison: str, as_of: str,
           source: str, url: str, detail: str = "") -> dict:
    return dict(id=id, sector=sector, label=label, value=round(value, 3),
                unit=unit, change=round(change, 3) if change is not None else None,
                comparison=comparison, as_of=as_of, source=source, url=url,
                detail=detail)


def parse_oil(raw: bytes) -> dict:
    text = raw.decode("utf-8-sig", "replace")
    rows = list(csv.reader(StringIO(text)))
    if len(rows) < 15 or len(rows[0]) < 4:
        raise ValueError("EIA oil CSV missing columns")
    period = datetime.strptime(rows[0][1].strip(), "%m/%d/%y").date().isoformat()
    previous = datetime.strptime(rows[0][2].strip(), "%m/%d/%y").date()
    if previous >= date.fromisoformat(period):
        raise ValueError("EIA oil dates out of order")
    by_name = {r[0].strip(): r for r in rows[1:] if len(r) >= 4}
    definitions = [
        ("oil_crude", "Stocks commerciaux de brut", "Commercial (Excluding SPR)", (100, 800)),
        ("oil_cushing", "Stocks de Cushing", "Cushing", (1, 100)),
        ("oil_gulf", "Stocks de brut Gulf Coast", "Gulf Coast (PADD 3)", (50, 500)),
        ("oil_gasoline", "Stocks d’essence", "Total Motor Gasoline", (80, 400)),
        ("oil_distillate", "Stocks de distillats", "Distillate Fuel Oil", (40, 350)),
        ("oil_jet", "Stocks de jet fuel", "Kerosene-Type Jet Fuel", (10, 100)),
        ("oil_spr", "Réserve stratégique US", "SPR", (100, 900)),
    ]
    result = []
    for id, label, name, (low, high) in definitions:
        row = by_name[name]
        value, prev, difference = (float(row[i].replace(",", "")) for i in (1, 2, 3))
        if not low <= value <= high or abs(value - prev - difference) > 0.02:
            raise ValueError("EIA oil unit or change mismatch: " + name)
        result.append(metric(id, "oil", label, value, "M bbl", difference,
                             "sur 1 semaine", period, "EIA WPSR", OIL_REPORT_URL))
    return {"metrics": result, "as_of": period, "url": OIL_REPORT_URL}


def parse_oil_flows(raw: bytes) -> dict:
    rows = list(csv.reader(StringIO(raw.decode("utf-8-sig", "replace"))))
    header = next((row for row in rows if len(row) > 5 and row[:2] == ["STUB_1", "STUB_2"]), None)
    if not header:
        raise ValueError("EIA oil flow table header missing")
    period = datetime.strptime(header[2].strip(), "%m/%d/%y").date().isoformat()
    definitions = [
        ("oil_production", "Production de brut US", "Crude Oil Supply", "Domestic Production", 5, 20),
        ("oil_imports", "Importations de brut US", "Crude Oil Supply", "Imports", 2, 20),
        ("oil_exports", "Exportations de brut US", "Crude Oil Supply", "Exports", 0.1, 12),
        ("oil_refinery", "Brut traité par les raffineries US", "Crude Oil Supply", "Crude Oil Input to Refineries", 5, 25),
    ]
    result = []
    for id, label, category, row_name, low, high in definitions:
        matches = [row for row in rows if len(row) > 5 and row[0].strip() == category and
                   re.sub(r"^\(\d+\)\s*", "", row[1].strip()) == row_name]
        if len(matches) != 1:
            raise ValueError("EIA oil flow missing or ambiguous: " + row_name)
        current, previous, reported_change = (float(matches[0][n].replace(",", "")) / 1000 for n in (2, 3, 4))
        if not low <= current <= high or abs(current - previous - reported_change) > 0.02:
            raise ValueError("EIA oil flow unit or change mismatch: " + row_name)
        result.append(metric(id, "oil", label, current, "M bbl/j", current - previous,
                             "sur 1 semaine", period, "EIA WPSR", OIL_REPORT_URL,
                             "Débit quotidien moyen de la semaine"))
    return {"metrics": result, "as_of": period, "url": OIL_REPORT_URL}


def parse_oil_history(raw: bytes) -> dict:
    report = json.loads(raw.decode("utf-8-sig"))
    series = report["data"]["U.S."]["time_series"]
    points = [{"date": item["date"], "value": round(float(item["value"]) / 1000, 3)}
              for item in series if item.get("value") is not None and not item.get("suppression_flag")]
    points = sorted(points, key=lambda x: x["date"])[-26:]
    if len(points) < 12 or not 100 <= points[-1]["value"] <= 800:
        raise ValueError("EIA historical crude series invalid")
    return {"points": points, "as_of": points[-1]["date"],
            "published": report["metadata"].get("release_date"), "url": OIL_REPORT_URL}


def parse_gas(raw: bytes) -> dict:
    report = json.loads(raw.decode("utf-8-sig"))
    period = report["current_week"]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", period):
        raise ValueError("EIA gas date invalid")
    names = {
        "total lower 48 states": ("gas_us", "Stockage de gaz US · Lower 48", (500, 5000)),
        "east region": ("gas_east", "Stockage gaz · East US", (100, 1700)),
        "midwest region": ("gas_midwest", "Stockage gaz · Midwest US", (100, 1700)),
        "south central region": ("gas_south", "Stockage gaz · South Central US", (100, 2500)),
    }
    result = []
    for item in report["series"]:
        key = item["name"].strip().lower()
        if key not in names:
            continue
        id, label, (low, high) = names[key]
        current, previous = item["data"][:2]
        value, prev = float(current[1]), float(previous[1])
        if current[0] != period or not low <= value <= high or abs(value - prev) > 500:
            raise ValueError("EIA gas mismatch: " + key)
        five_year = item.get("calculated", {}).get("pct-chg_5yr-avg")
        detail = (f"{float(five_year):+.1f} % vs moyenne 5 ans" if five_year is not None else "")
        result.append(metric(id, "gas", label, value, "Bcf", value - prev,
                             "sur 1 semaine", period, "EIA WNGSR", GAS_REPORT_URL, detail))
    if not any(item["id"] == "gas_us" for item in result):
        raise ValueError("EIA gas Lower 48 series missing")
    return {"metrics": result, "as_of": period, "url": GAS_REPORT_URL}


def rows_between(text: str, start: str, end: str) -> str:
    match = re.search(start + r"([\s\S]*?)" + end, text, re.I | re.M)
    if not match:
        raise ValueError("WASDE section missing: " + start)
    return match.group(1)


def row_four(section: str, label: str) -> tuple[float, float]:
    match = re.search(r"^\s*" + re.escape(label) + r"\s+(-?[\d,.]+)\s+(-?[\d,.]+)\s+(-?[\d,.]+)\s+(-?[\d,.]+)\s*$", section, re.M)
    if not match:
        raise ValueError("WASDE row missing: " + label)
    return tuple(float(x.replace(",", "")) for x in match.groups()[-2:])


def parse_wasde(raw: bytes, url: str) -> dict:
    text = raw.decode("utf-8-sig", "replace").replace("\r\n", "\n")
    month_tag = re.search(r"WASDE\s+-\s+\d+\s+-\s+8\s+(\w+\s+20\d\d)", text)
    if not month_tag:
        raise ValueError("WASDE report month missing")
    month = datetime.strptime(month_tag.group(1), "%B %Y").strftime("%Y-%m")
    corn_page = rows_between(text, r"U\.S\. Feed Grain and Corn Supply and Use", r"U\.S\. Sorghum, Barley, and Oats Supply and Use")
    corn = rows_between(corn_page, r"^CORN\s*$", r"^Avg\.FarmPrice \(\$/bu\)")
    soy_page = rows_between(text, r"U\.S\. Soybeans and Products Supply and Use \(Domestic Measure\)", r"U\.S\. Sugar Supply and Use")
    soy = rows_between(soy_page, r"^SOYBEANS\s*$", r"^SOYBEAN OIL\s*$")
    corn_production_old, corn_production = row_four(corn, "Production")
    corn_stock_old, corn_stock = row_four(corn, "Ending Stocks")
    corn_exports_old, corn_exports = row_four(corn, "Exports")
    soy_production_old, soy_production = row_four(soy, "Production")
    soy_stock_old, soy_stock = row_four(soy, "Ending Stocks")
    soy_exports_old, soy_exports = row_four(soy, "Exports")

    # World wheat: the two projected rows in the first World wheat summary.
    summary = rows_between(text, r"World and U\.S\. Supply and Use for Grains\s+1/", r"^\s+United States\s*$")
    wheat = rows_between(summary, r"^Wheat\s*$", r"^Coarse Grains")
    projection = wheat.split("(Proj.)", 1)[-1]
    wheat_rows = [line for line in projection.splitlines() if re.match(r"^\s*[A-Z][a-z]{2}\s+\d", line)]
    if len(wheat_rows) < 2:
        raise ValueError("WASDE world wheat projections missing")
    wheat_old, wheat_stock = [float(line.split()[-1]) for line in wheat_rows[-2:]]
    wheat_trade_old, wheat_trade = [float(line.split()[-3]) for line in wheat_rows[-2:]]

    # World corn: continuation table, projected year, World row and monthly projections.
    world_corn = rows_between(text, r"World Corn Supply and Use\s+1/\s+\(Contd\.\)", r"WASDE\s+-\s+\d+\s+-\s+24")
    world_projection = rows_between(world_corn, r"20\d\d/\d\d\s+Proj\.\s*World\s+3/", r"World Less China")
    world_rows = [line for line in world_projection.splitlines() if re.match(r"^\s*[A-Z][a-z]{2}\s+\d", line)]
    if len(world_rows) < 2:
        raise ValueError("WASDE world corn projections missing")
    world_old, world_stock = [float(line.split()[-1]) for line in world_rows[-2:]]
    if not (5000 < corn_production < 20000 and 200 < corn_stock < 5000 and
            1000 < corn_exports < 6000 and 2000 < soy_production < 8000 and
            50 < soy_stock < 2000 and 500 < soy_exports < 4000 and
            100 < world_stock < 500 and 100 < wheat_stock < 500 and 50 < wheat_trade < 400):
        raise ValueError("WASDE figure outside expected range")

    specs = [
        ("ag_corn_output", "Production maïs US", corn_production, corn_production_old, "M bu"),
        ("ag_corn_stocks", "Stocks finaux maïs US", corn_stock, corn_stock_old, "M bu"),
        ("ag_corn_exports", "Exportations prévues maïs US", corn_exports, corn_exports_old, "M bu"),
        ("ag_soy_output", "Production soja US", soy_production, soy_production_old, "M bu"),
        ("ag_soy_stocks", "Stocks finaux soja US", soy_stock, soy_stock_old, "M bu"),
        ("ag_soy_exports", "Exportations prévues soja US", soy_exports, soy_exports_old, "M bu"),
        ("ag_world_corn", "Stocks mondiaux de maïs", world_stock, world_old, "Mt"),
        ("ag_world_wheat", "Stocks mondiaux de blé", wheat_stock, wheat_old, "Mt"),
        ("ag_world_wheat_trade", "Commerce mondial de blé prévu", wheat_trade, wheat_trade_old, "Mt"),
    ]
    metrics = [metric(id, "agri", label, value, unit, value - old,
                      "vs rapport précédent", month, "USDA WASDE", url,
                      "Prévision de campagne, révisable")
               for id, label, value, old, unit in specs]
    return {"metrics": metrics, "as_of": month, "url": url}


def fetch_wasde(today: date) -> dict:
    for month_delta in range(3):
        year = today.year
        month = today.month - month_delta
        while month <= 0:
            month += 12
            year -= 1
        url = f"https://www.usda.gov/oce/commodity/wasde/wasde{month:02d}{year % 100:02d}.txt"
        try:
            return parse_wasde(fetch(url), url)
        except HTTPError as error:
            if error.code == 404:
                continue
            raise
    raise ValueError("No WASDE report found for the last three months")


def parse_news(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    stories = []
    for item in root.findall("./channel/item"):
        title = unescape(item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        desc = re.sub(r"<[^>]+>", " ", item.findtext("description") or "")
        desc = " ".join(unescape(desc).split())
        if not (title and url.startswith("https://www.eia.gov/")):
            continue
        try:
            published = parsedate_to_datetime(item.findtext("pubDate") or "").date().isoformat()
        except (ValueError, TypeError):
            continue
        stories.append(dict(title=title, summary=desc[:260], date=published,
                            url=url, source="EIA · Today in Energy"))
    if not stories:
        raise ValueError("EIA RSS has no usable headlines")
    return stories[:8]


def news_result(raw: bytes) -> dict:
    stories = parse_news(raw)
    return {"stories": stories, "as_of": max(item["date"] for item in stories), "url": NEWS_URL}


def parse_gie(raw: bytes) -> dict:
    report = json.loads(raw.decode("utf-8-sig"))
    rows = report.get("data", [])
    if not isinstance(rows, list):
        raise ValueError("GIE returned unexpected data")
    rows = [row for row in rows if isinstance(row, dict) and row.get("gasDayStart") and
            row.get("full") is not None and row.get("status") != "N" and
            (str(row.get("code", "")).upper() in ("EU", "EU27") or
             str(row.get("name", "")).lower() in ("europe", "european union"))]
    rows.sort(key=lambda item: item["gasDayStart"], reverse=True)
    if not rows:
        raise ValueError("GIE EU storage data missing")
    current = rows[0]
    value = float(current["full"])
    if not 0 <= value <= 100:
        raise ValueError("GIE fill percentage out of bounds")
    change = value - float(rows[1]["full"]) if len(rows) > 1 else None
    detail = f"{float(current['gasInStorage']):.1f} TWh stockés" if current.get("gasInStorage") is not None else ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", current["gasDayStart"]):
        raise ValueError("GIE gas day invalid")
    value_metric = metric("gas_eu", "gas", "Stockage gaz UE", value, "%", change,
                          "points vs veille", current["gasDayStart"], "GIE AGSI+",
                          GIE_REPORT_URL, detail)
    return {"metrics": [value_metric], "as_of": current["gasDayStart"], "url": GIE_REPORT_URL}


def get_previous() -> dict:
    if SNAPSHOT.exists():
        return json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    return {"metrics": [], "sources": {}, "stories": [], "history": {}}


def build_snapshot(previous: dict, results: dict, now: datetime) -> dict:
    values = {item["id"]: item for item in previous.get("metrics", [])}
    sources = previous.get("sources", {}).copy()
    history = previous.get("history", {}).copy()
    stories = previous.get("stories", [])
    for key in ("oil", "oil_flows", "oil_history", "gas", "wasde", "news", "gie"):
        result = results.get(key)
        if isinstance(result, Exception):
            old = sources.get(key, {})
            sources[key] = {**old, "status": "error", "checked_at": now.isoformat(),
                            "message": "Dernière donnée conservée ; source indisponible."}
            continue
        if result is None:
            if key == "gie":
                sources[key] = {"status": "needs_key", "url": GIE_REPORT_URL,
                                "message": "Clé personnelle GIE requise."}
            continue
        sources[key] = {"status": "ok", "as_of": result.get("as_of"),
                        "url": result.get("url", NEWS_URL), "checked_at": now.isoformat()}
        if result.get("published"):
            sources[key]["published"] = result["published"]
        for item in result.get("metrics", []):
            values[item["id"]] = item
        if key == "oil_history":
            history["oil_crude"] = result["points"]
        if key == "news":
            stories = result["stories"]

    values["metal_copper"] = metric("metal_copper", "metals", "Production minière cuivre · monde",
                                     23, "Mt", None, "estimation annuelle", "2025",
                                     "USGS MCS 2026",
                                     "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-copper.pdf",
                                     "Repère structurel, pas un stock LME")
    sources["metals"] = {"status": "structural", "as_of": "2025", "url":
                           "https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports"}
    return {"schema": 1, "generated_at": now.isoformat(), "sources": sources,
            "metrics": list(values.values()), "history": history, "stories": stories}


def save_snapshot(snapshot: dict) -> None:
    serialized = json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(serialized, encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    embed = serialized.replace("<", "\\u003c").replace(">", "\\u003e")
    tag = re.compile(r'(<script id="snapshot-data" type="application/json">)(.*?)(</script>)', re.S)
    html, count = tag.subn(lambda match: match.group(1) + "\n" + embed + match.group(3), html)
    if count != 1:
        raise ValueError("snapshot tag missing from index.html")
    HTML.write_text(html, encoding="utf-8")
    readme = ("# Commodity Cockpit\n\n"
              "Tableau de bord personnel des matières premières. Dans l'onglet **Code**, ouvrir [`index.html`](index.html), cliquer sur **Raw** ou **Download raw file**, enregistrer le fichier en `.html`, puis l'ouvrir dans un navigateur. Le code HTML complet figure aussi ci-dessous.\n\n"
              "Les chiffres physiques EIA et USDA sont collectés par [la tâche planifiée](.github/workflows/update-data.yml), puis intégrés à `index.html`. Chaque chiffre indique sa source, sa période et son unité. Les prix TradingView sont des références spot ou CFD indicatives ; certains futures sont bloqués hors de TradingView. Le cuivre USGS est un repère annuel.\n\n"
              "## Sources & automatisation\n\n"
              "- EIA WPSR : stocks de brut, Cushing, Gulf Coast, essence, distillats, jet et SPR ; production, importations, exportations et brut traité par les raffineries US.\n"
              "- EIA WNGSR : stockage de gaz US et régions, variation hebdomadaire et écart à la moyenne cinq ans.\n"
              "- USDA WASDE : production, exportations prévues et stocks de maïs et soja US ; stocks mondiaux de maïs et blé, commerce mondial prévu du blé. Les révisions comparent les deux colonnes de prévision du même rapport.\n"
              "- EIA Today in Energy : titres et résumés d'analyses récentes.\n"
              "- GIE AGSI+ : facultatif, ajouter une clé API personnelle `GIE_API_KEY` aux secrets du dépôt GitHub Actions. L'agrégat UE doit être reconnu dans la réponse avant tout affichage ; sans clé, aucun chiffre européen n'est montré.\n"
              "- LME : [rapports de stocks](https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports) à consulter, sans chiffre de stock automatisé tant qu'un flux stable n'est pas vérifié.\n\n"
              "Unités : M bbl = millions de barils ; M bbl/j = millions de barils par jour ; Bcf = milliards de pieds cubes ; M bu = millions de boisseaux ; Mt = millions de tonnes. Stocks et flux quotidiens ne sont jamais additionnés.\n\n"
              "Les clés restent dans les secrets GitHub et ne sont jamais insérées dans les fichiers publics. Le fichier HTML contient un instantané et s'ouvre directement après téléchargement. Un téléchargement isolé ne reçoit pas les nouvelles données : récupérer la dernière version depuis GitHub. Les tâches GitHub planifiées peuvent être retardées ou désactivées après une longue période sans activité ; dans ce cas, l'onglet Actions permet la relance manuelle.\n\n"
              "## Code complet\n\n```html\n" + html + "\n```\n")
    README.write_text(readme, encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    previous = get_previous()
    tasks = {
        "oil": lambda: parse_oil(fetch(OIL_URL)),
        "oil_flows": lambda: parse_oil_flows(fetch(OIL_FLOW_URL)),
        "oil_history": lambda: parse_oil_history(fetch(OIL_HISTORY_URL)),
        "gas": lambda: parse_gas(fetch(GAS_URL)),
        "wasde": lambda: fetch_wasde(now.date()),
        "news": lambda: news_result(fetch(NEWS_URL)),
    }
    gie_key = os.environ.get("GIE_API_KEY", "")
    if gie_key:
        tasks["gie"] = lambda: parse_gie(fetch(GIE_URL, {"x-key": gie_key}))
    results = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = {pool.submit(task): key for key, task in tasks.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
                print(f"{key}: ok")
            except Exception as error:
                results[key] = error
                print(f"{key}: unavailable ({type(error).__name__})", file=sys.stderr)
    snapshot = build_snapshot(previous, results, now)
    if not any(item.get("status") == "ok" for item in snapshot["sources"].values()):
        raise RuntimeError("No usable source: keeping published snapshot unchanged")
    save_snapshot(snapshot)
    print("Metrics:", len(snapshot["metrics"]), "| official headlines:", len(snapshot["stories"]))


if __name__ == "__main__":
    main()
