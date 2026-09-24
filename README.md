# Commodity Cockpit

Tableau de bord personnel des matières premières : cotations indicatives, calendrier macro et chiffres du marché physique.

## Ouvrir la page

Télécharger [`index.html`](index.html) depuis GitHub avec **Download raw file**, puis ouvrir le fichier dans un navigateur avec une connexion Internet. Le bouton **Marchés / Physique** change de page. Les chiffres EIA, USDA et USGS sont des instantanés datés ; le site signale leur ancienneté et ne les présente pas comme des données en direct.

Les cotations TradingView affichées sur la page sont des prix spot ou CFD indicatifs. Certaines données de futures ICE/CME/LME ne sont pas autorisées dans les widgets externes. Les liens vers les contrats exacts restent disponibles sous la watchlist.

## Code complet

```html
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Commodity Cockpit | Marchés & physique</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #09120f;
      --panel: #111d18;
      --panel2: #17261e;
      --line: #30443a;
      --text: #edf6ef;
      --muted: #a9baae;
      --accent: #66dda7;
      --amber: #e8bf78;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--text); font: 13px/1.45 system-ui, Arial, sans-serif; }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
    button { font: inherit; cursor: pointer; }
    .header { min-height: 62px; padding: 10px 20px; border-bottom: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    .brand { display: flex; align-items: baseline; gap: 10px; }
    .brand strong { font-size: 17px; letter-spacing: -.02em; }
    .brand small { color: var(--muted); font-size: 11px; }
    .nav { display: flex; gap: 5px; }
    .nav button { padding: 8px 16px; border: 1px solid transparent; border-radius: 6px; background: transparent; color: var(--muted); }
    .nav button.active { border-color: var(--line); background: #1c3529; color: var(--text); }
    .page[hidden] { display: none !important; }
    .tape { height: 64px; overflow: hidden; border-bottom: 1px solid var(--line); }
    .tape .tradingview-widget-container { height: 64px; }
    .grid { min-height: 720px; height: calc(100vh - 126px); padding: 12px; display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(385px, 1fr); gap: 12px; }
    .right { min-height: 0; display: grid; grid-template-rows: minmax(420px, 1fr) 285px; gap: 12px; }
    .card { min-height: 0; background: var(--panel); border: 1px solid var(--line); border-radius: 9px; overflow: hidden; }
    .chart, .watch, .calendar { display: flex; flex-direction: column; }
    .bar { min-height: 49px; padding: 8px 14px; display: flex; align-items: center; justify-content: space-between; gap: 10px; border-bottom: 1px solid var(--line); }
    .bar h2 { margin: 0; font-size: 13px; }
    .bar small { color: var(--muted); font-size: 11px; }
    .widget { flex: 1; min-height: 0; }
    .tradingview-widget-container, .tradingview-widget-container__widget { width: 100%; height: 100%; }
    .chart-foot { padding: 8px 13px; color: var(--muted); font-size: 11px; border-top: 1px solid var(--line); }
    .watch-foot { padding: 9px 13px; border-top: 1px solid var(--line); color: var(--muted); font-size: 11px; }
    details { display: inline; }
    details summary { display: inline; color: var(--accent); cursor: pointer; }
    details[open] { display: block; margin-top: 6px; }
    .futures-links a { display: inline-block; margin: 5px 12px 0 0; }
    .physical { max-width: 1460px; margin: auto; padding: 20px; }
    .intro { margin-bottom: 17px; display: flex; align-items: end; justify-content: space-between; gap: 12px; }
    .intro h1 { font-size: 22px; letter-spacing: -.03em; margin: 0 0 4px; }
    .intro p { margin: 0; color: var(--muted); }
    .date-chip { white-space: nowrap; border: 1px solid var(--line); background: var(--panel2); border-radius: 6px; padding: 7px 10px; color: var(--muted); font-size: 11px; }
    .section-title { margin: 22px 0 10px; display: flex; justify-content: space-between; align-items: baseline; gap: 10px; }
    .section-title h2 { margin: 0; font-size: 14px; }
    .section-title small { color: var(--muted); }
    .metric-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
    .metric { border: 1px solid var(--line); border-radius: 8px; padding: 14px; background: var(--panel); }
    .metric .label { color: var(--muted); font-size: 11px; }
    .metric .value { font-size: 23px; letter-spacing: -.04em; font-weight: 700; margin: 5px 0 1px; white-space: nowrap; }
    .metric .unit { color: var(--muted); font-size: 10px; }
    .metric .delta { color: var(--amber); font-size: 11px; margin-top: 8px; min-height: 15px; }
    .metric .source { color: var(--muted); font-size: 10px; margin-top: 8px; }
    .insight-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
    .insight { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 15px; }
    .insight .topic { font-size: 10px; color: var(--accent); letter-spacing: .08em; font-weight: 700; }
    .insight h3 { margin: 8px 0; font-size: 14px; }
    .insight p { margin: 0 0 12px; color: var(--muted); font-size: 12px; }
    .insight .meta { font-size: 10px; color: var(--muted); }
    .footnote { padding: 14px 0 22px; font-size: 11px; color: var(--muted); }
    .stale { color: var(--amber); }
    @media (max-width: 1000px) {
      .grid { height: auto; grid-template-columns: 1fr; }
      .chart { height: 580px; }
      .right { grid-template-columns: 1fr 1fr; grid-template-rows: 500px; }
      .metric-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 680px) {
      .header { padding: 9px; flex-wrap: wrap; }
      .brand small { display: none; }
      .tape { height: 58px; }
      .grid { display: block; padding: 8px; }
      .chart { height: 490px; margin-bottom: 9px; }
      .right { display: flex; flex-direction: column; }
      .watch { height: 470px; margin-bottom: 9px; }
      .calendar { height: 330px; }
      .physical { padding: 14px 10px; }
      .intro { display: block; }
      .date-chip { display: inline-block; margin-top: 12px; }
      .insight-grid { grid-template-columns: 1fr; }
      .metric .value { font-size: 20px; }
    }
  </style>
</head>
<body>
  <header class="header">
    <div class="brand"><strong>Commodity Cockpit</strong><small>Prix · stocks · flux · récoltes</small></div>
    <nav class="nav" aria-label="Sections">
      <button type="button" class="active" data-page="markets" aria-selected="true">Marchés</button>
      <button type="button" data-page="physical" aria-selected="false">Physique</button>
    </nav>
  </header>

  <div id="markets" class="page">
    <div class="tape" aria-label="Prix indicatifs des matières premières">
      <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
          {
            "symbols": [
              {"proName":"TVC:UKOIL","title":"Brent indicatif"},
              {"proName":"TVC:USOIL","title":"WTI indicatif"},
              {"proName":"PEPPERSTONE:NATGAS","title":"Gaz US spot"},
              {"proName":"OANDA:XAUUSD","title":"Or spot"},
              {"proName":"FXCM:COPPER","title":"Cuivre CFD"},
              {"proName":"FOREXCOM:WHEAT","title":"Blé CFD"},
              {"proName":"PEPPERSTONE:COFFEE","title":"Café CFD"},
              {"proName":"FX:EURUSD","title":"EUR/USD"}
            ],
            "showSymbolLogo": false,
            "isTransparent": true,
            "displayMode": "regular",
            "colorTheme": "dark",
            "locale": "en"
          }
        </script>
      </div>
    </div>

    <main class="grid">
      <section class="card chart" aria-label="Graphique Brent">
        <div class="bar"><h2>Brent · graphique indicatif</h2><a href="https://www.tradingview.com/symbols/UKOIL/" target="_blank" rel="noopener noreferrer">Graphique ↗</a></div>
        <div class="widget">
          <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <script src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
              {"autosize":true,"symbol":"TVC:UKOIL","interval":"60","timezone":"Europe/Paris","theme":"dark","style":"1","locale":"en","allow_symbol_change":true,"hide_top_toolbar":false,"support_host":"https://www.tradingview.com"}
            </script>
          </div>
        </div>
        <div class="chart-foot">Prix indicatif TradingView. Le contrat ICE BRN1! est distinct et peut être soumis à des restrictions de diffusion.</div>
      </section>

      <aside class="right">
        <section class="card watch">
          <div class="bar"><h2>À surveiller · dernier prix / variation</h2><small>Spot et CFD indicatifs</small></div>
          <div class="widget">
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <script src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>
                {
                  "width": "100%", "height": "100%",
                  "symbolsGroups": [
                    {"name":"ÉNERGIE","symbols":[
                      {"name":"TVC:UKOIL","displayName":"Brent · indicatif"},
                      {"name":"TVC:USOIL","displayName":"WTI · indicatif"},
                      {"name":"PEPPERSTONE:NATGAS","displayName":"Gaz US · spot"}
                    ]},
                    {"name":"MÉTAUX","symbols":[
                      {"name":"OANDA:XAUUSD","displayName":"Or · spot"},
                      {"name":"OANDA:XAGUSD","displayName":"Argent · spot"},
                      {"name":"FXCM:COPPER","displayName":"Cuivre · CFD"}
                    ]},
                    {"name":"AGRI & SOFTS","symbols":[
                      {"name":"FOREXCOM:WHEAT","displayName":"Blé · CFD"},
                      {"name":"SKILLING:CORN","displayName":"Maïs · CFD"},
                      {"name":"PEPPERSTONE:COFFEE","displayName":"Café · CFD"},
                      {"name":"PEPPERSTONE:COCOA","displayName":"Cacao · CFD"}
                    ]},
                    {"name":"MACRO","symbols":[
                      {"name":"FX:EURUSD","displayName":"EUR/USD"},
                      {"name":"TVC:DXY","displayName":"Dollar index"}
                    ]}
                  ],
                  "showSymbolLogo": false, "isTransparent": true,
                  "colorTheme": "dark", "locale": "en"
                }
              </script>
            </div>
          </div>
          <div class="watch-foot">
            Les CFD et prix spot ne sont pas les futures ICE, CME ou LME.
            <details><summary>Contrats exacts de ta liste ↗</summary>
              <div class="futures-links">
                <a href="https://www.tradingview.com/symbols/ICEEUR-BRN1%21/" target="_blank" rel="noopener noreferrer">Brent BRN1!</a>
                <a href="https://www.tradingview.com/symbols/NYMEX-CL1%21/" target="_blank" rel="noopener noreferrer">WTI CL1!</a>
                <a href="https://www.tradingview.com/symbols/ICEEUR-TTF1%21/" target="_blank" rel="noopener noreferrer">TTF1!</a>
                <a href="https://www.tradingview.com/symbols/COMEX-HG1%21/" target="_blank" rel="noopener noreferrer">Cuivre HG1!</a>
                <a href="https://www.tradingview.com/symbols/CBOT-ZW1%21/" target="_blank" rel="noopener noreferrer">Blé ZW1!</a>
                <a href="https://www.tradingview.com/symbols/CBOT-ZC1%21/" target="_blank" rel="noopener noreferrer">Maïs ZC1!</a>
              </div>
            </details>
          </div>
        </section>
        <section class="card calendar">
          <div class="bar"><h2>Calendrier macro</h2><a href="https://www.tradingview.com/economic-calendar/" target="_blank" rel="noopener noreferrer">Ouvrir ↗</a></div>
          <div class="widget">
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <script src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
                {"colorTheme":"dark","isTransparent":true,"locale":"en","width":"100%","height":"100%"}
              </script>
            </div>
          </div>
        </section>
      </aside>
    </main>
  </div>

  <div id="physical" class="page" hidden>
    <main class="physical">
      <div class="intro">
        <div><h1>Marché physique</h1><p>Stocks, raffinage et récoltes : les chiffres utiles et ce qu'ils signalent.</p></div>
        <div class="date-chip" id="freshness">Données publiées les 11 et 23 sept. 2026</div>
      </div>

      <div class="section-title"><h2>Pétrole & produits · États-Unis</h2><small>EIA · semaine terminée le 18 septembre 2026</small></div>
      <div class="metric-grid">
        <article class="metric"><div class="label">Stocks commerciaux de brut</div><div class="value">426,4 M bbl</div><div class="unit">hors réserve stratégique</div><div class="delta">+3,0 M bbl sur la semaine</div><div class="source"><a href="https://www.eia.gov/petroleum/supply/weekly/archive/2026/2026_09_23/wpsr_2026_09_23.php" target="_blank" rel="noopener noreferrer">EIA · 23 sept. ↗</a></div></article>
        <article class="metric"><div class="label">Brut traité par les raffineries</div><div class="value">16,8 M b/j</div><div class="unit">volumes hebdomadaires moyens</div><div class="delta">−519 000 b/j sur la semaine</div><div class="source"><a href="https://www.eia.gov/petroleum/supply/weekly/archive/2026/2026_09_23/wpsr_2026_09_23.php" target="_blank" rel="noopener noreferrer">EIA · 23 sept. ↗</a></div></article>
        <article class="metric"><div class="label">Utilisation des raffineries</div><div class="value">94,0 %</div><div class="unit">capacité disponible</div><div class="delta">À rapprocher des stocks de produits</div><div class="source"><a href="https://www.eia.gov/petroleum/supply/weekly/archive/2026/2026_09_23/wpsr_2026_09_23.php" target="_blank" rel="noopener noreferrer">EIA · 23 sept. ↗</a></div></article>
        <article class="metric"><div class="label">Stocks d'essence</div><div class="value">−1,7 M bbl</div><div class="unit">variation hebdomadaire</div><div class="delta">6 % sous la moyenne sur cinq ans</div><div class="source"><a href="https://www.eia.gov/petroleum/supply/weekly/archive/2026/2026_09_23/wpsr_2026_09_23.php" target="_blank" rel="noopener noreferrer">EIA · 23 sept. ↗</a></div></article>
      </div>

      <div class="section-title"><h2>Agriculture · campagne 2026/27</h2><small>USDA WASDE · 11 septembre 2026</small></div>
      <div class="metric-grid">
        <article class="metric"><div class="label">Production de maïs US prévue</div><div class="value">15,8 Md bu</div><div class="unit">milliards de bushels</div><div class="delta">−213 M bu vs août</div><div class="source"><a href="https://www.usda.gov/oce/commodity/wasde/wasde0926.pdf" target="_blank" rel="noopener noreferrer">USDA · WASDE ↗</a></div></article>
        <article class="metric"><div class="label">Stocks mondiaux de maïs prévus</div><div class="value">272,1 Mt</div><div class="unit">millions de tonnes</div><div class="delta">−2,6 Mt vs août</div><div class="source"><a href="https://www.usda.gov/oce/commodity/wasde/wasde0926.pdf" target="_blank" rel="noopener noreferrer">USDA · WASDE ↗</a></div></article>
        <article class="metric"><div class="label">Stocks de soja US prévus</div><div class="value">310 M bu</div><div class="unit">fin de campagne 2026/27</div><div class="delta">−10 M bu vs août</div><div class="source"><a href="https://www.usda.gov/oce/commodity/wasde/wasde0926.pdf" target="_blank" rel="noopener noreferrer">USDA · WASDE ↗</a></div></article>
        <article class="metric"><div class="label">Cuivre · production minière mondiale</div><div class="value">23,0 Mt</div><div class="unit">estimation 2025 · repère annuel</div><div class="delta">Donnée structurelle, pas un stock LME</div><div class="source"><a href="https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-copper.pdf" target="_blank" rel="noopener noreferrer">USGS · 2026 ↗</a></div></article>
      </div>

      <div class="section-title"><h2>Lecture rapide du physique</h2><small>Basée sur les publications ci-dessus</small></div>
      <div class="insight-grid">
        <article class="insight"><div class="topic">OIL · INVENTAIRES</div><h3>Brut en hausse, essence en baisse</h3><p>Les stocks de brut US gagnent 3,0 M bbl alors que l'essence perd 1,7 M bbl. La divergence invite à regarder séparément le brut, le raffinage et les produits finis.</p><div class="meta">EIA · 23 septembre 2026</div></article>
        <article class="insight"><div class="topic">OIL · RAFFINAGE</div><h3>Traitement de brut en retrait</h3><p>Les raffineries ont traité 519 000 b/j de moins sur la semaine, avec une utilisation de 94,0 %. À suivre pour les marges, les approvisionnements de produits et les écarts Brent/WTI.</p><div class="meta">EIA · 23 septembre 2026</div></article>
        <article class="insight"><div class="topic">AGRI · OFFRE</div><h3>Prévision de maïs réduite</h3><p>L'USDA abaisse la récolte US de 213 M bu et les stocks mondiaux attendus de 2,6 Mt par rapport à août. La météo, les rendements et les exports restent les prochains points de contrôle.</p><div class="meta">USDA WASDE · 11 septembre 2026</div></article>
      </div>
      <p class="footnote">Ce sont des observations datées, pas des cours ou nouvelles en direct. Les prix de la page Marchés dépendent des widgets TradingView et d'une connexion Internet. Les futures exacts peuvent être soumis à des restrictions de diffusion.</p>
    </main>
  </div>
  <script>
    const buttons = document.querySelectorAll('.nav button');
    for (const button of buttons) {
      button.addEventListener('click', () => {
        for (const item of buttons) {
          const selected = item === button;
          item.classList.toggle('active', selected);
          item.setAttribute('aria-selected', String(selected));
          document.getElementById(item.dataset.page).hidden = !selected;
        }
      });
    }

    // These are dated snapshots. Flag them visibly once a newer release is due.
    const age = (Date.now() - Date.parse('2026-09-23T17:00:00Z')) / 86400000;
    if (age > 8) {
      const label = document.getElementById('freshness');
      label.textContent = 'Archive · vérifier les nouvelles publications EIA / USDA';
      label.classList.add('stale');
    }
  </script>
</body>
</html>
```
