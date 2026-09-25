#!/usr/bin/env python3
"""Build a sourced, dated snapshot from public commodity publications.

Run with: python scripts/update_data.py
Only official, published values are included. A failed feed preserves its last
valid figures and records the error status; no values are estimated.
"""

from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, time, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from io import StringIO
import json
import math
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

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
SODIR_URL = "https://www.sodir.no/en/whats-new/news/production-figures/"
EIA_OIL_SPOT_URL = "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm"
EIA_GAS_SPOT_URL = "https://www.eia.gov/dnav/ng/NG_PRI_FUT_S1_D.htm"
GIE_URL = "https://agsi.gie.eu/api?type=eu&size=14"
GIE_REPORT_URL = "https://agsi.gie.eu/"
GIE_FR_URL = "https://agsi.gie.eu/api?country=fr&size=14"
ALSI_URL = "https://alsi.gie.eu/api?type=eu&size=14"
ALSI_FR_URL = "https://alsi.gie.eu/api?country=fr&size=14"
ALSI_REPORT_URL = "https://alsi.gie.eu/"
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
RTE_REPORT_URL = "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/"
RTE_URL = ("https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
           "eco2mix-national-tr/records?limit=100&where=date_heure%20%3C%3D%20now%28%29"
           "&order_by=date_heure%20desc")
ENTSOE_URL = "https://web-api.tp.entsoe.eu/api"
ENTSOE_REPORT_URL = "https://transparency.entsoe.eu/"
POWER_ZONES = {"fr": "10YFR-RTE------C", "de": "10Y1001A1001A82H"}


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


def measured(value: object) -> float | None:
    """Keep missing/invalid telemetry out of published values."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        result = float(value)
    except (ValueError, TypeError):
        return None
    return result if math.isfinite(result) else None


def parse_rte_power(raw: bytes, now: datetime) -> dict:
    document = json.loads(raw)
    rows = document.get("results") if isinstance(document, dict) else None
    if not isinstance(rows, list):
        raise ValueError("RTE records missing")
    points = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("date_heure"), str):
            continue
        try:
            stamp = datetime.fromisoformat(row["date_heure"].replace("Z", "+00:00"))
        except ValueError:
            continue
        if stamp.tzinfo is None or not now - timedelta(hours=48) <= stamp <= now:
            continue
        demand = measured(row.get("consommation"))
        if demand is None or not 5000 <= demand <= 120000:
            continue
        point = {"at": stamp.astimezone(timezone.utc).isoformat(), "load": round(demand)}
        for field in ("prevision_j", "prevision_j1", "nucleaire", "eolien", "solaire",
                      "hydraulique", "gaz", "bioenergies", "charbon", "fioul",
                      "ech_physiques", "pompage", "taux_co2"):
            value = measured(row.get(field))
            if value is not None and -35000 <= value <= 120000:
                point[field] = round(value)
        points.append(point)
    points.sort(key=lambda row: row["at"])
    if not points or datetime.fromisoformat(points[-1]["at"]) < now - timedelta(hours=30):
        sample = [row.get("date_heure") for row in (rows[:1] + rows[-1:]) if isinstance(row, dict)]
        raise ValueError("RTE observations unavailable or too old; sample times " + repr(sample))
    latest = points[-1]
    as_of = latest["at"][:10]
    time_label = "Observation " + latest["at"] + " UTC"
    values = [metric("power_load", "power", "Demande France", latest["load"], "MW",
                     latest["load"] - points[-5]["load"] if len(points) >= 5 else None,
                     "vs ~1 h", as_of, "RTE éCO2mix", RTE_REPORT_URL, time_label)]
    if "prevision_j" in latest and 5000 <= latest["prevision_j"] <= 120000:
        values.append(metric("power_load_gap", "power", "Écart à prévision de demande J",
                             latest["load"] - latest["prevision_j"], "MW", None,
                             "réalisé − prévision réactualisée le jour même", as_of,
                             "Calcul sur RTE éCO2mix", RTE_REPORT_URL, time_label))
    if "ech_physiques" in latest:
        values.append(metric("power_exchange", "power", "Solde des échanges physiques",
                             latest["ech_physiques"], "MW", None,
                             "export si négatif · import si positif", as_of,
                             "RTE éCO2mix", RTE_REPORT_URL, time_label))
    for field, label in (("nucleaire", "Nucléaire"), ("gaz", "Gaz électrique"),
                         ("eolien", "Éolien"), ("solaire", "Solaire"),
                         ("hydraulique", "Hydraulique"), ("bioenergies", "Bioénergies")):
        if field in latest and latest[field] >= 0:
            values.append(metric("power_" + field, "power", label, latest[field], "MW",
                                 None, "production observée", as_of, "RTE éCO2mix",
                                 RTE_REPORT_URL, time_label))
    if "eolien" in latest and "solaire" in latest:
        values.append(metric("power_residual", "power", "Demande résiduelle indicative",
                             latest["load"] - latest["eolien"] - latest["solaire"], "MW",
                             None, "demande − éolien − solaire", as_of,
                             "Calcul sur RTE éCO2mix", RTE_REPORT_URL,
                             "Calcul indicatif, sans jugement sur le prix ni l'appel au gaz. " + time_label))
    if "taux_co2" in latest:
        values.append(metric("power_carbon", "power", "Intensité CO₂ estimée",
                             latest["taux_co2"], "g/kWh", None,
                             "production française", as_of,
                             "RTE éCO2mix", RTE_REPORT_URL, time_label))
    # A compact, independently dated curve: keep a single day of observations.
    return {"metrics": values, "points": points[-96:], "as_of": latest["at"],
            "url": RTE_REPORT_URL}


def entsoe_query(zone: str, now: datetime, token: str) -> bytes:
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    params = {"documentType": "A65", "processType": "A01", "businessType": "A04",
              "outBiddingZone_Domain": POWER_ZONES[zone],
              "periodStart": (midnight - timedelta(days=1)).strftime("%Y%m%d%H%M"),
              "periodEnd": (midnight + timedelta(days=3)).strftime("%Y%m%d%H%M"),
              "securityToken": token}
    # Never print the request URL or its HTTPError: it contains a personal token.
    return fetch(ENTSOE_URL + "?" + urlencode(params))


def parse_entsoe_forecast(raw: bytes, zone: str, now: datetime) -> dict:
    root = ET.fromstring(raw)
    if root.tag.split("}")[-1] != "GL_MarketDocument":
        raise ValueError("ENTSO-E forecast document unavailable")
    if root.findtext("{*}type") != "A65" or root.findtext("{*}process.processType") != "A01":
        raise ValueError("ENTSO-E returned a different data item")
    points = {}
    for series in root.findall("{*}TimeSeries"):
        if series.findtext("{*}businessType") not in (None, "A04"):
            continue
        unit = series.findtext("{*}quantity_Measure_Unit.name")
        if unit not in ("MAW", "MW"):
            continue
        for block in series.findall("{*}Period"):
            stamp_text = block.findtext("{*}timeInterval/{*}start")
            interval = {"PT15M": 15, "PT30M": 30, "PT60M": 60}.get(block.findtext("{*}resolution"))
            if not stamp_text or not interval:
                continue
            start = datetime.fromisoformat(stamp_text.replace("Z", "+00:00"))
            for item in block.findall("{*}Point"):
                position = measured(item.findtext("{*}position"))
                quantity = measured(item.findtext("{*}quantity"))
                if position is None or position < 1 or position != int(position) or quantity is None or not 5000 <= quantity <= 150000:
                    continue
                stamp = start + timedelta(minutes=(int(position) - 1) * interval)
                if now - timedelta(hours=2) <= stamp <= now + timedelta(days=2):
                    points[stamp.astimezone(timezone.utc).isoformat()] = round(quantity)
    upcoming = sorted((stamp, amount) for stamp, amount in points.items()
                      if now <= datetime.fromisoformat(stamp) < now + timedelta(hours=24))
    if len(upcoming) < 4:
        raise ValueError("ENTSO-E future forecast missing")
    peak_at, peak = max(upcoming, key=lambda point: point[1])
    label = "France" if zone == "fr" else "Allemagne/Luxembourg"
    m = metric("power_forecast_" + zone, "power", "Pic prévu 24 h · " + label,
               peak, "MW", None, "prévision J-1, 24 h glissantes", peak_at[:10],
               "ENTSO-E · prévision J-1", ENTSOE_REPORT_URL, "Pic prévu à " + peak_at + " UTC")
    return {"metrics": [m], "as_of": peak_at, "url": ENTSOE_REPORT_URL}


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


def parse_fred(raw: bytes, series_id: str, today: date) -> dict:
    specs = {
        "DCOILBRENTEU": ("price_brent", "oil", "Brent Europe · spot EIA",
                         "$/bbl", 1, 350, "https://fred.stlouisfed.org/series/DCOILBRENTEU"),
        "DCOILWTICO": ("price_wti", "oil", "WTI Cushing · spot EIA",
                       "$/bbl", 1, 350, "https://fred.stlouisfed.org/series/DCOILWTICO"),
        "DHHNGSP": ("price_henry", "gas", "Henry Hub · spot EIA",
                   "$/MMBtu", 0.01, 50, "https://fred.stlouisfed.org/series/DHHNGSP"),
    }
    id, sector, label, unit, low, high, url = specs[series_id]
    reader = csv.DictReader(StringIO(raw.decode("utf-8-sig", "replace")))
    if not reader.fieldnames or series_id not in reader.fieldnames:
        raise ValueError("FRED series column missing: " + series_id)
    points = []
    for row in reader:
        value = (row.get(series_id) or "").strip()
        if value in ("", "."):
            continue
        observed = date.fromisoformat((row.get("DATE") or row.get("observation_date") or "").strip())
        price = float(value)
        if not low <= price <= high or observed > today:
            raise ValueError("FRED price or date out of bounds: " + series_id)
        points.append((observed, price))
    points.sort()
    if not points or today - points[-1][0] > timedelta(days=30):
        raise ValueError("FRED price data missing or more than 30 days old: " + series_id)
    observed, price = points[-1]
    previous = points[-2][1] if len(points) > 1 else None
    return {"metrics": [metric(id, sector, label, price, unit,
                               price - previous if previous is not None else None,
                               "vs séance précédente" if previous is not None else "prix observé",
                               observed.isoformat(), "EIA · via FRED", url,
                               "Prix spot quotidien ; publication différée, pas un future")],
            "as_of": observed.isoformat(), "url": url}


def parse_eia_spot(raw: bytes, commodity: str, today: date) -> dict:
    """Extract six dated closes from EIA's daily spot tables, with full row validation."""
    specs = {
        "brent": ("price_brent", "oil", "Brent Europe · spot EIA",
                  "$/bbl", "Brent - Europe", "Conventional Gasoline", 1, 350, EIA_OIL_SPOT_URL),
        "wti": ("price_wti", "oil", "WTI Cushing · spot EIA",
                "$/bbl", "WTI - Cushing, Oklahoma", "Brent - Europe", 1, 350, EIA_OIL_SPOT_URL),
        "henry": ("price_henry", "gas", "Henry Hub · spot EIA",
                  "$/MMBtu", "Henry Hub", "Futures Prices", 0.01, 50, EIA_GAS_SPOT_URL),
    }
    id, sector, label, unit, start, end, low, high, url = specs[commodity]
    html = raw.decode("utf-8-sig", "replace")
    html = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    plain = " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())
    first = plain.find(start)
    if first < 0:
        raise ValueError("EIA spot row missing: " + commodity)
    second = plain.find(end, first + len(start))
    if second < 0:
        raise ValueError("EIA spot following row missing: " + commodity)
    header = plain[max(0, first - 1400):first]
    dates = re.findall(r"\b\d{1,2}/\d{1,2}/\d{2}\b", header)[-6:]
    values = [float(v) for v in re.findall(r"(?<!\d)\d+(?:\.\d+)?(?!\d)", plain[first + len(start):second])
              if low <= float(v) <= high]
    if len(dates) != 6 or len(values) != len(dates):
        raise ValueError("EIA spot dates or columns mismatch: " + commodity)
    observations = [(datetime.strptime(d, "%m/%d/%y").date(), v)
                    for d, v in zip(dates, values)]
    if any(d > today for d, _ in observations) or today - observations[-1][0] > timedelta(days=30):
        raise ValueError("EIA spot observation stale or in future: " + commodity)
    observed, price = observations[-1]
    return {"metrics": [metric(id, sector, label, price, unit, price - observations[-2][1],
                               "vs séance précédente", observed.isoformat(), "EIA · prix spot", url,
                               "Clôture quotidienne publiée avec retard ; pas un future")],
            "as_of": observed.isoformat(), "url": url}


def parse_norway(raw: bytes, today: date) -> dict:
    html = raw.decode("utf-8", "replace")
    plain = " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())
    pattern = (r"Production figures\s+([A-Za-z]+)\s+(20\d\d).{0,500}?"
               r"Preliminary production figures for\s+\1\s+\2\s+show an average daily production of"
               r"\s+([\d,\s]+?)\s+barrels of oil, NGL and condensate")
    found = []
    for match in re.finditer(pattern, plain, re.I):
        observed = datetime.strptime(match.group(1).title() + " " + match.group(2), "%B %Y").date()
        value = float(match.group(3).replace(" ", "").replace(",", "")) / 1_000_000
        if observed <= today and 0.5 <= value <= 5:
            found.append((observed, value))
    found = sorted(set(found), reverse=True)
    if not found or today - found[0][0] > timedelta(days=110):
        raise ValueError("Sodir production report missing or too old")
    observed, value = found[0]
    previous = found[1][1] if len(found) > 1 else None
    return {"metrics": [metric("oil_norway_liquids", "oil",
                               "Production Norvège · pétrole et liquides", value, "M bbl/j",
                               value - previous if previous is not None else None,
                               "vs mois précédent" if previous is not None else "provisoire",
                               observed.strftime("%Y-%m"), "Sodir · provisoire",
                               SODIR_URL, "Pétrole + LGN + condensats ; pas uniquement le Brent")],
            "as_of": observed.strftime("%Y-%m"), "url": SODIR_URL}


def gie_rows(raw: bytes, region: str) -> list[dict]:
    report = json.loads(raw.decode("utf-8-sig"))
    rows = report.get("data", [])
    if not isinstance(rows, list):
        raise ValueError("GIE returned unexpected data")
    valid_codes = ("EU", "EU27") if region == "eu" else ("FR",)
    rows = [row for row in rows if isinstance(row, dict) and
            str(row.get("code", "")).upper() in valid_codes and
            row.get("status", "C") in ("C", "E") and row.get("gasDayStart")]
    rows.sort(key=lambda item: item["gasDayStart"], reverse=True)
    if not rows:
        raise ValueError("GIE " + region.upper() + " aggregate missing")
    for row in rows[:2]:
        date.fromisoformat(row["gasDayStart"])
    return rows


def parse_gie(raw: bytes, region: str = "eu") -> dict:
    rows = gie_rows(raw, region)
    current = rows[0]
    suffix, location = ("eu", "UE") if region == "eu" else ("fr", "France")
    percent, stock = float(current["full"]), float(current["gasInStorage"])
    if not 0 <= percent <= 100 or not 0 <= stock <= 1600:
        raise ValueError("GIE storage unit or percent invalid")
    previous = rows[1] if len(rows) > 1 and rows[1]["gasDayStart"] != current["gasDayStart"] else None
    percent_change = percent - float(previous["full"]) if previous and previous.get("full") is not None else None
    stock_change = stock - float(previous["gasInStorage"]) if previous and previous.get("gasInStorage") is not None else None
    flag = "Estimé par les opérateurs" if current.get("status") == "E" else "Déclaré par les opérateurs"
    result = [
        metric("gas_" + suffix, "gas", "Stockage gaz " + location + " · remplissage",
               percent, "%", percent_change, "points vs veille", current["gasDayStart"],
               "GIE AGSI+", GIE_REPORT_URL, flag),
        metric("gas_" + suffix + "_twh", "gas", "Gaz stocké " + location,
               stock, "TWh", stock_change, "vs veille", current["gasDayStart"],
               "GIE AGSI+", GIE_REPORT_URL, flag),
    ]
    if current.get("netWithdrawal") is not None:
        flow = float(current["netWithdrawal"])
        if not -15000 <= flow <= 15000:
            raise ValueError("GIE net withdrawal unit invalid")
        result.append(metric("gas_" + suffix + "_net", "gas", "Soutirage net " + location,
                             flow, "GWh/j", None, "positif = soutirage ; négatif = injection",
                             current["gasDayStart"], "GIE AGSI+", GIE_REPORT_URL, flag))
    points = [{"date": row["gasDayStart"], "value": float(row["full"])}
              for row in reversed(rows) if row.get("full") is not None and
              0 <= float(row["full"]) <= 100]
    return {"metrics": result, "as_of": current["gasDayStart"],
            "url": GIE_REPORT_URL, "points": points}


def alsi_inventory(row: dict) -> float | None:
    inventory = row.get("inventory")
    # Current ALSI records provide both liquid volume (lng) and energy (gwh).
    # The dashboard's LNG tank inventory uses the liquid volume in 10³ m³.
    if isinstance(inventory, dict):
        inventory = inventory.get("lng")
    return measured(inventory)


def parse_alsi(raw: bytes, region: str, today: date | None = None) -> dict:
    rows = gie_rows(raw, region)
    # An ALSI aggregate may be published before both measurements arrive.
    # Use the most recent complete observation and retain its actual date.
    complete = [row for row in rows if alsi_inventory(row) is not None
                and measured(row.get("sendOut")) is not None]
    if not complete:
        raise ValueError("ALSI " + region.upper() + " has no complete inventory/send-out observation")
    current = complete[0]
    observed = date.fromisoformat(current["gasDayStart"])
    today = today or datetime.now(timezone.utc).date()
    if not timedelta(0) <= today - observed <= timedelta(days=7):
        raise ValueError("ALSI " + region.upper() + " latest complete observation is stale")
    suffix, location = ("eu", "UE") if region == "eu" else ("fr", "France")
    inventory, sendout = alsi_inventory(current), measured(current.get("sendOut"))
    if not 0 <= inventory <= 50000 or not 0 <= sendout <= 30000:
        raise ValueError("ALSI inventory or send-out out of bounds")
    previous = next((row for row in complete[1:] if row["gasDayStart"] != current["gasDayStart"]), None)
    old_inventory = alsi_inventory(previous) if previous else None
    old_sendout = measured(previous.get("sendOut")) if previous else None
    flag = "Estimé par les opérateurs" if current.get("status") == "E" else "Déclaré par les opérateurs"
    result = [
        metric("lng_" + suffix + "_inventory", "gas", "GNL en cuves " + location,
               inventory, "10³ m³ GNL", inventory - old_inventory if old_inventory is not None else None,
               "vs veille", current["gasDayStart"], "GIE ALSI", ALSI_REPORT_URL, flag),
        metric("lng_" + suffix + "_sendout", "gas", "Émission terminaux GNL " + location,
               sendout, "GWh/j", sendout - old_sendout if old_sendout is not None else None,
               "vs veille", current["gasDayStart"], "GIE ALSI", ALSI_REPORT_URL, flag),
    ]
    points = [{"date": row["gasDayStart"], "value": float(measured(row["sendOut"]))}
              for row in reversed(complete) if measured(row["sendOut"]) is not None and
              0 <= float(measured(row["sendOut"])) <= 30000]
    return {"metrics": result, "as_of": current["gasDayStart"],
            "url": ALSI_REPORT_URL, "points": points}


def verified_calendar(today: date) -> list[dict]:
    """2026 US agency schedule, including the published holiday exceptions."""
    eastern = ZoneInfo("America/New_York")
    rows = []
    def add(day: date, hour: int, minute: int, label: str, context: str, url: str,
            day_only: bool = False) -> None:
        when = datetime.combine(day, time(hour, minute), eastern).astimezone(timezone.utc)
        rows.append({"at": when.isoformat(), "title": label, "context": context,
                     "url": url, "day_only": day_only})

    first = max(date(2026, 9, 25), today)
    last = date(2026, 12, 31)
    if first > last:
        return []
    oil_exceptions = {date(2026, 10, 14): (date(2026, 10, 15), 12),
                      date(2026, 11, 11): (date(2026, 11, 12), 12)}
    gas_exceptions = {date(2026, 11, 12): (date(2026, 11, 13), 10),
                      date(2026, 11, 26): (date(2026, 11, 25), 12)}
    day = first
    while day <= last:
        if day.weekday() == 2:  # Wednesday
            release, hour = oil_exceptions.get(day, (day, 10))
            if release >= today:
                add(release, hour, 30 if hour == 10 else 0, "EIA · stocks pétroliers WPSR",
                    "Brut, essence, distillats et raffineries US", "https://www.eia.gov/petroleum/supply/weekly/schedule.php")
        if day.weekday() == 3:  # Thursday
            release, hour = gas_exceptions.get(day, (day, 10))
            if release >= today:
                add(release, hour, 30 if hour == 10 else 0, "EIA · stockage gaz US",
                    "Variation et écart à la moyenne cinq ans", "https://ir.eia.gov/ngs/schedule.html")
        day += timedelta(days=1)
    for month, day_number in ((10, 9), (11, 10), (12, 10)):
        publication = date(2026, month, day_number)
        if publication >= today:
            add(publication, 12, 0, "USDA · WASDE",
                "Bilans mondiaux céréales et oléagineux",
                "https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report")
    if today <= date(2026, 10, 6):
        add(date(2026, 10, 6), 0, 0, "EIA · perspectives énergétiques STEO",
            "Date vérifiée ; horaire officiel non précisé",
            "https://www.eia.gov/outlooks/steo/release_schedule.php", day_only=True)
    return sorted(rows, key=lambda row: row["at"])


def get_previous() -> dict:
    if SNAPSHOT.exists():
        return json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    return {"metrics": [], "sources": {}, "stories": [], "history": {}}


def build_snapshot(previous: dict, results: dict, now: datetime) -> dict:
    values = {item["id"]: item for item in previous.get("metrics", [])}
    sources = previous.get("sources", {}).copy()
    history = previous.get("history", {}).copy()
    stories = previous.get("stories", [])
    for key in ("oil", "oil_flows", "oil_history", "gas", "wasde", "news", "norway",
                "brent", "wti", "henry", "gie", "gie_fr", "alsi", "alsi_fr",
                "rte_power", "entsoe_fr", "entsoe_de"):
        result = results.get(key)
        if isinstance(result, Exception):
            old = sources.get(key, {})
            sources[key] = {**old, "status": "error", "checked_at": now.isoformat(),
                            "message": "Dernière donnée conservée ; source indisponible."}
            continue
        if result is None:
            if key == "norway" and "oil_norway_liquids" in values:
                sources[key] = {"status": "manual", "as_of": values["oil_norway_liquids"]["as_of"],
                                "url": SODIR_URL,
                                "message": "Repère mensuel vérifié ; collecte automatique indisponible."}
            if key in ("gie", "gie_fr", "alsi", "alsi_fr"):
                sources[key] = {"status": "needs_key",
                                "url": GIE_REPORT_URL if key.startswith("gie") else ALSI_REPORT_URL,
                                "message": "Clé personnelle GIE requise."}
                prefix = {"gie": "gas_eu", "gie_fr": "gas_fr",
                          "alsi": "lng_eu", "alsi_fr": "lng_fr"}[key]
                for id in list(values):
                    if id == prefix or id.startswith(prefix + "_"):
                        del values[id]
                history.pop({"gie": "gas_eu", "gie_fr": "gas_fr",
                             "alsi": "lng_eu_sendout", "alsi_fr": "lng_fr_sendout"}[key], None)
            if key in ("entsoe_fr", "entsoe_de"):
                sources[key] = {"status": "needs_key", "url": ENTSOE_REPORT_URL,
                                "message": "Clé ENTSO-E requise pour la prévision J-1."}
                values.pop("power_forecast_" + key[-2:], None)
            continue
        sources[key] = {"status": "ok", "as_of": result.get("as_of"),
                        "url": result.get("url", NEWS_URL), "checked_at": now.isoformat()}
        if result.get("published"):
            sources[key]["published"] = result["published"]
        for item in result.get("metrics", []):
            values[item["id"]] = item
        if key == "oil_history":
            history["oil_crude"] = result["points"]
        if key in ("gie", "gie_fr", "alsi", "alsi_fr") and result.get("points"):
            history[{"gie": "gas_eu", "gie_fr": "gas_fr",
                     "alsi": "lng_eu_sendout", "alsi_fr": "lng_fr_sendout"}[key]] = result["points"]
        if key == "rte_power":
            history["power_fr"] = result["points"]
        if key == "news":
            stories = result["stories"]

    values["metal_copper"] = metric("metal_copper", "metals", "Production minière cuivre · monde",
                                     23, "Mt", None, "estimation annuelle", "2025",
                                     "USGS MCS 2026",
                                     "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-copper.pdf",
                                     "Repère structurel, pas un stock LME")
    sources["metals"] = {"status": "structural", "as_of": "2025", "url":
                           "https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports"}
    return {"schema": 3, "generated_at": now.isoformat(), "sources": sources,
            "metrics": list(values.values()), "history": history, "stories": stories,
            "calendar": verified_calendar(now.date())}


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
              "Les chiffres officiels sont collectés par [la tâche planifiée](.github/workflows/update-data.yml), puis intégrés à `index.html`. Chaque chiffre indique sa source, sa période et son unité. Brent, WTI et Henry Hub sont des cours spot EIA quotidiens, publiés avec retard ; ce ne sont pas des futures temps réel. Les liens TTF, PEG et JKM ne sont pas des cotations copiées. L'onglet **Power FR** affiche les mesures électriques RTE et, avec une clé ENTSO-E, des prévisions de demande France et DE-LU.\n\n"
              "## Sources & automatisation\n\n"
              "- EIA WPSR : stocks de brut, Cushing, Gulf Coast, essence, distillats, jet et SPR ; production, importations, exportations et brut traité par les raffineries US.\n"
              "- EIA WNGSR : stockage de gaz US et régions, variation hebdomadaire et écart à la moyenne cinq ans.\n"
              "- USDA WASDE : production, exportations prévues et stocks de maïs et soja US ; stocks mondiaux de maïs et blé, commerce mondial prévu du blé. Les révisions comparent les deux colonnes de prévision du même rapport.\n"
              "- EIA Today in Energy : titres et résumés d'analyses récentes.\n"
              "- Sodir (Norwegian Offshore Directorate) : chiffre mensuel provisoire d'août 2026 (pétrole, LGN et condensats), repère européen daté ; la source refuse actuellement les lectures automatisées du robot GitHub et ce chiffre n'est donc pas rafraîchi automatiquement.\n"
              "- EIA, tableaux de prix spot quotidiens : Brent Europe, WTI Cushing et Henry Hub ; le collecteur vérifie la correspondance des six dates et six colonnes avant publication.\n"
              "- GIE AGSI+ / ALSI : avec une clé API gratuite (accès aux **deux plateformes**), stockage gaz France/UE, soutirage net, stocks en cuves GNL et émissions des terminaux GNL France/UE. Ce sont des observations physiques quotidiennes, **pas des prix TTF, PEG ou JKM**. Créer la clé sur https://agsi.gie.eu/account, choisir accès AGSI + ALSI et enregistrer `GIE_API_KEY` dans Settings → Secrets and variables → Actions → New repository secret. Relancer le workflow depuis Actions. Sans clé, ces chiffres ne sont pas affichés.\n"
              "- RTE éCO2mix national temps réel : [dataset officiel](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/) actualisé à la source au quart d'heure ; consommation, nucléaire, gaz, vent, solaire, hydraulique, bioénergies et échanges physiques. Export = solde négatif ; import = positif. Le cockpit collecte un instantané toutes les deux heures via GitHub Actions et indique l'heure de la mesure et de la collecte. Demande résiduelle = consommation − éolien − solaire (calcul indicatif, **pas une prévision du prix**). Aucun compte requis.\n"
              "- ENTSO-E : prévision *day-ahead* de demande (A65/A01, Article 6.1.b, données [CC BY 4.0](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions)), France et Allemagne/Luxembourg ; affichage du pic prévu pour les prochaines 24 heures. Pour activer : créer un compte sur https://transparency.entsoe.eu/, demander l'accès API à `transparency@entsoe.eu` (objet `RESTful API access` et adresse enregistrée dans le corps), puis générer le jeton dans « My Account ». Enregistrer le jeton **uniquement** comme secret GitHub Actions `ENTSOE_API_TOKEN` via Settings → Secrets and variables → Actions → New repository secret ; relancer l'action. Ne jamais le coller dans le HTML, un fichier GitHub ou une conversation. Sans clé, RTE Power fonctionne déjà.\n"
              "- Prix électriques France/DE : bouton vers le [marché officiel RTE](https://www.rte-france.com/en/data-publications/eco2mix/market-data) ; les prix day-ahead EPEX ne sont pas couverts par la [liste ENTSO-E de réutilisation libre](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions) et RTE interdit la copie de ses prix via éCO2mix. Le jeton ENTSO-E n'est pas un droit de redistribution de ces cotations.\n"
              "- Calendrier natif : sorties EIA pétrole et gaz, USDA WASDE et STEO ; les exceptions 2026 connues sont incluses. Au-delà des dates vérifiées, le tableau l'indique sans inventer d'horaire.\n"
              "- Marchés : graphique et tableau de cotations indicatives TradingView/OANDA (Brent, WTI, gaz US, cuivre et or). Ce sont des instruments OTC indicatifs ; ils ne remplacent ni les futures ICE/NYMEX ni le spot EIA daté. Les widgets nécessitent Internet et le fournisseur peut limiter la diffusion. Aluminium, cacao et café sont accessibles via leurs pages de marché ; leurs prix ne sont pas intégrés sans droits vérifiés.\n"
              "- TTF/PEG/JKM : liens vers sources de marché ; un flux de cotations automatisé et redistribué publiquement nécessite un droit de diffusion. Aucune valeur ou spread instantané n'est inventé. ENTSO-E fournit des prévisions électriques ouvertes, ENTSOG des flux physiques de gaz, et GIE les stocks/terminaux.\n"
              "- Physique : courbes de 14 jours de remplissage AGSI France et d'émission ALSI France, 26 semaines de stocks de brut EIA ; les signaux de pression sont des scénarios conditionnels liés aux chiffres publiés, jamais un mouvement de prix constaté.\n"
              "- LME : [rapports de stocks](https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports) à consulter, sans chiffre de stock automatisé tant qu'un flux stable n'est pas vérifié.\n\n"
              "Unités : M bbl = millions de barils ; M bbl/j = millions de barils par jour ; Bcf = milliards de pieds cubes ; TWh = térawattheures ; GWh/j = gigawattheures par jour ; 10³ m³ GNL = milliers de mètres cubes de GNL liquide ; M bu = millions de boisseaux ; Mt = millions de tonnes. Stocks, prix et flux ne sont jamais additionnés.\n\n"
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
    tasks["brent"] = lambda: parse_eia_spot(fetch(EIA_OIL_SPOT_URL), "brent", now.date())
    tasks["wti"] = lambda: parse_eia_spot(fetch(EIA_OIL_SPOT_URL), "wti", now.date())
    tasks["henry"] = lambda: parse_eia_spot(fetch(EIA_GAS_SPOT_URL), "henry", now.date())
    tasks["rte_power"] = lambda: parse_rte_power(fetch(RTE_URL), now)
    entsoe_token = os.environ.get("ENTSOE_API_TOKEN", "").strip()
    if entsoe_token:
        for zone in POWER_ZONES:
            tasks["entsoe_" + zone] = (lambda code=zone: parse_entsoe_forecast(
                entsoe_query(code, now, entsoe_token), code, now))
    gie_key = os.environ.get("GIE_API_KEY", "")
    if gie_key:
        tasks["gie"] = lambda: parse_gie(fetch(GIE_URL, {"x-key": gie_key}))
        tasks["gie_fr"] = lambda: parse_gie(fetch(GIE_FR_URL, {"x-key": gie_key}), "fr")
        tasks["alsi"] = lambda: parse_alsi(fetch(ALSI_URL, {"x-key": gie_key}), "eu", now.date())
        tasks["alsi_fr"] = lambda: parse_alsi(fetch(ALSI_FR_URL, {"x-key": gie_key}), "fr", now.date())
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
                extra = ": " + str(error)[:100] if isinstance(error, ValueError) else ""
                print(f"{key}: unavailable ({type(error).__name__}{extra})", file=sys.stderr)
    snapshot = build_snapshot(previous, results, now)
    if not any(item.get("status") == "ok" for item in snapshot["sources"].values()):
        raise RuntimeError("No usable source: keeping published snapshot unchanged")
    save_snapshot(snapshot)
    print("Metrics:", len(snapshot["metrics"]), "| official headlines:", len(snapshot["stories"]))


if __name__ == "__main__":
    main()
