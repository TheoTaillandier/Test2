# Commodity Cockpit

Tableau de bord personnel des matières premières. Dans l'onglet **Code**, ouvrir [`index.html`](index.html), cliquer sur **Raw** ou **Download raw file**, enregistrer le fichier en `.html`, puis l'ouvrir dans un navigateur. Le code HTML complet figure aussi ci-dessous.

Les cotations en séance Brent, WTI et gaz US sont des widgets TradingView/OANDA : elles demandent Internet et sont indicatives, distinctes du contrat ICE et de Henry Hub physique. Le spot officiel EIA est montré séparément avec sa date. Les autres chiffres officiels sont collectés par [la tâche planifiée](.github/workflows/update-data.yml). Le bouton **Actualiser les données** récupère la dernière publication GitHub même depuis un HTML téléchargé ; hors connexion, le fichier garde son instantané daté. L'onglet **Power FR** affiche RTE et, avec une clé ENTSO-E, les prévisions de demande France et DE-LU.

## Sources & automatisation

- EIA WPSR : stocks de brut, Cushing, Gulf Coast, essence, distillats, jet et SPR ; production, importations, exportations et brut traité par les raffineries US.
- EIA WNGSR : stockage de gaz US et régions, variation hebdomadaire et écart à la moyenne cinq ans.
- USDA WASDE : production, exportations prévues et stocks de maïs et soja US ; stocks mondiaux de maïs et blé, commerce mondial prévu du blé. Les révisions comparent les deux colonnes de prévision du même rapport.
- EIA Today in Energy : titres et résumés d'analyses récentes.
- Sodir (Norwegian Offshore Directorate) : chiffre mensuel provisoire d'août 2026 (pétrole, LGN et condensats), repère européen daté ; la source refuse actuellement les lectures automatisées du robot GitHub et ce chiffre n'est donc pas rafraîchi automatiquement.
- EIA, tableaux de prix spot quotidiens : Brent Europe, WTI Cushing et Henry Hub ; le collecteur vérifie la correspondance des six dates et six colonnes avant publication. Une série FRED de 12 mois compare les clôtures spot Brent et WTI, sans se substituer à la cotation en séance.
- GIE AGSI+ / ALSI : avec une clé API gratuite (accès aux **deux plateformes**), stockage gaz France/UE, soutirage net, stocks en cuves GNL et émissions des terminaux GNL France/UE. Ce sont des observations physiques quotidiennes, **pas des prix TTF, PEG ou JKM**. Créer la clé sur https://agsi.gie.eu/account, choisir accès AGSI + ALSI et enregistrer `GIE_API_KEY` dans Settings → Secrets and variables → Actions → New repository secret. Relancer le workflow depuis Actions. Sans clé, ces chiffres ne sont pas affichés.
- RTE éCO2mix national temps réel : [dataset officiel](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/) actualisé à la source au quart d'heure ; consommation, nucléaire, gaz, vent, solaire, hydraulique, bioénergies et échanges physiques. Export = solde négatif ; import = positif. Le cockpit collecte un instantané toutes les deux heures via GitHub Actions et indique l'heure de la mesure et de la collecte. Demande résiduelle = consommation − éolien − solaire (calcul indicatif, **pas une prévision du prix**). Aucun compte requis.
- ENTSO-E : prévision *day-ahead* de demande (A65/A01, Article 6.1.b, données [CC BY 4.0](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions)), France et Allemagne/Luxembourg ; affichage du pic prévu pour les prochaines 24 heures. Pour activer : créer un compte sur https://transparency.entsoe.eu/, demander l'accès API à `transparency@entsoe.eu` (objet `RESTful API access` et adresse enregistrée dans le corps), puis générer le jeton dans « My Account ». Enregistrer le jeton **uniquement** comme secret GitHub Actions `ENTSOE_API_TOKEN` via Settings → Secrets and variables → Actions → New repository secret ; relancer l'action. Ne jamais le coller dans le HTML, un fichier GitHub ou une conversation. Sans clé, RTE Power fonctionne déjà.
- Prix électriques France/DE : bouton vers le [marché officiel RTE](https://www.rte-france.com/en/data-publications/eco2mix/market-data) ; les prix day-ahead EPEX ne sont pas couverts par la [liste ENTSO-E de réutilisation libre](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions) et RTE interdit la copie de ses prix via éCO2mix. Le jeton ENTSO-E n'est pas un droit de redistribution de ces cotations.
- Calendrier natif : sorties EIA pétrole et gaz, USDA WASDE et STEO ; les exceptions 2026 connues sont incluses. Au-delà des dates vérifiées, le tableau l'indique sans inventer d'horaire.
- Marchés : cinq tuiles de cotations en séance TradingView/OANDA (Brent, WTI, gaz US, cuivre, or), plus un graphique et un tableau. Instruments OTC indicatifs ; ils ne remplacent ni les futures ICE/NYMEX ni le spot EIA daté. Le gaz US OANDA n'est pas une cotation Henry Hub physique. Les widgets nécessitent Internet et le fournisseur peut limiter la diffusion. Aluminium, cacao et café sont accessibles via leurs pages de marché ; leurs prix ne sont pas intégrés sans droits vérifiés.
- TTF/PEG/JKM : liens vers sources de marché ; un flux de cotations automatisé et redistribué publiquement nécessite un droit de diffusion. Aucune valeur ou spread instantané n'est inventé. ENTSO-E fournit des prévisions électriques ouvertes, ENTSOG des flux physiques de gaz, et GIE les stocks/terminaux.
- Physique : stockage AGSI France sur 400 observations et comparaison de 90 jours à l'année précédente, émission ALSI France sur 14 jours, stocks de brut EIA sur 26 semaines et comparaison Brent/WTI spot sur un an. Graphiques avec axes et unités. Les signaux de pression sont des scénarios conditionnels liés aux chiffres publiés, jamais un mouvement de prix constaté. FranceAgriMer Céré’Obs, USDA Crop Progress, Météo-France et NOAA sont liés dans Agriculture ; aucun état de culture n'est inventé si la source n'est pas collectée.
- LME : [rapports de stocks](https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports) à consulter, sans chiffre de stock automatisé tant qu'un flux stable n'est pas vérifié.

Unités : M bbl = millions de barils ; M bbl/j = millions de barils par jour ; Bcf = milliards de pieds cubes ; TWh = térawattheures ; GWh/j = gigawattheures par jour ; 10³ m³ GNL = milliers de mètres cubes de GNL liquide ; M bu = millions de boisseaux ; Mt = millions de tonnes. Stocks, prix et flux ne sont jamais additionnés.

Les clés restent dans les secrets GitHub et ne sont jamais insérées dans les fichiers publics. Le fichier HTML contient un instantané et s'ouvre directement après téléchargement. Il essaie aussi de synchroniser `data/snapshot.json` depuis GitHub à l'ouverture et via le bouton manuel, sous réserve du réseau et des règles du navigateur ; sinon la date de l'instantané reste visible. Les tâches GitHub planifiées peuvent être retardées ou désactivées après une longue période sans activité ; dans ce cas, l'onglet Actions permet la relance manuelle.

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
    .live-strip { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:8px; padding:10px 13px; }
    .live-tile { min-width:0; background:var(--surface); border:1px solid var(--border); border-radius:7px; padding:6px; }
    .live-tile small { display:block; color:var(--muted); font-size:10px; padding:2px 5px; }
    .live-tile .widget { height:72px; }
    .live-tile a { font-size:10px; padding:0 5px; }
    .live-caption { padding:0 14px 7px; color:var(--muted); font-size:10px; }
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
    .trend-key { display:flex; gap:15px; margin:4px 0; font-size:10px; color:var(--muted); }
    .trend-key i { display:inline-block; width:15px; height:2px; vertical-align:middle; margin-right:4px; background:var(--accent); }
    .trend-key i.secondary { background:var(--warm); }
    .chart-figure { width:100%; height:175px; }
    .chart-figure line { stroke:var(--border); }
    .chart-figure text { fill:var(--muted); font-size:10px; }
    .chart-figure polyline { fill:none; stroke:var(--accent); stroke-width:2; vector-effect:non-scaling-stroke; }
    .chart-figure polyline.secondary { stroke:var(--warm); }
    .context-note { padding:10px 13px; margin:10px 0; border-left:2px solid var(--warm); color:var(--muted); background:var(--surface-2); font-size:11px; }
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
      .live-strip { grid-template-columns:repeat(2,minmax(0,1fr)); }
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
    <div class="live-strip" id="live-strip" aria-label="Cotations en séance"></div>
    <div class="live-caption">Cotation indicative OANDA via TradingView, actualisée par le fournisseur en séance. Ce n’est pas le contrat Brent ICE. Vérifier l’heure et le délai chez le fournisseur avant toute décision.</div>
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
      <div class="page-intro"><div><h1>Intelligence du marché physique</h1><p>Chiffres officiels, variation, période mesurée et fraîcheur de chaque publication.</p></div><div><span class="stamp" id="updated">Chargement de l'instantané…</span> <button type="button" class="stamp" id="refresh-data">Actualiser les données ↻</button></div></div>
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
          <section><h2 class="section-heading" id="sector-heading">Pétrole · prix spot et stocks</h2><div class="chart-duo"><div class="card side-pad trend" id="trend" hidden><h3 id="trend-title">Stocks commerciaux de brut US · 26 semaines</h3><svg viewBox="0 0 400 110" preserveAspectRatio="none" role="img" aria-label="Évolution des stocks ou flux physiques"><polyline id="trend-line" points=""></polyline></svg><div class="axis"><span id="trend-start"></span><span id="trend-end"></span></div></div><div class="card side-pad trend" id="trend-two" hidden><h3 id="trend-two-title">Deuxième repère</h3><svg viewBox="0 0 400 110" preserveAspectRatio="none" role="img" aria-label="Historique du deuxième repère"><polyline id="trend-two-line" points=""></polyline></svg><div class="axis"><span id="trend-two-start"></span><span id="trend-two-end"></span></div></div></div><div id="comparison-chart" class="card side-pad trend" hidden></div><div id="sector-context" class="context-note"></div><h2 class="section-heading" style="margin-top:16px">Dernières mesures officielles</h2><div class="metrics" id="metrics"></div></section>
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
  "generated_at": "2026-09-28T05:24:56+00:00",
  "history": {
    "gas_eu": [
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
      },
      {
        "date": "2026-09-25",
        "value": 70.62
      },
      {
        "date": "2026-09-26",
        "value": 70.87
      }
    ],
    "gas_fr": [
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
      },
      {
        "date": "2026-09-25",
        "value": 81.97
      },
      {
        "date": "2026-09-26",
        "value": 82.47
      }
    ],
    "lng_eu_sendout": [
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
      },
      {
        "date": "2026-09-25",
        "value": 4105.2
      },
      {
        "date": "2026-09-26",
        "value": 3626.7
      }
    ],
    "lng_fr_sendout": [
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
      },
      {
        "date": "2026-09-25",
        "value": 1223.1
      },
      {
        "date": "2026-09-26",
        "value": 1185.0
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
        "at": "2026-09-27T05:15:00+00:00",
        "bioenergies": 1016,
        "charbon": 0,
        "ech_physiques": -7966,
        "eolien": 3161,
        "fioul": 37,
        "gaz": 238,
        "hydraulique": 2169,
        "load": 32261,
        "nucleaire": 34086,
        "pompage": -674,
        "prevision_j": 32500,
        "prevision_j1": 32300,
        "solaire": 179,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T05:30:00+00:00",
        "bioenergies": 1022,
        "charbon": 0,
        "ech_physiques": -8003,
        "eolien": 3247,
        "fioul": 37,
        "gaz": 237,
        "hydraulique": 2190,
        "load": 32288,
        "nucleaire": 34045,
        "pompage": -677,
        "prevision_j": 32600,
        "prevision_j1": 32400,
        "solaire": 178,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T05:45:00+00:00",
        "bioenergies": 1017,
        "charbon": 0,
        "ech_physiques": -8005,
        "eolien": 3313,
        "fioul": 37,
        "gaz": 244,
        "hydraulique": 2183,
        "load": 32303,
        "nucleaire": 33997,
        "pompage": -678,
        "prevision_j": 32800,
        "prevision_j1": 32650,
        "solaire": 195,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T06:00:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -8109,
        "eolien": 3433,
        "fioul": 37,
        "gaz": 244,
        "hydraulique": 2200,
        "load": 32535,
        "nucleaire": 33984,
        "pompage": -675,
        "prevision_j": 33000,
        "prevision_j1": 32900,
        "solaire": 405,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T06:15:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -7570,
        "eolien": 3549,
        "fioul": 37,
        "gaz": 245,
        "hydraulique": 2205,
        "load": 32882,
        "nucleaire": 33801,
        "pompage": -1246,
        "prevision_j": 33450,
        "prevision_j1": 33400,
        "solaire": 865,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T06:30:00+00:00",
        "bioenergies": 1010,
        "charbon": 0,
        "ech_physiques": -7357,
        "eolien": 3612,
        "fioul": 36,
        "gaz": 245,
        "hydraulique": 2106,
        "load": 33280,
        "nucleaire": 33708,
        "pompage": -1449,
        "prevision_j": 33900,
        "prevision_j1": 33900,
        "solaire": 1402,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T06:45:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -7225,
        "eolien": 3594,
        "fioul": 37,
        "gaz": 243,
        "hydraulique": 2069,
        "load": 33915,
        "nucleaire": 33485,
        "pompage": -1449,
        "prevision_j": 34150,
        "prevision_j1": 34200,
        "solaire": 2171,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T07:00:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -8201,
        "eolien": 3601,
        "fioul": 37,
        "gaz": 245,
        "hydraulique": 1949,
        "load": 33819,
        "nucleaire": 33675,
        "pompage": -1447,
        "prevision_j": 34400,
        "prevision_j1": 34500,
        "solaire": 2956,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T07:15:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -7902,
        "eolien": 3621,
        "fioul": 36,
        "gaz": 419,
        "hydraulique": 1757,
        "load": 34718,
        "nucleaire": 33404,
        "pompage": -1615,
        "prevision_j": 35200,
        "prevision_j1": 35300,
        "solaire": 4032,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T07:30:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -7937,
        "eolien": 3511,
        "fioul": 37,
        "gaz": 488,
        "hydraulique": 1735,
        "load": 35122,
        "nucleaire": 33090,
        "pompage": -1628,
        "prevision_j": 36000,
        "prevision_j1": 36100,
        "solaire": 5184,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T07:45:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -7545,
        "eolien": 3373,
        "fioul": 37,
        "gaz": 488,
        "hydraulique": 1657,
        "load": 35634,
        "nucleaire": 32562,
        "pompage": -1632,
        "prevision_j": 36500,
        "prevision_j1": 36650,
        "solaire": 6409,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T08:00:00+00:00",
        "bioenergies": 989,
        "charbon": 0,
        "ech_physiques": -6245,
        "eolien": 3148,
        "fioul": 37,
        "gaz": 495,
        "hydraulique": 1675,
        "load": 36147,
        "nucleaire": 31005,
        "pompage": -2040,
        "prevision_j": 37000,
        "prevision_j1": 37200,
        "solaire": 7829,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T08:15:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -5089,
        "eolien": 3043,
        "fioul": 36,
        "gaz": 495,
        "hydraulique": 1538,
        "load": 36659,
        "nucleaire": 30031,
        "pompage": -2457,
        "prevision_j": 37450,
        "prevision_j1": 38000,
        "solaire": 9059,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T08:30:00+00:00",
        "bioenergies": 993,
        "charbon": 0,
        "ech_physiques": -5181,
        "eolien": 2947,
        "fioul": 37,
        "gaz": 505,
        "hydraulique": 1542,
        "load": 37172,
        "nucleaire": 28695,
        "pompage": -2423,
        "prevision_j": 37900,
        "prevision_j1": 38800,
        "solaire": 10368,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T08:45:00+00:00",
        "bioenergies": 988,
        "charbon": 0,
        "ech_physiques": -4159,
        "eolien": 2793,
        "fioul": 37,
        "gaz": 507,
        "hydraulique": 1525,
        "load": 38023,
        "nucleaire": 27590,
        "pompage": -2662,
        "prevision_j": 38350,
        "prevision_j1": 39250,
        "solaire": 11476,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T09:00:00+00:00",
        "bioenergies": 989,
        "charbon": 0,
        "ech_physiques": -3308,
        "eolien": 2845,
        "fioul": 36,
        "gaz": 504,
        "hydraulique": 1528,
        "load": 38649,
        "nucleaire": 26411,
        "pompage": -2659,
        "prevision_j": 38800,
        "prevision_j1": 39700,
        "solaire": 12337,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T09:15:00+00:00",
        "bioenergies": 992,
        "charbon": 0,
        "ech_physiques": -3392,
        "eolien": 2935,
        "fioul": 36,
        "gaz": 498,
        "hydraulique": 1567,
        "load": 39470,
        "nucleaire": 25984,
        "pompage": -2659,
        "prevision_j": 38900,
        "prevision_j1": 40100,
        "solaire": 13527,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T09:30:00+00:00",
        "bioenergies": 990,
        "charbon": 0,
        "ech_physiques": -4119,
        "eolien": 3029,
        "fioul": 36,
        "gaz": 484,
        "hydraulique": 1545,
        "load": 39346,
        "nucleaire": 25893,
        "pompage": -2590,
        "prevision_j": 39000,
        "prevision_j1": 40500,
        "solaire": 14083,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T09:45:00+00:00",
        "bioenergies": 992,
        "charbon": 0,
        "ech_physiques": -4786,
        "eolien": 3093,
        "fioul": 37,
        "gaz": 492,
        "hydraulique": 1571,
        "load": 40176,
        "nucleaire": 25712,
        "pompage": -1952,
        "prevision_j": 39750,
        "prevision_j1": 41200,
        "solaire": 15064,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T10:00:00+00:00",
        "bioenergies": 990,
        "charbon": 0,
        "ech_physiques": -2928,
        "eolien": 2641,
        "fioul": 37,
        "gaz": 489,
        "hydraulique": 1624,
        "load": 40299,
        "nucleaire": 25910,
        "pompage": -1939,
        "prevision_j": 40500,
        "prevision_j1": 41900,
        "solaire": 12788,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T10:15:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -1351,
        "eolien": 2343,
        "fioul": 37,
        "gaz": 483,
        "hydraulique": 1602,
        "load": 40720,
        "nucleaire": 26101,
        "pompage": -1940,
        "prevision_j": 40600,
        "prevision_j1": 41950,
        "solaire": 12471,
        "taux_co2": 17
      },
      {
        "at": "2026-09-27T10:30:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -700,
        "eolien": 2451,
        "fioul": 36,
        "gaz": 473,
        "hydraulique": 1534,
        "load": 40917,
        "nucleaire": 25701,
        "pompage": -1942,
        "prevision_j": 40700,
        "prevision_j1": 42000,
        "solaire": 12519,
        "taux_co2": 17
      },
      {
        "at": "2026-09-27T10:45:00+00:00",
        "bioenergies": 1010,
        "charbon": 0,
        "ech_physiques": -441,
        "eolien": 2413,
        "fioul": 37,
        "gaz": 472,
        "hydraulique": 1555,
        "load": 41374,
        "nucleaire": 25711,
        "pompage": -2178,
        "prevision_j": 41100,
        "prevision_j1": 42400,
        "solaire": 12945,
        "taux_co2": 17
      },
      {
        "at": "2026-09-27T11:00:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": 329,
        "eolien": 2133,
        "fioul": 37,
        "gaz": 471,
        "hydraulique": 1577,
        "load": 41089,
        "nucleaire": 25736,
        "pompage": -2414,
        "prevision_j": 41500,
        "prevision_j1": 42800,
        "solaire": 12365,
        "taux_co2": 17
      },
      {
        "at": "2026-09-27T11:15:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": 839,
        "eolien": 1579,
        "fioul": 37,
        "gaz": 470,
        "hydraulique": 1582,
        "load": 39908,
        "nucleaire": 25920,
        "pompage": -2419,
        "prevision_j": 40550,
        "prevision_j1": 41850,
        "solaire": 11192,
        "taux_co2": 17
      },
      {
        "at": "2026-09-27T11:30:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": 984,
        "eolien": 1415,
        "fioul": 37,
        "gaz": 467,
        "hydraulique": 1550,
        "load": 39149,
        "nucleaire": 25754,
        "pompage": -2654,
        "prevision_j": 39600,
        "prevision_j1": 40900,
        "solaire": 10873,
        "taux_co2": 18
      },
      {
        "at": "2026-09-27T11:45:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -46,
        "eolien": 1359,
        "fioul": 37,
        "gaz": 264,
        "hydraulique": 1574,
        "load": 38297,
        "nucleaire": 26118,
        "pompage": -2648,
        "prevision_j": 39300,
        "prevision_j1": 40600,
        "solaire": 10811,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T12:00:00+00:00",
        "bioenergies": 1001,
        "charbon": 0,
        "ech_physiques": 120,
        "eolien": 1375,
        "fioul": 37,
        "gaz": 259,
        "hydraulique": 1623,
        "load": 38428,
        "nucleaire": 26370,
        "pompage": -2651,
        "prevision_j": 39000,
        "prevision_j1": 40300,
        "solaire": 10543,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T12:15:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": 310,
        "eolien": 1670,
        "fioul": 36,
        "gaz": 261,
        "hydraulique": 1630,
        "load": 39596,
        "nucleaire": 26305,
        "pompage": -2640,
        "prevision_j": 39500,
        "prevision_j1": 40800,
        "solaire": 11109,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T12:30:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": 539,
        "eolien": 1854,
        "fioul": 37,
        "gaz": 259,
        "hydraulique": 1671,
        "load": 39286,
        "nucleaire": 25750,
        "pompage": -2639,
        "prevision_j": 40000,
        "prevision_j1": 41300,
        "solaire": 10957,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T12:45:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": 12,
        "eolien": 2081,
        "fioul": 36,
        "gaz": 255,
        "hydraulique": 1811,
        "load": 39565,
        "nucleaire": 25860,
        "pompage": -2570,
        "prevision_j": 39700,
        "prevision_j1": 41000,
        "solaire": 11073,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T13:00:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -1030,
        "eolien": 2391,
        "fioul": 37,
        "gaz": 257,
        "hydraulique": 1919,
        "load": 39141,
        "nucleaire": 25899,
        "pompage": -2562,
        "prevision_j": 39400,
        "prevision_j1": 40700,
        "solaire": 11365,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T13:15:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -1871,
        "eolien": 3094,
        "fioul": 36,
        "gaz": 259,
        "hydraulique": 1941,
        "load": 39294,
        "nucleaire": 25631,
        "pompage": -2564,
        "prevision_j": 39150,
        "prevision_j1": 40450,
        "solaire": 11921,
        "taux_co2": 14
      },
      {
        "at": "2026-09-27T13:30:00+00:00",
        "bioenergies": 1004,
        "charbon": 0,
        "ech_physiques": -3817,
        "eolien": 3131,
        "fioul": 37,
        "gaz": 254,
        "hydraulique": 1978,
        "load": 38786,
        "nucleaire": 25913,
        "pompage": -2557,
        "prevision_j": 38900,
        "prevision_j1": 40200,
        "solaire": 12038,
        "taux_co2": 14
      },
      {
        "at": "2026-09-27T13:45:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -5920,
        "eolien": 4147,
        "fioul": 37,
        "gaz": 255,
        "hydraulique": 1909,
        "load": 38753,
        "nucleaire": 26121,
        "pompage": -2551,
        "prevision_j": 38650,
        "prevision_j1": 40000,
        "solaire": 14165,
        "taux_co2": 13
      },
      {
        "at": "2026-09-27T14:00:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -6016,
        "eolien": 4233,
        "fioul": 37,
        "gaz": 259,
        "hydraulique": 1874,
        "load": 38720,
        "nucleaire": 26544,
        "pompage": -2452,
        "prevision_j": 38400,
        "prevision_j1": 39800,
        "solaire": 13582,
        "taux_co2": 13
      },
      {
        "at": "2026-09-27T14:15:00+00:00",
        "bioenergies": 1010,
        "charbon": 0,
        "ech_physiques": -7089,
        "eolien": 4421,
        "fioul": 37,
        "gaz": 521,
        "hydraulique": 2232,
        "load": 38705,
        "nucleaire": 27464,
        "pompage": -2449,
        "prevision_j": 38100,
        "prevision_j1": 39500,
        "solaire": 12858,
        "taux_co2": 15
      },
      {
        "at": "2026-09-27T14:30:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -7654,
        "eolien": 4337,
        "fioul": 37,
        "gaz": 541,
        "hydraulique": 2374,
        "load": 38399,
        "nucleaire": 28450,
        "pompage": -2447,
        "prevision_j": 37800,
        "prevision_j1": 39200,
        "solaire": 11833,
        "taux_co2": 16
      },
      {
        "at": "2026-09-27T14:45:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -8015,
        "eolien": 4150,
        "fioul": 37,
        "gaz": 726,
        "hydraulique": 2306,
        "load": 38955,
        "nucleaire": 29315,
        "pompage": -1666,
        "prevision_j": 37750,
        "prevision_j1": 39150,
        "solaire": 11078,
        "taux_co2": 17
      },
      {
        "at": "2026-09-27T15:00:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -7519,
        "eolien": 4039,
        "fioul": 37,
        "gaz": 734,
        "hydraulique": 2332,
        "load": 39048,
        "nucleaire": 30323,
        "pompage": -1665,
        "prevision_j": 37700,
        "prevision_j1": 39100,
        "solaire": 9789,
        "taux_co2": 17
      },
      {
        "at": "2026-09-27T15:15:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -8151,
        "eolien": 3940,
        "fioul": 37,
        "gaz": 762,
        "hydraulique": 2600,
        "load": 39016,
        "nucleaire": 30821,
        "pompage": -720,
        "prevision_j": 38100,
        "prevision_j1": 39450,
        "solaire": 8701,
        "taux_co2": 18
      },
      {
        "at": "2026-09-27T15:30:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -8277,
        "eolien": 3746,
        "fioul": 37,
        "gaz": 1120,
        "hydraulique": 2757,
        "load": 39414,
        "nucleaire": 31881,
        "pompage": -487,
        "prevision_j": 38500,
        "prevision_j1": 39800,
        "solaire": 7347,
        "taux_co2": 21
      },
      {
        "at": "2026-09-27T15:45:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -6980,
        "eolien": 3432,
        "fioul": 37,
        "gaz": 1170,
        "hydraulique": 2978,
        "load": 40041,
        "nucleaire": 32362,
        "pompage": -489,
        "prevision_j": 39000,
        "prevision_j1": 40300,
        "solaire": 6355,
        "taux_co2": 22
      },
      {
        "at": "2026-09-27T16:00:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": -6086,
        "eolien": 3172,
        "fioul": 37,
        "gaz": 1178,
        "hydraulique": 3273,
        "load": 40337,
        "nucleaire": 32360,
        "pompage": 0,
        "prevision_j": 39500,
        "prevision_j1": 40800,
        "solaire": 5020,
        "taux_co2": 22
      },
      {
        "at": "2026-09-27T16:15:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": -5452,
        "eolien": 2908,
        "fioul": 37,
        "gaz": 1881,
        "hydraulique": 3921,
        "load": 41050,
        "nucleaire": 32510,
        "pompage": -1,
        "prevision_j": 39850,
        "prevision_j1": 41150,
        "solaire": 4030,
        "taux_co2": 29
      },
      {
        "at": "2026-09-27T16:30:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -5129,
        "eolien": 2817,
        "fioul": 37,
        "gaz": 2434,
        "hydraulique": 4623,
        "load": 41327,
        "nucleaire": 32422,
        "pompage": -1,
        "prevision_j": 40200,
        "prevision_j1": 41500,
        "solaire": 2948,
        "taux_co2": 34
      },
      {
        "at": "2026-09-27T16:45:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -3805,
        "eolien": 2553,
        "fioul": 37,
        "gaz": 2651,
        "hydraulique": 5413,
        "load": 42493,
        "nucleaire": 32492,
        "pompage": 0,
        "prevision_j": 41000,
        "prevision_j1": 42300,
        "solaire": 2119,
        "taux_co2": 36
      },
      {
        "at": "2026-09-27T17:00:00+00:00",
        "bioenergies": 1014,
        "charbon": 0,
        "ech_physiques": -2941,
        "eolien": 2404,
        "fioul": 37,
        "gaz": 2735,
        "hydraulique": 5668,
        "load": 42894,
        "nucleaire": 32593,
        "pompage": 0,
        "prevision_j": 41800,
        "prevision_j1": 43100,
        "solaire": 1371,
        "taux_co2": 37
      },
      {
        "at": "2026-09-27T17:15:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -2300,
        "eolien": 2321,
        "fioul": 37,
        "gaz": 2744,
        "hydraulique": 5760,
        "load": 43307,
        "nucleaire": 32539,
        "pompage": 0,
        "prevision_j": 42150,
        "prevision_j1": 43400,
        "solaire": 843,
        "taux_co2": 38
      },
      {
        "at": "2026-09-27T17:30:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -1460,
        "eolien": 2298,
        "fioul": 37,
        "gaz": 2760,
        "hydraulique": 5860,
        "load": 43621,
        "nucleaire": 32615,
        "pompage": 0,
        "prevision_j": 42500,
        "prevision_j1": 43700,
        "solaire": 513,
        "taux_co2": 38
      },
      {
        "at": "2026-09-27T17:45:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -575,
        "eolien": 2178,
        "fioul": 37,
        "gaz": 2764,
        "hydraulique": 5737,
        "load": 44171,
        "nucleaire": 32692,
        "pompage": 0,
        "prevision_j": 42650,
        "prevision_j1": 43850,
        "solaire": 335,
        "taux_co2": 38
      },
      {
        "at": "2026-09-27T18:00:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -257,
        "eolien": 2115,
        "fioul": 37,
        "gaz": 2825,
        "hydraulique": 5554,
        "load": 44188,
        "nucleaire": 32711,
        "pompage": -1,
        "prevision_j": 42800,
        "prevision_j1": 44000,
        "solaire": 225,
        "taux_co2": 39
      },
      {
        "at": "2026-09-27T18:15:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -460,
        "eolien": 2193,
        "fioul": 36,
        "gaz": 2860,
        "hydraulique": 5458,
        "load": 44152,
        "nucleaire": 32712,
        "pompage": -1,
        "prevision_j": 42600,
        "prevision_j1": 43700,
        "solaire": 201,
        "taux_co2": 39
      },
      {
        "at": "2026-09-27T18:30:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -583,
        "eolien": 2203,
        "fioul": 37,
        "gaz": 2874,
        "hydraulique": 4564,
        "load": 43062,
        "nucleaire": 32737,
        "pompage": -1,
        "prevision_j": 42400,
        "prevision_j1": 43400,
        "solaire": 198,
        "taux_co2": 40
      },
      {
        "at": "2026-09-27T18:45:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -1176,
        "eolien": 2334,
        "fioul": 37,
        "gaz": 2878,
        "hydraulique": 4426,
        "load": 42401,
        "nucleaire": 32753,
        "pompage": -1,
        "prevision_j": 42400,
        "prevision_j1": 42950,
        "solaire": 195,
        "taux_co2": 40
      },
      {
        "at": "2026-09-27T19:00:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -1350,
        "eolien": 2431,
        "fioul": 37,
        "gaz": 2765,
        "hydraulique": 4135,
        "load": 41955,
        "nucleaire": 32794,
        "pompage": -1,
        "prevision_j": 42400,
        "prevision_j1": 42500,
        "solaire": 193,
        "taux_co2": 40
      },
      {
        "at": "2026-09-27T19:15:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -1917,
        "eolien": 2441,
        "fioul": 37,
        "gaz": 2867,
        "hydraulique": 4015,
        "load": 41230,
        "nucleaire": 32783,
        "pompage": -1,
        "prevision_j": 41750,
        "prevision_j1": 41900,
        "solaire": 0,
        "taux_co2": 41
      },
      {
        "at": "2026-09-27T19:30:00+00:00",
        "bioenergies": 1001,
        "charbon": 0,
        "ech_physiques": -2107,
        "eolien": 2573,
        "fioul": 36,
        "gaz": 2558,
        "hydraulique": 3862,
        "load": 40699,
        "nucleaire": 32768,
        "pompage": 0,
        "prevision_j": 41100,
        "prevision_j1": 41300,
        "solaire": 0,
        "taux_co2": 38
      },
      {
        "at": "2026-09-27T19:45:00+00:00",
        "bioenergies": 1004,
        "charbon": 0,
        "ech_physiques": -2315,
        "eolien": 2493,
        "fioul": 37,
        "gaz": 2480,
        "hydraulique": 3704,
        "load": 40182,
        "nucleaire": 32793,
        "pompage": -23,
        "prevision_j": 40350,
        "prevision_j1": 40600,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-27T20:00:00+00:00",
        "bioenergies": 999,
        "charbon": 0,
        "ech_physiques": -2624,
        "eolien": 2509,
        "fioul": 36,
        "gaz": 2482,
        "hydraulique": 3800,
        "load": 39983,
        "nucleaire": 32812,
        "pompage": -29,
        "prevision_j": 39600,
        "prevision_j1": 39900,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-27T20:15:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -2506,
        "eolien": 2533,
        "fioul": 37,
        "gaz": 2486,
        "hydraulique": 3727,
        "load": 40057,
        "nucleaire": 32847,
        "pompage": -38,
        "prevision_j": 40000,
        "prevision_j1": 40200,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-27T20:30:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -1766,
        "eolien": 2519,
        "fioul": 37,
        "gaz": 2489,
        "hydraulique": 3431,
        "load": 40463,
        "nucleaire": 32807,
        "pompage": -27,
        "prevision_j": 40400,
        "prevision_j1": 40500,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-27T20:45:00+00:00",
        "bioenergies": 1002,
        "charbon": 0,
        "ech_physiques": -1051,
        "eolien": 2599,
        "fioul": 36,
        "gaz": 2490,
        "hydraulique": 3410,
        "load": 41264,
        "nucleaire": 32819,
        "pompage": -7,
        "prevision_j": 40800,
        "prevision_j1": 40850,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-27T21:00:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -1364,
        "eolien": 2718,
        "fioul": 37,
        "gaz": 2260,
        "hydraulique": 3194,
        "load": 40638,
        "nucleaire": 32842,
        "pompage": -10,
        "prevision_j": 41200,
        "prevision_j1": 41200,
        "solaire": 0,
        "taux_co2": 35
      },
      {
        "at": "2026-09-27T21:15:00+00:00",
        "bioenergies": 980,
        "charbon": 0,
        "ech_physiques": -1340,
        "eolien": 2765,
        "fioul": 37,
        "gaz": 2163,
        "hydraulique": 2982,
        "load": 40443,
        "nucleaire": 32871,
        "pompage": -9,
        "prevision_j": 40850,
        "prevision_j1": 40800,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-27T21:30:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -1778,
        "eolien": 2766,
        "fioul": 37,
        "gaz": 2105,
        "hydraulique": 2851,
        "load": 39805,
        "nucleaire": 32851,
        "pompage": -6,
        "prevision_j": 40500,
        "prevision_j1": 40400,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-27T21:45:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -1732,
        "eolien": 2731,
        "fioul": 37,
        "gaz": 2105,
        "hydraulique": 2845,
        "load": 39849,
        "nucleaire": 32879,
        "pompage": -10,
        "prevision_j": 40150,
        "prevision_j1": 39850,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-27T22:00:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -1594,
        "eolien": 2752,
        "fioul": 37,
        "gaz": 2102,
        "hydraulique": 2271,
        "load": 38741,
        "nucleaire": 32270,
        "pompage": -32,
        "prevision_j": 39800,
        "prevision_j1": 39300,
        "solaire": 0,
        "taux_co2": 35
      },
      {
        "at": "2026-09-27T22:15:00+00:00",
        "bioenergies": 1001,
        "charbon": 0,
        "ech_physiques": -1440,
        "eolien": 2740,
        "fioul": 37,
        "gaz": 1804,
        "hydraulique": 2359,
        "load": 39336,
        "nucleaire": 32894,
        "pompage": -55,
        "prevision_j": 38700,
        "prevision_j1": 38450,
        "solaire": 0,
        "taux_co2": 32
      },
      {
        "at": "2026-09-27T22:30:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -1802,
        "eolien": 2701,
        "fioul": 37,
        "gaz": 1472,
        "hydraulique": 2285,
        "load": 38133,
        "nucleaire": 32986,
        "pompage": -544,
        "prevision_j": 37600,
        "prevision_j1": 37600,
        "solaire": 0,
        "taux_co2": 28
      },
      {
        "at": "2026-09-27T22:45:00+00:00",
        "bioenergies": 999,
        "charbon": 0,
        "ech_physiques": -2312,
        "eolien": 2711,
        "fioul": 37,
        "gaz": 1221,
        "hydraulique": 2314,
        "load": 37022,
        "nucleaire": 33024,
        "pompage": -942,
        "prevision_j": 36950,
        "prevision_j1": 36950,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-27T23:00:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -2941,
        "eolien": 2662,
        "fioul": 36,
        "gaz": 1246,
        "hydraulique": 2389,
        "load": 36469,
        "nucleaire": 33048,
        "pompage": -935,
        "prevision_j": 36300,
        "prevision_j1": 36300,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-27T23:15:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -2632,
        "eolien": 2611,
        "fioul": 37,
        "gaz": 1373,
        "hydraulique": 2521,
        "load": 37083,
        "nucleaire": 33115,
        "pompage": -928,
        "prevision_j": 36350,
        "prevision_j1": 36350,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-27T23:30:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -3237,
        "eolien": 2561,
        "fioul": 36,
        "gaz": 1300,
        "hydraulique": 2493,
        "load": 36510,
        "nucleaire": 33132,
        "pompage": -755,
        "prevision_j": 36400,
        "prevision_j1": 36400,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-27T23:45:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -3653,
        "eolien": 2519,
        "fioul": 37,
        "gaz": 1293,
        "hydraulique": 2399,
        "load": 36178,
        "nucleaire": 33200,
        "pompage": -588,
        "prevision_j": 36050,
        "prevision_j1": 36050,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-28T00:00:00+00:00",
        "bioenergies": 1002,
        "charbon": 0,
        "ech_physiques": -3992,
        "eolien": 2435,
        "fioul": 37,
        "gaz": 1112,
        "hydraulique": 2397,
        "load": 35624,
        "nucleaire": 33258,
        "pompage": -596,
        "prevision_j": 35700,
        "prevision_j1": 35700,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-28T00:15:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -4445,
        "eolien": 2346,
        "fioul": 37,
        "gaz": 1385,
        "hydraulique": 2308,
        "load": 35583,
        "nucleaire": 33301,
        "pompage": -354,
        "prevision_j": 35100,
        "prevision_j1": 35100,
        "solaire": 0,
        "taux_co2": 28
      },
      {
        "at": "2026-09-28T00:30:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -5438,
        "eolien": 2193,
        "fioul": 37,
        "gaz": 1362,
        "hydraulique": 2280,
        "load": 34513,
        "nucleaire": 33457,
        "pompage": -358,
        "prevision_j": 34500,
        "prevision_j1": 34500,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-28T00:45:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -5810,
        "eolien": 2221,
        "fioul": 37,
        "gaz": 1310,
        "hydraulique": 2096,
        "load": 33960,
        "nucleaire": 33520,
        "pompage": -363,
        "prevision_j": 33950,
        "prevision_j1": 33950,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-28T01:00:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -6625,
        "eolien": 2369,
        "fioul": 37,
        "gaz": 1266,
        "hydraulique": 2015,
        "load": 33306,
        "nucleaire": 33629,
        "pompage": -361,
        "prevision_j": 33400,
        "prevision_j1": 33400,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-28T01:15:00+00:00",
        "bioenergies": 1002,
        "charbon": 0,
        "ech_physiques": -7123,
        "eolien": 2324,
        "fioul": 37,
        "gaz": 1367,
        "hydraulique": 2016,
        "load": 32955,
        "nucleaire": 33725,
        "pompage": -361,
        "prevision_j": 33050,
        "prevision_j1": 33050,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-28T01:30:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -7508,
        "eolien": 2369,
        "fioul": 37,
        "gaz": 1378,
        "hydraulique": 2019,
        "load": 32692,
        "nucleaire": 33797,
        "pompage": -356,
        "prevision_j": 32700,
        "prevision_j1": 32700,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-28T01:45:00+00:00",
        "bioenergies": 993,
        "charbon": 0,
        "ech_physiques": -7483,
        "eolien": 2397,
        "fioul": 37,
        "gaz": 1371,
        "hydraulique": 2068,
        "load": 32739,
        "nucleaire": 33903,
        "pompage": -361,
        "prevision_j": 32700,
        "prevision_j1": 32550,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-28T02:00:00+00:00",
        "bioenergies": 993,
        "charbon": 0,
        "ech_physiques": -7559,
        "eolien": 2482,
        "fioul": 37,
        "gaz": 1311,
        "hydraulique": 2064,
        "load": 32268,
        "nucleaire": 33641,
        "pompage": -361,
        "prevision_j": 32700,
        "prevision_j1": 32400,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-28T02:15:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -7829,
        "eolien": 2643,
        "fioul": 37,
        "gaz": 1061,
        "hydraulique": 2164,
        "load": 32445,
        "nucleaire": 33862,
        "pompage": -193,
        "prevision_j": 32800,
        "prevision_j1": 32500,
        "solaire": 0,
        "taux_co2": 24
      },
      {
        "at": "2026-09-28T02:30:00+00:00",
        "bioenergies": 992,
        "charbon": 0,
        "ech_physiques": -8450,
        "eolien": 2710,
        "fioul": 37,
        "gaz": 1321,
        "hydraulique": 2179,
        "load": 32347,
        "nucleaire": 33873,
        "pompage": -195,
        "prevision_j": 32900,
        "prevision_j1": 32600,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-28T02:45:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -8405,
        "eolien": 2800,
        "fioul": 37,
        "gaz": 1347,
        "hydraulique": 2257,
        "load": 32640,
        "nucleaire": 33875,
        "pompage": -195,
        "prevision_j": 33200,
        "prevision_j1": 32950,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-28T03:00:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -8078,
        "eolien": 2886,
        "fioul": 37,
        "gaz": 1185,
        "hydraulique": 2327,
        "load": 32982,
        "nucleaire": 33910,
        "pompage": -190,
        "prevision_j": 33500,
        "prevision_j1": 33300,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-28T03:15:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -7743,
        "eolien": 2988,
        "fioul": 37,
        "gaz": 1468,
        "hydraulique": 2309,
        "load": 33851,
        "nucleaire": 34052,
        "pompage": -188,
        "prevision_j": 34150,
        "prevision_j1": 33950,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-28T03:30:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -8672,
        "eolien": 3020,
        "fioul": 36,
        "gaz": 2480,
        "hydraulique": 2475,
        "load": 34740,
        "nucleaire": 34441,
        "pompage": -16,
        "prevision_j": 34800,
        "prevision_j1": 34600,
        "solaire": 0,
        "taux_co2": 36
      },
      {
        "at": "2026-09-28T03:45:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -9066,
        "eolien": 3044,
        "fioul": 37,
        "gaz": 3283,
        "hydraulique": 2549,
        "load": 35340,
        "nucleaire": 34546,
        "pompage": -20,
        "prevision_j": 35700,
        "prevision_j1": 35550,
        "solaire": 0,
        "taux_co2": 43
      },
      {
        "at": "2026-09-28T04:00:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -8630,
        "eolien": 3125,
        "fioul": 36,
        "gaz": 3551,
        "hydraulique": 2608,
        "load": 36182,
        "nucleaire": 34534,
        "pompage": -19,
        "prevision_j": 36600,
        "prevision_j1": 36500,
        "solaire": 0,
        "taux_co2": 45
      },
      {
        "at": "2026-09-28T04:15:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -7606,
        "eolien": 2913,
        "fioul": 37,
        "gaz": 3729,
        "hydraulique": 3009,
        "load": 37737,
        "nucleaire": 34563,
        "pompage": -20,
        "prevision_j": 37800,
        "prevision_j1": 37700,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-28T04:30:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -7480,
        "eolien": 2843,
        "fioul": 37,
        "gaz": 3913,
        "hydraulique": 3635,
        "load": 38583,
        "nucleaire": 34557,
        "pompage": -20,
        "prevision_j": 39000,
        "prevision_j1": 38900,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-28T04:45:00+00:00",
        "bioenergies": 993,
        "charbon": 0,
        "ech_physiques": -7269,
        "eolien": 2806,
        "fioul": 37,
        "gaz": 3932,
        "hydraulique": 5019,
        "load": 40092,
        "nucleaire": 34561,
        "pompage": 0,
        "prevision_j": 40200,
        "prevision_j1": 40150,
        "solaire": 0,
        "taux_co2": 46
      },
      {
        "at": "2026-09-28T05:00:00+00:00",
        "bioenergies": 990,
        "charbon": 0,
        "ech_physiques": -7052,
        "eolien": 2869,
        "fioul": 37,
        "gaz": 3982,
        "hydraulique": 5797,
        "load": 41389,
        "nucleaire": 34563,
        "pompage": 0,
        "prevision_j": 41400,
        "prevision_j1": 41400,
        "solaire": 199,
        "taux_co2": 46
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
      "as_of": "2026-09-28",
      "change": 5207,
      "comparison": "vs ~1 h",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_load",
      "label": "Demande France",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 41389
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "export si négatif · import si positif",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_exchange",
      "label": "Solde des échanges physiques",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -7052
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_nucleaire",
      "label": "Nucléaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 34563
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_gaz",
      "label": "Gaz électrique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 3982
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_eolien",
      "label": "Éolien",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 2869
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_solaire",
      "label": "Solaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 199
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_hydraulique",
      "label": "Hydraulique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 5797
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_bioenergies",
      "label": "Bioénergies",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 990
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "demande − éolien − solaire",
      "detail": "Calcul indicatif, sans jugement sur le prix ni l'appel au gaz. Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_residual",
      "label": "Demande résiduelle indicative",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 38321
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "production française",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_carbon",
      "label": "Intensité CO₂ estimée",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "g/kWh",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 46
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "réalisé − prévision réactualisée le jour même",
      "detail": "Observation 2026-09-28T05:00:00+00:00 UTC",
      "id": "power_load_gap",
      "label": "Écart à prévision de demande J",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -11
    },
    {
      "as_of": "2026-09-26",
      "change": 0.25,
      "comparison": "points vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu",
      "label": "Stockage gaz UE · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 70.87
    },
    {
      "as_of": "2026-09-26",
      "change": 2.875,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_twh",
      "label": "Gaz stocké UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 801.992
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_net",
      "label": "Soutirage net UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -2831.3
    },
    {
      "as_of": "2026-09-26",
      "change": 0.5,
      "comparison": "points vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr",
      "label": "Stockage gaz France · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 82.47
    },
    {
      "as_of": "2026-09-26",
      "change": 0.618,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_twh",
      "label": "Gaz stocké France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 102.164
    },
    {
      "as_of": "2026-09-26",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_net",
      "label": "Soutirage net France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -618.0
    },
    {
      "as_of": "2026-09-26",
      "change": 69.18,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "lng_eu_inventory",
      "label": "GNL en cuves UE",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "10³ m³ GNL",
      "url": "https://alsi.gie.eu/",
      "value": 4049.77
    },
    {
      "as_of": "2026-09-26",
      "change": -478.5,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "lng_eu_sendout",
      "label": "Émission terminaux GNL UE",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "GWh/j",
      "url": "https://alsi.gie.eu/",
      "value": 3626.7
    },
    {
      "as_of": "2026-09-26",
      "change": 128.81,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "lng_fr_inventory",
      "label": "GNL en cuves France",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "10³ m³ GNL",
      "url": "https://alsi.gie.eu/",
      "value": 708.29
    },
    {
      "as_of": "2026-09-26",
      "change": -38.1,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "lng_fr_sendout",
      "label": "Émission terminaux GNL France",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "GWh/j",
      "url": "https://alsi.gie.eu/",
      "value": 1185.0
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "prévision J-1, 24 h glissantes",
      "detail": "Pic prévu à 2026-09-28T17:30:00+00:00 UTC",
      "id": "power_forecast_fr",
      "label": "Pic prévu 24 h · France",
      "sector": "power",
      "source": "ENTSO-E · prévision J-1",
      "unit": "MW",
      "url": "https://transparency.entsoe.eu/",
      "value": 48900
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "prévision J-1, 24 h glissantes",
      "detail": "Pic prévu à 2026-09-28T07:45:00+00:00 UTC",
      "id": "power_forecast_de",
      "label": "Pic prévu 24 h · Allemagne/Luxembourg",
      "sector": "power",
      "source": "ENTSO-E · prévision J-1",
      "unit": "MW",
      "url": "https://transparency.entsoe.eu/",
      "value": 62456
    }
  ],
  "schema": 3,
  "sources": {
    "alsi": {
      "as_of": "2026-09-26",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://alsi.gie.eu/"
    },
    "alsi_fr": {
      "as_of": "2026-09-26",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://alsi.gie.eu/"
    },
    "brent": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm"
    },
    "entsoe_de": {
      "as_of": "2026-09-28T07:45:00+00:00",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://transparency.entsoe.eu/"
    },
    "entsoe_fr": {
      "as_of": "2026-09-28T17:30:00+00:00",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://transparency.entsoe.eu/"
    },
    "gas": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://ir.eia.gov/ngs/ngs.html"
    },
    "gie": {
      "as_of": "2026-09-26",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "gie_fr": {
      "as_of": "2026-09-26",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "henry": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-28T05:24:56+00:00",
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
      "checked_at": "2026-09-28T05:24:56+00:00",
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
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_flows": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_history": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "published": "2026-09-23",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "rte_power": {
      "as_of": "2026-09-28T05:00:00+00:00",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/"
    },
    "wasde": {
      "as_of": "2026-09",
      "checked_at": "2026-09-28T05:24:56+00:00",
      "status": "ok",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt"
    },
    "wti": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-28T05:24:56+00:00",
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
    let snapshot = JSON.parse(document.getElementById('snapshot-data').textContent);
    let metrics = Array.isArray(snapshot.metrics) ? snapshot.metrics : [];
    let byId = Object.fromEntries(metrics.map(item => [item.id, item]));
    const sectors = {oil: 'Pétrole · cotations séparées des mesures physiques', gas: 'Gaz · France, Europe, GNL et États-Unis',
      agri: 'Agriculture · bilans USDA et état des cultures', metals: 'Métaux · offre, demande et stocks'};
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
      const explanations = {
        oil_crude:'Stocks US en baisse : moins de barils disponibles, signal à confronter aux importations et aux raffineries.',
        oil_cushing:'Cushing est le point de livraison du WTI : une baisse locale peut compter davantage pour le WTI que pour le Brent.',
        oil_norway_liquids:'Production mensuelle de pétrole et liquides en mer du Nord : un repère d’offre, avec publication différée.',
        gas_fr:'Niveau de remplissage, à interpréter par rapport à la saison et à l’année précédente.',
        gas_fr_net:'Positif = soutirage du stockage ; négatif = injection. Un débit quotidien, pas un prix.',
        lng_fr_sendout:'Quantité de gaz issue des terminaux et envoyée au réseau français chaque jour.',
        ag_corn_stocks:'Stocks de fin de campagne prévus : moins de stocks rendent le marché plus sensible aux aléas de récolte.',
        ag_world_wheat:'Stocks mondiaux prévus ; vérifier aussi la part exportable avant de conclure sur MATIF.',
        metal_copper:'Tonnage minier annuel : aucune conclusion de court terme sans inventaires et demande.'
      };
      if (explanations[item.id]) card.append(line(explanations[item.id], 'div', 'detail'));
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
        card.append(line(period(item.as_of) + ' · ' + changeText(item) + (stale(item) ? ' · archive' : ''), 'span'));
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
    function renderLive() {
      const box = document.getElementById('live-strip');
      const quotes = [
        ['Brent · indicatif', 'OANDA:BCOUSD', 'https://www.tradingview.com/symbols/BCOUSD/?exchange=OANDA'],
        ['WTI · indicatif', 'OANDA:WTICOUSD', 'https://www.tradingview.com/symbols/WTICOUSD/?exchange=OANDA'],
        ['Gaz US · indicatif', 'OANDA:NATGASUSD', 'https://www.tradingview.com/symbols/NATGASUSD/?exchange=OANDA'],
        ['Cuivre · indicatif', 'OANDA:XCUUSD', 'https://www.tradingview.com/symbols/XCUUSD/?exchange=OANDA'],
        ['Or · indicatif', 'OANDA:XAUUSD', 'https://www.tradingview.com/symbols/XAUUSD/?exchange=OANDA']
      ];
      for (const [name, symbol, href] of quotes) {
        const tile = line('', 'article', 'live-tile');
        tile.append(line(name, 'small'));
        const widget = line('Chargement du cours…', 'div', 'widget');
        tile.append(widget);
        const link = line('Source, horaire et délai ↗', 'a');
        link.href = href; link.target = '_blank'; link.rel = 'noopener noreferrer';
        tile.append(link); box.append(tile);
        embed(widget, 'https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js',
          {symbol,width:'100%',locale:'fr',colorTheme:'dark',isTransparent:true});
      }
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
      renderComparison(history);
    }

    function renderComparison(history) {
      const card = document.getElementById('comparison-chart');
      card.replaceChildren();
      let title, a, b, unit, note;
      if (selectedSector === 'oil' && history.oil_prices) {
        title = 'Brent vs WTI · 12 mois · clôtures spot officielles';
        a = history.oil_prices.brent || []; b = history.oil_prices.wti || [];
        unit = '$/bbl';
        note = 'Séries EIA via FRED, publiées avec retard. Ce graphique historique ne remplace pas la cotation en séance au-dessus.';
      } else if (selectedSector === 'gas' && Array.isArray(history.gas_fr)) {
        title = 'Stockage France · 90 derniers jours vs mêmes dates N−1';
        const all = history.gas_fr;
        a = all.slice(-90);
        const byDay = new Map(all.map(point => [point.date, point]));
        b = a.map(point => byDay.get(String(Number(point.date.slice(0, 4)) - 1) + point.date.slice(4)))
          .filter(Boolean);
        unit = '% plein';
        note = 'Comparer au même moment de l’année évite de confondre remplissage saisonnier et tension exceptionnelle.';
      } else { card.hidden = true; return; }
      if (a.length < 5 || b.length < 5) { card.hidden = true; return; }
      card.hidden = false;
      card.append(line(title, 'h3'));
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 640 175');
      svg.setAttribute('preserveAspectRatio', 'none');
      svg.setAttribute('class', 'chart-figure');
      svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', title + ' en ' + unit);
      const allValues = [...a, ...b].map(point => point.value).filter(Number.isFinite);
      const low = Math.floor(Math.min(...allValues) / 5) * 5;
      const high = Math.ceil(Math.max(...allValues) / 5) * 5 + (Math.max(...allValues) === low ? 5 : 0);
      const first = Date.parse(a[0].date), last = Date.parse(a[a.length - 1].date);
      const element = (tag, attrs) => {
        const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
        svg.append(node); return node;
      };
      for (let i = 0; i <= 4; i++) {
        const y = 147 - i * 33;
        element('line', {x1:45,x2:633,y1:y,y2:y});
        element('text', {x:2,y:y+3}).textContent = number(low + (high-low)*i/4, 0);
      }
      const path = (points, secondary, shiftYear) => points.map(point => {
        const date = shiftYear ? String(Number(point.date.slice(0,4)) + 1) + point.date.slice(4) : point.date;
        const x = 45 + 588 * (Date.parse(date) - first) / Math.max(1, last-first);
        const y = 147 - 132 * (point.value - low) / (high-low);
        return x.toFixed(1) + ',' + y.toFixed(1);
      }).join(' ');
      element('polyline', {points:path(a),class:'primary'});
      element('polyline', {points:path(b,true,selectedSector === 'gas'),class:'secondary'});
      card.append(svg);
      const legend = line('', 'div', 'trend-key');
      for (const [label, cls] of [[selectedSector === 'gas' ? 'Cette année' : 'Brent', ''],
                                  [selectedSector === 'gas' ? 'Année précédente' : 'WTI', 'secondary']]) {
        const span = line(label, 'span'); const marker = line('', 'i', cls); span.prepend(marker); legend.append(span);
      }
      card.append(legend);
      card.append(line(period(a[0].date) + ' → ' + period(a[a.length-1].date) + ' · axe : ' + unit, 'small'));
      card.append(line(note, 'p', 'detail'));
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
      const context = document.getElementById('sector-context');
      const notes = {
        oil: 'Stocks US : variation hebdomadaire, pertinente surtout pour le WTI. Production norvégienne : repère européen mensuel, pétrole et liquides confondus. Le Brent en séance figure dans Marchés ; le spot EIA ci-dessous est daté.',
        gas: 'Un remplissage quotidien positif en septembre est normal. Compare les stocks France à la même saison l’an dernier, puis les émissions GNL et le soutirage net. Le prix PEG/TTF peut réagir à d’autres nouvelles en même temps.',
        agri: 'USDA WASDE mesure l’offre et la demande prévues : moins de stocks finaux tend à soutenir les prix, toutes choses égales par ailleurs. Suivre la météo et les cultures avant le prochain rapport : FranceAgriMer Céré’Obs (France) et USDA Crop Progress (US).',
        metals: 'La production minière annuelle décrit l’offre structurelle, pas la tension du jour. Pour interpréter le cuivre ou l’aluminium, rapprocher inventaires LME, production et demande industrielle ; aucune variation de prix immédiate ne se déduit du seul tonnage.'
      };
      context.textContent = notes[selectedSector];
      const references = selectedSector === 'agri' ? [
        ['FranceAgriMer · Céré’Obs ↗','https://cereobs.franceagrimer.fr/'],
        ['USDA · Crop Progress ↗','https://www.nass.usda.gov/Publications/National_Crop_Progress/'],
        ['Météo-France · bulletins agricoles ↗','https://meteofrance.com/actualites-et-dossiers/actualites/climat'],
        ['NOAA · suivi sécheresse US ↗','https://www.drought.gov/']
      ] : selectedSector === 'metals' ? [
        ['LME · inventaires entrepôts ↗','https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports'],
        ['USGS · fiches métaux ↗','https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries']
      ] : [];
      for (const [label, href] of references) {
        const link = line(label, 'a'); link.href = href;
        link.target = '_blank'; link.rel = 'noopener noreferrer';
        context.append(' · ',link);
      }
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
        const tick = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        tick.setAttribute('x','5'); tick.setAttribute('y',String(y-4));
        tick.setAttribute('fill','#a4b9ab'); tick.setAttribute('font-size','11');
        tick.textContent = number(min + level * (max-min),0) + ' MW';
        svg.append(tick);
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
      document.getElementById('power-curve').replaceChildren(svg);
      document.getElementById('power-axis').replaceChildren(
        line('● Demande · ' + parisTime(observed[0].at), 'span'),
        line('● Résiduelle indicative · ' + parisTime(observed[observed.length - 1].at), 'span'));
    }

    document.querySelectorAll('.filters button').forEach(button => button.addEventListener('click', () => {
      selectedSector = button.dataset.sector;
      renderSector();
    }));
    function refreshPanels() {
      for (const id of ['source-status','watch-list','agenda','mini-grid','stories',
                         'signals','metrics','power-grid','power-mix','power-forecast'])
        document.getElementById(id).replaceChildren();
      document.getElementById('release-list').replaceChildren(line('Dernières publications vérifiées','h3'));
      const curve = document.getElementById('power-curve');
      curve.replaceChildren(line('Collecte RTE en attente.','span'));
      for (const fn of [renderStatus,renderWatch,renderAgenda,renderMini,renderReleases,
                        renderStories,renderSector,renderPower]) {
        try { fn(); } catch (error) { console.error('Panneau indisponible :', fn.name, error); }
      }
    }
    renderLive();
    renderQuotes();
    refreshPanels();
    async function refreshSnapshot() {
      const button = document.getElementById('refresh-data');
      button.disabled = true; button.textContent = 'Synchronisation…';
      try {
        const url = 'https://raw.githubusercontent.com/TheoTaillandier/Test2/main/data/snapshot.json?t=' + Date.now();
        const response = await fetch(url, {cache:'no-store'});
        if (!response.ok) throw new Error('HTTP ' + response.status);
        const next = await response.json();
        if (!next.generated_at || !Array.isArray(next.metrics) || !next.history ||
            Date.parse(next.generated_at) <= Date.parse(snapshot.generated_at || 0)) {
          button.textContent = 'Données déjà à jour'; return;
        }
        snapshot = next; metrics = next.metrics;
        byId = Object.fromEntries(metrics.map(item => [item.id,item]));
        refreshPanels();
        button.textContent = 'Données synchronisées';
      } catch (error) {
        button.textContent = 'Hors connexion · instantané daté';
        console.warn('Synchronisation impossible :', error);
      } finally { button.disabled = false; }
    }
    document.getElementById('refresh-data').addEventListener('click', refreshSnapshot);
    refreshSnapshot();
  </script>
</body>
</html>

```
