<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Commodity Cockpit — Marchés</title>

  <style>
    :root {
      color-scheme: dark;
      --bg: #09110f;
      --panel: #101b18;
      --line: #294038;
      --text: #edf5f1;
      --muted: #a4b5ae;
      --accent: #59d7aa;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 14px Arial, sans-serif;
    }

    a {
      color: var(--accent);
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }

    header {
      height: 66px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 22px;
      border-bottom: 1px solid var(--line);
    }

    h1 {
      font-size: 18px;
      margin: 0;
    }

    header span {
      color: var(--muted);
      font-size: 11px;
    }

    .tape {
      height: 76px;
      border-bottom: 1px solid var(--line);
      overflow: hidden;
    }

    .layout {
      height: calc(100vh - 142px);
      min-height: 630px;
      display: grid;
      grid-template-columns: minmax(0, 2fr) minmax(350px, 1fr);
      gap: 12px;
      padding: 12px;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }

    .chart {
      display: flex;
      flex-direction: column;
      min-height: 0;
    }

    .chart-heading {
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--line);
    }

    h2 {
      font-size: 13px;
      margin: 0;
    }

    .widget-fill {
      flex: 1;
      min-height: 0;
    }

    .right {
      min-height: 0;
      display: grid;
      grid-template-rows: minmax(300px, 1.1fr) minmax(260px, .9fr);
      gap: 12px;
    }

    .calendar {
      display: flex;
      flex-direction: column;
      min-height: 0;
    }

    .calendar .widget-fill {
      min-height: 0;
    }

    .sources {
      padding: 16px;
      overflow: auto;
    }

    .sources p {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
      margin: 8px 0 12px;
    }

    .links {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .links a {
      padding: 11px;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #14221d;
      font-size: 12px;
    }

    .footnote {
      margin-top: 13px;
      font-size: 11px;
      color: var(--muted);
    }

    .tradingview-widget-container,
    .tradingview-widget-container__widget {
      width: 100%;
      height: 100%;
    }

    @media (max-width: 900px) {
      .layout {
        height: auto;
        grid-template-columns: 1fr;
      }

      .chart {
        height: 650px;
      }

      .right {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 420px;
      }

      .calendar,
      .sources {
        min-width: 0;
      }
    }

    @media (max-width: 650px) {
      header {
        padding: 0 12px;
      }

      .layout {
        padding: 8px;
      }

      .chart {
        height: 550px;
      }

      .right {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 420px auto;
      }

      .sources {
        min-height: 280px;
      }

      .links {
        grid-template-columns: 1fr 1fr;
      }
    }
  </style>
</head>

<body>
  <header>
    <h1>Commodity Cockpit</h1>
    <span>Sources publiques · données selon disponibilité des fournisseurs</span>
  </header>

  <!-- Bandeau de prix TradingView -->
  <div class="tape" aria-label="Prix de marché TradingView">
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>

      <script
        type="text/javascript"
        src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js"
        async
      >
      {
        "symbols": [
          {"proName": "TVC:UKOIL", "title": "Brent"},
          {"proName": "TVC:USOIL", "title": "WTI"},
          {"proName": "NYMEX:NG1!", "title": "US Gas"},
          {"proName": "COMEX:GC1!", "title": "Gold"},
          {"proName": "COMEX:HG1!", "title": "Copper"},
          {"proName": "FX:EURUSD", "title": "EUR/USD"},
          {"proName": "TVC:DXY", "title": "DXY"}
        ],
        "showSymbolLogo": false,
        "isTransparent": true,
        "displayMode": "adaptive",
        "colorTheme": "dark",
        "locale": "en"
      }
      </script>
    </div>
  </div>

  <main class="layout">

    <!-- Grand graphique à gauche -->
    <section class="panel chart">
      <div class="chart-heading">
        <h2>Graphique interactif · Brent</h2>

        <a
          href="https://www.tradingview.com/symbols/UKOIL/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Ouvrir TradingView ↗
        </a>
      </div>

      <div class="widget-fill">
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>

          <script
            type="text/javascript"
            src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js"
            async
          >
          {
            "autosize": true,
            "symbol": "TVC:UKOIL",
            "interval": "60",
            "timezone": "Europe/Paris",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "allow_symbol_change": true,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "calendar": false,
            "support_host": "https://www.tradingview.com"
          }
          </script>
        </div>
      </div>
    </section>

    <!-- Colonne de droite -->
    <aside class="right">

      <!-- Calendrier macro TradingView -->
      <section class="panel calendar">
        <div class="chart-heading">
          <h2>Calendrier macro</h2>

          <a
            href="https://www.tradingview.com/economic-calendar/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Plein écran ↗
          </a>
        </div>

        <div class="widget-fill">
          <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>

            <script
              type="text/javascript"
              src="https://s3.tradingview.com/external-embedding/embed-widget-events.js"
              async
            >
            {
              "colorTheme": "dark",
              "isTransparent": true,
              "locale": "en",
              "countryFilter": "us,eu,gb,cn",
              "importanceFilter": "0,1",
              "width": "100%",
              "height": "100%"
            }
            </script>
          </div>
        </div>
      </section>

      <!-- Liens vers les sources publiques -->
      <section class="panel sources">
        <h2>Actualités et marché physique</h2>

        <p>
          Ouvre la source qui t'intéresse. Les articles et publications
          affichés sur ces sites sont maintenus par leurs éditeurs.
        </p>

        <div class="links">
          <a
            href="https://www.reuters.com/business/energy/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Reuters · Energy ↗
          </a>

          <a
            href="https://www.reuters.com/markets/commodities/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Reuters · Commodities ↗
          </a>

          <a
            href="https://www.eia.gov/petroleum/supply/weekly/"
            target="_blank"
            rel="noopener noreferrer"
          >
            EIA · Stocks pétrole ↗
          </a>

          <a
            href="https://ir.eia.gov/"
            target="_blank"
            rel="noopener noreferrer"
          >
            EIA · Heures de publication ↗
          </a>

          <a
            href="https://agsi.gie.eu/"
            target="_blank"
            rel="noopener noreferrer"
          >
            GIE · Stocks gaz UE ↗
          </a>

          <a
            href="https://www.lme.com/en/Market-data/Reports-and-data/Warehouse-and-stocks-reports"
            target="_blank"
            rel="noopener noreferrer"
          >
            LME · Stocks métaux ↗
          </a>
        </div>

        <div class="footnote">
          Les widgets ont besoin d'une connexion Internet. Certains cours
          peuvent être différés selon la place de marché et le fournisseur.
        </div>
      </section>

    </aside>
  </main>
</body>
</html>
