# Commodity Cockpit

Tableau de bord personnel des matières premières. Dans l'onglet **Code**, ouvrir [`index.html`](index.html), cliquer sur **Raw** ou **Download raw file**, enregistrer le fichier en `.html`, puis l'ouvrir dans un navigateur. Le code HTML complet figure aussi ci-dessous.

Les chiffres officiels sont collectés par [la tâche planifiée](.github/workflows/update-data.yml), puis intégrés à `index.html`. Chaque chiffre indique sa source, sa période et son unité. Brent, WTI et Henry Hub sont des cours spot EIA quotidiens, publiés avec retard ; ce ne sont pas des futures temps réel. Les liens TTF, PEG et JKM ne sont pas des cotations copiées. L'onglet **Power FR** affiche les mesures électriques RTE et, avec une clé ENTSO-E, des prévisions de demande France et DE-LU.

## Sources & automatisation

- EIA WPSR : stocks de brut, Cushing, Gulf Coast, essence, distillats, jet et SPR ; production, importations, exportations et brut traité par les raffineries US.
- EIA WNGSR : stockage de gaz US et régions, variation hebdomadaire et écart à la moyenne cinq ans.
- USDA WASDE : production, exportations prévues et stocks de maïs et soja US ; stocks mondiaux de maïs et blé, commerce mondial prévu du blé. Les révisions comparent les deux colonnes de prévision du même rapport.
- EIA Today in Energy : titres et résumés d'analyses récentes.
- Sodir (Norwegian Offshore Directorate) : chiffre mensuel provisoire d'août 2026 (pétrole, LGN et condensats), repère européen daté ; la source refuse actuellement les lectures automatisées du robot GitHub et ce chiffre n'est donc pas rafraîchi automatiquement.
- EIA, tableaux de prix spot quotidiens : Brent Europe, WTI Cushing et Henry Hub ; le collecteur vérifie la correspondance des six dates et six colonnes avant publication.
- GIE AGSI+ / ALSI : avec une clé API gratuite (accès aux **deux plateformes**), stockage gaz France/UE, soutirage net, stocks en cuves GNL et émissions des terminaux GNL France/UE. Ce sont des observations physiques quotidiennes, **pas des prix TTF, PEG ou JKM**. Créer la clé sur https://agsi.gie.eu/account, choisir accès AGSI + ALSI et enregistrer `GIE_API_KEY` dans Settings → Secrets and variables → Actions → New repository secret. Relancer le workflow depuis Actions. Sans clé, ces chiffres ne sont pas affichés.
- RTE éCO2mix national temps réel : [dataset officiel](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/) actualisé à la source au quart d'heure ; consommation, nucléaire, gaz, vent, solaire, hydraulique, bioénergies et échanges physiques. Export = solde négatif ; import = positif. Le cockpit collecte un instantané toutes les deux heures via GitHub Actions et indique l'heure de la mesure et de la collecte. Demande résiduelle = consommation − éolien − solaire (calcul indicatif, **pas une prévision du prix**). Aucun compte requis.
- ENTSO-E : prévision *day-ahead* de demande (A65/A01, Article 6.1.b, données [CC BY 4.0](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions)), France et Allemagne/Luxembourg ; affichage du pic prévu pour les prochaines 24 heures. Pour activer : créer un compte sur https://transparency.entsoe.eu/, demander l'accès API à `transparency@entsoe.eu` (objet `RESTful API access` et adresse enregistrée dans le corps), puis générer le jeton dans « My Account ». Enregistrer le jeton **uniquement** comme secret GitHub Actions `ENTSOE_API_TOKEN` via Settings → Secrets and variables → Actions → New repository secret ; relancer l'action. Ne jamais le coller dans le HTML, un fichier GitHub ou une conversation. Sans clé, RTE Power fonctionne déjà.
- Prix électriques France/DE : bouton vers le [marché officiel RTE](https://www.rte-france.com/en/data-publications/eco2mix/market-data) ; les prix day-ahead EPEX ne sont pas couverts par la [liste ENTSO-E de réutilisation libre](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions) et RTE interdit la copie de ses prix via éCO2mix. Le jeton ENTSO-E n'est pas un droit de redistribution de ces cotations.
- Calendrier natif : sorties EIA pétrole et gaz, USDA WASDE et STEO ; les exceptions 2026 connues sont incluses. Au-delà des dates vérifiées, le tableau l'indique sans inventer d'horaire.
- Marchés : graphique et tableau de cotations indicatives TradingView/OANDA (Brent, WTI, gaz US, cuivre et or). Ce sont des instruments OTC indicatifs ; ils ne remplacent ni les futures ICE/NYMEX ni le spot EIA daté. Les widgets nécessitent Internet et le fournisseur peut limiter la diffusion. Aluminium, cacao et café sont accessibles via leurs pages de marché ; leurs prix ne sont pas intégrés sans droits vérifiés.
- TTF/PEG/JKM : liens vers sources de marché ; un flux de cotations automatisé et redistribué publiquement nécessite un droit de diffusion. Aucune valeur ou spread instantané n'est inventé. ENTSO-E fournit des prévisions électriques ouvertes, ENTSOG des flux physiques de gaz, et GIE les stocks/terminaux.
- Physique : courbes de 14 jours de remplissage AGSI France et d'émission ALSI France, 26 semaines de stocks de brut EIA ; les signaux de pression sont des scénarios conditionnels liés aux chiffres publiés, jamais un mouvement de prix constaté.
- LME : [rapports de stocks](https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports) à consulter, sans chiffre de stock automatisé tant qu'un flux stable n'est pas vérifié.

Unités : M bbl = millions de barils ; M bbl/j = millions de barils par jour ; Bcf = milliards de pieds cubes ; TWh = térawattheures ; GWh/j = gigawattheures par jour ; 10³ m³ GNL = milliers de mètres cubes de GNL liquide ; M bu = millions de boisseaux ; Mt = millions de tonnes. Stocks, prix et flux ne sont jamais additionnés.

Les clés restent dans les secrets GitHub et ne sont jamais insérées dans les fichiers publics. Le fichier HTML contient un instantané et s'ouvre directement après téléchargement. Un téléchargement isolé ne reçoit pas les nouvelles données : récupérer la dernière version depuis GitHub. Les tâches GitHub planifiées peuvent être retardées ou désactivées après une longue période sans activité ; dans ce cas, l'onglet Actions permet la relance manuelle.

## Code complet

```html
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Commodity Cockpit — Marchés, physique & power</title>
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
    .ticker { display: flex; gap: 8px; align-items: center; min-height: 65px; overflow-x: auto; padding: 8px 14px; border-bottom: 1px solid var(--border); scrollbar-width: thin; }
    .ticker a { flex: 0 0 auto; border: 1px solid var(--border); border-radius: 7px; min-width: 145px; padding: 5px 10px; color: var(--text); }
    .ticker b { display: block; font-size: 13px; }
    .ticker small { color: var(--muted); font-size: 10px; }
    .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; min-height: 0; }
    .bar { min-height: 46px; padding: 8px 13px; display: flex; align-items: center; justify-content: space-between; gap: 12px; border-bottom: 1px solid var(--border); }
    .bar h2 { margin: 0; font-size: 13px; }
    .bar small { font-size: 10px; color: var(--muted); }
    .widget, .tradingview-widget-container, .tradingview-widget-container__widget { width: 100%; height: 100%; min-height: 0; }
    .market-grid { height: min(850px, calc(100vh - 175px)); min-height: 690px; padding: 12px; display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(365px, .9fr); gap: 12px; }
    .market-grid { height: auto; min-height: 850px; grid-template-columns: minmax(0, 1.45fr) minmax(380px, 1fr); }
    .chart { min-height: 850px; }
    .chart .widget { min-height: 715px; }
    .chart-picks { display:flex; flex-wrap:wrap; gap:5px; padding:8px 12px; border-bottom:1px solid var(--border); }
    .chart-picks button { border:1px solid var(--border); color:var(--muted); background:var(--surface-2); padding:5px 9px; border-radius:6px; }
    .chart-picks button.active { color:var(--accent); border-color:var(--accent); }
    .quote-widget { height:260px; flex:none; overflow:hidden; border-bottom:1px solid var(--border); }
    .price-links { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; padding:0 12px 14px; }
    .price-link { padding:12px; background:var(--surface-2); border:1px solid var(--border); border-radius:7px; }
    .price-link strong,.price-link small { display:block; }
    .price-link strong { font-size:13px; margin-bottom:3px; }
    .price-link small { font-size:10px; color:var(--muted); }
    .price-link p { margin:6px 0 0; font-size:11px; }
    .signal-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin:0 0 14px; }
    .signal { padding:14px; border-left:3px solid var(--accent); }
    .signal.down { border-left-color:var(--red); }
    .signal.flat { border-left-color:var(--warm); }
    .signal strong { display:block; font-size:14px; margin:4px 0; }
    .signal small,.signal p { color:var(--muted); font-size:11px; }
    .signal p { margin:8px 0 0; }
    .gauge { height:9px; border-radius:20px; background:#294039; overflow:hidden; margin:12px 0 4px; }
    .gauge i { display:block; height:100%; background:var(--accent); border-radius:20px; }
    .chart-duo { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; margin-top:12px; }
    .chart-duo .trend { margin:0; }
    .chart-duo h3 { font-size:12px; }
    .chart, .watch, .calendar { display: flex; flex-direction: column; }
    .right { min-height: 0; display: grid; grid-template-rows: minmax(280px, 300px) minmax(535px, 1fr); gap: 12px; }
    .right .calendar { grid-row:1; }
    .right .watch { grid-row:2; }
    .chart .widget, .watch .widget, .calendar .widget { flex: 1; }
    .caption { padding: 8px 12px; border-top: 1px solid var(--border); color: var(--muted); font-size: 10px; }
    .market-snapshot, .release-list { border-top: 1px solid var(--border); padding: 8px 12px; flex: none; }
    .market-snapshot { min-height: 80px; }
    .market-snapshot h3, .release-list h3 { font-size: 10px; color: var(--muted); margin: 0 0 5px; font-weight: 600; }
    .market-snapshot .row, .release-list .row { display: flex; justify-content: space-between; gap: 8px; padding: 2px 0; font-size: 10px; }
    .market-snapshot .row b, .release-list .row b { font-weight: 600; color: var(--text); white-space: nowrap; }
    .market-snapshot .row small { color: var(--muted); }
    .release-list .row a { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .watch-list, .agenda { min-height: 0; overflow-y: auto; }
    .watch-group { padding: 7px 12px 3px; color: var(--muted); font-size: 10px; letter-spacing: .07em; }
    .quote-row { padding: 7px 12px; display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 3px 12px; align-items: center; border-top: 1px solid var(--border); }
    .quote-row strong { display: block; font-size: 11px; }
    .quote-row small { color: var(--muted); font-size: 10px; }
    .quote-value { text-align: right; font-weight: 700; white-space: nowrap; }
    .quote-value a { font-weight: 500; font-size: 10px; }
    .quote-row .quote-note { grid-column: 1 / -1; color: var(--muted); font-size: 10px; }
    .agenda-row { padding: 9px 12px; display: grid; grid-template-columns: 67px minmax(0, 1fr); gap: 9px; border-top: 1px solid var(--border); }
    .agenda-when { color: var(--warm); font-size: 11px; font-weight: 700; }
    .agenda-when small { display: block; color: var(--muted); font-weight: 400; }
    .agenda-row a { display: block; color: var(--text); font-size: 11px; font-weight: 600; }
    .agenda-row p { margin: 2px 0 0; color: var(--muted); font-size: 10px; }
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
    .power-head { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
    .power-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin:12px 0; }
    .power-card { min-height:123px; padding:14px; }
    .power-card small { color:var(--muted); }
    .power-card strong { display:block; font-size:24px; margin:10px 0 3px; line-height:1.1; }
    .power-card span { font-size:10px; color:var(--warm); }
    .power-layout { display:grid; grid-template-columns:minmax(0,1.35fr) minmax(300px,.8fr); gap:12px; }
    .power-layout .card { padding:15px; }
    .power-layout h2, .power-bottom h2 { font-size:13px; margin:0 0 5px; }
    .power-layout p, .power-bottom p { color:var(--muted); font-size:11px; margin:3px 0 12px; }
    .power-chart { height:225px; width:100%; display:block; overflow:visible; }
    .power-chart polyline { fill:none; stroke-width:2; vector-effect:non-scaling-stroke; }
    .power-chart .demand-line { stroke:var(--accent); }
    .power-chart .residual-line { stroke:var(--warm); }
    .power-chart line { stroke:var(--border); vector-effect:non-scaling-stroke; }
    .power-legend { display:flex; justify-content:space-between; color:var(--muted); font-size:10px; gap:10px; }
    .power-legend b { color:var(--text); }
    .power-mix-row { display:grid; grid-template-columns:90px 1fr 75px; align-items:center; gap:10px; margin:11px 0; font-size:11px; }
    .power-mix-row .track { height:8px; background:var(--surface-2); border-radius:9px; overflow:hidden; }
    .power-mix-row i { display:block; height:100%; border-radius:9px; }
    .power-mix-row strong { text-align:right; }
    .power-bottom { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; margin-top:12px; }
    .power-bottom .card { padding:15px; }
    .power-forecast { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; margin:12px 0; }
    .power-forecast div { background:var(--surface-2); border:1px solid var(--border); border-radius:6px; padding:10px; }
    .power-forecast small, .power-forecast span { display:block; color:var(--muted); font-size:10px; }
    .power-forecast strong { display:block; font-size:18px; margin:3px 0; }
    .empty { padding: 20px; color: var(--muted); }
    .footer { max-width: 1460px; margin: auto; padding: 10px 18px 24px; font-size: 10px; color: var(--muted); }
    @media (max-width: 1050px) {
      .market-grid { height: auto; grid-template-columns: 1fr; }
      .chart { height: 575px; }
      .right { grid-template-columns: 1fr 1fr; grid-template-rows: 560px; }
      .right .calendar,.right .watch { grid-row:auto; }
      .chart .widget { min-height:0; }
      .physical-layout { grid-template-columns: 1fr; }
      .physical-side { grid-template-columns: 1fr 1fr; }
      .power-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .power-layout { grid-template-columns:1fr; }
      .chart { min-height:0; }
      .chart-duo { grid-template-columns:1fr; }
    }
    @media (max-width: 680px) {
      .header { padding: 9px; flex-wrap: wrap; }
      .brand span { display: none; }
      .market-grid { display: block; padding: 8px; }
      .chart { height: 490px; margin-bottom: 9px; }
      .right { display: flex; flex-direction:column; }
      .calendar { order:-1; }
      .watch { height: 530px; margin-bottom: 9px; }
      .calendar { height: 390px; }
      .market-context { padding: 0 8px 15px; }
      .mini-grid, .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .workspace { padding: 12px 9px; }
      .page-intro { display: block; }
      .stamp { display: inline-block; margin-top: 10px; }
      .physical-side { grid-template-columns: 1fr; }
      .power-grid, .power-bottom { grid-template-columns:1fr; }
      .power-forecast { grid-template-columns:1fr; }
      .price-links,.signal-grid { grid-template-columns:1fr; }
    }
  </style>
</head>
<body>
  <header class="header">
    <div class="brand"><strong>Commodity Cockpit</strong><span>Marchés · physique · électricité</span></div>
    <nav class="nav" aria-label="Navigation">
      <button type="button" data-page="markets" aria-selected="true">Marchés</button>
      <button type="button" data-page="physical" aria-selected="false">Physique</button>
      <button type="button" data-page="power" aria-selected="false">Power FR</button>
    </nav>
  </header>

  <section class="page" id="markets">
    <div class="ticker" id="ticker" aria-label="Derniers cours spot officiels datés"></div>
    <main class="market-grid">
      <section class="card chart">
        <div class="bar"><h2 id="market-chart-title">Brent · indicatif OANDA</h2><a id="market-chart-link" href="https://www.tradingview.com/symbols/BCOUSD/?exchange=OANDA" target="_blank" rel="noopener noreferrer">Ouvrir ↗</a></div>
        <div class="chart-picks" id="chart-picks" aria-label="Choisir le graphique"></div>
        <div class="widget" id="market-chart"><p class="empty">Chargement de TradingView…</p></div>
        <div class="caption">Graphique tiers en séance : cotation indicative du fournisseur indiqué, avec disponibilité selon ses droits. Ce n’est ni le Brent ICE ni un prix d’exécution. Dernier spot officiel EIA daté dans le ruban.</div>
      </section>
      <aside class="right">
        <section class="card watch">
          <div class="bar"><h2>À surveiller · cotations en séance</h2><small>TradingView · accès tiers</small></div>
          <div class="quote-widget" id="market-quotes"><p class="empty">Chargement des cotations indicatives…</p></div>
          <div class="watch-list" id="watch-list"></div>
          <div class="caption">Cotations OANDA : prix indicatifs, fournisseur et horaire affichés dans TradingView. Contrats boursiers et cours officiels spot : détails ci-dessous.</div>
        </section>
        <section class="card calendar">
          <div class="bar"><h2>Prochaines publications · heure de Paris</h2><a href="https://www.eia.gov/petroleum/supply/weekly/schedule.php" target="_blank" rel="noopener noreferrer">Dates ↗</a></div>
          <div class="agenda" id="agenda"></div>
          <div class="release-list" id="release-list"><h3>Dernières publications vérifiées</h3></div>
        </section>
      </aside>
    </main>
    <section class="market-context"><h2>TTF, PEG, JKM · références de gaz et GNL</h2><div class="price-links" id="gas-prices"></div><h2>Le physique en chiffres · <a href="#physical" data-open="physical">explications ↗</a></h2><div class="mini-grid" id="mini-grid"></div></section>
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
      <h2 class="section-heading">À comprendre en 10 secondes · sens possible pour les prix</h2>
      <div class="signal-grid" id="signals"></div>
      <div class="physical-layout">
          <section><h2 class="section-heading" id="sector-heading">Pétrole · prix spot et stocks</h2><div class="chart-duo"><div class="card side-pad trend" id="trend" hidden><h3 id="trend-title">Stocks commerciaux de brut US · 26 semaines</h3><svg viewBox="0 0 400 110" preserveAspectRatio="none" role="img" aria-label="Évolution des stocks ou flux physiques"><polyline id="trend-line" points=""></polyline></svg><div class="axis"><span id="trend-start"></span><span id="trend-end"></span></div></div><div class="card side-pad trend" id="trend-two" hidden><h3 id="trend-two-title">Deuxième repère</h3><svg viewBox="0 0 400 110" preserveAspectRatio="none" role="img" aria-label="Historique du deuxième repère"><polyline id="trend-two-line" points=""></polyline></svg><div class="axis"><span id="trend-two-start"></span><span id="trend-two-end"></span></div></div></div><h2 class="section-heading" style="margin-top:16px">Dernières mesures officielles</h2><div class="metrics" id="metrics"></div></section>
        <aside class="physical-side">
          <section class="card side-pad" id="takeaways"><h3>Ce que disent les publications</h3><div id="takeaway-list"></div></section>
          <section class="card side-pad"><h3>Actualités qui éclairent le physique · EIA</h3><p>Production, stocks, raffinage et GNL. Les articles décrivent des faits publiés ; leur effet sur les prix reste à analyser.</p><div id="stories"></div></section>
          <section class="card side-pad"><h3>Ce que mesurent les données</h3><p>GIE AGSI+ : stocks de gaz France et UE. GIE ALSI : GNL dans les terminaux et émission en GWh/j. <a href="https://transparency.entsog.eu/" target="_blank" rel="noopener noreferrer">ENTSOG ↗</a> donne les flux de réseau. Un stock et un débit ne se comparent pas directement. Les signaux montrent une pression possible toutes choses égales par ailleurs ; ils ne mesurent pas une variation instantanée du TTF, du PEG ou du JKM.</p></section>
        </aside>
      </div>
    </main>
  </section>

  <section class="page" id="power" hidden>
    <main class="workspace">
      <div class="page-intro"><div><h1>Power · France</h1><p>Demande, mix et échanges physiques RTE ; prévisions J-1 ENTSO-E avec clé.</p></div><span class="stamp" id="power-updated">Instantané en attente</span></div>
      <div class="power-head"><span class="badge" id="power-rte-status">RTE : collecte en attente</span><span class="badge" id="power-entsoe-status">ENTSO-E : clé en attente</span><span class="badge">Observations ≠ prix de marché</span></div>
      <div class="power-grid" id="power-grid"></div>
      <div class="power-layout">
        <section class="card"><h2>Demande et demande résiduelle · 24 h</h2><p>Résiduelle indicative = consommation − production éolienne − solaire ; un indicateur de tension physique, pas une prévision de prix.</p><div id="power-curve" class="empty">Collecte RTE en attente.</div><div class="power-legend" id="power-axis"></div></section>
        <section class="card"><h2>Production française · dernière observation</h2><p>Puissance par filière, en MW. Les parts portent sur la production affichée, pas sur la consommation.</p><div id="power-mix" class="empty">Collecte RTE en attente.</div><small id="power-mix-time" class="detail"></small></section>
      </div>
      <div class="power-bottom">
        <section class="card"><h2>Pour surveiller le gaz et les échanges</h2><p id="power-readout">Le gaz électrique, l'éolien, le solaire et le solde d'import/export seront affichés après la première collecte RTE.</p><p>Un solde RTE négatif signifie une exportation nette ; positif, une importation nette. Les données sont des télémesures complétées d'estimations.</p><a href="https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/" target="_blank" rel="noopener noreferrer">Source RTE éCO2mix ↗</a></section>
        <section class="card"><h2>Demande anticipée · France et DE-LU</h2><p>Point haut prévu dans les prochaines 24 h, prévision day-ahead ENTSO-E sous licence CC BY 4.0. Chaque marché a sa taille : comparer la trajectoire, pas les niveaux bruts.</p><div class="power-forecast" id="power-forecast"></div><p id="power-forecast-note"></p><a href="https://transparency.entsoe.eu/" target="_blank" rel="noopener noreferrer">Transparence ENTSO-E ↗</a></section>
        <section class="card"><h2>Prix power France / Allemagne</h2><p>Pour le spot day-ahead et son écart, consulter la vue officielle EPEX/RTE. Les prix de bourse ne figurent pas dans la liste ENTSO-E des séries librement redistribuables ; la clé API ne change pas ces droits.</p><a href="https://www.rte-france.com/en/data-publications/eco2mix/market-data" target="_blank" rel="noopener noreferrer">Voir les prix spot RTE ↗</a></section>
        <section class="card"><h2>Sources, délais et accès</h2><p>RTE actualise sa source au quart d'heure ; cette page reflète la dernière exécution planifiée puis doit être retéléchargée sur GitHub. Heure des mesures et heure de collecte sont affichées séparément.</p><p>La clé ENTSO-E reste dans le secret <code>ENTSOE_API_TOKEN</code> du dépôt. Le flux GIE du gaz utilise séparément <code>GIE_API_KEY</code>.</p></section>
      </div>
    </main>
  </section>

  <p class="footer">Sources : EIA (spot publié et stocks), GIE AGSI/ALSI, USDA, USGS, RTE, ENTSO-E. Cotations indicatives tierces : TradingView/OANDA ; droits et délais du fournisseur. TTF, PEG et JKM : accès officiel aux cotations sans prix reproduit faute de flux redistribuable. Une source inaccessible conserve sa dernière valeur datée et est signalée.</p>

  <!-- Replaced by scripts/update_data.py; retained inside HTML for one-file opening. -->
  <script id="snapshot-data" type="application/json">
{
  "calendar": [
    {
      "at": "2026-09-30T14:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-10-01T14:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-10-06T04:00:00+00:00",
      "context": "Date vérifiée ; horaire officiel non précisé",
      "day_only": true,
      "title": "EIA · perspectives énergétiques STEO",
      "url": "https://www.eia.gov/outlooks/steo/release_schedule.php"
    },
    {
      "at": "2026-10-07T14:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-10-08T14:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-10-09T16:00:00+00:00",
      "context": "Bilans mondiaux céréales et oléagineux",
      "day_only": false,
      "title": "USDA · WASDE",
      "url": "https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report"
    },
    {
      "at": "2026-10-15T14:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-10-15T16:00:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-10-21T14:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-10-22T14:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-10-28T14:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-10-29T14:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-11-04T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-11-05T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-11-10T17:00:00+00:00",
      "context": "Bilans mondiaux céréales et oléagineux",
      "day_only": false,
      "title": "USDA · WASDE",
      "url": "https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report"
    },
    {
      "at": "2026-11-12T17:00:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-11-13T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-11-18T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-11-19T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-11-25T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-11-25T17:00:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-12-02T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-12-03T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-12-09T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-12-10T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-12-10T17:00:00+00:00",
      "context": "Bilans mondiaux céréales et oléagineux",
      "day_only": false,
      "title": "USDA · WASDE",
      "url": "https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report"
    },
    {
      "at": "2026-12-16T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-12-17T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-12-23T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-12-24T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    },
    {
      "at": "2026-12-30T15:30:00+00:00",
      "context": "Brut, essence, distillats et raffineries US",
      "day_only": false,
      "title": "EIA · stocks pétroliers WPSR",
      "url": "https://www.eia.gov/petroleum/supply/weekly/schedule.php"
    },
    {
      "at": "2026-12-31T15:30:00+00:00",
      "context": "Variation et écart à la moyenne cinq ans",
      "day_only": false,
      "title": "EIA · stockage gaz US",
      "url": "https://ir.eia.gov/ngs/schedule.html"
    }
  ],
  "generated_at": "2026-09-26T04:58:49+00:00",
  "history": {
    "gas_eu": [
      {
        "date": "2026-09-11",
        "value": 67.78
      },
      {
        "date": "2026-09-12",
        "value": 68.04
      },
      {
        "date": "2026-09-13",
        "value": 68.3
      },
      {
        "date": "2026-09-14",
        "value": 68.49
      },
      {
        "date": "2026-09-15",
        "value": 68.66
      },
      {
        "date": "2026-09-16",
        "value": 68.84
      },
      {
        "date": "2026-09-17",
        "value": 69.06
      },
      {
        "date": "2026-09-18",
        "value": 69.31
      },
      {
        "date": "2026-09-19",
        "value": 69.62
      },
      {
        "date": "2026-09-20",
        "value": 69.94
      },
      {
        "date": "2026-09-21",
        "value": 70.14
      },
      {
        "date": "2026-09-22",
        "value": 70.24
      },
      {
        "date": "2026-09-23",
        "value": 70.35
      },
      {
        "date": "2026-09-24",
        "value": 70.45
      }
    ],
    "gas_fr": [
      {
        "date": "2026-09-11",
        "value": 75.77
      },
      {
        "date": "2026-09-12",
        "value": 76.27
      },
      {
        "date": "2026-09-13",
        "value": 76.74
      },
      {
        "date": "2026-09-14",
        "value": 77.16
      },
      {
        "date": "2026-09-15",
        "value": 77.53
      },
      {
        "date": "2026-09-16",
        "value": 78.01
      },
      {
        "date": "2026-09-17",
        "value": 78.52
      },
      {
        "date": "2026-09-18",
        "value": 79.1
      },
      {
        "date": "2026-09-19",
        "value": 79.69
      },
      {
        "date": "2026-09-20",
        "value": 80.31
      },
      {
        "date": "2026-09-21",
        "value": 80.82
      },
      {
        "date": "2026-09-22",
        "value": 81.09
      },
      {
        "date": "2026-09-23",
        "value": 81.43
      },
      {
        "date": "2026-09-24",
        "value": 81.61
      }
    ],
    "lng_eu_sendout": [
      {
        "date": "2026-09-11",
        "value": 3126.7
      },
      {
        "date": "2026-09-12",
        "value": 3097.6
      },
      {
        "date": "2026-09-13",
        "value": 3215.2
      },
      {
        "date": "2026-09-14",
        "value": 3677.8
      },
      {
        "date": "2026-09-15",
        "value": 3322.6
      },
      {
        "date": "2026-09-16",
        "value": 3279.0
      },
      {
        "date": "2026-09-17",
        "value": 3661.0
      },
      {
        "date": "2026-09-18",
        "value": 3873.1
      },
      {
        "date": "2026-09-19",
        "value": 3778.9
      },
      {
        "date": "2026-09-20",
        "value": 3816.7
      },
      {
        "date": "2026-09-21",
        "value": 4235.5
      },
      {
        "date": "2026-09-22",
        "value": 3892.5
      },
      {
        "date": "2026-09-23",
        "value": 3932.2
      },
      {
        "date": "2026-09-24",
        "value": 3889.8
      }
    ],
    "lng_fr_sendout": [
      {
        "date": "2026-09-11",
        "value": 726.1
      },
      {
        "date": "2026-09-12",
        "value": 756.9
      },
      {
        "date": "2026-09-13",
        "value": 776.7
      },
      {
        "date": "2026-09-14",
        "value": 857.8
      },
      {
        "date": "2026-09-15",
        "value": 354.4
      },
      {
        "date": "2026-09-16",
        "value": 687.1
      },
      {
        "date": "2026-09-17",
        "value": 920.0
      },
      {
        "date": "2026-09-18",
        "value": 1052.8
      },
      {
        "date": "2026-09-19",
        "value": 1074.4
      },
      {
        "date": "2026-09-20",
        "value": 1075.6
      },
      {
        "date": "2026-09-21",
        "value": 1085.1
      },
      {
        "date": "2026-09-22",
        "value": 800.4
      },
      {
        "date": "2026-09-23",
        "value": 881.8
      },
      {
        "date": "2026-09-24",
        "value": 847.8
      }
    ],
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
    ],
    "power_fr": [
      {
        "at": "2026-09-25T04:45:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -10223,
        "eolien": 3142,
        "fioul": 37,
        "gaz": 3360,
        "hydraulique": 4540,
        "load": 40844,
        "nucleaire": 38994,
        "pompage": -1,
        "prevision_j": 41550,
        "prevision_j1": 41550,
        "solaire": 0,
        "taux_co2": 38
      },
      {
        "at": "2026-09-25T05:00:00+00:00",
        "bioenergies": 1004,
        "charbon": 0,
        "ech_physiques": -9525,
        "eolien": 3117,
        "fioul": 37,
        "gaz": 3369,
        "hydraulique": 4989,
        "load": 42190,
        "nucleaire": 38990,
        "pompage": 0,
        "prevision_j": 42600,
        "prevision_j1": 42600,
        "solaire": 182,
        "taux_co2": 38
      },
      {
        "at": "2026-09-25T05:15:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": -9480,
        "eolien": 3219,
        "fioul": 37,
        "gaz": 3377,
        "hydraulique": 5725,
        "load": 43463,
        "nucleaire": 39170,
        "pompage": -1,
        "prevision_j": 43450,
        "prevision_j1": 43450,
        "solaire": 184,
        "taux_co2": 37
      },
      {
        "at": "2026-09-25T05:30:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -9532,
        "eolien": 3247,
        "fioul": 37,
        "gaz": 3370,
        "hydraulique": 6095,
        "load": 43902,
        "nucleaire": 39171,
        "pompage": -17,
        "prevision_j": 44300,
        "prevision_j1": 44300,
        "solaire": 188,
        "taux_co2": 37
      },
      {
        "at": "2026-09-25T05:45:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -10068,
        "eolien": 3310,
        "fioul": 37,
        "gaz": 3375,
        "hydraulique": 6806,
        "load": 44279,
        "nucleaire": 39191,
        "pompage": -27,
        "prevision_j": 44750,
        "prevision_j1": 44950,
        "solaire": 236,
        "taux_co2": 37
      },
      {
        "at": "2026-09-25T06:00:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -10427,
        "eolien": 3499,
        "fioul": 37,
        "gaz": 3376,
        "hydraulique": 7151,
        "load": 44677,
        "nucleaire": 39175,
        "pompage": -34,
        "prevision_j": 45200,
        "prevision_j1": 45600,
        "solaire": 481,
        "taux_co2": 36
      },
      {
        "at": "2026-09-25T06:15:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -9692,
        "eolien": 3522,
        "fioul": 37,
        "gaz": 3377,
        "hydraulique": 7192,
        "load": 45508,
        "nucleaire": 38728,
        "pompage": -38,
        "prevision_j": 45450,
        "prevision_j1": 46050,
        "solaire": 986,
        "taux_co2": 36
      },
      {
        "at": "2026-09-25T06:30:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -9565,
        "eolien": 3451,
        "fioul": 37,
        "gaz": 3502,
        "hydraulique": 6880,
        "load": 45547,
        "nucleaire": 38237,
        "pompage": -41,
        "prevision_j": 45700,
        "prevision_j1": 46500,
        "solaire": 1649,
        "taux_co2": 37
      },
      {
        "at": "2026-09-25T06:45:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -9449,
        "eolien": 3368,
        "fioul": 36,
        "gaz": 3399,
        "hydraulique": 6449,
        "load": 45702,
        "nucleaire": 38110,
        "pompage": -47,
        "prevision_j": 45900,
        "prevision_j1": 46850,
        "solaire": 2687,
        "taux_co2": 36
      },
      {
        "at": "2026-09-25T07:00:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -9145,
        "eolien": 3182,
        "fioul": 37,
        "gaz": 2848,
        "hydraulique": 6105,
        "load": 45772,
        "nucleaire": 38163,
        "pompage": -205,
        "prevision_j": 46100,
        "prevision_j1": 47200,
        "solaire": 3711,
        "taux_co2": 32
      },
      {
        "at": "2026-09-25T07:15:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": -9693,
        "eolien": 2936,
        "fioul": 37,
        "gaz": 2691,
        "hydraulique": 5843,
        "load": 46046,
        "nucleaire": 38104,
        "pompage": -17,
        "prevision_j": 46300,
        "prevision_j1": 47300,
        "solaire": 5128,
        "taux_co2": 30
      },
      {
        "at": "2026-09-25T07:30:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -8980,
        "eolien": 2637,
        "fioul": 36,
        "gaz": 2432,
        "hydraulique": 4603,
        "load": 46234,
        "nucleaire": 38094,
        "pompage": -160,
        "prevision_j": 46500,
        "prevision_j1": 47400,
        "solaire": 6556,
        "taux_co2": 28
      },
      {
        "at": "2026-09-25T07:45:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -8541,
        "eolien": 2345,
        "fioul": 37,
        "gaz": 1361,
        "hydraulique": 4052,
        "load": 46235,
        "nucleaire": 38047,
        "pompage": -161,
        "prevision_j": 46600,
        "prevision_j1": 47400,
        "solaire": 8074,
        "taux_co2": 20
      },
      {
        "at": "2026-09-25T08:00:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -7826,
        "eolien": 2053,
        "fioul": 37,
        "gaz": 997,
        "hydraulique": 3481,
        "load": 46607,
        "nucleaire": 37589,
        "pompage": -206,
        "prevision_j": 46700,
        "prevision_j1": 47400,
        "solaire": 9490,
        "taux_co2": 17
      },
      {
        "at": "2026-09-25T08:15:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -8182,
        "eolien": 1766,
        "fioul": 37,
        "gaz": 812,
        "hydraulique": 3267,
        "load": 46895,
        "nucleaire": 37339,
        "pompage": -224,
        "prevision_j": 47050,
        "prevision_j1": 47650,
        "solaire": 11090,
        "taux_co2": 16
      },
      {
        "at": "2026-09-25T08:30:00+00:00",
        "bioenergies": 999,
        "charbon": 0,
        "ech_physiques": -8304,
        "eolien": 1588,
        "fioul": 37,
        "gaz": 684,
        "hydraulique": 3205,
        "load": 46888,
        "nucleaire": 37368,
        "pompage": -973,
        "prevision_j": 47400,
        "prevision_j1": 47900,
        "solaire": 12333,
        "taux_co2": 15
      },
      {
        "at": "2026-09-25T08:45:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -8012,
        "eolien": 1466,
        "fioul": 37,
        "gaz": 539,
        "hydraulique": 2809,
        "load": 47507,
        "nucleaire": 37250,
        "pompage": -1312,
        "prevision_j": 47450,
        "prevision_j1": 47850,
        "solaire": 13840,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T09:00:00+00:00",
        "bioenergies": 989,
        "charbon": 0,
        "ech_physiques": -8645,
        "eolien": 1338,
        "fioul": 37,
        "gaz": 550,
        "hydraulique": 2688,
        "load": 47604,
        "nucleaire": 37337,
        "pompage": -1481,
        "prevision_j": 47500,
        "prevision_j1": 47800,
        "solaire": 14909,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T09:15:00+00:00",
        "bioenergies": 989,
        "charbon": 0,
        "ech_physiques": -8705,
        "eolien": 1272,
        "fioul": 37,
        "gaz": 556,
        "hydraulique": 2659,
        "load": 48174,
        "nucleaire": 37174,
        "pompage": -1805,
        "prevision_j": 47850,
        "prevision_j1": 48050,
        "solaire": 16105,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T09:30:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -8940,
        "eolien": 1220,
        "fioul": 37,
        "gaz": 562,
        "hydraulique": 2421,
        "load": 47963,
        "nucleaire": 36724,
        "pompage": -1803,
        "prevision_j": 48200,
        "prevision_j1": 48300,
        "solaire": 16815,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T09:45:00+00:00",
        "bioenergies": 988,
        "charbon": 0,
        "ech_physiques": -8545,
        "eolien": 1247,
        "fioul": 37,
        "gaz": 296,
        "hydraulique": 2430,
        "load": 48343,
        "nucleaire": 36080,
        "pompage": -1806,
        "prevision_j": 48650,
        "prevision_j1": 48650,
        "solaire": 17650,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T10:00:00+00:00",
        "bioenergies": 987,
        "charbon": 0,
        "ech_physiques": -8614,
        "eolien": 1268,
        "fioul": 37,
        "gaz": 297,
        "hydraulique": 2374,
        "load": 48759,
        "nucleaire": 35969,
        "pompage": -1803,
        "prevision_j": 49100,
        "prevision_j1": 49000,
        "solaire": 18318,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T10:15:00+00:00",
        "bioenergies": 988,
        "charbon": 0,
        "ech_physiques": -8792,
        "eolien": 1268,
        "fioul": 37,
        "gaz": 295,
        "hydraulique": 2310,
        "load": 48654,
        "nucleaire": 35958,
        "pompage": -2039,
        "prevision_j": 48900,
        "prevision_j1": 48800,
        "solaire": 18900,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T10:30:00+00:00",
        "bioenergies": 989,
        "charbon": 0,
        "ech_physiques": -8812,
        "eolien": 1303,
        "fioul": 37,
        "gaz": 290,
        "hydraulique": 2306,
        "load": 48993,
        "nucleaire": 35820,
        "pompage": -2040,
        "prevision_j": 48700,
        "prevision_j1": 48600,
        "solaire": 19364,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T10:45:00+00:00",
        "bioenergies": 990,
        "charbon": 0,
        "ech_physiques": -9136,
        "eolien": 1326,
        "fioul": 37,
        "gaz": 292,
        "hydraulique": 2298,
        "load": 48983,
        "nucleaire": 35948,
        "pompage": -2094,
        "prevision_j": 49100,
        "prevision_j1": 49000,
        "solaire": 19651,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T11:00:00+00:00",
        "bioenergies": 992,
        "charbon": 0,
        "ech_physiques": -9493,
        "eolien": 1367,
        "fioul": 37,
        "gaz": 290,
        "hydraulique": 2292,
        "load": 48743,
        "nucleaire": 35918,
        "pompage": -2101,
        "prevision_j": 49500,
        "prevision_j1": 49400,
        "solaire": 19777,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T11:15:00+00:00",
        "bioenergies": 989,
        "charbon": 0,
        "ech_physiques": -9157,
        "eolien": 1356,
        "fioul": 37,
        "gaz": 283,
        "hydraulique": 2321,
        "load": 48736,
        "nucleaire": 35442,
        "pompage": -2105,
        "prevision_j": 48700,
        "prevision_j1": 48600,
        "solaire": 19894,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T11:30:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -9529,
        "eolien": 1358,
        "fioul": 37,
        "gaz": 292,
        "hydraulique": 2337,
        "load": 46868,
        "nucleaire": 34136,
        "pompage": -2333,
        "prevision_j": 47900,
        "prevision_j1": 47800,
        "solaire": 19903,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T11:45:00+00:00",
        "bioenergies": 990,
        "charbon": 0,
        "ech_physiques": -9183,
        "eolien": 1330,
        "fioul": 37,
        "gaz": 288,
        "hydraulique": 2217,
        "load": 46770,
        "nucleaire": 33906,
        "pompage": -2330,
        "prevision_j": 47950,
        "prevision_j1": 47850,
        "solaire": 19928,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T12:00:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -8309,
        "eolien": 1324,
        "fioul": 37,
        "gaz": 286,
        "hydraulique": 2102,
        "load": 47253,
        "nucleaire": 33759,
        "pompage": -2332,
        "prevision_j": 48000,
        "prevision_j1": 47900,
        "solaire": 19797,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T12:15:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -8238,
        "eolien": 1350,
        "fioul": 37,
        "gaz": 292,
        "hydraulique": 2078,
        "load": 47751,
        "nucleaire": 34119,
        "pompage": -2118,
        "prevision_j": 48250,
        "prevision_j1": 48500,
        "solaire": 19539,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T12:30:00+00:00",
        "bioenergies": 987,
        "charbon": 0,
        "ech_physiques": -7871,
        "eolien": 1347,
        "fioul": 37,
        "gaz": 290,
        "hydraulique": 2052,
        "load": 47321,
        "nucleaire": 33908,
        "pompage": -2118,
        "prevision_j": 48500,
        "prevision_j1": 49100,
        "solaire": 18879,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T12:45:00+00:00",
        "bioenergies": 985,
        "charbon": 0,
        "ech_physiques": -8345,
        "eolien": 1421,
        "fioul": 37,
        "gaz": 323,
        "hydraulique": 2011,
        "load": 47278,
        "nucleaire": 34156,
        "pompage": -2204,
        "prevision_j": 48200,
        "prevision_j1": 48800,
        "solaire": 18953,
        "taux_co2": 11
      },
      {
        "at": "2026-09-25T13:00:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -8215,
        "eolien": 1558,
        "fioul": 156,
        "gaz": 341,
        "hydraulique": 1997,
        "load": 47788,
        "nucleaire": 34069,
        "pompage": -2209,
        "prevision_j": 47900,
        "prevision_j1": 48500,
        "solaire": 19161,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T13:15:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -8202,
        "eolien": 1618,
        "fioul": 154,
        "gaz": 376,
        "hydraulique": 1993,
        "load": 47675,
        "nucleaire": 34218,
        "pompage": -2204,
        "prevision_j": 47750,
        "prevision_j1": 48350,
        "solaire": 18728,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T13:30:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -8388,
        "eolien": 1643,
        "fioul": 154,
        "gaz": 389,
        "hydraulique": 1965,
        "load": 47078,
        "nucleaire": 34192,
        "pompage": -2205,
        "prevision_j": 47600,
        "prevision_j1": 48200,
        "solaire": 18350,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T13:45:00+00:00",
        "bioenergies": 986,
        "charbon": 0,
        "ech_physiques": -8511,
        "eolien": 1676,
        "fioul": 153,
        "gaz": 428,
        "hydraulique": 2059,
        "load": 46873,
        "nucleaire": 34660,
        "pompage": -2202,
        "prevision_j": 47250,
        "prevision_j1": 47850,
        "solaire": 17688,
        "taux_co2": 14
      },
      {
        "at": "2026-09-25T14:00:00+00:00",
        "bioenergies": 985,
        "charbon": 0,
        "ech_physiques": -8678,
        "eolien": 1823,
        "fioul": 36,
        "gaz": 601,
        "hydraulique": 2240,
        "load": 46801,
        "nucleaire": 34859,
        "pompage": -2202,
        "prevision_j": 46900,
        "prevision_j1": 47500,
        "solaire": 17152,
        "taux_co2": 13
      },
      {
        "at": "2026-09-25T14:15:00+00:00",
        "bioenergies": 985,
        "charbon": 0,
        "ech_physiques": -8736,
        "eolien": 1827,
        "fioul": 37,
        "gaz": 787,
        "hydraulique": 2353,
        "load": 46382,
        "nucleaire": 35025,
        "pompage": -2232,
        "prevision_j": 46300,
        "prevision_j1": 46900,
        "solaire": 16343,
        "taux_co2": 15
      },
      {
        "at": "2026-09-25T14:30:00+00:00",
        "bioenergies": 981,
        "charbon": 0,
        "ech_physiques": -8236,
        "eolien": 1894,
        "fioul": 37,
        "gaz": 869,
        "hydraulique": 2346,
        "load": 46248,
        "nucleaire": 35184,
        "pompage": -2231,
        "prevision_j": 45700,
        "prevision_j1": 46300,
        "solaire": 15396,
        "taux_co2": 16
      },
      {
        "at": "2026-09-25T14:45:00+00:00",
        "bioenergies": 986,
        "charbon": 0,
        "ech_physiques": -8714,
        "eolien": 1909,
        "fioul": 37,
        "gaz": 999,
        "hydraulique": 2576,
        "load": 46186,
        "nucleaire": 35765,
        "pompage": -1772,
        "prevision_j": 45600,
        "prevision_j1": 46200,
        "solaire": 14394,
        "taux_co2": 17
      },
      {
        "at": "2026-09-25T15:00:00+00:00",
        "bioenergies": 993,
        "charbon": 0,
        "ech_physiques": -8303,
        "eolien": 2093,
        "fioul": 37,
        "gaz": 1047,
        "hydraulique": 2526,
        "load": 46611,
        "nucleaire": 35769,
        "pompage": -620,
        "prevision_j": 45500,
        "prevision_j1": 46100,
        "solaire": 13066,
        "taux_co2": 17
      },
      {
        "at": "2026-09-25T15:15:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -9655,
        "eolien": 2262,
        "fioul": 37,
        "gaz": 1302,
        "hydraulique": 3384,
        "load": 46286,
        "nucleaire": 36094,
        "pompage": -1,
        "prevision_j": 46050,
        "prevision_j1": 46550,
        "solaire": 11767,
        "taux_co2": 19
      },
      {
        "at": "2026-09-25T15:30:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -9335,
        "eolien": 2370,
        "fioul": 34,
        "gaz": 1478,
        "hydraulique": 4267,
        "load": 46470,
        "nucleaire": 36194,
        "pompage": 0,
        "prevision_j": 46600,
        "prevision_j1": 47000,
        "solaire": 10447,
        "taux_co2": 21
      },
      {
        "at": "2026-09-25T15:45:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -9852,
        "eolien": 2464,
        "fioul": 380,
        "gaz": 2179,
        "hydraulique": 5213,
        "load": 46662,
        "nucleaire": 36175,
        "pompage": 0,
        "prevision_j": 46800,
        "prevision_j1": 47100,
        "solaire": 9092,
        "taux_co2": 30
      },
      {
        "at": "2026-09-25T16:00:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -10102,
        "eolien": 2543,
        "fioul": 765,
        "gaz": 2828,
        "hydraulique": 5978,
        "load": 46534,
        "nucleaire": 35947,
        "pompage": 0,
        "prevision_j": 47000,
        "prevision_j1": 47200,
        "solaire": 7569,
        "taux_co2": 41
      },
      {
        "at": "2026-09-25T16:15:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -10288,
        "eolien": 2586,
        "fioul": 702,
        "gaz": 3515,
        "hydraulique": 6736,
        "load": 46571,
        "nucleaire": 36244,
        "pompage": 0,
        "prevision_j": 47200,
        "prevision_j1": 47300,
        "solaire": 6073,
        "taux_co2": 45
      },
      {
        "at": "2026-09-25T16:30:00+00:00",
        "bioenergies": 999,
        "charbon": 0,
        "ech_physiques": -9401,
        "eolien": 2622,
        "fioul": 701,
        "gaz": 4206,
        "hydraulique": 7244,
        "load": 47159,
        "nucleaire": 36144,
        "pompage": 0,
        "prevision_j": 47400,
        "prevision_j1": 47400,
        "solaire": 4635,
        "taux_co2": 50
      },
      {
        "at": "2026-09-25T16:45:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -9462,
        "eolien": 2540,
        "fioul": 701,
        "gaz": 4367,
        "hydraulique": 8852,
        "load": 47715,
        "nucleaire": 36346,
        "pompage": 0,
        "prevision_j": 47800,
        "prevision_j1": 47850,
        "solaire": 3261,
        "taux_co2": 51
      },
      {
        "at": "2026-09-25T17:00:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -7829,
        "eolien": 2522,
        "fioul": 704,
        "gaz": 4423,
        "hydraulique": 8706,
        "load": 47794,
        "nucleaire": 36242,
        "pompage": 0,
        "prevision_j": 48200,
        "prevision_j1": 48300,
        "solaire": 2027,
        "taux_co2": 53
      },
      {
        "at": "2026-09-25T17:15:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -7631,
        "eolien": 2519,
        "fioul": 711,
        "gaz": 4474,
        "hydraulique": 8607,
        "load": 47322,
        "nucleaire": 36346,
        "pompage": 0,
        "prevision_j": 48100,
        "prevision_j1": 48200,
        "solaire": 1201,
        "taux_co2": 54
      },
      {
        "at": "2026-09-25T17:30:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -7051,
        "eolien": 2566,
        "fioul": 715,
        "gaz": 4482,
        "hydraulique": 8728,
        "load": 47537,
        "nucleaire": 36332,
        "pompage": 0,
        "prevision_j": 48000,
        "prevision_j1": 48100,
        "solaire": 670,
        "taux_co2": 55
      },
      {
        "at": "2026-09-25T17:45:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -6625,
        "eolien": 2582,
        "fioul": 718,
        "gaz": 4504,
        "hydraulique": 8522,
        "load": 47537,
        "nucleaire": 36374,
        "pompage": 0,
        "prevision_j": 47850,
        "prevision_j1": 47950,
        "solaire": 376,
        "taux_co2": 55
      },
      {
        "at": "2026-09-25T18:00:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -6842,
        "eolien": 2576,
        "fioul": 723,
        "gaz": 4543,
        "hydraulique": 8840,
        "load": 47548,
        "nucleaire": 36423,
        "pompage": -31,
        "prevision_j": 47700,
        "prevision_j1": 47800,
        "solaire": 223,
        "taux_co2": 55
      },
      {
        "at": "2026-09-25T18:15:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -6699,
        "eolien": 2641,
        "fioul": 726,
        "gaz": 4560,
        "hydraulique": 8511,
        "load": 47339,
        "nucleaire": 36041,
        "pompage": -33,
        "prevision_j": 47200,
        "prevision_j1": 47350,
        "solaire": 188,
        "taux_co2": 56
      },
      {
        "at": "2026-09-25T18:30:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -7307,
        "eolien": 2740,
        "fioul": 730,
        "gaz": 4580,
        "hydraulique": 8675,
        "load": 46562,
        "nucleaire": 35675,
        "pompage": -48,
        "prevision_j": 46700,
        "prevision_j1": 46900,
        "solaire": 190,
        "taux_co2": 56
      },
      {
        "at": "2026-09-25T18:45:00+00:00",
        "bioenergies": 993,
        "charbon": 0,
        "ech_physiques": -7684,
        "eolien": 2793,
        "fioul": 735,
        "gaz": 4592,
        "hydraulique": 8560,
        "load": 45955,
        "nucleaire": 35550,
        "pompage": -48,
        "prevision_j": 46200,
        "prevision_j1": 46400,
        "solaire": 188,
        "taux_co2": 57
      },
      {
        "at": "2026-09-25T19:00:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -8812,
        "eolien": 2987,
        "fioul": 735,
        "gaz": 4591,
        "hydraulique": 8570,
        "load": 45010,
        "nucleaire": 35463,
        "pompage": -50,
        "prevision_j": 45700,
        "prevision_j1": 45900,
        "solaire": 187,
        "taux_co2": 57
      },
      {
        "at": "2026-09-25T19:15:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -9235,
        "eolien": 3269,
        "fioul": 737,
        "gaz": 4604,
        "hydraulique": 7969,
        "load": 44094,
        "nucleaire": 35410,
        "pompage": -56,
        "prevision_j": 45100,
        "prevision_j1": 45300,
        "solaire": 0,
        "taux_co2": 57
      },
      {
        "at": "2026-09-25T19:30:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -9343,
        "eolien": 3467,
        "fioul": 739,
        "gaz": 4611,
        "hydraulique": 7502,
        "load": 43584,
        "nucleaire": 35418,
        "pompage": -4,
        "prevision_j": 44500,
        "prevision_j1": 44700,
        "solaire": 0,
        "taux_co2": 58
      },
      {
        "at": "2026-09-25T19:45:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -8992,
        "eolien": 3590,
        "fioul": 740,
        "gaz": 4553,
        "hydraulique": 6970,
        "load": 43206,
        "nucleaire": 35320,
        "pompage": 0,
        "prevision_j": 43850,
        "prevision_j1": 44050,
        "solaire": 0,
        "taux_co2": 58
      },
      {
        "at": "2026-09-25T20:00:00+00:00",
        "bioenergies": 1002,
        "charbon": 0,
        "ech_physiques": -9543,
        "eolien": 3787,
        "fioul": 739,
        "gaz": 4538,
        "hydraulique": 6860,
        "load": 42497,
        "nucleaire": 35245,
        "pompage": 0,
        "prevision_j": 43200,
        "prevision_j1": 43400,
        "solaire": 0,
        "taux_co2": 58
      },
      {
        "at": "2026-09-25T20:15:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": -8443,
        "eolien": 3741,
        "fioul": 702,
        "gaz": 4560,
        "hydraulique": 6580,
        "load": 42840,
        "nucleaire": 34913,
        "pompage": 0,
        "prevision_j": 43700,
        "prevision_j1": 43950,
        "solaire": 0,
        "taux_co2": 58
      },
      {
        "at": "2026-09-25T20:30:00+00:00",
        "bioenergies": 1015,
        "charbon": 0,
        "ech_physiques": -7633,
        "eolien": 3762,
        "fioul": 499,
        "gaz": 4503,
        "hydraulique": 6659,
        "load": 43105,
        "nucleaire": 34698,
        "pompage": 0,
        "prevision_j": 44200,
        "prevision_j1": 44500,
        "solaire": 0,
        "taux_co2": 55
      },
      {
        "at": "2026-09-25T20:45:00+00:00",
        "bioenergies": 1014,
        "charbon": 0,
        "ech_physiques": -6587,
        "eolien": 3979,
        "fioul": 501,
        "gaz": 4490,
        "hydraulique": 6584,
        "load": 44175,
        "nucleaire": 34542,
        "pompage": 0,
        "prevision_j": 44500,
        "prevision_j1": 44800,
        "solaire": 0,
        "taux_co2": 55
      },
      {
        "at": "2026-09-25T21:00:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -6949,
        "eolien": 4156,
        "fioul": 502,
        "gaz": 4496,
        "hydraulique": 6157,
        "load": 43133,
        "nucleaire": 34188,
        "pompage": 0,
        "prevision_j": 44800,
        "prevision_j1": 45100,
        "solaire": 0,
        "taux_co2": 56
      },
      {
        "at": "2026-09-25T21:15:00+00:00",
        "bioenergies": 1015,
        "charbon": 0,
        "ech_physiques": -6772,
        "eolien": 4058,
        "fioul": 499,
        "gaz": 4499,
        "hydraulique": 6042,
        "load": 42938,
        "nucleaire": 34025,
        "pompage": 0,
        "prevision_j": 44150,
        "prevision_j1": 44450,
        "solaire": 0,
        "taux_co2": 56
      },
      {
        "at": "2026-09-25T21:30:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -6275,
        "eolien": 3979,
        "fioul": 180,
        "gaz": 4335,
        "hydraulique": 5381,
        "load": 42323,
        "nucleaire": 33942,
        "pompage": 0,
        "prevision_j": 43500,
        "prevision_j1": 43800,
        "solaire": 0,
        "taux_co2": 51
      },
      {
        "at": "2026-09-25T21:45:00+00:00",
        "bioenergies": 1017,
        "charbon": 0,
        "ech_physiques": -6127,
        "eolien": 3894,
        "fioul": 37,
        "gaz": 4298,
        "hydraulique": 5295,
        "load": 42041,
        "nucleaire": 33914,
        "pompage": 0,
        "prevision_j": 42700,
        "prevision_j1": 42750,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-25T22:00:00+00:00",
        "bioenergies": 1018,
        "charbon": 0,
        "ech_physiques": -6292,
        "eolien": 3834,
        "fioul": 35,
        "gaz": 4224,
        "hydraulique": 5231,
        "load": 41534,
        "nucleaire": 33837,
        "pompage": -35,
        "prevision_j": 41900,
        "prevision_j1": 41700,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-25T22:15:00+00:00",
        "bioenergies": 1019,
        "charbon": 0,
        "ech_physiques": -6787,
        "eolien": 3757,
        "fioul": 36,
        "gaz": 4053,
        "hydraulique": 5269,
        "load": 41211,
        "nucleaire": 33824,
        "pompage": -33,
        "prevision_j": 41050,
        "prevision_j1": 40950,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-25T22:30:00+00:00",
        "bioenergies": 1014,
        "charbon": 0,
        "ech_physiques": -8300,
        "eolien": 3653,
        "fioul": 37,
        "gaz": 3972,
        "hydraulique": 5169,
        "load": 39812,
        "nucleaire": 33848,
        "pompage": -33,
        "prevision_j": 40200,
        "prevision_j1": 40200,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-25T22:45:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -8933,
        "eolien": 3494,
        "fioul": 36,
        "gaz": 3980,
        "hydraulique": 5088,
        "load": 38630,
        "nucleaire": 33841,
        "pompage": -34,
        "prevision_j": 39250,
        "prevision_j1": 39250,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-25T23:00:00+00:00",
        "bioenergies": 1017,
        "charbon": 0,
        "ech_physiques": -8527,
        "eolien": 3434,
        "fioul": 37,
        "gaz": 3914,
        "hydraulique": 4471,
        "load": 38124,
        "nucleaire": 33737,
        "pompage": -30,
        "prevision_j": 38300,
        "prevision_j1": 38300,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-25T23:15:00+00:00",
        "bioenergies": 1018,
        "charbon": 0,
        "ech_physiques": -8150,
        "eolien": 3276,
        "fioul": 37,
        "gaz": 3992,
        "hydraulique": 4399,
        "load": 38354,
        "nucleaire": 33754,
        "pompage": -35,
        "prevision_j": 38550,
        "prevision_j1": 38550,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-25T23:30:00+00:00",
        "bioenergies": 1019,
        "charbon": 0,
        "ech_physiques": -7934,
        "eolien": 3256,
        "fioul": 37,
        "gaz": 3972,
        "hydraulique": 3479,
        "load": 37665,
        "nucleaire": 33755,
        "pompage": -40,
        "prevision_j": 38800,
        "prevision_j1": 38800,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-25T23:45:00+00:00",
        "bioenergies": 1026,
        "charbon": 0,
        "ech_physiques": -7890,
        "eolien": 3197,
        "fioul": 36,
        "gaz": 3991,
        "hydraulique": 3346,
        "load": 37425,
        "nucleaire": 33742,
        "pompage": -39,
        "prevision_j": 38350,
        "prevision_j1": 38350,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-26T00:00:00+00:00",
        "bioenergies": 1019,
        "charbon": 0,
        "ech_physiques": -8089,
        "eolien": 3173,
        "fioul": 37,
        "gaz": 3862,
        "hydraulique": 3106,
        "load": 36755,
        "nucleaire": 33688,
        "pompage": -41,
        "prevision_j": 37900,
        "prevision_j1": 37900,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-26T00:15:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -8216,
        "eolien": 3062,
        "fioul": 37,
        "gaz": 3874,
        "hydraulique": 2972,
        "load": 36537,
        "nucleaire": 33807,
        "pompage": -42,
        "prevision_j": 36950,
        "prevision_j1": 36950,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-26T00:30:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -9230,
        "eolien": 3165,
        "fioul": 37,
        "gaz": 3871,
        "hydraulique": 2907,
        "load": 35582,
        "nucleaire": 33837,
        "pompage": -43,
        "prevision_j": 36000,
        "prevision_j1": 36000,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-26T00:45:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -9314,
        "eolien": 3168,
        "fioul": 36,
        "gaz": 3835,
        "hydraulique": 2791,
        "load": 35188,
        "nucleaire": 33833,
        "pompage": -273,
        "prevision_j": 35300,
        "prevision_j1": 35300,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-26T01:00:00+00:00",
        "bioenergies": 1016,
        "charbon": 0,
        "ech_physiques": -9846,
        "eolien": 3165,
        "fioul": 37,
        "gaz": 3622,
        "hydraulique": 2772,
        "load": 34294,
        "nucleaire": 33850,
        "pompage": -279,
        "prevision_j": 34600,
        "prevision_j1": 34600,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-26T01:15:00+00:00",
        "bioenergies": 1017,
        "charbon": 0,
        "ech_physiques": -10041,
        "eolien": 3159,
        "fioul": 36,
        "gaz": 3640,
        "hydraulique": 2615,
        "load": 33905,
        "nucleaire": 33909,
        "pompage": -479,
        "prevision_j": 34300,
        "prevision_j1": 34300,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-26T01:30:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -10100,
        "eolien": 3150,
        "fioul": 37,
        "gaz": 3574,
        "hydraulique": 2521,
        "load": 33636,
        "nucleaire": 33889,
        "pompage": -480,
        "prevision_j": 34000,
        "prevision_j1": 34000,
        "solaire": 0,
        "taux_co2": 46
      },
      {
        "at": "2026-09-26T01:45:00+00:00",
        "bioenergies": 1010,
        "charbon": 0,
        "ech_physiques": -10432,
        "eolien": 3242,
        "fioul": 36,
        "gaz": 3494,
        "hydraulique": 2414,
        "load": 33413,
        "nucleaire": 33919,
        "pompage": -241,
        "prevision_j": 33600,
        "prevision_j1": 33600,
        "solaire": 0,
        "taux_co2": 46
      },
      {
        "at": "2026-09-26T02:00:00+00:00",
        "bioenergies": 1015,
        "charbon": 0,
        "ech_physiques": -10426,
        "eolien": 3185,
        "fioul": 36,
        "gaz": 3356,
        "hydraulique": 2358,
        "load": 33185,
        "nucleaire": 33905,
        "pompage": -245,
        "prevision_j": 33200,
        "prevision_j1": 33200,
        "solaire": 0,
        "taux_co2": 45
      },
      {
        "at": "2026-09-26T02:15:00+00:00",
        "bioenergies": 1015,
        "charbon": 0,
        "ech_physiques": -10805,
        "eolien": 3127,
        "fioul": 36,
        "gaz": 3510,
        "hydraulique": 2349,
        "load": 32901,
        "nucleaire": 33937,
        "pompage": -242,
        "prevision_j": 32900,
        "prevision_j1": 32900,
        "solaire": 0,
        "taux_co2": 46
      },
      {
        "at": "2026-09-26T02:30:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -10566,
        "eolien": 3041,
        "fioul": 37,
        "gaz": 3528,
        "hydraulique": 2327,
        "load": 33001,
        "nucleaire": 33906,
        "pompage": -244,
        "prevision_j": 32600,
        "prevision_j1": 32600,
        "solaire": 0,
        "taux_co2": 46
      },
      {
        "at": "2026-09-26T02:45:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -10867,
        "eolien": 2921,
        "fioul": 37,
        "gaz": 3541,
        "hydraulique": 2343,
        "load": 32636,
        "nucleaire": 33898,
        "pompage": -240,
        "prevision_j": 32600,
        "prevision_j1": 32600,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-26T03:00:00+00:00",
        "bioenergies": 1015,
        "charbon": 0,
        "ech_physiques": -10728,
        "eolien": 2838,
        "fioul": 36,
        "gaz": 3565,
        "hydraulique": 2384,
        "load": 32765,
        "nucleaire": 33907,
        "pompage": -238,
        "prevision_j": 32600,
        "prevision_j1": 32600,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-26T03:15:00+00:00",
        "bioenergies": 1017,
        "charbon": 0,
        "ech_physiques": -10651,
        "eolien": 2729,
        "fioul": 36,
        "gaz": 3567,
        "hydraulique": 2447,
        "load": 33000,
        "nucleaire": 33898,
        "pompage": -35,
        "prevision_j": 32850,
        "prevision_j1": 32850,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-26T03:30:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -10805,
        "eolien": 2633,
        "fioul": 37,
        "gaz": 3587,
        "hydraulique": 2436,
        "load": 32739,
        "nucleaire": 33898,
        "pompage": -40,
        "prevision_j": 33100,
        "prevision_j1": 33100,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-26T03:45:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -10644,
        "eolien": 2634,
        "fioul": 36,
        "gaz": 3582,
        "hydraulique": 2463,
        "load": 32878,
        "nucleaire": 33854,
        "pompage": -39,
        "prevision_j": 33250,
        "prevision_j1": 33250,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-26T04:00:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": -10467,
        "eolien": 2721,
        "fioul": 37,
        "gaz": 3496,
        "hydraulique": 2475,
        "load": 33122,
        "nucleaire": 33898,
        "pompage": -40,
        "prevision_j": 33400,
        "prevision_j1": 33400,
        "solaire": 0,
        "taux_co2": 46
      },
      {
        "at": "2026-09-26T04:15:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -10102,
        "eolien": 2767,
        "fioul": 37,
        "gaz": 3756,
        "hydraulique": 2701,
        "load": 34021,
        "nucleaire": 33900,
        "pompage": -40,
        "prevision_j": 33700,
        "prevision_j1": 33700,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-26T04:30:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -10470,
        "eolien": 2702,
        "fioul": 37,
        "gaz": 3758,
        "hydraulique": 2945,
        "load": 33851,
        "nucleaire": 33913,
        "pompage": -42,
        "prevision_j": 34000,
        "prevision_j1": 34000,
        "solaire": 0,
        "taux_co2": 48
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
    },
    {
      "as_of": "2026-08",
      "change": 0.097,
      "comparison": "vs mois précédent",
      "detail": "Pétrole + LGN + condensats ; pas uniquement le Brent",
      "id": "oil_norway_liquids",
      "label": "Production Norvège · pétrole et liquides",
      "sector": "oil",
      "source": "Sodir · provisoire",
      "unit": "M bbl/j",
      "url": "https://www.sodir.no/en/whats-new/news/production-figures/2026/production-figures-august-2026/",
      "value": 2.073
    },
    {
      "as_of": "2026-09-22",
      "change": -1.26,
      "comparison": "vs séance précédente",
      "detail": "Clôture quotidienne publiée avec retard ; pas un future",
      "id": "price_brent",
      "label": "Brent Europe · spot EIA",
      "sector": "oil",
      "source": "EIA · prix spot",
      "unit": "$/bbl",
      "url": "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm",
      "value": 114.89
    },
    {
      "as_of": "2026-09-22",
      "change": -0.56,
      "comparison": "vs séance précédente",
      "detail": "Clôture quotidienne publiée avec retard ; pas un future",
      "id": "price_wti",
      "label": "WTI Cushing · spot EIA",
      "sector": "oil",
      "source": "EIA · prix spot",
      "unit": "$/bbl",
      "url": "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm",
      "value": 96.41
    },
    {
      "as_of": "2026-09-22",
      "change": -0.03,
      "comparison": "vs séance précédente",
      "detail": "Clôture quotidienne publiée avec retard ; pas un future",
      "id": "price_henry",
      "label": "Henry Hub · spot EIA",
      "sector": "gas",
      "source": "EIA · prix spot",
      "unit": "$/MMBtu",
      "url": "https://www.eia.gov/dnav/ng/NG_PRI_FUT_S1_D.htm",
      "value": 2.9
    },
    {
      "as_of": "2026-09-26",
      "change": 1112,
      "comparison": "vs ~1 h",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_load",
      "label": "Demande France",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 33851
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "export si négatif · import si positif",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_exchange",
      "label": "Solde des échanges physiques",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -10470
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_nucleaire",
      "label": "Nucléaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 33913
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_gaz",
      "label": "Gaz électrique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 3758
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_eolien",
      "label": "Éolien",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 2702
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_solaire",
      "label": "Solaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 0
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_hydraulique",
      "label": "Hydraulique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 2945
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_bioenergies",
      "label": "Bioénergies",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 1003
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "demande − éolien − solaire",
      "detail": "Calcul indicatif, sans jugement sur le prix ni l'appel au gaz. Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_residual",
      "label": "Demande résiduelle indicative",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 31149
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "production française",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_carbon",
      "label": "Intensité CO₂ estimée",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "g/kWh",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 48
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "réalisé − prévision réactualisée le jour même",
      "detail": "Observation 2026-09-26T04:30:00+00:00 UTC",
      "id": "power_load_gap",
      "label": "Écart à prévision de demande J",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -149
    },
    {
      "as_of": "2026-09-24",
      "change": 0.1,
      "comparison": "points vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu",
      "label": "Stockage gaz UE · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 70.45
    },
    {
      "as_of": "2026-09-24",
      "change": 1.09,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_twh",
      "label": "Gaz stocké UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 797.198
    },
    {
      "as_of": "2026-09-24",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_net",
      "label": "Soutirage net UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -1095.0
    },
    {
      "as_of": "2026-09-24",
      "change": 0.18,
      "comparison": "points vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr",
      "label": "Stockage gaz France · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 81.61
    },
    {
      "as_of": "2026-09-24",
      "change": 0.222,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_twh",
      "label": "Gaz stocké France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 101.093
    },
    {
      "as_of": "2026-09-24",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_net",
      "label": "Soutirage net France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -221.6
    },
    {
      "as_of": "2026-09-24",
      "change": -228.03,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "lng_eu_inventory",
      "label": "GNL en cuves UE",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "10³ m³ GNL",
      "url": "https://alsi.gie.eu/",
      "value": 4203.3
    },
    {
      "as_of": "2026-09-24",
      "change": -42.4,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "lng_eu_sendout",
      "label": "Émission terminaux GNL UE",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "GWh/j",
      "url": "https://alsi.gie.eu/",
      "value": 3889.8
    },
    {
      "as_of": "2026-09-24",
      "change": -59.01,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "lng_fr_inventory",
      "label": "GNL en cuves France",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "10³ m³ GNL",
      "url": "https://alsi.gie.eu/",
      "value": 710.53
    },
    {
      "as_of": "2026-09-24",
      "change": -34.0,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "lng_fr_sendout",
      "label": "Émission terminaux GNL France",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "GWh/j",
      "url": "https://alsi.gie.eu/",
      "value": 847.8
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "prévision J-1, 24 h glissantes",
      "detail": "Pic prévu à 2026-09-26T11:00:00+00:00 UTC",
      "id": "power_forecast_fr",
      "label": "Pic prévu 24 h · France",
      "sector": "power",
      "source": "ENTSO-E · prévision J-1",
      "unit": "MW",
      "url": "https://transparency.entsoe.eu/",
      "value": 43600
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "prévision J-1, 24 h glissantes",
      "detail": "Pic prévu à 2026-09-26T08:45:00+00:00 UTC",
      "id": "power_forecast_de",
      "label": "Pic prévu 24 h · Allemagne/Luxembourg",
      "sector": "power",
      "source": "ENTSO-E · prévision J-1",
      "unit": "MW",
      "url": "https://transparency.entsoe.eu/",
      "value": 52143
    }
  ],
  "schema": 3,
  "sources": {
    "alsi": {
      "as_of": "2026-09-24",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://alsi.gie.eu/"
    },
    "alsi_fr": {
      "as_of": "2026-09-24",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://alsi.gie.eu/"
    },
    "brent": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm"
    },
    "entsoe_de": {
      "as_of": "2026-09-26T08:45:00+00:00",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://transparency.entsoe.eu/"
    },
    "entsoe_fr": {
      "as_of": "2026-09-26T11:00:00+00:00",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://transparency.entsoe.eu/"
    },
    "gas": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://ir.eia.gov/ngs/ngs.html"
    },
    "gie": {
      "as_of": "2026-09-24",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "gie_fr": {
      "as_of": "2026-09-24",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "henry": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/dnav/ng/NG_PRI_FUT_S1_D.htm"
    },
    "metals": {
      "as_of": "2025",
      "status": "structural",
      "url": "https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports"
    },
    "news": {
      "as_of": "2026-09-25",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/rss/todayinenergy.xml"
    },
    "norway": {
      "as_of": "2026-08",
      "message": "Repère mensuel vérifié ; collecte automatique indisponible.",
      "status": "manual",
      "url": "https://www.sodir.no/en/whats-new/news/production-figures/"
    },
    "oil": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_flows": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_history": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "published": "2026-09-23",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "rte_power": {
      "as_of": "2026-09-26T04:30:00+00:00",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/"
    },
    "wasde": {
      "as_of": "2026-09",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt"
    },
    "wti": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-26T04:58:49+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm"
    }
  },
  "stories": [
    {
      "date": "2026-09-25",
      "source": "EIA · Today in Energy",
      "summary": "The Henry Hub natural gas spot price averaged $2.93 per million British thermal units from June through August, 6% less than the same period last year. Prices were lower this summer despite exceptionally hot weather that increased electricity demand for air co",
      "title": "Henry Hub natural gas prices this summer were 6% lower than last summer",
      "url": "https://www.eia.gov/todayinenergy/detail.php?id=68204"
    },
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
    }
  ]
}
</script>
  <script>
    const snapshot = JSON.parse(document.getElementById('snapshot-data').textContent);
    const metrics = Array.isArray(snapshot.metrics) ? snapshot.metrics : [];
    const byId = Object.fromEntries(metrics.map(item => [item.id, item]));
    const sectors = {oil: 'Pétrole · Brent spot, flux et stocks', gas: 'Gaz · France, Europe, GNL et États-Unis',
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
      const limit = item.id === 'oil_norway_liquids' ? 80 : item.id.startsWith('price_') ? 8 :
        item.source?.startsWith('GIE') ? 4 : ({oil: 13, gas: 13, agri: 49, metals: 800}[item.sector] || 14);
      return age(item) > limit;
    }
    function safeLink(url) {
      try {
        const parsed = new URL(url);
        const hosts = ['www.eia.gov', 'ir.eia.gov', 'www.usda.gov', 'pubs.usgs.gov',
          'agsi.gie.eu', 'alsi.gie.eu', 'fred.stlouisfed.org', 'www.sodir.no', 'www.eex.com',
          'www.ice.com', 'www.tradingview.com', 'transparency.entsog.eu'];
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
      if (item.id === 'gas_eu' || item.id === 'gas_fr') return symbol + number(Math.abs(item.change), 2) + ' point(s) vs veille';
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
      if (['gas_fr','gas_eu'].includes(item.id)) {
        const track = line('', 'div', 'gauge');
        const fill = line('', 'i');
        fill.style.width = Math.max(0, Math.min(100, item.value)) + '%';
        track.append(fill);
        card.append(track);
      }
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
      const labels = {brent: 'Brent spot', wti: 'WTI spot', henry: 'Henry Hub spot',
        norway: 'Production Norvège',
        oil: 'EIA stocks pétrole', oil_flows: 'EIA flux pétrole', gas: 'EIA gaz US', wasde: 'USDA WASDE',
        news: 'Analyses EIA', gie: 'GIE stockage UE', gie_fr: 'GIE stockage France',
        alsi: 'GIE GNL UE', alsi_fr: 'GIE GNL France', metals: 'USGS métaux'};
      for (const [id, label] of Object.entries(labels)) {
        const source = snapshot.sources?.[id] || {};
        const sample = {brent:'price_brent',wti:'price_wti',henry:'price_henry',
          norway:'oil_norway_liquids',
          oil:'oil_crude',oil_flows:'oil_imports',gas:'gas_us',wasde:'ag_corn_stocks',
          gie:'gas_eu',gie_fr:'gas_fr',alsi:'lng_eu_inventory',
          alsi_fr:'lng_fr_inventory',metals:'metal_copper'}[id];
        const hasValue = Boolean(sample && byId[sample]) || (id === 'news' && (snapshot.stories || []).length > 0);
        const status = source.status === 'ok' ? period(source.as_of || '') +
          (byId[sample] && stale(byId[sample]) ? ' · archive' : '') :
          source.status === 'needs_key' ? 'clé requise' :
          source.status === 'structural' ? 'repère annuel' :
          source.status === 'manual' ? 'repère mensuel daté' :
          hasValue ? 'dernière valeur conservée' : 'source indisponible';
        container.append(line(label + ' · ' + status, 'span',
          'badge ' + (source.status === 'ok' && (!byId[sample] || !stale(byId[sample])) ? 'good' : 'warn')));
      }
      document.getElementById('updated').textContent = snapshot.generated_at ?
        'Collecte : ' + new Intl.DateTimeFormat('fr-FR', {dateStyle:'medium', timeStyle:'short', timeZone:'Europe/Paris'}).format(new Date(snapshot.generated_at)) + ' · Paris' :
        'Instantané local';
    }

    function renderMini() {
      const grid = document.getElementById('mini-grid');
      for (const id of ['price_brent', 'oil_crude', 'gas_fr', 'lng_fr_sendout', 'gas_us', 'ag_world_corn']) {
        const item = byId[id];
        if (!item) continue;
        const card = line('', 'div', 'mini');
        card.append(line(item.label, 'small'));
        card.append(line(number(item.value, digits(item)) + ' ' + item.unit, 'strong'));
        card.append(line(changeText(item) + (stale(item) ? ' · archive' : ''), 'span'));
        grid.append(card);
      }
      if (!grid.children.length) grid.append(line('La collecte des chiffres physiques est en attente.', 'p', 'empty'));
    }

    function renderMarketSummary() {
      const box = document.getElementById('market-snapshot');
      for (const id of ['gas_fr', 'lng_fr_sendout', 'oil_norway_liquids', 'oil_crude', 'gas_us']) {
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

    const marketLinks = [
      {label: 'TTF · indice spot EEX', note: 'Prix en séance sur la source · pas le future M+1',
       url: 'https://www.eex.com/en/market-data/market-data-hub/natural-gas/indices'},
      {label: 'TTF · future ICE', note: 'Échéance et délai de cotation sur TradingView',
       url: 'https://www.tradingview.com/symbols/ICEEUR-TFN1%21/'},
      {label: 'PEG France · indice spot EEX', note: 'Référence PEG · prix en séance sur la source',
       url: 'https://www.eex.com/en/market-data/market-data-hub/natural-gas/indices'},
      {label: 'JKM · future ICE', note: 'Contrat financier indexé sur le JKM Platts · $/MMBtu',
       url: 'https://www.ice.com/products/6753280/jkm-lng-platts-future'},
    ];
    const charts = [
      {name:'Brent', symbol:'OANDA:BCOUSD', url:'https://www.tradingview.com/symbols/BCOUSD/?exchange=OANDA'},
      {name:'WTI', symbol:'OANDA:WTICOUSD', url:'https://www.tradingview.com/symbols/WTICOUSD/?exchange=OANDA'},
      {name:'Gaz US', symbol:'OANDA:NATGASUSD', url:'https://www.tradingview.com/symbols/NATGASUSD/?exchange=OANDA'},
      {name:'Cuivre', symbol:'OANDA:XCUUSD', url:'https://www.tradingview.com/symbols/XCUUSD/?exchange=OANDA'},
      {name:'Or', symbol:'OANDA:XAUUSD', url:'https://www.tradingview.com/symbols/XAUUSD/?exchange=OANDA'}
    ];
    function embed(container, scriptUrl, config) {
      container.replaceChildren();
      const frame = line('', 'div', 'tradingview-widget-container');
      frame.append(line('', 'div', 'tradingview-widget-container__widget'));
      const script = document.createElement('script');
      script.async = true;
      script.src = scriptUrl;
      script.textContent = JSON.stringify(config);
      frame.append(script);
      container.append(frame);
    }
    function renderChart(index = 0) {
      const choice = charts[index];
      document.getElementById('market-chart-title').textContent = choice.name + ' · indicatif OANDA';
      document.getElementById('market-chart-link').href = choice.url;
      document.querySelectorAll('#chart-picks button').forEach((button, i) => {
        button.classList.toggle('active', i === index);
        button.setAttribute('aria-pressed', String(i === index));
      });
      embed(document.getElementById('market-chart'),
        'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js',
        {autosize:true,symbol:choice.symbol,interval:'60',timezone:'Europe/Paris',
         theme:'dark',style:'1',locale:'fr',allow_symbol_change:true,
         hide_top_toolbar:false,support_host:'https://www.tradingview.com'});
    }
    function renderQuotes() {
      const picks = document.getElementById('chart-picks');
      charts.forEach((choice, index) => {
        const button = line(choice.name, 'button');
        button.type = 'button';
        button.addEventListener('click', () => renderChart(index));
        picks.append(button);
      });
      renderChart();
      embed(document.getElementById('market-quotes'),
        'https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js',
        {width:'100%',height:'100%',symbolsGroups:[
          {name:'Énergie · indicatif OANDA',symbols:[
            {name:'OANDA:BCOUSD',displayName:'Brent · indicatif'},
            {name:'OANDA:WTICOUSD',displayName:'WTI · indicatif'},
            {name:'OANDA:NATGASUSD',displayName:'Gaz US · indicatif'}]},
          {name:'Métaux · indicatif OANDA',symbols:[
            {name:'OANDA:XCUUSD',displayName:'Cuivre · USD/lb'},
            {name:'OANDA:XAUUSD',displayName:'Or · USD/oz'}]}],
         showSymbolLogo:false, isTransparent:true,colorTheme:'dark',locale:'fr'});
      const gas = document.getElementById('gas-prices');
      for (const [title,detail,href] of [
        ['TTF','Spot EEX et future M+1 ICE · €/MWh','https://www.eex.com/en/market-data/market-data-hub/natural-gas/indices'],
        ['PEG France','Indice spot EEX · €/MWh','https://www.eex.com/en/market-data/market-data-hub/natural-gas/indices'],
        ['JKM','Future ICE indexé sur le JKM Platts · $/MMBtu','https://www.ice.com/products/6753280/jkm-lng-platts-future']]) {
        const card = line('', 'article', 'price-link');
        card.append(line(title, 'strong'), line(detail, 'small'));
        const link = line('Consulter le cours et son horaire ↗', 'a');
        link.href = href; link.target = '_blank'; link.rel = 'noopener noreferrer';
        card.append(link, line('Cotation non redistribuée sur ce tableau.', 'p'));
        gas.append(card);
      }
    }
    function renderTicker() {
      const box = document.getElementById('ticker');
      for (const [id, title] of [['price_brent','BRENT spot'], ['price_wti','WTI spot'],
                                 ['price_henry','HENRY HUB spot']]) {
        const item = byId[id];
        const anchor = document.createElement('a');
        anchor.href = safeLink(item?.url) || (id === 'price_henry' ?
          'https://www.eia.gov/naturalgas/' : 'https://www.eia.gov/dnav/pet/PET_PRI_SPT_S1_D.htm');
        anchor.target = '_blank';
        anchor.rel = 'noopener noreferrer';
        anchor.append(line(title, 'small'));
        anchor.append(line(item ? number(item.value, 2) + ' ' + item.unit :
          'Dernière donnée en attente', 'b'));
        anchor.append(line(item ? period(item.as_of) + (stale(item) ? ' · archive' : '') :
          'EIA · clôture quotidienne', 'small'));
        box.append(anchor);
      }
    }

    function renderWatch() {
      const box = document.getElementById('watch-list');
      box.append(line('REPÈRES SPOT OFFICIELS · CLÔTURES DATÉES', 'div', 'watch-group'));
      for (const id of ['price_brent', 'price_wti', 'price_henry']) {
        const item = byId[id];
        const row = line('', 'div', 'quote-row');
        const label = {price_brent:'Brent Europe · spot',price_wti:'WTI Cushing · spot',
          price_henry:'Henry Hub · spot'}[id];
        row.append(line(label, 'strong'));
        const price = line(item ? number(item.value, 2) + ' ' + item.unit + ' ↗' :
          'En attente', item ? 'a' : 'span', 'quote-value');
        if (item) {
          price.href = safeLink(item.url);
          price.target = '_blank';
          price.rel = 'noopener noreferrer';
        }
        row.append(price);
        row.append(line(item ? 'EIA spot · ' + period(item.as_of) +
          (stale(item) ? ' · ARCHIVE' : '') : 'Collecte officielle en cours', 'small', 'quote-note'));
        box.append(row);
      }
      box.append(line('CONTRATS ET AUTRES MATIÈRES · ACCÈS DIRECT', 'div', 'watch-group'));
      const other = [
        ...marketLinks.slice(1, 2),
        {label:'Aluminium · LME',note:'Cours et unité sur la bourse',url:'https://www.lme.com/Metals/Non-ferrous/LME-Aluminium'},
        {label:'Cacao · ICE',note:'Future CC1! · échéance à vérifier',url:'https://www.tradingview.com/symbols/ICEUS-CC1%21/'},
        {label:'Café Arabica · ICE',note:'Future KC1! · échéance à vérifier',url:'https://www.tradingview.com/symbols/ICEUS-KC1%21/'}
      ];
      for (const item of other) {
        const row = line('', 'div', 'quote-row');
        row.append(line(item.label, 'strong'));
        const wrap = line('', 'span', 'quote-value');
        const link = line('Voir cours ↗', 'a');
        link.href = item.url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        wrap.append(link);
        row.append(wrap, line(item.note, 'small', 'quote-note'));
        box.append(row);
      }
      box.append(line('JKM–TTF : mêmes échéances et même unité indispensables pour comparer un spread.', 'div', 'caption'));
    }

    function renderAgenda() {
      const box = document.getElementById('agenda');
      const upcoming = (snapshot.calendar || []).filter(event =>
        event.day_only ? Date.parse(event.at) + 86400000 > Date.now() :
          Date.parse(event.at) > Date.now()).slice(0, 4);
      for (const event of upcoming) {
        const row = line('', 'div', 'agenda-row');
        const when = line('', 'span', 'agenda-when');
        const moment = new Date(event.at);
        when.append(line(new Intl.DateTimeFormat('fr-FR', {day:'2-digit', month:'short',
          timeZone:'Europe/Paris'}).format(moment), 'span'));
        when.append(line(event.day_only ? 'heure à confirmer' :
          new Intl.DateTimeFormat('fr-FR', {hour:'2-digit', minute:'2-digit',
          timeZone:'Europe/Paris'}).format(moment), 'small'));
        const detail = line('', 'div');
        const link = line(event.title + ' ↗', 'a');
        link.href = safeLink(event.url) || 'https://www.eia.gov/';
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        detail.append(link, line(event.context, 'p'));
        row.append(when, detail);
        box.append(row);
      }
      if (!upcoming.length) box.append(line('Dates à vérifier sur les calendriers officiels avant de nouvelles prévisions.', 'p', 'empty'));
    }

    function renderReleases() {
      const box = document.getElementById('release-list');
      for (const [id, label] of [['oil_crude','EIA pétrole'], ['gas_fr','GIE stockage France'],
                                 ['gas_us','EIA gaz US'], ['ag_corn_stocks','USDA WASDE']]) {
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

    const signalRules = {
      oil: [
        {id:'oil_crude', label:'Brut US · stocks', market:'Brent / WTI', rising:'Stocks en hausse : offre disponible plus abondante, pression possible à la baisse.', falling:'Stocks en baisse : offre plus resserrée, pression possible à la hausse.'},
        {id:'oil_cushing', label:'Cushing · stocks WTI', market:'WTI', rising:'Cushing se remplit : facteur potentiellement baissier pour le WTI.', falling:'Cushing se vide : facteur potentiellement haussier pour le WTI.'},
        {id:'oil_imports', label:'Importations US', market:'Brent / WTI', rising:'Entrées plus élevées : peuvent alimenter les stocks et les raffineries.', falling:'Entrées plus faibles : peuvent resserrer le brut disponible.'}],
      gas: [
        {id:'gas_fr', label:'Stockage France', market:'PEG / TTF', rising:'Remplissage en hausse : coussin de sécurité en progression.', falling:'Remplissage en baisse : coussin de sécurité en recul.'},
        {id:'gas_eu', label:'Stockage Europe', market:'TTF', rising:'Stock européen en hausse : tension potentielle moindre.', falling:'Stock européen en baisse : tension potentielle accrue.'},
        {id:'lng_fr_sendout', label:'GNL · terminaux France', market:'PEG / TTF', rising:'Émission plus forte : davantage de gaz arrive au réseau français.', falling:'Émission plus faible : apport des terminaux plus limité.'}],
      agri: [
        {id:'ag_world_corn', label:'Stocks mondiaux de maïs', market:'Maïs', rising:'Révision des stocks à la hausse : pression potentielle à la baisse.', falling:'Révision des stocks à la baisse : pression potentielle à la hausse.'}]
    };
    function renderSignals() {
      const box = document.getElementById('signals');
      box.replaceChildren();
      const rules = signalRules[selectedSector] || [];
      for (const rule of rules) {
        const item = byId[rule.id];
        if (!item) continue;
        const delta = item.change;
        const known = Number.isFinite(delta) && !stale(item);
        const cls = !known || !delta ? 'flat' : delta < 0 ? 'down' : '';
        const card = line('', 'article', 'card signal ' + cls);
        card.append(line(rule.label + ' · ' + period(item.as_of), 'small'));
        card.append(line(number(item.value, digits(item)) + ' ' + item.unit, 'strong'));
        card.append(line(known ? changeText(item) : 'Variation récente non vérifiée', 'small'));
        card.append(line(known && delta ? delta > 0 ? rule.rising : rule.falling :
          'Pas de signal directionnel récent. Vérifier la prochaine publication.', 'p'));
        card.append(line('Marché concerné : ' + rule.market + ' · scénario, pas une réaction de cours.', 'small'));
        box.append(card);
      }
      if (!box.children.length) box.append(line('Pas encore de variation récente exploitable pour ce secteur. Les chiffres datés restent accessibles ci-dessous.', 'p', 'empty'));
    }

    function renderStories() {
      const box = document.getElementById('stories');
      const relevant = (snapshot.stories || []).filter(item =>
        /crude|oil|natural gas|\blng\b|diesel|refin|petroleum|gasoline|fuel|storage/i.test(item.title + ' ' + item.summary));
      for (const item of relevant.slice(0, 5)) {
        const href = safeLink(item.url);
        if (!href) continue;
        const story = line('', 'article', 'story');
        const title = line(item.title, 'a');
        title.href = href;
        title.target = '_blank';
        title.rel = 'noopener noreferrer';
        story.append(title);
        if (item.summary) story.append(line(item.summary, 'p'));
        story.append(line(item.source + ' · ' + period(item.date) +
          ((Date.now() - Date.parse(item.date + 'T12:00:00Z')) / 86400000 > 30 ? ' · ARCHIVE' : ''), 'small'));
        box.append(story);
      }
      if (!box.children.length) box.append(line('Aucun article EIA sur le pétrole ou le gaz dans le flux actuel.', 'p'));
    }

    function drawTrend(panelId, lineId, startId, endId, titleId, title, points) {
      const panel = document.getElementById(panelId);
      panel.hidden = !Array.isArray(points) || points.length < 2;
      if (panel.hidden) return;
      const nums = points.map(point => point.value);
      const span = Math.max(0.1, Math.max(...nums) - Math.min(...nums));
      const low = Math.min(...nums) - span * .15;
      const high = Math.max(...nums) + span * .15;
      const coords = nums.map((value, index) => {
        const x = 4 + (index * 392 / (nums.length - 1));
        const y = 100 - ((value - low) / (high - low) * 90);
        return x.toFixed(1) + ',' + y.toFixed(1);
      });
      document.getElementById(lineId).setAttribute('points', coords.join(' '));
      document.getElementById(startId).textContent = period(points[0].date) + ' · ' + number(nums[0], 1);
      document.getElementById(endId).textContent = period(points[points.length - 1].date) + ' · ' + number(nums[nums.length - 1], 1);
      document.getElementById(titleId).textContent = title;
    }
    function renderTrend() {
      const history = snapshot.history || {};
      const pairs = selectedSector === 'oil' ?
        [['Stocks brut US · millions de barils · 26 semaines',history.oil_crude],null] :
        selectedSector === 'gas' ? [
          ['Stockage France · % · données quotidiennes GIE',history.gas_fr],
          ['GNL France · émission GWh/j · données GIE',history.lng_fr_sendout]] : [null,null];
      for (const [index, pair] of pairs.entries()) {
        const suffix = index ? '-two' : '';
        drawTrend('trend' + suffix, 'trend' + suffix + '-line',
          'trend' + suffix + '-start', 'trend' + suffix + '-end',
          'trend' + suffix + '-title', pair?.[0] || '', pair?.[1] || []);
      }
    }

    function renderSector() {
      document.getElementById('sector-heading').textContent = sectors[selectedSector];
      const box = document.getElementById('metrics');
      box.replaceChildren();
      const preferred = selectedSector === 'oil' ? ['price_brent','oil_norway_liquids',
        'price_wti','oil_crude','oil_cushing'] :
        selectedSector === 'gas' ? ['gas_fr','gas_fr_twh','gas_fr_net','lng_fr_sendout',
          'lng_fr_inventory','gas_eu','gas_eu_twh','lng_eu_sendout','price_henry','gas_us'] : [];
      const order = new Map(preferred.map((id, index) => [id, index]));
      const sorted = metrics.filter(metric => metric.sector === selectedSector)
        .sort((a, b) => (order.get(a.id) ?? 999) - (order.get(b.id) ?? 999));
      for (const item of sorted) box.append(renderMetric(item));
      if (!box.children.length) box.append(line('Aucune valeur vérifiée disponible pour ce secteur.', 'p', 'empty'));
      document.querySelectorAll('.filters button').forEach(button => button.classList.toggle('active', button.dataset.sector === selectedSector));
      renderTakeaways();
      renderSignals();
      renderTrend();
    }

    function parisTime(value) {
      const stamp = new Date(value);
      return Number.isNaN(stamp.getTime()) ? 'heure indisponible' :
        new Intl.DateTimeFormat('fr-FR', {day:'numeric',month:'short',hour:'2-digit',minute:'2-digit',
          timeZone:'Europe/Paris'}).format(stamp) + ' · Paris';
    }

    function renderPower() {
      const grid = document.getElementById('power-grid');
      const points = Array.isArray(snapshot.history?.power_fr) ? snapshot.history.power_fr : [];
      const latest = points[points.length - 1];
      const measuredAt = latest && Date.parse(latest.at);
      const powerOld = !measuredAt || Date.now() - measuredAt > 6 * 3600000;
      const source = snapshot.sources?.rte_power || {};
      const rte = document.getElementById('power-rte-status');
      rte.textContent = latest ?
        'RTE · ' + (powerOld ? 'archive · ' : '') + parisTime(latest.at) +
          (source.status === 'error' ? ' · dernière valeur conservée' : '') :
        'RTE · première collecte en attente';
      rte.classList.toggle('good', !!latest && !powerOld && source.status === 'ok');
      rte.classList.toggle('warn', !latest || powerOld || source.status === 'error');
      document.getElementById('power-updated').textContent = snapshot.generated_at ?
        'Dernière collecte : ' + parisTime(snapshot.generated_at) : 'Instantané local';
      const picks = [
        ['power_load', 'consommation observée'],
        ['power_gaz', 'production électrique au gaz'],
        ['power_exchange', 'négatif : export / positif : import'],
        ['power_residual', 'calcul : demande − éolien − solaire']
      ];
      for (const [id, hint] of picks) {
        const item = byId[id];
        const card = line('', 'article', 'card power-card');
        card.append(line(item?.label || id, 'small'));
        card.append(line(item ? number(item.value, 0) + ' MW' : '—', 'strong'));
        card.append(line(item ? (powerOld ? 'Archive · ' : '') + hint : 'Mesure en attente', 'span'));
        grid.append(card);
      }
      const entsoe = document.getElementById('power-entsoe-status');
      const entsoeRows = ['fr', 'de'].map(zone => ({zone, item:byId['power_forecast_' + zone],
        source:snapshot.sources?.['entsoe_' + zone] || {}}));
      const configured = entsoeRows.some(entry => entry.source.status !== 'needs_key' && entry.source.status);
      entsoe.textContent = configured ? 'ENTSO-E · ' +
        (entsoeRows.every(entry => entry.source.status === 'ok') ? 'prévisions collectées' : 'collecte partielle') :
        'ENTSO-E · clé non configurée';
      entsoe.classList.toggle('good', entsoeRows.every(entry => entry.source.status === 'ok'));
      entsoe.classList.toggle('warn', !entsoeRows.every(entry => entry.source.status === 'ok'));
      const forecast = document.getElementById('power-forecast');
      for (const entry of entsoeRows) {
        const box = line('', 'div');
        box.append(line(entry.zone === 'fr' ? 'France' : 'DE-LU', 'small'));
        const m = entry.item;
        box.append(line(m ? number(m.value, 0) + ' MW' : '—', 'strong'));
        const forecastAt = entry.source.as_of;
        const valid = m && forecastAt && Date.parse(forecastAt) >= Date.now();
        box.append(line(m ? (valid ? 'Pic prévu : ' : 'Prévision archivée : ') +
          parisTime(forecastAt) : entry.source.status === 'needs_key' ? 'Clé requise' :
          'Publication indisponible', 'span'));
        forecast.append(box);
      }
      document.getElementById('power-forecast-note').textContent = !configured ?
        'Activer : Settings → Secrets and variables → Actions → ENTSOE_API_TOKEN ; puis relancer le workflow.' :
        'Prévisions datées : valeur du pic prévu, pas un prix ni la consommation déjà réalisée.';
      if (!latest) return;
      const gas = byId.power_gaz?.value;
      const exchange = byId.power_exchange?.value;
      const wind = byId.power_eolien?.value;
      const solar = byId.power_solaire?.value;
      const facts = [];
      if (gas !== undefined) facts.push('Gaz mobilisé : ' + number(gas, 0) + ' MW.');
      const loadGap = byId.power_load_gap?.value;
      if (loadGap !== undefined) facts.push('Demande réalisée ' +
        number(Math.abs(loadGap), 0) + ' MW ' + (loadGap < 0 ? 'sous' : loadGap > 0 ? 'au-dessus de' : 'égale à') +
        ' la prévision RTE du jour.');
      if (wind !== undefined && solar !== undefined) facts.push('Éolien + solaire : ' + number(wind + solar, 0) + ' MW.');
      if (exchange !== undefined) facts.push('Solde physique : ' + number(Math.abs(exchange), 0) +
        ' MW d’' + (exchange < 0 ? 'exportations nettes' : exchange > 0 ? 'importations nettes' : 'équilibre net') + '.');
      document.getElementById('power-readout').textContent = facts.join(' ') +
        ' Observation du ' + parisTime(latest.at) + (powerOld ? ' (archivée).' : '.');
      const fuels = [
        ['Nucléaire', 'nucleaire', '#8dc4f5'], ['Gaz', 'gaz', '#f1c984'],
        ['Éolien', 'eolien', '#78dda8'], ['Solaire', 'solaire', '#edaa75'],
        ['Hydraulique', 'hydraulique', '#82c8df'], ['Bioénergies', 'bioenergies', '#bba5ef'],
        ['Charbon', 'charbon', '#b7aa9d'], ['Fioul', 'fioul', '#d9a2a2']
      ].filter(([, key]) => Number.isFinite(latest[key]) && latest[key] >= 0);
      const total = fuels.reduce((sum, [,key]) => sum + latest[key], 0);
      const mix = document.getElementById('power-mix');
      mix.replaceChildren();
      if (total) {
        for (const [name, key, color] of fuels) {
          const row = line('', 'div', 'power-mix-row');
          row.append(line(name, 'span'));
          const track = line('', 'div', 'track');
          const bar = line('', 'i');
          bar.style.width = Math.max(0, Math.min(100, latest[key] / total * 100)) + '%';
          bar.style.background = color;
          track.append(bar);
          row.append(track, line(number(latest[key], 0), 'strong'));
          mix.append(row);
        }
        document.getElementById('power-mix-time').textContent = 'Mesure : ' + parisTime(latest.at) + ' · RTE.';
      } else mix.append(line('Répartition des filières indisponible.', 'span'));
      const observed = points.filter(row => Number.isFinite(row.load) &&
        Date.parse(row.at) >= measuredAt - 24 * 3600000);
      if (observed.length < 3) return;
      const residual = row => Number.isFinite(row.eolien) && Number.isFinite(row.solaire) ?
        row.load - row.eolien - row.solaire : null;
      const all = observed.flatMap(row => [row.load, residual(row)]).filter(Number.isFinite);
      const min = Math.floor(Math.min(...all) / 5000) * 5000;
      const max = Math.ceil(Math.max(...all) / 5000) * 5000;
      const start = Date.parse(observed[0].at), end = Date.parse(observed[observed.length - 1].at);
      if (max <= min || start === end) return;
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 600 225');
      svg.setAttribute('preserveAspectRatio', 'none');
      svg.setAttribute('class', 'power-chart');
      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-label', 'Puissance sur 24 heures : demande et demande résiduelle indicatives');
      for (const level of [0, .5, 1]) {
        const y = 200 - level * 180;
        const guide = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        for (const [key, value] of [['x1',0],['x2',600],['y1',y],['y2',y]])
          guide.setAttribute(key, String(value));
        svg.append(guide);
      }
      for (const [read, css] of [(row => row.load, 'demand-line'), (residual, 'residual-line')]) {
        const lineSvg = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
        lineSvg.setAttribute('class', css);
        lineSvg.setAttribute('points', observed.map(row => {
          const value = read(row);
          if (!Number.isFinite(value)) return null;
          return ((Date.parse(row.at) - start) / (end - start) * 600).toFixed(1) + ',' +
                 (200 - (value - min) / (max - min) * 180).toFixed(1);
        }).filter(Boolean).join(' '));
        svg.append(lineSvg);
      }
      document.getElementById('power-curve').replaceWith(svg);
      document.getElementById('power-axis').replaceChildren(
        line('● Demande · ' + parisTime(observed[0].at), 'span'),
        line('● Résiduelle indicative · ' + parisTime(observed[observed.length - 1].at), 'span'));
    }

    document.querySelectorAll('.filters button').forEach(button => button.addEventListener('click', () => {
      selectedSector = button.dataset.sector;
      renderSector();
    }));
    renderStatus();
    renderTicker();
    renderQuotes();
    renderWatch();
    renderAgenda();
    renderMini();
    renderReleases();
    renderStories();
    renderSector();
    renderPower();
  </script>
</body>
</html>

```
