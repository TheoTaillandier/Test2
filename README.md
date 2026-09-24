<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Commodity Cockpit · Prix et marché physique</title>

  <style>
    :root {
      color-scheme: dark;
      --bg: #08110f;
      --panel: #101b18;
      --line: #294037;
      --fg: #f0f5f2;
      --muted: #a8bab0;
      --mint: #54d6a3;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--fg);
      font: 13px Arial, sans-serif;
    }

    a { color: var(--mint); text-decoration: none; }
    a:hover { text-decoration: underline; }
    button { cursor: pointer; font: inherit; }

    header {
      height: 58px;
      padding: 0 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--line);
    }

    header strong { font-size: 15px; }
    header span, .hint { color: var(--muted); font-size: 11px; }

    .shell {
      height: calc(100vh - 58px);
      min-height: 650px;
      padding: 10px;
      display: grid;
      grid-template-columns: minmax(0, 1.55fr) minmax(380px, 1fr);
      gap: 10px;
    }

    .card {
      min-height: 0;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: var(--panel);
      overflow: hidden;
    }

    .chart { display: flex; flex-direction: column; }

    .bar {
      min-height: 44px;
      padding: 0 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--line);
      gap: 8px;
    }

    .bar h2 { font-size: 12px; margin: 0; }
    .chart .widget { flex: 1; min-height: 0; }

    .aside {
      min-height: 0;
      display: grid;
      grid-template-rows: minmax(320px, 1.15fr) minmax(250px, 1fr);
      gap: 10px;
    }

    .watch { display: flex; flex-direction: column; }
    .watch .widget { flex: 1; min-height: 0; }
    .info { display: flex; flex-direction: column; }

    .tabs {
      display: flex;
      gap: 4px;
      padding: 6px;
      border-bottom: 1px solid var(--line);
    }

    .tabs button,
    .sector button {
      border: 0;
      border-radius: 4px;
      background: transparent;
      color: var(--muted);
      padding: 7px 9px;
    }

    .tabs button.active,
    .sector button.active {
      background: #20372e;
      color: var(--fg);
    }

    .pane {
      display: none;
      min-height: 0;
      flex: 1;
      overflow: auto;
    }

    .pane.active { display: block; }

    .feed-head {
      padding: 8px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      border-bottom: 1px solid var(--line);
    }

    .sector { display: flex; flex-wrap: wrap; gap: 2px; }
    .sector button { font-size: 10px; padding: 5px 7px; }
    .feed { padding: 0 11px; }

    .story {
      display: block;
      color: var(--fg);
      padding: 11px 1px;
      border-bottom: 1px solid var(--line);
      line-height: 1.35;
    }

    .story:hover { color: var(--mint); }

    .story small {
      display: block;
      margin-top: 5px;
      color: var(--muted);
      font-size: 10px;
    }

    .status {
      color: var(--muted);
      padding: 14px 2px;
      line-height: 1.5;
    }

    .source-links {
      padding: 12px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .source-links a {
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #15251f;
      font-size: 11px;
    }

    .intro {
      padding: 11px 12px;
      color: var(--muted);
      line-height: 1.45;
    }

    .tv, .tv > div { width: 100%; height: 100%; }

    @media (max-width: 980px) {
      .shell { height: auto; grid-template-columns: 1fr; }
      .chart { height: 650px; }

      .aside {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: minmax(460px, auto);
      }

      .watch, .info { height: 460px; }
    }

    @media (max-width: 680px) {
      header span { display: none; }
      .shell { display: block; }
      .chart { height: 520px; margin-bottom: 10px; }
      .aside { display: flex; flex-direction: column; }
      .watch { height: 480px; margin-bottom: 10px; }
      .info { height: 430px; }
    }
  </style>
</head>

<body>
  <header>
    <strong>Commodity Cockpit</strong>
    <span>Prix TradingView · actualités publiques · heure de Paris</span>
  </header>

  <main class="shell">
    <section class="card chart">
      <div class="bar">
        <h2>Graphique · Brent futures</h2>
        <a
          href="https://www.tradingview.com/chart/?symbol=ICEEUR%3ABRN1%21"
          target="_blank"
          rel="noopener noreferrer"
        >TradingView ↗</a>
      </div>

      <div class="widget">
        <div class="tv">
          <div></div>
          <script
            src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js"
            async
          >
          {
            "autosize": true,
            "symbol": "ICEEUR:BRN1!",
            "interval": "60",
            "timezone": "Europe/Paris",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "allow_symbol_change": true,
            "hide_top_toolbar": false,
            "save_image": false,
            "support_host": "https://www.tradingview.com"
          }
          </script>
        </div>
      </div>
    </section>

    <aside class="aside">
      <section class="card watch">
        <div class="bar">
          <h2>À surveiller · Last / Chg%</h2>
          <span class="hint">
            Futures continus, cotations possiblement différées
          </span>
        </div>

        <div class="widget">
          <div class="tv">
            <div></div>
            <script
              src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js"
              async
            >
            {
              "width": "100%",
              "height": "100%",
              "symbolsGroups": [
                {
                  "name": "MACRO",
                  "symbols": [
                    {
                      "name": "FX:EURUSD",
                      "displayName": "EUR/USD"
                    },
                    {
                      "name": "TVC:DXY",
                      "displayName": "Dollar index"
                    },
                    {
                      "name": "CME_MINI:ES1!",
                      "displayName": "S&P 500"
                    }
                  ]
                },
                {
                  "name": "ENERGY",
                  "symbols": [
                    {
                      "name": "ICEEUR:BRN1!",
                      "displayName": "Brent · ICE"
                    },
                    {
                      "name": "NYMEX:CL1!",
                      "displayName": "WTI · NYMEX"
                    },
                    {
                      "name": "ICEEUR:TTF1!",
                      "displayName": "TTF gas · ICE"
                    },
                    {
                      "name": "NYMEX:NG1!",
                      "displayName": "US gas · NYMEX"
                    }
                  ]
                },
                {
                  "name": "METALS",
                  "symbols": [
                    {
                      "name": "COMEX:GC1!",
                      "displayName": "Gold"
                    },
                    {
                      "name": "COMEX:HG1!",
                      "displayName": "Copper"
                    },
                    {
                      "name": "COMEX:ALI1!",
                      "displayName": "Aluminium"
                    }
                  ]
                },
                {
                  "name": "AGRI",
                  "symbols": [
                    {
                      "name": "CBOT:ZW1!",
                      "displayName": "Wheat"
                    },
                    {
                      "name": "CBOT:ZC1!",
                      "displayName": "Corn"
                    },
                    {
                      "name": "CBOT:ZS1!",
                      "displayName": "Soybeans"
                    }
                  ]
                },
                {
                  "name": "SOFTS",
                  "symbols": [
                    {
                      "name": "ICEUS:KC1!",
                      "displayName": "Coffee"
                    },
                    {
                      "name": "ICEUS:CC1!",
                      "displayName": "Cocoa"
                    },
                    {
                      "name": "ICEUS:SB1!",
                      "displayName": "Sugar"
                    }
                  ]
                }
              ],
              "showSymbolLogo": false,
              "isTransparent": true,
              "colorTheme": "dark",
              "locale": "en"
            }
            </script>
          </div>
        </div>
      </section>

      <section class="card info">
        <div class="tabs">
          <button class="active" data-pane="news">
            Veille physique
          </button>
          <button data-pane="calendar">
            Calendrier
          </button>
          <button data-pane="sources">
            Sources
          </button>
        </div>

        <div class="pane active" id="news">
          <div class="feed-head">
            <div class="sector">
              <button class="active" data-topic="energy">
                Énergie
              </button>
              <button data-topic="metals">
                Métaux
              </button>
              <button data-topic="agri">
                Agri
              </button>
            </div>

            <button id="refresh" title="Actualiser">↻</button>
          </div>

          <div class="feed" id="feed">
            <p class="status">Chargement des articles…</p>
          </div>

          <div class="intro">
            Sélection automatique par mots clés : lis l'article source
            pour confirmer son effet sur le marché physique.
          </div>
        </div>

        <div class="pane" id="calendar">
          <div class="tv">
            <div></div>
            <script
              src="https://s3.tradingview.com/external-embedding/embed-widget-events.js"
              async
            >
            {
              "colorTheme": "dark",
              "isTransparent": true,
              "locale": "en",
              "countryFilter": "us,eu,gb,cn",
              "width": "100%",
              "height": "100%"
            }
            </script>
          </div>
        </div>

        <div class="pane" id="sources">
          <div class="intro">
            Publications de stocks, flux et nouvelles de marché.
          </div>

          <div class="source-links">
            <a
              href="https://www.reuters.com/business/energy/"
              target="_blank"
              rel="noopener noreferrer"
            >Reuters · Energy ↗</a>

            <a
              href="https://www.reuters.com/markets/commodities/"
              target="_blank"
              rel="noopener noreferrer"
            >Reuters · Commodities ↗</a>

            <a
              href="https://www.eia.gov/petroleum/supply/weekly/"
              target="_blank"
              rel="noopener noreferrer"
            >EIA · Pétrole ↗</a>

            <a
              href="https://ir.eia.gov/"
              target="_blank"
              rel="noopener noreferrer"
            >EIA · Publications ↗</a>

            <a
              href="https://agsi.gie.eu/"
              target="_blank"
              rel="noopener noreferrer"
            >GIE · Stocks gaz UE ↗</a>

            <a
              href="https://www.lme.com/en/Market-data/Reports-and-data/Warehouse-and-stocks-reports"
              target="_blank"
              rel="noopener noreferrer"
            >LME · Stocks métaux ↗</a>
          </div>
        </div>
      </section>
    </aside>
  </main>

  <script>
    const queries = {
      energy:
        '(oil OR crude OR LNG OR natural gas) ' +
        '(supply OR exports OR refinery OR pipeline OR production OR storage OR tanker)',

      metals:
        '(copper OR aluminum OR aluminium OR nickel) ' +
        '(mine OR smelter OR production OR exports OR inventories)',

      agri:
        '(wheat OR corn OR soybeans OR coffee OR cocoa OR sugar) ' +
        '(harvest OR drought OR exports OR crop OR production)'
    };

    let topic = 'energy';
    let requestNumber = 0;

    function safeUrl(value) {
      try {
        const url = new URL(value);
        return /^https?:$/.test(url.protocol) ? url.href : null;
      } catch {
        return null;
      }
    }

    async function loadNews() {
      const request = ++requestNumber;
      const el = document.querySelector('#feed');

      el.replaceChildren();

      const loading = document.createElement('p');
      loading.className = 'status';
      loading.textContent = 'Recherche des articles récents…';
      el.append(loading);

      const params = new URLSearchParams({
        query: queries[topic] + ' sourcelang:english',
        mode: 'artlist',
        maxrecords: '25',
        timespan: '2d',
        sort: 'datedesc',
        format: 'json'
      });

      try {
        const response = await fetch(
          'https://api.gdeltproject.org/api/v2/doc/doc?' + params,
          { cache: 'no-store' }
        );

        if (!response.ok) {
          throw Error('service indisponible');
        }

        const data = await response.json();

        if (request !== requestNumber) return;

        el.replaceChildren();
        const unique = new Set();

        const articles = (data.articles || [])
          .filter(item => {
            const url = safeUrl(item.url);

            if (!url || !item.title || unique.has(url)) {
              return false;
            }

            unique.add(url);
            return true;
          })
          .slice(0, 6);

        if (!articles.length) {
          throw Error('aucun résultat');
        }

        for (const item of articles) {
          const link = document.createElement('a');
          link.className = 'story';
          link.href = safeUrl(item.url);
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          link.textContent = item.title;

          const meta = document.createElement('small');
          let date = '';

          if (item.seendate) {
            const raw = String(item.seendate);

            const parsed = /^\d{14}$/.test(raw)
              ? new Date(
                  raw.slice(0, 4) + '-' +
                  raw.slice(4, 6) + '-' +
                  raw.slice(6, 8) + 'T' +
                  raw.slice(8, 10) + ':' +
                  raw.slice(10, 12) + ':' +
                  raw.slice(12, 14) + 'Z'
                )
              : new Date(raw);

            if (!isNaN(parsed)) {
              date = new Intl.DateTimeFormat('fr-FR', {
                timeZone: 'Europe/Paris',
                day: 'numeric',
                month: 'short',
                hour: '2-digit',
                minute: '2-digit'
              }).format(parsed);
            }
          }

          meta.textContent = [item.domain, date]
            .filter(Boolean)
            .join(' · ');

          link.append(meta);
          el.append(link);
        }
      } catch (error) {
        if (request !== requestNumber) return;

        el.replaceChildren();

        const message = document.createElement('p');
        message.className = 'status';
        message.textContent =
          'Flux momentanément indisponible. Consulte Reuters ou les sources publiques dans l’onglet Sources.';

        el.append(message);
      }
    }

    document.querySelectorAll('.tabs button').forEach(button => {
      button.addEventListener('click', () => {
        document
          .querySelectorAll('.tabs button, .pane')
          .forEach(node => node.classList.remove('active'));

        button.classList.add('active');

        document
          .getElementById(button.dataset.pane)
          .classList.add('active');
      });
    });

    document.querySelectorAll('.sector button').forEach(button => {
      button.addEventListener('click', () => {
        document
          .querySelectorAll('.sector button')
          .forEach(node => node.classList.remove('active'));

        button.classList.add('active');
        topic = button.dataset.topic;
        loadNews();
      });
    });

    document
      .getElementById('refresh')
      .addEventListener('click', loadNews);

    loadNews();
    setInterval(loadNews, 15 * 60 * 1000);
  </script>
</body>
</html>
