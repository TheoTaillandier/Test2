<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Commodity Market Cockpit</title>

  <style>
    :root {
      --background: #07100e;
      --panel: #0d1715;
      --panel-secondary: #111e1b;
      --border: #20302c;
      --text: #edf5f1;
      --muted: #82928d;
      --green: #46d7ae;
      --red: #ff6f73;
      --orange: #f1b85b;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(
          circle at 10% -10%,
          rgba(70, 215, 174, 0.1),
          transparent 30%
        ),
        var(--background);

      color: var(--text);
      font-family: Inter, Arial, sans-serif;
    }

    button,
    a {
      font: inherit;
    }

    button {
      cursor: pointer;
    }

    .app {
      min-height: 100vh;
      padding: 0 18px 18px;
    }

    /* HEADER */

    .header {
      height: 68px;
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 11px;
    }

    .logo {
      width: 34px;
      height: 34px;
      display: grid;
      place-items: center;
      border: 1px solid var(--green);
      border-radius: 5px;
      color: var(--green);
      font-size: 11px;
      font-weight: 700;
    }

    .brand-text {
      display: flex;
      flex-direction: column;
    }

    .brand-text strong {
      font-size: 13px;
    }

    .brand-text span {
      margin-top: 3px;
      color: var(--muted);
      font-size: 10px;
    }

    .sector-navigation {
      display: flex;
      gap: 4px;
      padding: 3px;
      background: #09110f;
      border: 1px solid var(--border);
      border-radius: 6px;
    }

    .sector-button {
      padding: 8px 15px;
      border: 0;
      border-radius: 4px;
      background: transparent;
      color: var(--muted);
      font-size: 11px;
    }

    .sector-button.active {
      background: var(--panel-secondary);
      color: var(--text);
    }

    .market-status {
      justify-self: end;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--muted);
      font-family: monospace;
      font-size: 10px;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      background: var(--green);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--green);
    }

    #clock {
      margin-left: 8px;
      color: var(--text);
    }

    /* TICKERS */

    .ticker-strip {
      height: 64px;
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      border-bottom: 1px solid var(--border);
    }

    .ticker {
      padding: 12px 14px;
      border-right: 1px solid var(--border);
      transition: 0.2s;
    }

    .ticker:first-child {
      border-left: 1px solid var(--border);
    }

    .ticker:hover,
    .ticker.selected {
      background: rgba(70, 215, 174, 0.05);
    }

    .ticker-line {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }

    .ticker-symbol,
    .ticker-unit {
      color: var(--muted);
      font-family: monospace;
      font-size: 9px;
    }

    .ticker-price {
      font-family: monospace;
      font-size: 14px;
    }

    .ticker-move {
      font-family: monospace;
      font-size: 10px;
    }

    .positive {
      color: var(--green);
    }

    .negative {
      color: var(--red);
    }

    /* MAIN LAYOUT */

    .workspace {
      height: calc(100vh - 150px);
      min-height: 680px;
      display: grid;
      grid-template-columns: minmax(0, 2.05fr) minmax(340px, 1fr);
      gap: 12px;
      padding-top: 12px;
    }

    .panel {
      overflow: hidden;
      background: rgba(13, 23, 21, 0.95);
      border: 1px solid var(--border);
      border-radius: 7px;
    }

    .panel-header {
      min-height: 72px;
      padding: 16px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }

    .eyebrow {
      margin: 0 0 6px;
      color: var(--green);
      font-family: monospace;
      font-size: 9px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    h1,
    h2,
    h3,
    p {
      margin-top: 0;
    }

    h1 {
      margin-bottom: 0;
      font-size: 18px;
    }

    h2 {
      margin-bottom: 0;
      font-size: 14px;
    }

    .instrument-name {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .contract,
    .date {
      padding: 4px 6px;
      border: 1px solid var(--border);
      border-radius: 3px;
      color: var(--muted);
      font-family: monospace;
      font-size: 9px;
    }

    /* CHART */

    .chart-panel {
      min-width: 0;
      display: flex;
      flex-direction: column;
    }

    .chart-buttons {
      display: flex;
      gap: 8px;
    }

    .periods {
      display: flex;
      padding: 2px;
      background: #08100e;
      border: 1px solid var(--border);
      border-radius: 4px;
    }

    .period-button {
      padding: 6px 9px;
      border: 0;
      border-radius: 3px;
      background: transparent;
      color: var(--muted);
      font-size: 10px;
    }

    .period-button.active {
      background: #1b2a26;
      color: var(--text);
    }

    .expand-button {
      width: 32px;
      border: 1px solid var(--border);
      border-radius: 4px;
      background: transparent;
      color: var(--muted);
    }

    .price-summary {
      padding: 18px 20px 0;
      display: flex;
      align-items: baseline;
      gap: 12px;
    }

    .main-price {
      font-family: monospace;
      font-size: 29px;
      font-weight: 600;
    }

    .main-move,
    .main-delta {
      font-family: monospace;
      font-size: 11px;
    }

    .main-delta {
      color: var(--muted);
    }

    .chart-container {
      position: relative;
      flex: 1;
      min-height: 380px;
      margin: 8px 18px 0 20px;
    }

    .chart {
      width: calc(100% - 45px);
      height: 100%;
      overflow: visible;
    }

    .chart-grid line {
      stroke: #1c2a27;
      stroke-width: 1;
    }

    .chart-area {
      fill: url("#chart-gradient");
    }

    .chart-line {
      fill: none;
      stroke: var(--green);
      stroke-width: 2.5;
      vector-effect: non-scaling-stroke;
    }

    .price-guide {
      stroke: var(--green);
      stroke-dasharray: 5 5;
      opacity: 0.35;
    }

    .last-point {
      fill: var(--green);
      stroke: var(--panel);
      stroke-width: 3;
    }

    .axis-y {
      position: absolute;
      top: 7%;
      right: 0;
      bottom: 11%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      color: #53635e;
      font-family: monospace;
      font-size: 9px;
    }

    .axis-x {
      position: absolute;
      right: 45px;
      bottom: 3px;
      left: 0;
      display: flex;
      justify-content: space-between;
      color: #53635e;
      font-family: monospace;
      font-size: 9px;
    }

    .price-label {
      position: absolute;
      top: 14%;
      right: 0;
      padding: 4px 6px;
      background: var(--green);
      border-radius: 2px;
      color: #04100c;
      font-family: monospace;
      font-size: 9px;
      font-weight: 700;
    }

    .chart-footer {
      min-height: 60px;
      padding: 0 18px;
      display: grid;
      grid-template-columns: repeat(4, 1fr) auto;
      align-items: center;
      border-top: 1px solid var(--border);
    }

    .metric {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .metric span {
      color: var(--muted);
      font-family: monospace;
      font-size: 9px;
    }

    .metric strong {
      font-family: monospace;
      font-size: 10px;
    }

    .tradingview-link {
      color: var(--green);
      font-size: 10px;
      text-decoration: none;
    }

    /* RIGHT COLUMN */

    .intelligence-column {
      min-height: 0;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 12px;
    }

    .catalyst-panel .panel-header {
      min-height: 68px;
      padding: 13px 15px;
    }

    .events {
      padding: 2px 14px;
    }

    .event {
      padding: 12px 0;
      display: grid;
      grid-template-columns: 48px 1fr auto;
      gap: 10px;
      align-items: center;
      border-bottom: 1px solid rgba(32, 48, 44, 0.75);
    }

    .event time {
      font-family: monospace;
      font-size: 10px;
    }

    .event-description {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .event-description strong {
      font-size: 10px;
    }

    .event-description span {
      color: var(--muted);
      font-size: 9px;
    }

    .impact {
      padding: 3px 5px;
      border-radius: 2px;
      font-family: monospace;
      font-size: 8px;
    }

    .impact-high {
      background: rgba(255, 111, 115, 0.1);
      color: var(--red);
    }

    .impact-medium {
      background: rgba(241, 184, 91, 0.1);
      color: var(--orange);
    }

    .calendar-button {
      width: 100%;
      padding: 12px 15px;
      border: 0;
      background: transparent;
      color: var(--muted);
      text-align: left;
      font-size: 9px;
    }

    .calendar-button span {
      float: right;
      color: var(--green);
    }

    /* NEWS AND PHYSICAL DATA */

    .news-panel {
      min-height: 0;
      display: flex;
      flex-direction: column;
    }

    .tabs {
      height: 46px;
      padding: 0 15px;
      display: flex;
      align-items: end;
      gap: 20px;
      border-bottom: 1px solid var(--border);
    }

    .tab {
      position: relative;
      height: 100%;
      border: 0;
      background: transparent;
      color: var(--muted);
      font-size: 10px;
    }

    .tab.active {
      color: var(--text);
    }

    .tab.active::after {
      content: "";
      position: absolute;
      right: 0;
      bottom: -1px;
      left: 0;
      height: 2px;
      background: var(--green);
    }

    .tab-content {
      display: none;
      overflow-y: auto;
    }

    .tab-content.active {
      display: block;
    }

    .headline {
      padding: 13px 15px;
      border-bottom: 1px solid rgba(32, 48, 44, 0.7);
    }

    .headline:hover {
      background: rgba(255, 255, 255, 0.02);
    }

    .headline-source {
      color: var(--green);
      font-family: monospace;
      font-size: 8px;
    }

    .headline h3 {
      margin: 6px 0 10px;
      font-size: 11px;
      font-weight: 500;
      line-height: 1.45;
    }

    .headline-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .headline-category {
      padding: 3px 5px;
      border: 1px solid var(--border);
      border-radius: 2px;
      color: #b2c0bc;
      font-family: monospace;
      font-size: 8px;
    }

    .headline-time {
      color: var(--muted);
      font-family: monospace;
      font-size: 8px;
    }

    .physical-grid {
      padding: 8px;
      display: grid;
      grid-template-columns: 1fr 1fr;
    }

    .physical-item {
      min-height: 95px;
      margin: 4px;
      padding: 13px;
      display: flex;
      flex-direction: column;
      gap: 7px;
      border: 1px solid var(--border);
    }

    .physical-item span {
      color: var(--muted);
      font-size: 9px;
    }

    .physical-item strong {
      font-family: monospace;
      font-size: 11px;
    }

    .physical-item small {
      color: var(--green);
      font-family: monospace;
      font-size: 8px;
    }

    .brief {
      padding: 20px;
    }

    .brief h3 {
      font-size: 16px;
    }

    .brief p,
    .brief li {
      color: #a4b2ad;
      font-size: 10px;
      line-height: 1.6;
    }

    /* DAILY FOCUS */

    .daily-focus {
      min-height: 60px;
      padding: 11px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border: 1px solid rgba(70, 215, 174, 0.3);
      border-radius: 7px;
      background: linear-gradient(
        90deg,
        rgba(70, 215, 174, 0.09),
        rgba(70, 215, 174, 0.02)
      );
    }

    .daily-focus strong {
      font-size: 10px;
    }

    .alert-button {
      padding: 7px 10px;
      border: 1px solid var(--green);
      border-radius: 3px;
      background: transparent;
      color: var(--green);
      font-family: monospace;
      font-size: 9px;
    }

    .toast {
      position: fixed;
      right: 24px;
      bottom: 22px;
      padding: 11px 15px;
      border-radius: 4px;
      background: var(--green);
      color: #06110e;
      font-family: monospace;
      font-size: 10px;
      font-weight: 700;
      opacity: 0;
      transform: translateY(15px);
      pointer-events: none;
      transition: 0.25s;
    }

    .toast.visible {
      opacity: 1;
      transform: translateY(0);
    }

    /* EXPANDED CHART */

    body.chart-expanded .ticker-strip,
    body.chart-expanded .intelligence-column {
      display: none;
    }

    body.chart-expanded .workspace {
      height: calc(100vh - 85px);
      grid-template-columns: 1fr;
    }

    /* RESPONSIVE */

    @media (max-width: 1000px) {
      .sector-navigation {
        display: none;
      }

      .header {
        grid-template-columns: 1fr auto;
      }

      .ticker-strip {
        height: auto;
        grid-template-columns: repeat(4, 1fr);
      }

      .ticker:nth-child(n + 5) {
        display: none;
      }

      .workspace {
        height: auto;
        grid-template-columns: 1fr;
      }

      .chart-panel {
        height: 650px;
      }

      .intelligence-column {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto;
      }

      .news-panel {
        grid-row: span 2;
      }
    }

    @media (max-width: 650px) {
      .app {
        padding: 0 9px 14px;
      }

      .market-status {
        font-size: 0;
      }

      #clock {
        font-size: 9px;
      }

      .ticker-strip {
        grid-template-columns: repeat(2, 1fr);
      }

      .ticker:nth-child(n + 5) {
        display: flex;
        flex-direction: column;
      }

      .ticker:nth-child(n + 7) {
        display: none;
      }

      .workspace {
        display: block;
      }

      .chart-panel {
        height: 570px;
        margin-bottom: 10px;
      }

      .intelligence-column {
        display: grid;
        grid-template-columns: 1fr;
      }

      .periods {
        display: none;
      }

      .chart-footer {
        grid-template-columns: 1fr 1fr auto;
      }

      .metric:nth-child(n + 3) {
        display: none;
      }
    }
  </style>
</head>

<body>
  <div class="app">

    <header class="header">
      <div class="brand">
        <div class="logo">TC</div>

        <div class="brand-text">
          <strong>Commodity Cockpit</strong>
          <span>Market intelligence</span>
        </div>
      </div>

      <nav class="sector-navigation">
        <button class="sector-button active" data-sector="energy">
          Energy
        </button>

        <button class="sector-button" data-sector="metals">
          Metals
        </button>

        <button class="sector-button" data-sector="agriculture">
          Agriculture
        </button>
      </nav>

      <div class="market-status">
        <span class="status-dot"></span>
        Markets live
        <span id="clock"></span>
      </div>
    </header>

    <section class="ticker-strip" id="ticker-strip"></section>

    <main class="workspace">

      <!-- LARGE LEFT-HAND MARKET VIEW -->

      <section class="panel chart-panel">
        <header class="panel-header">
          <div>
            <p class="eyebrow">Primary market</p>

            <div class="instrument-name">
              <h1 id="instrument-name">Brent Crude</h1>

              <span class="contract" id="instrument-contract">
                ICE · Front month
              </span>
            </div>
          </div>

          <div class="chart-buttons">
            <div class="periods">
              <button class="period-button">1D</button>
              <button class="period-button active">5D</button>
              <button class="period-button">1M</button>
              <button class="period-button">1Y</button>
            </div>

            <button
              class="expand-button"
              id="expand-chart"
              title="Expand chart"
            >
              ↗
            </button>
          </div>
        </header>

        <div class="price-summary">
          <strong class="main-price" id="main-price">$78.46</strong>

          <span class="main-move positive" id="main-move">
            +1.24%
          </span>

          <span class="main-delta" id="main-delta">
            +$0.96 today
          </span>
        </div>

        <div class="chart-container">
          <svg
            class="chart"
            viewBox="0 0 1000 510"
            preserveAspectRatio="none"
            aria-label="Illustrative commodity price chart"
          >
            <defs>
              <linearGradient
                id="chart-gradient"
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop
                  offset="0%"
                  stop-color="#46d7ae"
                  stop-opacity="0.28"
                />

                <stop
                  offset="100%"
                  stop-color="#46d7ae"
                  stop-opacity="0"
                />
              </linearGradient>
            </defs>

            <g class="chart-grid">
              <line x1="0" y1="60" x2="1000" y2="60"></line>
              <line x1="0" y1="155" x2="1000" y2="155"></line>
              <line x1="0" y1="250" x2="1000" y2="250"></line>
              <line x1="0" y1="345" x2="1000" y2="345"></line>
              <line x1="0" y1="440" x2="1000" y2="440"></line>
            </g>

            <path
              class="chart-area"
              d="
                M0 406
                C40 390 62 410 98 367
                S162 350 192 374
                S255 330 286 344
                S330 286 375 312
                S440 292 470 242
                S535 276 570 226
                S630 196 670 225
                S728 154 760 172
                S825 126 860 146
                S918 78 1000 91
                L1000 510
                L0 510
                Z
              "
            ></path>

            <path
              class="chart-line"
              d="
                M0 406
                C40 390 62 410 98 367
                S162 350 192 374
                S255 330 286 344
                S330 286 375 312
                S440 292 470 242
                S535 276 570 226
                S630 196 670 225
                S728 154 760 172
                S825 126 860 146
                S918 78 1000 91
              "
            ></path>

            <line
              class="price-guide"
              x1="0"
              y1="91"
              x2="1000"
              y2="91"
            ></line>

            <circle
              class="last-point"
              cx="1000"
              cy="91"
              r="6"
            ></circle>
          </svg>

          <div class="axis-y">
            <span>79.20</span>
            <span>78.60</span>
            <span>78.00</span>
            <span>77.40</span>
            <span>76.80</span>
          </div>

          <div class="axis-x">
            <span>16 Sep</span>
            <span>17 Sep</span>
            <span>18 Sep</span>
            <span>19 Sep</span>
            <span>22 Sep</span>
          </div>

          <div class="price-label" id="price-label">
            78.46
          </div>
        </div>

        <footer class="chart-footer">
          <div class="metric">
            <span>Day range</span>
            <strong>77.12 — 79.03</strong>
          </div>

          <div class="metric">
            <span>Volume</span>
            <strong>184.2K</strong>
          </div>

          <div class="metric">
            <span>Open interest</span>
            <strong>2.08M</strong>
          </div>

          <div class="metric">
            <span>Brent–WTI</span>
            <strong>$4.31</strong>
          </div>

          <a
            class="tradingview-link"
            href="https://www.tradingview.com/"
            target="_blank"
            rel="noopener"
          >
            Open TradingView ↗
          </a>
        </footer>
      </section>

      <!-- RIGHT-HAND INTELLIGENCE COLUMN -->

      <aside class="intelligence-column">

        <section class="panel catalyst-panel">
          <header class="panel-header">
            <div>
              <p class="eyebrow">Next 24 hours</p>
              <h2>Market catalysts</h2>
            </div>

            <span class="date">Tue 22 Sep</span>
          </header>

          <div class="events">
            <article class="event">
              <time>14:30</time>

              <div class="event-description">
                <strong>US crude inventories</strong>
                <span>EIA weekly report · Energy</span>
              </div>

              <span class="impact impact-high">HIGH</span>
            </article>

            <article class="event">
              <time>16:00</time>

              <div class="event-description">
                <strong>US consumer confidence</strong>
                <span>Conference Board · Macro</span>
              </div>

              <span class="impact impact-medium">MED</span>
            </article>

            <article class="event">
              <time>18:00</time>

              <div class="event-description">
                <strong>Fed Chair remarks</strong>
                <span>Rates and USD sensitivity</span>
              </div>

              <span class="impact impact-medium">MED</span>
            </article>
          </div>

          <button class="calendar-button">
            View full calendar
            <span>→</span>
          </button>
        </section>

        <section class="panel news-panel">

          <nav class="tabs">
            <button class="tab active" data-tab="headlines">
              Headlines
            </button>

            <button class="tab" data-tab="physical">
              Physical
            </button>

            <button class="tab" data-tab="brief">
              My brief
            </button>
          </nav>

          <div class="tab-content active" id="headlines">
            <article class="headline">
              <span class="headline-source">
                REUTERS · 08:31
              </span>

              <h3>
                Oil edges higher as traders assess supply risks
                and the inventory outlook
              </h3>

              <div class="headline-footer">
                <span class="headline-category">OIL</span>
                <span class="headline-time">3 min ago</span>
              </div>
            </article>

            <article class="headline">
              <span class="headline-source">
                REUTERS · 08:12
              </span>

              <h3>
                European gas prices gain as Norwegian pipeline
                flows decline
              </h3>

              <div class="headline-footer">
                <span class="headline-category">GAS</span>
                <span class="headline-time">22 min ago</span>
              </div>
            </article>

            <article class="headline">
              <span class="headline-source">
                MARKET · 07:46
              </span>

              <h3>
                Copper steadies as the dollar softens ahead of
                US economic data
              </h3>

              <div class="headline-footer">
                <span class="headline-category">METALS</span>
                <span class="headline-time">48 min ago</span>
              </div>
            </article>

            <article class="headline">
              <span class="headline-source">
                AGRI · 07:18
              </span>

              <h3>
                Wheat futures monitor the pace of Black Sea exports
              </h3>

              <div class="headline-footer">
                <span class="headline-category">GRAINS</span>
                <span class="headline-time">1 hour ago</span>
              </div>
            </article>
          </div>

          <div class="tab-content" id="physical">
            <div class="physical-grid">
              <div class="physical-item">
                <span>EIA crude stocks</span>
                <strong>Wed · 14:30</strong>
                <small>Consensus: −1.4m bbl</small>
              </div>

              <div class="physical-item">
                <span>Norwegian gas flows</span>
                <strong>319 mcm/d</strong>
                <small class="negative">−2.8% day/day</small>
              </div>

              <div class="physical-item">
                <span>ARA gasoil stocks</span>
                <strong>2.21m tonnes</strong>
                <small>Thursday update</small>
              </div>

              <div class="physical-item">
                <span>LME inventories</span>
                <strong>Watch copper</strong>
                <small>Daily · 09:00</small>
              </div>
            </div>
          </div>

          <div class="tab-content" id="brief">
            <div class="brief">
              <p class="eyebrow">Morning view</p>

              <h3>Energy leads market sentiment</h3>

              <p>
                Oil remains firm but headline-driven. The main
                variables today are US inventories, the dollar's
                response to macroeconomic data and European gas flows.
              </p>

              <ul>
                <li>Bias: cautiously bullish Brent</li>
                <li>Important technical level: $79.00</li>
                <li>Main downside risk: stronger US dollar</li>
              </ul>
            </div>
          </div>
        </section>

        <section class="daily-focus">
          <div>
            <p class="eyebrow">Today's focus</p>
            <strong>US inventories at 14:30</strong>
          </div>

          <button class="alert-button" id="alert-button">
            Set alert
          </button>
        </section>
      </aside>
    </main>
  </div>

  <div class="toast" id="toast">
    Alert saved for 14:25
  </div>

  <script>
    const markets = {
      energy: [
        {
          symbol: "BRENT",
          name: "Brent Crude",
          contract: "ICE · Front month",
          price: "78.46",
          move: "+1.24%",
          delta: "+$0.96 today",
          unit: "USD/bbl",
          currency: "$",
          positive: true
        },
        {
          symbol: "WTI",
          name: "WTI Crude",
          contract: "NYMEX · Front month",
          price: "74.15",
          move: "+1.08%",
          delta: "+$0.79 today",
          unit: "USD/bbl",
          currency: "$",
          positive: true
        },
        {
          symbol: "TTF",
          name: "Dutch TTF Gas",
          contract: "ICE Endex · Front month",
          price: "36.82",
          move: "+2.41%",
          delta: "+€0.87 today",
          unit: "EUR/MWh",
          currency: "€",
          positive: true
        },
        {
          symbol: "JKM",
          name: "Japan Korea Marker",
          contract: "Platts · Front month",
          price: "12.64",
          move: "−0.32%",
          delta: "−$0.04 today",
          unit: "USD/MMBtu",
          currency: "$",
          positive: false
        },
        {
          symbol: "GASOIL",
          name: "Low Sulphur Gasoil",
          contract: "ICE · Front month",
          price: "724.50",
          move: "+0.76%",
          delta: "+$5.46 today",
          unit: "USD/mt",
          currency: "$",
          positive: true
        },
        {
          symbol: "EUR/USD",
          name: "Euro / US Dollar",
          contract: "FX spot",
          price: "1.1742",
          move: "−0.18%",
          delta: "−0.0021 today",
          unit: "SPOT",
          currency: "",
          positive: false
        },
        {
          symbol: "DXY",
          name: "US Dollar Index",
          contract: "ICE · Spot index",
          price: "97.61",
          move: "+0.22%",
          delta: "+0.21 today",
          unit: "INDEX",
          currency: "",
          positive: true
        }
      ],

      metals: [
        {
          symbol: "COPPER",
          name: "LME Copper",
          contract: "LME · 3 month",
          price: "10,184",
          move: "+0.84%",
          delta: "+$85 today",
          unit: "USD/mt",
          currency: "$",
          positive: true
        },
        {
          symbol: "GOLD",
          name: "Gold",
          contract: "COMEX · Front month",
          price: "3,706",
          move: "+0.42%",
          delta: "+$15.40 today",
          unit: "USD/oz",
          currency: "$",
          positive: true
        },
        {
          symbol: "ALUMINIUM",
          name: "LME Aluminium",
          contract: "LME · 3 month",
          price: "2,674",
          move: "−0.28%",
          delta: "−$7.50 today",
          unit: "USD/mt",
          currency: "$",
          positive: false
        },
        {
          symbol: "NICKEL",
          name: "LME Nickel",
          contract: "LME · 3 month",
          price: "15,420",
          move: "+0.19%",
          delta: "+$29 today",
          unit: "USD/mt",
          currency: "$",
          positive: true
        },
        {
          symbol: "IRON ORE",
          name: "Iron Ore 62%",
          contract: "SGX · Front month",
          price: "104.61",
          move: "−0.61%",
          delta: "−$0.64 today",
          unit: "USD/dmt",
          currency: "$",
          positive: false
        },
        {
          symbol: "EUR/USD",
          name: "Euro / US Dollar",
          contract: "FX spot",
          price: "1.1742",
          move: "−0.18%",
          delta: "−0.0021 today",
          unit: "SPOT",
          currency: "",
          positive: false
        },
        {
          symbol: "DXY",
          name: "US Dollar Index",
          contract: "ICE · Spot index",
          price: "97.61",
          move: "+0.22%",
          delta: "+0.21 today",
          unit: "INDEX",
          currency: "",
          positive: true
        }
      ],

      agriculture: [
        {
          symbol: "WHEAT",
          name: "Milling Wheat",
          contract: "Euronext · Front month",
          price: "193.75",
          move: "+0.52%",
          delta: "+€1.00 today",
          unit: "EUR/mt",
          currency: "€",
          positive: true
        },
        {
          symbol: "CORN",
          name: "Corn",
          contract: "CBOT · Front month",
          price: "428.25",
          move: "−0.35%",
          delta: "−1.50 today",
          unit: "USd/bu",
          currency: "",
          positive: false
        },
        {
          symbol: "SOYBEAN",
          name: "Soybeans",
          contract: "CBOT · Front month",
          price: "1,012",
          move: "+0.27%",
          delta: "+2.75 today",
          unit: "USd/bu",
          currency: "",
          positive: true
        },
        {
          symbol: "COCOA",
          name: "London Cocoa",
          contract: "ICE · Front month",
          price: "5,321",
          move: "−1.44%",
          delta: "−£78 today",
          unit: "GBP/mt",
          currency: "£",
          positive: false
        },
        {
          symbol: "SUGAR",
          name: "Raw Sugar No.11",
          contract: "ICE · Front month",
          price: "16.08",
          move: "+0.63%",
          delta: "+0.10 today",
          unit: "USd/lb",
          currency: "",
          positive: true
        },
        {
          symbol: "EUR/USD",
          name: "Euro / US Dollar",
          contract: "FX spot",
          price: "1.1742",
          move: "−0.18%",
          delta: "−0.0021 today",
          unit: "SPOT",
          currency: "",
          positive: false
        },
        {
          symbol: "DXY",
          name: "US Dollar Index",
          contract: "ICE · Spot index",
          price: "97.61",
          move: "+0.22%",
          delta: "+0.21 today",
          unit: "INDEX",
          currency: "",
          positive: true
        }
      ]
    };

    const tickerStrip = document.querySelector("#ticker-strip");
    let activeSector = "energy";

    function displayMarket(market) {
      document.querySelector("#instrument-name").textContent =
        market.name;

      document.querySelector("#instrument-contract").textContent =
        market.contract;

      document.querySelector("#main-price").textContent =
        market.currency + market.price;

      document.querySelector("#main-delta").textContent =
        market.delta;

      document.querySelector("#price-label").textContent =
        market.price;

      const movement = document.querySelector("#main-move");

      movement.textContent = market.move;
      movement.className =
        "main-move " +
        (market.positive ? "positive" : "negative");
    }

    function selectTicker(index) {
      const tickers = document.querySelectorAll(".ticker");

      tickers.forEach((ticker) => {
        ticker.classList.remove("selected");
      });

      tickers[index].classList.add("selected");
      displayMarket(markets[activeSector][index]);
    }

    function renderTickers(sector) {
      activeSector = sector;
      tickerStrip.innerHTML = "";

      markets[sector].forEach((market, index) => {
        const ticker = document.createElement("button");

        ticker.className =
          "ticker" + (index === 0 ? " selected" : "");

        ticker.style.background = "transparent";
        ticker.style.color = "inherit";
        ticker.style.borderTop = "0";
        ticker.style.borderBottom = "0";

        ticker.innerHTML = `
          <div class="ticker-line">
            <span class="ticker-symbol">${market.symbol}</span>
            <strong class="ticker-price">${market.price}</strong>
          </div>

          <div class="ticker-line">
            <span class="ticker-unit">${market.unit}</span>

            <span
              class="ticker-move ${
                market.positive ? "positive" : "negative"
              }"
            >
              ${market.move}
            </span>
          </div>
        `;

        ticker.addEventListener("click", () => {
          selectTicker(index);
        });

        tickerStrip.appendChild(ticker);
      });

      displayMarket(markets[sector][0]);
    }

    document
      .querySelectorAll(".sector-button")
      .forEach((button) => {
        button.addEventListener("click", () => {
          document
            .querySelectorAll(".sector-button")
            .forEach((item) => {
              item.classList.remove("active");
            });

          button.classList.add("active");
          renderTickers(button.dataset.sector);
        });
      });

    document
      .querySelectorAll(".period-button")
      .forEach((button) => {
        button.addEventListener("click", () => {
          document
            .querySelectorAll(".period-button")
            .forEach((item) => {
              item.classList.remove("active");
            });

          button.classList.add("active");
        });
      });

    document
      .querySelectorAll(".tab")
      .forEach((button) => {
        button.addEventListener("click", () => {
          document
            .querySelectorAll(".tab")
            .forEach((tab) => {
              tab.classList.remove("active");
            });

          document
            .querySelectorAll(".tab-content")
            .forEach((content) => {
              content.classList.remove("active");
            });

          button.classList.add("active");

          document
            .querySelector("#" + button.dataset.tab)
            .classList.add("active");
        });
      });

    document
      .querySelector("#expand-chart")
      .addEventListener("click", () => {
        document.body.classList.toggle("chart-expanded");
      });

    document
      .querySelector("#alert-button")
      .addEventListener("click", () => {
        const toast = document.querySelector("#toast");

        toast.classList.add("visible");

        setTimeout(() => {
          toast.classList.remove("visible");
        }, 2200);
      });

    function updateClock() {
      const time = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Paris",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false
      }).format(new Date());

      document.querySelector("#clock").textContent =
        time + " CET";
    }

    setInterval(updateClock, 1000);

    updateClock();
    renderTickers("energy");
  </script>
</body>
</html>
