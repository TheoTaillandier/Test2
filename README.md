# Commodity Cockpit

Tableau de bord personnel des matières premières. Dans l'onglet **Code**, ouvrir [`index.html`](index.html), cliquer sur **Raw** ou **Download raw file**, enregistrer le fichier en `.html`, puis l'ouvrir dans un navigateur. Le code HTML complet figure aussi ci-dessous.

Les chiffres physiques EIA et USDA sont collectés par [la tâche planifiée](.github/workflows/update-data.yml), puis intégrés à `index.html`. Chaque chiffre indique sa source, sa période et son unité. Les prix TradingView sont des références spot ou CFD indicatives ; certains futures sont bloqués hors de TradingView. Le cuivre USGS est un repère annuel.

## Sources & automatisation

- EIA WPSR : stocks de brut, Cushing, Gulf Coast, essence, distillats, jet et SPR ; production, importations, exportations et brut traité par les raffineries US.
- EIA WNGSR : stockage de gaz US et régions, variation hebdomadaire et écart à la moyenne cinq ans.
- USDA WASDE : production, exportations prévues et stocks de maïs et soja US ; stocks mondiaux de maïs et blé, commerce mondial prévu du blé. Les révisions comparent les deux colonnes de prévision du même rapport.
- EIA Today in Energy : titres et résumés d'analyses récentes.
- GIE AGSI+ : facultatif, ajouter une clé API personnelle `GIE_API_KEY` aux secrets du dépôt GitHub Actions. L'agrégat UE doit être reconnu dans la réponse avant tout affichage ; sans clé, aucun chiffre européen n'est montré.
- LME : [rapports de stocks](https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports) à consulter, sans chiffre de stock automatisé tant qu'un flux stable n'est pas vérifié.

Unités : M bbl = millions de barils ; M bbl/j = millions de barils par jour ; Bcf = milliards de pieds cubes ; M bu = millions de boisseaux ; Mt = millions de tonnes. Stocks et flux quotidiens ne sont jamais additionnés.

Les clés restent dans les secrets GitHub et ne sont jamais insérées dans les fichiers publics. Le fichier HTML contient un instantané et s'ouvre directement après téléchargement. Un téléchargement isolé ne reçoit pas les nouvelles données : récupérer la dernière version depuis GitHub. Les tâches GitHub planifiées peuvent être retardées ou désactivées après une longue période sans activité ; dans ce cas, l'onglet Actions permet la relance manuelle.

## Code complet

```html
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Commodity Cockpit — Marchés & physique</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #08110f;
      --surface: #101d18;
      --surface-2: #172820;
      --border: #2a4336;
      --text: #f0f5f1;
      --muted: #a4b9ab;
      --accent: #78dda8;
      --warm: #f1c984;
      --red: #f29a90;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--text); font: 13px/1.48 system-ui, -apple-system, Segoe UI, sans-serif; }
    button { font: inherit; cursor: pointer; }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .header { min-height: 62px; padding: 8px 18px; display: flex; justify-content: space-between; align-items: center; gap: 14px; border-bottom: 1px solid var(--border); }
    .brand strong { font-size: 17px; letter-spacing: -.025em; }
    .brand span { color: var(--muted); font-size: 11px; margin-left: 9px; }
    .nav { display: flex; gap: 5px; }
    .nav button, .filters button { border: 1px solid transparent; background: transparent; color: var(--muted); border-radius: 6px; padding: 8px 14px; }
    .nav button[aria-selected="true"], .filters button.active { background: #1b3629; border-color: var(--border); color: var(--text); }
    .page[hidden] { display: none !important; }
    .ticker { height: 60px; overflow: hidden; border-bottom: 1px solid var(--border); }
    .ticker .tradingview-widget-container { height: 60px; }
    .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; min-height: 0; }
    .bar { min-height: 46px; padding: 8px 13px; display: flex; align-items: center; justify-content: space-between; gap: 12px; border-bottom: 1px solid var(--border); }
    .bar h2 { margin: 0; font-size: 13px; }
    .bar small { font-size: 10px; color: var(--muted); }
    .widget, .tradingview-widget-container, .tradingview-widget-container__widget { width: 100%; height: 100%; min-height: 0; }
    .market-grid { height: min(750px, calc(100vh - 215px)); min-height: 615px; padding: 12px; display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(365px, 1fr); gap: 12px; }
    .chart, .watch, .calendar { display: flex; flex-direction: column; }
    .right { min-height: 0; display: grid; grid-template-rows: minmax(380px, 1fr) 255px; gap: 12px; }
    .chart .widget, .watch .widget, .calendar .widget { flex: 1; }
    .caption { padding: 8px 12px; border-top: 1px solid var(--border); color: var(--muted); font-size: 10px; }
    .market-snapshot, .release-list { border-top: 1px solid var(--border); padding: 8px 12px; flex: none; }
    .market-snapshot { min-height: 105px; }
    .market-snapshot h3, .release-list h3 { font-size: 10px; color: var(--muted); margin: 0 0 5px; font-weight: 600; }
    .market-snapshot .row, .release-list .row { display: flex; justify-content: space-between; gap: 8px; padding: 2px 0; font-size: 10px; }
    .market-snapshot .row b, .release-list .row b { font-weight: 600; color: var(--text); white-space: nowrap; }
    .market-snapshot .row small { color: var(--muted); }
    .release-list .row a { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .market-context { padding: 0 12px 18px; }
    .market-context h2 { font-size: 13px; margin: 4px 0 9px; }
    .mini-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
    .mini { padding: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 7px; }
    .mini small, .metric small { display: block; color: var(--muted); font-size: 10px; }
    .mini strong { display: block; font-size: 18px; margin: 4px 0 1px; }
    .mini span { color: var(--warm); font-size: 10px; }
    .workspace { max-width: 1460px; margin: auto; padding: 18px; }
    .page-intro { display: flex; align-items: end; justify-content: space-between; gap: 14px; margin-bottom: 15px; }
    .page-intro h1 { font-size: 22px; margin: 0 0 4px; letter-spacing: -.025em; }
    .page-intro p { color: var(--muted); margin: 0; }
    .stamp { border: 1px solid var(--border); background: var(--surface-2); border-radius: 6px; padding: 7px 10px; color: var(--muted); font-size: 10px; white-space: nowrap; }
    .source-status { display: flex; flex-wrap: wrap; gap: 7px; margin: 0 0 15px; }
    .badge { border: 1px solid var(--border); background: var(--surface); border-radius: 100px; padding: 5px 10px; font-size: 10px; color: var(--muted); }
    .badge.good { color: var(--accent); }
    .badge.warn { color: var(--warm); }
    .filters { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 12px; }
    .filters button { padding: 7px 11px; }
    .physical-layout { display: grid; grid-template-columns: minmax(0, 1fr) 350px; gap: 12px; align-items: start; }
    .section-heading { margin: 0 0 10px; font-size: 14px; }
    .metrics { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
    .metric { padding: 14px; min-height: 151px; }
    .metric .number { font-size: 23px; font-weight: 700; letter-spacing: -.035em; margin: 7px 0 2px; }
    .metric .change { color: var(--warm); font-size: 11px; min-height: 17px; }
    .metric .meta { color: var(--muted); font-size: 10px; margin-top: 9px; }
    .metric .detail { color: var(--muted); font-size: 10px; margin-top: 4px; }
    .physical-side { display: grid; gap: 12px; }
    .side-pad { padding: 13px; }
    .side-pad h3 { font-size: 12px; margin: 0 0 9px; }
    .side-pad p { margin: 0 0 8px; color: var(--muted); font-size: 11px; }
    .story { padding: 11px 0; border-top: 1px solid var(--border); }
    .story a { color: var(--text); font-size: 11px; font-weight: 600; }
    .story p { color: var(--muted); font-size: 10px; margin: 4px 0; }
    .story small { color: var(--muted); font-size: 10px; }
    .trend { margin-top: 12px; }
    .trend svg { width: 100%; height: 110px; overflow: visible; }
    .trend polyline { stroke: var(--accent); stroke-width: 2; fill: none; vector-effect: non-scaling-stroke; }
    .trend .axis { display: flex; justify-content: space-between; color: var(--muted); font-size: 10px; }
    .empty { padding: 20px; color: var(--muted); }
    .footer { max-width: 1460px; margin: auto; padding: 10px 18px 24px; font-size: 10px; color: var(--muted); }
    @media (max-width: 1050px) {
      .market-grid { height: auto; grid-template-columns: 1fr; }
      .chart { height: 575px; }
      .right { grid-template-columns: 1fr 1fr; grid-template-rows: 490px; }
      .physical-layout { grid-template-columns: 1fr; }
      .physical-side { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 680px) {
      .header { padding: 9px; flex-wrap: wrap; }
      .brand span { display: none; }
      .market-grid { display: block; padding: 8px; }
      .chart { height: 490px; margin-bottom: 9px; }
      .right { display: block; }
      .watch { height: 470px; margin-bottom: 9px; }
      .calendar { height: 310px; }
      .market-context { padding: 0 8px 15px; }
      .mini-grid, .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .workspace { padding: 12px 9px; }
      .page-intro { display: block; }
      .stamp { display: inline-block; margin-top: 10px; }
      .physical-side { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header class="header">
    <div class="brand"><strong>Commodity Cockpit</strong><span>Marchés · stocks · flux · récoltes</span></div>
    <nav class="nav" aria-label="Navigation">
      <button type="button" data-page="markets" aria-selected="true">Marchés</button>
      <button type="button" data-page="physical" aria-selected="false">Physique</button>
    </nav>
  </header>

  <section class="page" id="markets">
    <div class="ticker" aria-label="Prix indicatifs">
      <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
          {"symbols":[
            {"proName":"TVC:UKOIL","title":"Brent indicatif"},
            {"proName":"TVC:USOIL","title":"WTI indicatif"},
            {"proName":"PEPPERSTONE:NATGAS","title":"Gaz US spot"},
            {"proName":"OANDA:XAUUSD","title":"Or spot"},
            {"proName":"FXCM:COPPER","title":"Cuivre CFD"},
            {"proName":"FOREXCOM:WHEAT","title":"Blé CFD"},
            {"proName":"FX:EURUSD","title":"EUR/USD"}
          ],"showSymbolLogo":false,"isTransparent":true,"displayMode":"regular","colorTheme":"dark","locale":"en"}
        </script>
      </div>
    </div>
    <main class="market-grid">
      <section class="card chart">
        <div class="bar"><h2>Brent · graphique indicatif</h2><a href="https://www.tradingview.com/symbols/UKOIL/" target="_blank" rel="noopener noreferrer">Ouvrir ↗</a></div>
        <div class="widget">
          <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
              {"autosize":true,"symbol":"TVC:UKOIL","interval":"60","timezone":"Europe/Paris","theme":"dark","style":"1","locale":"en","allow_symbol_change":true,"hide_top_toolbar":false,"support_host":"https://www.tradingview.com"}
            </script>
          </div>
        </div>
        <div class="caption">Prix indicatif. Un contrat future exact peut avoir un prix différent et des restrictions de diffusion.</div>
      </section>
      <aside class="right">
        <section class="card watch">
          <div class="bar"><h2>À surveiller · cours / variation</h2><small>Spot et CFD indicatifs</small></div>
          <div class="widget">
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <script src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>
                {"width":"100%","height":"100%","symbolsGroups":[
                  {"name":"ÉNERGIE","symbols":[{"name":"TVC:UKOIL","displayName":"Brent indicatif"},{"name":"TVC:USOIL","displayName":"WTI indicatif"},{"name":"PEPPERSTONE:NATGAS","displayName":"Gaz US spot"}]},
                  {"name":"MÉTAUX","symbols":[{"name":"OANDA:XAUUSD","displayName":"Or spot"},{"name":"OANDA:XAGUSD","displayName":"Argent spot"},{"name":"FXCM:COPPER","displayName":"Cuivre CFD"}]},
                  {"name":"AGRI & SOFTS","symbols":[{"name":"FOREXCOM:WHEAT","displayName":"Blé CFD"},{"name":"SKILLING:CORN","displayName":"Maïs CFD"},{"name":"PEPPERSTONE:COFFEE","displayName":"Café CFD"},{"name":"PEPPERSTONE:COCOA","displayName":"Cacao CFD"}]},
                  {"name":"MACRO","symbols":[{"name":"FX:EURUSD","displayName":"EUR/USD"},{"name":"TVC:DXY","displayName":"Dollar index"}]}
                ],"showSymbolLogo":false,"isTransparent":true,"colorTheme":"dark","locale":"en"}
              </script>
            </div>
          </div>
          <div class="market-snapshot" id="market-snapshot"><h3>Repères physiques vérifiés · disponibles même sans cotations</h3></div>
          <div class="caption">Plusieurs futures ICE/CME sont réservés à TradingView. <a href="https://www.tradingview.com/symbols/ICEEUR-BRN1%21/" target="_blank" rel="noopener noreferrer">Brent ICE ↗</a> · <a href="https://www.tradingview.com/symbols/ICEEUR-TTF1%21/" target="_blank" rel="noopener noreferrer">TTF ICE ↗</a></div>
        </section>
        <section class="card calendar">
          <div class="bar"><h2>Calendrier économique</h2><a href="https://www.tradingview.com/economic-calendar/" target="_blank" rel="noopener noreferrer">Ouvrir ↗</a></div>
          <div class="widget">
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <script src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
                {"colorTheme":"dark","isTransparent":true,"locale":"en","width":"100%","height":"100%"}
              </script>
            </div>
          </div>
          <div class="release-list" id="release-list"><h3>Dernières publications vérifiées</h3></div>
        </section>
      </aside>
    </main>
    <section class="market-context"><h2>Le marché physique en quatre chiffres · <a href="#physical" data-open="physical">détails ↗</a></h2><div class="mini-grid" id="mini-grid"></div></section>
  </section>

  <section class="page" id="physical" hidden>
    <main class="workspace">
      <div class="page-intro"><div><h1>Intelligence du marché physique</h1><p>Chiffres officiels, variation, période mesurée et fraîcheur de chaque publication.</p></div><span class="stamp" id="updated">Chargement de l'instantané…</span></div>
      <div class="source-status" id="source-status"></div>
      <div class="filters" role="group" aria-label="Filtrer les matières premières">
        <button type="button" class="active" data-sector="oil">Pétrole</button>
        <button type="button" data-sector="gas">Gaz</button>
        <button type="button" data-sector="agri">Agriculture</button>
        <button type="button" data-sector="metals">Métaux</button>
      </div>
      <div class="physical-layout">
        <section><h2 class="section-heading" id="sector-heading">Pétrole · stocks physiques US</h2><div class="metrics" id="metrics"></div><div class="card side-pad trend" id="trend" hidden><h3>Stocks commerciaux de brut US · 26 dernières semaines</h3><svg viewBox="0 0 400 110" preserveAspectRatio="none" role="img" aria-label="Évolution hebdomadaire des stocks commerciaux de brut US"><polyline id="trend-line" points=""></polyline></svg><div class="axis"><span id="trend-start"></span><span id="trend-end"></span></div></div></section>
        <aside class="physical-side">
          <section class="card side-pad" id="takeaways"><h3>Ce que disent les publications</h3><div id="takeaway-list"></div></section>
          <section class="card side-pad"><h3>Analyses récentes · EIA</h3><p>Articles officiels sur l'énergie. Les titres ne sont pas des alertes de marché.</p><div id="stories"></div></section>
          <section class="card side-pad"><h3>Couverture des données</h3><p>Le gaz européen peut s'ajouter via la clé personnelle GIE AGSI+ dans GitHub Actions. Pour le cuivre, le chiffre USGS est annuel ; les <a href="https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports" target="_blank" rel="noopener noreferrer">stocks LME ↗</a> ne sont pas repris sans flux vérifié.</p></section>
        </aside>
      </div>
    </main>
  </section>

  <p class="footer">Sources : EIA WPSR et WNGSR, USDA WASDE, USGS, et GIE si configuré. Prix TradingView indicatifs, possiblement différés. Une source inaccessible conserve sa dernière valeur et est signalée.</p>

  <!-- Replaced by scripts/update_data.py; retained inside HTML for one-file opening. -->
  <script id="snapshot-data" type="application/json">
{
  "generated_at": "2026-09-24T23:13:36+00:00",
  "history": {
    "oil_crude": [
      {
        "date": "2026-03-27",
        "value": 461.636
      },
      {
        "date": "2026-04-03",
        "value": 464.717
      },
      {
        "date": "2026-04-10",
        "value": 463.804
      },
      {
        "date": "2026-04-17",
        "value": 465.729
      },
      {
        "date": "2026-04-24",
        "value": 459.495
      },
      {
        "date": "2026-05-01",
        "value": 457.182
      },
      {
        "date": "2026-05-08",
        "value": 452.876
      },
      {
        "date": "2026-05-15",
        "value": 445.013
      },
      {
        "date": "2026-05-22",
        "value": 441.686
      },
      {
        "date": "2026-05-29",
        "value": 433.712
      },
      {
        "date": "2026-06-05",
        "value": 426.485
      },
      {
        "date": "2026-06-12",
        "value": 418.222
      },
      {
        "date": "2026-06-19",
        "value": 412.134
      },
      {
        "date": "2026-06-26",
        "value": 408.359
      },
      {
        "date": "2026-07-03",
        "value": 411.357
      },
      {
        "date": "2026-07-10",
        "value": 409.665
      },
      {
        "date": "2026-07-17",
        "value": 411.675
      },
      {
        "date": "2026-07-24",
        "value": 404.508
      },
      {
        "date": "2026-07-31",
        "value": 406.987
      },
      {
        "date": "2026-08-07",
        "value": 424.41
      },
      {
        "date": "2026-08-14",
        "value": 428.815
      },
      {
        "date": "2026-08-21",
        "value": 428.91
      },
      {
        "date": "2026-08-28",
        "value": 424.46
      },
      {
        "date": "2026-09-04",
        "value": 424.069
      },
      {
        "date": "2026-09-11",
        "value": 423.429
      },
      {
        "date": "2026-09-18",
        "value": 426.398
      }
    ]
  },
  "metrics": [
    {
      "as_of": "2026-09-18",
      "change": 2.969,
      "comparison": "sur 1 semaine",
      "detail": "",
      "id": "oil_crude",
      "label": "Stocks commerciaux de brut",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 426.398
    },
    {
      "as_of": "2026-09-18",
      "change": 2.266,
      "comparison": "sur 1 semaine",
      "detail": "",
      "id": "oil_cushing",
      "label": "Stocks de Cushing",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 23.748
    },
    {
      "as_of": "2026-09-18",
      "change": -2.093,
      "comparison": "sur 1 semaine",
      "detail": "",
      "id": "oil_gulf",
      "label": "Stocks de brut Gulf Coast",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 244.08
    },
    {
      "as_of": "2026-09-18",
      "change": -1.686,
      "comparison": "sur 1 semaine",
      "detail": "",
      "id": "oil_gasoline",
      "label": "Stocks d’essence",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 206.046
    },
    {
      "as_of": "2026-09-18",
      "change": -0.428,
      "comparison": "sur 1 semaine",
      "detail": "",
      "id": "oil_distillate",
      "label": "Stocks de distillats",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 107.431
    },
    {
      "as_of": "2026-09-18",
      "change": 0.129,
      "comparison": "sur 1 semaine",
      "detail": "",
      "id": "oil_jet",
      "label": "Stocks de jet fuel",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 45.466
    },
    {
      "as_of": "2026-09-18",
      "change": -0.405,
      "comparison": "sur 1 semaine",
      "detail": "",
      "id": "oil_spr",
      "label": "Réserve stratégique US",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 284.552
    },
    {
      "as_of": "2026-09-18",
      "change": 53.0,
      "comparison": "sur 1 semaine",
      "detail": "+2.9 % vs moyenne 5 ans",
      "id": "gas_us",
      "label": "Stockage de gaz US · Lower 48",
      "sector": "gas",
      "source": "EIA WNGSR",
      "unit": "Bcf",
      "url": "https://ir.eia.gov/ngs/ngs.html",
      "value": 3351.0
    },
    {
      "as_of": "2026-09-18",
      "change": 20.0,
      "comparison": "sur 1 semaine",
      "detail": "+5.2 % vs moyenne 5 ans",
      "id": "gas_east",
      "label": "Stockage gaz · East US",
      "sector": "gas",
      "source": "EIA WNGSR",
      "unit": "Bcf",
      "url": "https://ir.eia.gov/ngs/ngs.html",
      "value": 815.0
    },
    {
      "as_of": "2026-09-18",
      "change": 25.0,
      "comparison": "sur 1 semaine",
      "detail": "+3.5 % vs moyenne 5 ans",
      "id": "gas_midwest",
      "label": "Stockage gaz · Midwest US",
      "sector": "gas",
      "source": "EIA WNGSR",
      "unit": "Bcf",
      "url": "https://ir.eia.gov/ngs/ngs.html",
      "value": 959.0
    },
    {
      "as_of": "2026-09-18",
      "change": 2.0,
      "comparison": "sur 1 semaine",
      "detail": "-1.7 % vs moyenne 5 ans",
      "id": "gas_south",
      "label": "Stockage gaz · South Central US",
      "sector": "gas",
      "source": "EIA WNGSR",
      "unit": "Bcf",
      "url": "https://ir.eia.gov/ngs/ngs.html",
      "value": 1041.0
    },
    {
      "as_of": "2025",
      "change": null,
      "comparison": "estimation annuelle",
      "detail": "Repère structurel, pas un stock LME",
      "id": "metal_copper",
      "label": "Production minière cuivre · monde",
      "sector": "metals",
      "source": "USGS MCS 2026",
      "unit": "Mt",
      "url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-copper.pdf",
      "value": 23
    },
    {
      "as_of": "2026-09-18",
      "change": -0.005,
      "comparison": "sur 1 semaine",
      "detail": "Débit quotidien moyen de la semaine",
      "id": "oil_production",
      "label": "Production de brut US",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl/j",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 13.939
    },
    {
      "as_of": "2026-09-18",
      "change": -1.181,
      "comparison": "sur 1 semaine",
      "detail": "Débit quotidien moyen de la semaine",
      "id": "oil_imports",
      "label": "Importations de brut US",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl/j",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 5.877
    },
    {
      "as_of": "2026-09-18",
      "change": -1.55,
      "comparison": "sur 1 semaine",
      "detail": "Débit quotidien moyen de la semaine",
      "id": "oil_exports",
      "label": "Exportations de brut US",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl/j",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 3.281
    },
    {
      "as_of": "2026-09-18",
      "change": -0.519,
      "comparison": "sur 1 semaine",
      "detail": "Débit quotidien moyen de la semaine",
      "id": "oil_refinery",
      "label": "Brut traité par les raffineries US",
      "sector": "oil",
      "source": "EIA WPSR",
      "unit": "M bbl/j",
      "url": "https://www.eia.gov/petroleum/supply/weekly/",
      "value": 16.811
    },
    {
      "as_of": "2026-09",
      "change": -213.0,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_corn_output",
      "label": "Production maïs US",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "M bu",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 15800.0
    },
    {
      "as_of": "2026-09",
      "change": -86.0,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_corn_stocks",
      "label": "Stocks finaux maïs US",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "M bu",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 1567.0
    },
    {
      "as_of": "2026-09",
      "change": 0.0,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_corn_exports",
      "label": "Exportations prévues maïs US",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "M bu",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 3275.0
    },
    {
      "as_of": "2026-09",
      "change": 16.0,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_soy_output",
      "label": "Production soja US",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "M bu",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 4535.0
    },
    {
      "as_of": "2026-09",
      "change": -10.0,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_soy_stocks",
      "label": "Stocks finaux soja US",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "M bu",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 310.0
    },
    {
      "as_of": "2026-09",
      "change": 25.0,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_soy_exports",
      "label": "Exportations prévues soja US",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "M bu",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 1685.0
    },
    {
      "as_of": "2026-09",
      "change": -2.56,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_world_corn",
      "label": "Stocks mondiaux de maïs",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "Mt",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 272.1
    },
    {
      "as_of": "2026-09",
      "change": 3.04,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_world_wheat",
      "label": "Stocks mondiaux de blé",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "Mt",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 276.29
    },
    {
      "as_of": "2026-09",
      "change": -0.94,
      "comparison": "vs rapport précédent",
      "detail": "Prévision de campagne, révisable",
      "id": "ag_world_wheat_trade",
      "label": "Commerce mondial de blé prévu",
      "sector": "agri",
      "source": "USDA WASDE",
      "unit": "Mt",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt",
      "value": 211.77
    }
  ],
  "schema": 1,
  "sources": {
    "gas": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-24T23:13:36+00:00",
      "status": "ok",
      "url": "https://ir.eia.gov/ngs/ngs.html"
    },
    "gie": {
      "message": "Clé personnelle GIE requise.",
      "status": "needs_key",
      "url": "https://agsi.gie.eu/"
    },
    "metals": {
      "as_of": "2025",
      "status": "structural",
      "url": "https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports"
    },
    "news": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-24T23:13:36+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/rss/todayinenergy.xml"
    },
    "oil": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-24T23:13:36+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_flows": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-24T23:13:36+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_history": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-24T23:13:36+00:00",
      "published": "2026-09-23",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "wasde": {
      "as_of": "2026-09",
      "checked_at": "2026-09-24T23:13:36+00:00",
      "status": "ok",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt"
    }
  },
  "stories": [
    {
      "date": "2026-09-22",
      "source": "EIA · Today in Energy",
      "summary": "Publicly traded companies represent a tiny share of the total number of companies producing crude oil and natural gas in the United States, but they make up a large share of U.S. production. In 2025, publicly traded companies accounted for just 2% of about 12,",
      "title": "Public companies produce most U.S. crude oil and natural gas",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68184"
    },
    {
      "date": "2026-09-18",
      "source": "EIA · Today in Energy",
      "summary": "The price of distillate fuel oil, often sold as diesel, is driven by the price of crude oil, retail margins, distribution costs, taxes, and crack spreads, the indicator we use for refining margins. Tight global supplies of distillate fuel oil and elevated crud",
      "title": "What goes into diesel prices?",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68164"
    },
    {
      "date": "2026-09-15",
      "source": "EIA · Today in Energy",
      "summary": "On August 28, 2026, Cheniere Energy, Inc., completed its Corpus Christi Liquefaction Stage 3 Project (CCL Stage 3) in Texas, taking custody and control of the seventh and last liquefied natural gas (LNG) train in the project.",
      "title": "Corpus Christi LNG expansion makes facility the second-largest in the United States",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68144"
    },
    {
      "date": "2026-09-10",
      "source": "EIA · Today in Energy",
      "summary": "We forecast U.S. crude oil production will average 13.8 million barrels per day (b/d) in 2026, surpassing the previous record of 13.7 million b/d set in 2025, in our latest Short-Term Energy Outlook (STEO).",
      "title": "United States on track for record crude oil production in 2026",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68125"
    },
    {
      "date": "2026-09-09",
      "source": "EIA · Today in Energy",
      "summary": "Low-cost Appalachian and Canadian natural gas supplies coupled with lower-than-usual regional consumption have pushed down natural gas prices at a major New England pricing hub in recent months to trade at a discount to the widely cited U.S. benchmark, Henry H",
      "title": "New England natural gas prices have been trading near record discounts to Henry Hub",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68124"
    },
    {
      "date": "2026-09-04",
      "source": "EIA · Today in Energy",
      "summary": "What are crack spreads and why are they elevated? Crack spreads are indicators of the profitability of refining crude oil into petroleum products such as gasoline and diesel. One common crack spread is calculated by subtracting the spot market price of a gallo",
      "title": "Elevated crack spreads and crude oil prices contribute to higher prices at the pump",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68104"
    },
    {
      "date": "2026-09-03",
      "source": "EIA · Today in Energy",
      "summary": "Sustained high temperatures have contributed to persistently high electricity demand in the Electric Reliability Council of Texas (ERCOT), the regional transmission organization for most of the state.",
      "title": "Weekly average load in ERCOT continues near record high",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68084"
    },
    {
      "date": "2026-09-01",
      "source": "EIA · Today in Energy",
      "summary": "U.S. liquefied natural gas (LNG) exports averaged 17.4 billion cubic feet per day (Bcf/d) in the first six months of the year, 23% more than the same period in 2025, according to our Natural Gas Monthly. In our latest Short-Term Energy Outlook, we estimate U.S",
      "title": "U.S. LNG exports rose 23% in the first half of 2026 because of higher capacity",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68064"
    }
  ]
}
</script>
  <script>
    const snapshot = JSON.parse(document.getElementById('snapshot-data').textContent);
    const metrics = Array.isArray(snapshot.metrics) ? snapshot.metrics : [];
    const byId = Object.fromEntries(metrics.map(item => [item.id, item]));
    const sectors = {oil: 'Pétrole · stocks physiques US', gas: 'Gaz · stockages',
      agri: 'Agriculture · prévisions USDA', metals: 'Métaux · repères structurels'};
    let selectedSector = 'oil';

    function number(value, digits = 1) {
      return new Intl.NumberFormat('fr-FR', {maximumFractionDigits: digits, minimumFractionDigits: digits}).format(value);
    }
    function period(value) {
      if (!value) return 'date inconnue';
      if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
        return new Intl.DateTimeFormat('fr-FR', {day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC'}).format(new Date(value + 'T12:00:00Z'));
      }
      if (/^\d{4}-\d{2}$/.test(value)) {
        return new Intl.DateTimeFormat('fr-FR', {month: 'long', year: 'numeric', timeZone: 'UTC'}).format(new Date(value + '-01T12:00:00Z'));
      }
      return value;
    }
    function age(item) {
      const sourceDate = item.as_of.length === 4 ? item.as_of + '-01-01' : item.as_of.length === 7 ? item.as_of + '-01' : item.as_of;
      return (Date.now() - Date.parse(sourceDate + 'T12:00:00Z')) / 86400000;
    }
    function stale(item) {
      return age(item) > ({oil: 13, gas: 13, agri: 49, metals: 800}[item.sector] || 14);
    }
    function safeLink(url) {
      try {
        const parsed = new URL(url);
        const hosts = ['www.eia.gov', 'ir.eia.gov', 'www.usda.gov', 'pubs.usgs.gov', 'agsi.gie.eu'];
        return parsed.protocol === 'https:' && hosts.includes(parsed.hostname) ? parsed.href : null;
      } catch { return null; }
    }
    function line(text, tag = 'div', className = '') {
      const element = document.createElement(tag);
      element.className = className;
      element.textContent = text;
      return element;
    }
    function changeText(item) {
      if (item.change === null || item.change === undefined) return item.comparison;
      const symbol = item.change > 0 ? '+' : item.change < 0 ? '−' : '';
      if (item.id === 'gas_eu') return symbol + number(Math.abs(item.change), 2) + ' point(s) vs veille';
      return symbol + number(Math.abs(item.change), digits(item)) + ' ' + item.unit + ' ' + item.comparison;
    }
    function digits(item) {
      return item.unit === 'Bcf' || item.unit === 'M bu' ? 0 : item.unit.startsWith('M bbl') ? 3 : 2;
    }

    function switchPage(page) {
      for (const button of document.querySelectorAll('.nav button')) {
        button.setAttribute('aria-selected', String(button.dataset.page === page));
      }
      for (const section of document.querySelectorAll('.page')) section.hidden = section.id !== page;
    }
    document.querySelectorAll('.nav button, [data-open]').forEach(button => {
      button.addEventListener('click', event => {
        event.preventDefault();
        switchPage(button.dataset.page || button.dataset.open);
      });
    });

    function renderMetric(item) {
      const card = line('', 'article', 'card metric');
      card.append(line(item.label, 'small'));
      card.append(line(number(item.value, digits(item)) + ' ' + item.unit, 'div', 'number'));
      card.append(line(changeText(item), 'div', 'change'));
      card.append(line((stale(item) ? 'ARCHIVE · ' : '') + 'Période : ' + period(item.as_of), 'div', 'meta'));
      if (item.detail) card.append(line(item.detail, 'div', 'detail'));
      const href = safeLink(item.url);
      if (href) {
        const source = line(item.source + ' ↗', 'a', 'detail');
        source.href = href;
        source.target = '_blank';
        source.rel = 'noopener noreferrer';
        card.append(source);
      }
      return card;
    }

    function renderStatus() {
      const container = document.getElementById('source-status');
      const labels = {oil: 'EIA stocks pétrole', oil_flows: 'EIA flux pétrole', gas: 'EIA gaz US', wasde: 'USDA WASDE',
        news: 'Analyses EIA', gie: 'GIE gaz UE', metals: 'USGS métaux'};
      for (const [id, label] of Object.entries(labels)) {
        const source = snapshot.sources?.[id] || {};
        const sample = {oil:'oil_crude',oil_flows:'oil_imports',gas:'gas_us',wasde:'ag_corn_stocks',
          gie:'gas_eu',metals:'metal_copper'}[id];
        const hasValue = Boolean(sample && byId[sample]) || (id === 'news' && (snapshot.stories || []).length > 0);
        const status = source.status === 'ok' ? period(source.as_of || '') :
          source.status === 'needs_key' ? 'clé requise' :
          source.status === 'structural' ? 'repère annuel' :
          hasValue ? 'dernière valeur conservée' : 'source indisponible';
        container.append(line(label + ' · ' + status, 'span',
          'badge ' + (source.status === 'ok' ? 'good' : 'warn')));
      }
      document.getElementById('updated').textContent = snapshot.generated_at ?
        'Collecte : ' + new Intl.DateTimeFormat('fr-FR', {dateStyle:'medium', timeStyle:'short', timeZone:'Europe/Paris'}).format(new Date(snapshot.generated_at)) + ' · Paris' :
        'Instantané local';
    }

    function renderMini() {
      const grid = document.getElementById('mini-grid');
      for (const id of ['oil_crude', 'oil_cushing', 'gas_us', 'ag_world_corn']) {
        const item = byId[id];
        if (!item) continue;
        const card = line('', 'div', 'mini');
        card.append(line(item.label, 'small'));
        card.append(line(number(item.value, item.unit === 'Bcf' || item.unit === 'M bu' ? 0 : 1) + ' ' + item.unit, 'strong'));
        card.append(line(changeText(item) + (stale(item) ? ' · archive' : ''), 'span'));
        grid.append(card);
      }
      if (!grid.children.length) grid.append(line('La collecte des chiffres physiques est en attente.', 'p', 'empty'));
    }

    function renderMarketSummary() {
      const box = document.getElementById('market-snapshot');
      for (const id of ['oil_crude', 'oil_imports', 'gas_us']) {
        const item = byId[id];
        if (!item) continue;
        const row = line('', 'div', 'row');
        const left = line(item.label, 'span');
        const right = line(number(item.value, digits(item)) + ' ' + item.unit, 'b');
        row.append(left, right);
        box.append(row);
      }
      if (box.children.length === 1) box.append(line('Collecte des chiffres en attente.', 'small'));
    }

    function renderReleases() {
      const box = document.getElementById('release-list');
      for (const [id, label] of [['oil_crude','EIA pétrole'], ['gas_us','EIA gaz'], ['ag_corn_stocks','USDA WASDE']]) {
        const item = byId[id];
        if (!item) continue;
        const row = line('', 'div', 'row');
        const link = line(label + ' ↗', 'a');
        link.href = safeLink(item.url);
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        row.append(link, line(period(item.as_of) + (stale(item) ? ' · archive' : ''), 'b'));
        box.append(row);
      }
      if (box.children.length === 1) box.append(line('En attente de publications vérifiées.', 'small'));
    }

    function renderTakeaways() {
      const box = document.getElementById('takeaway-list');
      box.replaceChildren();
      const selected = metrics.filter(item => item.sector === selectedSector && item.change !== null && item.change !== undefined);
      for (const item of selected.slice(0, 3)) {
        const note = line('', 'div', 'story');
        note.append(line(item.label + ' : ' + changeText(item) + '.', 'div'));
        note.append(line('Observation ' + item.source + ' · ' + period(item.as_of) + (stale(item) ? ' · archive' : ''), 'small'));
        box.append(note);
      }
      if (!box.children.length) box.append(line('Aucune variation vérifiée pour cette catégorie.', 'p'));
    }

    function renderStories() {
      const box = document.getElementById('stories');
      for (const item of (snapshot.stories || []).slice(0, 5)) {
        const href = safeLink(item.url);
        if (!href) continue;
        const story = line('', 'article', 'story');
        const title = line(item.title, 'a');
        title.href = href;
        title.target = '_blank';
        title.rel = 'noopener noreferrer';
        story.append(title);
        if (item.summary) story.append(line(item.summary, 'p'));
        story.append(line(item.source + ' · ' + period(item.date), 'small'));
        box.append(story);
      }
      if (!box.children.length) box.append(line('Flux d’analyses actuellement indisponible.', 'p'));
    }

    function renderTrend() {
      const panel = document.getElementById('trend');
      const points = snapshot.history?.oil_crude || [];
      panel.hidden = selectedSector !== 'oil' || points.length < 12;
      if (panel.hidden) return;
      const nums = points.map(point => point.value);
      const low = Math.min(...nums) - 3;
      const high = Math.max(...nums) + 3;
      const coords = nums.map((value, index) => {
        const x = 4 + (index * 392 / (nums.length - 1));
        const y = 100 - ((value - low) / (high - low) * 90);
        return x.toFixed(1) + ',' + y.toFixed(1);
      });
      document.getElementById('trend-line').setAttribute('points', coords.join(' '));
      document.getElementById('trend-start').textContent = period(points[0].date);
      document.getElementById('trend-end').textContent = period(points[points.length - 1].date);
    }

    function renderSector() {
      document.getElementById('sector-heading').textContent = sectors[selectedSector];
      const box = document.getElementById('metrics');
      box.replaceChildren();
      for (const item of metrics.filter(metric => metric.sector === selectedSector)) box.append(renderMetric(item));
      if (!box.children.length) box.append(line('Aucune valeur vérifiée disponible pour ce secteur.', 'p', 'empty'));
      document.querySelectorAll('.filters button').forEach(button => button.classList.toggle('active', button.dataset.sector === selectedSector));
      renderTakeaways();
      renderTrend();
    }

    document.querySelectorAll('.filters button').forEach(button => button.addEventListener('click', () => {
      selectedSector = button.dataset.sector;
      renderSector();
    }));
    renderStatus();
    renderMini();
    renderMarketSummary();
    renderReleases();
    renderStories();
    renderSector();
  </script>
</body>
</html>

```
