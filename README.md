# Commodity Cockpit

Tableau de bord personnel des matières premières. Dans l'onglet **Code**, ouvrir [`index.html`](index.html), cliquer sur **Raw** ou **Download raw file**, enregistrer le fichier en `.html`, puis l'ouvrir dans un navigateur. Le code HTML complet figure aussi ci-dessous.

Les cotations en séance Brent, WTI et gaz US sont des widgets TradingView/OANDA : elles demandent Internet et sont indicatives, distinctes du contrat ICE et de Henry Hub physique. Le spot officiel EIA est montré séparément avec sa date. Les autres chiffres officiels sont collectés par [la tâche planifiée](.github/workflows/update-data.yml). Le bouton **Actualiser les données** récupère la dernière publication GitHub même depuis un HTML téléchargé ; hors connexion, le fichier garde son instantané daté. L'onglet **Power FR** affiche RTE et, avec une clé ENTSO-E, les prévisions de demande France et DE-LU. [Méthodologie, unités et limites](methodology.md).

## Sources & automatisation

- EIA WPSR : stocks de brut, Cushing, Gulf Coast, essence, distillats, jet et SPR ; production, importations, exportations et brut traité par les raffineries US.
- EIA WNGSR : stockage de gaz US et régions, variation hebdomadaire et écart à la moyenne cinq ans.
- USDA WASDE : production, exportations prévues et stocks de maïs et soja US ; stocks mondiaux de maïs et blé, commerce mondial prévu du blé. Les révisions comparent les deux colonnes de prévision du même rapport.
- USDA NASS Crop Progress : état bon/excellent du maïs et du soja US comparé à la même semaine N−1, avancement de récolte comparé à la moyenne cinq ans ; rapport hebdomadaire en saison, daté et validé avant publication. Les liens FranceAgriMer et météo restent des sources à consulter, pas des observations inventées.
- EIA Today in Energy : titres et résumés d'analyses récentes.
- Sodir (Norwegian Offshore Directorate) : chiffre mensuel provisoire d'août 2026 (pétrole, LGN et condensats), repère européen daté ; la source refuse actuellement les lectures automatisées du robot GitHub et ce chiffre n'est donc pas rafraîchi automatiquement.
- EIA, tableaux de prix spot quotidiens : Brent Europe, WTI Cushing et Henry Hub ; le collecteur vérifie la correspondance des six dates et six colonnes avant publication. Une série de 12 mois compare les clôtures spot Brent et WTI : FRED, puis miroir public EIA `datasets/oil-prices` si FRED est indisponible, avec date et provenance explicites ; elle ne se substitue pas à la cotation en séance.
- GIE AGSI+ / ALSI : avec une clé API gratuite (accès aux **deux plateformes**), stockage gaz France/UE, soutirage net, stocks en cuves GNL et émissions des terminaux GNL France/UE. Ce sont des observations physiques quotidiennes, **pas des prix TTF, PEG ou JKM**. Créer la clé sur https://agsi.gie.eu/account, choisir accès AGSI + ALSI et enregistrer `GIE_API_KEY` dans Settings → Secrets and variables → Actions → New repository secret. Relancer le workflow depuis Actions. Sans clé, ces chiffres ne sont pas affichés.
- RTE éCO2mix national temps réel : [dataset officiel](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/) actualisé à la source au quart d'heure ; consommation, nucléaire, gaz, vent, solaire, hydraulique, bioénergies et échanges physiques. Export = solde négatif ; import = positif. Le cockpit collecte les dernières pages toutes les deux heures et conserve le dernier relevé de chaque heure dans `data/power_fr.json` sur 365 jours glissants. L'historique s'accumule depuis la première collecte, il n'invente pas une année déjà acquise. Il est aussi embarqué dans le HTML téléchargé. Demande résiduelle = consommation − éolien − solaire (calcul indicatif, **pas une prévision du prix**). Aucun compte requis.
- ENTSO-E : prévision *day-ahead* de demande (A65/A01, Article 6.1.b, données [CC BY 4.0](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions)), France et Allemagne/Luxembourg ; affichage du pic prévu pour les prochaines 24 heures. Pour activer : créer un compte sur https://transparency.entsoe.eu/, demander l'accès API à `transparency@entsoe.eu` (objet `RESTful API access` et adresse enregistrée dans le corps), puis générer le jeton dans « My Account ». Enregistrer le jeton **uniquement** comme secret GitHub Actions `ENTSOE_API_TOKEN` via Settings → Secrets and variables → Actions → New repository secret ; relancer l'action. Ne jamais le coller dans le HTML, un fichier GitHub ou une conversation. Sans clé, RTE Power fonctionne déjà.
- Prix day-ahead France et DE-LU : API Fraunhofer ISE Energy-Charts. Le collecteur exige explicitement la mention de licence CC BY 4.0 dans chaque réponse et une unité EUR/MWh ; sinon il refuse la publication. L'attribution exacte déclarée par la réponse (actuellement Bundesnetzagentur / SMARD) accompagne les chiffres. `data/power_prices.json` conserve un historique glissant d'un an à partir des points réellement collectés. Le prix porte sur la **livraison** de chaque quart d'heure ou heure, il a été fixé la veille ; ce n'est pas un cours intraday en direct. Source et transformation sont affichées.
- Intraday continu France : [page de marché EPEX](https://www.epexspot.com/en/market-results) et [RTE](https://www.rte-france.com/en/data-publications/eco2mix/market-data) en accès direct. ENTSO-E 12.1.d rend obligatoire le day-ahead et l'intraday facultatif. RTE interdit la récupération des prix affichés dans éCO2mix et EPEX vend son flux de données ; le site ne fabrique donc pas un spread day-ahead/intraday. Les données de prix Fraunhofer sont attribuées conformément à la licence déclarée dans l'API.
- Calendrier natif : sorties EIA pétrole et gaz, USDA WASDE et STEO ; les exceptions 2026 connues sont incluses. Au-delà des dates vérifiées, le tableau l'indique sans inventer d'horaire.
- Marchés : cinq tuiles de cotations en séance TradingView/OANDA (Brent, WTI, gaz US, cuivre, or), plus un graphique et un tableau. Instruments OTC indicatifs ; ils ne remplacent ni les futures ICE/NYMEX ni le spot EIA daté. Le gaz US OANDA n'est pas une cotation Henry Hub physique. Les widgets nécessitent Internet et le fournisseur peut limiter la diffusion. Aluminium, cacao et café sont accessibles via leurs pages de marché ; leurs prix ne sont pas intégrés sans droits vérifiés.
- TTF/PEG/JKM : liens vers sources de marché ; un flux de cotations automatisé et redistribué publiquement nécessite un droit de diffusion. Aucune valeur ou spread instantané n'est inventé. ENTSO-E fournit des prévisions électriques ouvertes, ENTSOG des flux physiques de gaz, et GIE les stocks/terminaux.
- Physique : stockage AGSI France sur deux pages de 300 observations et comparaison de 90 jours à l'année précédente, émission ALSI France sur 14 jours, stocks de brut EIA sur 26 semaines et comparaison Brent/WTI spot sur un an lorsque FRED répond. Graphiques avec axes et unités. Les signaux de pression sont des scénarios conditionnels liés aux chiffres publiés, jamais un mouvement de prix constaté. FranceAgriMer Céré’Obs, USDA Crop Progress, Météo-France et NOAA sont liés dans Agriculture ; aucun état de culture n'est inventé si la source n'est pas collectée.
- USGS MCS 2026 : production mondiale de cuivre minier et d'aluminium primaire en 2025 (74 Mt contre 72,8 Mt en 2024 pour l'aluminium). Ce sont des repères annuels, sans signal de séance. LME : [rapports de stocks](https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports) à consulter, sans chiffre de stock automatisé tant qu'un flux stable n'est pas vérifié.

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
    .power-history-panel { padding:16px; margin-top:12px; }
    .power-history-panel h2 { font-size:14px; margin:0 0 5px; }
    .power-history-panel p { color:var(--muted); font-size:11px; margin:5px 0 12px; }
    .power-controls { display:flex; gap:6px; flex-wrap:wrap; margin:9px 0; }
    .power-controls button { border:1px solid var(--border); border-radius:6px; background:var(--surface-2); color:var(--muted); padding:6px 10px; font:inherit; font-size:11px; cursor:pointer; }
    .power-controls button[aria-pressed="true"] { border-color:var(--accent); color:var(--accent); }
    .power-history-chart { min-height:260px; }
    .power-history-chart svg { display:block; width:100%; height:235px; }
    .power-history-chart svg line { stroke:var(--border); }
    .power-history-chart svg polyline { fill:none; stroke:var(--accent); stroke-width:2; vector-effect:non-scaling-stroke; }
    .power-history-chart svg .zero { stroke:var(--warm); stroke-dasharray:4 4; }
    .power-history-chart svg text { fill:var(--muted); font-size:11px; }
    .power-meta { color:var(--muted); font-size:11px; }
    .price-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:9px; margin:12px 0; }
    .price-grid article { background:var(--surface-2); border:1px solid var(--border); border-radius:7px; padding:10px; }
    .price-grid small { display:block; color:var(--muted); font-size:10px; }
    .price-grid strong { display:block; font-size:20px; margin:5px 0; }
    .price-grid span { color:var(--muted); font-size:10px; }
    .power-price-chart { height:225px; }
    .power-price-chart svg { width:100%; height:225px; display:block; }
    .power-price-chart polyline { fill:none; stroke:var(--accent); stroke-width:2; vector-effect:non-scaling-stroke; }
    .power-price-chart polyline.secondary { stroke:var(--warm); }
    .power-price-chart line { stroke:var(--border); }
    .power-price-chart line.zero { stroke-dasharray:4 4; stroke:var(--warm); }
    .power-price-chart text { fill:var(--muted); font-size:10px; }
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
      .power-grid, .power-bottom, .price-grid { grid-template-columns:1fr; }
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
      <section class="card power-history-panel">
        <h2>Historique physique · RTE</h2>
        <p>Observations horaires conservées au fil des collectes. Le choix « 1 an » montre uniquement la période réellement disponible ; les valeurs absentes ne sont pas reconstruites.</p>
        <div class="power-controls" id="power-span" aria-label="Période du graphique"></div>
        <div class="power-controls" id="power-series" aria-label="Mesure du graphique"></div>
        <div class="power-history-chart" id="power-history-chart"><span class="empty">Historique RTE en attente.</span></div>
        <div class="power-meta" id="power-history-meta"></div>
        <p id="power-history-reading"></p>
      </section>
      <section class="card power-history-panel" id="power-prices-panel">
        <h2>Prix Power · enchère day-ahead France / DE-LU</h2>
        <p>Prix fixés la veille pour chaque période de livraison en €/MWh. France et Allemagne/Luxembourg partagent une échelle et une heure de livraison ; le graphique ne représente pas les transactions intraday en cours.</p>
        <div class="price-grid" id="power-price-grid"></div>
        <div class="power-controls" id="power-price-span" aria-label="Période des prix"></div>
        <div class="power-price-chart" id="power-price-chart"><span class="empty">Collecte des prix en attente.</span></div>
        <div class="power-meta" id="power-price-meta"></div>
        <p id="power-price-reading"></p>
        <p id="power-price-context"></p>
        <p><a href="https://www.energy-charts.info/charts/price_spot_market/chart.htm?c=FR" target="_blank" rel="noopener noreferrer">Fraunhofer ISE Energy-Charts ↗</a> · <span id="power-price-license">Licence vérifiée dans la réponse source.</span> Graphiques et indicateurs recalculés ici.</p>
      </section>
      <div class="power-bottom">
        <section class="card"><h2>Pour surveiller le gaz et les échanges</h2><p id="power-readout">Le gaz électrique, l'éolien, le solaire et le solde d'import/export seront affichés après la première collecte RTE.</p><p>Un solde RTE négatif signifie une exportation nette ; positif, une importation nette. Les données sont des télémesures complétées d'estimations.</p><a href="https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/" target="_blank" rel="noopener noreferrer">Source RTE éCO2mix ↗</a></section>
        <section class="card"><h2>Demande anticipée · France et DE-LU</h2><p>Point haut prévu dans les prochaines 24 h, prévision day-ahead ENTSO-E sous licence CC BY 4.0. Chaque marché a sa taille : comparer la trajectoire, pas les niveaux bruts.</p><div class="power-forecast" id="power-forecast"></div><p id="power-forecast-note"></p><a href="https://transparency.entsoe.eu/" target="_blank" rel="noopener noreferrer">Transparence ENTSO-E ↗</a></section>
        <section class="card"><h2>Intraday continu · France</h2><p>Le day-ahead ci-dessus est une enchère close la veille. Le marché intraday continu échange ensuite jusqu'à l'approche de la livraison. ENTSO-E rend le day-ahead obligatoire, mais l'intraday n'y est publié que volontairement ; nous n'avons pas de série française continue vérifiée et redistribuable. Le prix d'équilibrage RTE est encore un autre mécanisme.</p><p>Un spread day-ahead/intraday demande les deux prix pour la même période de livraison.</p><a href="https://www.epexspot.com/en/market-results" target="_blank" rel="noopener noreferrer">Résultats intraday EPEX ↗</a> · <a href="https://www.rte-france.com/en/data-publications/eco2mix/market-data" target="_blank" rel="noopener noreferrer">Marché RTE ↗</a></section>
        <section class="card"><h2>Méthode et qualité des mesures</h2><p><b>Observé provisoire</b> : RTE éCO2mix, dernier relevé de chaque heure UTC. <b>Calculé</b> : demande résiduelle = consommation − éolien − solaire ; ce calcul ne représente pas le dispatch réel d'une centrale ni un prix. Les trous de collecte restent visibles dans la courbe.</p><p>La couverture réelle, la date de mesure et l'heure de collecte sont affichées. Le fichier HTML embarque l'historique ; « Actualiser les données » le synchronise depuis GitHub si le réseau le permet.</p><p>Les jetons ENTSO-E et GIE restent dans les secrets GitHub.</p></section>
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
  "generated_at": "2026-09-30T01:19:56+00:00",
  "history": {
    "gas_eu": [
      {
        "date": "2025-02-06",
        "value": 49.97
      },
      {
        "date": "2025-02-07",
        "value": 49.41
      },
      {
        "date": "2025-02-08",
        "value": 48.92
      },
      {
        "date": "2025-02-09",
        "value": 48.38
      },
      {
        "date": "2025-02-10",
        "value": 47.88
      },
      {
        "date": "2025-02-11",
        "value": 47.24
      },
      {
        "date": "2025-02-12",
        "value": 46.49
      },
      {
        "date": "2025-02-13",
        "value": 45.9
      },
      {
        "date": "2025-02-14",
        "value": 45.2
      },
      {
        "date": "2025-02-15",
        "value": 44.62
      },
      {
        "date": "2025-02-16",
        "value": 44.06
      },
      {
        "date": "2025-02-17",
        "value": 43.33
      },
      {
        "date": "2025-02-18",
        "value": 42.59
      },
      {
        "date": "2025-02-19",
        "value": 41.86
      },
      {
        "date": "2025-02-20",
        "value": 41.32
      },
      {
        "date": "2025-02-21",
        "value": 40.95
      },
      {
        "date": "2025-02-22",
        "value": 40.7
      },
      {
        "date": "2025-02-23",
        "value": 40.51
      },
      {
        "date": "2025-02-24",
        "value": 40.22
      },
      {
        "date": "2025-02-25",
        "value": 39.85
      },
      {
        "date": "2025-02-26",
        "value": 39.47
      },
      {
        "date": "2025-02-27",
        "value": 39.05
      },
      {
        "date": "2025-02-28",
        "value": 38.18
      },
      {
        "date": "2025-03-01",
        "value": 38.16
      },
      {
        "date": "2025-03-02",
        "value": 37.91
      },
      {
        "date": "2025-03-03",
        "value": 37.56
      },
      {
        "date": "2025-03-04",
        "value": 37.25
      },
      {
        "date": "2025-03-05",
        "value": 37.0
      },
      {
        "date": "2025-03-06",
        "value": 36.81
      },
      {
        "date": "2025-03-07",
        "value": 36.66
      },
      {
        "date": "2025-03-08",
        "value": 36.63
      },
      {
        "date": "2025-03-09",
        "value": 36.6
      },
      {
        "date": "2025-03-10",
        "value": 36.42
      },
      {
        "date": "2025-03-11",
        "value": 36.16
      },
      {
        "date": "2025-03-12",
        "value": 35.83
      },
      {
        "date": "2025-03-13",
        "value": 35.47
      },
      {
        "date": "2025-03-14",
        "value": 35.16
      },
      {
        "date": "2025-03-15",
        "value": 34.96
      },
      {
        "date": "2025-03-16",
        "value": 34.78
      },
      {
        "date": "2025-03-17",
        "value": 34.47
      },
      {
        "date": "2025-03-18",
        "value": 34.19
      },
      {
        "date": "2025-03-19",
        "value": 33.96
      },
      {
        "date": "2025-03-20",
        "value": 33.81
      },
      {
        "date": "2025-03-21",
        "value": 33.78
      },
      {
        "date": "2025-03-22",
        "value": 33.84
      },
      {
        "date": "2025-03-23",
        "value": 33.87
      },
      {
        "date": "2025-03-24",
        "value": 33.76
      },
      {
        "date": "2025-03-25",
        "value": 33.65
      },
      {
        "date": "2025-03-26",
        "value": 33.56
      },
      {
        "date": "2025-03-27",
        "value": 33.51
      },
      {
        "date": "2025-03-28",
        "value": 33.51
      },
      {
        "date": "2025-03-29",
        "value": 33.59
      },
      {
        "date": "2025-03-30",
        "value": 33.67
      },
      {
        "date": "2025-03-31",
        "value": 33.8
      },
      {
        "date": "2025-04-01",
        "value": 34.3
      },
      {
        "date": "2025-04-02",
        "value": 34.4
      },
      {
        "date": "2025-04-03",
        "value": 34.47
      },
      {
        "date": "2025-04-04",
        "value": 34.61
      },
      {
        "date": "2025-04-05",
        "value": 34.81
      },
      {
        "date": "2025-04-06",
        "value": 35.02
      },
      {
        "date": "2025-04-07",
        "value": 35.0
      },
      {
        "date": "2025-04-08",
        "value": 34.98
      },
      {
        "date": "2025-04-09",
        "value": 34.99
      },
      {
        "date": "2025-04-10",
        "value": 35.03
      },
      {
        "date": "2025-04-11",
        "value": 35.12
      },
      {
        "date": "2025-04-12",
        "value": 35.36
      },
      {
        "date": "2025-04-13",
        "value": 35.63
      },
      {
        "date": "2025-04-14",
        "value": 35.81
      },
      {
        "date": "2025-04-15",
        "value": 35.98
      },
      {
        "date": "2025-04-16",
        "value": 36.11
      },
      {
        "date": "2025-04-17",
        "value": 36.26
      },
      {
        "date": "2025-04-18",
        "value": 36.46
      },
      {
        "date": "2025-04-19",
        "value": 36.75
      },
      {
        "date": "2025-04-20",
        "value": 37.05
      },
      {
        "date": "2025-04-21",
        "value": 37.33
      },
      {
        "date": "2025-04-22",
        "value": 37.54
      },
      {
        "date": "2025-04-23",
        "value": 37.74
      },
      {
        "date": "2025-04-24",
        "value": 37.92
      },
      {
        "date": "2025-04-25",
        "value": 38.14
      },
      {
        "date": "2025-04-26",
        "value": 38.42
      },
      {
        "date": "2025-04-27",
        "value": 38.7
      },
      {
        "date": "2025-04-28",
        "value": 38.96
      },
      {
        "date": "2025-04-29",
        "value": 39.23
      },
      {
        "date": "2025-04-30",
        "value": 39.53
      },
      {
        "date": "2025-05-01",
        "value": 39.9
      },
      {
        "date": "2025-05-02",
        "value": 40.3
      },
      {
        "date": "2025-05-03",
        "value": 40.74
      },
      {
        "date": "2025-05-04",
        "value": 41.14
      },
      {
        "date": "2025-05-05",
        "value": 41.4
      },
      {
        "date": "2025-05-06",
        "value": 41.59
      },
      {
        "date": "2025-05-07",
        "value": 41.79
      },
      {
        "date": "2025-05-08",
        "value": 41.92
      },
      {
        "date": "2025-05-09",
        "value": 42.16
      },
      {
        "date": "2025-05-10",
        "value": 42.47
      },
      {
        "date": "2025-05-11",
        "value": 42.83
      },
      {
        "date": "2025-05-12",
        "value": 43.1
      },
      {
        "date": "2025-05-13",
        "value": 43.36
      },
      {
        "date": "2025-05-14",
        "value": 43.64
      },
      {
        "date": "2025-05-15",
        "value": 43.88
      },
      {
        "date": "2025-05-16",
        "value": 44.13
      },
      {
        "date": "2025-05-17",
        "value": 44.43
      },
      {
        "date": "2025-05-18",
        "value": 44.71
      },
      {
        "date": "2025-05-19",
        "value": 44.93
      },
      {
        "date": "2025-05-20",
        "value": 45.16
      },
      {
        "date": "2025-05-21",
        "value": 45.29
      },
      {
        "date": "2025-05-22",
        "value": 45.47
      },
      {
        "date": "2025-05-23",
        "value": 45.69
      },
      {
        "date": "2025-05-24",
        "value": 45.95
      },
      {
        "date": "2025-05-25",
        "value": 46.31
      },
      {
        "date": "2025-05-26",
        "value": 46.6
      },
      {
        "date": "2025-05-27",
        "value": 46.88
      },
      {
        "date": "2025-05-28",
        "value": 47.17
      },
      {
        "date": "2025-05-29",
        "value": 47.53
      },
      {
        "date": "2025-05-30",
        "value": 47.89
      },
      {
        "date": "2025-05-31",
        "value": 48.34
      },
      {
        "date": "2025-06-01",
        "value": 48.88
      },
      {
        "date": "2025-06-02",
        "value": 49.22
      },
      {
        "date": "2025-06-03",
        "value": 49.55
      },
      {
        "date": "2025-06-04",
        "value": 49.89
      },
      {
        "date": "2025-06-05",
        "value": 50.17
      },
      {
        "date": "2025-06-06",
        "value": 50.53
      },
      {
        "date": "2025-06-07",
        "value": 50.97
      },
      {
        "date": "2025-06-08",
        "value": 51.4
      },
      {
        "date": "2025-06-09",
        "value": 51.79
      },
      {
        "date": "2025-06-10",
        "value": 52.12
      },
      {
        "date": "2025-06-11",
        "value": 52.44
      },
      {
        "date": "2025-06-12",
        "value": 52.75
      },
      {
        "date": "2025-06-13",
        "value": 53.02
      },
      {
        "date": "2025-06-14",
        "value": 53.4
      },
      {
        "date": "2025-06-15",
        "value": 53.78
      },
      {
        "date": "2025-06-16",
        "value": 54.07
      },
      {
        "date": "2025-06-17",
        "value": 54.38
      },
      {
        "date": "2025-06-18",
        "value": 54.72
      },
      {
        "date": "2025-06-19",
        "value": 55.06
      },
      {
        "date": "2025-06-20",
        "value": 55.4
      },
      {
        "date": "2025-06-21",
        "value": 55.81
      },
      {
        "date": "2025-06-22",
        "value": 56.23
      },
      {
        "date": "2025-06-23",
        "value": 56.59
      },
      {
        "date": "2025-06-24",
        "value": 56.91
      },
      {
        "date": "2025-06-25",
        "value": 57.17
      },
      {
        "date": "2025-06-26",
        "value": 57.42
      },
      {
        "date": "2025-06-27",
        "value": 57.77
      },
      {
        "date": "2025-06-28",
        "value": 58.18
      },
      {
        "date": "2025-06-29",
        "value": 58.59
      },
      {
        "date": "2025-06-30",
        "value": 58.9
      },
      {
        "date": "2025-07-01",
        "value": 59.15
      },
      {
        "date": "2025-07-02",
        "value": 59.44
      },
      {
        "date": "2025-07-03",
        "value": 59.69
      },
      {
        "date": "2025-07-04",
        "value": 59.98
      },
      {
        "date": "2025-07-05",
        "value": 60.3
      },
      {
        "date": "2025-07-06",
        "value": 60.65
      },
      {
        "date": "2025-07-07",
        "value": 60.94
      },
      {
        "date": "2025-07-08",
        "value": 61.59
      },
      {
        "date": "2025-07-09",
        "value": 61.56
      },
      {
        "date": "2025-07-10",
        "value": 61.92
      },
      {
        "date": "2025-07-11",
        "value": 62.23
      },
      {
        "date": "2025-07-12",
        "value": 62.63
      },
      {
        "date": "2025-07-13",
        "value": 63.02
      },
      {
        "date": "2025-07-14",
        "value": 63.32
      },
      {
        "date": "2025-07-15",
        "value": 63.61
      },
      {
        "date": "2025-07-16",
        "value": 63.82
      },
      {
        "date": "2025-07-17",
        "value": 64.05
      },
      {
        "date": "2025-07-18",
        "value": 64.34
      },
      {
        "date": "2025-07-19",
        "value": 64.7
      },
      {
        "date": "2025-07-20",
        "value": 65.08
      },
      {
        "date": "2025-07-21",
        "value": 65.36
      },
      {
        "date": "2025-07-22",
        "value": 65.65
      },
      {
        "date": "2025-07-23",
        "value": 65.94
      },
      {
        "date": "2025-07-24",
        "value": 66.19
      },
      {
        "date": "2025-07-25",
        "value": 66.47
      },
      {
        "date": "2025-07-26",
        "value": 66.83
      },
      {
        "date": "2025-07-27",
        "value": 67.28
      },
      {
        "date": "2025-07-28",
        "value": 67.59
      },
      {
        "date": "2025-07-29",
        "value": 67.94
      },
      {
        "date": "2025-07-30",
        "value": 68.28
      },
      {
        "date": "2025-07-31",
        "value": 68.58
      },
      {
        "date": "2025-08-01",
        "value": 68.85
      },
      {
        "date": "2025-08-02",
        "value": 69.24
      },
      {
        "date": "2025-08-03",
        "value": 69.62
      },
      {
        "date": "2025-08-04",
        "value": 69.96
      },
      {
        "date": "2025-08-05",
        "value": 70.3
      },
      {
        "date": "2025-08-06",
        "value": 70.62
      },
      {
        "date": "2025-08-07",
        "value": 70.93
      },
      {
        "date": "2025-08-08",
        "value": 71.25
      },
      {
        "date": "2025-08-09",
        "value": 71.57
      },
      {
        "date": "2025-08-10",
        "value": 72.01
      },
      {
        "date": "2025-08-11",
        "value": 72.31
      },
      {
        "date": "2025-08-12",
        "value": 72.54
      },
      {
        "date": "2025-08-13",
        "value": 72.74
      },
      {
        "date": "2025-08-14",
        "value": 72.99
      },
      {
        "date": "2025-08-15",
        "value": 73.31
      },
      {
        "date": "2025-08-16",
        "value": 73.63
      },
      {
        "date": "2025-08-17",
        "value": 73.95
      },
      {
        "date": "2025-08-18",
        "value": 74.24
      },
      {
        "date": "2025-08-19",
        "value": 74.53
      },
      {
        "date": "2025-08-20",
        "value": 74.8
      },
      {
        "date": "2025-08-21",
        "value": 75.08
      },
      {
        "date": "2025-08-22",
        "value": 75.35
      },
      {
        "date": "2025-08-23",
        "value": 75.67
      },
      {
        "date": "2025-08-24",
        "value": 75.99
      },
      {
        "date": "2025-08-25",
        "value": 76.24
      },
      {
        "date": "2025-08-26",
        "value": 76.46
      },
      {
        "date": "2025-08-27",
        "value": 76.64
      },
      {
        "date": "2025-08-28",
        "value": 76.85
      },
      {
        "date": "2025-08-29",
        "value": 77.09
      },
      {
        "date": "2025-08-30",
        "value": 77.38
      },
      {
        "date": "2025-08-31",
        "value": 77.65
      },
      {
        "date": "2025-09-01",
        "value": 78.1
      },
      {
        "date": "2025-09-02",
        "value": 78.29
      },
      {
        "date": "2025-09-03",
        "value": 78.51
      },
      {
        "date": "2025-09-04",
        "value": 78.74
      },
      {
        "date": "2025-09-05",
        "value": 78.95
      },
      {
        "date": "2025-09-06",
        "value": 79.2
      },
      {
        "date": "2025-09-07",
        "value": 79.48
      },
      {
        "date": "2025-09-08",
        "value": 79.63
      },
      {
        "date": "2025-09-09",
        "value": 79.73
      },
      {
        "date": "2025-09-10",
        "value": 79.86
      },
      {
        "date": "2025-09-11",
        "value": 79.98
      },
      {
        "date": "2025-09-12",
        "value": 80.12
      },
      {
        "date": "2025-09-13",
        "value": 80.35
      },
      {
        "date": "2025-09-14",
        "value": 80.6
      },
      {
        "date": "2025-09-15",
        "value": 80.83
      },
      {
        "date": "2025-09-16",
        "value": 80.97
      },
      {
        "date": "2025-09-17",
        "value": 81.09
      },
      {
        "date": "2025-09-18",
        "value": 81.23
      },
      {
        "date": "2025-09-19",
        "value": 81.38
      },
      {
        "date": "2025-09-20",
        "value": 81.61
      },
      {
        "date": "2025-09-21",
        "value": 81.85
      },
      {
        "date": "2025-09-22",
        "value": 81.96
      },
      {
        "date": "2025-09-23",
        "value": 82.0
      },
      {
        "date": "2025-09-24",
        "value": 82.03
      },
      {
        "date": "2025-09-25",
        "value": 82.09
      },
      {
        "date": "2025-09-26",
        "value": 82.17
      },
      {
        "date": "2025-09-27",
        "value": 82.34
      },
      {
        "date": "2025-09-28",
        "value": 82.5
      },
      {
        "date": "2025-09-29",
        "value": 82.59
      },
      {
        "date": "2025-09-30",
        "value": 82.5
      },
      {
        "date": "2025-10-01",
        "value": 82.59
      },
      {
        "date": "2025-10-02",
        "value": 82.55
      },
      {
        "date": "2025-10-03",
        "value": 82.61
      },
      {
        "date": "2025-10-04",
        "value": 82.75
      },
      {
        "date": "2025-10-05",
        "value": 82.88
      },
      {
        "date": "2025-10-06",
        "value": 82.89
      },
      {
        "date": "2025-10-07",
        "value": 82.86
      },
      {
        "date": "2025-10-08",
        "value": 82.83
      },
      {
        "date": "2025-10-09",
        "value": 82.82
      },
      {
        "date": "2025-10-10",
        "value": 82.88
      },
      {
        "date": "2025-10-11",
        "value": 83.03
      },
      {
        "date": "2025-10-12",
        "value": 83.15
      },
      {
        "date": "2025-10-13",
        "value": 83.09
      },
      {
        "date": "2025-10-14",
        "value": 83.04
      },
      {
        "date": "2025-10-15",
        "value": 82.93
      },
      {
        "date": "2025-10-16",
        "value": 82.81
      },
      {
        "date": "2025-10-17",
        "value": 82.75
      },
      {
        "date": "2025-10-18",
        "value": 82.78
      },
      {
        "date": "2025-10-19",
        "value": 82.84
      },
      {
        "date": "2025-10-20",
        "value": 82.82
      },
      {
        "date": "2025-10-21",
        "value": 82.82
      },
      {
        "date": "2025-10-22",
        "value": 82.82
      },
      {
        "date": "2025-10-23",
        "value": 82.86
      },
      {
        "date": "2025-10-24",
        "value": 82.86
      },
      {
        "date": "2025-10-25",
        "value": 82.79
      },
      {
        "date": "2025-10-26",
        "value": 82.91
      },
      {
        "date": "2025-10-27",
        "value": 82.86
      },
      {
        "date": "2025-10-28",
        "value": 82.83
      },
      {
        "date": "2025-10-29",
        "value": 82.79
      },
      {
        "date": "2025-10-30",
        "value": 82.8
      },
      {
        "date": "2025-10-31",
        "value": 82.82
      },
      {
        "date": "2025-11-01",
        "value": 82.81
      },
      {
        "date": "2025-11-02",
        "value": 82.9
      },
      {
        "date": "2025-11-03",
        "value": 83.02
      },
      {
        "date": "2025-11-04",
        "value": 83.02
      },
      {
        "date": "2025-11-05",
        "value": 82.97
      },
      {
        "date": "2025-11-06",
        "value": 82.83
      },
      {
        "date": "2025-11-07",
        "value": 82.68
      },
      {
        "date": "2025-11-08",
        "value": 82.61
      },
      {
        "date": "2025-11-09",
        "value": 82.55
      },
      {
        "date": "2025-11-10",
        "value": 82.39
      },
      {
        "date": "2025-11-11",
        "value": 82.3
      },
      {
        "date": "2025-11-12",
        "value": 82.22
      },
      {
        "date": "2025-11-13",
        "value": 82.11
      },
      {
        "date": "2025-11-14",
        "value": 82.03
      },
      {
        "date": "2025-11-15",
        "value": 81.98
      },
      {
        "date": "2025-11-16",
        "value": 81.89
      },
      {
        "date": "2025-11-17",
        "value": 81.62
      },
      {
        "date": "2025-11-18",
        "value": 81.16
      },
      {
        "date": "2025-11-19",
        "value": 80.7
      },
      {
        "date": "2025-11-20",
        "value": 80.14
      },
      {
        "date": "2025-11-21",
        "value": 79.54
      },
      {
        "date": "2025-11-22",
        "value": 79.07
      },
      {
        "date": "2025-11-23",
        "value": 78.63
      },
      {
        "date": "2025-11-24",
        "value": 78.08
      },
      {
        "date": "2025-11-25",
        "value": 77.52
      },
      {
        "date": "2025-11-26",
        "value": 76.93
      },
      {
        "date": "2025-11-27",
        "value": 76.4
      },
      {
        "date": "2025-11-28",
        "value": 75.94
      },
      {
        "date": "2025-11-29",
        "value": 75.62
      },
      {
        "date": "2025-11-30",
        "value": 75.21
      },
      {
        "date": "2025-12-01",
        "value": 74.79
      },
      {
        "date": "2025-12-02",
        "value": 74.26
      },
      {
        "date": "2025-12-03",
        "value": 73.66
      },
      {
        "date": "2025-12-04",
        "value": 73.12
      },
      {
        "date": "2025-12-05",
        "value": 72.57
      },
      {
        "date": "2025-12-06",
        "value": 72.26
      },
      {
        "date": "2025-12-07",
        "value": 72.04
      },
      {
        "date": "2025-12-08",
        "value": 71.79
      },
      {
        "date": "2025-12-09",
        "value": 71.52
      },
      {
        "date": "2025-12-10",
        "value": 71.23
      },
      {
        "date": "2025-12-11",
        "value": 70.84
      },
      {
        "date": "2025-12-12",
        "value": 70.39
      },
      {
        "date": "2025-12-13",
        "value": 70.04
      },
      {
        "date": "2025-12-14",
        "value": 69.73
      },
      {
        "date": "2025-12-15",
        "value": 69.25
      },
      {
        "date": "2025-12-16",
        "value": 68.64
      },
      {
        "date": "2025-12-17",
        "value": 68.15
      },
      {
        "date": "2025-12-18",
        "value": 67.86
      },
      {
        "date": "2025-12-19",
        "value": 67.51
      },
      {
        "date": "2025-12-20",
        "value": 67.16
      },
      {
        "date": "2025-12-21",
        "value": 66.89
      },
      {
        "date": "2025-12-22",
        "value": 66.48
      },
      {
        "date": "2025-12-23",
        "value": 66.08
      },
      {
        "date": "2025-12-24",
        "value": 65.67
      },
      {
        "date": "2025-12-25",
        "value": 65.15
      },
      {
        "date": "2025-12-26",
        "value": 64.6
      },
      {
        "date": "2025-12-27",
        "value": 64.15
      },
      {
        "date": "2025-12-28",
        "value": 63.7
      },
      {
        "date": "2025-12-29",
        "value": 63.12
      },
      {
        "date": "2025-12-30",
        "value": 62.53
      },
      {
        "date": "2025-12-31",
        "value": 61.96
      },
      {
        "date": "2026-01-01",
        "value": 61.5
      },
      {
        "date": "2026-01-02",
        "value": 60.96
      },
      {
        "date": "2026-01-03",
        "value": 60.4
      },
      {
        "date": "2026-01-04",
        "value": 59.73
      },
      {
        "date": "2026-01-05",
        "value": 58.88
      },
      {
        "date": "2026-01-06",
        "value": 58.03
      },
      {
        "date": "2026-01-07",
        "value": 57.13
      },
      {
        "date": "2026-01-08",
        "value": 56.24
      },
      {
        "date": "2026-01-09",
        "value": 55.48
      },
      {
        "date": "2026-01-10",
        "value": 54.72
      },
      {
        "date": "2026-01-11",
        "value": 53.96
      },
      {
        "date": "2026-01-12",
        "value": 53.18
      },
      {
        "date": "2026-01-13",
        "value": 52.48
      },
      {
        "date": "2026-01-14",
        "value": 51.87
      },
      {
        "date": "2026-01-15",
        "value": 51.32
      },
      {
        "date": "2026-01-16",
        "value": 50.82
      },
      {
        "date": "2026-01-17",
        "value": 50.32
      },
      {
        "date": "2026-01-18",
        "value": 49.81
      },
      {
        "date": "2026-01-19",
        "value": 49.08
      },
      {
        "date": "2026-01-20",
        "value": 48.3
      },
      {
        "date": "2026-01-21",
        "value": 47.57
      },
      {
        "date": "2026-01-22",
        "value": 46.82
      },
      {
        "date": "2026-01-23",
        "value": 46.1
      },
      {
        "date": "2026-01-24",
        "value": 45.51
      },
      {
        "date": "2026-01-25",
        "value": 44.91
      },
      {
        "date": "2026-01-26",
        "value": 44.19
      },
      {
        "date": "2026-01-27",
        "value": 43.53
      },
      {
        "date": "2026-01-28",
        "value": 42.85
      },
      {
        "date": "2026-01-29",
        "value": 42.15
      },
      {
        "date": "2026-01-30",
        "value": 41.54
      },
      {
        "date": "2026-01-31",
        "value": 41.02
      },
      {
        "date": "2026-02-01",
        "value": 40.53
      },
      {
        "date": "2026-02-02",
        "value": 39.87
      },
      {
        "date": "2026-02-03",
        "value": 39.18
      },
      {
        "date": "2026-02-04",
        "value": 38.5
      },
      {
        "date": "2026-02-05",
        "value": 37.89
      },
      {
        "date": "2026-02-06",
        "value": 37.37
      },
      {
        "date": "2026-02-07",
        "value": 37.04
      },
      {
        "date": "2026-02-08",
        "value": 36.67
      },
      {
        "date": "2026-02-09",
        "value": 36.12
      },
      {
        "date": "2026-02-10",
        "value": 35.62
      },
      {
        "date": "2026-02-11",
        "value": 35.2
      },
      {
        "date": "2026-02-12",
        "value": 34.8
      },
      {
        "date": "2026-02-13",
        "value": 34.37
      },
      {
        "date": "2026-02-14",
        "value": 33.95
      },
      {
        "date": "2026-02-15",
        "value": 33.53
      },
      {
        "date": "2026-02-16",
        "value": 33.02
      },
      {
        "date": "2026-02-17",
        "value": 32.5
      },
      {
        "date": "2026-02-18",
        "value": 31.97
      },
      {
        "date": "2026-02-19",
        "value": 31.46
      },
      {
        "date": "2026-02-20",
        "value": 31.07
      },
      {
        "date": "2026-02-21",
        "value": 30.86
      },
      {
        "date": "2026-02-22",
        "value": 30.79
      },
      {
        "date": "2026-02-23",
        "value": 30.6
      },
      {
        "date": "2026-02-24",
        "value": 30.35
      },
      {
        "date": "2026-02-25",
        "value": 30.19
      },
      {
        "date": "2026-02-26",
        "value": 30.09
      },
      {
        "date": "2026-02-27",
        "value": 30.05
      },
      {
        "date": "2026-02-28",
        "value": 29.98
      },
      {
        "date": "2026-03-01",
        "value": 29.97
      },
      {
        "date": "2026-03-02",
        "value": 29.89
      },
      {
        "date": "2026-03-03",
        "value": 29.75
      },
      {
        "date": "2026-03-04",
        "value": 29.59
      },
      {
        "date": "2026-03-05",
        "value": 29.52
      },
      {
        "date": "2026-03-06",
        "value": 29.42
      },
      {
        "date": "2026-03-07",
        "value": 29.4
      },
      {
        "date": "2026-03-08",
        "value": 29.4
      },
      {
        "date": "2026-03-09",
        "value": 29.3
      },
      {
        "date": "2026-03-10",
        "value": 29.27
      },
      {
        "date": "2026-03-11",
        "value": 29.24
      },
      {
        "date": "2026-03-12",
        "value": 29.17
      },
      {
        "date": "2026-03-13",
        "value": 29.1
      },
      {
        "date": "2026-03-14",
        "value": 29.06
      },
      {
        "date": "2026-03-15",
        "value": 29.04
      },
      {
        "date": "2026-03-16",
        "value": 28.97
      },
      {
        "date": "2026-03-17",
        "value": 28.82
      },
      {
        "date": "2026-03-18",
        "value": 28.69
      },
      {
        "date": "2026-03-19",
        "value": 28.58
      },
      {
        "date": "2026-03-20",
        "value": 28.51
      },
      {
        "date": "2026-03-21",
        "value": 28.49
      },
      {
        "date": "2026-03-22",
        "value": 28.48
      },
      {
        "date": "2026-03-23",
        "value": 28.42
      },
      {
        "date": "2026-03-24",
        "value": 28.45
      },
      {
        "date": "2026-03-25",
        "value": 28.44
      },
      {
        "date": "2026-03-26",
        "value": 28.29
      },
      {
        "date": "2026-03-27",
        "value": 28.15
      },
      {
        "date": "2026-03-28",
        "value": 28.13
      },
      {
        "date": "2026-03-29",
        "value": 28.1
      },
      {
        "date": "2026-03-30",
        "value": 27.98
      },
      {
        "date": "2026-03-31",
        "value": 27.62
      },
      {
        "date": "2026-04-01",
        "value": 27.89
      },
      {
        "date": "2026-04-02",
        "value": 27.88
      },
      {
        "date": "2026-04-03",
        "value": 27.93
      },
      {
        "date": "2026-04-04",
        "value": 28.15
      },
      {
        "date": "2026-04-05",
        "value": 28.38
      },
      {
        "date": "2026-04-06",
        "value": 28.58
      },
      {
        "date": "2026-04-07",
        "value": 28.74
      },
      {
        "date": "2026-04-08",
        "value": 28.89
      },
      {
        "date": "2026-04-09",
        "value": 29.01
      },
      {
        "date": "2026-04-10",
        "value": 29.14
      },
      {
        "date": "2026-04-11",
        "value": 29.36
      },
      {
        "date": "2026-04-12",
        "value": 29.5
      },
      {
        "date": "2026-04-13",
        "value": 29.52
      },
      {
        "date": "2026-04-14",
        "value": 29.51
      },
      {
        "date": "2026-04-15",
        "value": 29.55
      },
      {
        "date": "2026-04-16",
        "value": 29.7
      },
      {
        "date": "2026-04-17",
        "value": 29.92
      },
      {
        "date": "2026-04-18",
        "value": 30.2
      },
      {
        "date": "2026-04-19",
        "value": 30.46
      },
      {
        "date": "2026-04-20",
        "value": 30.61
      },
      {
        "date": "2026-04-21",
        "value": 30.71
      },
      {
        "date": "2026-04-22",
        "value": 30.82
      },
      {
        "date": "2026-04-23",
        "value": 30.95
      },
      {
        "date": "2026-04-24",
        "value": 31.19
      },
      {
        "date": "2026-04-25",
        "value": 31.47
      },
      {
        "date": "2026-04-26",
        "value": 31.75
      },
      {
        "date": "2026-04-27",
        "value": 31.97
      },
      {
        "date": "2026-04-28",
        "value": 32.23
      },
      {
        "date": "2026-04-29",
        "value": 32.49
      },
      {
        "date": "2026-04-30",
        "value": 32.73
      },
      {
        "date": "2026-05-01",
        "value": 33.06
      },
      {
        "date": "2026-05-02",
        "value": 33.43
      },
      {
        "date": "2026-05-03",
        "value": 33.78
      },
      {
        "date": "2026-05-04",
        "value": 34.05
      },
      {
        "date": "2026-05-05",
        "value": 34.24
      },
      {
        "date": "2026-05-06",
        "value": 34.38
      },
      {
        "date": "2026-05-07",
        "value": 34.5
      },
      {
        "date": "2026-05-08",
        "value": 34.73
      },
      {
        "date": "2026-05-09",
        "value": 35.04
      },
      {
        "date": "2026-05-10",
        "value": 35.35
      },
      {
        "date": "2026-05-11",
        "value": 35.56
      },
      {
        "date": "2026-05-12",
        "value": 35.71
      },
      {
        "date": "2026-05-13",
        "value": 35.83
      },
      {
        "date": "2026-05-14",
        "value": 35.98
      },
      {
        "date": "2026-05-15",
        "value": 36.14
      },
      {
        "date": "2026-05-16",
        "value": 36.34
      },
      {
        "date": "2026-05-17",
        "value": 36.56
      },
      {
        "date": "2026-05-18",
        "value": 36.72
      },
      {
        "date": "2026-05-19",
        "value": 36.87
      },
      {
        "date": "2026-05-20",
        "value": 36.99
      },
      {
        "date": "2026-05-21",
        "value": 37.18
      },
      {
        "date": "2026-05-22",
        "value": 37.45
      },
      {
        "date": "2026-05-23",
        "value": 37.83
      },
      {
        "date": "2026-05-24",
        "value": 38.21
      },
      {
        "date": "2026-05-25",
        "value": 38.52
      },
      {
        "date": "2026-05-26",
        "value": 38.83
      },
      {
        "date": "2026-05-27",
        "value": 39.13
      },
      {
        "date": "2026-05-28",
        "value": 39.42
      },
      {
        "date": "2026-05-29",
        "value": 39.73
      },
      {
        "date": "2026-05-30",
        "value": 40.09
      },
      {
        "date": "2026-05-31",
        "value": 40.47
      },
      {
        "date": "2026-06-01",
        "value": 40.76
      },
      {
        "date": "2026-06-02",
        "value": 41.03
      },
      {
        "date": "2026-06-03",
        "value": 41.25
      },
      {
        "date": "2026-06-04",
        "value": 41.53
      },
      {
        "date": "2026-06-05",
        "value": 41.79
      },
      {
        "date": "2026-06-06",
        "value": 42.13
      },
      {
        "date": "2026-06-07",
        "value": 42.48
      },
      {
        "date": "2026-06-08",
        "value": 42.79
      },
      {
        "date": "2026-06-09",
        "value": 43.09
      },
      {
        "date": "2026-06-10",
        "value": 43.36
      },
      {
        "date": "2026-06-11",
        "value": 43.59
      },
      {
        "date": "2026-06-12",
        "value": 43.91
      },
      {
        "date": "2026-06-13",
        "value": 44.34
      },
      {
        "date": "2026-06-14",
        "value": 44.72
      },
      {
        "date": "2026-06-15",
        "value": 45.03
      },
      {
        "date": "2026-06-16",
        "value": 45.29
      },
      {
        "date": "2026-06-17",
        "value": 45.56
      },
      {
        "date": "2026-06-18",
        "value": 45.82
      },
      {
        "date": "2026-06-19",
        "value": 46.1
      },
      {
        "date": "2026-06-20",
        "value": 46.41
      },
      {
        "date": "2026-06-21",
        "value": 46.73
      },
      {
        "date": "2026-06-22",
        "value": 46.98
      },
      {
        "date": "2026-06-23",
        "value": 47.21
      },
      {
        "date": "2026-06-24",
        "value": 47.44
      },
      {
        "date": "2026-06-25",
        "value": 47.7
      },
      {
        "date": "2026-06-26",
        "value": 47.98
      },
      {
        "date": "2026-06-27",
        "value": 48.31
      },
      {
        "date": "2026-06-28",
        "value": 48.63
      },
      {
        "date": "2026-06-29",
        "value": 48.87
      },
      {
        "date": "2026-06-30",
        "value": 49.09
      },
      {
        "date": "2026-07-01",
        "value": 49.24
      },
      {
        "date": "2026-07-02",
        "value": 49.47
      },
      {
        "date": "2026-07-03",
        "value": 49.72
      },
      {
        "date": "2026-07-04",
        "value": 50.05
      },
      {
        "date": "2026-07-05",
        "value": 50.37
      },
      {
        "date": "2026-07-06",
        "value": 50.64
      },
      {
        "date": "2026-07-07",
        "value": 50.89
      },
      {
        "date": "2026-07-08",
        "value": 51.11
      },
      {
        "date": "2026-07-09",
        "value": 51.32
      },
      {
        "date": "2026-07-10",
        "value": 51.53
      },
      {
        "date": "2026-07-11",
        "value": 51.87
      },
      {
        "date": "2026-07-12",
        "value": 52.24
      },
      {
        "date": "2026-07-13",
        "value": 52.52
      },
      {
        "date": "2026-07-14",
        "value": 52.77
      },
      {
        "date": "2026-07-15",
        "value": 53.0
      },
      {
        "date": "2026-07-16",
        "value": 53.15
      },
      {
        "date": "2026-07-17",
        "value": 53.37
      },
      {
        "date": "2026-07-18",
        "value": 53.68
      },
      {
        "date": "2026-07-19",
        "value": 54.0
      },
      {
        "date": "2026-07-20",
        "value": 54.2
      },
      {
        "date": "2026-07-21",
        "value": 54.38
      },
      {
        "date": "2026-07-22",
        "value": 54.61
      },
      {
        "date": "2026-07-23",
        "value": 54.82
      },
      {
        "date": "2026-07-24",
        "value": 55.06
      },
      {
        "date": "2026-07-25",
        "value": 55.35
      },
      {
        "date": "2026-07-26",
        "value": 55.67
      },
      {
        "date": "2026-07-27",
        "value": 55.91
      },
      {
        "date": "2026-07-28",
        "value": 56.15
      },
      {
        "date": "2026-07-29",
        "value": 56.39
      },
      {
        "date": "2026-07-30",
        "value": 56.63
      },
      {
        "date": "2026-07-31",
        "value": 56.86
      },
      {
        "date": "2026-08-01",
        "value": 57.09
      },
      {
        "date": "2026-08-02",
        "value": 57.41
      },
      {
        "date": "2026-08-03",
        "value": 57.64
      },
      {
        "date": "2026-08-04",
        "value": 57.85
      },
      {
        "date": "2026-08-05",
        "value": 58.07
      },
      {
        "date": "2026-08-06",
        "value": 58.3
      },
      {
        "date": "2026-08-07",
        "value": 58.53
      },
      {
        "date": "2026-08-08",
        "value": 58.82
      },
      {
        "date": "2026-08-09",
        "value": 59.1
      },
      {
        "date": "2026-08-10",
        "value": 59.37
      },
      {
        "date": "2026-08-11",
        "value": 59.63
      },
      {
        "date": "2026-08-12",
        "value": 59.9
      },
      {
        "date": "2026-08-13",
        "value": 60.16
      },
      {
        "date": "2026-08-14",
        "value": 60.44
      },
      {
        "date": "2026-08-15",
        "value": 60.79
      },
      {
        "date": "2026-08-16",
        "value": 61.13
      },
      {
        "date": "2026-08-17",
        "value": 61.37
      },
      {
        "date": "2026-08-18",
        "value": 61.6
      },
      {
        "date": "2026-08-19",
        "value": 61.81
      },
      {
        "date": "2026-08-20",
        "value": 62.04
      },
      {
        "date": "2026-08-21",
        "value": 62.32
      },
      {
        "date": "2026-08-22",
        "value": 62.64
      },
      {
        "date": "2026-08-23",
        "value": 62.99
      },
      {
        "date": "2026-08-24",
        "value": 63.28
      },
      {
        "date": "2026-08-25",
        "value": 63.55
      },
      {
        "date": "2026-08-26",
        "value": 63.81
      },
      {
        "date": "2026-08-27",
        "value": 64.09
      },
      {
        "date": "2026-08-28",
        "value": 64.38
      },
      {
        "date": "2026-08-29",
        "value": 64.74
      },
      {
        "date": "2026-08-30",
        "value": 65.1
      },
      {
        "date": "2026-08-31",
        "value": 65.4
      },
      {
        "date": "2026-09-01",
        "value": 65.62
      },
      {
        "date": "2026-09-02",
        "value": 65.83
      },
      {
        "date": "2026-09-03",
        "value": 66.07
      },
      {
        "date": "2026-09-04",
        "value": 66.35
      },
      {
        "date": "2026-09-05",
        "value": 66.59
      },
      {
        "date": "2026-09-06",
        "value": 66.91
      },
      {
        "date": "2026-09-07",
        "value": 67.14
      },
      {
        "date": "2026-09-08",
        "value": 67.35
      },
      {
        "date": "2026-09-09",
        "value": 67.52
      },
      {
        "date": "2026-09-10",
        "value": 67.66
      },
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
      },
      {
        "date": "2026-09-25",
        "value": 70.62
      },
      {
        "date": "2026-09-26",
        "value": 70.88
      },
      {
        "date": "2026-09-27",
        "value": 71.17
      },
      {
        "date": "2026-09-28",
        "value": 71.33
      }
    ],
    "gas_fr": [
      {
        "date": "2025-02-06",
        "value": 31.43
      },
      {
        "date": "2025-02-07",
        "value": 30.8
      },
      {
        "date": "2025-02-08",
        "value": 30.29
      },
      {
        "date": "2025-02-09",
        "value": 29.85
      },
      {
        "date": "2025-02-10",
        "value": 29.3
      },
      {
        "date": "2025-02-11",
        "value": 28.58
      },
      {
        "date": "2025-02-12",
        "value": 27.98
      },
      {
        "date": "2025-02-13",
        "value": 27.38
      },
      {
        "date": "2025-02-14",
        "value": 26.77
      },
      {
        "date": "2025-02-15",
        "value": 26.19
      },
      {
        "date": "2025-02-16",
        "value": 25.64
      },
      {
        "date": "2025-02-17",
        "value": 24.87
      },
      {
        "date": "2025-02-18",
        "value": 24.24
      },
      {
        "date": "2025-02-19",
        "value": 23.76
      },
      {
        "date": "2025-02-20",
        "value": 23.51
      },
      {
        "date": "2025-02-21",
        "value": 23.32
      },
      {
        "date": "2025-02-22",
        "value": 23.37
      },
      {
        "date": "2025-02-23",
        "value": 23.5
      },
      {
        "date": "2025-02-24",
        "value": 23.56
      },
      {
        "date": "2025-02-25",
        "value": 23.48
      },
      {
        "date": "2025-02-26",
        "value": 23.26
      },
      {
        "date": "2025-02-27",
        "value": 22.94
      },
      {
        "date": "2025-02-28",
        "value": 22.61
      },
      {
        "date": "2025-03-01",
        "value": 22.38
      },
      {
        "date": "2025-03-02",
        "value": 22.18
      },
      {
        "date": "2025-03-03",
        "value": 21.81
      },
      {
        "date": "2025-03-04",
        "value": 21.6
      },
      {
        "date": "2025-03-05",
        "value": 21.53
      },
      {
        "date": "2025-03-06",
        "value": 21.62
      },
      {
        "date": "2025-03-07",
        "value": 21.76
      },
      {
        "date": "2025-03-08",
        "value": 22.15
      },
      {
        "date": "2025-03-09",
        "value": 22.52
      },
      {
        "date": "2025-03-10",
        "value": 22.7
      },
      {
        "date": "2025-03-11",
        "value": 22.72
      },
      {
        "date": "2025-03-12",
        "value": 22.47
      },
      {
        "date": "2025-03-13",
        "value": 22.1
      },
      {
        "date": "2025-03-14",
        "value": 21.78
      },
      {
        "date": "2025-03-15",
        "value": 21.57
      },
      {
        "date": "2025-03-16",
        "value": 21.44
      },
      {
        "date": "2025-03-17",
        "value": 21.26
      },
      {
        "date": "2025-03-18",
        "value": 21.12
      },
      {
        "date": "2025-03-19",
        "value": 21.1
      },
      {
        "date": "2025-03-20",
        "value": 21.29
      },
      {
        "date": "2025-03-21",
        "value": 21.74
      },
      {
        "date": "2025-03-22",
        "value": 22.14
      },
      {
        "date": "2025-03-23",
        "value": 22.47
      },
      {
        "date": "2025-03-24",
        "value": 22.66
      },
      {
        "date": "2025-03-25",
        "value": 22.86
      },
      {
        "date": "2025-03-26",
        "value": 23.13
      },
      {
        "date": "2025-03-27",
        "value": 23.48
      },
      {
        "date": "2025-03-28",
        "value": 23.81
      },
      {
        "date": "2025-03-29",
        "value": 24.18
      },
      {
        "date": "2025-03-30",
        "value": 24.59
      },
      {
        "date": "2025-03-31",
        "value": 24.99
      },
      {
        "date": "2025-04-01",
        "value": 27.28
      },
      {
        "date": "2025-04-02",
        "value": 27.73
      },
      {
        "date": "2025-04-03",
        "value": 27.95
      },
      {
        "date": "2025-04-04",
        "value": 28.49
      },
      {
        "date": "2025-04-05",
        "value": 29.26
      },
      {
        "date": "2025-04-06",
        "value": 30.01
      },
      {
        "date": "2025-04-07",
        "value": 30.55
      },
      {
        "date": "2025-04-08",
        "value": 30.99
      },
      {
        "date": "2025-04-09",
        "value": 31.54
      },
      {
        "date": "2025-04-10",
        "value": 32.11
      },
      {
        "date": "2025-04-11",
        "value": 32.7
      },
      {
        "date": "2025-04-12",
        "value": 33.32
      },
      {
        "date": "2025-04-13",
        "value": 33.95
      },
      {
        "date": "2025-04-14",
        "value": 34.53
      },
      {
        "date": "2025-04-15",
        "value": 35.11
      },
      {
        "date": "2025-04-16",
        "value": 35.54
      },
      {
        "date": "2025-04-17",
        "value": 35.95
      },
      {
        "date": "2025-04-18",
        "value": 36.35
      },
      {
        "date": "2025-04-19",
        "value": 36.92
      },
      {
        "date": "2025-04-20",
        "value": 37.49
      },
      {
        "date": "2025-04-21",
        "value": 37.97
      },
      {
        "date": "2025-04-22",
        "value": 38.46
      },
      {
        "date": "2025-04-23",
        "value": 38.95
      },
      {
        "date": "2025-04-24",
        "value": 39.38
      },
      {
        "date": "2025-04-25",
        "value": 39.84
      },
      {
        "date": "2025-04-26",
        "value": 40.42
      },
      {
        "date": "2025-04-27",
        "value": 41.0
      },
      {
        "date": "2025-04-28",
        "value": 41.52
      },
      {
        "date": "2025-04-29",
        "value": 42.04
      },
      {
        "date": "2025-04-30",
        "value": 42.64
      },
      {
        "date": "2025-05-01",
        "value": 43.29
      },
      {
        "date": "2025-05-02",
        "value": 43.94
      },
      {
        "date": "2025-05-03",
        "value": 44.67
      },
      {
        "date": "2025-05-04",
        "value": 45.37
      },
      {
        "date": "2025-05-05",
        "value": 45.81
      },
      {
        "date": "2025-05-06",
        "value": 46.36
      },
      {
        "date": "2025-05-07",
        "value": 46.86
      },
      {
        "date": "2025-05-08",
        "value": 47.4
      },
      {
        "date": "2025-05-09",
        "value": 47.93
      },
      {
        "date": "2025-05-10",
        "value": 48.52
      },
      {
        "date": "2025-05-11",
        "value": 49.14
      },
      {
        "date": "2025-05-12",
        "value": 49.6
      },
      {
        "date": "2025-05-13",
        "value": 50.0
      },
      {
        "date": "2025-05-14",
        "value": 50.32
      },
      {
        "date": "2025-05-15",
        "value": 50.51
      },
      {
        "date": "2025-05-16",
        "value": 50.81
      },
      {
        "date": "2025-05-17",
        "value": 51.17
      },
      {
        "date": "2025-05-18",
        "value": 51.51
      },
      {
        "date": "2025-05-19",
        "value": 51.65
      },
      {
        "date": "2025-05-20",
        "value": 51.88
      },
      {
        "date": "2025-05-21",
        "value": 51.73
      },
      {
        "date": "2025-05-22",
        "value": 51.66
      },
      {
        "date": "2025-05-23",
        "value": 51.97
      },
      {
        "date": "2025-05-24",
        "value": 51.98
      },
      {
        "date": "2025-05-25",
        "value": 52.46
      },
      {
        "date": "2025-05-26",
        "value": 52.82
      },
      {
        "date": "2025-05-27",
        "value": 53.24
      },
      {
        "date": "2025-05-28",
        "value": 53.64
      },
      {
        "date": "2025-05-29",
        "value": 54.1
      },
      {
        "date": "2025-05-30",
        "value": 54.61
      },
      {
        "date": "2025-05-31",
        "value": 55.3
      },
      {
        "date": "2025-06-01",
        "value": 55.87
      },
      {
        "date": "2025-06-02",
        "value": 56.29
      },
      {
        "date": "2025-06-03",
        "value": 56.72
      },
      {
        "date": "2025-06-04",
        "value": 57.11
      },
      {
        "date": "2025-06-05",
        "value": 57.48
      },
      {
        "date": "2025-06-06",
        "value": 57.96
      },
      {
        "date": "2025-06-07",
        "value": 58.48
      },
      {
        "date": "2025-06-08",
        "value": 58.98
      },
      {
        "date": "2025-06-09",
        "value": 59.45
      },
      {
        "date": "2025-06-10",
        "value": 59.87
      },
      {
        "date": "2025-06-11",
        "value": 60.33
      },
      {
        "date": "2025-06-12",
        "value": 60.7
      },
      {
        "date": "2025-06-13",
        "value": 60.69
      },
      {
        "date": "2025-06-14",
        "value": 61.03
      },
      {
        "date": "2025-06-15",
        "value": 61.38
      },
      {
        "date": "2025-06-16",
        "value": 61.63
      },
      {
        "date": "2025-06-17",
        "value": 62.06
      },
      {
        "date": "2025-06-18",
        "value": 62.41
      },
      {
        "date": "2025-06-19",
        "value": 62.66
      },
      {
        "date": "2025-06-20",
        "value": 62.94
      },
      {
        "date": "2025-06-21",
        "value": 63.37
      },
      {
        "date": "2025-06-22",
        "value": 63.87
      },
      {
        "date": "2025-06-23",
        "value": 64.27
      },
      {
        "date": "2025-06-24",
        "value": 64.52
      },
      {
        "date": "2025-06-25",
        "value": 64.69
      },
      {
        "date": "2025-06-26",
        "value": 64.87
      },
      {
        "date": "2025-06-27",
        "value": 65.23
      },
      {
        "date": "2025-06-28",
        "value": 65.63
      },
      {
        "date": "2025-06-29",
        "value": 66.02
      },
      {
        "date": "2025-06-30",
        "value": 66.29
      },
      {
        "date": "2025-07-01",
        "value": 66.47
      },
      {
        "date": "2025-07-02",
        "value": 66.75
      },
      {
        "date": "2025-07-03",
        "value": 67.0
      },
      {
        "date": "2025-07-04",
        "value": 67.22
      },
      {
        "date": "2025-07-05",
        "value": 67.6
      },
      {
        "date": "2025-07-06",
        "value": 67.98
      },
      {
        "date": "2025-07-07",
        "value": 68.32
      },
      {
        "date": "2025-07-08",
        "value": 68.64
      },
      {
        "date": "2025-07-09",
        "value": 68.93
      },
      {
        "date": "2025-07-10",
        "value": 69.26
      },
      {
        "date": "2025-07-11",
        "value": 69.56
      },
      {
        "date": "2025-07-12",
        "value": 69.95
      },
      {
        "date": "2025-07-13",
        "value": 70.33
      },
      {
        "date": "2025-07-14",
        "value": 70.75
      },
      {
        "date": "2025-07-15",
        "value": 71.16
      },
      {
        "date": "2025-07-16",
        "value": 71.43
      },
      {
        "date": "2025-07-17",
        "value": 71.59
      },
      {
        "date": "2025-07-18",
        "value": 71.92
      },
      {
        "date": "2025-07-19",
        "value": 72.36
      },
      {
        "date": "2025-07-20",
        "value": 72.77
      },
      {
        "date": "2025-07-21",
        "value": 73.12
      },
      {
        "date": "2025-07-22",
        "value": 73.45
      },
      {
        "date": "2025-07-23",
        "value": 73.74
      },
      {
        "date": "2025-07-24",
        "value": 74.01
      },
      {
        "date": "2025-07-25",
        "value": 74.28
      },
      {
        "date": "2025-07-26",
        "value": 74.66
      },
      {
        "date": "2025-07-27",
        "value": 75.08
      },
      {
        "date": "2025-07-28",
        "value": 75.45
      },
      {
        "date": "2025-07-29",
        "value": 75.85
      },
      {
        "date": "2025-07-30",
        "value": 76.28
      },
      {
        "date": "2025-07-31",
        "value": 76.67
      },
      {
        "date": "2025-08-01",
        "value": 77.19
      },
      {
        "date": "2025-08-02",
        "value": 77.66
      },
      {
        "date": "2025-08-03",
        "value": 78.17
      },
      {
        "date": "2025-08-04",
        "value": 78.5
      },
      {
        "date": "2025-08-05",
        "value": 78.8
      },
      {
        "date": "2025-08-06",
        "value": 79.13
      },
      {
        "date": "2025-08-07",
        "value": 79.39
      },
      {
        "date": "2025-08-08",
        "value": 79.64
      },
      {
        "date": "2025-08-09",
        "value": 80.07
      },
      {
        "date": "2025-08-10",
        "value": 80.58
      },
      {
        "date": "2025-08-11",
        "value": 80.81
      },
      {
        "date": "2025-08-12",
        "value": 80.91
      },
      {
        "date": "2025-08-13",
        "value": 80.98
      },
      {
        "date": "2025-08-14",
        "value": 81.09
      },
      {
        "date": "2025-08-15",
        "value": 81.29
      },
      {
        "date": "2025-08-16",
        "value": 81.51
      },
      {
        "date": "2025-08-17",
        "value": 81.73
      },
      {
        "date": "2025-08-18",
        "value": 82.16
      },
      {
        "date": "2025-08-19",
        "value": 82.6
      },
      {
        "date": "2025-08-20",
        "value": 82.96
      },
      {
        "date": "2025-08-21",
        "value": 83.29
      },
      {
        "date": "2025-08-22",
        "value": 83.54
      },
      {
        "date": "2025-08-23",
        "value": 83.89
      },
      {
        "date": "2025-08-24",
        "value": 84.33
      },
      {
        "date": "2025-08-25",
        "value": 84.72
      },
      {
        "date": "2025-08-26",
        "value": 85.02
      },
      {
        "date": "2025-08-27",
        "value": 85.33
      },
      {
        "date": "2025-08-28",
        "value": 85.78
      },
      {
        "date": "2025-08-29",
        "value": 86.25
      },
      {
        "date": "2025-08-30",
        "value": 86.56
      },
      {
        "date": "2025-08-31",
        "value": 86.53
      },
      {
        "date": "2025-09-01",
        "value": 86.79
      },
      {
        "date": "2025-09-02",
        "value": 87.33
      },
      {
        "date": "2025-09-03",
        "value": 87.66
      },
      {
        "date": "2025-09-04",
        "value": 87.97
      },
      {
        "date": "2025-09-05",
        "value": 88.24
      },
      {
        "date": "2025-09-06",
        "value": 88.6
      },
      {
        "date": "2025-09-07",
        "value": 88.93
      },
      {
        "date": "2025-09-08",
        "value": 89.21
      },
      {
        "date": "2025-09-09",
        "value": 89.48
      },
      {
        "date": "2025-09-10",
        "value": 89.71
      },
      {
        "date": "2025-09-11",
        "value": 89.77
      },
      {
        "date": "2025-09-12",
        "value": 89.89
      },
      {
        "date": "2025-09-13",
        "value": 89.93
      },
      {
        "date": "2025-09-14",
        "value": 89.97
      },
      {
        "date": "2025-09-15",
        "value": 90.18
      },
      {
        "date": "2025-09-16",
        "value": 90.23
      },
      {
        "date": "2025-09-17",
        "value": 90.16
      },
      {
        "date": "2025-09-18",
        "value": 90.23
      },
      {
        "date": "2025-09-19",
        "value": 90.25
      },
      {
        "date": "2025-09-20",
        "value": 90.57
      },
      {
        "date": "2025-09-21",
        "value": 90.87
      },
      {
        "date": "2025-09-22",
        "value": 91.06
      },
      {
        "date": "2025-09-23",
        "value": 91.16
      },
      {
        "date": "2025-09-24",
        "value": 91.25
      },
      {
        "date": "2025-09-25",
        "value": 91.08
      },
      {
        "date": "2025-09-26",
        "value": 91.07
      },
      {
        "date": "2025-09-27",
        "value": 91.25
      },
      {
        "date": "2025-09-28",
        "value": 91.45
      },
      {
        "date": "2025-09-29",
        "value": 91.58
      },
      {
        "date": "2025-09-30",
        "value": 91.75
      },
      {
        "date": "2025-10-01",
        "value": 91.62
      },
      {
        "date": "2025-10-02",
        "value": 91.5
      },
      {
        "date": "2025-10-03",
        "value": 91.69
      },
      {
        "date": "2025-10-04",
        "value": 91.99
      },
      {
        "date": "2025-10-05",
        "value": 92.32
      },
      {
        "date": "2025-10-06",
        "value": 92.47
      },
      {
        "date": "2025-10-07",
        "value": 92.41
      },
      {
        "date": "2025-10-08",
        "value": 92.38
      },
      {
        "date": "2025-10-09",
        "value": 92.38
      },
      {
        "date": "2025-10-10",
        "value": 92.45
      },
      {
        "date": "2025-10-11",
        "value": 92.8
      },
      {
        "date": "2025-10-12",
        "value": 93.0
      },
      {
        "date": "2025-10-13",
        "value": 92.84
      },
      {
        "date": "2025-10-14",
        "value": 92.83
      },
      {
        "date": "2025-10-15",
        "value": 92.69
      },
      {
        "date": "2025-10-16",
        "value": 92.34
      },
      {
        "date": "2025-10-17",
        "value": 92.19
      },
      {
        "date": "2025-10-18",
        "value": 92.27
      },
      {
        "date": "2025-10-19",
        "value": 92.46
      },
      {
        "date": "2025-10-20",
        "value": 92.56
      },
      {
        "date": "2025-10-21",
        "value": 92.69
      },
      {
        "date": "2025-10-22",
        "value": 92.83
      },
      {
        "date": "2025-10-23",
        "value": 92.83
      },
      {
        "date": "2025-10-24",
        "value": 92.73
      },
      {
        "date": "2025-10-25",
        "value": 92.78
      },
      {
        "date": "2025-10-26",
        "value": 92.79
      },
      {
        "date": "2025-10-27",
        "value": 92.7
      },
      {
        "date": "2025-10-28",
        "value": 92.63
      },
      {
        "date": "2025-10-29",
        "value": 92.59
      },
      {
        "date": "2025-10-30",
        "value": 92.62
      },
      {
        "date": "2025-10-31",
        "value": 92.78
      },
      {
        "date": "2025-11-01",
        "value": 93.05
      },
      {
        "date": "2025-11-02",
        "value": 93.21
      },
      {
        "date": "2025-11-03",
        "value": 93.19
      },
      {
        "date": "2025-11-04",
        "value": 93.29
      },
      {
        "date": "2025-11-05",
        "value": 93.36
      },
      {
        "date": "2025-11-06",
        "value": 93.3
      },
      {
        "date": "2025-11-07",
        "value": 93.19
      },
      {
        "date": "2025-11-08",
        "value": 93.18
      },
      {
        "date": "2025-11-09",
        "value": 93.16
      },
      {
        "date": "2025-11-10",
        "value": 93.12
      },
      {
        "date": "2025-11-11",
        "value": 93.2
      },
      {
        "date": "2025-11-12",
        "value": 93.33
      },
      {
        "date": "2025-11-13",
        "value": 93.31
      },
      {
        "date": "2025-11-14",
        "value": 93.4
      },
      {
        "date": "2025-11-15",
        "value": 93.55
      },
      {
        "date": "2025-11-16",
        "value": 93.46
      },
      {
        "date": "2025-11-17",
        "value": 93.14
      },
      {
        "date": "2025-11-18",
        "value": 92.39
      },
      {
        "date": "2025-11-19",
        "value": 91.58
      },
      {
        "date": "2025-11-20",
        "value": 90.53
      },
      {
        "date": "2025-11-21",
        "value": 89.47
      },
      {
        "date": "2025-11-22",
        "value": 88.64
      },
      {
        "date": "2025-11-23",
        "value": 87.98
      },
      {
        "date": "2025-11-24",
        "value": 87.27
      },
      {
        "date": "2025-11-25",
        "value": 86.41
      },
      {
        "date": "2025-11-26",
        "value": 85.44
      },
      {
        "date": "2025-11-27",
        "value": 84.63
      },
      {
        "date": "2025-11-28",
        "value": 83.92
      },
      {
        "date": "2025-11-29",
        "value": 83.38
      },
      {
        "date": "2025-11-30",
        "value": 81.97
      },
      {
        "date": "2025-12-01",
        "value": 81.86
      },
      {
        "date": "2025-12-02",
        "value": 80.92
      },
      {
        "date": "2025-12-03",
        "value": 79.94
      },
      {
        "date": "2025-12-04",
        "value": 79.03
      },
      {
        "date": "2025-12-05",
        "value": 78.3
      },
      {
        "date": "2025-12-06",
        "value": 77.74
      },
      {
        "date": "2025-12-07",
        "value": 77.31
      },
      {
        "date": "2025-12-08",
        "value": 76.85
      },
      {
        "date": "2025-12-09",
        "value": 76.49
      },
      {
        "date": "2025-12-10",
        "value": 76.1
      },
      {
        "date": "2025-12-11",
        "value": 75.49
      },
      {
        "date": "2025-12-12",
        "value": 74.89
      },
      {
        "date": "2025-12-13",
        "value": 74.46
      },
      {
        "date": "2025-12-14",
        "value": 73.93
      },
      {
        "date": "2025-12-15",
        "value": 73.31
      },
      {
        "date": "2025-12-16",
        "value": 72.61
      },
      {
        "date": "2025-12-17",
        "value": 72.0
      },
      {
        "date": "2025-12-18",
        "value": 71.51
      },
      {
        "date": "2025-12-19",
        "value": 71.01
      },
      {
        "date": "2025-12-20",
        "value": 70.43
      },
      {
        "date": "2025-12-21",
        "value": 69.88
      },
      {
        "date": "2025-12-22",
        "value": 69.12
      },
      {
        "date": "2025-12-23",
        "value": 68.44
      },
      {
        "date": "2025-12-24",
        "value": 67.71
      },
      {
        "date": "2025-12-25",
        "value": 66.7
      },
      {
        "date": "2025-12-26",
        "value": 65.58
      },
      {
        "date": "2025-12-27",
        "value": 64.59
      },
      {
        "date": "2025-12-28",
        "value": 63.57
      },
      {
        "date": "2025-12-29",
        "value": 62.36
      },
      {
        "date": "2025-12-30",
        "value": 61.12
      },
      {
        "date": "2025-12-31",
        "value": 60.04
      },
      {
        "date": "2026-01-01",
        "value": 59.13
      },
      {
        "date": "2026-01-02",
        "value": 58.1
      },
      {
        "date": "2026-01-03",
        "value": 57.02
      },
      {
        "date": "2026-01-04",
        "value": 55.71
      },
      {
        "date": "2026-01-05",
        "value": 54.2
      },
      {
        "date": "2026-01-06",
        "value": 52.73
      },
      {
        "date": "2026-01-07",
        "value": 51.37
      },
      {
        "date": "2026-01-08",
        "value": 50.23
      },
      {
        "date": "2026-01-09",
        "value": 49.29
      },
      {
        "date": "2026-01-10",
        "value": 48.28
      },
      {
        "date": "2026-01-11",
        "value": 47.25
      },
      {
        "date": "2026-01-12",
        "value": 46.35
      },
      {
        "date": "2026-01-13",
        "value": 45.38
      },
      {
        "date": "2026-01-14",
        "value": 44.54
      },
      {
        "date": "2026-01-15",
        "value": 43.88
      },
      {
        "date": "2026-01-16",
        "value": 43.15
      },
      {
        "date": "2026-01-17",
        "value": 42.42
      },
      {
        "date": "2026-01-18",
        "value": 41.75
      },
      {
        "date": "2026-01-19",
        "value": 40.81
      },
      {
        "date": "2026-01-20",
        "value": 39.83
      },
      {
        "date": "2026-01-21",
        "value": 39.04
      },
      {
        "date": "2026-01-22",
        "value": 38.01
      },
      {
        "date": "2026-01-23",
        "value": 37.1
      },
      {
        "date": "2026-01-24",
        "value": 36.38
      },
      {
        "date": "2026-01-25",
        "value": 35.57
      },
      {
        "date": "2026-01-26",
        "value": 34.53
      },
      {
        "date": "2026-01-27",
        "value": 33.67
      },
      {
        "date": "2026-01-28",
        "value": 32.73
      },
      {
        "date": "2026-01-29",
        "value": 31.89
      },
      {
        "date": "2026-01-30",
        "value": 31.2
      },
      {
        "date": "2026-01-31",
        "value": 30.67
      },
      {
        "date": "2026-02-01",
        "value": 30.18
      },
      {
        "date": "2026-02-02",
        "value": 29.52
      },
      {
        "date": "2026-02-03",
        "value": 29.0
      },
      {
        "date": "2026-02-04",
        "value": 28.5
      },
      {
        "date": "2026-02-05",
        "value": 28.06
      },
      {
        "date": "2026-02-06",
        "value": 27.67
      },
      {
        "date": "2026-02-07",
        "value": 27.36
      },
      {
        "date": "2026-02-08",
        "value": 26.99
      },
      {
        "date": "2026-02-09",
        "value": 26.45
      },
      {
        "date": "2026-02-10",
        "value": 26.09
      },
      {
        "date": "2026-02-11",
        "value": 25.74
      },
      {
        "date": "2026-02-12",
        "value": 25.36
      },
      {
        "date": "2026-02-13",
        "value": 24.98
      },
      {
        "date": "2026-02-14",
        "value": 24.5
      },
      {
        "date": "2026-02-15",
        "value": 24.04
      },
      {
        "date": "2026-02-16",
        "value": 23.56
      },
      {
        "date": "2026-02-17",
        "value": 22.99
      },
      {
        "date": "2026-02-18",
        "value": 22.47
      },
      {
        "date": "2026-02-19",
        "value": 21.82
      },
      {
        "date": "2026-02-20",
        "value": 21.32
      },
      {
        "date": "2026-02-21",
        "value": 21.14
      },
      {
        "date": "2026-02-22",
        "value": 21.08
      },
      {
        "date": "2026-02-23",
        "value": 21.08
      },
      {
        "date": "2026-02-24",
        "value": 20.97
      },
      {
        "date": "2026-02-25",
        "value": 21.01
      },
      {
        "date": "2026-02-26",
        "value": 21.14
      },
      {
        "date": "2026-02-27",
        "value": 21.38
      },
      {
        "date": "2026-02-28",
        "value": 21.54
      },
      {
        "date": "2026-03-01",
        "value": 21.65
      },
      {
        "date": "2026-03-02",
        "value": 21.69
      },
      {
        "date": "2026-03-03",
        "value": 21.65
      },
      {
        "date": "2026-03-04",
        "value": 21.62
      },
      {
        "date": "2026-03-05",
        "value": 21.72
      },
      {
        "date": "2026-03-06",
        "value": 21.75
      },
      {
        "date": "2026-03-07",
        "value": 21.86
      },
      {
        "date": "2026-03-08",
        "value": 21.98
      },
      {
        "date": "2026-03-09",
        "value": 21.92
      },
      {
        "date": "2026-03-10",
        "value": 21.89
      },
      {
        "date": "2026-03-11",
        "value": 21.91
      },
      {
        "date": "2026-03-12",
        "value": 21.91
      },
      {
        "date": "2026-03-13",
        "value": 21.99
      },
      {
        "date": "2026-03-14",
        "value": 21.94
      },
      {
        "date": "2026-03-15",
        "value": 22.01
      },
      {
        "date": "2026-03-16",
        "value": 22.0
      },
      {
        "date": "2026-03-17",
        "value": 22.11
      },
      {
        "date": "2026-03-18",
        "value": 21.99
      },
      {
        "date": "2026-03-19",
        "value": 21.84
      },
      {
        "date": "2026-03-20",
        "value": 21.85
      },
      {
        "date": "2026-03-21",
        "value": 21.98
      },
      {
        "date": "2026-03-22",
        "value": 22.07
      },
      {
        "date": "2026-03-23",
        "value": 21.96
      },
      {
        "date": "2026-03-24",
        "value": 22.07
      },
      {
        "date": "2026-03-25",
        "value": 22.08
      },
      {
        "date": "2026-03-26",
        "value": 21.86
      },
      {
        "date": "2026-03-27",
        "value": 21.67
      },
      {
        "date": "2026-03-28",
        "value": 21.71
      },
      {
        "date": "2026-03-29",
        "value": 21.86
      },
      {
        "date": "2026-03-30",
        "value": 21.88
      },
      {
        "date": "2026-03-31",
        "value": 21.81
      },
      {
        "date": "2026-04-01",
        "value": 22.06
      },
      {
        "date": "2026-04-02",
        "value": 21.97
      },
      {
        "date": "2026-04-03",
        "value": 22.07
      },
      {
        "date": "2026-04-04",
        "value": 22.43
      },
      {
        "date": "2026-04-05",
        "value": 22.78
      },
      {
        "date": "2026-04-06",
        "value": 23.1
      },
      {
        "date": "2026-04-07",
        "value": 23.53
      },
      {
        "date": "2026-04-08",
        "value": 24.02
      },
      {
        "date": "2026-04-09",
        "value": 24.52
      },
      {
        "date": "2026-04-10",
        "value": 25.04
      },
      {
        "date": "2026-04-11",
        "value": 25.5
      },
      {
        "date": "2026-04-12",
        "value": 25.85
      },
      {
        "date": "2026-04-13",
        "value": 25.93
      },
      {
        "date": "2026-04-14",
        "value": 26.05
      },
      {
        "date": "2026-04-15",
        "value": 26.28
      },
      {
        "date": "2026-04-16",
        "value": 26.63
      },
      {
        "date": "2026-04-17",
        "value": 27.06
      },
      {
        "date": "2026-04-18",
        "value": 27.55
      },
      {
        "date": "2026-04-19",
        "value": 27.97
      },
      {
        "date": "2026-04-20",
        "value": 28.27
      },
      {
        "date": "2026-04-21",
        "value": 28.47
      },
      {
        "date": "2026-04-22",
        "value": 28.81
      },
      {
        "date": "2026-04-23",
        "value": 29.13
      },
      {
        "date": "2026-04-24",
        "value": 29.53
      },
      {
        "date": "2026-04-25",
        "value": 30.06
      },
      {
        "date": "2026-04-26",
        "value": 30.53
      },
      {
        "date": "2026-04-27",
        "value": 30.99
      },
      {
        "date": "2026-04-28",
        "value": 31.44
      },
      {
        "date": "2026-04-29",
        "value": 31.91
      },
      {
        "date": "2026-04-30",
        "value": 32.35
      },
      {
        "date": "2026-05-01",
        "value": 32.88
      },
      {
        "date": "2026-05-02",
        "value": 33.51
      },
      {
        "date": "2026-05-03",
        "value": 34.08
      },
      {
        "date": "2026-05-04",
        "value": 34.54
      },
      {
        "date": "2026-05-05",
        "value": 34.88
      },
      {
        "date": "2026-05-06",
        "value": 34.93
      },
      {
        "date": "2026-05-07",
        "value": 34.96
      },
      {
        "date": "2026-05-08",
        "value": 35.38
      },
      {
        "date": "2026-05-09",
        "value": 35.81
      },
      {
        "date": "2026-05-10",
        "value": 36.2
      },
      {
        "date": "2026-05-11",
        "value": 36.45
      },
      {
        "date": "2026-05-12",
        "value": 36.63
      },
      {
        "date": "2026-05-13",
        "value": 36.85
      },
      {
        "date": "2026-05-14",
        "value": 37.07
      },
      {
        "date": "2026-05-15",
        "value": 37.16
      },
      {
        "date": "2026-05-16",
        "value": 37.34
      },
      {
        "date": "2026-05-17",
        "value": 37.55
      },
      {
        "date": "2026-05-18",
        "value": 37.64
      },
      {
        "date": "2026-05-19",
        "value": 37.78
      },
      {
        "date": "2026-05-20",
        "value": 37.74
      },
      {
        "date": "2026-05-21",
        "value": 37.78
      },
      {
        "date": "2026-05-22",
        "value": 38.1
      },
      {
        "date": "2026-05-23",
        "value": 38.58
      },
      {
        "date": "2026-05-24",
        "value": 39.09
      },
      {
        "date": "2026-05-25",
        "value": 39.44
      },
      {
        "date": "2026-05-26",
        "value": 39.73
      },
      {
        "date": "2026-05-27",
        "value": 40.01
      },
      {
        "date": "2026-05-28",
        "value": 40.3
      },
      {
        "date": "2026-05-29",
        "value": 40.69
      },
      {
        "date": "2026-05-30",
        "value": 41.23
      },
      {
        "date": "2026-05-31",
        "value": 41.88
      },
      {
        "date": "2026-06-01",
        "value": 42.05
      },
      {
        "date": "2026-06-02",
        "value": 42.29
      },
      {
        "date": "2026-06-03",
        "value": 42.4
      },
      {
        "date": "2026-06-04",
        "value": 42.6
      },
      {
        "date": "2026-06-05",
        "value": 42.8
      },
      {
        "date": "2026-06-06",
        "value": 43.12
      },
      {
        "date": "2026-06-07",
        "value": 43.48
      },
      {
        "date": "2026-06-08",
        "value": 43.8
      },
      {
        "date": "2026-06-09",
        "value": 43.99
      },
      {
        "date": "2026-06-10",
        "value": 44.09
      },
      {
        "date": "2026-06-11",
        "value": 44.22
      },
      {
        "date": "2026-06-12",
        "value": 44.58
      },
      {
        "date": "2026-06-13",
        "value": 45.0
      },
      {
        "date": "2026-06-14",
        "value": 45.43
      },
      {
        "date": "2026-06-15",
        "value": 45.87
      },
      {
        "date": "2026-06-16",
        "value": 46.28
      },
      {
        "date": "2026-06-17",
        "value": 46.66
      },
      {
        "date": "2026-06-18",
        "value": 47.03
      },
      {
        "date": "2026-06-19",
        "value": 47.31
      },
      {
        "date": "2026-06-20",
        "value": 47.59
      },
      {
        "date": "2026-06-21",
        "value": 47.85
      },
      {
        "date": "2026-06-22",
        "value": 48.0
      },
      {
        "date": "2026-06-23",
        "value": 48.11
      },
      {
        "date": "2026-06-24",
        "value": 48.25
      },
      {
        "date": "2026-06-25",
        "value": 48.36
      },
      {
        "date": "2026-06-26",
        "value": 48.61
      },
      {
        "date": "2026-06-27",
        "value": 48.87
      },
      {
        "date": "2026-06-28",
        "value": 49.15
      },
      {
        "date": "2026-06-29",
        "value": 49.23
      },
      {
        "date": "2026-06-30",
        "value": 49.44
      },
      {
        "date": "2026-07-01",
        "value": 49.53
      },
      {
        "date": "2026-07-02",
        "value": 49.67
      },
      {
        "date": "2026-07-03",
        "value": 49.79
      },
      {
        "date": "2026-07-04",
        "value": 50.04
      },
      {
        "date": "2026-07-05",
        "value": 50.28
      },
      {
        "date": "2026-07-06",
        "value": 50.41
      },
      {
        "date": "2026-07-07",
        "value": 50.6
      },
      {
        "date": "2026-07-08",
        "value": 50.73
      },
      {
        "date": "2026-07-09",
        "value": 50.78
      },
      {
        "date": "2026-07-10",
        "value": 50.82
      },
      {
        "date": "2026-07-11",
        "value": 51.14
      },
      {
        "date": "2026-07-12",
        "value": 51.51
      },
      {
        "date": "2026-07-13",
        "value": 51.73
      },
      {
        "date": "2026-07-14",
        "value": 51.91
      },
      {
        "date": "2026-07-15",
        "value": 52.09
      },
      {
        "date": "2026-07-16",
        "value": 52.12
      },
      {
        "date": "2026-07-17",
        "value": 52.23
      },
      {
        "date": "2026-07-18",
        "value": 52.61
      },
      {
        "date": "2026-07-19",
        "value": 53.01
      },
      {
        "date": "2026-07-20",
        "value": 53.21
      },
      {
        "date": "2026-07-21",
        "value": 53.33
      },
      {
        "date": "2026-07-22",
        "value": 53.54
      },
      {
        "date": "2026-07-23",
        "value": 53.74
      },
      {
        "date": "2026-07-24",
        "value": 53.98
      },
      {
        "date": "2026-07-25",
        "value": 54.25
      },
      {
        "date": "2026-07-26",
        "value": 54.68
      },
      {
        "date": "2026-07-27",
        "value": 55.02
      },
      {
        "date": "2026-07-28",
        "value": 55.35
      },
      {
        "date": "2026-07-29",
        "value": 55.74
      },
      {
        "date": "2026-07-30",
        "value": 56.17
      },
      {
        "date": "2026-07-31",
        "value": 56.57
      },
      {
        "date": "2026-08-01",
        "value": 57.05
      },
      {
        "date": "2026-08-02",
        "value": 57.52
      },
      {
        "date": "2026-08-03",
        "value": 57.88
      },
      {
        "date": "2026-08-04",
        "value": 58.24
      },
      {
        "date": "2026-08-05",
        "value": 58.71
      },
      {
        "date": "2026-08-06",
        "value": 59.15
      },
      {
        "date": "2026-08-07",
        "value": 59.54
      },
      {
        "date": "2026-08-08",
        "value": 59.99
      },
      {
        "date": "2026-08-09",
        "value": 60.43
      },
      {
        "date": "2026-08-10",
        "value": 60.9
      },
      {
        "date": "2026-08-11",
        "value": 61.34
      },
      {
        "date": "2026-08-12",
        "value": 61.79
      },
      {
        "date": "2026-08-13",
        "value": 62.28
      },
      {
        "date": "2026-08-14",
        "value": 62.71
      },
      {
        "date": "2026-08-15",
        "value": 63.19
      },
      {
        "date": "2026-08-16",
        "value": 63.67
      },
      {
        "date": "2026-08-17",
        "value": 64.03
      },
      {
        "date": "2026-08-18",
        "value": 64.46
      },
      {
        "date": "2026-08-19",
        "value": 64.78
      },
      {
        "date": "2026-08-20",
        "value": 65.22
      },
      {
        "date": "2026-08-21",
        "value": 65.72
      },
      {
        "date": "2026-08-22",
        "value": 66.26
      },
      {
        "date": "2026-08-23",
        "value": 66.81
      },
      {
        "date": "2026-08-24",
        "value": 67.33
      },
      {
        "date": "2026-08-25",
        "value": 67.83
      },
      {
        "date": "2026-08-26",
        "value": 68.33
      },
      {
        "date": "2026-08-27",
        "value": 68.87
      },
      {
        "date": "2026-08-28",
        "value": 69.42
      },
      {
        "date": "2026-08-29",
        "value": 70.08
      },
      {
        "date": "2026-08-30",
        "value": 70.71
      },
      {
        "date": "2026-08-31",
        "value": 71.31
      },
      {
        "date": "2026-09-01",
        "value": 71.72
      },
      {
        "date": "2026-09-02",
        "value": 72.11
      },
      {
        "date": "2026-09-03",
        "value": 72.52
      },
      {
        "date": "2026-09-04",
        "value": 73.02
      },
      {
        "date": "2026-09-05",
        "value": 73.41
      },
      {
        "date": "2026-09-06",
        "value": 73.89
      },
      {
        "date": "2026-09-07",
        "value": 74.26
      },
      {
        "date": "2026-09-08",
        "value": 74.69
      },
      {
        "date": "2026-09-09",
        "value": 75.05
      },
      {
        "date": "2026-09-10",
        "value": 75.4
      },
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
      },
      {
        "date": "2026-09-25",
        "value": 81.97
      },
      {
        "date": "2026-09-26",
        "value": 82.47
      },
      {
        "date": "2026-09-27",
        "value": 83.03
      },
      {
        "date": "2026-09-28",
        "value": 83.23
      }
    ],
    "lng_eu_sendout": [
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
        "value": 3897.8
      },
      {
        "date": "2026-09-25",
        "value": 4165.4
      },
      {
        "date": "2026-09-26",
        "value": 3647.7
      },
      {
        "date": "2026-09-27",
        "value": 3566.2
      },
      {
        "date": "2026-09-28",
        "value": 3631.5
      }
    ],
    "lng_fr_sendout": [
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
      },
      {
        "date": "2026-09-27",
        "value": 1178.6
      },
      {
        "date": "2026-09-28",
        "value": 967.7
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
    "oil_prices": {
      "brent": [
        {
          "date": "2025-09-25",
          "value": 70.48
        },
        {
          "date": "2025-09-26",
          "value": 71.15
        },
        {
          "date": "2025-09-29",
          "value": 69.0
        },
        {
          "date": "2025-09-30",
          "value": 68.52
        },
        {
          "date": "2025-10-01",
          "value": 66.67
        },
        {
          "date": "2025-10-02",
          "value": 65.44
        },
        {
          "date": "2025-10-03",
          "value": 66.13
        },
        {
          "date": "2025-10-06",
          "value": 67.09
        },
        {
          "date": "2025-10-07",
          "value": 67.1
        },
        {
          "date": "2025-10-08",
          "value": 67.42
        },
        {
          "date": "2025-10-09",
          "value": 67.23
        },
        {
          "date": "2025-10-10",
          "value": 64.41
        },
        {
          "date": "2025-10-13",
          "value": 64.15
        },
        {
          "date": "2025-10-14",
          "value": 63.0
        },
        {
          "date": "2025-10-15",
          "value": 62.33
        },
        {
          "date": "2025-10-16",
          "value": 61.08
        },
        {
          "date": "2025-10-17",
          "value": 61.23
        },
        {
          "date": "2025-10-20",
          "value": 60.71
        },
        {
          "date": "2025-10-21",
          "value": 61.0
        },
        {
          "date": "2025-10-22",
          "value": 62.28
        },
        {
          "date": "2025-10-23",
          "value": 66.32
        },
        {
          "date": "2025-10-24",
          "value": 65.8
        },
        {
          "date": "2025-10-27",
          "value": 65.52
        },
        {
          "date": "2025-10-28",
          "value": 64.03
        },
        {
          "date": "2025-10-29",
          "value": 65.01
        },
        {
          "date": "2025-10-30",
          "value": 65.11
        },
        {
          "date": "2025-10-31",
          "value": 65.44
        },
        {
          "date": "2025-11-03",
          "value": 65.79
        },
        {
          "date": "2025-11-04",
          "value": 65.04
        },
        {
          "date": "2025-11-05",
          "value": 63.54
        },
        {
          "date": "2025-11-06",
          "value": 63.41
        },
        {
          "date": "2025-11-07",
          "value": 63.72
        },
        {
          "date": "2025-11-10",
          "value": 63.01
        },
        {
          "date": "2025-11-11",
          "value": 63.86
        },
        {
          "date": "2025-11-12",
          "value": 61.88
        },
        {
          "date": "2025-11-13",
          "value": 62.14
        },
        {
          "date": "2025-11-14",
          "value": 63.45
        },
        {
          "date": "2025-11-17",
          "value": 63.16
        },
        {
          "date": "2025-11-18",
          "value": 64.86
        },
        {
          "date": "2025-11-19",
          "value": 63.78
        },
        {
          "date": "2025-11-20",
          "value": 63.64
        },
        {
          "date": "2025-11-21",
          "value": 62.78
        },
        {
          "date": "2025-11-24",
          "value": 64.83
        },
        {
          "date": "2025-11-25",
          "value": 63.99
        },
        {
          "date": "2025-11-26",
          "value": 64.81
        },
        {
          "date": "2025-11-27",
          "value": 64.18
        },
        {
          "date": "2025-11-28",
          "value": 64.07
        },
        {
          "date": "2025-12-01",
          "value": 64.22
        },
        {
          "date": "2025-12-02",
          "value": 63.37
        },
        {
          "date": "2025-12-03",
          "value": 63.75
        },
        {
          "date": "2025-12-04",
          "value": 64.15
        },
        {
          "date": "2025-12-05",
          "value": 64.42
        },
        {
          "date": "2025-12-08",
          "value": 63.3
        },
        {
          "date": "2025-12-09",
          "value": 62.62
        },
        {
          "date": "2025-12-10",
          "value": 63.12
        },
        {
          "date": "2025-12-11",
          "value": 61.87
        },
        {
          "date": "2025-12-12",
          "value": 62.11
        },
        {
          "date": "2025-12-15",
          "value": 61.55
        },
        {
          "date": "2025-12-16",
          "value": 59.93
        },
        {
          "date": "2025-12-17",
          "value": 60.61
        },
        {
          "date": "2025-12-18",
          "value": 60.69
        },
        {
          "date": "2025-12-19",
          "value": 61.35
        },
        {
          "date": "2025-12-22",
          "value": 62.22
        },
        {
          "date": "2025-12-23",
          "value": 63.7
        },
        {
          "date": "2025-12-24",
          "value": 63.7
        },
        {
          "date": "2025-12-29",
          "value": 63.1
        },
        {
          "date": "2025-12-30",
          "value": 62.3
        },
        {
          "date": "2025-12-31",
          "value": 61.35
        },
        {
          "date": "2026-01-02",
          "value": 61.98
        },
        {
          "date": "2026-01-05",
          "value": 63.0
        },
        {
          "date": "2026-01-06",
          "value": 62.1
        },
        {
          "date": "2026-01-07",
          "value": 61.08
        },
        {
          "date": "2026-01-08",
          "value": 63.34
        },
        {
          "date": "2026-01-09",
          "value": 65.11
        },
        {
          "date": "2026-01-12",
          "value": 65.4
        },
        {
          "date": "2026-01-13",
          "value": 67.58
        },
        {
          "date": "2026-01-14",
          "value": 68.87
        },
        {
          "date": "2026-01-15",
          "value": 66.16
        },
        {
          "date": "2026-01-16",
          "value": 66.97
        },
        {
          "date": "2026-01-19",
          "value": 66.91
        },
        {
          "date": "2026-01-20",
          "value": 67.68
        },
        {
          "date": "2026-01-21",
          "value": 66.72
        },
        {
          "date": "2026-01-22",
          "value": 65.46
        },
        {
          "date": "2026-01-23",
          "value": 68.16
        },
        {
          "date": "2026-01-26",
          "value": 67.7
        },
        {
          "date": "2026-01-27",
          "value": 70.28
        },
        {
          "date": "2026-01-28",
          "value": 70.9
        },
        {
          "date": "2026-01-29",
          "value": 71.0
        },
        {
          "date": "2026-01-30",
          "value": 72.25
        },
        {
          "date": "2026-02-02",
          "value": 67.72
        },
        {
          "date": "2026-02-03",
          "value": 70.01
        },
        {
          "date": "2026-02-04",
          "value": 71.15
        },
        {
          "date": "2026-02-05",
          "value": 69.87
        },
        {
          "date": "2026-02-06",
          "value": 70.45
        },
        {
          "date": "2026-02-09",
          "value": 71.19
        },
        {
          "date": "2026-02-10",
          "value": 71.01
        },
        {
          "date": "2026-02-11",
          "value": 71.52
        },
        {
          "date": "2026-02-12",
          "value": 69.8
        },
        {
          "date": "2026-02-13",
          "value": 69.96
        },
        {
          "date": "2026-02-16",
          "value": 70.81
        },
        {
          "date": "2026-02-17",
          "value": 69.77
        },
        {
          "date": "2026-02-18",
          "value": 71.78
        },
        {
          "date": "2026-02-19",
          "value": 73.17
        },
        {
          "date": "2026-02-20",
          "value": 72.75
        },
        {
          "date": "2026-02-23",
          "value": 71.9
        },
        {
          "date": "2026-02-24",
          "value": 71.21
        },
        {
          "date": "2026-02-25",
          "value": 70.69
        },
        {
          "date": "2026-02-26",
          "value": 71.66
        },
        {
          "date": "2026-02-27",
          "value": 71.32
        },
        {
          "date": "2026-03-02",
          "value": 77.24
        },
        {
          "date": "2026-03-03",
          "value": 83.28
        },
        {
          "date": "2026-03-04",
          "value": 81.56
        },
        {
          "date": "2026-03-05",
          "value": 88.59
        },
        {
          "date": "2026-03-06",
          "value": 95.74
        },
        {
          "date": "2026-03-09",
          "value": 94.35
        },
        {
          "date": "2026-03-10",
          "value": 89.84
        },
        {
          "date": "2026-03-11",
          "value": 90.98
        },
        {
          "date": "2026-03-12",
          "value": 102.38
        },
        {
          "date": "2026-03-13",
          "value": 103.23
        },
        {
          "date": "2026-03-16",
          "value": 101.04
        },
        {
          "date": "2026-03-17",
          "value": 108.39
        },
        {
          "date": "2026-03-18",
          "value": 118.09
        },
        {
          "date": "2026-03-19",
          "value": 111.05
        },
        {
          "date": "2026-03-20",
          "value": 118.42
        },
        {
          "date": "2026-03-23",
          "value": 103.79
        },
        {
          "date": "2026-03-24",
          "value": 108.42
        },
        {
          "date": "2026-03-25",
          "value": 109.14
        },
        {
          "date": "2026-03-26",
          "value": 113.39
        },
        {
          "date": "2026-03-27",
          "value": 121.47
        },
        {
          "date": "2026-03-30",
          "value": 121.88
        },
        {
          "date": "2026-03-31",
          "value": 126.69
        },
        {
          "date": "2026-04-01",
          "value": 119.56
        },
        {
          "date": "2026-04-02",
          "value": 127.61
        },
        {
          "date": "2026-04-07",
          "value": 138.21
        },
        {
          "date": "2026-04-08",
          "value": 122.11
        },
        {
          "date": "2026-04-09",
          "value": 119.03
        },
        {
          "date": "2026-04-10",
          "value": 119.07
        },
        {
          "date": "2026-04-13",
          "value": 123.28
        },
        {
          "date": "2026-04-14",
          "value": 118.69
        },
        {
          "date": "2026-04-15",
          "value": 114.93
        },
        {
          "date": "2026-04-16",
          "value": 116.63
        },
        {
          "date": "2026-04-17",
          "value": 98.63
        },
        {
          "date": "2026-04-20",
          "value": 103.4
        },
        {
          "date": "2026-04-21",
          "value": 106.14
        },
        {
          "date": "2026-04-22",
          "value": 113.44
        },
        {
          "date": "2026-04-23",
          "value": 113.25
        },
        {
          "date": "2026-04-24",
          "value": 111.86
        },
        {
          "date": "2026-04-27",
          "value": 113.89
        },
        {
          "date": "2026-04-28",
          "value": 117.62
        },
        {
          "date": "2026-04-29",
          "value": 124.16
        },
        {
          "date": "2026-04-30",
          "value": 124.24
        },
        {
          "date": "2026-05-01",
          "value": 118.26
        },
        {
          "date": "2026-05-05",
          "value": 114.51
        },
        {
          "date": "2026-05-06",
          "value": 103.7
        },
        {
          "date": "2026-05-07",
          "value": 101.82
        },
        {
          "date": "2026-05-08",
          "value": 103.48
        },
        {
          "date": "2026-05-11",
          "value": 106.11
        },
        {
          "date": "2026-05-12",
          "value": 111.37
        },
        {
          "date": "2026-05-13",
          "value": 110.28
        },
        {
          "date": "2026-05-14",
          "value": 110.91
        },
        {
          "date": "2026-05-15",
          "value": 113.96
        },
        {
          "date": "2026-05-18",
          "value": 116.73
        },
        {
          "date": "2026-05-19",
          "value": 114.64
        },
        {
          "date": "2026-05-20",
          "value": 108.93
        },
        {
          "date": "2026-05-21",
          "value": 105.84
        },
        {
          "date": "2026-05-22",
          "value": 106.9
        },
        {
          "date": "2026-05-26",
          "value": 102.75
        },
        {
          "date": "2026-05-27",
          "value": 97.11
        },
        {
          "date": "2026-05-28",
          "value": 95.47
        },
        {
          "date": "2026-05-29",
          "value": 92.88
        },
        {
          "date": "2026-06-01",
          "value": 98.29
        },
        {
          "date": "2026-06-02",
          "value": 98.49
        },
        {
          "date": "2026-06-03",
          "value": 101.69
        },
        {
          "date": "2026-06-04",
          "value": 98.98
        },
        {
          "date": "2026-06-05",
          "value": 97.29
        },
        {
          "date": "2026-06-08",
          "value": 97.46
        },
        {
          "date": "2026-06-09",
          "value": 94.15
        },
        {
          "date": "2026-06-10",
          "value": 95.73
        },
        {
          "date": "2026-06-11",
          "value": 92.84
        },
        {
          "date": "2026-06-12",
          "value": 88.64
        },
        {
          "date": "2026-06-15",
          "value": 84.36
        },
        {
          "date": "2026-06-16",
          "value": 80.5
        },
        {
          "date": "2026-06-17",
          "value": 80.33
        },
        {
          "date": "2026-06-18",
          "value": 79.35
        },
        {
          "date": "2026-06-19",
          "value": 80.46
        },
        {
          "date": "2026-06-22",
          "value": 76.49
        },
        {
          "date": "2026-06-23",
          "value": 75.69
        },
        {
          "date": "2026-06-24",
          "value": 72.09
        },
        {
          "date": "2026-06-25",
          "value": 73.74
        },
        {
          "date": "2026-06-26",
          "value": 70.16
        },
        {
          "date": "2026-06-29",
          "value": 71.59
        },
        {
          "date": "2026-06-30",
          "value": 70.46
        },
        {
          "date": "2026-07-01",
          "value": 69.24
        },
        {
          "date": "2026-07-02",
          "value": 68.53
        },
        {
          "date": "2026-07-03",
          "value": 68.68
        },
        {
          "date": "2026-07-06",
          "value": 69.56
        },
        {
          "date": "2026-07-07",
          "value": 71.78
        },
        {
          "date": "2026-07-08",
          "value": 76.5
        },
        {
          "date": "2026-07-09",
          "value": 74.46
        },
        {
          "date": "2026-07-10",
          "value": 74.34
        },
        {
          "date": "2026-07-13",
          "value": 81.62
        },
        {
          "date": "2026-07-14",
          "value": 83.69
        },
        {
          "date": "2026-07-15",
          "value": 83.08
        },
        {
          "date": "2026-07-16",
          "value": 81.23
        },
        {
          "date": "2026-07-17",
          "value": 85.01
        },
        {
          "date": "2026-07-20",
          "value": 86.99
        },
        {
          "date": "2026-07-21",
          "value": 93.85
        },
        {
          "date": "2026-07-22",
          "value": 94.12
        },
        {
          "date": "2026-07-23",
          "value": 105.32
        },
        {
          "date": "2026-07-24",
          "value": 100.31
        },
        {
          "date": "2026-07-27",
          "value": 91.82
        },
        {
          "date": "2026-07-28",
          "value": 85.51
        },
        {
          "date": "2026-07-29",
          "value": 91.95
        },
        {
          "date": "2026-07-30",
          "value": 91.91
        },
        {
          "date": "2026-07-31",
          "value": 96.95
        },
        {
          "date": "2026-08-03",
          "value": 88.9
        },
        {
          "date": "2026-08-04",
          "value": 86.47
        },
        {
          "date": "2026-08-05",
          "value": 86.65
        },
        {
          "date": "2026-08-06",
          "value": 89.65
        },
        {
          "date": "2026-08-07",
          "value": 87.62
        },
        {
          "date": "2026-08-10",
          "value": 92.74
        },
        {
          "date": "2026-08-11",
          "value": 93.26
        },
        {
          "date": "2026-08-12",
          "value": 92.52
        },
        {
          "date": "2026-08-13",
          "value": 92.03
        },
        {
          "date": "2026-08-14",
          "value": 92.02
        },
        {
          "date": "2026-08-17",
          "value": 92.43
        },
        {
          "date": "2026-08-18",
          "value": 95.29
        },
        {
          "date": "2026-08-19",
          "value": 92.37
        },
        {
          "date": "2026-08-20",
          "value": 94.0
        },
        {
          "date": "2026-08-21",
          "value": 96.92
        },
        {
          "date": "2026-08-24",
          "value": 92.71
        },
        {
          "date": "2026-08-25",
          "value": 88.24
        },
        {
          "date": "2026-08-26",
          "value": 87.77
        },
        {
          "date": "2026-08-27",
          "value": 90.18
        },
        {
          "date": "2026-08-28",
          "value": 89.75
        },
        {
          "date": "2026-09-01",
          "value": 96.02
        },
        {
          "date": "2026-09-02",
          "value": 97.59
        },
        {
          "date": "2026-09-03",
          "value": 100.52
        },
        {
          "date": "2026-09-04",
          "value": 102.24
        },
        {
          "date": "2026-09-07",
          "value": 104.47
        },
        {
          "date": "2026-09-08",
          "value": 106.12
        },
        {
          "date": "2026-09-09",
          "value": 109.51
        },
        {
          "date": "2026-09-10",
          "value": 120.98
        },
        {
          "date": "2026-09-11",
          "value": 118.06
        },
        {
          "date": "2026-09-14",
          "value": 121.25
        },
        {
          "date": "2026-09-15",
          "value": 130.8
        },
        {
          "date": "2026-09-16",
          "value": 127.84
        },
        {
          "date": "2026-09-17",
          "value": 121.18
        },
        {
          "date": "2026-09-18",
          "value": 119.66
        },
        {
          "date": "2026-09-21",
          "value": 116.15
        },
        {
          "date": "2026-09-22",
          "value": 114.89
        }
      ],
      "wti": [
        {
          "date": "2025-09-25",
          "value": 65.51
        },
        {
          "date": "2025-09-26",
          "value": 66.5
        },
        {
          "date": "2025-09-29",
          "value": 64.27
        },
        {
          "date": "2025-09-30",
          "value": 63.17
        },
        {
          "date": "2025-10-01",
          "value": 62.59
        },
        {
          "date": "2025-10-02",
          "value": 61.28
        },
        {
          "date": "2025-10-03",
          "value": 61.65
        },
        {
          "date": "2025-10-06",
          "value": 62.49
        },
        {
          "date": "2025-10-07",
          "value": 62.52
        },
        {
          "date": "2025-10-08",
          "value": 63.37
        },
        {
          "date": "2025-10-09",
          "value": 62.36
        },
        {
          "date": "2025-10-10",
          "value": 59.75
        },
        {
          "date": "2025-10-14",
          "value": 59.52
        },
        {
          "date": "2025-10-15",
          "value": 59.08
        },
        {
          "date": "2025-10-16",
          "value": 58.29
        },
        {
          "date": "2025-10-17",
          "value": 58.3
        },
        {
          "date": "2025-10-20",
          "value": 58.34
        },
        {
          "date": "2025-10-21",
          "value": 58.66
        },
        {
          "date": "2025-10-22",
          "value": 59.3
        },
        {
          "date": "2025-10-23",
          "value": 62.44
        },
        {
          "date": "2025-10-24",
          "value": 62.27
        },
        {
          "date": "2025-10-27",
          "value": 62.13
        },
        {
          "date": "2025-10-28",
          "value": 60.97
        },
        {
          "date": "2025-10-29",
          "value": 61.26
        },
        {
          "date": "2025-10-30",
          "value": 61.36
        },
        {
          "date": "2025-10-31",
          "value": 61.75
        },
        {
          "date": "2025-11-03",
          "value": 61.79
        },
        {
          "date": "2025-11-04",
          "value": 61.38
        },
        {
          "date": "2025-11-05",
          "value": 60.4
        },
        {
          "date": "2025-11-06",
          "value": 60.24
        },
        {
          "date": "2025-11-07",
          "value": 60.54
        },
        {
          "date": "2025-11-10",
          "value": 60.94
        },
        {
          "date": "2025-11-12",
          "value": 59.3
        },
        {
          "date": "2025-11-13",
          "value": 59.54
        },
        {
          "date": "2025-11-14",
          "value": 60.87
        },
        {
          "date": "2025-11-17",
          "value": 60.66
        },
        {
          "date": "2025-11-18",
          "value": 61.51
        },
        {
          "date": "2025-11-19",
          "value": 60.27
        },
        {
          "date": "2025-11-20",
          "value": 60.07
        },
        {
          "date": "2025-11-21",
          "value": 58.86
        },
        {
          "date": "2025-11-24",
          "value": 59.11
        },
        {
          "date": "2025-11-25",
          "value": 58.25
        },
        {
          "date": "2025-11-26",
          "value": 58.81
        },
        {
          "date": "2025-11-28",
          "value": 58.58
        },
        {
          "date": "2025-12-01",
          "value": 59.47
        },
        {
          "date": "2025-12-02",
          "value": 58.81
        },
        {
          "date": "2025-12-03",
          "value": 59.09
        },
        {
          "date": "2025-12-04",
          "value": 59.82
        },
        {
          "date": "2025-12-05",
          "value": 60.23
        },
        {
          "date": "2025-12-08",
          "value": 59.04
        },
        {
          "date": "2025-12-09",
          "value": 58.4
        },
        {
          "date": "2025-12-10",
          "value": 58.67
        },
        {
          "date": "2025-12-11",
          "value": 57.76
        },
        {
          "date": "2025-12-12",
          "value": 57.61
        },
        {
          "date": "2025-12-15",
          "value": 56.97
        },
        {
          "date": "2025-12-16",
          "value": 55.44
        },
        {
          "date": "2025-12-17",
          "value": 56.07
        },
        {
          "date": "2025-12-18",
          "value": 56.22
        },
        {
          "date": "2025-12-19",
          "value": 56.8
        },
        {
          "date": "2025-12-22",
          "value": 58.18
        },
        {
          "date": "2025-12-23",
          "value": 58.55
        },
        {
          "date": "2025-12-24",
          "value": 58.72
        },
        {
          "date": "2025-12-26",
          "value": 56.6
        },
        {
          "date": "2025-12-29",
          "value": 57.89
        },
        {
          "date": "2025-12-30",
          "value": 57.79
        },
        {
          "date": "2025-12-31",
          "value": 57.26
        },
        {
          "date": "2026-01-02",
          "value": 57.21
        },
        {
          "date": "2026-01-05",
          "value": 58.1
        },
        {
          "date": "2026-01-06",
          "value": 56.97
        },
        {
          "date": "2026-01-07",
          "value": 56.01
        },
        {
          "date": "2026-01-08",
          "value": 57.74
        },
        {
          "date": "2026-01-09",
          "value": 58.96
        },
        {
          "date": "2026-01-12",
          "value": 59.39
        },
        {
          "date": "2026-01-13",
          "value": 60.85
        },
        {
          "date": "2026-01-14",
          "value": 61.84
        },
        {
          "date": "2026-01-15",
          "value": 59.13
        },
        {
          "date": "2026-01-16",
          "value": 59.4
        },
        {
          "date": "2026-01-20",
          "value": 60.3
        },
        {
          "date": "2026-01-21",
          "value": 60.38
        },
        {
          "date": "2026-01-22",
          "value": 59.24
        },
        {
          "date": "2026-01-23",
          "value": 60.7
        },
        {
          "date": "2026-01-26",
          "value": 60.46
        },
        {
          "date": "2026-01-27",
          "value": 62.04
        },
        {
          "date": "2026-01-28",
          "value": 62.75
        },
        {
          "date": "2026-01-29",
          "value": 64.77
        },
        {
          "date": "2026-01-30",
          "value": 64.5
        },
        {
          "date": "2026-02-02",
          "value": 61.6
        },
        {
          "date": "2026-02-03",
          "value": 62.62
        },
        {
          "date": "2026-02-04",
          "value": 64.56
        },
        {
          "date": "2026-02-05",
          "value": 62.9
        },
        {
          "date": "2026-02-06",
          "value": 63.77
        },
        {
          "date": "2026-02-09",
          "value": 64.53
        },
        {
          "date": "2026-02-10",
          "value": 64.2
        },
        {
          "date": "2026-02-11",
          "value": 64.8
        },
        {
          "date": "2026-02-12",
          "value": 63.08
        },
        {
          "date": "2026-02-13",
          "value": 63.05
        },
        {
          "date": "2026-02-17",
          "value": 62.53
        },
        {
          "date": "2026-02-18",
          "value": 65.33
        },
        {
          "date": "2026-02-19",
          "value": 66.66
        },
        {
          "date": "2026-02-20",
          "value": 66.69
        },
        {
          "date": "2026-02-23",
          "value": 66.36
        },
        {
          "date": "2026-02-24",
          "value": 65.62
        },
        {
          "date": "2026-02-25",
          "value": 65.3
        },
        {
          "date": "2026-02-26",
          "value": 65.1
        },
        {
          "date": "2026-02-27",
          "value": 66.96
        },
        {
          "date": "2026-03-02",
          "value": 71.13
        },
        {
          "date": "2026-03-03",
          "value": 74.48
        },
        {
          "date": "2026-03-04",
          "value": 74.58
        },
        {
          "date": "2026-03-05",
          "value": 80.88
        },
        {
          "date": "2026-03-06",
          "value": 90.77
        },
        {
          "date": "2026-03-09",
          "value": 94.65
        },
        {
          "date": "2026-03-10",
          "value": 83.71
        },
        {
          "date": "2026-03-11",
          "value": 86.8
        },
        {
          "date": "2026-03-12",
          "value": 95.61
        },
        {
          "date": "2026-03-13",
          "value": 98.48
        },
        {
          "date": "2026-03-16",
          "value": 93.39
        },
        {
          "date": "2026-03-17",
          "value": 96.01
        },
        {
          "date": "2026-03-18",
          "value": 96.12
        },
        {
          "date": "2026-03-19",
          "value": 96.11
        },
        {
          "date": "2026-03-20",
          "value": 98.71
        },
        {
          "date": "2026-03-23",
          "value": 89.33
        },
        {
          "date": "2026-03-24",
          "value": 93.18
        },
        {
          "date": "2026-03-25",
          "value": 91.51
        },
        {
          "date": "2026-03-26",
          "value": 96.18
        },
        {
          "date": "2026-03-27",
          "value": 101.26
        },
        {
          "date": "2026-03-30",
          "value": 104.69
        },
        {
          "date": "2026-03-31",
          "value": 102.86
        },
        {
          "date": "2026-04-01",
          "value": 101.9
        },
        {
          "date": "2026-04-02",
          "value": 113.23
        },
        {
          "date": "2026-04-06",
          "value": 114.01
        },
        {
          "date": "2026-04-07",
          "value": 114.58
        },
        {
          "date": "2026-04-08",
          "value": 96.17
        },
        {
          "date": "2026-04-09",
          "value": 99.62
        },
        {
          "date": "2026-04-10",
          "value": 98.34
        },
        {
          "date": "2026-04-13",
          "value": 100.72
        },
        {
          "date": "2026-04-14",
          "value": 93.07
        },
        {
          "date": "2026-04-15",
          "value": 93.04
        },
        {
          "date": "2026-04-16",
          "value": 96.46
        },
        {
          "date": "2026-04-17",
          "value": 85.91
        },
        {
          "date": "2026-04-20",
          "value": 91.06
        },
        {
          "date": "2026-04-21",
          "value": 93.64
        },
        {
          "date": "2026-04-22",
          "value": 94.76
        },
        {
          "date": "2026-04-23",
          "value": 99.27
        },
        {
          "date": "2026-04-24",
          "value": 98.42
        },
        {
          "date": "2026-04-27",
          "value": 99.89
        },
        {
          "date": "2026-04-28",
          "value": 103.45
        },
        {
          "date": "2026-04-29",
          "value": 110.47
        },
        {
          "date": "2026-04-30",
          "value": 108.64
        },
        {
          "date": "2026-05-01",
          "value": 105.38
        },
        {
          "date": "2026-05-04",
          "value": 109.76
        },
        {
          "date": "2026-05-05",
          "value": 105.66
        },
        {
          "date": "2026-05-06",
          "value": 98.75
        },
        {
          "date": "2026-05-07",
          "value": 98.38
        },
        {
          "date": "2026-05-08",
          "value": 98.87
        },
        {
          "date": "2026-05-11",
          "value": 101.56
        },
        {
          "date": "2026-05-12",
          "value": 105.78
        },
        {
          "date": "2026-05-13",
          "value": 104.52
        },
        {
          "date": "2026-05-14",
          "value": 104.66
        },
        {
          "date": "2026-05-15",
          "value": 108.99
        },
        {
          "date": "2026-05-18",
          "value": 112.25
        },
        {
          "date": "2026-05-19",
          "value": 112.09
        },
        {
          "date": "2026-05-20",
          "value": 101.69
        },
        {
          "date": "2026-05-21",
          "value": 100.2
        },
        {
          "date": "2026-05-22",
          "value": 100.35
        },
        {
          "date": "2026-05-26",
          "value": 97.63
        },
        {
          "date": "2026-05-27",
          "value": 92.35
        },
        {
          "date": "2026-05-28",
          "value": 92.65
        },
        {
          "date": "2026-05-29",
          "value": 91.16
        },
        {
          "date": "2026-06-01",
          "value": 95.96
        },
        {
          "date": "2026-06-02",
          "value": 97.47
        },
        {
          "date": "2026-06-03",
          "value": 99.76
        },
        {
          "date": "2026-06-04",
          "value": 96.83
        },
        {
          "date": "2026-06-05",
          "value": 94.32
        },
        {
          "date": "2026-06-08",
          "value": 95.0
        },
        {
          "date": "2026-06-09",
          "value": 91.9
        },
        {
          "date": "2026-06-10",
          "value": 93.68
        },
        {
          "date": "2026-06-11",
          "value": 91.58
        },
        {
          "date": "2026-06-12",
          "value": 88.62
        },
        {
          "date": "2026-06-15",
          "value": 84.65
        },
        {
          "date": "2026-06-16",
          "value": 79.8
        },
        {
          "date": "2026-06-17",
          "value": 80.65
        },
        {
          "date": "2026-06-18",
          "value": 80.35
        },
        {
          "date": "2026-06-22",
          "value": 78.94
        },
        {
          "date": "2026-06-23",
          "value": 74.62
        },
        {
          "date": "2026-06-24",
          "value": 71.42
        },
        {
          "date": "2026-06-25",
          "value": 72.67
        },
        {
          "date": "2026-06-26",
          "value": 70.3
        },
        {
          "date": "2026-06-29",
          "value": 71.87
        },
        {
          "date": "2026-06-30",
          "value": 70.56
        },
        {
          "date": "2026-07-01",
          "value": 69.74
        },
        {
          "date": "2026-07-02",
          "value": 69.73
        },
        {
          "date": "2026-07-06",
          "value": 69.6
        },
        {
          "date": "2026-07-07",
          "value": 71.53
        },
        {
          "date": "2026-07-08",
          "value": 74.56
        },
        {
          "date": "2026-07-09",
          "value": 73.15
        },
        {
          "date": "2026-07-10",
          "value": 72.45
        },
        {
          "date": "2026-07-13",
          "value": 79.2
        },
        {
          "date": "2026-07-14",
          "value": 80.44
        },
        {
          "date": "2026-07-15",
          "value": 80.73
        },
        {
          "date": "2026-07-16",
          "value": 80.03
        },
        {
          "date": "2026-07-17",
          "value": 83.43
        },
        {
          "date": "2026-07-20",
          "value": 84.38
        },
        {
          "date": "2026-07-21",
          "value": 86.04
        },
        {
          "date": "2026-07-22",
          "value": 87.66
        },
        {
          "date": "2026-07-23",
          "value": 93.08
        },
        {
          "date": "2026-07-24",
          "value": 91.74
        },
        {
          "date": "2026-07-27",
          "value": 84.25
        },
        {
          "date": "2026-07-28",
          "value": 80.91
        },
        {
          "date": "2026-07-29",
          "value": 86.08
        },
        {
          "date": "2026-07-30",
          "value": 85.15
        },
        {
          "date": "2026-07-31",
          "value": 86.16
        },
        {
          "date": "2026-08-03",
          "value": 81.96
        },
        {
          "date": "2026-08-04",
          "value": 77.33
        },
        {
          "date": "2026-08-05",
          "value": 76.78
        },
        {
          "date": "2026-08-06",
          "value": 78.88
        },
        {
          "date": "2026-08-07",
          "value": 79.77
        },
        {
          "date": "2026-08-10",
          "value": 83.76
        },
        {
          "date": "2026-08-11",
          "value": 84.77
        },
        {
          "date": "2026-08-12",
          "value": 84.97
        },
        {
          "date": "2026-08-13",
          "value": 82.77
        },
        {
          "date": "2026-08-14",
          "value": 83.99
        },
        {
          "date": "2026-08-17",
          "value": 86.04
        },
        {
          "date": "2026-08-18",
          "value": 86.48
        },
        {
          "date": "2026-08-19",
          "value": 87.28
        },
        {
          "date": "2026-08-20",
          "value": 89.75
        },
        {
          "date": "2026-08-21",
          "value": 87.21
        },
        {
          "date": "2026-08-24",
          "value": 86.34
        },
        {
          "date": "2026-08-25",
          "value": 83.9
        },
        {
          "date": "2026-08-26",
          "value": 83.46
        },
        {
          "date": "2026-08-27",
          "value": 84.81
        },
        {
          "date": "2026-08-28",
          "value": 84.57
        },
        {
          "date": "2026-08-31",
          "value": 87.03
        },
        {
          "date": "2026-09-01",
          "value": 91.48
        },
        {
          "date": "2026-09-02",
          "value": 92.15
        },
        {
          "date": "2026-09-03",
          "value": 92.55
        },
        {
          "date": "2026-09-04",
          "value": 92.69
        },
        {
          "date": "2026-09-08",
          "value": 94.21
        },
        {
          "date": "2026-09-09",
          "value": 97.26
        },
        {
          "date": "2026-09-10",
          "value": 103.57
        },
        {
          "date": "2026-09-11",
          "value": 101.27
        },
        {
          "date": "2026-09-14",
          "value": 102.42
        },
        {
          "date": "2026-09-15",
          "value": 107.02
        },
        {
          "date": "2026-09-16",
          "value": 103.62
        },
        {
          "date": "2026-09-17",
          "value": 103.21
        },
        {
          "date": "2026-09-18",
          "value": 101.44
        },
        {
          "date": "2026-09-21",
          "value": 96.97
        },
        {
          "date": "2026-09-22",
          "value": 96.41
        }
      ]
    },
    "power_fr": [
      {
        "at": "2026-09-29T01:15:00+00:00",
        "bioenergies": 1052,
        "charbon": 0,
        "ech_physiques": -10076,
        "eolien": 4958,
        "fioul": 37,
        "gaz": 2593,
        "hydraulique": 2346,
        "load": 34698,
        "nucleaire": 33903,
        "pompage": -15,
        "prevision_j": 34900,
        "prevision_j1": 34900,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-29T01:30:00+00:00",
        "bioenergies": 1058,
        "charbon": 0,
        "ech_physiques": -10255,
        "eolien": 4946,
        "fioul": 37,
        "gaz": 2546,
        "hydraulique": 2331,
        "load": 34219,
        "nucleaire": 33932,
        "pompage": -187,
        "prevision_j": 34500,
        "prevision_j1": 34500,
        "solaire": 0,
        "taux_co2": 36
      },
      {
        "at": "2026-09-29T01:45:00+00:00",
        "bioenergies": 1060,
        "charbon": 0,
        "ech_physiques": -10224,
        "eolien": 4980,
        "fioul": 37,
        "gaz": 2232,
        "hydraulique": 2344,
        "load": 33973,
        "nucleaire": 33951,
        "pompage": -194,
        "prevision_j": 34350,
        "prevision_j1": 34350,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-29T02:00:00+00:00",
        "bioenergies": 1060,
        "charbon": 0,
        "ech_physiques": -9931,
        "eolien": 4894,
        "fioul": 37,
        "gaz": 2229,
        "hydraulique": 2325,
        "load": 34048,
        "nucleaire": 33993,
        "pompage": -361,
        "prevision_j": 34200,
        "prevision_j1": 34200,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-29T02:15:00+00:00",
        "bioenergies": 1057,
        "charbon": 0,
        "ech_physiques": -9727,
        "eolien": 4854,
        "fioul": 37,
        "gaz": 2233,
        "hydraulique": 2299,
        "load": 34058,
        "nucleaire": 34057,
        "pompage": -598,
        "prevision_j": 34300,
        "prevision_j1": 34300,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-29T02:30:00+00:00",
        "bioenergies": 1053,
        "charbon": 0,
        "ech_physiques": -9710,
        "eolien": 4840,
        "fioul": 37,
        "gaz": 2220,
        "hydraulique": 2295,
        "load": 34016,
        "nucleaire": 34091,
        "pompage": -598,
        "prevision_j": 34400,
        "prevision_j1": 34400,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-29T02:45:00+00:00",
        "bioenergies": 1050,
        "charbon": 0,
        "ech_physiques": -9446,
        "eolien": 4755,
        "fioul": 37,
        "gaz": 2222,
        "hydraulique": 2252,
        "load": 34068,
        "nucleaire": 34162,
        "pompage": -597,
        "prevision_j": 34550,
        "prevision_j1": 34550,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-29T03:00:00+00:00",
        "bioenergies": 1049,
        "charbon": 0,
        "ech_physiques": -9231,
        "eolien": 4870,
        "fioul": 37,
        "gaz": 2160,
        "hydraulique": 2347,
        "load": 34540,
        "nucleaire": 34186,
        "pompage": -598,
        "prevision_j": 34700,
        "prevision_j1": 34700,
        "solaire": 0,
        "taux_co2": 33
      },
      {
        "at": "2026-09-29T03:15:00+00:00",
        "bioenergies": 1042,
        "charbon": 0,
        "ech_physiques": -9381,
        "eolien": 4934,
        "fioul": 37,
        "gaz": 2159,
        "hydraulique": 2660,
        "load": 35160,
        "nucleaire": 34280,
        "pompage": -428,
        "prevision_j": 35250,
        "prevision_j1": 35350,
        "solaire": 0,
        "taux_co2": 32
      },
      {
        "at": "2026-09-29T03:30:00+00:00",
        "bioenergies": 1049,
        "charbon": 0,
        "ech_physiques": -9404,
        "eolien": 5119,
        "fioul": 37,
        "gaz": 2145,
        "hydraulique": 2665,
        "load": 35509,
        "nucleaire": 34254,
        "pompage": -186,
        "prevision_j": 35800,
        "prevision_j1": 36000,
        "solaire": 0,
        "taux_co2": 32
      },
      {
        "at": "2026-09-29T03:45:00+00:00",
        "bioenergies": 1047,
        "charbon": 0,
        "ech_physiques": -9667,
        "eolien": 5419,
        "fioul": 37,
        "gaz": 2321,
        "hydraulique": 2761,
        "load": 36122,
        "nucleaire": 34306,
        "pompage": -5,
        "prevision_j": 36550,
        "prevision_j1": 36750,
        "solaire": 0,
        "taux_co2": 33
      },
      {
        "at": "2026-09-29T04:00:00+00:00",
        "bioenergies": 1045,
        "charbon": 0,
        "ech_physiques": -9187,
        "eolien": 5640,
        "fioul": 36,
        "gaz": 2803,
        "hydraulique": 2804,
        "load": 37277,
        "nucleaire": 34276,
        "pompage": -5,
        "prevision_j": 37300,
        "prevision_j1": 37500,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-29T04:15:00+00:00",
        "bioenergies": 1046,
        "charbon": 0,
        "ech_physiques": -8280,
        "eolien": 5659,
        "fioul": 37,
        "gaz": 3119,
        "hydraulique": 3086,
        "load": 38945,
        "nucleaire": 34299,
        "pompage": -4,
        "prevision_j": 38600,
        "prevision_j1": 38800,
        "solaire": 0,
        "taux_co2": 40
      },
      {
        "at": "2026-09-29T04:30:00+00:00",
        "bioenergies": 1046,
        "charbon": 0,
        "ech_physiques": -7959,
        "eolien": 5636,
        "fioul": 37,
        "gaz": 3122,
        "hydraulique": 3390,
        "load": 39601,
        "nucleaire": 34278,
        "pompage": 0,
        "prevision_j": 39900,
        "prevision_j1": 40100,
        "solaire": 0,
        "taux_co2": 40
      },
      {
        "at": "2026-09-29T04:45:00+00:00",
        "bioenergies": 1052,
        "charbon": 0,
        "ech_physiques": -7496,
        "eolien": 5647,
        "fioul": 37,
        "gaz": 3357,
        "hydraulique": 3579,
        "load": 40550,
        "nucleaire": 34274,
        "pompage": 0,
        "prevision_j": 41100,
        "prevision_j1": 41300,
        "solaire": 0,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T05:00:00+00:00",
        "bioenergies": 1055,
        "charbon": 0,
        "ech_physiques": -6967,
        "eolien": 5720,
        "fioul": 37,
        "gaz": 3579,
        "hydraulique": 3936,
        "load": 41962,
        "nucleaire": 34254,
        "pompage": -1,
        "prevision_j": 42300,
        "prevision_j1": 42500,
        "solaire": 209,
        "taux_co2": 43
      },
      {
        "at": "2026-09-29T05:15:00+00:00",
        "bioenergies": 1054,
        "charbon": 0,
        "ech_physiques": -6846,
        "eolien": 5865,
        "fioul": 37,
        "gaz": 3587,
        "hydraulique": 5065,
        "load": 43379,
        "nucleaire": 34274,
        "pompage": 0,
        "prevision_j": 43150,
        "prevision_j1": 43350,
        "solaire": 212,
        "taux_co2": 42
      },
      {
        "at": "2026-09-29T05:30:00+00:00",
        "bioenergies": 1044,
        "charbon": 0,
        "ech_physiques": -6692,
        "eolien": 5898,
        "fioul": 36,
        "gaz": 3714,
        "hydraulique": 5248,
        "load": 43975,
        "nucleaire": 34203,
        "pompage": 0,
        "prevision_j": 44000,
        "prevision_j1": 44200,
        "solaire": 211,
        "taux_co2": 42
      },
      {
        "at": "2026-09-29T05:45:00+00:00",
        "bioenergies": 1052,
        "charbon": 0,
        "ech_physiques": -6361,
        "eolien": 5950,
        "fioul": 37,
        "gaz": 3713,
        "hydraulique": 5278,
        "load": 44456,
        "nucleaire": 34232,
        "pompage": -1,
        "prevision_j": 44400,
        "prevision_j1": 44600,
        "solaire": 220,
        "taux_co2": 42
      },
      {
        "at": "2026-09-29T06:00:00+00:00",
        "bioenergies": 1058,
        "charbon": 0,
        "ech_physiques": -5691,
        "eolien": 6036,
        "fioul": 37,
        "gaz": 3709,
        "hydraulique": 5059,
        "load": 44976,
        "nucleaire": 34271,
        "pompage": -1,
        "prevision_j": 44800,
        "prevision_j1": 45000,
        "solaire": 369,
        "taux_co2": 42
      },
      {
        "at": "2026-09-29T06:15:00+00:00",
        "bioenergies": 1062,
        "charbon": 0,
        "ech_physiques": -5362,
        "eolien": 6232,
        "fioul": 37,
        "gaz": 3648,
        "hydraulique": 4685,
        "load": 45603,
        "nucleaire": 34316,
        "pompage": 0,
        "prevision_j": 45000,
        "prevision_j1": 45200,
        "solaire": 699,
        "taux_co2": 42
      },
      {
        "at": "2026-09-29T06:30:00+00:00",
        "bioenergies": 1065,
        "charbon": 0,
        "ech_physiques": -4871,
        "eolien": 6207,
        "fioul": 37,
        "gaz": 3652,
        "hydraulique": 4452,
        "load": 46097,
        "nucleaire": 34293,
        "pompage": 0,
        "prevision_j": 45200,
        "prevision_j1": 45400,
        "solaire": 1109,
        "taux_co2": 42
      },
      {
        "at": "2026-09-29T06:45:00+00:00",
        "bioenergies": 1063,
        "charbon": 0,
        "ech_physiques": -4781,
        "eolien": 6276,
        "fioul": 37,
        "gaz": 3613,
        "hydraulique": 4139,
        "load": 46338,
        "nucleaire": 34289,
        "pompage": -1,
        "prevision_j": 45500,
        "prevision_j1": 45700,
        "solaire": 1689,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T07:00:00+00:00",
        "bioenergies": 1080,
        "charbon": 0,
        "ech_physiques": -4664,
        "eolien": 6299,
        "fioul": 37,
        "gaz": 3409,
        "hydraulique": 3613,
        "load": 46285,
        "nucleaire": 34299,
        "pompage": -1,
        "prevision_j": 45800,
        "prevision_j1": 46000,
        "solaire": 2220,
        "taux_co2": 40
      },
      {
        "at": "2026-09-29T07:15:00+00:00",
        "bioenergies": 1074,
        "charbon": 0,
        "ech_physiques": -4647,
        "eolien": 6322,
        "fioul": 37,
        "gaz": 3442,
        "hydraulique": 3288,
        "load": 46840,
        "nucleaire": 34294,
        "pompage": -1,
        "prevision_j": 46050,
        "prevision_j1": 46250,
        "solaire": 2988,
        "taux_co2": 40
      },
      {
        "at": "2026-09-29T07:30:00+00:00",
        "bioenergies": 1077,
        "charbon": 0,
        "ech_physiques": -4661,
        "eolien": 6196,
        "fioul": 37,
        "gaz": 3298,
        "hydraulique": 2771,
        "load": 46666,
        "nucleaire": 34308,
        "pompage": 0,
        "prevision_j": 46300,
        "prevision_j1": 46500,
        "solaire": 3634,
        "taux_co2": 38
      },
      {
        "at": "2026-09-29T07:45:00+00:00",
        "bioenergies": 1076,
        "charbon": 0,
        "ech_physiques": -4978,
        "eolien": 6058,
        "fioul": 37,
        "gaz": 3091,
        "hydraulique": 2762,
        "load": 46901,
        "nucleaire": 34282,
        "pompage": 0,
        "prevision_j": 46350,
        "prevision_j1": 46550,
        "solaire": 4588,
        "taux_co2": 36
      },
      {
        "at": "2026-09-29T08:00:00+00:00",
        "bioenergies": 1080,
        "charbon": 0,
        "ech_physiques": -5042,
        "eolien": 6098,
        "fioul": 37,
        "gaz": 2652,
        "hydraulique": 2676,
        "load": 47199,
        "nucleaire": 34258,
        "pompage": -2,
        "prevision_j": 46400,
        "prevision_j1": 46600,
        "solaire": 5565,
        "taux_co2": 32
      },
      {
        "at": "2026-09-29T08:15:00+00:00",
        "bioenergies": 1082,
        "charbon": 0,
        "ech_physiques": -4942,
        "eolien": 5913,
        "fioul": 37,
        "gaz": 2206,
        "hydraulique": 2211,
        "load": 47848,
        "nucleaire": 34255,
        "pompage": -23,
        "prevision_j": 46950,
        "prevision_j1": 47000,
        "solaire": 6858,
        "taux_co2": 29
      },
      {
        "at": "2026-09-29T08:30:00+00:00",
        "bioenergies": 1081,
        "charbon": 0,
        "ech_physiques": -4909,
        "eolien": 5869,
        "fioul": 37,
        "gaz": 1911,
        "hydraulique": 2115,
        "load": 47866,
        "nucleaire": 34229,
        "pompage": -24,
        "prevision_j": 47500,
        "prevision_j1": 47400,
        "solaire": 7577,
        "taux_co2": 26
      },
      {
        "at": "2026-09-29T08:45:00+00:00",
        "bioenergies": 1091,
        "charbon": 0,
        "ech_physiques": -5188,
        "eolien": 5891,
        "fioul": 37,
        "gaz": 1526,
        "hydraulique": 1955,
        "load": 47902,
        "nucleaire": 34193,
        "pompage": -25,
        "prevision_j": 47600,
        "prevision_j1": 47500,
        "solaire": 8438,
        "taux_co2": 23
      },
      {
        "at": "2026-09-29T09:00:00+00:00",
        "bioenergies": 1090,
        "charbon": 0,
        "ech_physiques": -5295,
        "eolien": 5815,
        "fioul": 37,
        "gaz": 1344,
        "hydraulique": 1758,
        "load": 48001,
        "nucleaire": 34186,
        "pompage": -192,
        "prevision_j": 47700,
        "prevision_j1": 47600,
        "solaire": 9267,
        "taux_co2": 21
      },
      {
        "at": "2026-09-29T09:15:00+00:00",
        "bioenergies": 1085,
        "charbon": 0,
        "ech_physiques": -5538,
        "eolien": 5709,
        "fioul": 37,
        "gaz": 1159,
        "hydraulique": 1842,
        "load": 48386,
        "nucleaire": 33887,
        "pompage": -340,
        "prevision_j": 47900,
        "prevision_j1": 47850,
        "solaire": 10452,
        "taux_co2": 20
      },
      {
        "at": "2026-09-29T09:30:00+00:00",
        "bioenergies": 1091,
        "charbon": 0,
        "ech_physiques": -5752,
        "eolien": 5754,
        "fioul": 37,
        "gaz": 765,
        "hydraulique": 1707,
        "load": 48138,
        "nucleaire": 33876,
        "pompage": -191,
        "prevision_j": 48100,
        "prevision_j1": 48100,
        "solaire": 10789,
        "taux_co2": 17
      },
      {
        "at": "2026-09-29T09:45:00+00:00",
        "bioenergies": 1100,
        "charbon": 0,
        "ech_physiques": -5706,
        "eolien": 5853,
        "fioul": 37,
        "gaz": 683,
        "hydraulique": 1583,
        "load": 48637,
        "nucleaire": 33886,
        "pompage": -358,
        "prevision_j": 49050,
        "prevision_j1": 48650,
        "solaire": 11598,
        "taux_co2": 16
      },
      {
        "at": "2026-09-29T10:00:00+00:00",
        "bioenergies": 1094,
        "charbon": 0,
        "ech_physiques": -5507,
        "eolien": 5933,
        "fioul": 36,
        "gaz": 687,
        "hydraulique": 1556,
        "load": 48932,
        "nucleaire": 33756,
        "pompage": -520,
        "prevision_j": 50000,
        "prevision_j1": 49200,
        "solaire": 12031,
        "taux_co2": 16
      },
      {
        "at": "2026-09-29T10:15:00+00:00",
        "bioenergies": 1101,
        "charbon": 0,
        "ech_physiques": -6194,
        "eolien": 6035,
        "fioul": 37,
        "gaz": 321,
        "hydraulique": 1581,
        "load": 48819,
        "nucleaire": 33781,
        "pompage": -519,
        "prevision_j": 49700,
        "prevision_j1": 48950,
        "solaire": 12768,
        "taux_co2": 13
      },
      {
        "at": "2026-09-29T10:30:00+00:00",
        "bioenergies": 1101,
        "charbon": 0,
        "ech_physiques": -6739,
        "eolien": 6153,
        "fioul": 37,
        "gaz": 257,
        "hydraulique": 1591,
        "load": 48949,
        "nucleaire": 33773,
        "pompage": -517,
        "prevision_j": 49400,
        "prevision_j1": 48700,
        "solaire": 13518,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T10:45:00+00:00",
        "bioenergies": 1102,
        "charbon": 0,
        "ech_physiques": -6808,
        "eolien": 6375,
        "fioul": 36,
        "gaz": 251,
        "hydraulique": 1627,
        "load": 49123,
        "nucleaire": 33501,
        "pompage": -514,
        "prevision_j": 49800,
        "prevision_j1": 49150,
        "solaire": 13887,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T11:00:00+00:00",
        "bioenergies": 1103,
        "charbon": 0,
        "ech_physiques": -7599,
        "eolien": 6404,
        "fioul": 37,
        "gaz": 255,
        "hydraulique": 1558,
        "load": 48473,
        "nucleaire": 33369,
        "pompage": -512,
        "prevision_j": 50200,
        "prevision_j1": 49600,
        "solaire": 14268,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T11:15:00+00:00",
        "bioenergies": 1093,
        "charbon": 0,
        "ech_physiques": -8060,
        "eolien": 6572,
        "fioul": 37,
        "gaz": 253,
        "hydraulique": 1574,
        "load": 48367,
        "nucleaire": 33027,
        "pompage": -584,
        "prevision_j": 49300,
        "prevision_j1": 48800,
        "solaire": 14667,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T11:30:00+00:00",
        "bioenergies": 1103,
        "charbon": 0,
        "ech_physiques": -8642,
        "eolien": 6538,
        "fioul": 37,
        "gaz": 265,
        "hydraulique": 1598,
        "load": 48104,
        "nucleaire": 33005,
        "pompage": -581,
        "prevision_j": 48400,
        "prevision_j1": 48000,
        "solaire": 15029,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T11:45:00+00:00",
        "bioenergies": 1095,
        "charbon": 0,
        "ech_physiques": -8677,
        "eolien": 6793,
        "fioul": 37,
        "gaz": 267,
        "hydraulique": 1577,
        "load": 48237,
        "nucleaire": 32852,
        "pompage": -584,
        "prevision_j": 48250,
        "prevision_j1": 47900,
        "solaire": 15172,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T12:00:00+00:00",
        "bioenergies": 1100,
        "charbon": 0,
        "ech_physiques": -8077,
        "eolien": 6887,
        "fioul": 37,
        "gaz": 265,
        "hydraulique": 1555,
        "load": 48729,
        "nucleaire": 32817,
        "pompage": -583,
        "prevision_j": 48100,
        "prevision_j1": 47800,
        "solaire": 15032,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T12:15:00+00:00",
        "bioenergies": 1105,
        "charbon": 0,
        "ech_physiques": -7983,
        "eolien": 7039,
        "fioul": 37,
        "gaz": 264,
        "hydraulique": 1593,
        "load": 49043,
        "nucleaire": 32877,
        "pompage": -579,
        "prevision_j": 48800,
        "prevision_j1": 48600,
        "solaire": 14875,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T12:30:00+00:00",
        "bioenergies": 1105,
        "charbon": 0,
        "ech_physiques": -8502,
        "eolien": 7279,
        "fioul": 37,
        "gaz": 265,
        "hydraulique": 1665,
        "load": 48553,
        "nucleaire": 32859,
        "pompage": -579,
        "prevision_j": 49500,
        "prevision_j1": 49400,
        "solaire": 14505,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T12:45:00+00:00",
        "bioenergies": 1101,
        "charbon": 0,
        "ech_physiques": -8243,
        "eolien": 7534,
        "fioul": 37,
        "gaz": 264,
        "hydraulique": 1743,
        "load": 48972,
        "nucleaire": 32860,
        "pompage": -579,
        "prevision_j": 49350,
        "prevision_j1": 49100,
        "solaire": 14200,
        "taux_co2": 12
      },
      {
        "at": "2026-09-29T13:00:00+00:00",
        "bioenergies": 1102,
        "charbon": 0,
        "ech_physiques": -8332,
        "eolien": 7495,
        "fioul": 37,
        "gaz": 454,
        "hydraulique": 1616,
        "load": 48865,
        "nucleaire": 32914,
        "pompage": -579,
        "prevision_j": 49200,
        "prevision_j1": 48800,
        "solaire": 14147,
        "taux_co2": 13
      },
      {
        "at": "2026-09-29T13:15:00+00:00",
        "bioenergies": 1100,
        "charbon": 0,
        "ech_physiques": -8669,
        "eolien": 7666,
        "fioul": 37,
        "gaz": 452,
        "hydraulique": 1606,
        "load": 48544,
        "nucleaire": 33005,
        "pompage": -509,
        "prevision_j": 48800,
        "prevision_j1": 48550,
        "solaire": 13864,
        "taux_co2": 13
      },
      {
        "at": "2026-09-29T13:30:00+00:00",
        "bioenergies": 1096,
        "charbon": 0,
        "ech_physiques": -8965,
        "eolien": 7796,
        "fioul": 37,
        "gaz": 496,
        "hydraulique": 2018,
        "load": 48490,
        "nucleaire": 33050,
        "pompage": -508,
        "prevision_j": 48400,
        "prevision_j1": 48300,
        "solaire": 13507,
        "taux_co2": 13
      },
      {
        "at": "2026-09-29T13:45:00+00:00",
        "bioenergies": 1101,
        "charbon": 0,
        "ech_physiques": -9627,
        "eolien": 7978,
        "fioul": 36,
        "gaz": 505,
        "hydraulique": 2173,
        "load": 47951,
        "nucleaire": 33371,
        "pompage": -509,
        "prevision_j": 48450,
        "prevision_j1": 48150,
        "solaire": 12939,
        "taux_co2": 14
      },
      {
        "at": "2026-09-29T14:00:00+00:00",
        "bioenergies": 1099,
        "charbon": 0,
        "ech_physiques": -9223,
        "eolien": 7879,
        "fioul": 36,
        "gaz": 548,
        "hydraulique": 2375,
        "load": 47585,
        "nucleaire": 33397,
        "pompage": -508,
        "prevision_j": 48500,
        "prevision_j1": 48000,
        "solaire": 12189,
        "taux_co2": 14
      },
      {
        "at": "2026-09-29T14:15:00+00:00",
        "bioenergies": 1098,
        "charbon": 0,
        "ech_physiques": -9080,
        "eolien": 7864,
        "fioul": 36,
        "gaz": 598,
        "hydraulique": 2471,
        "load": 47327,
        "nucleaire": 33530,
        "pompage": -507,
        "prevision_j": 48000,
        "prevision_j1": 47700,
        "solaire": 11458,
        "taux_co2": 14
      },
      {
        "at": "2026-09-29T14:30:00+00:00",
        "bioenergies": 1096,
        "charbon": 0,
        "ech_physiques": -9018,
        "eolien": 7728,
        "fioul": 36,
        "gaz": 709,
        "hydraulique": 2541,
        "load": 46709,
        "nucleaire": 33698,
        "pompage": -506,
        "prevision_j": 47500,
        "prevision_j1": 47400,
        "solaire": 10434,
        "taux_co2": 16
      },
      {
        "at": "2026-09-29T14:45:00+00:00",
        "bioenergies": 1097,
        "charbon": 0,
        "ech_physiques": -8933,
        "eolien": 7761,
        "fioul": 36,
        "gaz": 1541,
        "hydraulique": 2482,
        "load": 47114,
        "nucleaire": 33919,
        "pompage": -505,
        "prevision_j": 47200,
        "prevision_j1": 47100,
        "solaire": 9717,
        "taux_co2": 22
      },
      {
        "at": "2026-09-29T15:00:00+00:00",
        "bioenergies": 1103,
        "charbon": 0,
        "ech_physiques": -8272,
        "eolien": 7849,
        "fioul": 36,
        "gaz": 1526,
        "hydraulique": 2521,
        "load": 46797,
        "nucleaire": 33443,
        "pompage": 0,
        "prevision_j": 46900,
        "prevision_j1": 46800,
        "solaire": 8584,
        "taux_co2": 22
      },
      {
        "at": "2026-09-29T15:15:00+00:00",
        "bioenergies": 1102,
        "charbon": 0,
        "ech_physiques": -8445,
        "eolien": 7872,
        "fioul": 36,
        "gaz": 1927,
        "hydraulique": 2689,
        "load": 46578,
        "nucleaire": 33766,
        "pompage": -1,
        "prevision_j": 47050,
        "prevision_j1": 47000,
        "solaire": 7627,
        "taux_co2": 25
      },
      {
        "at": "2026-09-29T15:30:00+00:00",
        "bioenergies": 1102,
        "charbon": 0,
        "ech_physiques": -8047,
        "eolien": 8017,
        "fioul": 36,
        "gaz": 2308,
        "hydraulique": 2807,
        "load": 46610,
        "nucleaire": 33915,
        "pompage": 0,
        "prevision_j": 47200,
        "prevision_j1": 47200,
        "solaire": 6466,
        "taux_co2": 29
      },
      {
        "at": "2026-09-29T15:45:00+00:00",
        "bioenergies": 1111,
        "charbon": 0,
        "ech_physiques": -7724,
        "eolien": 7760,
        "fioul": 36,
        "gaz": 2653,
        "hydraulique": 3189,
        "load": 46439,
        "nucleaire": 33908,
        "pompage": 0,
        "prevision_j": 47550,
        "prevision_j1": 47700,
        "solaire": 5506,
        "taux_co2": 32
      },
      {
        "at": "2026-09-29T16:00:00+00:00",
        "bioenergies": 1110,
        "charbon": 0,
        "ech_physiques": -7080,
        "eolien": 7745,
        "fioul": 36,
        "gaz": 3229,
        "hydraulique": 3680,
        "load": 47217,
        "nucleaire": 33922,
        "pompage": 0,
        "prevision_j": 47900,
        "prevision_j1": 48200,
        "solaire": 4556,
        "taux_co2": 36
      },
      {
        "at": "2026-09-29T16:15:00+00:00",
        "bioenergies": 1109,
        "charbon": 0,
        "ech_physiques": -6142,
        "eolien": 7332,
        "fioul": 36,
        "gaz": 3335,
        "hydraulique": 3972,
        "load": 47212,
        "nucleaire": 33999,
        "pompage": 0,
        "prevision_j": 48250,
        "prevision_j1": 48450,
        "solaire": 3565,
        "taux_co2": 38
      },
      {
        "at": "2026-09-29T16:30:00+00:00",
        "bioenergies": 1109,
        "charbon": 0,
        "ech_physiques": -5091,
        "eolien": 7061,
        "fioul": 36,
        "gaz": 3194,
        "hydraulique": 4461,
        "load": 47420,
        "nucleaire": 34002,
        "pompage": 0,
        "prevision_j": 48600,
        "prevision_j1": 48700,
        "solaire": 2641,
        "taux_co2": 37
      },
      {
        "at": "2026-09-29T16:45:00+00:00",
        "bioenergies": 1109,
        "charbon": 0,
        "ech_physiques": -5065,
        "eolien": 6815,
        "fioul": 36,
        "gaz": 3504,
        "hydraulique": 5407,
        "load": 48162,
        "nucleaire": 34044,
        "pompage": -1,
        "prevision_j": 49400,
        "prevision_j1": 49450,
        "solaire": 1950,
        "taux_co2": 39
      },
      {
        "at": "2026-09-29T17:00:00+00:00",
        "bioenergies": 1114,
        "charbon": 0,
        "ech_physiques": -4040,
        "eolien": 6628,
        "fioul": 36,
        "gaz": 3542,
        "hydraulique": 5902,
        "load": 48822,
        "nucleaire": 34022,
        "pompage": 0,
        "prevision_j": 50200,
        "prevision_j1": 50200,
        "solaire": 1219,
        "taux_co2": 40
      },
      {
        "at": "2026-09-29T17:15:00+00:00",
        "bioenergies": 1110,
        "charbon": 0,
        "ech_physiques": -3100,
        "eolien": 6555,
        "fioul": 36,
        "gaz": 3565,
        "hydraulique": 6027,
        "load": 49455,
        "nucleaire": 34051,
        "pompage": 0,
        "prevision_j": 49750,
        "prevision_j1": 49900,
        "solaire": 830,
        "taux_co2": 40
      },
      {
        "at": "2026-09-29T17:30:00+00:00",
        "bioenergies": 1109,
        "charbon": 0,
        "ech_physiques": -2898,
        "eolien": 6375,
        "fioul": 36,
        "gaz": 3570,
        "hydraulique": 6085,
        "load": 49174,
        "nucleaire": 34008,
        "pompage": 0,
        "prevision_j": 49300,
        "prevision_j1": 49600,
        "solaire": 471,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T17:45:00+00:00",
        "bioenergies": 1118,
        "charbon": 0,
        "ech_physiques": -2527,
        "eolien": 6534,
        "fioul": 36,
        "gaz": 3607,
        "hydraulique": 6079,
        "load": 49347,
        "nucleaire": 34027,
        "pompage": 0,
        "prevision_j": 49200,
        "prevision_j1": 49500,
        "solaire": 312,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T18:00:00+00:00",
        "bioenergies": 1120,
        "charbon": 0,
        "ech_physiques": -2910,
        "eolien": 6782,
        "fioul": 36,
        "gaz": 3595,
        "hydraulique": 6020,
        "load": 48951,
        "nucleaire": 34071,
        "pompage": 0,
        "prevision_j": 49100,
        "prevision_j1": 49400,
        "solaire": 218,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T18:15:00+00:00",
        "bioenergies": 1116,
        "charbon": 0,
        "ech_physiques": -3759,
        "eolien": 7146,
        "fioul": 36,
        "gaz": 3631,
        "hydraulique": 5478,
        "load": 48242,
        "nucleaire": 34046,
        "pompage": 0,
        "prevision_j": 48550,
        "prevision_j1": 48800,
        "solaire": 208,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T18:30:00+00:00",
        "bioenergies": 1124,
        "charbon": 0,
        "ech_physiques": -4926,
        "eolien": 7591,
        "fioul": 36,
        "gaz": 3604,
        "hydraulique": 5122,
        "load": 47161,
        "nucleaire": 34127,
        "pompage": 0,
        "prevision_j": 48000,
        "prevision_j1": 48200,
        "solaire": 207,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T18:45:00+00:00",
        "bioenergies": 1122,
        "charbon": 0,
        "ech_physiques": -5663,
        "eolien": 8008,
        "fioul": 36,
        "gaz": 3618,
        "hydraulique": 4524,
        "load": 46140,
        "nucleaire": 34069,
        "pompage": 0,
        "prevision_j": 47050,
        "prevision_j1": 47250,
        "solaire": 200,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T19:00:00+00:00",
        "bioenergies": 1124,
        "charbon": 0,
        "ech_physiques": -6142,
        "eolien": 8623,
        "fioul": 36,
        "gaz": 3622,
        "hydraulique": 3997,
        "load": 45497,
        "nucleaire": 34045,
        "pompage": 0,
        "prevision_j": 46100,
        "prevision_j1": 46300,
        "solaire": 202,
        "taux_co2": 41
      },
      {
        "at": "2026-09-29T19:15:00+00:00",
        "bioenergies": 1126,
        "charbon": 0,
        "ech_physiques": -6045,
        "eolien": 8961,
        "fioul": 36,
        "gaz": 3629,
        "hydraulique": 2947,
        "load": 44819,
        "nucleaire": 34126,
        "pompage": 0,
        "prevision_j": 45350,
        "prevision_j1": 45500,
        "solaire": 0,
        "taux_co2": 42
      },
      {
        "at": "2026-09-29T19:30:00+00:00",
        "bioenergies": 1119,
        "charbon": 0,
        "ech_physiques": -6516,
        "eolien": 9351,
        "fioul": 35,
        "gaz": 3313,
        "hydraulique": 2704,
        "load": 44075,
        "nucleaire": 34138,
        "pompage": -2,
        "prevision_j": 44600,
        "prevision_j1": 44700,
        "solaire": 0,
        "taux_co2": 39
      },
      {
        "at": "2026-09-29T19:45:00+00:00",
        "bioenergies": 1121,
        "charbon": 0,
        "ech_physiques": -7267,
        "eolien": 9795,
        "fioul": 37,
        "gaz": 2944,
        "hydraulique": 2770,
        "load": 43359,
        "nucleaire": 34134,
        "pompage": 0,
        "prevision_j": 43900,
        "prevision_j1": 44000,
        "solaire": 0,
        "taux_co2": 36
      },
      {
        "at": "2026-09-29T20:00:00+00:00",
        "bioenergies": 1121,
        "charbon": 0,
        "ech_physiques": -7469,
        "eolien": 10084,
        "fioul": 35,
        "gaz": 2524,
        "hydraulique": 2706,
        "load": 42905,
        "nucleaire": 34103,
        "pompage": -1,
        "prevision_j": 43200,
        "prevision_j1": 43300,
        "solaire": 0,
        "taux_co2": 33
      },
      {
        "at": "2026-09-29T20:15:00+00:00",
        "bioenergies": 1122,
        "charbon": 0,
        "ech_physiques": -6565,
        "eolien": 10240,
        "fioul": 37,
        "gaz": 2094,
        "hydraulique": 2546,
        "load": 43509,
        "nucleaire": 34119,
        "pompage": 0,
        "prevision_j": 43650,
        "prevision_j1": 43700,
        "solaire": 0,
        "taux_co2": 29
      },
      {
        "at": "2026-09-29T20:30:00+00:00",
        "bioenergies": 1124,
        "charbon": 0,
        "ech_physiques": -6056,
        "eolien": 10438,
        "fioul": 37,
        "gaz": 1657,
        "hydraulique": 2449,
        "load": 43351,
        "nucleaire": 34093,
        "pompage": -19,
        "prevision_j": 44100,
        "prevision_j1": 44100,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-29T20:45:00+00:00",
        "bioenergies": 1118,
        "charbon": 0,
        "ech_physiques": -5457,
        "eolien": 10796,
        "fioul": 35,
        "gaz": 942,
        "hydraulique": 2461,
        "load": 43884,
        "nucleaire": 34130,
        "pompage": -183,
        "prevision_j": 44600,
        "prevision_j1": 44600,
        "solaire": 0,
        "taux_co2": 20
      },
      {
        "at": "2026-09-29T21:00:00+00:00",
        "bioenergies": 1126,
        "charbon": 0,
        "ech_physiques": -5701,
        "eolien": 11062,
        "fioul": 33,
        "gaz": 801,
        "hydraulique": 2394,
        "load": 43443,
        "nucleaire": 33978,
        "pompage": -191,
        "prevision_j": 45100,
        "prevision_j1": 45100,
        "solaire": 0,
        "taux_co2": 19
      },
      {
        "at": "2026-09-29T21:15:00+00:00",
        "bioenergies": 1120,
        "charbon": 0,
        "ech_physiques": -6005,
        "eolien": 11201,
        "fioul": 33,
        "gaz": 791,
        "hydraulique": 2255,
        "load": 43411,
        "nucleaire": 34072,
        "pompage": -159,
        "prevision_j": 44200,
        "prevision_j1": 44250,
        "solaire": 0,
        "taux_co2": 18
      },
      {
        "at": "2026-09-29T21:30:00+00:00",
        "bioenergies": 1122,
        "charbon": 0,
        "ech_physiques": -5970,
        "eolien": 11285,
        "fioul": 33,
        "gaz": 521,
        "hydraulique": 2221,
        "load": 42782,
        "nucleaire": 33906,
        "pompage": -318,
        "prevision_j": 43300,
        "prevision_j1": 43400,
        "solaire": 0,
        "taux_co2": 16
      },
      {
        "at": "2026-09-29T21:45:00+00:00",
        "bioenergies": 1120,
        "charbon": 0,
        "ech_physiques": -6320,
        "eolien": 11494,
        "fioul": 33,
        "gaz": 901,
        "hydraulique": 2248,
        "load": 43079,
        "nucleaire": 33904,
        "pompage": -328,
        "prevision_j": 42700,
        "prevision_j1": 42750,
        "solaire": 0,
        "taux_co2": 19
      },
      {
        "at": "2026-09-29T22:00:00+00:00",
        "bioenergies": 1127,
        "charbon": 0,
        "ech_physiques": -6858,
        "eolien": 11431,
        "fioul": 33,
        "gaz": 892,
        "hydraulique": 2259,
        "load": 42257,
        "nucleaire": 33875,
        "pompage": -517,
        "prevision_j": 42100,
        "prevision_j1": 42100,
        "solaire": 0,
        "taux_co2": 19
      },
      {
        "at": "2026-09-29T22:15:00+00:00",
        "bioenergies": 1119,
        "charbon": 0,
        "ech_physiques": -6777,
        "eolien": 11412,
        "fioul": 33,
        "gaz": 897,
        "hydraulique": 2469,
        "load": 42304,
        "nucleaire": 33896,
        "pompage": -848,
        "prevision_j": 41500,
        "prevision_j1": 41500,
        "solaire": 0,
        "taux_co2": 19
      },
      {
        "at": "2026-09-29T22:30:00+00:00",
        "bioenergies": 1115,
        "charbon": 0,
        "ech_physiques": -8018,
        "eolien": 11541,
        "fioul": 33,
        "gaz": 914,
        "hydraulique": 2522,
        "load": 41249,
        "nucleaire": 34000,
        "pompage": -851,
        "prevision_j": 40900,
        "prevision_j1": 40900,
        "solaire": 0,
        "taux_co2": 19
      },
      {
        "at": "2026-09-29T22:45:00+00:00",
        "bioenergies": 1117,
        "charbon": 0,
        "ech_physiques": -9042,
        "eolien": 11636,
        "fioul": 33,
        "gaz": 487,
        "hydraulique": 2628,
        "load": 39672,
        "nucleaire": 33686,
        "pompage": -848,
        "prevision_j": 40000,
        "prevision_j1": 40000,
        "solaire": 0,
        "taux_co2": 16
      },
      {
        "at": "2026-09-29T23:00:00+00:00",
        "bioenergies": 1118,
        "charbon": 0,
        "ech_physiques": -9310,
        "eolien": 11735,
        "fioul": 33,
        "gaz": 626,
        "hydraulique": 2457,
        "load": 39328,
        "nucleaire": 33547,
        "pompage": -847,
        "prevision_j": 39100,
        "prevision_j1": 39100,
        "solaire": 0,
        "taux_co2": 17
      },
      {
        "at": "2026-09-29T23:15:00+00:00",
        "bioenergies": 1121,
        "charbon": 0,
        "ech_physiques": -9354,
        "eolien": 11523,
        "fioul": 34,
        "gaz": 655,
        "hydraulique": 2429,
        "load": 39394,
        "nucleaire": 33843,
        "pompage": -845,
        "prevision_j": 39600,
        "prevision_j1": 39600,
        "solaire": 0,
        "taux_co2": 17
      },
      {
        "at": "2026-09-29T23:30:00+00:00",
        "bioenergies": 1120,
        "charbon": 0,
        "ech_physiques": -9592,
        "eolien": 11757,
        "fioul": 36,
        "gaz": 665,
        "hydraulique": 2440,
        "load": 39192,
        "nucleaire": 33848,
        "pompage": -1082,
        "prevision_j": 40100,
        "prevision_j1": 40100,
        "solaire": 0,
        "taux_co2": 17
      },
      {
        "at": "2026-09-29T23:45:00+00:00",
        "bioenergies": 1121,
        "charbon": 0,
        "ech_physiques": -9849,
        "eolien": 11857,
        "fioul": 37,
        "gaz": 670,
        "hydraulique": 2451,
        "load": 38995,
        "nucleaire": 33854,
        "pompage": -1076,
        "prevision_j": 39300,
        "prevision_j1": 39300,
        "solaire": 0,
        "taux_co2": 17
      },
      {
        "at": "2026-09-30T00:00:00+00:00",
        "bioenergies": 1126,
        "charbon": 0,
        "ech_physiques": -9958,
        "eolien": 11736,
        "fioul": 35,
        "gaz": 651,
        "hydraulique": 2380,
        "load": 38404,
        "nucleaire": 33684,
        "pompage": -1079,
        "prevision_j": 38500,
        "prevision_j1": 38500,
        "solaire": 0,
        "taux_co2": 17
      },
      {
        "at": "2026-09-30T00:15:00+00:00",
        "bioenergies": 1122,
        "charbon": 0,
        "ech_physiques": -9424,
        "eolien": 11624,
        "fioul": 36,
        "gaz": 654,
        "hydraulique": 2117,
        "load": 37892,
        "nucleaire": 33030,
        "pompage": -1075,
        "prevision_j": 37900,
        "prevision_j1": 37900,
        "solaire": 0,
        "taux_co2": 18
      },
      {
        "at": "2026-09-30T00:30:00+00:00",
        "bioenergies": 1127,
        "charbon": 0,
        "ech_physiques": -9288,
        "eolien": 11568,
        "fioul": 37,
        "gaz": 408,
        "hydraulique": 2100,
        "load": 36864,
        "nucleaire": 32099,
        "pompage": -1142,
        "prevision_j": 37300,
        "prevision_j1": 37300,
        "solaire": 0,
        "taux_co2": 16
      },
      {
        "at": "2026-09-30T00:45:00+00:00",
        "bioenergies": 1126,
        "charbon": 0,
        "ech_physiques": -9391,
        "eolien": 11502,
        "fioul": 37,
        "gaz": 290,
        "hydraulique": 2099,
        "load": 36311,
        "nucleaire": 32031,
        "pompage": -1374,
        "prevision_j": 36700,
        "prevision_j1": 36700,
        "solaire": 0,
        "taux_co2": 15
      },
      {
        "at": "2026-09-30T01:00:00+00:00",
        "bioenergies": 1119,
        "charbon": 0,
        "ech_physiques": -10044,
        "eolien": 11541,
        "fioul": 37,
        "gaz": 287,
        "hydraulique": 2098,
        "load": 35775,
        "nucleaire": 32299,
        "pompage": -1371,
        "prevision_j": 36100,
        "prevision_j1": 36100,
        "solaire": 0,
        "taux_co2": 15
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
      "as_of": "2026-09-30",
      "change": -2629,
      "comparison": "vs ~1 h",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_load",
      "label": "Demande France",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 35775
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "export si négatif · import si positif",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_exchange",
      "label": "Solde des échanges physiques",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -10044
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_nucleaire",
      "label": "Nucléaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 32299
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_gaz",
      "label": "Gaz électrique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 287
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_eolien",
      "label": "Éolien",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 11541
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_solaire",
      "label": "Solaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 0
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_hydraulique",
      "label": "Hydraulique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 2098
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_bioenergies",
      "label": "Bioénergies",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 1119
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "demande − éolien − solaire",
      "detail": "Calcul indicatif, sans jugement sur le prix ni l'appel au gaz. Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_residual",
      "label": "Demande résiduelle indicative",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 24234
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "production française",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_carbon",
      "label": "Intensité CO₂ estimée",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "g/kWh",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 15
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "réalisé − prévision réactualisée le jour même",
      "detail": "Observation 2026-09-30T01:00:00+00:00 UTC",
      "id": "power_load_gap",
      "label": "Écart à prévision de demande J",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -325
    },
    {
      "as_of": "2026-09-28",
      "change": 0.16,
      "comparison": "points vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu",
      "label": "Stockage gaz UE · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 71.33
    },
    {
      "as_of": "2026-09-28",
      "change": 1.861,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_twh",
      "label": "Gaz stocké UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 807.141
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_net",
      "label": "Soutirage net UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -1884.9
    },
    {
      "as_of": "2026-09-28",
      "change": 0.2,
      "comparison": "points vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr",
      "label": "Stockage gaz France · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 83.23
    },
    {
      "as_of": "2026-09-28",
      "change": 0.253,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_twh",
      "label": "Gaz stocké France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 103.104
    },
    {
      "as_of": "2026-09-28",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_net",
      "label": "Soutirage net France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -253.1
    },
    {
      "as_of": "2026-09-28",
      "change": 179.01,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "lng_eu_inventory",
      "label": "GNL en cuves UE",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "10³ m³ GNL",
      "url": "https://alsi.gie.eu/",
      "value": 4159.66
    },
    {
      "as_of": "2026-09-28",
      "change": 65.3,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "lng_eu_sendout",
      "label": "Émission terminaux GNL UE",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "GWh/j",
      "url": "https://alsi.gie.eu/",
      "value": 3631.5
    },
    {
      "as_of": "2026-09-28",
      "change": 136.49,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "lng_fr_inventory",
      "label": "GNL en cuves France",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "10³ m³ GNL",
      "url": "https://alsi.gie.eu/",
      "value": 665.54
    },
    {
      "as_of": "2026-09-28",
      "change": -210.9,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "lng_fr_sendout",
      "label": "Émission terminaux GNL France",
      "sector": "gas",
      "source": "GIE ALSI",
      "unit": "GWh/j",
      "url": "https://alsi.gie.eu/",
      "value": 967.7
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "prévision J-1, 24 h glissantes",
      "detail": "Pic prévu à 2026-09-30T11:00:00+00:00 UTC",
      "id": "power_forecast_fr",
      "label": "Pic prévu 24 h · France",
      "sector": "power",
      "source": "ENTSO-E · prévision J-1",
      "unit": "MW",
      "url": "https://transparency.entsoe.eu/",
      "value": 51100
    },
    {
      "as_of": "2026-09-30",
      "change": null,
      "comparison": "prévision J-1, 24 h glissantes",
      "detail": "Pic prévu à 2026-09-30T07:30:00+00:00 UTC",
      "id": "power_forecast_de",
      "label": "Pic prévu 24 h · Allemagne/Luxembourg",
      "sector": "power",
      "source": "ENTSO-E · prévision J-1",
      "unit": "MW",
      "url": "https://transparency.entsoe.eu/",
      "value": 62218
    },
    {
      "as_of": "2026-09-28",
      "change": -9,
      "comparison": "vs même date N−1",
      "detail": "Part des cultures jugées bonnes ou excellentes · 18 États majeurs",
      "id": "ag_corn_condition",
      "label": "Maïs US · bon/excellent",
      "sector": "agri",
      "source": "USDA NASS Crop Progress",
      "unit": "%",
      "url": "https://esmis.nal.usda.gov/sites/default/release-files/796082/prog3926.txt",
      "value": 57
    },
    {
      "as_of": "2026-09-28",
      "change": 0,
      "comparison": "vs moyenne 5 ans",
      "detail": "17 % à la même date N−1 · 13 % semaine précédente",
      "id": "ag_corn_harvest",
      "label": "Maïs US · récolté",
      "sector": "agri",
      "source": "USDA NASS Crop Progress",
      "unit": "%",
      "url": "https://esmis.nal.usda.gov/sites/default/release-files/796082/prog3926.txt",
      "value": 18
    },
    {
      "as_of": "2026-09-28",
      "change": -4,
      "comparison": "vs même date N−1",
      "detail": "Part des cultures jugées bonnes ou excellentes · 18 États majeurs",
      "id": "ag_soy_condition",
      "label": "Soja US · bon/excellent",
      "sector": "agri",
      "source": "USDA NASS Crop Progress",
      "unit": "%",
      "url": "https://esmis.nal.usda.gov/sites/default/release-files/796082/prog3926.txt",
      "value": 58
    },
    {
      "as_of": "2026-09-28",
      "change": 0,
      "comparison": "vs moyenne 5 ans",
      "detail": "18 % à la même date N−1 · 12 % semaine précédente",
      "id": "ag_soy_harvest",
      "label": "Soja US · récolté",
      "sector": "agri",
      "source": "USDA NASS Crop Progress",
      "unit": "%",
      "url": "https://esmis.nal.usda.gov/sites/default/release-files/796082/prog3926.txt",
      "value": 17
    },
    {
      "as_of": "2025",
      "change": 1.2,
      "comparison": "vs 2024",
      "detail": "Production annuelle estimée ; 2024 : 72,8 Mt. Pas un stock LME",
      "id": "metal_aluminum",
      "label": "Aluminium primaire · monde",
      "sector": "metals",
      "source": "USGS MCS 2026",
      "unit": "Mt",
      "url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-aluminum.pdf",
      "value": 74
    }
  ],
  "schema": 3,
  "sources": {
    "alsi": {
      "as_of": "2026-09-28",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://alsi.gie.eu/"
    },
    "alsi_fr": {
      "as_of": "2026-09-28",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://alsi.gie.eu/"
    },
    "brent": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm"
    },
    "crop_progress": {
      "as_of": "2026-09-28",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://esmis.nal.usda.gov/sites/default/release-files/796082/prog3926.txt"
    },
    "entsoe_de": {
      "as_of": "2026-09-30T07:30:00+00:00",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://transparency.entsoe.eu/"
    },
    "entsoe_fr": {
      "as_of": "2026-09-30T11:00:00+00:00",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://transparency.entsoe.eu/"
    },
    "gas": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://ir.eia.gov/ngs/ngs.html"
    },
    "gie": {
      "as_of": "2026-09-28",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "gie_fr": {
      "as_of": "2026-09-28",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "henry": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-30T01:19:56+00:00",
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
      "checked_at": "2026-09-30T01:19:56+00:00",
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
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_flows": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_history": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "published": "2026-09-23",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_price_history": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "provenance": "EIA · miroir datasets/oil-prices",
      "status": "ok",
      "url": "https://github.com/datasets/oil-prices"
    },
    "power_price_de": {
      "as_of": "2026-09-30T21:45:00+00:00",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "licence": "CC BY 4.0 (creativecommons.org/licenses/by/4.0) from Bundesnetzagentur | SMARD.de",
      "provenance": "Fraunhofer ISE Energy-Charts · day-ahead",
      "status": "ok",
      "url": "https://www.energy-charts.info/charts/price_spot_market/chart.htm?c=DE"
    },
    "power_price_fr": {
      "as_of": "2026-09-30T21:45:00+00:00",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "licence": "CC BY 4.0 (creativecommons.org/licenses/by/4.0) from Bundesnetzagentur | SMARD.de",
      "provenance": "Fraunhofer ISE Energy-Charts · day-ahead",
      "status": "ok",
      "url": "https://www.energy-charts.info/charts/price_spot_market/chart.htm?c=FR"
    },
    "rte_power": {
      "as_of": "2026-09-30T01:00:00+00:00",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "status": "ok",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/"
    },
    "wasde": {
      "as_of": "2026-09",
      "checked_at": "2026-09-30T01:19:56+00:00",
      "message": "Dernière donnée conservée ; source indisponible.",
      "status": "error",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt"
    },
    "wti": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-30T01:19:56+00:00",
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
  <script id="power-history-data" type="application/json">
{"schema":1,"source":"RTE éCO2mix national temps réel","url":"https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/","quality":"observé provisoire · un relevé par heure UTC","generated_at":"2026-09-30T01:19:56+00:00","first_at":"2026-09-20T07:45:00+00:00","last_at":"2026-09-30T01:00:00+00:00","points":[{"at":"2026-09-20T07:45:00+00:00","load":36025,"nucleaire":29829,"gaz":500,"eolien":2997,"solaire":7923,"hydraulique":1416,"bioenergies":958,"charbon":0,"fioul":33,"ech_physiques":-5492},{"at":"2026-09-20T08:45:00+00:00","load":38871,"nucleaire":29547,"gaz":501,"eolien":2047,"solaire":9922,"hydraulique":1479,"bioenergies":963,"charbon":0,"fioul":35,"ech_physiques":-4670},{"at":"2026-09-20T09:45:00+00:00","load":40689,"nucleaire":28030,"gaz":500,"eolien":1418,"solaire":11731,"hydraulique":1322,"bioenergies":964,"charbon":0,"fioul":33,"ech_physiques":-1268},{"at":"2026-09-20T10:45:00+00:00","load":41846,"nucleaire":28134,"gaz":500,"eolien":1169,"solaire":11673,"hydraulique":1404,"bioenergies":967,"charbon":0,"fioul":33,"ech_physiques":-180},{"at":"2026-09-20T11:45:00+00:00","load":39522,"nucleaire":28324,"gaz":500,"eolien":1148,"solaire":12532,"hydraulique":1323,"bioenergies":970,"charbon":0,"fioul":33,"ech_physiques":-2692},{"at":"2026-09-20T12:45:00+00:00","load":39673,"nucleaire":28790,"gaz":496,"eolien":1150,"solaire":11886,"hydraulique":1260,"bioenergies":967,"charbon":0,"fioul":33,"ech_physiques":-2453},{"at":"2026-09-20T13:45:00+00:00","load":38997,"nucleaire":29659,"gaz":490,"eolien":1176,"solaire":10663,"hydraulique":1338,"bioenergies":967,"charbon":0,"fioul":33,"ech_physiques":-3117},{"at":"2026-09-20T14:45:00+00:00","load":38550,"nucleaire":29922,"gaz":499,"eolien":3321,"solaire":12748,"hydraulique":1861,"bioenergies":968,"charbon":0,"fioul":33,"ech_physiques":-8135},{"at":"2026-09-20T15:45:00+00:00","load":39191,"nucleaire":32201,"gaz":494,"eolien":3292,"solaire":7921,"hydraulique":2192,"bioenergies":961,"charbon":0,"fioul":33,"ech_physiques":-6448},{"at":"2026-09-20T16:45:00+00:00","load":41609,"nucleaire":35421,"gaz":1065,"eolien":2833,"solaire":3218,"hydraulique":3317,"bioenergies":962,"charbon":0,"fioul":34,"ech_physiques":-5214},{"at":"2026-09-20T17:45:00+00:00","load":43046,"nucleaire":35677,"gaz":1476,"eolien":2526,"solaire":538,"hydraulique":5257,"bioenergies":961,"charbon":0,"fioul":37,"ech_physiques":-3837},{"at":"2026-09-20T18:45:00+00:00","load":42371,"nucleaire":35876,"gaz":1496,"eolien":3034,"solaire":218,"hydraulique":5231,"bioenergies":958,"charbon":0,"fioul":35,"ech_physiques":-4801},{"at":"2026-09-20T19:45:00+00:00","load":39936,"nucleaire":36019,"gaz":1501,"eolien":3215,"solaire":0,"hydraulique":3738,"bioenergies":962,"charbon":0,"fioul":35,"ech_physiques":-5423},{"at":"2026-09-20T20:45:00+00:00","load":40364,"nucleaire":36062,"gaz":1544,"eolien":3302,"solaire":0,"hydraulique":4301,"bioenergies":958,"charbon":0,"fioul":35,"ech_physiques":-5378},{"at":"2026-09-20T21:45:00+00:00","load":40445,"nucleaire":37084,"gaz":1626,"eolien":3026,"solaire":0,"hydraulique":3226,"bioenergies":965,"charbon":0,"fioul":35,"ech_physiques":-5522},{"at":"2026-09-20T22:45:00+00:00","load":36809,"nucleaire":37165,"gaz":805,"eolien":2888,"solaire":0,"hydraulique":3217,"bioenergies":967,"charbon":0,"fioul":34,"ech_physiques":-8279},{"at":"2026-09-20T23:45:00+00:00","load":36085,"nucleaire":37180,"gaz":472,"eolien":2925,"solaire":0,"hydraulique":2744,"bioenergies":970,"charbon":0,"fioul":33,"ech_physiques":-8204},{"at":"2026-09-21T00:45:00+00:00","load":33681,"nucleaire":37177,"gaz":485,"eolien":2833,"solaire":0,"hydraulique":2387,"bioenergies":977,"charbon":0,"fioul":35,"ech_physiques":-9920},{"at":"2026-09-21T01:45:00+00:00","load":32352,"nucleaire":37063,"gaz":490,"eolien":2748,"solaire":0,"hydraulique":2247,"bioenergies":973,"charbon":0,"fioul":33,"ech_physiques":-10292},{"at":"2026-09-21T02:45:00+00:00","load":32402,"nucleaire":37190,"gaz":669,"eolien":2690,"solaire":0,"hydraulique":2320,"bioenergies":970,"charbon":0,"fioul":35,"ech_physiques":-11014},{"at":"2026-09-21T03:45:00+00:00","load":35055,"nucleaire":37181,"gaz":1161,"eolien":2449,"solaire":0,"hydraulique":3254,"bioenergies":967,"charbon":0,"fioul":37,"ech_physiques":-9823},{"at":"2026-09-21T04:45:00+00:00","load":39329,"nucleaire":37337,"gaz":2124,"eolien":2342,"solaire":0,"hydraulique":5292,"bioenergies":961,"charbon":0,"fioul":37,"ech_physiques":-8807},{"at":"2026-09-21T05:45:00+00:00","load":43271,"nucleaire":37355,"gaz":3121,"eolien":2397,"solaire":308,"hydraulique":7593,"bioenergies":968,"charbon":0,"fioul":328,"ech_physiques":-9217},{"at":"2026-09-21T06:45:00+00:00","load":44945,"nucleaire":37327,"gaz":3242,"eolien":2420,"solaire":2625,"hydraulique":6133,"bioenergies":968,"charbon":0,"fioul":352,"ech_physiques":-8395},{"at":"2026-09-21T07:45:00+00:00","load":45824,"nucleaire":37233,"gaz":1722,"eolien":1886,"solaire":7401,"hydraulique":4058,"bioenergies":960,"charbon":0,"fioul":37,"ech_physiques":-7454},{"at":"2026-09-21T08:45:00+00:00","load":46549,"nucleaire":37109,"gaz":783,"eolien":1711,"solaire":12802,"hydraulique":2941,"bioenergies":954,"charbon":0,"fioul":37,"ech_physiques":-8394},{"at":"2026-09-21T09:45:00+00:00","load":47199,"nucleaire":36506,"gaz":546,"eolien":1926,"solaire":16583,"hydraulique":2307,"bioenergies":951,"charbon":0,"fioul":36,"ech_physiques":-9798},{"at":"2026-09-21T10:45:00+00:00","load":47489,"nucleaire":34252,"gaz":317,"eolien":2091,"solaire":18601,"hydraulique":2136,"bioenergies":953,"charbon":0,"fioul":37,"ech_physiques":-8913},{"at":"2026-09-21T11:45:00+00:00","load":46132,"nucleaire":34065,"gaz":344,"eolien":2181,"solaire":19160,"hydraulique":2182,"bioenergies":963,"charbon":0,"fioul":37,"ech_physiques":-10590},{"at":"2026-09-21T12:45:00+00:00","load":46737,"nucleaire":33888,"gaz":396,"eolien":2350,"solaire":18198,"hydraulique":2008,"bioenergies":956,"charbon":0,"fioul":37,"ech_physiques":-9050},{"at":"2026-09-21T13:45:00+00:00","load":45306,"nucleaire":34095,"gaz":436,"eolien":2363,"solaire":16845,"hydraulique":1912,"bioenergies":957,"charbon":0,"fioul":36,"ech_physiques":-9548},{"at":"2026-09-21T14:45:00+00:00","load":44917,"nucleaire":35071,"gaz":454,"eolien":2746,"solaire":13709,"hydraulique":2826,"bioenergies":957,"charbon":0,"fioul":36,"ech_physiques":-9507},{"at":"2026-09-21T15:45:00+00:00","load":45056,"nucleaire":36422,"gaz":1591,"eolien":3244,"solaire":8907,"hydraulique":4058,"bioenergies":956,"charbon":0,"fioul":35,"ech_physiques":-10337},{"at":"2026-09-21T16:45:00+00:00","load":47409,"nucleaire":36425,"gaz":3480,"eolien":3655,"solaire":3658,"hydraulique":7569,"bioenergies":959,"charbon":0,"fioul":35,"ech_physiques":-8555},{"at":"2026-09-21T17:45:00+00:00","load":48103,"nucleaire":36371,"gaz":3693,"eolien":3185,"solaire":511,"hydraulique":7716,"bioenergies":956,"charbon":0,"fioul":35,"ech_physiques":-4407},{"at":"2026-09-21T18:45:00+00:00","load":45774,"nucleaire":36321,"gaz":3833,"eolien":3775,"solaire":200,"hydraulique":7623,"bioenergies":956,"charbon":0,"fioul":35,"ech_physiques":-7334},{"at":"2026-09-21T19:45:00+00:00","load":42691,"nucleaire":36812,"gaz":4124,"eolien":4337,"solaire":0,"hydraulique":6996,"bioenergies":959,"charbon":0,"fioul":36,"ech_physiques":-10296},{"at":"2026-09-21T20:45:00+00:00","load":43441,"nucleaire":37196,"gaz":3795,"eolien":4179,"solaire":0,"hydraulique":5451,"bioenergies":958,"charbon":0,"fioul":36,"ech_physiques":-8171},{"at":"2026-09-21T21:45:00+00:00","load":41864,"nucleaire":37296,"gaz":2861,"eolien":4355,"solaire":0,"hydraulique":3767,"bioenergies":962,"charbon":0,"fioul":36,"ech_physiques":-7280},{"at":"2026-09-21T22:45:00+00:00","load":38810,"nucleaire":37315,"gaz":3006,"eolien":4384,"solaire":0,"hydraulique":3451,"bioenergies":958,"charbon":0,"fioul":35,"ech_physiques":-10386},{"at":"2026-09-21T23:45:00+00:00","load":37667,"nucleaire":37369,"gaz":2029,"eolien":4136,"solaire":0,"hydraulique":3211,"bioenergies":964,"charbon":0,"fioul":37,"ech_physiques":-9903},{"at":"2026-09-22T00:45:00+00:00","load":35453,"nucleaire":37416,"gaz":1854,"eolien":4095,"solaire":0,"hydraulique":2846,"bioenergies":959,"charbon":0,"fioul":36,"ech_physiques":-11669},{"at":"2026-09-22T01:45:00+00:00","load":33906,"nucleaire":37353,"gaz":1920,"eolien":3980,"solaire":0,"hydraulique":2924,"bioenergies":942,"charbon":0,"fioul":37,"ech_physiques":-12962},{"at":"2026-09-22T02:45:00+00:00","load":33816,"nucleaire":37515,"gaz":1882,"eolien":3831,"solaire":0,"hydraulique":3044,"bioenergies":945,"charbon":0,"fioul":37,"ech_physiques":-13386},{"at":"2026-09-22T03:45:00+00:00","load":35811,"nucleaire":37554,"gaz":2235,"eolien":3913,"solaire":0,"hydraulique":3647,"bioenergies":947,"charbon":0,"fioul":37,"ech_physiques":-12473},{"at":"2026-09-22T04:45:00+00:00","load":40670,"nucleaire":37556,"gaz":3140,"eolien":3892,"solaire":0,"hydraulique":5623,"bioenergies":942,"charbon":0,"fioul":37,"ech_physiques":-10525},{"at":"2026-09-22T05:45:00+00:00","load":43892,"nucleaire":37581,"gaz":3819,"eolien":3777,"solaire":277,"hydraulique":7845,"bioenergies":940,"charbon":0,"fioul":37,"ech_physiques":-10696},{"at":"2026-09-22T06:45:00+00:00","load":45214,"nucleaire":37549,"gaz":3835,"eolien":3449,"solaire":3026,"hydraulique":6808,"bioenergies":964,"charbon":0,"fioul":36,"ech_physiques":-10803},{"at":"2026-09-22T07:45:00+00:00","load":45921,"nucleaire":37335,"gaz":1798,"eolien":2342,"solaire":8634,"hydraulique":3517,"bioenergies":948,"charbon":0,"fioul":37,"ech_physiques":-8654},{"at":"2026-09-22T08:45:00+00:00","load":46856,"nucleaire":37322,"gaz":506,"eolien":2145,"solaire":14396,"hydraulique":2786,"bioenergies":969,"charbon":0,"fioul":36,"ech_physiques":-9837},{"at":"2026-09-22T09:45:00+00:00","load":47886,"nucleaire":36314,"gaz":285,"eolien":2673,"solaire":18090,"hydraulique":2517,"bioenergies":967,"charbon":0,"fioul":37,"ech_physiques":-10964},{"at":"2026-09-22T10:45:00+00:00","load":48257,"nucleaire":34436,"gaz":284,"eolien":2694,"solaire":19975,"hydraulique":2460,"bioenergies":966,"charbon":0,"fioul":37,"ech_physiques":-10497},{"at":"2026-09-22T11:45:00+00:00","load":46257,"nucleaire":33481,"gaz":282,"eolien":2665,"solaire":20335,"hydraulique":2359,"bioenergies":973,"charbon":0,"fioul":36,"ech_physiques":-11828},{"at":"2026-09-22T12:45:00+00:00","load":46727,"nucleaire":33673,"gaz":287,"eolien":2674,"solaire":19372,"hydraulique":2409,"bioenergies":963,"charbon":0,"fioul":36,"ech_physiques":-10649},{"at":"2026-09-22T13:45:00+00:00","load":46218,"nucleaire":34155,"gaz":281,"eolien":2890,"solaire":18232,"hydraulique":2351,"bioenergies":969,"charbon":0,"fioul":36,"ech_physiques":-10616},{"at":"2026-09-22T14:45:00+00:00","load":45165,"nucleaire":34815,"gaz":438,"eolien":3271,"solaire":15056,"hydraulique":2803,"bioenergies":966,"charbon":0,"fioul":35,"ech_physiques":-10572},{"at":"2026-09-22T15:45:00+00:00","load":45292,"nucleaire":36992,"gaz":1241,"eolien":3743,"solaire":9895,"hydraulique":3710,"bioenergies":971,"charbon":0,"fioul":35,"ech_physiques":-11078},{"at":"2026-09-22T16:45:00+00:00","load":47766,"nucleaire":37417,"gaz":4038,"eolien":3918,"solaire":3978,"hydraulique":7994,"bioenergies":969,"charbon":0,"fioul":906,"ech_physiques":-11820},{"at":"2026-09-22T17:45:00+00:00","load":48151,"nucleaire":37464,"gaz":4280,"eolien":3955,"solaire":494,"hydraulique":8527,"bioenergies":973,"charbon":0,"fioul":920,"ech_physiques":-8463},{"at":"2026-09-22T18:45:00+00:00","load":46077,"nucleaire":37548,"gaz":4397,"eolien":5081,"solaire":190,"hydraulique":7143,"bioenergies":974,"charbon":0,"fioul":683,"ech_physiques":-9865},{"at":"2026-09-22T19:45:00+00:00","load":42530,"nucleaire":37606,"gaz":3933,"eolien":6127,"solaire":0,"hydraulique":5981,"bioenergies":977,"charbon":0,"fioul":161,"ech_physiques":-12212},{"at":"2026-09-22T20:45:00+00:00","load":43536,"nucleaire":37643,"gaz":3645,"eolien":6606,"solaire":0,"hydraulique":6906,"bioenergies":975,"charbon":0,"fioul":33,"ech_physiques":-12278},{"at":"2026-09-22T21:45:00+00:00","load":41579,"nucleaire":38369,"gaz":3623,"eolien":6307,"solaire":0,"hydraulique":4975,"bioenergies":979,"charbon":0,"fioul":33,"ech_physiques":-12705},{"at":"2026-09-22T22:45:00+00:00","load":38570,"nucleaire":38378,"gaz":2994,"eolien":5686,"solaire":0,"hydraulique":4046,"bioenergies":979,"charbon":0,"fioul":34,"ech_physiques":-13602},{"at":"2026-09-22T23:45:00+00:00","load":38069,"nucleaire":38407,"gaz":1616,"eolien":5285,"solaire":0,"hydraulique":3838,"bioenergies":974,"charbon":0,"fioul":36,"ech_physiques":-12043},{"at":"2026-09-23T00:45:00+00:00","load":35455,"nucleaire":38343,"gaz":1356,"eolien":4717,"solaire":0,"hydraulique":3417,"bioenergies":977,"charbon":0,"fioul":37,"ech_physiques":-13078},{"at":"2026-09-23T01:45:00+00:00","load":34011,"nucleaire":38474,"gaz":1626,"eolien":3799,"solaire":0,"hydraulique":3303,"bioenergies":975,"charbon":0,"fioul":37,"ech_physiques":-13875},{"at":"2026-09-23T02:45:00+00:00","load":34140,"nucleaire":38528,"gaz":1474,"eolien":3014,"solaire":0,"hydraulique":3685,"bioenergies":979,"charbon":0,"fioul":37,"ech_physiques":-13275},{"at":"2026-09-23T03:45:00+00:00","load":36016,"nucleaire":38563,"gaz":2426,"eolien":2537,"solaire":0,"hydraulique":3489,"bioenergies":994,"charbon":0,"fioul":37,"ech_physiques":-12037},{"at":"2026-09-23T04:45:00+00:00","load":40459,"nucleaire":38583,"gaz":3667,"eolien":2195,"solaire":0,"hydraulique":5351,"bioenergies":1007,"charbon":0,"fioul":37,"ech_physiques":-10435},{"at":"2026-09-23T05:45:00+00:00","load":43656,"nucleaire":38544,"gaz":3853,"eolien":2018,"solaire":274,"hydraulique":7197,"bioenergies":997,"charbon":0,"fioul":37,"ech_physiques":-9616},{"at":"2026-09-23T06:45:00+00:00","load":45625,"nucleaire":38563,"gaz":3487,"eolien":1847,"solaire":3043,"hydraulique":5813,"bioenergies":1003,"charbon":0,"fioul":37,"ech_physiques":-8204},{"at":"2026-09-23T07:45:00+00:00","load":46280,"nucleaire":38535,"gaz":2419,"eolien":1134,"solaire":8521,"hydraulique":3438,"bioenergies":1005,"charbon":0,"fioul":37,"ech_physiques":-8773},{"at":"2026-09-23T08:45:00+00:00","load":46899,"nucleaire":37905,"gaz":1337,"eolien":858,"solaire":14066,"hydraulique":2444,"bioenergies":1001,"charbon":0,"fioul":37,"ech_physiques":-9564},{"at":"2026-09-23T09:45:00+00:00","load":48382,"nucleaire":37708,"gaz":736,"eolien":756,"solaire":17818,"hydraulique":2288,"bioenergies":1001,"charbon":0,"fioul":37,"ech_physiques":-10311},{"at":"2026-09-23T10:45:00+00:00","load":48871,"nucleaire":36783,"gaz":532,"eolien":916,"solaire":19568,"hydraulique":2204,"bioenergies":1004,"charbon":0,"fioul":36,"ech_physiques":-10224},{"at":"2026-09-23T11:45:00+00:00","load":47556,"nucleaire":35788,"gaz":488,"eolien":988,"solaire":19881,"hydraulique":2107,"bioenergies":1007,"charbon":0,"fioul":36,"ech_physiques":-10415},{"at":"2026-09-23T12:45:00+00:00","load":47942,"nucleaire":36556,"gaz":352,"eolien":1039,"solaire":18799,"hydraulique":1993,"bioenergies":1007,"charbon":0,"fioul":35,"ech_physiques":-10078},{"at":"2026-09-23T13:45:00+00:00","load":47720,"nucleaire":36656,"gaz":462,"eolien":1333,"solaire":17845,"hydraulique":2385,"bioenergies":1002,"charbon":0,"fioul":35,"ech_physiques":-10245},{"at":"2026-09-23T14:45:00+00:00","load":46616,"nucleaire":36587,"gaz":704,"eolien":1883,"solaire":14631,"hydraulique":3477,"bioenergies":1007,"charbon":0,"fioul":35,"ech_physiques":-9714},{"at":"2026-09-23T15:45:00+00:00","load":47107,"nucleaire":37562,"gaz":1693,"eolien":1689,"solaire":9497,"hydraulique":4946,"bioenergies":1002,"charbon":0,"fioul":35,"ech_physiques":-9441},{"at":"2026-09-23T16:45:00+00:00","load":48955,"nucleaire":37737,"gaz":3809,"eolien":1793,"solaire":3639,"hydraulique":7986,"bioenergies":1009,"charbon":0,"fioul":321,"ech_physiques":-7395},{"at":"2026-09-23T17:45:00+00:00","load":48747,"nucleaire":37787,"gaz":4256,"eolien":2104,"solaire":464,"hydraulique":8231,"bioenergies":1007,"charbon":0,"fioul":835,"ech_physiques":-5964},{"at":"2026-09-23T18:45:00+00:00","load":46721,"nucleaire":37830,"gaz":4324,"eolien":2635,"solaire":181,"hydraulique":7749,"bioenergies":1011,"charbon":0,"fioul":44,"ech_physiques":-7444},{"at":"2026-09-23T19:45:00+00:00","load":43540,"nucleaire":37925,"gaz":4143,"eolien":2861,"solaire":0,"hydraulique":5991,"bioenergies":1014,"charbon":0,"fioul":36,"ech_physiques":-8419},{"at":"2026-09-23T20:45:00+00:00","load":44019,"nucleaire":37754,"gaz":3739,"eolien":3008,"solaire":0,"hydraulique":4820,"bioenergies":1010,"charbon":0,"fioul":36,"ech_physiques":-6340},{"at":"2026-09-23T21:45:00+00:00","load":42785,"nucleaire":37077,"gaz":2772,"eolien":3015,"solaire":0,"hydraulique":4208,"bioenergies":1009,"charbon":0,"fioul":36,"ech_physiques":-5322},{"at":"2026-09-23T22:45:00+00:00","load":39596,"nucleaire":37007,"gaz":1864,"eolien":2882,"solaire":0,"hydraulique":4974,"bioenergies":1014,"charbon":0,"fioul":36,"ech_physiques":-8155},{"at":"2026-09-23T23:45:00+00:00","load":38515,"nucleaire":36990,"gaz":1405,"eolien":2916,"solaire":0,"hydraulique":3473,"bioenergies":1019,"charbon":0,"fioul":35,"ech_physiques":-7296},{"at":"2026-09-24T00:45:00+00:00","load":35896,"nucleaire":37014,"gaz":755,"eolien":2804,"solaire":0,"hydraulique":3572,"bioenergies":1017,"charbon":0,"fioul":33,"ech_physiques":-8491},{"at":"2026-09-24T01:45:00+00:00","load":34323,"nucleaire":37046,"gaz":770,"eolien":2608,"solaire":0,"hydraulique":3154,"bioenergies":1015,"charbon":0,"fioul":98,"ech_physiques":-9255},{"at":"2026-09-24T02:45:00+00:00","load":34486,"nucleaire":37102,"gaz":771,"eolien":2309,"solaire":0,"hydraulique":3057,"bioenergies":1003,"charbon":0,"fioul":100,"ech_physiques":-9221},{"at":"2026-09-24T03:45:00+00:00","load":36224,"nucleaire":37095,"gaz":2096,"eolien":1976,"solaire":0,"hydraulique":3299,"bioenergies":999,"charbon":0,"fioul":101,"ech_physiques":-8878},{"at":"2026-09-24T04:45:00+00:00","load":40794,"nucleaire":37123,"gaz":3455,"eolien":1837,"solaire":0,"hydraulique":4266,"bioenergies":999,"charbon":0,"fioul":37,"ech_physiques":-7212},{"at":"2026-09-24T05:45:00+00:00","load":44431,"nucleaire":37127,"gaz":3561,"eolien":1713,"solaire":244,"hydraulique":6792,"bioenergies":1011,"charbon":0,"fioul":36,"ech_physiques":-6402},{"at":"2026-09-24T06:45:00+00:00","load":45971,"nucleaire":37045,"gaz":3559,"eolien":1650,"solaire":2646,"hydraulique":6124,"bioenergies":1011,"charbon":0,"fioul":37,"ech_physiques":-6425},{"at":"2026-09-24T07:45:00+00:00","load":46592,"nucleaire":36785,"gaz":3080,"eolien":1437,"solaire":6864,"hydraulique":3830,"bioenergies":1012,"charbon":0,"fioul":37,"ech_physiques":-6442},{"at":"2026-09-24T08:45:00+00:00","load":47584,"nucleaire":36688,"gaz":1119,"eolien":1008,"solaire":11675,"hydraulique":3055,"bioenergies":1005,"charbon":0,"fioul":37,"ech_physiques":-6455},{"at":"2026-09-24T09:45:00+00:00","load":48081,"nucleaire":36609,"gaz":949,"eolien":742,"solaire":15059,"hydraulique":3419,"bioenergies":1003,"charbon":0,"fioul":36,"ech_physiques":-8173},{"at":"2026-09-24T10:45:00+00:00","load":48795,"nucleaire":36711,"gaz":1059,"eolien":696,"solaire":16915,"hydraulique":3314,"bioenergies":1002,"charbon":0,"fioul":36,"ech_physiques":-8711},{"at":"2026-09-24T11:45:00+00:00","load":48126,"nucleaire":36540,"gaz":390,"eolien":704,"solaire":17300,"hydraulique":2744,"bioenergies":1007,"charbon":0,"fioul":36,"ech_physiques":-8850},{"at":"2026-09-24T12:45:00+00:00","load":48432,"nucleaire":36500,"gaz":681,"eolien":664,"solaire":16316,"hydraulique":2922,"bioenergies":1007,"charbon":0,"fioul":35,"ech_physiques":-7910},{"at":"2026-09-24T13:45:00+00:00","load":47374,"nucleaire":36644,"gaz":978,"eolien":721,"solaire":14582,"hydraulique":3064,"bioenergies":991,"charbon":0,"fioul":35,"ech_physiques":-8126},{"at":"2026-09-24T14:45:00+00:00","load":46801,"nucleaire":36459,"gaz":1104,"eolien":798,"solaire":11859,"hydraulique":3641,"bioenergies":995,"charbon":0,"fioul":35,"ech_physiques":-6931},{"at":"2026-09-24T15:45:00+00:00","load":46573,"nucleaire":36702,"gaz":3428,"eolien":819,"solaire":7614,"hydraulique":4208,"bioenergies":998,"charbon":0,"fioul":35,"ech_physiques":-7375},{"at":"2026-09-24T16:45:00+00:00","load":48474,"nucleaire":36740,"gaz":3878,"eolien":894,"solaire":3060,"hydraulique":6978,"bioenergies":999,"charbon":0,"fioul":35,"ech_physiques":-4107},{"at":"2026-09-24T17:45:00+00:00","load":48724,"nucleaire":36804,"gaz":4345,"eolien":1266,"solaire":435,"hydraulique":8483,"bioenergies":998,"charbon":0,"fioul":35,"ech_physiques":-3963},{"at":"2026-09-24T18:45:00+00:00","load":46471,"nucleaire":36838,"gaz":4641,"eolien":1919,"solaire":189,"hydraulique":7927,"bioenergies":999,"charbon":0,"fioul":35,"ech_physiques":-6351},{"at":"2026-09-24T19:45:00+00:00","load":43271,"nucleaire":36969,"gaz":4617,"eolien":2830,"solaire":0,"hydraulique":6592,"bioenergies":1000,"charbon":0,"fioul":36,"ech_physiques":-8627},{"at":"2026-09-24T20:45:00+00:00","load":44149,"nucleaire":37565,"gaz":4659,"eolien":3394,"solaire":0,"hydraulique":5071,"bioenergies":995,"charbon":0,"fioul":36,"ech_physiques":-7552},{"at":"2026-09-24T21:45:00+00:00","load":42584,"nucleaire":37723,"gaz":3884,"eolien":3723,"solaire":0,"hydraulique":4341,"bioenergies":1008,"charbon":0,"fioul":35,"ech_physiques":-8111},{"at":"2026-09-24T22:45:00+00:00","load":39586,"nucleaire":37852,"gaz":3407,"eolien":3962,"solaire":0,"hydraulique":3615,"bioenergies":997,"charbon":0,"fioul":37,"ech_physiques":-9909},{"at":"2026-09-24T23:45:00+00:00","load":38413,"nucleaire":37866,"gaz":2400,"eolien":4000,"solaire":0,"hydraulique":3058,"bioenergies":1009,"charbon":0,"fioul":36,"ech_physiques":-9858},{"at":"2026-09-25T00:45:00+00:00","load":35758,"nucleaire":37979,"gaz":1597,"eolien":3649,"solaire":0,"hydraulique":2850,"bioenergies":1007,"charbon":0,"fioul":37,"ech_physiques":-11075},{"at":"2026-09-25T01:45:00+00:00","load":34441,"nucleaire":38550,"gaz":1464,"eolien":3355,"solaire":0,"hydraulique":2756,"bioenergies":1008,"charbon":0,"fioul":36,"ech_physiques":-12356},{"at":"2026-09-25T02:45:00+00:00","load":34240,"nucleaire":39125,"gaz":1555,"eolien":3284,"solaire":0,"hydraulique":2797,"bioenergies":1008,"charbon":0,"fioul":37,"ech_physiques":-12678},{"at":"2026-09-25T03:45:00+00:00","load":36409,"nucleaire":39138,"gaz":1957,"eolien":3100,"solaire":0,"hydraulique":2919,"bioenergies":1018,"charbon":0,"fioul":37,"ech_physiques":-11404},{"at":"2026-09-25T04:45:00+00:00","load":40844,"nucleaire":38994,"gaz":3360,"eolien":3142,"solaire":0,"hydraulique":4540,"bioenergies":1007,"charbon":0,"fioul":37,"ech_physiques":-10223},{"at":"2026-09-25T05:45:00+00:00","load":44279,"nucleaire":39191,"gaz":3375,"eolien":3310,"solaire":236,"hydraulique":6806,"bioenergies":1005,"charbon":0,"fioul":37,"ech_physiques":-10068},{"at":"2026-09-25T06:45:00+00:00","load":45702,"nucleaire":38110,"gaz":3399,"eolien":3368,"solaire":2687,"hydraulique":6449,"bioenergies":994,"charbon":0,"fioul":36,"ech_physiques":-9449},{"at":"2026-09-25T07:45:00+00:00","load":46235,"nucleaire":38047,"gaz":1361,"eolien":2345,"solaire":8074,"hydraulique":4052,"bioenergies":1007,"charbon":0,"fioul":37,"ech_physiques":-8541},{"at":"2026-09-25T08:45:00+00:00","load":47507,"nucleaire":37250,"gaz":539,"eolien":1466,"solaire":13840,"hydraulique":2809,"bioenergies":1000,"charbon":0,"fioul":37,"ech_physiques":-8012},{"at":"2026-09-25T09:45:00+00:00","load":48343,"nucleaire":36080,"gaz":296,"eolien":1247,"solaire":17650,"hydraulique":2430,"bioenergies":988,"charbon":0,"fioul":37,"ech_physiques":-8545},{"at":"2026-09-25T10:45:00+00:00","load":48983,"nucleaire":35948,"gaz":292,"eolien":1326,"solaire":19651,"hydraulique":2298,"bioenergies":990,"charbon":0,"fioul":37,"ech_physiques":-9136},{"at":"2026-09-25T11:45:00+00:00","load":46770,"nucleaire":33906,"gaz":288,"eolien":1330,"solaire":19928,"hydraulique":2217,"bioenergies":990,"charbon":0,"fioul":37,"ech_physiques":-9183},{"at":"2026-09-25T12:45:00+00:00","load":47278,"nucleaire":34156,"gaz":323,"eolien":1421,"solaire":18953,"hydraulique":2011,"bioenergies":985,"charbon":0,"fioul":37,"ech_physiques":-8345},{"at":"2026-09-25T13:45:00+00:00","load":46873,"nucleaire":34660,"gaz":428,"eolien":1676,"solaire":17688,"hydraulique":2059,"bioenergies":986,"charbon":0,"fioul":153,"ech_physiques":-8511},{"at":"2026-09-25T14:45:00+00:00","load":46186,"nucleaire":35765,"gaz":999,"eolien":1909,"solaire":14394,"hydraulique":2576,"bioenergies":986,"charbon":0,"fioul":37,"ech_physiques":-8714},{"at":"2026-09-25T15:45:00+00:00","load":46662,"nucleaire":36175,"gaz":2179,"eolien":2464,"solaire":9092,"hydraulique":5213,"bioenergies":994,"charbon":0,"fioul":380,"ech_physiques":-9852},{"at":"2026-09-25T16:45:00+00:00","load":47715,"nucleaire":36346,"gaz":4367,"eolien":2540,"solaire":3261,"hydraulique":8852,"bioenergies":995,"charbon":0,"fioul":701,"ech_physiques":-9462},{"at":"2026-09-25T17:45:00+00:00","load":47537,"nucleaire":36374,"gaz":4504,"eolien":2582,"solaire":376,"hydraulique":8522,"bioenergies":997,"charbon":0,"fioul":718,"ech_physiques":-6625},{"at":"2026-09-25T18:45:00+00:00","load":45955,"nucleaire":35550,"gaz":4592,"eolien":2793,"solaire":188,"hydraulique":8560,"bioenergies":993,"charbon":0,"fioul":735,"ech_physiques":-7684},{"at":"2026-09-25T19:45:00+00:00","load":43206,"nucleaire":35320,"gaz":4553,"eolien":3590,"solaire":0,"hydraulique":6970,"bioenergies":1003,"charbon":0,"fioul":740,"ech_physiques":-8992},{"at":"2026-09-25T20:45:00+00:00","load":44175,"nucleaire":34542,"gaz":4490,"eolien":3979,"solaire":0,"hydraulique":6584,"bioenergies":1014,"charbon":0,"fioul":501,"ech_physiques":-6587},{"at":"2026-09-25T21:45:00+00:00","load":42041,"nucleaire":33914,"gaz":4298,"eolien":3894,"solaire":0,"hydraulique":5295,"bioenergies":1017,"charbon":0,"fioul":37,"ech_physiques":-6127},{"at":"2026-09-25T22:45:00+00:00","load":38630,"nucleaire":33841,"gaz":3980,"eolien":3494,"solaire":0,"hydraulique":5088,"bioenergies":1012,"charbon":0,"fioul":36,"ech_physiques":-8933},{"at":"2026-09-25T23:45:00+00:00","load":37425,"nucleaire":33742,"gaz":3991,"eolien":3197,"solaire":0,"hydraulique":3346,"bioenergies":1026,"charbon":0,"fioul":36,"ech_physiques":-7890},{"at":"2026-09-26T00:45:00+00:00","load":35188,"nucleaire":33833,"gaz":3835,"eolien":3168,"solaire":0,"hydraulique":2791,"bioenergies":1013,"charbon":0,"fioul":36,"ech_physiques":-9314},{"at":"2026-09-26T01:45:00+00:00","load":33413,"nucleaire":33919,"gaz":3494,"eolien":3242,"solaire":0,"hydraulique":2414,"bioenergies":1010,"charbon":0,"fioul":36,"ech_physiques":-10432},{"at":"2026-09-26T02:45:00+00:00","load":32636,"nucleaire":33898,"gaz":3541,"eolien":2921,"solaire":0,"hydraulique":2343,"bioenergies":1013,"charbon":0,"fioul":37,"ech_physiques":-10867},{"at":"2026-09-26T03:45:00+00:00","load":32878,"nucleaire":33854,"gaz":3582,"eolien":2634,"solaire":0,"hydraulique":2463,"bioenergies":1009,"charbon":0,"fioul":36,"ech_physiques":-10644},{"at":"2026-09-26T04:45:00+00:00","load":34212,"nucleaire":33897,"gaz":3740,"eolien":2637,"solaire":0,"hydraulique":3192,"bioenergies":1005,"charbon":0,"fioul":37,"ech_physiques":-10252},{"at":"2026-09-26T05:45:00+00:00","load":35422,"nucleaire":33946,"gaz":3610,"eolien":2750,"solaire":214,"hydraulique":3485,"bioenergies":1008,"charbon":0,"fioul":37,"ech_physiques":-9716},{"at":"2026-09-26T06:45:00+00:00","load":37748,"nucleaire":33694,"gaz":2287,"eolien":2872,"solaire":2027,"hydraulique":3339,"bioenergies":1008,"charbon":0,"fioul":33,"ech_physiques":-7295},{"at":"2026-09-26T07:45:00+00:00","load":39991,"nucleaire":33326,"gaz":661,"eolien":2413,"solaire":5721,"hydraulique":2602,"bioenergies":1005,"charbon":0,"fioul":33,"ech_physiques":-5502},{"at":"2026-09-26T08:45:00+00:00","load":41100,"nucleaire":32568,"gaz":553,"eolien":2209,"solaire":10109,"hydraulique":2094,"bioenergies":1005,"charbon":0,"fioul":33,"ech_physiques":-5284},{"at":"2026-09-26T09:45:00+00:00","load":42951,"nucleaire":31740,"gaz":278,"eolien":1927,"solaire":13153,"hydraulique":1882,"bioenergies":1008,"charbon":0,"fioul":33,"ech_physiques":-4610},{"at":"2026-09-26T10:45:00+00:00","load":43852,"nucleaire":28980,"gaz":274,"eolien":1630,"solaire":15141,"hydraulique":1869,"bioenergies":998,"charbon":0,"fioul":33,"ech_physiques":-2469},{"at":"2026-09-26T11:45:00+00:00","load":41333,"nucleaire":28690,"gaz":285,"eolien":1470,"solaire":16669,"hydraulique":1934,"bioenergies":1011,"charbon":0,"fioul":33,"ech_physiques":-5824},{"at":"2026-09-26T12:45:00+00:00","load":41280,"nucleaire":29515,"gaz":283,"eolien":1350,"solaire":16670,"hydraulique":1950,"bioenergies":1009,"charbon":0,"fioul":32,"ech_physiques":-6787},{"at":"2026-09-26T13:45:00+00:00","load":40458,"nucleaire":31056,"gaz":285,"eolien":1278,"solaire":16181,"hydraulique":2114,"bioenergies":1013,"charbon":0,"fioul":32,"ech_physiques":-9172},{"at":"2026-09-26T14:45:00+00:00","load":39865,"nucleaire":32357,"gaz":297,"eolien":1297,"solaire":13272,"hydraulique":2722,"bioenergies":971,"charbon":0,"fioul":33,"ech_physiques":-9317},{"at":"2026-09-26T15:45:00+00:00","load":40877,"nucleaire":33448,"gaz":2263,"eolien":1417,"solaire":8488,"hydraulique":3133,"bioenergies":1012,"charbon":0,"fioul":33,"ech_physiques":-8898},{"at":"2026-09-26T16:45:00+00:00","load":42110,"nucleaire":33525,"gaz":3636,"eolien":1547,"solaire":3033,"hydraulique":6232,"bioenergies":1013,"charbon":0,"fioul":35,"ech_physiques":-6903},{"at":"2026-09-26T17:45:00+00:00","load":42916,"nucleaire":33606,"gaz":3912,"eolien":1617,"solaire":356,"hydraulique":7065,"bioenergies":1013,"charbon":0,"fioul":35,"ech_physiques":-4692},{"at":"2026-09-26T18:45:00+00:00","load":41295,"nucleaire":33712,"gaz":3944,"eolien":1936,"solaire":186,"hydraulique":6333,"bioenergies":1014,"charbon":0,"fioul":34,"ech_physiques":-6213},{"at":"2026-09-26T19:45:00+00:00","load":39282,"nucleaire":33676,"gaz":3940,"eolien":2298,"solaire":0,"hydraulique":4832,"bioenergies":1004,"charbon":0,"fioul":36,"ech_physiques":-6753},{"at":"2026-09-26T20:45:00+00:00","load":40644,"nucleaire":33674,"gaz":3807,"eolien":2552,"solaire":0,"hydraulique":4380,"bioenergies":1016,"charbon":0,"fioul":35,"ech_physiques":-4804},{"at":"2026-09-26T21:45:00+00:00","load":39625,"nucleaire":33883,"gaz":3537,"eolien":2446,"solaire":0,"hydraulique":3401,"bioenergies":1015,"charbon":0,"fioul":37,"ech_physiques":-4657},{"at":"2026-09-26T22:45:00+00:00","load":36722,"nucleaire":34343,"gaz":3291,"eolien":2425,"solaire":0,"hydraulique":3663,"bioenergies":1015,"charbon":0,"fioul":37,"ech_physiques":-7614},{"at":"2026-09-26T23:45:00+00:00","load":35954,"nucleaire":34442,"gaz":2462,"eolien":2256,"solaire":0,"hydraulique":3038,"bioenergies":1018,"charbon":0,"fioul":37,"ech_physiques":-6911},{"at":"2026-09-27T00:45:00+00:00","load":33265,"nucleaire":34795,"gaz":226,"eolien":2163,"solaire":0,"hydraulique":2824,"bioenergies":1011,"charbon":0,"fioul":37,"ech_physiques":-6708},{"at":"2026-09-27T01:45:00+00:00","load":31603,"nucleaire":34556,"gaz":232,"eolien":2372,"solaire":0,"hydraulique":3193,"bioenergies":1015,"charbon":0,"fioul":36,"ech_physiques":-8700},{"at":"2026-09-27T02:45:00+00:00","load":30806,"nucleaire":34090,"gaz":239,"eolien":2400,"solaire":0,"hydraulique":2598,"bioenergies":1012,"charbon":0,"fioul":37,"ech_physiques":-8477},{"at":"2026-09-27T03:45:00+00:00","load":31146,"nucleaire":34130,"gaz":232,"eolien":2663,"solaire":0,"hydraulique":2083,"bioenergies":1017,"charbon":0,"fioul":37,"ech_physiques":-8312},{"at":"2026-09-27T04:45:00+00:00","load":32117,"nucleaire":34092,"gaz":244,"eolien":3016,"solaire":0,"hydraulique":2078,"bioenergies":1014,"charbon":0,"fioul":37,"ech_physiques":-7680},{"at":"2026-09-27T05:45:00+00:00","load":32303,"nucleaire":33997,"gaz":244,"eolien":3313,"solaire":195,"hydraulique":2183,"bioenergies":1017,"charbon":0,"fioul":37,"ech_physiques":-8005},{"at":"2026-09-27T06:45:00+00:00","load":33915,"nucleaire":33485,"gaz":243,"eolien":3594,"solaire":2171,"hydraulique":2069,"bioenergies":1007,"charbon":0,"fioul":37,"ech_physiques":-7225},{"at":"2026-09-27T07:45:00+00:00","load":35634,"nucleaire":32562,"gaz":488,"eolien":3373,"solaire":6409,"hydraulique":1657,"bioenergies":995,"charbon":0,"fioul":37,"ech_physiques":-7545},{"at":"2026-09-27T08:45:00+00:00","load":38023,"nucleaire":27590,"gaz":507,"eolien":2793,"solaire":11476,"hydraulique":1525,"bioenergies":988,"charbon":0,"fioul":37,"ech_physiques":-4159},{"at":"2026-09-27T09:45:00+00:00","load":40176,"nucleaire":25712,"gaz":492,"eolien":3093,"solaire":15064,"hydraulique":1571,"bioenergies":992,"charbon":0,"fioul":37,"ech_physiques":-4786},{"at":"2026-09-27T10:45:00+00:00","load":41374,"nucleaire":25711,"gaz":472,"eolien":2413,"solaire":12945,"hydraulique":1555,"bioenergies":1010,"charbon":0,"fioul":37,"ech_physiques":-441},{"at":"2026-09-27T11:45:00+00:00","load":38297,"nucleaire":26118,"gaz":264,"eolien":1359,"solaire":10811,"hydraulique":1574,"bioenergies":997,"charbon":0,"fioul":37,"ech_physiques":-46},{"at":"2026-09-27T12:45:00+00:00","load":39565,"nucleaire":25860,"gaz":255,"eolien":2081,"solaire":11073,"hydraulique":1811,"bioenergies":1006,"charbon":0,"fioul":36,"ech_physiques":12},{"at":"2026-09-27T13:45:00+00:00","load":38753,"nucleaire":26121,"gaz":255,"eolien":4147,"solaire":14165,"hydraulique":1909,"bioenergies":1005,"charbon":0,"fioul":37,"ech_physiques":-5920},{"at":"2026-09-27T14:45:00+00:00","load":38955,"nucleaire":29315,"gaz":726,"eolien":4150,"solaire":11078,"hydraulique":2306,"bioenergies":1011,"charbon":0,"fioul":37,"ech_physiques":-8015},{"at":"2026-09-27T15:45:00+00:00","load":40041,"nucleaire":32362,"gaz":1170,"eolien":3432,"solaire":6355,"hydraulique":2978,"bioenergies":1009,"charbon":0,"fioul":37,"ech_physiques":-6980},{"at":"2026-09-27T16:45:00+00:00","load":42493,"nucleaire":32492,"gaz":2651,"eolien":2553,"solaire":2119,"hydraulique":5413,"bioenergies":1011,"charbon":0,"fioul":37,"ech_physiques":-3805},{"at":"2026-09-27T17:45:00+00:00","load":44171,"nucleaire":32692,"gaz":2764,"eolien":2178,"solaire":335,"hydraulique":5737,"bioenergies":1011,"charbon":0,"fioul":37,"ech_physiques":-575},{"at":"2026-09-27T18:45:00+00:00","load":42401,"nucleaire":32753,"gaz":2878,"eolien":2334,"solaire":195,"hydraulique":4426,"bioenergies":1012,"charbon":0,"fioul":37,"ech_physiques":-1176},{"at":"2026-09-27T19:45:00+00:00","load":40182,"nucleaire":32793,"gaz":2480,"eolien":2493,"solaire":0,"hydraulique":3704,"bioenergies":1004,"charbon":0,"fioul":37,"ech_physiques":-2315},{"at":"2026-09-27T20:45:00+00:00","load":41264,"nucleaire":32819,"gaz":2490,"eolien":2599,"solaire":0,"hydraulique":3410,"bioenergies":1002,"charbon":0,"fioul":36,"ech_physiques":-1051},{"at":"2026-09-27T21:45:00+00:00","load":39849,"nucleaire":32879,"gaz":2105,"eolien":2731,"solaire":0,"hydraulique":2845,"bioenergies":998,"charbon":0,"fioul":37,"ech_physiques":-1732},{"at":"2026-09-27T22:45:00+00:00","load":37022,"nucleaire":33024,"gaz":1221,"eolien":2711,"solaire":0,"hydraulique":2314,"bioenergies":999,"charbon":0,"fioul":37,"ech_physiques":-2312},{"at":"2026-09-27T23:45:00+00:00","load":36178,"nucleaire":33200,"gaz":1293,"eolien":2519,"solaire":0,"hydraulique":2399,"bioenergies":998,"charbon":0,"fioul":37,"ech_physiques":-3653},{"at":"2026-09-28T00:45:00+00:00","load":33960,"nucleaire":33520,"gaz":1310,"eolien":2221,"solaire":0,"hydraulique":2096,"bioenergies":1005,"charbon":0,"fioul":37,"ech_physiques":-5810},{"at":"2026-09-28T01:45:00+00:00","load":32739,"nucleaire":33903,"gaz":1371,"eolien":2397,"solaire":0,"hydraulique":2068,"bioenergies":993,"charbon":0,"fioul":37,"ech_physiques":-7483},{"at":"2026-09-28T02:45:00+00:00","load":32640,"nucleaire":33875,"gaz":1347,"eolien":2800,"solaire":0,"hydraulique":2257,"bioenergies":996,"charbon":0,"fioul":37,"ech_physiques":-8405},{"at":"2026-09-28T03:45:00+00:00","load":35340,"nucleaire":34546,"gaz":3283,"eolien":3044,"solaire":0,"hydraulique":2549,"bioenergies":1000,"charbon":0,"fioul":37,"ech_physiques":-9066},{"at":"2026-09-28T04:45:00+00:00","load":40092,"nucleaire":34561,"gaz":3932,"eolien":2806,"solaire":0,"hydraulique":5019,"bioenergies":993,"charbon":0,"fioul":37,"ech_physiques":-7269},{"at":"2026-09-28T05:45:00+00:00","load":43563,"nucleaire":34554,"gaz":3983,"eolien":2990,"solaire":219,"hydraulique":6577,"bioenergies":991,"charbon":0,"fioul":37,"ech_physiques":-6121},{"at":"2026-09-28T06:45:00+00:00","load":45360,"nucleaire":34552,"gaz":3957,"eolien":2924,"solaire":1741,"hydraulique":5036,"bioenergies":978,"charbon":0,"fioul":37,"ech_physiques":-3993},{"at":"2026-09-28T07:45:00+00:00","load":46475,"nucleaire":34444,"gaz":3733,"eolien":2890,"solaire":4470,"hydraulique":4194,"bioenergies":987,"charbon":0,"fioul":36,"ech_physiques":-4259},{"at":"2026-09-28T08:45:00+00:00","load":47676,"nucleaire":34383,"gaz":3161,"eolien":2658,"solaire":8032,"hydraulique":2934,"bioenergies":991,"charbon":0,"fioul":37,"ech_physiques":-4026},{"at":"2026-09-28T09:45:00+00:00","load":48383,"nucleaire":34417,"gaz":1682,"eolien":2192,"solaire":11138,"hydraulique":2470,"bioenergies":995,"charbon":0,"fioul":37,"ech_physiques":-3828},{"at":"2026-09-28T10:45:00+00:00","load":48896,"nucleaire":33336,"gaz":1219,"eolien":2313,"solaire":12755,"hydraulique":2280,"bioenergies":992,"charbon":0,"fioul":37,"ech_physiques":-3126},{"at":"2026-09-28T11:45:00+00:00","load":47528,"nucleaire":33306,"gaz":1314,"eolien":2200,"solaire":13617,"hydraulique":2307,"bioenergies":991,"charbon":0,"fioul":37,"ech_physiques":-5020},{"at":"2026-09-28T12:45:00+00:00","load":48738,"nucleaire":33582,"gaz":1384,"eolien":2280,"solaire":13074,"hydraulique":2424,"bioenergies":996,"charbon":0,"fioul":37,"ech_physiques":-4338},{"at":"2026-09-28T13:45:00+00:00","load":47708,"nucleaire":33894,"gaz":1806,"eolien":2219,"solaire":11568,"hydraulique":2670,"bioenergies":980,"charbon":0,"fioul":37,"ech_physiques":-5186},{"at":"2026-09-28T14:45:00+00:00","load":46249,"nucleaire":34230,"gaz":3222,"eolien":2352,"solaire":8759,"hydraulique":4143,"bioenergies":982,"charbon":0,"fioul":37,"ech_physiques":-7462},{"at":"2026-09-28T15:45:00+00:00","load":46003,"nucleaire":34394,"gaz":3374,"eolien":2398,"solaire":5255,"hydraulique":6864,"bioenergies":991,"charbon":0,"fioul":37,"ech_physiques":-7544},{"at":"2026-09-28T16:45:00+00:00","load":47932,"nucleaire":34387,"gaz":3616,"eolien":2571,"solaire":1839,"hydraulique":7932,"bioenergies":999,"charbon":0,"fioul":382,"ech_physiques":-4045},{"at":"2026-09-28T17:45:00+00:00","load":49212,"nucleaire":34830,"gaz":3635,"eolien":2714,"solaire":331,"hydraulique":7484,"bioenergies":1024,"charbon":0,"fioul":384,"ech_physiques":-1221},{"at":"2026-09-28T18:45:00+00:00","load":46153,"nucleaire":34882,"gaz":3761,"eolien":3429,"solaire":203,"hydraulique":7100,"bioenergies":1033,"charbon":0,"fioul":305,"ech_physiques":-4836},{"at":"2026-09-28T19:45:00+00:00","load":43136,"nucleaire":34904,"gaz":3988,"eolien":4172,"solaire":0,"hydraulique":5137,"bioenergies":1047,"charbon":0,"fioul":37,"ech_physiques":-6135},{"at":"2026-09-28T20:45:00+00:00","load":43753,"nucleaire":34904,"gaz":3862,"eolien":4407,"solaire":0,"hydraulique":4707,"bioenergies":1053,"charbon":0,"fioul":37,"ech_physiques":-5177},{"at":"2026-09-28T21:45:00+00:00","load":41880,"nucleaire":34928,"gaz":3324,"eolien":4592,"solaire":0,"hydraulique":3431,"bioenergies":1053,"charbon":0,"fioul":37,"ech_physiques":-5402},{"at":"2026-09-28T22:45:00+00:00","load":38813,"nucleaire":34487,"gaz":3079,"eolien":4718,"solaire":0,"hydraulique":2560,"bioenergies":1063,"charbon":0,"fioul":36,"ech_physiques":-7111},{"at":"2026-09-28T23:45:00+00:00","load":38156,"nucleaire":33879,"gaz":2850,"eolien":4852,"solaire":0,"hydraulique":2499,"bioenergies":1057,"charbon":0,"fioul":37,"ech_physiques":-7009},{"at":"2026-09-29T00:45:00+00:00","load":35592,"nucleaire":33915,"gaz":2528,"eolien":4817,"solaire":0,"hydraulique":2291,"bioenergies":1060,"charbon":0,"fioul":37,"ech_physiques":-9048},{"at":"2026-09-29T01:45:00+00:00","load":33973,"nucleaire":33951,"gaz":2232,"eolien":4980,"solaire":0,"hydraulique":2344,"bioenergies":1060,"charbon":0,"fioul":37,"ech_physiques":-10224},{"at":"2026-09-29T02:45:00+00:00","load":34068,"nucleaire":34162,"gaz":2222,"eolien":4755,"solaire":0,"hydraulique":2252,"bioenergies":1050,"charbon":0,"fioul":37,"ech_physiques":-9446},{"at":"2026-09-29T03:45:00+00:00","load":36122,"nucleaire":34306,"gaz":2321,"eolien":5419,"solaire":0,"hydraulique":2761,"bioenergies":1047,"charbon":0,"fioul":37,"ech_physiques":-9667},{"at":"2026-09-29T04:45:00+00:00","load":40550,"nucleaire":34274,"gaz":3357,"eolien":5647,"solaire":0,"hydraulique":3579,"bioenergies":1052,"charbon":0,"fioul":37,"ech_physiques":-7496},{"at":"2026-09-29T05:45:00+00:00","load":44456,"nucleaire":34232,"gaz":3713,"eolien":5950,"solaire":220,"hydraulique":5278,"bioenergies":1052,"charbon":0,"fioul":37,"ech_physiques":-6361},{"at":"2026-09-29T06:45:00+00:00","load":46338,"nucleaire":34289,"gaz":3613,"eolien":6276,"solaire":1689,"hydraulique":4139,"bioenergies":1063,"charbon":0,"fioul":37,"ech_physiques":-4781},{"at":"2026-09-29T07:45:00+00:00","load":46901,"nucleaire":34282,"gaz":3091,"eolien":6058,"solaire":4588,"hydraulique":2762,"bioenergies":1076,"charbon":0,"fioul":37,"ech_physiques":-4978},{"at":"2026-09-29T08:45:00+00:00","load":47902,"nucleaire":34193,"gaz":1526,"eolien":5891,"solaire":8438,"hydraulique":1955,"bioenergies":1091,"charbon":0,"fioul":37,"ech_physiques":-5188},{"at":"2026-09-29T09:45:00+00:00","load":48637,"nucleaire":33886,"gaz":683,"eolien":5853,"solaire":11598,"hydraulique":1583,"bioenergies":1100,"charbon":0,"fioul":37,"ech_physiques":-5706},{"at":"2026-09-29T10:45:00+00:00","load":49123,"nucleaire":33501,"gaz":251,"eolien":6375,"solaire":13887,"hydraulique":1627,"bioenergies":1102,"charbon":0,"fioul":36,"ech_physiques":-6808},{"at":"2026-09-29T11:45:00+00:00","load":48237,"nucleaire":32852,"gaz":267,"eolien":6793,"solaire":15172,"hydraulique":1577,"bioenergies":1095,"charbon":0,"fioul":37,"ech_physiques":-8677},{"at":"2026-09-29T12:45:00+00:00","load":48972,"nucleaire":32860,"gaz":264,"eolien":7534,"solaire":14200,"hydraulique":1743,"bioenergies":1101,"charbon":0,"fioul":37,"ech_physiques":-8243},{"at":"2026-09-29T13:45:00+00:00","load":47951,"nucleaire":33371,"gaz":505,"eolien":7978,"solaire":12939,"hydraulique":2173,"bioenergies":1101,"charbon":0,"fioul":36,"ech_physiques":-9627},{"at":"2026-09-29T14:45:00+00:00","load":47114,"nucleaire":33919,"gaz":1541,"eolien":7761,"solaire":9717,"hydraulique":2482,"bioenergies":1097,"charbon":0,"fioul":36,"ech_physiques":-8933},{"at":"2026-09-29T15:45:00+00:00","load":46439,"nucleaire":33908,"gaz":2653,"eolien":7760,"solaire":5506,"hydraulique":3189,"bioenergies":1111,"charbon":0,"fioul":36,"ech_physiques":-7724},{"at":"2026-09-29T16:45:00+00:00","load":48162,"nucleaire":34044,"gaz":3504,"eolien":6815,"solaire":1950,"hydraulique":5407,"bioenergies":1109,"charbon":0,"fioul":36,"ech_physiques":-5065},{"at":"2026-09-29T17:45:00+00:00","load":49347,"nucleaire":34027,"gaz":3607,"eolien":6534,"solaire":312,"hydraulique":6079,"bioenergies":1118,"charbon":0,"fioul":36,"ech_physiques":-2527},{"at":"2026-09-29T18:45:00+00:00","load":46140,"nucleaire":34069,"gaz":3618,"eolien":8008,"solaire":200,"hydraulique":4524,"bioenergies":1122,"charbon":0,"fioul":36,"ech_physiques":-5663},{"at":"2026-09-29T19:45:00+00:00","load":43359,"nucleaire":34134,"gaz":2944,"eolien":9795,"solaire":0,"hydraulique":2770,"bioenergies":1121,"charbon":0,"fioul":37,"ech_physiques":-7267},{"at":"2026-09-29T20:45:00+00:00","load":43884,"nucleaire":34130,"gaz":942,"eolien":10796,"solaire":0,"hydraulique":2461,"bioenergies":1118,"charbon":0,"fioul":35,"ech_physiques":-5457},{"at":"2026-09-29T21:45:00+00:00","load":43079,"nucleaire":33904,"gaz":901,"eolien":11494,"solaire":0,"hydraulique":2248,"bioenergies":1120,"charbon":0,"fioul":33,"ech_physiques":-6320},{"at":"2026-09-29T22:45:00+00:00","load":39672,"nucleaire":33686,"gaz":487,"eolien":11636,"solaire":0,"hydraulique":2628,"bioenergies":1117,"charbon":0,"fioul":33,"ech_physiques":-9042},{"at":"2026-09-29T23:45:00+00:00","load":38995,"nucleaire":33854,"gaz":670,"eolien":11857,"solaire":0,"hydraulique":2451,"bioenergies":1121,"charbon":0,"fioul":37,"ech_physiques":-9849},{"at":"2026-09-30T00:45:00+00:00","load":36311,"nucleaire":32031,"gaz":290,"eolien":11502,"solaire":0,"hydraulique":2099,"bioenergies":1126,"charbon":0,"fioul":37,"ech_physiques":-9391},{"at":"2026-09-30T01:00:00+00:00","load":35775,"nucleaire":32299,"gaz":287,"eolien":11541,"solaire":0,"hydraulique":2098,"bioenergies":1119,"charbon":0,"fioul":37,"ech_physiques":-10044}]}
</script>
  <script id="power-price-data" type="application/json">
{"schema":1,"source":"Fraunhofer ISE Energy-Charts","market":"day-ahead auction · France and DE-LU","unit":"EUR/MWh","generated_at":"2026-09-30T01:19:56+00:00","series":{"fr":[{"at":"2026-09-18T22:00:00+00:00","value":144.89},{"at":"2026-09-18T22:15:00+00:00","value":132.57},{"at":"2026-09-18T22:30:00+00:00","value":112.13},{"at":"2026-09-18T22:45:00+00:00","value":81.14},{"at":"2026-09-18T23:00:00+00:00","value":110.55},{"at":"2026-09-18T23:15:00+00:00","value":96.62},{"at":"2026-09-18T23:30:00+00:00","value":94.72},{"at":"2026-09-18T23:45:00+00:00","value":76.14},{"at":"2026-09-19T00:00:00+00:00","value":90.46},{"at":"2026-09-19T00:15:00+00:00","value":79.0},{"at":"2026-09-19T00:30:00+00:00","value":68.56},{"at":"2026-09-19T00:45:00+00:00","value":63.16},{"at":"2026-09-19T01:00:00+00:00","value":60.85},{"at":"2026-09-19T01:15:00+00:00","value":43.73},{"at":"2026-09-19T01:30:00+00:00","value":33.84},{"at":"2026-09-19T01:45:00+00:00","value":28.37},{"at":"2026-09-19T02:00:00+00:00","value":46.01},{"at":"2026-09-19T02:15:00+00:00","value":48.75},{"at":"2026-09-19T02:30:00+00:00","value":45.46},{"at":"2026-09-19T02:45:00+00:00","value":40.76},{"at":"2026-09-19T03:00:00+00:00","value":45.03},{"at":"2026-09-19T03:15:00+00:00","value":44.42},{"at":"2026-09-19T03:30:00+00:00","value":43.69},{"at":"2026-09-19T03:45:00+00:00","value":55.28},{"at":"2026-09-19T04:00:00+00:00","value":51.76},{"at":"2026-09-19T04:15:00+00:00","value":58.11},{"at":"2026-09-19T04:30:00+00:00","value":52.43},{"at":"2026-09-19T04:45:00+00:00","value":56.57},{"at":"2026-09-19T05:00:00+00:00","value":56.08},{"at":"2026-09-19T05:15:00+00:00","value":56.35},{"at":"2026-09-19T05:30:00+00:00","value":57.67},{"at":"2026-09-19T05:45:00+00:00","value":49.21},{"at":"2026-09-19T06:00:00+00:00","value":58.08},{"at":"2026-09-19T06:15:00+00:00","value":38.94},{"at":"2026-09-19T06:30:00+00:00","value":33.77},{"at":"2026-09-19T06:45:00+00:00","value":12.34},{"at":"2026-09-19T07:00:00+00:00","value":29.34},{"at":"2026-09-19T07:15:00+00:00","value":9.32},{"at":"2026-09-19T07:30:00+00:00","value":3.98},{"at":"2026-09-19T07:45:00+00:00","value":0.72},{"at":"2026-09-19T08:00:00+00:00","value":0.51},{"at":"2026-09-19T08:15:00+00:00","value":0.23},{"at":"2026-09-19T08:30:00+00:00","value":0.0},{"at":"2026-09-19T08:45:00+00:00","value":0.0},{"at":"2026-09-19T09:00:00+00:00","value":-0.01},{"at":"2026-09-19T09:15:00+00:00","value":-0.01},{"at":"2026-09-19T09:30:00+00:00","value":-0.01},{"at":"2026-09-19T09:45:00+00:00","value":-0.02},{"at":"2026-09-19T10:00:00+00:00","value":-0.11},{"at":"2026-09-19T10:15:00+00:00","value":-0.11},{"at":"2026-09-19T10:30:00+00:00","value":-0.11},{"at":"2026-09-19T10:45:00+00:00","value":-0.3},{"at":"2026-09-19T11:00:00+00:00","value":-0.7},{"at":"2026-09-19T11:15:00+00:00","value":-0.82},{"at":"2026-09-19T11:30:00+00:00","value":-1.06},{"at":"2026-09-19T11:45:00+00:00","value":-1.29},{"at":"2026-09-19T12:00:00+00:00","value":-1.0},{"at":"2026-09-19T12:15:00+00:00","value":-1.0},{"at":"2026-09-19T12:30:00+00:00","value":-0.91},{"at":"2026-09-19T12:45:00+00:00","value":-0.78},{"at":"2026-09-19T13:00:00+00:00","value":-0.5},{"at":"2026-09-19T13:15:00+00:00","value":-0.19},{"at":"2026-09-19T13:30:00+00:00","value":-0.11},{"at":"2026-09-19T13:45:00+00:00","value":-0.09},{"at":"2026-09-19T14:00:00+00:00","value":-0.1},{"at":"2026-09-19T14:15:00+00:00","value":-0.07},{"at":"2026-09-19T14:30:00+00:00","value":-0.01},{"at":"2026-09-19T14:45:00+00:00","value":-0.01},{"at":"2026-09-19T15:00:00+00:00","value":-0.01},{"at":"2026-09-19T15:15:00+00:00","value":0.0},{"at":"2026-09-19T15:30:00+00:00","value":0.51},{"at":"2026-09-19T15:45:00+00:00","value":2.51},{"at":"2026-09-19T16:00:00+00:00","value":19.17},{"at":"2026-09-19T16:15:00+00:00","value":64.08},{"at":"2026-09-19T16:30:00+00:00","value":94.5},{"at":"2026-09-19T16:45:00+00:00","value":115.03},{"at":"2026-09-19T17:00:00+00:00","value":115.0},{"at":"2026-09-19T17:15:00+00:00","value":136.34},{"at":"2026-09-19T17:30:00+00:00","value":149.32},{"at":"2026-09-19T17:45:00+00:00","value":154.22},{"at":"2026-09-19T18:00:00+00:00","value":147.94},{"at":"2026-09-19T18:15:00+00:00","value":134.32},{"at":"2026-09-19T18:30:00+00:00","value":120.54},{"at":"2026-09-19T18:45:00+00:00","value":110.84},{"at":"2026-09-19T19:00:00+00:00","value":121.37},{"at":"2026-09-19T19:15:00+00:00","value":111.72},{"at":"2026-09-19T19:30:00+00:00","value":107.12},{"at":"2026-09-19T19:45:00+00:00","value":87.06},{"at":"2026-09-19T20:00:00+00:00","value":103.17},{"at":"2026-09-19T20:15:00+00:00","value":102.91},{"at":"2026-09-19T20:30:00+00:00","value":102.44},{"at":"2026-09-19T20:45:00+00:00","value":100.74},{"at":"2026-09-19T21:00:00+00:00","value":103.81},{"at":"2026-09-19T21:15:00+00:00","value":98.49},{"at":"2026-09-19T21:30:00+00:00","value":97.84},{"at":"2026-09-19T21:45:00+00:00","value":89.06},{"at":"2026-09-19T22:00:00+00:00","value":38.91},{"at":"2026-09-19T22:15:00+00:00","value":39.31},{"at":"2026-09-19T22:30:00+00:00","value":36.87},{"at":"2026-09-19T22:45:00+00:00","value":33.78},{"at":"2026-09-19T23:00:00+00:00","value":40.7},{"at":"2026-09-19T23:15:00+00:00","value":35.64},{"at":"2026-09-19T23:30:00+00:00","value":35.19},{"at":"2026-09-19T23:45:00+00:00","value":32.15},{"at":"2026-09-20T00:00:00+00:00","value":30.83},{"at":"2026-09-20T00:15:00+00:00","value":32.73},{"at":"2026-09-20T00:30:00+00:00","value":32.93},{"at":"2026-09-20T00:45:00+00:00","value":28.67},{"at":"2026-09-20T01:00:00+00:00","value":28.29},{"at":"2026-09-20T01:15:00+00:00","value":28.37},{"at":"2026-09-20T01:30:00+00:00","value":27.98},{"at":"2026-09-20T01:45:00+00:00","value":25.51},{"at":"2026-09-20T02:00:00+00:00","value":27.21},{"at":"2026-09-20T02:15:00+00:00","value":24.79},{"at":"2026-09-20T02:30:00+00:00","value":23.69},{"at":"2026-09-20T02:45:00+00:00","value":23.11},{"at":"2026-09-20T03:00:00+00:00","value":27.35},{"at":"2026-09-20T03:15:00+00:00","value":27.48},{"at":"2026-09-20T03:30:00+00:00","value":23.59},{"at":"2026-09-20T03:45:00+00:00","value":24.68},{"at":"2026-09-20T04:00:00+00:00","value":27.51},{"at":"2026-09-20T04:15:00+00:00","value":30.91},{"at":"2026-09-20T04:30:00+00:00","value":31.69},{"at":"2026-09-20T04:45:00+00:00","value":33.31},{"at":"2026-09-20T05:00:00+00:00","value":33.43},{"at":"2026-09-20T05:15:00+00:00","value":32.67},{"at":"2026-09-20T05:30:00+00:00","value":34.73},{"at":"2026-09-20T05:45:00+00:00","value":22.25},{"at":"2026-09-20T06:00:00+00:00","value":40.93},{"at":"2026-09-20T06:15:00+00:00","value":20.4},{"at":"2026-09-20T06:30:00+00:00","value":10.61},{"at":"2026-09-20T06:45:00+00:00","value":5.12},{"at":"2026-09-20T07:00:00+00:00","value":8.98},{"at":"2026-09-20T07:15:00+00:00","value":5.19},{"at":"2026-09-20T07:30:00+00:00","value":1.4},{"at":"2026-09-20T07:45:00+00:00","value":0.01},{"at":"2026-09-20T08:00:00+00:00","value":0.01},{"at":"2026-09-20T08:15:00+00:00","value":0.0},{"at":"2026-09-20T08:30:00+00:00","value":-0.01},{"at":"2026-09-20T08:45:00+00:00","value":-0.03},{"at":"2026-09-20T09:00:00+00:00","value":-0.04},{"at":"2026-09-20T09:15:00+00:00","value":-0.09},{"at":"2026-09-20T09:30:00+00:00","value":-0.11},{"at":"2026-09-20T09:45:00+00:00","value":-0.11},{"at":"2026-09-20T10:00:00+00:00","value":-0.23},{"at":"2026-09-20T10:15:00+00:00","value":-0.23},{"at":"2026-09-20T10:30:00+00:00","value":-0.31},{"at":"2026-09-20T10:45:00+00:00","value":-0.81},{"at":"2026-09-20T11:00:00+00:00","value":-1.0},{"at":"2026-09-20T11:15:00+00:00","value":-1.06},{"at":"2026-09-20T11:30:00+00:00","value":-1.14},{"at":"2026-09-20T11:45:00+00:00","value":-1.11},{"at":"2026-09-20T12:00:00+00:00","value":-1.0},{"at":"2026-09-20T12:15:00+00:00","value":-1.0},{"at":"2026-09-20T12:30:00+00:00","value":-1.0},{"at":"2026-09-20T12:45:00+00:00","value":-1.0},{"at":"2026-09-20T13:00:00+00:00","value":-1.0},{"at":"2026-09-20T13:15:00+00:00","value":-0.82},{"at":"2026-09-20T13:30:00+00:00","value":-0.8},{"at":"2026-09-20T13:45:00+00:00","value":-0.78},{"at":"2026-09-20T14:00:00+00:00","value":-0.01},{"at":"2026-09-20T14:15:00+00:00","value":-0.01},{"at":"2026-09-20T14:30:00+00:00","value":0.0},{"at":"2026-09-20T14:45:00+00:00","value":0.0},{"at":"2026-09-20T15:00:00+00:00","value":7.0},{"at":"2026-09-20T15:15:00+00:00","value":18.8},{"at":"2026-09-20T15:30:00+00:00","value":42.01},{"at":"2026-09-20T15:45:00+00:00","value":72.19},{"at":"2026-09-20T16:00:00+00:00","value":70.23},{"at":"2026-09-20T16:15:00+00:00","value":114.46},{"at":"2026-09-20T16:30:00+00:00","value":148.34},{"at":"2026-09-20T16:45:00+00:00","value":237.8},{"at":"2026-09-20T17:00:00+00:00","value":162.96},{"at":"2026-09-20T17:15:00+00:00","value":230.0},{"at":"2026-09-20T17:30:00+00:00","value":200.74},{"at":"2026-09-20T17:45:00+00:00","value":225.57},{"at":"2026-09-20T18:00:00+00:00","value":198.9},{"at":"2026-09-20T18:15:00+00:00","value":200.74},{"at":"2026-09-20T18:30:00+00:00","value":205.71},{"at":"2026-09-20T18:45:00+00:00","value":200.74},{"at":"2026-09-20T19:00:00+00:00","value":211.13},{"at":"2026-09-20T19:15:00+00:00","value":200.99},{"at":"2026-09-20T19:30:00+00:00","value":191.42},{"at":"2026-09-20T19:45:00+00:00","value":192.36},{"at":"2026-09-20T20:00:00+00:00","value":200.74},{"at":"2026-09-20T20:15:00+00:00","value":189.94},{"at":"2026-09-20T20:30:00+00:00","value":195.87},{"at":"2026-09-20T20:45:00+00:00","value":186.76},{"at":"2026-09-20T21:00:00+00:00","value":180.56},{"at":"2026-09-20T21:15:00+00:00","value":186.76},{"at":"2026-09-20T21:30:00+00:00","value":186.18},{"at":"2026-09-20T21:45:00+00:00","value":166.5},{"at":"2026-09-20T22:00:00+00:00","value":200.76},{"at":"2026-09-20T22:15:00+00:00","value":190.0},{"at":"2026-09-20T22:30:00+00:00","value":165.94},{"at":"2026-09-20T22:45:00+00:00","value":145.17},{"at":"2026-09-20T23:00:00+00:00","value":169.93},{"at":"2026-09-20T23:15:00+00:00","value":148.45},{"at":"2026-09-20T23:30:00+00:00","value":153.27},{"at":"2026-09-20T23:45:00+00:00","value":136.33},{"at":"2026-09-21T00:00:00+00:00","value":150.9},{"at":"2026-09-21T00:15:00+00:00","value":135.56},{"at":"2026-09-21T00:30:00+00:00","value":130.4},{"at":"2026-09-21T00:45:00+00:00","value":139.13},{"at":"2026-09-21T01:00:00+00:00","value":139.24},{"at":"2026-09-21T01:15:00+00:00","value":143.39},{"at":"2026-09-21T01:30:00+00:00","value":136.01},{"at":"2026-09-21T01:45:00+00:00","value":120.87},{"at":"2026-09-21T02:00:00+00:00","value":131.59},{"at":"2026-09-21T02:15:00+00:00","value":134.24},{"at":"2026-09-21T02:30:00+00:00","value":137.99},{"at":"2026-09-21T02:45:00+00:00","value":129.67},{"at":"2026-09-21T03:00:00+00:00","value":124.48},{"at":"2026-09-21T03:15:00+00:00","value":149.01},{"at":"2026-09-21T03:30:00+00:00","value":141.87},{"at":"2026-09-21T03:45:00+00:00","value":158.0},{"at":"2026-09-21T04:00:00+00:00","value":163.14},{"at":"2026-09-21T04:15:00+00:00","value":186.53},{"at":"2026-09-21T04:30:00+00:00","value":182.99},{"at":"2026-09-21T04:45:00+00:00","value":187.69},{"at":"2026-09-21T05:00:00+00:00","value":211.7},{"at":"2026-09-21T05:15:00+00:00","value":224.0},{"at":"2026-09-21T05:30:00+00:00","value":227.0},{"at":"2026-09-21T05:45:00+00:00","value":230.57},{"at":"2026-09-21T06:00:00+00:00","value":263.9},{"at":"2026-09-21T06:15:00+00:00","value":246.23},{"at":"2026-09-21T06:30:00+00:00","value":226.0},{"at":"2026-09-21T06:45:00+00:00","value":195.0},{"at":"2026-09-21T07:00:00+00:00","value":212.25},{"at":"2026-09-21T07:15:00+00:00","value":186.25},{"at":"2026-09-21T07:30:00+00:00","value":167.52},{"at":"2026-09-21T07:45:00+00:00","value":110.77},{"at":"2026-09-21T08:00:00+00:00","value":131.12},{"at":"2026-09-21T08:15:00+00:00","value":91.6},{"at":"2026-09-21T08:30:00+00:00","value":83.6},{"at":"2026-09-21T08:45:00+00:00","value":48.5},{"at":"2026-09-21T09:00:00+00:00","value":55.68},{"at":"2026-09-21T09:15:00+00:00","value":46.38},{"at":"2026-09-21T09:30:00+00:00","value":35.94},{"at":"2026-09-21T09:45:00+00:00","value":33.22},{"at":"2026-09-21T10:00:00+00:00","value":32.17},{"at":"2026-09-21T10:15:00+00:00","value":28.15},{"at":"2026-09-21T10:30:00+00:00","value":28.0},{"at":"2026-09-21T10:45:00+00:00","value":23.34},{"at":"2026-09-21T11:00:00+00:00","value":23.47},{"at":"2026-09-21T11:15:00+00:00","value":20.17},{"at":"2026-09-21T11:30:00+00:00","value":16.75},{"at":"2026-09-21T11:45:00+00:00","value":16.38},{"at":"2026-09-21T12:00:00+00:00","value":20.02},{"at":"2026-09-21T12:15:00+00:00","value":22.08},{"at":"2026-09-21T12:30:00+00:00","value":22.54},{"at":"2026-09-21T12:45:00+00:00","value":26.11},{"at":"2026-09-21T13:00:00+00:00","value":25.67},{"at":"2026-09-21T13:15:00+00:00","value":31.3},{"at":"2026-09-21T13:30:00+00:00","value":20.24},{"at":"2026-09-21T13:45:00+00:00","value":17.24},{"at":"2026-09-21T14:00:00+00:00","value":37.19},{"at":"2026-09-21T14:15:00+00:00","value":76.19},{"at":"2026-09-21T14:30:00+00:00","value":54.27},{"at":"2026-09-21T14:45:00+00:00","value":52.38},{"at":"2026-09-21T15:00:00+00:00","value":75.23},{"at":"2026-09-21T15:15:00+00:00","value":111.75},{"at":"2026-09-21T15:30:00+00:00","value":163.93},{"at":"2026-09-21T15:45:00+00:00","value":208.84},{"at":"2026-09-21T16:00:00+00:00","value":174.12},{"at":"2026-09-21T16:15:00+00:00","value":202.94},{"at":"2026-09-21T16:30:00+00:00","value":224.23},{"at":"2026-09-21T16:45:00+00:00","value":261.77},{"at":"2026-09-21T17:00:00+00:00","value":221.71},{"at":"2026-09-21T17:15:00+00:00","value":224.92},{"at":"2026-09-21T17:30:00+00:00","value":251.9},{"at":"2026-09-21T17:45:00+00:00","value":276.54},{"at":"2026-09-21T18:00:00+00:00","value":251.3},{"at":"2026-09-21T18:15:00+00:00","value":250.28},{"at":"2026-09-21T18:30:00+00:00","value":243.48},{"at":"2026-09-21T18:45:00+00:00","value":219.04},{"at":"2026-09-21T19:00:00+00:00","value":232.7},{"at":"2026-09-21T19:15:00+00:00","value":219.22},{"at":"2026-09-21T19:30:00+00:00","value":215.05},{"at":"2026-09-21T19:45:00+00:00","value":207.8},{"at":"2026-09-21T20:00:00+00:00","value":216.63},{"at":"2026-09-21T20:15:00+00:00","value":205.54},{"at":"2026-09-21T20:30:00+00:00","value":206.93},{"at":"2026-09-21T20:45:00+00:00","value":197.26},{"at":"2026-09-21T21:00:00+00:00","value":199.01},{"at":"2026-09-21T21:15:00+00:00","value":185.42},{"at":"2026-09-21T21:30:00+00:00","value":187.25},{"at":"2026-09-21T21:45:00+00:00","value":172.4},{"at":"2026-09-21T22:00:00+00:00","value":191.21},{"at":"2026-09-21T22:15:00+00:00","value":184.04},{"at":"2026-09-21T22:30:00+00:00","value":177.73},{"at":"2026-09-21T22:45:00+00:00","value":176.79},{"at":"2026-09-21T23:00:00+00:00","value":178.2},{"at":"2026-09-21T23:15:00+00:00","value":175.61},{"at":"2026-09-21T23:30:00+00:00","value":177.48},{"at":"2026-09-21T23:45:00+00:00","value":176.66},{"at":"2026-09-22T00:00:00+00:00","value":176.87},{"at":"2026-09-22T00:15:00+00:00","value":175.45},{"at":"2026-09-22T00:30:00+00:00","value":173.57},{"at":"2026-09-22T00:45:00+00:00","value":172.68},{"at":"2026-09-22T01:00:00+00:00","value":174.62},{"at":"2026-09-22T01:15:00+00:00","value":171.86},{"at":"2026-09-22T01:30:00+00:00","value":171.27},{"at":"2026-09-22T01:45:00+00:00","value":172.25},{"at":"2026-09-22T02:00:00+00:00","value":175.15},{"at":"2026-09-22T02:15:00+00:00","value":174.73},{"at":"2026-09-22T02:30:00+00:00","value":176.45},{"at":"2026-09-22T02:45:00+00:00","value":181.0},{"at":"2026-09-22T03:00:00+00:00","value":170.03},{"at":"2026-09-22T03:15:00+00:00","value":181.47},{"at":"2026-09-22T03:30:00+00:00","value":192.99},{"at":"2026-09-22T03:45:00+00:00","value":185.53},{"at":"2026-09-22T04:00:00+00:00","value":199.28},{"at":"2026-09-22T04:15:00+00:00","value":201.5},{"at":"2026-09-22T04:30:00+00:00","value":202.1},{"at":"2026-09-22T04:45:00+00:00","value":210.0},{"at":"2026-09-22T05:00:00+00:00","value":226.0},{"at":"2026-09-22T05:15:00+00:00","value":228.72},{"at":"2026-09-22T05:30:00+00:00","value":237.23},{"at":"2026-09-22T05:45:00+00:00","value":244.71},{"at":"2026-09-22T06:00:00+00:00","value":282.29},{"at":"2026-09-22T06:15:00+00:00","value":268.06},{"at":"2026-09-22T06:30:00+00:00","value":240.76},{"at":"2026-09-22T06:45:00+00:00","value":204.98},{"at":"2026-09-22T07:00:00+00:00","value":215.0},{"at":"2026-09-22T07:15:00+00:00","value":193.91},{"at":"2026-09-22T07:30:00+00:00","value":186.93},{"at":"2026-09-22T07:45:00+00:00","value":166.18},{"at":"2026-09-22T08:00:00+00:00","value":163.0},{"at":"2026-09-22T08:15:00+00:00","value":120.5},{"at":"2026-09-22T08:30:00+00:00","value":95.06},{"at":"2026-09-22T08:45:00+00:00","value":40.0},{"at":"2026-09-22T09:00:00+00:00","value":52.0},{"at":"2026-09-22T09:15:00+00:00","value":38.99},{"at":"2026-09-22T09:30:00+00:00","value":38.66},{"at":"2026-09-22T09:45:00+00:00","value":27.0},{"at":"2026-09-22T10:00:00+00:00","value":20.01},{"at":"2026-09-22T10:15:00+00:00","value":19.64},{"at":"2026-09-22T10:30:00+00:00","value":12.96},{"at":"2026-09-22T10:45:00+00:00","value":10.01},{"at":"2026-09-22T11:00:00+00:00","value":4.61},{"at":"2026-09-22T11:15:00+00:00","value":3.43},{"at":"2026-09-22T11:30:00+00:00","value":1.99},{"at":"2026-09-22T11:45:00+00:00","value":2.0},{"at":"2026-09-22T12:00:00+00:00","value":6.07},{"at":"2026-09-22T12:15:00+00:00","value":15.1},{"at":"2026-09-22T12:30:00+00:00","value":20.17},{"at":"2026-09-22T12:45:00+00:00","value":24.11},{"at":"2026-09-22T13:00:00+00:00","value":25.0},{"at":"2026-09-22T13:15:00+00:00","value":24.01},{"at":"2026-09-22T13:30:00+00:00","value":22.14},{"at":"2026-09-22T13:45:00+00:00","value":24.01},{"at":"2026-09-22T14:00:00+00:00","value":32.5},{"at":"2026-09-22T14:15:00+00:00","value":39.09},{"at":"2026-09-22T14:30:00+00:00","value":54.41},{"at":"2026-09-22T14:45:00+00:00","value":70.0},{"at":"2026-09-22T15:00:00+00:00","value":92.55},{"at":"2026-09-22T15:15:00+00:00","value":107.32},{"at":"2026-09-22T15:30:00+00:00","value":156.64},{"at":"2026-09-22T15:45:00+00:00","value":169.11},{"at":"2026-09-22T16:00:00+00:00","value":207.24},{"at":"2026-09-22T16:15:00+00:00","value":218.14},{"at":"2026-09-22T16:30:00+00:00","value":244.63},{"at":"2026-09-22T16:45:00+00:00","value":268.06},{"at":"2026-09-22T17:00:00+00:00","value":250.0},{"at":"2026-09-22T17:15:00+00:00","value":268.06},{"at":"2026-09-22T17:30:00+00:00","value":287.94},{"at":"2026-09-22T17:45:00+00:00","value":300.0},{"at":"2026-09-22T18:00:00+00:00","value":285.0},{"at":"2026-09-22T18:15:00+00:00","value":290.01},{"at":"2026-09-22T18:30:00+00:00","value":278.18},{"at":"2026-09-22T18:45:00+00:00","value":276.51},{"at":"2026-09-22T19:00:00+00:00","value":272.51},{"at":"2026-09-22T19:15:00+00:00","value":251.44},{"at":"2026-09-22T19:30:00+00:00","value":255.83},{"at":"2026-09-22T19:45:00+00:00","value":227.5},{"at":"2026-09-22T20:00:00+00:00","value":253.01},{"at":"2026-09-22T20:15:00+00:00","value":231.8},{"at":"2026-09-22T20:30:00+00:00","value":232.19},{"at":"2026-09-22T20:45:00+00:00","value":224.41},{"at":"2026-09-22T21:00:00+00:00","value":224.0},{"at":"2026-09-22T21:15:00+00:00","value":214.54},{"at":"2026-09-22T21:30:00+00:00","value":210.21},{"at":"2026-09-22T21:45:00+00:00","value":201.18},{"at":"2026-09-22T22:00:00+00:00","value":194.55},{"at":"2026-09-22T22:15:00+00:00","value":188.51},{"at":"2026-09-22T22:30:00+00:00","value":186.39},{"at":"2026-09-22T22:45:00+00:00","value":166.66},{"at":"2026-09-22T23:00:00+00:00","value":175.28},{"at":"2026-09-22T23:15:00+00:00","value":174.88},{"at":"2026-09-22T23:30:00+00:00","value":173.68},{"at":"2026-09-22T23:45:00+00:00","value":179.76},{"at":"2026-09-23T00:00:00+00:00","value":174.52},{"at":"2026-09-23T00:15:00+00:00","value":171.1},{"at":"2026-09-23T00:30:00+00:00","value":164.07},{"at":"2026-09-23T00:45:00+00:00","value":161.89},{"at":"2026-09-23T01:00:00+00:00","value":152.23},{"at":"2026-09-23T01:15:00+00:00","value":156.85},{"at":"2026-09-23T01:30:00+00:00","value":155.77},{"at":"2026-09-23T01:45:00+00:00","value":160.27},{"at":"2026-09-23T02:00:00+00:00","value":151.49},{"at":"2026-09-23T02:15:00+00:00","value":155.69},{"at":"2026-09-23T02:30:00+00:00","value":157.22},{"at":"2026-09-23T02:45:00+00:00","value":161.57},{"at":"2026-09-23T03:00:00+00:00","value":161.23},{"at":"2026-09-23T03:15:00+00:00","value":167.04},{"at":"2026-09-23T03:30:00+00:00","value":175.01},{"at":"2026-09-23T03:45:00+00:00","value":157.83},{"at":"2026-09-23T04:00:00+00:00","value":179.66},{"at":"2026-09-23T04:15:00+00:00","value":205.12},{"at":"2026-09-23T04:30:00+00:00","value":170.94},{"at":"2026-09-23T04:45:00+00:00","value":197.13},{"at":"2026-09-23T05:00:00+00:00","value":206.5},{"at":"2026-09-23T05:15:00+00:00","value":219.88},{"at":"2026-09-23T05:30:00+00:00","value":225.0},{"at":"2026-09-23T05:45:00+00:00","value":226.9},{"at":"2026-09-23T06:00:00+00:00","value":257.65},{"at":"2026-09-23T06:15:00+00:00","value":240.5},{"at":"2026-09-23T06:30:00+00:00","value":224.31},{"at":"2026-09-23T06:45:00+00:00","value":189.12},{"at":"2026-09-23T07:00:00+00:00","value":207.12},{"at":"2026-09-23T07:15:00+00:00","value":193.88},{"at":"2026-09-23T07:30:00+00:00","value":170.82},{"at":"2026-09-23T07:45:00+00:00","value":146.46},{"at":"2026-09-23T08:00:00+00:00","value":166.24},{"at":"2026-09-23T08:15:00+00:00","value":148.1},{"at":"2026-09-23T08:30:00+00:00","value":134.95},{"at":"2026-09-23T08:45:00+00:00","value":93.3},{"at":"2026-09-23T09:00:00+00:00","value":90.0},{"at":"2026-09-23T09:15:00+00:00","value":73.59},{"at":"2026-09-23T09:30:00+00:00","value":57.59},{"at":"2026-09-23T09:45:00+00:00","value":38.99},{"at":"2026-09-23T10:00:00+00:00","value":40.0},{"at":"2026-09-23T10:15:00+00:00","value":35.0},{"at":"2026-09-23T10:30:00+00:00","value":35.0},{"at":"2026-09-23T10:45:00+00:00","value":30.0},{"at":"2026-09-23T11:00:00+00:00","value":24.01},{"at":"2026-09-23T11:15:00+00:00","value":15.0},{"at":"2026-09-23T11:30:00+00:00","value":11.1},{"at":"2026-09-23T11:45:00+00:00","value":10.02},{"at":"2026-09-23T12:00:00+00:00","value":24.01},{"at":"2026-09-23T12:15:00+00:00","value":23.38},{"at":"2026-09-23T12:30:00+00:00","value":25.58},{"at":"2026-09-23T12:45:00+00:00","value":27.23},{"at":"2026-09-23T13:00:00+00:00","value":25.71},{"at":"2026-09-23T13:15:00+00:00","value":28.28},{"at":"2026-09-23T13:30:00+00:00","value":34.08},{"at":"2026-09-23T13:45:00+00:00","value":38.77},{"at":"2026-09-23T14:00:00+00:00","value":38.77},{"at":"2026-09-23T14:15:00+00:00","value":51.51},{"at":"2026-09-23T14:30:00+00:00","value":74.0},{"at":"2026-09-23T14:45:00+00:00","value":107.72},{"at":"2026-09-23T15:00:00+00:00","value":114.94},{"at":"2026-09-23T15:15:00+00:00","value":111.65},{"at":"2026-09-23T15:30:00+00:00","value":141.64},{"at":"2026-09-23T15:45:00+00:00","value":152.38},{"at":"2026-09-23T16:00:00+00:00","value":175.05},{"at":"2026-09-23T16:15:00+00:00","value":187.45},{"at":"2026-09-23T16:30:00+00:00","value":191.65},{"at":"2026-09-23T16:45:00+00:00","value":230.21},{"at":"2026-09-23T17:00:00+00:00","value":240.5},{"at":"2026-09-23T17:15:00+00:00","value":255.32},{"at":"2026-09-23T17:30:00+00:00","value":264.47},{"at":"2026-09-23T17:45:00+00:00","value":274.36},{"at":"2026-09-23T18:00:00+00:00","value":266.17},{"at":"2026-09-23T18:15:00+00:00","value":252.97},{"at":"2026-09-23T18:30:00+00:00","value":237.18},{"at":"2026-09-23T18:45:00+00:00","value":212.96},{"at":"2026-09-23T19:00:00+00:00","value":219.26},{"at":"2026-09-23T19:15:00+00:00","value":210.39},{"at":"2026-09-23T19:30:00+00:00","value":196.79},{"at":"2026-09-23T19:45:00+00:00","value":184.9},{"at":"2026-09-23T20:00:00+00:00","value":189.38},{"at":"2026-09-23T20:15:00+00:00","value":181.48},{"at":"2026-09-23T20:30:00+00:00","value":179.9},{"at":"2026-09-23T20:45:00+00:00","value":172.87},{"at":"2026-09-23T21:00:00+00:00","value":176.08},{"at":"2026-09-23T21:15:00+00:00","value":164.18},{"at":"2026-09-23T21:30:00+00:00","value":166.93},{"at":"2026-09-23T21:45:00+00:00","value":161.77},{"at":"2026-09-23T22:00:00+00:00","value":194.36},{"at":"2026-09-23T22:15:00+00:00","value":177.51},{"at":"2026-09-23T22:30:00+00:00","value":173.33},{"at":"2026-09-23T22:45:00+00:00","value":179.6},{"at":"2026-09-23T23:00:00+00:00","value":186.71},{"at":"2026-09-23T23:15:00+00:00","value":177.91},{"at":"2026-09-23T23:30:00+00:00","value":180.46},{"at":"2026-09-23T23:45:00+00:00","value":160.68},{"at":"2026-09-24T00:00:00+00:00","value":156.42},{"at":"2026-09-24T00:15:00+00:00","value":147.84},{"at":"2026-09-24T00:30:00+00:00","value":142.51},{"at":"2026-09-24T00:45:00+00:00","value":134.99},{"at":"2026-09-24T01:00:00+00:00","value":141.93},{"at":"2026-09-24T01:15:00+00:00","value":135.29},{"at":"2026-09-24T01:30:00+00:00","value":141.99},{"at":"2026-09-24T01:45:00+00:00","value":136.17},{"at":"2026-09-24T02:00:00+00:00","value":147.26},{"at":"2026-09-24T02:15:00+00:00","value":147.99},{"at":"2026-09-24T02:30:00+00:00","value":149.37},{"at":"2026-09-24T02:45:00+00:00","value":158.24},{"at":"2026-09-24T03:00:00+00:00","value":174.82},{"at":"2026-09-24T03:15:00+00:00","value":149.98},{"at":"2026-09-24T03:30:00+00:00","value":153.0},{"at":"2026-09-24T03:45:00+00:00","value":169.69},{"at":"2026-09-24T04:00:00+00:00","value":164.62},{"at":"2026-09-24T04:15:00+00:00","value":179.25},{"at":"2026-09-24T04:30:00+00:00","value":196.3},{"at":"2026-09-24T04:45:00+00:00","value":200.0},{"at":"2026-09-24T05:00:00+00:00","value":200.0},{"at":"2026-09-24T05:15:00+00:00","value":210.0},{"at":"2026-09-24T05:30:00+00:00","value":215.37},{"at":"2026-09-24T05:45:00+00:00","value":220.42},{"at":"2026-09-24T06:00:00+00:00","value":250.0},{"at":"2026-09-24T06:15:00+00:00","value":238.03},{"at":"2026-09-24T06:30:00+00:00","value":214.97},{"at":"2026-09-24T06:45:00+00:00","value":195.98},{"at":"2026-09-24T07:00:00+00:00","value":221.84},{"at":"2026-09-24T07:15:00+00:00","value":194.99},{"at":"2026-09-24T07:30:00+00:00","value":174.0},{"at":"2026-09-24T07:45:00+00:00","value":161.75},{"at":"2026-09-24T08:00:00+00:00","value":165.1},{"at":"2026-09-24T08:15:00+00:00","value":167.14},{"at":"2026-09-24T08:30:00+00:00","value":147.56},{"at":"2026-09-24T08:45:00+00:00","value":116.36},{"at":"2026-09-24T09:00:00+00:00","value":126.36},{"at":"2026-09-24T09:15:00+00:00","value":78.86},{"at":"2026-09-24T09:30:00+00:00","value":60.02},{"at":"2026-09-24T09:45:00+00:00","value":53.68},{"at":"2026-09-24T10:00:00+00:00","value":50.1},{"at":"2026-09-24T10:15:00+00:00","value":38.55},{"at":"2026-09-24T10:30:00+00:00","value":35.48},{"at":"2026-09-24T10:45:00+00:00","value":38.55},{"at":"2026-09-24T11:00:00+00:00","value":27.0},{"at":"2026-09-24T11:15:00+00:00","value":23.5},{"at":"2026-09-24T11:30:00+00:00","value":17.62},{"at":"2026-09-24T11:45:00+00:00","value":20.0},{"at":"2026-09-24T12:00:00+00:00","value":30.0},{"at":"2026-09-24T12:15:00+00:00","value":34.99},{"at":"2026-09-24T12:30:00+00:00","value":38.66},{"at":"2026-09-24T12:45:00+00:00","value":38.55},{"at":"2026-09-24T13:00:00+00:00","value":38.66},{"at":"2026-09-24T13:15:00+00:00","value":38.77},{"at":"2026-09-24T13:30:00+00:00","value":38.99},{"at":"2026-09-24T13:45:00+00:00","value":73.61},{"at":"2026-09-24T14:00:00+00:00","value":74.07},{"at":"2026-09-24T14:15:00+00:00","value":95.13},{"at":"2026-09-24T14:30:00+00:00","value":118.13},{"at":"2026-09-24T14:45:00+00:00","value":152.8},{"at":"2026-09-24T15:00:00+00:00","value":141.6},{"at":"2026-09-24T15:15:00+00:00","value":170.89},{"at":"2026-09-24T15:30:00+00:00","value":171.17},{"at":"2026-09-24T15:45:00+00:00","value":214.43},{"at":"2026-09-24T16:00:00+00:00","value":169.37},{"at":"2026-09-24T16:15:00+00:00","value":218.93},{"at":"2026-09-24T16:30:00+00:00","value":233.27},{"at":"2026-09-24T16:45:00+00:00","value":261.0},{"at":"2026-09-24T17:00:00+00:00","value":251.4},{"at":"2026-09-24T17:15:00+00:00","value":265.8},{"at":"2026-09-24T17:30:00+00:00","value":267.94},{"at":"2026-09-24T17:45:00+00:00","value":288.23},{"at":"2026-09-24T18:00:00+00:00","value":272.65},{"at":"2026-09-24T18:15:00+00:00","value":265.8},{"at":"2026-09-24T18:30:00+00:00","value":253.5},{"at":"2026-09-24T18:45:00+00:00","value":248.05},{"at":"2026-09-24T19:00:00+00:00","value":240.29},{"at":"2026-09-24T19:15:00+00:00","value":230.9},{"at":"2026-09-24T19:30:00+00:00","value":224.17},{"at":"2026-09-24T19:45:00+00:00","value":210.4},{"at":"2026-09-24T20:00:00+00:00","value":222.09},{"at":"2026-09-24T20:15:00+00:00","value":205.95},{"at":"2026-09-24T20:30:00+00:00","value":202.67},{"at":"2026-09-24T20:45:00+00:00","value":194.87},{"at":"2026-09-24T21:00:00+00:00","value":198.86},{"at":"2026-09-24T21:15:00+00:00","value":190.36},{"at":"2026-09-24T21:30:00+00:00","value":187.58},{"at":"2026-09-24T21:45:00+00:00","value":182.5},{"at":"2026-09-24T22:00:00+00:00","value":197.12},{"at":"2026-09-24T22:15:00+00:00","value":184.82},{"at":"2026-09-24T22:30:00+00:00","value":176.3},{"at":"2026-09-24T22:45:00+00:00","value":170.83},{"at":"2026-09-24T23:00:00+00:00","value":175.34},{"at":"2026-09-24T23:15:00+00:00","value":171.96},{"at":"2026-09-24T23:30:00+00:00","value":171.6},{"at":"2026-09-24T23:45:00+00:00","value":170.96},{"at":"2026-09-25T00:00:00+00:00","value":168.83},{"at":"2026-09-25T00:15:00+00:00","value":167.62},{"at":"2026-09-25T00:30:00+00:00","value":166.96},{"at":"2026-09-25T00:45:00+00:00","value":162.32},{"at":"2026-09-25T01:00:00+00:00","value":165.48},{"at":"2026-09-25T01:15:00+00:00","value":163.57},{"at":"2026-09-25T01:30:00+00:00","value":163.99},{"at":"2026-09-25T01:45:00+00:00","value":169.14},{"at":"2026-09-25T02:00:00+00:00","value":158.58},{"at":"2026-09-25T02:15:00+00:00","value":155.25},{"at":"2026-09-25T02:30:00+00:00","value":157.09},{"at":"2026-09-25T02:45:00+00:00","value":164.94},{"at":"2026-09-25T03:00:00+00:00","value":167.4},{"at":"2026-09-25T03:15:00+00:00","value":169.26},{"at":"2026-09-25T03:30:00+00:00","value":187.11},{"at":"2026-09-25T03:45:00+00:00","value":177.6},{"at":"2026-09-25T04:00:00+00:00","value":196.18},{"at":"2026-09-25T04:15:00+00:00","value":197.12},{"at":"2026-09-25T04:30:00+00:00","value":199.56},{"at":"2026-09-25T04:45:00+00:00","value":210.94},{"at":"2026-09-25T05:00:00+00:00","value":219.93},{"at":"2026-09-25T05:15:00+00:00","value":237.02},{"at":"2026-09-25T05:30:00+00:00","value":243.97},{"at":"2026-09-25T05:45:00+00:00","value":246.06},{"at":"2026-09-25T06:00:00+00:00","value":261.99},{"at":"2026-09-25T06:15:00+00:00","value":251.3},{"at":"2026-09-25T06:30:00+00:00","value":235.0},{"at":"2026-09-25T06:45:00+00:00","value":200.0},{"at":"2026-09-25T07:00:00+00:00","value":201.18},{"at":"2026-09-25T07:15:00+00:00","value":199.3},{"at":"2026-09-25T07:30:00+00:00","value":189.27},{"at":"2026-09-25T07:45:00+00:00","value":157.5},{"at":"2026-09-25T08:00:00+00:00","value":163.0},{"at":"2026-09-25T08:15:00+00:00","value":148.0},{"at":"2026-09-25T08:30:00+00:00","value":140.99},{"at":"2026-09-25T08:45:00+00:00","value":100.01},{"at":"2026-09-25T09:00:00+00:00","value":97.06},{"at":"2026-09-25T09:15:00+00:00","value":85.2},{"at":"2026-09-25T09:30:00+00:00","value":72.89},{"at":"2026-09-25T09:45:00+00:00","value":55.88},{"at":"2026-09-25T10:00:00+00:00","value":52.88},{"at":"2026-09-25T10:15:00+00:00","value":38.99},{"at":"2026-09-25T10:30:00+00:00","value":47.76},{"at":"2026-09-25T10:45:00+00:00","value":42.75},{"at":"2026-09-25T11:00:00+00:00","value":38.99},{"at":"2026-09-25T11:15:00+00:00","value":36.12},{"at":"2026-09-25T11:30:00+00:00","value":26.14},{"at":"2026-09-25T11:45:00+00:00","value":19.17},{"at":"2026-09-25T12:00:00+00:00","value":23.12},{"at":"2026-09-25T12:15:00+00:00","value":35.0},{"at":"2026-09-25T12:30:00+00:00","value":38.99},{"at":"2026-09-25T12:45:00+00:00","value":39.1},{"at":"2026-09-25T13:00:00+00:00","value":39.1},{"at":"2026-09-25T13:15:00+00:00","value":39.1},{"at":"2026-09-25T13:30:00+00:00","value":38.66},{"at":"2026-09-25T13:45:00+00:00","value":44.01},{"at":"2026-09-25T14:00:00+00:00","value":65.0},{"at":"2026-09-25T14:15:00+00:00","value":69.0},{"at":"2026-09-25T14:30:00+00:00","value":74.61},{"at":"2026-09-25T14:45:00+00:00","value":106.82},{"at":"2026-09-25T15:00:00+00:00","value":142.48},{"at":"2026-09-25T15:15:00+00:00","value":171.9},{"at":"2026-09-25T15:30:00+00:00","value":178.75},{"at":"2026-09-25T15:45:00+00:00","value":204.01},{"at":"2026-09-25T16:00:00+00:00","value":202.24},{"at":"2026-09-25T16:15:00+00:00","value":229.77},{"at":"2026-09-25T16:30:00+00:00","value":239.54},{"at":"2026-09-25T16:45:00+00:00","value":272.29},{"at":"2026-09-25T17:00:00+00:00","value":242.5},{"at":"2026-09-25T17:15:00+00:00","value":248.58},{"at":"2026-09-25T17:30:00+00:00","value":255.1},{"at":"2026-09-25T17:45:00+00:00","value":287.13},{"at":"2026-09-25T18:00:00+00:00","value":270.0},{"at":"2026-09-25T18:15:00+00:00","value":255.0},{"at":"2026-09-25T18:30:00+00:00","value":247.73},{"at":"2026-09-25T18:45:00+00:00","value":237.51},{"at":"2026-09-25T19:00:00+00:00","value":244.81},{"at":"2026-09-25T19:15:00+00:00","value":232.14},{"at":"2026-09-25T19:30:00+00:00","value":219.97},{"at":"2026-09-25T19:45:00+00:00","value":204.46},{"at":"2026-09-25T20:00:00+00:00","value":220.92},{"at":"2026-09-25T20:15:00+00:00","value":210.0},{"at":"2026-09-25T20:30:00+00:00","value":203.67},{"at":"2026-09-25T20:45:00+00:00","value":196.65},{"at":"2026-09-25T21:00:00+00:00","value":201.18},{"at":"2026-09-25T21:15:00+00:00","value":198.5},{"at":"2026-09-25T21:30:00+00:00","value":194.86},{"at":"2026-09-25T21:45:00+00:00","value":185.3},{"at":"2026-09-25T22:00:00+00:00","value":207.72},{"at":"2026-09-25T22:15:00+00:00","value":201.51},{"at":"2026-09-25T22:30:00+00:00","value":194.81},{"at":"2026-09-25T22:45:00+00:00","value":186.47},{"at":"2026-09-25T23:00:00+00:00","value":189.42},{"at":"2026-09-25T23:15:00+00:00","value":185.76},{"at":"2026-09-25T23:30:00+00:00","value":184.41},{"at":"2026-09-25T23:45:00+00:00","value":182.59},{"at":"2026-09-26T00:00:00+00:00","value":183.13},{"at":"2026-09-26T00:15:00+00:00","value":181.63},{"at":"2026-09-26T00:30:00+00:00","value":176.13},{"at":"2026-09-26T00:45:00+00:00","value":169.87},{"at":"2026-09-26T01:00:00+00:00","value":169.43},{"at":"2026-09-26T01:15:00+00:00","value":166.35},{"at":"2026-09-26T01:30:00+00:00","value":165.51},{"at":"2026-09-26T01:45:00+00:00","value":165.12},{"at":"2026-09-26T02:00:00+00:00","value":163.01},{"at":"2026-09-26T02:15:00+00:00","value":163.56},{"at":"2026-09-26T02:30:00+00:00","value":163.56},{"at":"2026-09-26T02:45:00+00:00","value":164.07},{"at":"2026-09-26T03:00:00+00:00","value":161.62},{"at":"2026-09-26T03:15:00+00:00","value":161.59},{"at":"2026-09-26T03:30:00+00:00","value":163.54},{"at":"2026-09-26T03:45:00+00:00","value":168.06},{"at":"2026-09-26T04:00:00+00:00","value":170.16},{"at":"2026-09-26T04:15:00+00:00","value":178.75},{"at":"2026-09-26T04:30:00+00:00","value":184.15},{"at":"2026-09-26T04:45:00+00:00","value":190.61},{"at":"2026-09-26T05:00:00+00:00","value":194.92},{"at":"2026-09-26T05:15:00+00:00","value":196.88},{"at":"2026-09-26T05:30:00+00:00","value":195.6},{"at":"2026-09-26T05:45:00+00:00","value":196.76},{"at":"2026-09-26T06:00:00+00:00","value":211.34},{"at":"2026-09-26T06:15:00+00:00","value":203.0},{"at":"2026-09-26T06:30:00+00:00","value":187.34},{"at":"2026-09-26T06:45:00+00:00","value":166.4},{"at":"2026-09-26T07:00:00+00:00","value":193.17},{"at":"2026-09-26T07:15:00+00:00","value":165.98},{"at":"2026-09-26T07:30:00+00:00","value":139.03},{"at":"2026-09-26T07:45:00+00:00","value":127.59},{"at":"2026-09-26T08:00:00+00:00","value":132.41},{"at":"2026-09-26T08:15:00+00:00","value":120.56},{"at":"2026-09-26T08:30:00+00:00","value":104.99},{"at":"2026-09-26T08:45:00+00:00","value":97.54},{"at":"2026-09-26T09:00:00+00:00","value":78.49},{"at":"2026-09-26T09:15:00+00:00","value":59.02},{"at":"2026-09-26T09:30:00+00:00","value":46.32},{"at":"2026-09-26T09:45:00+00:00","value":39.62},{"at":"2026-09-26T10:00:00+00:00","value":30.3},{"at":"2026-09-26T10:15:00+00:00","value":26.93},{"at":"2026-09-26T10:30:00+00:00","value":22.31},{"at":"2026-09-26T10:45:00+00:00","value":16.15},{"at":"2026-09-26T11:00:00+00:00","value":11.42},{"at":"2026-09-26T11:15:00+00:00","value":2.22},{"at":"2026-09-26T11:30:00+00:00","value":0.76},{"at":"2026-09-26T11:45:00+00:00","value":0.76},{"at":"2026-09-26T12:00:00+00:00","value":8.99},{"at":"2026-09-26T12:15:00+00:00","value":12.51},{"at":"2026-09-26T12:30:00+00:00","value":23.3},{"at":"2026-09-26T12:45:00+00:00","value":25.02},{"at":"2026-09-26T13:00:00+00:00","value":23.0},{"at":"2026-09-26T13:15:00+00:00","value":40.0},{"at":"2026-09-26T13:30:00+00:00","value":35.93},{"at":"2026-09-26T13:45:00+00:00","value":59.07},{"at":"2026-09-26T14:00:00+00:00","value":62.43},{"at":"2026-09-26T14:15:00+00:00","value":95.77},{"at":"2026-09-26T14:30:00+00:00","value":106.77},{"at":"2026-09-26T14:45:00+00:00","value":160.1},{"at":"2026-09-26T15:00:00+00:00","value":141.25},{"at":"2026-09-26T15:15:00+00:00","value":158.98},{"at":"2026-09-26T15:30:00+00:00","value":128.03},{"at":"2026-09-26T15:45:00+00:00","value":181.76},{"at":"2026-09-26T16:00:00+00:00","value":169.94},{"at":"2026-09-26T16:15:00+00:00","value":202.75},{"at":"2026-09-26T16:30:00+00:00","value":219.48},{"at":"2026-09-26T16:45:00+00:00","value":234.23},{"at":"2026-09-26T17:00:00+00:00","value":222.0},{"at":"2026-09-26T17:15:00+00:00","value":230.46},{"at":"2026-09-26T17:30:00+00:00","value":243.61},{"at":"2026-09-26T17:45:00+00:00","value":251.08},{"at":"2026-09-26T18:00:00+00:00","value":238.97},{"at":"2026-09-26T18:15:00+00:00","value":232.0},{"at":"2026-09-26T18:30:00+00:00","value":222.48},{"at":"2026-09-26T18:45:00+00:00","value":211.99},{"at":"2026-09-26T19:00:00+00:00","value":218.18},{"at":"2026-09-26T19:15:00+00:00","value":210.24},{"at":"2026-09-26T19:30:00+00:00","value":205.53},{"at":"2026-09-26T19:45:00+00:00","value":200.0},{"at":"2026-09-26T20:00:00+00:00","value":207.0},{"at":"2026-09-26T20:15:00+00:00","value":200.62},{"at":"2026-09-26T20:30:00+00:00","value":197.73},{"at":"2026-09-26T20:45:00+00:00","value":191.89},{"at":"2026-09-26T21:00:00+00:00","value":195.2},{"at":"2026-09-26T21:15:00+00:00","value":188.45},{"at":"2026-09-26T21:30:00+00:00","value":182.55},{"at":"2026-09-26T21:45:00+00:00","value":177.8},{"at":"2026-09-26T22:00:00+00:00","value":192.07},{"at":"2026-09-26T22:15:00+00:00","value":187.0},{"at":"2026-09-26T22:30:00+00:00","value":183.34},{"at":"2026-09-26T22:45:00+00:00","value":172.83},{"at":"2026-09-26T23:00:00+00:00","value":180.7},{"at":"2026-09-26T23:15:00+00:00","value":178.0},{"at":"2026-09-26T23:30:00+00:00","value":176.62},{"at":"2026-09-26T23:45:00+00:00","value":178.0},{"at":"2026-09-27T00:00:00+00:00","value":176.0},{"at":"2026-09-27T00:15:00+00:00","value":171.31},{"at":"2026-09-27T00:30:00+00:00","value":169.97},{"at":"2026-09-27T00:45:00+00:00","value":168.08},{"at":"2026-09-27T01:00:00+00:00","value":168.16},{"at":"2026-09-27T01:15:00+00:00","value":166.78},{"at":"2026-09-27T01:30:00+00:00","value":165.4},{"at":"2026-09-27T01:45:00+00:00","value":165.39},{"at":"2026-09-27T02:00:00+00:00","value":165.0},{"at":"2026-09-27T02:15:00+00:00","value":160.83},{"at":"2026-09-27T02:30:00+00:00","value":160.44},{"at":"2026-09-27T02:45:00+00:00","value":160.0},{"at":"2026-09-27T03:00:00+00:00","value":160.44},{"at":"2026-09-27T03:15:00+00:00","value":158.08},{"at":"2026-09-27T03:30:00+00:00","value":159.4},{"at":"2026-09-27T03:45:00+00:00","value":156.76},{"at":"2026-09-27T04:00:00+00:00","value":156.25},{"at":"2026-09-27T04:15:00+00:00","value":156.79},{"at":"2026-09-27T04:30:00+00:00","value":163.19},{"at":"2026-09-27T04:45:00+00:00","value":163.77},{"at":"2026-09-27T05:00:00+00:00","value":169.21},{"at":"2026-09-27T05:15:00+00:00","value":160.68},{"at":"2026-09-27T05:30:00+00:00","value":147.95},{"at":"2026-09-27T05:45:00+00:00","value":134.63},{"at":"2026-09-27T06:00:00+00:00","value":160.43},{"at":"2026-09-27T06:15:00+00:00","value":143.86},{"at":"2026-09-27T06:30:00+00:00","value":119.48},{"at":"2026-09-27T06:45:00+00:00","value":95.84},{"at":"2026-09-27T07:00:00+00:00","value":110.16},{"at":"2026-09-27T07:15:00+00:00","value":80.97},{"at":"2026-09-27T07:30:00+00:00","value":37.22},{"at":"2026-09-27T07:45:00+00:00","value":23.14},{"at":"2026-09-27T08:00:00+00:00","value":36.14},{"at":"2026-09-27T08:15:00+00:00","value":15.85},{"at":"2026-09-27T08:30:00+00:00","value":4.47},{"at":"2026-09-27T08:45:00+00:00","value":1.5},{"at":"2026-09-27T09:00:00+00:00","value":0.89},{"at":"2026-09-27T09:15:00+00:00","value":0.0},{"at":"2026-09-27T09:30:00+00:00","value":0.0},{"at":"2026-09-27T09:45:00+00:00","value":0.0},{"at":"2026-09-27T10:00:00+00:00","value":-0.01},{"at":"2026-09-27T10:15:00+00:00","value":-0.01},{"at":"2026-09-27T10:30:00+00:00","value":-0.01},{"at":"2026-09-27T10:45:00+00:00","value":-0.01},{"at":"2026-09-27T11:00:00+00:00","value":-0.11},{"at":"2026-09-27T11:15:00+00:00","value":-0.11},{"at":"2026-09-27T11:30:00+00:00","value":-1.24},{"at":"2026-09-27T11:45:00+00:00","value":-2.03},{"at":"2026-09-27T12:00:00+00:00","value":-0.11},{"at":"2026-09-27T12:15:00+00:00","value":-0.11},{"at":"2026-09-27T12:30:00+00:00","value":-0.11},{"at":"2026-09-27T12:45:00+00:00","value":-0.11},{"at":"2026-09-27T13:00:00+00:00","value":-0.01},{"at":"2026-09-27T13:15:00+00:00","value":-0.01},{"at":"2026-09-27T13:30:00+00:00","value":0.0},{"at":"2026-09-27T13:45:00+00:00","value":0.0},{"at":"2026-09-27T14:00:00+00:00","value":0.0},{"at":"2026-09-27T14:15:00+00:00","value":0.15},{"at":"2026-09-27T14:30:00+00:00","value":7.01},{"at":"2026-09-27T14:45:00+00:00","value":45.25},{"at":"2026-09-27T15:00:00+00:00","value":41.25},{"at":"2026-09-27T15:15:00+00:00","value":92.71},{"at":"2026-09-27T15:30:00+00:00","value":144.61},{"at":"2026-09-27T15:45:00+00:00","value":179.2},{"at":"2026-09-27T16:00:00+00:00","value":168.79},{"at":"2026-09-27T16:15:00+00:00","value":189.78},{"at":"2026-09-27T16:30:00+00:00","value":198.61},{"at":"2026-09-27T16:45:00+00:00","value":202.34},{"at":"2026-09-27T17:00:00+00:00","value":195.34},{"at":"2026-09-27T17:15:00+00:00","value":196.64},{"at":"2026-09-27T17:30:00+00:00","value":205.0},{"at":"2026-09-27T17:45:00+00:00","value":210.26},{"at":"2026-09-27T18:00:00+00:00","value":201.21},{"at":"2026-09-27T18:15:00+00:00","value":201.0},{"at":"2026-09-27T18:30:00+00:00","value":197.33},{"at":"2026-09-27T18:45:00+00:00","value":186.26},{"at":"2026-09-27T19:00:00+00:00","value":191.66},{"at":"2026-09-27T19:15:00+00:00","value":185.6},{"at":"2026-09-27T19:30:00+00:00","value":175.53},{"at":"2026-09-27T19:45:00+00:00","value":168.22},{"at":"2026-09-27T20:00:00+00:00","value":181.92},{"at":"2026-09-27T20:15:00+00:00","value":173.66},{"at":"2026-09-27T20:30:00+00:00","value":172.32},{"at":"2026-09-27T20:45:00+00:00","value":163.89},{"at":"2026-09-27T21:00:00+00:00","value":168.36},{"at":"2026-09-27T21:15:00+00:00","value":162.42},{"at":"2026-09-27T21:30:00+00:00","value":159.91},{"at":"2026-09-27T21:45:00+00:00","value":153.85},{"at":"2026-09-27T22:00:00+00:00","value":162.9},{"at":"2026-09-27T22:15:00+00:00","value":163.01},{"at":"2026-09-27T22:30:00+00:00","value":163.54},{"at":"2026-09-27T22:45:00+00:00","value":162.51},{"at":"2026-09-27T23:00:00+00:00","value":168.03},{"at":"2026-09-27T23:15:00+00:00","value":163.02},{"at":"2026-09-27T23:30:00+00:00","value":163.54},{"at":"2026-09-27T23:45:00+00:00","value":162.2},{"at":"2026-09-28T00:00:00+00:00","value":160.05},{"at":"2026-09-28T00:15:00+00:00","value":157.65},{"at":"2026-09-28T00:30:00+00:00","value":156.03},{"at":"2026-09-28T00:45:00+00:00","value":154.49},{"at":"2026-09-28T01:00:00+00:00","value":155.15},{"at":"2026-09-28T01:15:00+00:00","value":157.06},{"at":"2026-09-28T01:30:00+00:00","value":157.44},{"at":"2026-09-28T01:45:00+00:00","value":159.56},{"at":"2026-09-28T02:00:00+00:00","value":158.58},{"at":"2026-09-28T02:15:00+00:00","value":160.0},{"at":"2026-09-28T02:30:00+00:00","value":163.54},{"at":"2026-09-28T02:45:00+00:00","value":168.69},{"at":"2026-09-28T03:00:00+00:00","value":169.26},{"at":"2026-09-28T03:15:00+00:00","value":173.1},{"at":"2026-09-28T03:30:00+00:00","value":178.08},{"at":"2026-09-28T03:45:00+00:00","value":185.9},{"at":"2026-09-28T04:00:00+00:00","value":193.68},{"at":"2026-09-28T04:15:00+00:00","value":204.99},{"at":"2026-09-28T04:30:00+00:00","value":214.84},{"at":"2026-09-28T04:45:00+00:00","value":231.02},{"at":"2026-09-28T05:00:00+00:00","value":229.39},{"at":"2026-09-28T05:15:00+00:00","value":244.02},{"at":"2026-09-28T05:30:00+00:00","value":246.3},{"at":"2026-09-28T05:45:00+00:00","value":245.84},{"at":"2026-09-28T06:00:00+00:00","value":275.95},{"at":"2026-09-28T06:15:00+00:00","value":254.9},{"at":"2026-09-28T06:30:00+00:00","value":241.63},{"at":"2026-09-28T06:45:00+00:00","value":227.52},{"at":"2026-09-28T07:00:00+00:00","value":255.75},{"at":"2026-09-28T07:15:00+00:00","value":241.6},{"at":"2026-09-28T07:30:00+00:00","value":233.16},{"at":"2026-09-28T07:45:00+00:00","value":213.58},{"at":"2026-09-28T08:00:00+00:00","value":225.99},{"at":"2026-09-28T08:15:00+00:00","value":210.02},{"at":"2026-09-28T08:30:00+00:00","value":201.81},{"at":"2026-09-28T08:45:00+00:00","value":177.7},{"at":"2026-09-28T09:00:00+00:00","value":181.66},{"at":"2026-09-28T09:15:00+00:00","value":177.98},{"at":"2026-09-28T09:30:00+00:00","value":180.8},{"at":"2026-09-28T09:45:00+00:00","value":175.58},{"at":"2026-09-28T10:00:00+00:00","value":175.43},{"at":"2026-09-28T10:15:00+00:00","value":155.0},{"at":"2026-09-28T10:30:00+00:00","value":153.75},{"at":"2026-09-28T10:45:00+00:00","value":148.56},{"at":"2026-09-28T11:00:00+00:00","value":151.94},{"at":"2026-09-28T11:15:00+00:00","value":147.32},{"at":"2026-09-28T11:30:00+00:00","value":149.5},{"at":"2026-09-28T11:45:00+00:00","value":152.53},{"at":"2026-09-28T12:00:00+00:00","value":152.4},{"at":"2026-09-28T12:15:00+00:00","value":155.42},{"at":"2026-09-28T12:30:00+00:00","value":159.0},{"at":"2026-09-28T12:45:00+00:00","value":163.58},{"at":"2026-09-28T13:00:00+00:00","value":158.1},{"at":"2026-09-28T13:15:00+00:00","value":164.76},{"at":"2026-09-28T13:30:00+00:00","value":165.0},{"at":"2026-09-28T13:45:00+00:00","value":182.0},{"at":"2026-09-28T14:00:00+00:00","value":169.95},{"at":"2026-09-28T14:15:00+00:00","value":186.87},{"at":"2026-09-28T14:30:00+00:00","value":201.93},{"at":"2026-09-28T14:45:00+00:00","value":217.88},{"at":"2026-09-28T15:00:00+00:00","value":207.45},{"at":"2026-09-28T15:15:00+00:00","value":231.26},{"at":"2026-09-28T15:30:00+00:00","value":241.07},{"at":"2026-09-28T15:45:00+00:00","value":266.9},{"at":"2026-09-28T16:00:00+00:00","value":234.14},{"at":"2026-09-28T16:15:00+00:00","value":252.66},{"at":"2026-09-28T16:30:00+00:00","value":294.11},{"at":"2026-09-28T16:45:00+00:00","value":390.6},{"at":"2026-09-28T17:00:00+00:00","value":350.0},{"at":"2026-09-28T17:15:00+00:00","value":354.0},{"at":"2026-09-28T17:30:00+00:00","value":349.99},{"at":"2026-09-28T17:45:00+00:00","value":314.86},{"at":"2026-09-28T18:00:00+00:00","value":320.83},{"at":"2026-09-28T18:15:00+00:00","value":280.59},{"at":"2026-09-28T18:30:00+00:00","value":260.91},{"at":"2026-09-28T18:45:00+00:00","value":246.9},{"at":"2026-09-28T19:00:00+00:00","value":252.58},{"at":"2026-09-28T19:15:00+00:00","value":234.44},{"at":"2026-09-28T19:30:00+00:00","value":223.98},{"at":"2026-09-28T19:45:00+00:00","value":205.0},{"at":"2026-09-28T20:00:00+00:00","value":216.93},{"at":"2026-09-28T20:15:00+00:00","value":208.16},{"at":"2026-09-28T20:30:00+00:00","value":201.99},{"at":"2026-09-28T20:45:00+00:00","value":186.32},{"at":"2026-09-28T21:00:00+00:00","value":197.01},{"at":"2026-09-28T21:15:00+00:00","value":187.78},{"at":"2026-09-28T21:30:00+00:00","value":179.24},{"at":"2026-09-28T21:45:00+00:00","value":168.66},{"at":"2026-09-28T22:00:00+00:00","value":201.22},{"at":"2026-09-28T22:15:00+00:00","value":191.39},{"at":"2026-09-28T22:30:00+00:00","value":181.38},{"at":"2026-09-28T22:45:00+00:00","value":175.18},{"at":"2026-09-28T23:00:00+00:00","value":183.46},{"at":"2026-09-28T23:15:00+00:00","value":177.19},{"at":"2026-09-28T23:30:00+00:00","value":174.89},{"at":"2026-09-28T23:45:00+00:00","value":169.09},{"at":"2026-09-29T00:00:00+00:00","value":173.53},{"at":"2026-09-29T00:15:00+00:00","value":171.98},{"at":"2026-09-29T00:30:00+00:00","value":170.98},{"at":"2026-09-29T00:45:00+00:00","value":169.56},{"at":"2026-09-29T01:00:00+00:00","value":166.26},{"at":"2026-09-29T01:15:00+00:00","value":167.06},{"at":"2026-09-29T01:30:00+00:00","value":165.29},{"at":"2026-09-29T01:45:00+00:00","value":166.9},{"at":"2026-09-29T02:00:00+00:00","value":163.39},{"at":"2026-09-29T02:15:00+00:00","value":163.53},{"at":"2026-09-29T02:30:00+00:00","value":161.95},{"at":"2026-09-29T02:45:00+00:00","value":158.41},{"at":"2026-09-29T03:00:00+00:00","value":157.1},{"at":"2026-09-29T03:15:00+00:00","value":160.7},{"at":"2026-09-29T03:30:00+00:00","value":172.94},{"at":"2026-09-29T03:45:00+00:00","value":180.0},{"at":"2026-09-29T04:00:00+00:00","value":172.8},{"at":"2026-09-29T04:15:00+00:00","value":185.0},{"at":"2026-09-29T04:30:00+00:00","value":194.62},{"at":"2026-09-29T04:45:00+00:00","value":210.37},{"at":"2026-09-29T05:00:00+00:00","value":211.75},{"at":"2026-09-29T05:15:00+00:00","value":228.1},{"at":"2026-09-29T05:30:00+00:00","value":228.64},{"at":"2026-09-29T05:45:00+00:00","value":228.1},{"at":"2026-09-29T06:00:00+00:00","value":239.17},{"at":"2026-09-29T06:15:00+00:00","value":231.15},{"at":"2026-09-29T06:30:00+00:00","value":216.12},{"at":"2026-09-29T06:45:00+00:00","value":193.96},{"at":"2026-09-29T07:00:00+00:00","value":215.83},{"at":"2026-09-29T07:15:00+00:00","value":189.43},{"at":"2026-09-29T07:30:00+00:00","value":178.12},{"at":"2026-09-29T07:45:00+00:00","value":169.02},{"at":"2026-09-29T08:00:00+00:00","value":200.25},{"at":"2026-09-29T08:15:00+00:00","value":187.45},{"at":"2026-09-29T08:30:00+00:00","value":180.36},{"at":"2026-09-29T08:45:00+00:00","value":161.46},{"at":"2026-09-29T09:00:00+00:00","value":157.73},{"at":"2026-09-29T09:15:00+00:00","value":143.77},{"at":"2026-09-29T09:30:00+00:00","value":119.08},{"at":"2026-09-29T09:45:00+00:00","value":106.43},{"at":"2026-09-29T10:00:00+00:00","value":103.05},{"at":"2026-09-29T10:15:00+00:00","value":93.72},{"at":"2026-09-29T10:30:00+00:00","value":93.45},{"at":"2026-09-29T10:45:00+00:00","value":79.93},{"at":"2026-09-29T11:00:00+00:00","value":86.38},{"at":"2026-09-29T11:15:00+00:00","value":77.99},{"at":"2026-09-29T11:30:00+00:00","value":70.21},{"at":"2026-09-29T11:45:00+00:00","value":64.07},{"at":"2026-09-29T12:00:00+00:00","value":65.66},{"at":"2026-09-29T12:15:00+00:00","value":79.03},{"at":"2026-09-29T12:30:00+00:00","value":88.03},{"at":"2026-09-29T12:45:00+00:00","value":93.47},{"at":"2026-09-29T13:00:00+00:00","value":89.63},{"at":"2026-09-29T13:15:00+00:00","value":105.31},{"at":"2026-09-29T13:30:00+00:00","value":96.11},{"at":"2026-09-29T13:45:00+00:00","value":110.73},{"at":"2026-09-29T14:00:00+00:00","value":95.83},{"at":"2026-09-29T14:15:00+00:00","value":127.17},{"at":"2026-09-29T14:30:00+00:00","value":143.77},{"at":"2026-09-29T14:45:00+00:00","value":181.17},{"at":"2026-09-29T15:00:00+00:00","value":167.13},{"at":"2026-09-29T15:15:00+00:00","value":171.48},{"at":"2026-09-29T15:30:00+00:00","value":160.52},{"at":"2026-09-29T15:45:00+00:00","value":205.22},{"at":"2026-09-29T16:00:00+00:00","value":182.9},{"at":"2026-09-29T16:15:00+00:00","value":222.41},{"at":"2026-09-29T16:30:00+00:00","value":232.88},{"at":"2026-09-29T16:45:00+00:00","value":250.12},{"at":"2026-09-29T17:00:00+00:00","value":243.54},{"at":"2026-09-29T17:15:00+00:00","value":240.44},{"at":"2026-09-29T17:30:00+00:00","value":243.03},{"at":"2026-09-29T17:45:00+00:00","value":236.24},{"at":"2026-09-29T18:00:00+00:00","value":238.94},{"at":"2026-09-29T18:15:00+00:00","value":227.55},{"at":"2026-09-29T18:30:00+00:00","value":213.58},{"at":"2026-09-29T18:45:00+00:00","value":198.14},{"at":"2026-09-29T19:00:00+00:00","value":189.14},{"at":"2026-09-29T19:15:00+00:00","value":187.65},{"at":"2026-09-29T19:30:00+00:00","value":180.22},{"at":"2026-09-29T19:45:00+00:00","value":168.64},{"at":"2026-09-29T20:00:00+00:00","value":176.0},{"at":"2026-09-29T20:15:00+00:00","value":168.49},{"at":"2026-09-29T20:30:00+00:00","value":173.0},{"at":"2026-09-29T20:45:00+00:00","value":153.89},{"at":"2026-09-29T21:00:00+00:00","value":151.87},{"at":"2026-09-29T21:15:00+00:00","value":144.36},{"at":"2026-09-29T21:30:00+00:00","value":140.33},{"at":"2026-09-29T21:45:00+00:00","value":128.83},{"at":"2026-09-29T22:00:00+00:00","value":122.15},{"at":"2026-09-29T22:15:00+00:00","value":107.57},{"at":"2026-09-29T22:30:00+00:00","value":94.26},{"at":"2026-09-29T22:45:00+00:00","value":40.96},{"at":"2026-09-29T23:00:00+00:00","value":100.0},{"at":"2026-09-29T23:15:00+00:00","value":73.01},{"at":"2026-09-29T23:30:00+00:00","value":75.91},{"at":"2026-09-29T23:45:00+00:00","value":32.72},{"at":"2026-09-30T00:00:00+00:00","value":90.0},{"at":"2026-09-30T00:15:00+00:00","value":101.94},{"at":"2026-09-30T00:30:00+00:00","value":55.41},{"at":"2026-09-30T00:45:00+00:00","value":20.59},{"at":"2026-09-30T01:00:00+00:00","value":80.76},{"at":"2026-09-30T01:15:00+00:00","value":34.54},{"at":"2026-09-30T01:30:00+00:00","value":30.53},{"at":"2026-09-30T01:45:00+00:00","value":44.95},{"at":"2026-09-30T02:00:00+00:00","value":32.45},{"at":"2026-09-30T02:15:00+00:00","value":53.12},{"at":"2026-09-30T02:30:00+00:00","value":55.0},{"at":"2026-09-30T02:45:00+00:00","value":60.67},{"at":"2026-09-30T03:00:00+00:00","value":20.95},{"at":"2026-09-30T03:15:00+00:00","value":40.04},{"at":"2026-09-30T03:30:00+00:00","value":38.56},{"at":"2026-09-30T03:45:00+00:00","value":114.24},{"at":"2026-09-30T04:00:00+00:00","value":150.0},{"at":"2026-09-30T04:15:00+00:00","value":164.0},{"at":"2026-09-30T04:30:00+00:00","value":171.59},{"at":"2026-09-30T04:45:00+00:00","value":174.0},{"at":"2026-09-30T05:00:00+00:00","value":192.88},{"at":"2026-09-30T05:15:00+00:00","value":207.0},{"at":"2026-09-30T05:30:00+00:00","value":211.81},{"at":"2026-09-30T05:45:00+00:00","value":207.07},{"at":"2026-09-30T06:00:00+00:00","value":223.94},{"at":"2026-09-30T06:15:00+00:00","value":208.48},{"at":"2026-09-30T06:30:00+00:00","value":189.98},{"at":"2026-09-30T06:45:00+00:00","value":169.59},{"at":"2026-09-30T07:00:00+00:00","value":201.94},{"at":"2026-09-30T07:15:00+00:00","value":184.99},{"at":"2026-09-30T07:30:00+00:00","value":173.54},{"at":"2026-09-30T07:45:00+00:00","value":162.41},{"at":"2026-09-30T08:00:00+00:00","value":185.87},{"at":"2026-09-30T08:15:00+00:00","value":175.5},{"at":"2026-09-30T08:30:00+00:00","value":145.1},{"at":"2026-09-30T08:45:00+00:00","value":132.08},{"at":"2026-09-30T09:00:00+00:00","value":132.35},{"at":"2026-09-30T09:15:00+00:00","value":130.0},{"at":"2026-09-30T09:30:00+00:00","value":124.79},{"at":"2026-09-30T09:45:00+00:00","value":115.15},{"at":"2026-09-30T10:00:00+00:00","value":103.41},{"at":"2026-09-30T10:15:00+00:00","value":108.7},{"at":"2026-09-30T10:30:00+00:00","value":108.7},{"at":"2026-09-30T10:45:00+00:00","value":100.0},{"at":"2026-09-30T11:00:00+00:00","value":89.99},{"at":"2026-09-30T11:15:00+00:00","value":90.7},{"at":"2026-09-30T11:30:00+00:00","value":90.0},{"at":"2026-09-30T11:45:00+00:00","value":85.6},{"at":"2026-09-30T12:00:00+00:00","value":89.4},{"at":"2026-09-30T12:15:00+00:00","value":94.99},{"at":"2026-09-30T12:30:00+00:00","value":100.0},{"at":"2026-09-30T12:45:00+00:00","value":118.55},{"at":"2026-09-30T13:00:00+00:00","value":112.93},{"at":"2026-09-30T13:15:00+00:00","value":121.87},{"at":"2026-09-30T13:30:00+00:00","value":127.87},{"at":"2026-09-30T13:45:00+00:00","value":123.68},{"at":"2026-09-30T14:00:00+00:00","value":120.68},{"at":"2026-09-30T14:15:00+00:00","value":135.59},{"at":"2026-09-30T14:30:00+00:00","value":171.38},{"at":"2026-09-30T14:45:00+00:00","value":191.47},{"at":"2026-09-30T15:00:00+00:00","value":174.62},{"at":"2026-09-30T15:15:00+00:00","value":196.78},{"at":"2026-09-30T15:30:00+00:00","value":213.58},{"at":"2026-09-30T15:45:00+00:00","value":233.17},{"at":"2026-09-30T16:00:00+00:00","value":214.87},{"at":"2026-09-30T16:15:00+00:00","value":228.7},{"at":"2026-09-30T16:30:00+00:00","value":235.0},{"at":"2026-09-30T16:45:00+00:00","value":251.77},{"at":"2026-09-30T17:00:00+00:00","value":243.77},{"at":"2026-09-30T17:15:00+00:00","value":250.0},{"at":"2026-09-30T17:30:00+00:00","value":260.0},{"at":"2026-09-30T17:45:00+00:00","value":261.03},{"at":"2026-09-30T18:00:00+00:00","value":249.79},{"at":"2026-09-30T18:15:00+00:00","value":248.59},{"at":"2026-09-30T18:30:00+00:00","value":232.14},{"at":"2026-09-30T18:45:00+00:00","value":221.41},{"at":"2026-09-30T19:00:00+00:00","value":243.15},{"at":"2026-09-30T19:15:00+00:00","value":230.45},{"at":"2026-09-30T19:30:00+00:00","value":212.76},{"at":"2026-09-30T19:45:00+00:00","value":175.86},{"at":"2026-09-30T20:00:00+00:00","value":223.49},{"at":"2026-09-30T20:15:00+00:00","value":201.93},{"at":"2026-09-30T20:30:00+00:00","value":200.96},{"at":"2026-09-30T20:45:00+00:00","value":190.0},{"at":"2026-09-30T21:00:00+00:00","value":202.38},{"at":"2026-09-30T21:15:00+00:00","value":184.3},{"at":"2026-09-30T21:30:00+00:00","value":199.6},{"at":"2026-09-30T21:45:00+00:00","value":173.72}],"de":[{"at":"2026-09-18T22:00:00+00:00","value":132.52},{"at":"2026-09-18T22:15:00+00:00","value":117.76},{"at":"2026-09-18T22:30:00+00:00","value":97.43},{"at":"2026-09-18T22:45:00+00:00","value":65.83},{"at":"2026-09-18T23:00:00+00:00","value":96.05},{"at":"2026-09-18T23:15:00+00:00","value":82.44},{"at":"2026-09-18T23:30:00+00:00","value":79.18},{"at":"2026-09-18T23:45:00+00:00","value":60.43},{"at":"2026-09-19T00:00:00+00:00","value":73.77},{"at":"2026-09-19T00:15:00+00:00","value":62.38},{"at":"2026-09-19T00:30:00+00:00","value":52.75},{"at":"2026-09-19T00:45:00+00:00","value":48.02},{"at":"2026-09-19T01:00:00+00:00","value":45.15},{"at":"2026-09-19T01:15:00+00:00","value":32.75},{"at":"2026-09-19T01:30:00+00:00","value":26.48},{"at":"2026-09-19T01:45:00+00:00","value":23.16},{"at":"2026-09-19T02:00:00+00:00","value":33.57},{"at":"2026-09-19T02:15:00+00:00","value":36.04},{"at":"2026-09-19T02:30:00+00:00","value":36.9},{"at":"2026-09-19T02:45:00+00:00","value":36.66},{"at":"2026-09-19T03:00:00+00:00","value":34.79},{"at":"2026-09-19T03:15:00+00:00","value":34.41},{"at":"2026-09-19T03:30:00+00:00","value":34.03},{"at":"2026-09-19T03:45:00+00:00","value":39.94},{"at":"2026-09-19T04:00:00+00:00","value":40.74},{"at":"2026-09-19T04:15:00+00:00","value":46.66},{"at":"2026-09-19T04:30:00+00:00","value":40.08},{"at":"2026-09-19T04:45:00+00:00","value":43.47},{"at":"2026-09-19T05:00:00+00:00","value":41.38},{"at":"2026-09-19T05:15:00+00:00","value":41.99},{"at":"2026-09-19T05:30:00+00:00","value":45.07},{"at":"2026-09-19T05:45:00+00:00","value":40.1},{"at":"2026-09-19T06:00:00+00:00","value":47.71},{"at":"2026-09-19T06:15:00+00:00","value":36.53},{"at":"2026-09-19T06:30:00+00:00","value":27.96},{"at":"2026-09-19T06:45:00+00:00","value":11.8},{"at":"2026-09-19T07:00:00+00:00","value":16.9},{"at":"2026-09-19T07:15:00+00:00","value":6.55},{"at":"2026-09-19T07:30:00+00:00","value":2.74},{"at":"2026-09-19T07:45:00+00:00","value":0.01},{"at":"2026-09-19T08:00:00+00:00","value":0.1},{"at":"2026-09-19T08:15:00+00:00","value":0.0},{"at":"2026-09-19T08:30:00+00:00","value":-0.03},{"at":"2026-09-19T08:45:00+00:00","value":-0.09},{"at":"2026-09-19T09:00:00+00:00","value":-0.13},{"at":"2026-09-19T09:15:00+00:00","value":-0.16},{"at":"2026-09-19T09:30:00+00:00","value":-0.21},{"at":"2026-09-19T09:45:00+00:00","value":-0.74},{"at":"2026-09-19T10:00:00+00:00","value":-0.78},{"at":"2026-09-19T10:15:00+00:00","value":-0.65},{"at":"2026-09-19T10:30:00+00:00","value":-0.71},{"at":"2026-09-19T10:45:00+00:00","value":-0.86},{"at":"2026-09-19T11:00:00+00:00","value":-1.01},{"at":"2026-09-19T11:15:00+00:00","value":-1.06},{"at":"2026-09-19T11:30:00+00:00","value":-1.34},{"at":"2026-09-19T11:45:00+00:00","value":-1.62},{"at":"2026-09-19T12:00:00+00:00","value":-1.27},{"at":"2026-09-19T12:15:00+00:00","value":-1.26},{"at":"2026-09-19T12:30:00+00:00","value":-1.21},{"at":"2026-09-19T12:45:00+00:00","value":-1.46},{"at":"2026-09-19T13:00:00+00:00","value":-1.85},{"at":"2026-09-19T13:15:00+00:00","value":-1.5},{"at":"2026-09-19T13:30:00+00:00","value":-1.43},{"at":"2026-09-19T13:45:00+00:00","value":-1.94},{"at":"2026-09-19T14:00:00+00:00","value":-0.1},{"at":"2026-09-19T14:15:00+00:00","value":-0.07},{"at":"2026-09-19T14:30:00+00:00","value":-0.01},{"at":"2026-09-19T14:45:00+00:00","value":0.0},{"at":"2026-09-19T15:00:00+00:00","value":0.0},{"at":"2026-09-19T15:15:00+00:00","value":0.0},{"at":"2026-09-19T15:30:00+00:00","value":8.2},{"at":"2026-09-19T15:45:00+00:00","value":25.0},{"at":"2026-09-19T16:00:00+00:00","value":30.0},{"at":"2026-09-19T16:15:00+00:00","value":51.74},{"at":"2026-09-19T16:30:00+00:00","value":79.66},{"at":"2026-09-19T16:45:00+00:00","value":100.43},{"at":"2026-09-19T17:00:00+00:00","value":99.98},{"at":"2026-09-19T17:15:00+00:00","value":119.52},{"at":"2026-09-19T17:30:00+00:00","value":129.37},{"at":"2026-09-19T17:45:00+00:00","value":134.25},{"at":"2026-09-19T18:00:00+00:00","value":133.07},{"at":"2026-09-19T18:15:00+00:00","value":119.19},{"at":"2026-09-19T18:30:00+00:00","value":107.0},{"at":"2026-09-19T18:45:00+00:00","value":99.94},{"at":"2026-09-19T19:00:00+00:00","value":101.57},{"at":"2026-09-19T19:15:00+00:00","value":99.95},{"at":"2026-09-19T19:30:00+00:00","value":91.05},{"at":"2026-09-19T19:45:00+00:00","value":67.32},{"at":"2026-09-19T20:00:00+00:00","value":88.87},{"at":"2026-09-19T20:15:00+00:00","value":86.21},{"at":"2026-09-19T20:30:00+00:00","value":83.64},{"at":"2026-09-19T20:45:00+00:00","value":75.7},{"at":"2026-09-19T21:00:00+00:00","value":85.0},{"at":"2026-09-19T21:15:00+00:00","value":80.0},{"at":"2026-09-19T21:30:00+00:00","value":77.65},{"at":"2026-09-19T21:45:00+00:00","value":70.82},{"at":"2026-09-19T22:00:00+00:00","value":18.2},{"at":"2026-09-19T22:15:00+00:00","value":16.37},{"at":"2026-09-19T22:30:00+00:00","value":14.99},{"at":"2026-09-19T22:45:00+00:00","value":13.61},{"at":"2026-09-19T23:00:00+00:00","value":14.85},{"at":"2026-09-19T23:15:00+00:00","value":13.05},{"at":"2026-09-19T23:30:00+00:00","value":12.49},{"at":"2026-09-19T23:45:00+00:00","value":11.04},{"at":"2026-09-20T00:00:00+00:00","value":8.57},{"at":"2026-09-20T00:15:00+00:00","value":11.25},{"at":"2026-09-20T00:30:00+00:00","value":12.2},{"at":"2026-09-20T00:45:00+00:00","value":8.0},{"at":"2026-09-20T01:00:00+00:00","value":8.19},{"at":"2026-09-20T01:15:00+00:00","value":7.92},{"at":"2026-09-20T01:30:00+00:00","value":8.05},{"at":"2026-09-20T01:45:00+00:00","value":7.09},{"at":"2026-09-20T02:00:00+00:00","value":9.69},{"at":"2026-09-20T02:15:00+00:00","value":8.95},{"at":"2026-09-20T02:30:00+00:00","value":8.75},{"at":"2026-09-20T02:45:00+00:00","value":8.6},{"at":"2026-09-20T03:00:00+00:00","value":10.12},{"at":"2026-09-20T03:15:00+00:00","value":9.62},{"at":"2026-09-20T03:30:00+00:00","value":9.47},{"at":"2026-09-20T03:45:00+00:00","value":10.81},{"at":"2026-09-20T04:00:00+00:00","value":8.13},{"at":"2026-09-20T04:15:00+00:00","value":8.96},{"at":"2026-09-20T04:30:00+00:00","value":10.37},{"at":"2026-09-20T04:45:00+00:00","value":12.55},{"at":"2026-09-20T05:00:00+00:00","value":11.51},{"at":"2026-09-20T05:15:00+00:00","value":12.74},{"at":"2026-09-20T05:30:00+00:00","value":13.34},{"at":"2026-09-20T05:45:00+00:00","value":11.49},{"at":"2026-09-20T06:00:00+00:00","value":13.4},{"at":"2026-09-20T06:15:00+00:00","value":12.51},{"at":"2026-09-20T06:30:00+00:00","value":8.34},{"at":"2026-09-20T06:45:00+00:00","value":5.12},{"at":"2026-09-20T07:00:00+00:00","value":8.15},{"at":"2026-09-20T07:15:00+00:00","value":5.06},{"at":"2026-09-20T07:30:00+00:00","value":1.4},{"at":"2026-09-20T07:45:00+00:00","value":0.01},{"at":"2026-09-20T08:00:00+00:00","value":0.01},{"at":"2026-09-20T08:15:00+00:00","value":0.0},{"at":"2026-09-20T08:30:00+00:00","value":-0.01},{"at":"2026-09-20T08:45:00+00:00","value":-0.04},{"at":"2026-09-20T09:00:00+00:00","value":-0.04},{"at":"2026-09-20T09:15:00+00:00","value":-0.1},{"at":"2026-09-20T09:30:00+00:00","value":-0.12},{"at":"2026-09-20T09:45:00+00:00","value":-0.17},{"at":"2026-09-20T10:00:00+00:00","value":-1.0},{"at":"2026-09-20T10:15:00+00:00","value":-1.0},{"at":"2026-09-20T10:30:00+00:00","value":-1.05},{"at":"2026-09-20T10:45:00+00:00","value":-1.59},{"at":"2026-09-20T11:00:00+00:00","value":-1.92},{"at":"2026-09-20T11:15:00+00:00","value":-1.97},{"at":"2026-09-20T11:30:00+00:00","value":-2.02},{"at":"2026-09-20T11:45:00+00:00","value":-2.02},{"at":"2026-09-20T12:00:00+00:00","value":-1.94},{"at":"2026-09-20T12:15:00+00:00","value":-1.95},{"at":"2026-09-20T12:30:00+00:00","value":-1.94},{"at":"2026-09-20T12:45:00+00:00","value":-1.91},{"at":"2026-09-20T13:00:00+00:00","value":-1.56},{"at":"2026-09-20T13:15:00+00:00","value":-1.39},{"at":"2026-09-20T13:30:00+00:00","value":-1.01},{"at":"2026-09-20T13:45:00+00:00","value":-1.0},{"at":"2026-09-20T14:00:00+00:00","value":-0.18},{"at":"2026-09-20T14:15:00+00:00","value":-0.1},{"at":"2026-09-20T14:30:00+00:00","value":-0.08},{"at":"2026-09-20T14:45:00+00:00","value":-0.01},{"at":"2026-09-20T15:00:00+00:00","value":-0.03},{"at":"2026-09-20T15:15:00+00:00","value":0.0},{"at":"2026-09-20T15:30:00+00:00","value":0.01},{"at":"2026-09-20T15:45:00+00:00","value":10.72},{"at":"2026-09-20T16:00:00+00:00","value":15.13},{"at":"2026-09-20T16:15:00+00:00","value":35.62},{"at":"2026-09-20T16:30:00+00:00","value":58.37},{"at":"2026-09-20T16:45:00+00:00","value":92.51},{"at":"2026-09-20T17:00:00+00:00","value":61.64},{"at":"2026-09-20T17:15:00+00:00","value":79.14},{"at":"2026-09-20T17:30:00+00:00","value":86.21},{"at":"2026-09-20T17:45:00+00:00","value":102.24},{"at":"2026-09-20T18:00:00+00:00","value":86.69},{"at":"2026-09-20T18:15:00+00:00","value":88.42},{"at":"2026-09-20T18:30:00+00:00","value":82.02},{"at":"2026-09-20T18:45:00+00:00","value":89.48},{"at":"2026-09-20T19:00:00+00:00","value":90.08},{"at":"2026-09-20T19:15:00+00:00","value":79.26},{"at":"2026-09-20T19:30:00+00:00","value":67.9},{"at":"2026-09-20T19:45:00+00:00","value":65.36},{"at":"2026-09-20T20:00:00+00:00","value":76.2},{"at":"2026-09-20T20:15:00+00:00","value":80.07},{"at":"2026-09-20T20:30:00+00:00","value":67.31},{"at":"2026-09-20T20:45:00+00:00","value":61.68},{"at":"2026-09-20T21:00:00+00:00","value":63.74},{"at":"2026-09-20T21:15:00+00:00","value":60.09},{"at":"2026-09-20T21:30:00+00:00","value":57.78},{"at":"2026-09-20T21:45:00+00:00","value":51.76},{"at":"2026-09-20T22:00:00+00:00","value":50.68},{"at":"2026-09-20T22:15:00+00:00","value":50.29},{"at":"2026-09-20T22:30:00+00:00","value":45.28},{"at":"2026-09-20T22:45:00+00:00","value":40.81},{"at":"2026-09-20T23:00:00+00:00","value":45.61},{"at":"2026-09-20T23:15:00+00:00","value":41.88},{"at":"2026-09-20T23:30:00+00:00","value":42.85},{"at":"2026-09-20T23:45:00+00:00","value":40.01},{"at":"2026-09-21T00:00:00+00:00","value":41.33},{"at":"2026-09-21T00:15:00+00:00","value":37.85},{"at":"2026-09-21T00:30:00+00:00","value":38.38},{"at":"2026-09-21T00:45:00+00:00","value":39.82},{"at":"2026-09-21T01:00:00+00:00","value":40.85},{"at":"2026-09-21T01:15:00+00:00","value":41.02},{"at":"2026-09-21T01:30:00+00:00","value":39.9},{"at":"2026-09-21T01:45:00+00:00","value":37.99},{"at":"2026-09-21T02:00:00+00:00","value":37.53},{"at":"2026-09-21T02:15:00+00:00","value":39.24},{"at":"2026-09-21T02:30:00+00:00","value":43.76},{"at":"2026-09-21T02:45:00+00:00","value":47.2},{"at":"2026-09-21T03:00:00+00:00","value":43.27},{"at":"2026-09-21T03:15:00+00:00","value":54.93},{"at":"2026-09-21T03:30:00+00:00","value":60.38},{"at":"2026-09-21T03:45:00+00:00","value":76.69},{"at":"2026-09-21T04:00:00+00:00","value":91.43},{"at":"2026-09-21T04:15:00+00:00","value":124.61},{"at":"2026-09-21T04:30:00+00:00","value":130.5},{"at":"2026-09-21T04:45:00+00:00","value":148.88},{"at":"2026-09-21T05:00:00+00:00","value":160.88},{"at":"2026-09-21T05:15:00+00:00","value":187.01},{"at":"2026-09-21T05:30:00+00:00","value":194.48},{"at":"2026-09-21T05:45:00+00:00","value":170.08},{"at":"2026-09-21T06:00:00+00:00","value":257.09},{"at":"2026-09-21T06:15:00+00:00","value":195.49},{"at":"2026-09-21T06:30:00+00:00","value":154.11},{"at":"2026-09-21T06:45:00+00:00","value":108.01},{"at":"2026-09-21T07:00:00+00:00","value":121.74},{"at":"2026-09-21T07:15:00+00:00","value":103.29},{"at":"2026-09-21T07:30:00+00:00","value":63.51},{"at":"2026-09-21T07:45:00+00:00","value":43.74},{"at":"2026-09-21T08:00:00+00:00","value":62.15},{"at":"2026-09-21T08:15:00+00:00","value":33.39},{"at":"2026-09-21T08:30:00+00:00","value":28.43},{"at":"2026-09-21T08:45:00+00:00","value":11.39},{"at":"2026-09-21T09:00:00+00:00","value":19.82},{"at":"2026-09-21T09:15:00+00:00","value":13.13},{"at":"2026-09-21T09:30:00+00:00","value":2.66},{"at":"2026-09-21T09:45:00+00:00","value":0.03},{"at":"2026-09-21T10:00:00+00:00","value":0.76},{"at":"2026-09-21T10:15:00+00:00","value":0.01},{"at":"2026-09-21T10:30:00+00:00","value":0.02},{"at":"2026-09-21T10:45:00+00:00","value":0.01},{"at":"2026-09-21T11:00:00+00:00","value":0.0},{"at":"2026-09-21T11:15:00+00:00","value":0.0},{"at":"2026-09-21T11:30:00+00:00","value":0.0},{"at":"2026-09-21T11:45:00+00:00","value":0.0},{"at":"2026-09-21T12:00:00+00:00","value":0.0},{"at":"2026-09-21T12:15:00+00:00","value":0.0},{"at":"2026-09-21T12:30:00+00:00","value":0.01},{"at":"2026-09-21T12:45:00+00:00","value":0.03},{"at":"2026-09-21T13:00:00+00:00","value":0.0},{"at":"2026-09-21T13:15:00+00:00","value":0.03},{"at":"2026-09-21T13:30:00+00:00","value":0.1},{"at":"2026-09-21T13:45:00+00:00","value":5.47},{"at":"2026-09-21T14:00:00+00:00","value":0.08},{"at":"2026-09-21T14:15:00+00:00","value":20.95},{"at":"2026-09-21T14:30:00+00:00","value":33.95},{"at":"2026-09-21T14:45:00+00:00","value":59.32},{"at":"2026-09-21T15:00:00+00:00","value":22.71},{"at":"2026-09-21T15:15:00+00:00","value":67.08},{"at":"2026-09-21T15:30:00+00:00","value":135.63},{"at":"2026-09-21T15:45:00+00:00","value":203.34},{"at":"2026-09-21T16:00:00+00:00","value":166.62},{"at":"2026-09-21T16:15:00+00:00","value":198.79},{"at":"2026-09-21T16:30:00+00:00","value":222.59},{"at":"2026-09-21T16:45:00+00:00","value":261.72},{"at":"2026-09-21T17:00:00+00:00","value":220.8},{"at":"2026-09-21T17:15:00+00:00","value":223.97},{"at":"2026-09-21T17:30:00+00:00","value":251.23},{"at":"2026-09-21T17:45:00+00:00","value":275.9},{"at":"2026-09-21T18:00:00+00:00","value":251.3},{"at":"2026-09-21T18:15:00+00:00","value":250.28},{"at":"2026-09-21T18:30:00+00:00","value":243.48},{"at":"2026-09-21T18:45:00+00:00","value":219.04},{"at":"2026-09-21T19:00:00+00:00","value":232.28},{"at":"2026-09-21T19:15:00+00:00","value":218.15},{"at":"2026-09-21T19:30:00+00:00","value":213.93},{"at":"2026-09-21T19:45:00+00:00","value":206.68},{"at":"2026-09-21T20:00:00+00:00","value":216.0},{"at":"2026-09-21T20:15:00+00:00","value":204.58},{"at":"2026-09-21T20:30:00+00:00","value":206.08},{"at":"2026-09-21T20:45:00+00:00","value":196.23},{"at":"2026-09-21T21:00:00+00:00","value":197.98},{"at":"2026-09-21T21:15:00+00:00","value":184.14},{"at":"2026-09-21T21:30:00+00:00","value":186.58},{"at":"2026-09-21T21:45:00+00:00","value":172.11},{"at":"2026-09-21T22:00:00+00:00","value":189.97},{"at":"2026-09-21T22:15:00+00:00","value":183.05},{"at":"2026-09-21T22:30:00+00:00","value":176.66},{"at":"2026-09-21T22:45:00+00:00","value":175.81},{"at":"2026-09-21T23:00:00+00:00","value":177.29},{"at":"2026-09-21T23:15:00+00:00","value":174.96},{"at":"2026-09-21T23:30:00+00:00","value":176.55},{"at":"2026-09-21T23:45:00+00:00","value":175.61},{"at":"2026-09-22T00:00:00+00:00","value":175.89},{"at":"2026-09-22T00:15:00+00:00","value":174.39},{"at":"2026-09-22T00:30:00+00:00","value":172.41},{"at":"2026-09-22T00:45:00+00:00","value":171.52},{"at":"2026-09-22T01:00:00+00:00","value":173.57},{"at":"2026-09-22T01:15:00+00:00","value":170.91},{"at":"2026-09-22T01:30:00+00:00","value":170.42},{"at":"2026-09-22T01:45:00+00:00","value":171.42},{"at":"2026-09-22T02:00:00+00:00","value":172.65},{"at":"2026-09-22T02:15:00+00:00","value":172.33},{"at":"2026-09-22T02:30:00+00:00","value":174.19},{"at":"2026-09-22T02:45:00+00:00","value":180.34},{"at":"2026-09-22T03:00:00+00:00","value":167.7},{"at":"2026-09-22T03:15:00+00:00","value":180.53},{"at":"2026-09-22T03:30:00+00:00","value":193.44},{"at":"2026-09-22T03:45:00+00:00","value":224.33},{"at":"2026-09-22T04:00:00+00:00","value":198.34},{"at":"2026-09-22T04:15:00+00:00","value":225.83},{"at":"2026-09-22T04:30:00+00:00","value":253.32},{"at":"2026-09-22T04:45:00+00:00","value":277.03},{"at":"2026-09-22T05:00:00+00:00","value":289.86},{"at":"2026-09-22T05:15:00+00:00","value":302.05},{"at":"2026-09-22T05:30:00+00:00","value":293.4},{"at":"2026-09-22T05:45:00+00:00","value":276.47},{"at":"2026-09-22T06:00:00+00:00","value":282.29},{"at":"2026-09-22T06:15:00+00:00","value":268.06},{"at":"2026-09-22T06:30:00+00:00","value":240.76},{"at":"2026-09-22T06:45:00+00:00","value":204.98},{"at":"2026-09-22T07:00:00+00:00","value":247.86},{"at":"2026-09-22T07:15:00+00:00","value":217.86},{"at":"2026-09-22T07:30:00+00:00","value":191.48},{"at":"2026-09-22T07:45:00+00:00","value":166.18},{"at":"2026-09-22T08:00:00+00:00","value":186.02},{"at":"2026-09-22T08:15:00+00:00","value":173.99},{"at":"2026-09-22T08:30:00+00:00","value":167.25},{"at":"2026-09-22T08:45:00+00:00","value":161.83},{"at":"2026-09-22T09:00:00+00:00","value":162.63},{"at":"2026-09-22T09:15:00+00:00","value":151.03},{"at":"2026-09-22T09:30:00+00:00","value":144.7},{"at":"2026-09-22T09:45:00+00:00","value":135.85},{"at":"2026-09-22T10:00:00+00:00","value":128.76},{"at":"2026-09-22T10:15:00+00:00","value":130.54},{"at":"2026-09-22T10:30:00+00:00","value":125.51},{"at":"2026-09-22T10:45:00+00:00","value":118.22},{"at":"2026-09-22T11:00:00+00:00","value":119.31},{"at":"2026-09-22T11:15:00+00:00","value":117.72},{"at":"2026-09-22T11:30:00+00:00","value":114.92},{"at":"2026-09-22T11:45:00+00:00","value":112.14},{"at":"2026-09-22T12:00:00+00:00","value":115.15},{"at":"2026-09-22T12:15:00+00:00","value":119.39},{"at":"2026-09-22T12:30:00+00:00","value":119.08},{"at":"2026-09-22T12:45:00+00:00","value":122.93},{"at":"2026-09-22T13:00:00+00:00","value":124.89},{"at":"2026-09-22T13:15:00+00:00","value":130.22},{"at":"2026-09-22T13:30:00+00:00","value":139.62},{"at":"2026-09-22T13:45:00+00:00","value":151.71},{"at":"2026-09-22T14:00:00+00:00","value":147.3},{"at":"2026-09-22T14:15:00+00:00","value":161.28},{"at":"2026-09-22T14:30:00+00:00","value":185.78},{"at":"2026-09-22T14:45:00+00:00","value":213.13},{"at":"2026-09-22T15:00:00+00:00","value":164.68},{"at":"2026-09-22T15:15:00+00:00","value":211.86},{"at":"2026-09-22T15:30:00+00:00","value":241.96},{"at":"2026-09-22T15:45:00+00:00","value":289.06},{"at":"2026-09-22T16:00:00+00:00","value":253.0},{"at":"2026-09-22T16:15:00+00:00","value":317.94},{"at":"2026-09-22T16:30:00+00:00","value":417.93},{"at":"2026-09-22T16:45:00+00:00","value":510.34},{"at":"2026-09-22T17:00:00+00:00","value":564.09},{"at":"2026-09-22T17:15:00+00:00","value":647.5},{"at":"2026-09-22T17:30:00+00:00","value":640.67},{"at":"2026-09-22T17:45:00+00:00","value":533.26},{"at":"2026-09-22T18:00:00+00:00","value":543.39},{"at":"2026-09-22T18:15:00+00:00","value":442.38},{"at":"2026-09-22T18:30:00+00:00","value":389.22},{"at":"2026-09-22T18:45:00+00:00","value":357.66},{"at":"2026-09-22T19:00:00+00:00","value":315.72},{"at":"2026-09-22T19:15:00+00:00","value":292.8},{"at":"2026-09-22T19:30:00+00:00","value":291.88},{"at":"2026-09-22T19:45:00+00:00","value":256.14},{"at":"2026-09-22T20:00:00+00:00","value":258.79},{"at":"2026-09-22T20:15:00+00:00","value":252.99},{"at":"2026-09-22T20:30:00+00:00","value":249.35},{"at":"2026-09-22T20:45:00+00:00","value":225.58},{"at":"2026-09-22T21:00:00+00:00","value":226.09},{"at":"2026-09-22T21:15:00+00:00","value":214.54},{"at":"2026-09-22T21:30:00+00:00","value":210.21},{"at":"2026-09-22T21:45:00+00:00","value":201.18},{"at":"2026-09-22T22:00:00+00:00","value":194.51},{"at":"2026-09-22T22:15:00+00:00","value":188.57},{"at":"2026-09-22T22:30:00+00:00","value":190.3},{"at":"2026-09-22T22:45:00+00:00","value":182.46},{"at":"2026-09-22T23:00:00+00:00","value":181.76},{"at":"2026-09-22T23:15:00+00:00","value":174.93},{"at":"2026-09-22T23:30:00+00:00","value":173.68},{"at":"2026-09-22T23:45:00+00:00","value":179.0},{"at":"2026-09-23T00:00:00+00:00","value":174.52},{"at":"2026-09-23T00:15:00+00:00","value":171.11},{"at":"2026-09-23T00:30:00+00:00","value":177.24},{"at":"2026-09-23T00:45:00+00:00","value":183.06},{"at":"2026-09-23T01:00:00+00:00","value":176.72},{"at":"2026-09-23T01:15:00+00:00","value":178.53},{"at":"2026-09-23T01:30:00+00:00","value":178.72},{"at":"2026-09-23T01:45:00+00:00","value":173.43},{"at":"2026-09-23T02:00:00+00:00","value":173.39},{"at":"2026-09-23T02:15:00+00:00","value":178.13},{"at":"2026-09-23T02:30:00+00:00","value":178.35},{"at":"2026-09-23T02:45:00+00:00","value":173.94},{"at":"2026-09-23T03:00:00+00:00","value":171.61},{"at":"2026-09-23T03:15:00+00:00","value":188.0},{"at":"2026-09-23T03:30:00+00:00","value":202.0},{"at":"2026-09-23T03:45:00+00:00","value":232.86},{"at":"2026-09-23T04:00:00+00:00","value":236.07},{"at":"2026-09-23T04:15:00+00:00","value":260.63},{"at":"2026-09-23T04:30:00+00:00","value":355.5},{"at":"2026-09-23T04:45:00+00:00","value":347.79},{"at":"2026-09-23T05:00:00+00:00","value":370.63},{"at":"2026-09-23T05:15:00+00:00","value":385.35},{"at":"2026-09-23T05:30:00+00:00","value":348.25},{"at":"2026-09-23T05:45:00+00:00","value":280.09},{"at":"2026-09-23T06:00:00+00:00","value":274.32},{"at":"2026-09-23T06:15:00+00:00","value":240.5},{"at":"2026-09-23T06:30:00+00:00","value":224.31},{"at":"2026-09-23T06:45:00+00:00","value":189.12},{"at":"2026-09-23T07:00:00+00:00","value":217.94},{"at":"2026-09-23T07:15:00+00:00","value":193.88},{"at":"2026-09-23T07:30:00+00:00","value":170.82},{"at":"2026-09-23T07:45:00+00:00","value":146.46},{"at":"2026-09-23T08:00:00+00:00","value":166.24},{"at":"2026-09-23T08:15:00+00:00","value":148.1},{"at":"2026-09-23T08:30:00+00:00","value":134.95},{"at":"2026-09-23T08:45:00+00:00","value":116.12},{"at":"2026-09-23T09:00:00+00:00","value":119.82},{"at":"2026-09-23T09:15:00+00:00","value":107.13},{"at":"2026-09-23T09:30:00+00:00","value":86.82},{"at":"2026-09-23T09:45:00+00:00","value":75.87},{"at":"2026-09-23T10:00:00+00:00","value":85.87},{"at":"2026-09-23T10:15:00+00:00","value":73.37},{"at":"2026-09-23T10:30:00+00:00","value":69.72},{"at":"2026-09-23T10:45:00+00:00","value":63.26},{"at":"2026-09-23T11:00:00+00:00","value":64.74},{"at":"2026-09-23T11:15:00+00:00","value":60.02},{"at":"2026-09-23T11:30:00+00:00","value":55.07},{"at":"2026-09-23T11:45:00+00:00","value":49.47},{"at":"2026-09-23T12:00:00+00:00","value":41.99},{"at":"2026-09-23T12:15:00+00:00","value":64.85},{"at":"2026-09-23T12:30:00+00:00","value":85.33},{"at":"2026-09-23T12:45:00+00:00","value":108.18},{"at":"2026-09-23T13:00:00+00:00","value":72.09},{"at":"2026-09-23T13:15:00+00:00","value":101.31},{"at":"2026-09-23T13:30:00+00:00","value":126.3},{"at":"2026-09-23T13:45:00+00:00","value":141.93},{"at":"2026-09-23T14:00:00+00:00","value":124.17},{"at":"2026-09-23T14:15:00+00:00","value":148.07},{"at":"2026-09-23T14:30:00+00:00","value":165.54},{"at":"2026-09-23T14:45:00+00:00","value":189.45},{"at":"2026-09-23T15:00:00+00:00","value":158.94},{"at":"2026-09-23T15:15:00+00:00","value":186.1},{"at":"2026-09-23T15:30:00+00:00","value":211.46},{"at":"2026-09-23T15:45:00+00:00","value":239.54},{"at":"2026-09-23T16:00:00+00:00","value":206.0},{"at":"2026-09-23T16:15:00+00:00","value":225.83},{"at":"2026-09-23T16:30:00+00:00","value":267.94},{"at":"2026-09-23T16:45:00+00:00","value":275.11},{"at":"2026-09-23T17:00:00+00:00","value":271.83},{"at":"2026-09-23T17:15:00+00:00","value":257.33},{"at":"2026-09-23T17:30:00+00:00","value":272.89},{"at":"2026-09-23T17:45:00+00:00","value":284.31},{"at":"2026-09-23T18:00:00+00:00","value":262.21},{"at":"2026-09-23T18:15:00+00:00","value":249.7},{"at":"2026-09-23T18:30:00+00:00","value":223.83},{"at":"2026-09-23T18:45:00+00:00","value":210.76},{"at":"2026-09-23T19:00:00+00:00","value":213.26},{"at":"2026-09-23T19:15:00+00:00","value":205.96},{"at":"2026-09-23T19:30:00+00:00","value":190.73},{"at":"2026-09-23T19:45:00+00:00","value":170.84},{"at":"2026-09-23T20:00:00+00:00","value":182.87},{"at":"2026-09-23T20:15:00+00:00","value":170.36},{"at":"2026-09-23T20:30:00+00:00","value":165.74},{"at":"2026-09-23T20:45:00+00:00","value":161.5},{"at":"2026-09-23T21:00:00+00:00","value":166.95},{"at":"2026-09-23T21:15:00+00:00","value":154.16},{"at":"2026-09-23T21:30:00+00:00","value":150.68},{"at":"2026-09-23T21:45:00+00:00","value":144.2},{"at":"2026-09-23T22:00:00+00:00","value":124.78},{"at":"2026-09-23T22:15:00+00:00","value":136.68},{"at":"2026-09-23T22:30:00+00:00","value":130.6},{"at":"2026-09-23T22:45:00+00:00","value":129.4},{"at":"2026-09-23T23:00:00+00:00","value":121.01},{"at":"2026-09-23T23:15:00+00:00","value":118.29},{"at":"2026-09-23T23:30:00+00:00","value":119.7},{"at":"2026-09-23T23:45:00+00:00","value":116.49},{"at":"2026-09-24T00:00:00+00:00","value":117.38},{"at":"2026-09-24T00:15:00+00:00","value":114.96},{"at":"2026-09-24T00:30:00+00:00","value":114.36},{"at":"2026-09-24T00:45:00+00:00","value":111.35},{"at":"2026-09-24T01:00:00+00:00","value":109.27},{"at":"2026-09-24T01:15:00+00:00","value":107.97},{"at":"2026-09-24T01:30:00+00:00","value":106.5},{"at":"2026-09-24T01:45:00+00:00","value":104.39},{"at":"2026-09-24T02:00:00+00:00","value":106.36},{"at":"2026-09-24T02:15:00+00:00","value":106.43},{"at":"2026-09-24T02:30:00+00:00","value":105.65},{"at":"2026-09-24T02:45:00+00:00","value":110.85},{"at":"2026-09-24T03:00:00+00:00","value":118.13},{"at":"2026-09-24T03:15:00+00:00","value":118.67},{"at":"2026-09-24T03:30:00+00:00","value":121.55},{"at":"2026-09-24T03:45:00+00:00","value":128.45},{"at":"2026-09-24T04:00:00+00:00","value":123.98},{"at":"2026-09-24T04:15:00+00:00","value":142.78},{"at":"2026-09-24T04:30:00+00:00","value":156.71},{"at":"2026-09-24T04:45:00+00:00","value":167.77},{"at":"2026-09-24T05:00:00+00:00","value":161.37},{"at":"2026-09-24T05:15:00+00:00","value":167.17},{"at":"2026-09-24T05:30:00+00:00","value":172.69},{"at":"2026-09-24T05:45:00+00:00","value":170.83},{"at":"2026-09-24T06:00:00+00:00","value":185.99},{"at":"2026-09-24T06:15:00+00:00","value":175.9},{"at":"2026-09-24T06:30:00+00:00","value":172.6},{"at":"2026-09-24T06:45:00+00:00","value":160.57},{"at":"2026-09-24T07:00:00+00:00","value":172.79},{"at":"2026-09-24T07:15:00+00:00","value":162.39},{"at":"2026-09-24T07:30:00+00:00","value":144.42},{"at":"2026-09-24T07:45:00+00:00","value":130.04},{"at":"2026-09-24T08:00:00+00:00","value":136.4},{"at":"2026-09-24T08:15:00+00:00","value":122.77},{"at":"2026-09-24T08:30:00+00:00","value":106.24},{"at":"2026-09-24T08:45:00+00:00","value":81.51},{"at":"2026-09-24T09:00:00+00:00","value":98.66},{"at":"2026-09-24T09:15:00+00:00","value":78.86},{"at":"2026-09-24T09:30:00+00:00","value":60.02},{"at":"2026-09-24T09:45:00+00:00","value":36.1},{"at":"2026-09-24T10:00:00+00:00","value":25.01},{"at":"2026-09-24T10:15:00+00:00","value":15.11},{"at":"2026-09-24T10:30:00+00:00","value":13.88},{"at":"2026-09-24T10:45:00+00:00","value":10.0},{"at":"2026-09-24T11:00:00+00:00","value":14.0},{"at":"2026-09-24T11:15:00+00:00","value":10.03},{"at":"2026-09-24T11:30:00+00:00","value":12.32},{"at":"2026-09-24T11:45:00+00:00","value":10.05},{"at":"2026-09-24T12:00:00+00:00","value":8.86},{"at":"2026-09-24T12:15:00+00:00","value":10.9},{"at":"2026-09-24T12:30:00+00:00","value":24.0},{"at":"2026-09-24T12:45:00+00:00","value":34.99},{"at":"2026-09-24T13:00:00+00:00","value":38.66},{"at":"2026-09-24T13:15:00+00:00","value":61.86},{"at":"2026-09-24T13:30:00+00:00","value":95.0},{"at":"2026-09-24T13:45:00+00:00","value":108.0},{"at":"2026-09-24T14:00:00+00:00","value":76.9},{"at":"2026-09-24T14:15:00+00:00","value":108.86},{"at":"2026-09-24T14:30:00+00:00","value":132.15},{"at":"2026-09-24T14:45:00+00:00","value":152.8},{"at":"2026-09-24T15:00:00+00:00","value":141.6},{"at":"2026-09-24T15:15:00+00:00","value":170.89},{"at":"2026-09-24T15:30:00+00:00","value":193.19},{"at":"2026-09-24T15:45:00+00:00","value":214.43},{"at":"2026-09-24T16:00:00+00:00","value":186.47},{"at":"2026-09-24T16:15:00+00:00","value":218.93},{"at":"2026-09-24T16:30:00+00:00","value":236.02},{"at":"2026-09-24T16:45:00+00:00","value":262.74},{"at":"2026-09-24T17:00:00+00:00","value":249.33},{"at":"2026-09-24T17:15:00+00:00","value":263.79},{"at":"2026-09-24T17:30:00+00:00","value":267.94},{"at":"2026-09-24T17:45:00+00:00","value":288.23},{"at":"2026-09-24T18:00:00+00:00","value":272.65},{"at":"2026-09-24T18:15:00+00:00","value":265.8},{"at":"2026-09-24T18:30:00+00:00","value":253.5},{"at":"2026-09-24T18:45:00+00:00","value":248.05},{"at":"2026-09-24T19:00:00+00:00","value":240.29},{"at":"2026-09-24T19:15:00+00:00","value":230.0},{"at":"2026-09-24T19:30:00+00:00","value":223.38},{"at":"2026-09-24T19:45:00+00:00","value":209.62},{"at":"2026-09-24T20:00:00+00:00","value":220.96},{"at":"2026-09-24T20:15:00+00:00","value":204.52},{"at":"2026-09-24T20:30:00+00:00","value":201.0},{"at":"2026-09-24T20:45:00+00:00","value":192.99},{"at":"2026-09-24T21:00:00+00:00","value":196.93},{"at":"2026-09-24T21:15:00+00:00","value":188.32},{"at":"2026-09-24T21:30:00+00:00","value":185.64},{"at":"2026-09-24T21:45:00+00:00","value":181.14},{"at":"2026-09-24T22:00:00+00:00","value":196.99},{"at":"2026-09-24T22:15:00+00:00","value":184.4},{"at":"2026-09-24T22:30:00+00:00","value":175.79},{"at":"2026-09-24T22:45:00+00:00","value":170.59},{"at":"2026-09-24T23:00:00+00:00","value":175.13},{"at":"2026-09-24T23:15:00+00:00","value":171.84},{"at":"2026-09-24T23:30:00+00:00","value":171.43},{"at":"2026-09-24T23:45:00+00:00","value":170.27},{"at":"2026-09-25T00:00:00+00:00","value":167.76},{"at":"2026-09-25T00:15:00+00:00","value":166.49},{"at":"2026-09-25T00:30:00+00:00","value":165.93},{"at":"2026-09-25T00:45:00+00:00","value":162.38},{"at":"2026-09-25T01:00:00+00:00","value":164.46},{"at":"2026-09-25T01:15:00+00:00","value":165.55},{"at":"2026-09-25T01:30:00+00:00","value":169.18},{"at":"2026-09-25T01:45:00+00:00","value":169.27},{"at":"2026-09-25T02:00:00+00:00","value":172.29},{"at":"2026-09-25T02:15:00+00:00","value":170.87},{"at":"2026-09-25T02:30:00+00:00","value":169.82},{"at":"2026-09-25T02:45:00+00:00","value":165.87},{"at":"2026-09-25T03:00:00+00:00","value":168.41},{"at":"2026-09-25T03:15:00+00:00","value":169.79},{"at":"2026-09-25T03:30:00+00:00","value":192.29},{"at":"2026-09-25T03:45:00+00:00","value":221.15},{"at":"2026-09-25T04:00:00+00:00","value":204.38},{"at":"2026-09-25T04:15:00+00:00","value":236.08},{"at":"2026-09-25T04:30:00+00:00","value":236.44},{"at":"2026-09-25T04:45:00+00:00","value":264.16},{"at":"2026-09-25T05:00:00+00:00","value":252.93},{"at":"2026-09-25T05:15:00+00:00","value":266.66},{"at":"2026-09-25T05:30:00+00:00","value":273.61},{"at":"2026-09-25T05:45:00+00:00","value":252.41},{"at":"2026-09-25T06:00:00+00:00","value":290.87},{"at":"2026-09-25T06:15:00+00:00","value":260.69},{"at":"2026-09-25T06:30:00+00:00","value":243.4},{"at":"2026-09-25T06:45:00+00:00","value":203.99},{"at":"2026-09-25T07:00:00+00:00","value":235.46},{"at":"2026-09-25T07:15:00+00:00","value":202.74},{"at":"2026-09-25T07:30:00+00:00","value":189.27},{"at":"2026-09-25T07:45:00+00:00","value":157.5},{"at":"2026-09-25T08:00:00+00:00","value":182.5},{"at":"2026-09-25T08:15:00+00:00","value":165.0},{"at":"2026-09-25T08:30:00+00:00","value":148.66},{"at":"2026-09-25T08:45:00+00:00","value":137.99},{"at":"2026-09-25T09:00:00+00:00","value":137.82},{"at":"2026-09-25T09:15:00+00:00","value":123.02},{"at":"2026-09-25T09:30:00+00:00","value":100.36},{"at":"2026-09-25T09:45:00+00:00","value":72.42},{"at":"2026-09-25T10:00:00+00:00","value":85.78},{"at":"2026-09-25T10:15:00+00:00","value":62.83},{"at":"2026-09-25T10:30:00+00:00","value":49.38},{"at":"2026-09-25T10:45:00+00:00","value":42.75},{"at":"2026-09-25T11:00:00+00:00","value":39.01},{"at":"2026-09-25T11:15:00+00:00","value":36.12},{"at":"2026-09-25T11:30:00+00:00","value":26.14},{"at":"2026-09-25T11:45:00+00:00","value":19.17},{"at":"2026-09-25T12:00:00+00:00","value":23.12},{"at":"2026-09-25T12:15:00+00:00","value":35.0},{"at":"2026-09-25T12:30:00+00:00","value":39.94},{"at":"2026-09-25T12:45:00+00:00","value":61.49},{"at":"2026-09-25T13:00:00+00:00","value":40.0},{"at":"2026-09-25T13:15:00+00:00","value":73.58},{"at":"2026-09-25T13:30:00+00:00","value":107.83},{"at":"2026-09-25T13:45:00+00:00","value":126.76},{"at":"2026-09-25T14:00:00+00:00","value":119.91},{"at":"2026-09-25T14:15:00+00:00","value":142.44},{"at":"2026-09-25T14:30:00+00:00","value":165.0},{"at":"2026-09-25T14:45:00+00:00","value":190.71},{"at":"2026-09-25T15:00:00+00:00","value":157.71},{"at":"2026-09-25T15:15:00+00:00","value":192.8},{"at":"2026-09-25T15:30:00+00:00","value":206.21},{"at":"2026-09-25T15:45:00+00:00","value":239.26},{"at":"2026-09-25T16:00:00+00:00","value":202.24},{"at":"2026-09-25T16:15:00+00:00","value":230.0},{"at":"2026-09-25T16:30:00+00:00","value":248.72},{"at":"2026-09-25T16:45:00+00:00","value":284.74},{"at":"2026-09-25T17:00:00+00:00","value":291.76},{"at":"2026-09-25T17:15:00+00:00","value":305.47},{"at":"2026-09-25T17:30:00+00:00","value":315.78},{"at":"2026-09-25T17:45:00+00:00","value":300.7},{"at":"2026-09-25T18:00:00+00:00","value":270.0},{"at":"2026-09-25T18:15:00+00:00","value":255.0},{"at":"2026-09-25T18:30:00+00:00","value":246.96},{"at":"2026-09-25T18:45:00+00:00","value":236.7},{"at":"2026-09-25T19:00:00+00:00","value":244.18},{"at":"2026-09-25T19:15:00+00:00","value":231.25},{"at":"2026-09-25T19:30:00+00:00","value":218.38},{"at":"2026-09-25T19:45:00+00:00","value":202.89},{"at":"2026-09-25T20:00:00+00:00","value":219.99},{"at":"2026-09-25T20:15:00+00:00","value":208.59},{"at":"2026-09-25T20:30:00+00:00","value":202.11},{"at":"2026-09-25T20:45:00+00:00","value":194.72},{"at":"2026-09-25T21:00:00+00:00","value":199.81},{"at":"2026-09-25T21:15:00+00:00","value":193.53},{"at":"2026-09-25T21:30:00+00:00","value":182.41},{"at":"2026-09-25T21:45:00+00:00","value":171.29},{"at":"2026-09-25T22:00:00+00:00","value":205.94},{"at":"2026-09-25T22:15:00+00:00","value":199.14},{"at":"2026-09-25T22:30:00+00:00","value":194.54},{"at":"2026-09-25T22:45:00+00:00","value":185.56},{"at":"2026-09-25T23:00:00+00:00","value":187.85},{"at":"2026-09-25T23:15:00+00:00","value":184.4},{"at":"2026-09-25T23:30:00+00:00","value":182.86},{"at":"2026-09-25T23:45:00+00:00","value":181.02},{"at":"2026-09-26T00:00:00+00:00","value":181.33},{"at":"2026-09-26T00:15:00+00:00","value":179.17},{"at":"2026-09-26T00:30:00+00:00","value":173.17},{"at":"2026-09-26T00:45:00+00:00","value":166.7},{"at":"2026-09-26T01:00:00+00:00","value":165.93},{"at":"2026-09-26T01:15:00+00:00","value":163.25},{"at":"2026-09-26T01:30:00+00:00","value":162.56},{"at":"2026-09-26T01:45:00+00:00","value":162.47},{"at":"2026-09-26T02:00:00+00:00","value":159.61},{"at":"2026-09-26T02:15:00+00:00","value":160.35},{"at":"2026-09-26T02:30:00+00:00","value":161.3},{"at":"2026-09-26T02:45:00+00:00","value":161.76},{"at":"2026-09-26T03:00:00+00:00","value":159.09},{"at":"2026-09-26T03:15:00+00:00","value":158.03},{"at":"2026-09-26T03:30:00+00:00","value":160.44},{"at":"2026-09-26T03:45:00+00:00","value":164.62},{"at":"2026-09-26T04:00:00+00:00","value":167.7},{"at":"2026-09-26T04:15:00+00:00","value":176.77},{"at":"2026-09-26T04:30:00+00:00","value":181.6},{"at":"2026-09-26T04:45:00+00:00","value":188.88},{"at":"2026-09-26T05:00:00+00:00","value":192.05},{"at":"2026-09-26T05:15:00+00:00","value":194.29},{"at":"2026-09-26T05:30:00+00:00","value":194.14},{"at":"2026-09-26T05:45:00+00:00","value":196.76},{"at":"2026-09-26T06:00:00+00:00","value":210.93},{"at":"2026-09-26T06:15:00+00:00","value":203.0},{"at":"2026-09-26T06:30:00+00:00","value":187.34},{"at":"2026-09-26T06:45:00+00:00","value":166.4},{"at":"2026-09-26T07:00:00+00:00","value":193.17},{"at":"2026-09-26T07:15:00+00:00","value":165.98},{"at":"2026-09-26T07:30:00+00:00","value":139.03},{"at":"2026-09-26T07:45:00+00:00","value":127.59},{"at":"2026-09-26T08:00:00+00:00","value":132.41},{"at":"2026-09-26T08:15:00+00:00","value":120.56},{"at":"2026-09-26T08:30:00+00:00","value":104.99},{"at":"2026-09-26T08:45:00+00:00","value":90.0},{"at":"2026-09-26T09:00:00+00:00","value":78.49},{"at":"2026-09-26T09:15:00+00:00","value":59.07},{"at":"2026-09-26T09:30:00+00:00","value":46.32},{"at":"2026-09-26T09:45:00+00:00","value":28.53},{"at":"2026-09-26T10:00:00+00:00","value":17.33},{"at":"2026-09-26T10:15:00+00:00","value":12.51},{"at":"2026-09-26T10:30:00+00:00","value":9.47},{"at":"2026-09-26T10:45:00+00:00","value":4.71},{"at":"2026-09-26T11:00:00+00:00","value":4.64},{"at":"2026-09-26T11:15:00+00:00","value":3.73},{"at":"2026-09-26T11:30:00+00:00","value":2.43},{"at":"2026-09-26T11:45:00+00:00","value":2.42},{"at":"2026-09-26T12:00:00+00:00","value":9.02},{"at":"2026-09-26T12:15:00+00:00","value":12.51},{"at":"2026-09-26T12:30:00+00:00","value":23.3},{"at":"2026-09-26T12:45:00+00:00","value":28.97},{"at":"2026-09-26T13:00:00+00:00","value":23.0},{"at":"2026-09-26T13:15:00+00:00","value":40.0},{"at":"2026-09-26T13:30:00+00:00","value":59.82},{"at":"2026-09-26T13:45:00+00:00","value":83.28},{"at":"2026-09-26T14:00:00+00:00","value":91.58},{"at":"2026-09-26T14:15:00+00:00","value":122.8},{"at":"2026-09-26T14:30:00+00:00","value":135.09},{"at":"2026-09-26T14:45:00+00:00","value":160.1},{"at":"2026-09-26T15:00:00+00:00","value":154.56},{"at":"2026-09-26T15:15:00+00:00","value":194.8},{"at":"2026-09-26T15:30:00+00:00","value":215.13},{"at":"2026-09-26T15:45:00+00:00","value":203.04},{"at":"2026-09-26T16:00:00+00:00","value":196.0},{"at":"2026-09-26T16:15:00+00:00","value":206.37},{"at":"2026-09-26T16:30:00+00:00","value":220.86},{"at":"2026-09-26T16:45:00+00:00","value":234.23},{"at":"2026-09-26T17:00:00+00:00","value":222.0},{"at":"2026-09-26T17:15:00+00:00","value":230.46},{"at":"2026-09-26T17:30:00+00:00","value":243.61},{"at":"2026-09-26T17:45:00+00:00","value":251.08},{"at":"2026-09-26T18:00:00+00:00","value":238.97},{"at":"2026-09-26T18:15:00+00:00","value":232.0},{"at":"2026-09-26T18:30:00+00:00","value":222.48},{"at":"2026-09-26T18:45:00+00:00","value":211.99},{"at":"2026-09-26T19:00:00+00:00","value":218.18},{"at":"2026-09-26T19:15:00+00:00","value":210.24},{"at":"2026-09-26T19:30:00+00:00","value":205.53},{"at":"2026-09-26T19:45:00+00:00","value":200.0},{"at":"2026-09-26T20:00:00+00:00","value":207.0},{"at":"2026-09-26T20:15:00+00:00","value":200.62},{"at":"2026-09-26T20:30:00+00:00","value":197.73},{"at":"2026-09-26T20:45:00+00:00","value":191.89},{"at":"2026-09-26T21:00:00+00:00","value":195.2},{"at":"2026-09-26T21:15:00+00:00","value":188.45},{"at":"2026-09-26T21:30:00+00:00","value":182.55},{"at":"2026-09-26T21:45:00+00:00","value":177.8},{"at":"2026-09-26T22:00:00+00:00","value":192.07},{"at":"2026-09-26T22:15:00+00:00","value":185.95},{"at":"2026-09-26T22:30:00+00:00","value":182.68},{"at":"2026-09-26T22:45:00+00:00","value":172.18},{"at":"2026-09-26T23:00:00+00:00","value":180.47},{"at":"2026-09-26T23:15:00+00:00","value":178.0},{"at":"2026-09-26T23:30:00+00:00","value":176.62},{"at":"2026-09-26T23:45:00+00:00","value":178.0},{"at":"2026-09-27T00:00:00+00:00","value":176.0},{"at":"2026-09-27T00:15:00+00:00","value":171.31},{"at":"2026-09-27T00:30:00+00:00","value":169.97},{"at":"2026-09-27T00:45:00+00:00","value":168.08},{"at":"2026-09-27T01:00:00+00:00","value":168.16},{"at":"2026-09-27T01:15:00+00:00","value":166.78},{"at":"2026-09-27T01:30:00+00:00","value":165.4},{"at":"2026-09-27T01:45:00+00:00","value":165.39},{"at":"2026-09-27T02:00:00+00:00","value":165.0},{"at":"2026-09-27T02:15:00+00:00","value":160.83},{"at":"2026-09-27T02:30:00+00:00","value":160.44},{"at":"2026-09-27T02:45:00+00:00","value":160.0},{"at":"2026-09-27T03:00:00+00:00","value":160.44},{"at":"2026-09-27T03:15:00+00:00","value":158.08},{"at":"2026-09-27T03:30:00+00:00","value":159.4},{"at":"2026-09-27T03:45:00+00:00","value":156.76},{"at":"2026-09-27T04:00:00+00:00","value":156.03},{"at":"2026-09-27T04:15:00+00:00","value":156.05},{"at":"2026-09-27T04:30:00+00:00","value":162.42},{"at":"2026-09-27T04:45:00+00:00","value":162.85},{"at":"2026-09-27T05:00:00+00:00","value":165.56},{"at":"2026-09-27T05:15:00+00:00","value":157.95},{"at":"2026-09-27T05:30:00+00:00","value":146.68},{"at":"2026-09-27T05:45:00+00:00","value":134.63},{"at":"2026-09-27T06:00:00+00:00","value":160.43},{"at":"2026-09-27T06:15:00+00:00","value":143.86},{"at":"2026-09-27T06:30:00+00:00","value":119.48},{"at":"2026-09-27T06:45:00+00:00","value":87.03},{"at":"2026-09-27T07:00:00+00:00","value":101.36},{"at":"2026-09-27T07:15:00+00:00","value":76.32},{"at":"2026-09-27T07:30:00+00:00","value":30.96},{"at":"2026-09-27T07:45:00+00:00","value":18.32},{"at":"2026-09-27T08:00:00+00:00","value":5.51},{"at":"2026-09-27T08:15:00+00:00","value":0.06},{"at":"2026-09-27T08:30:00+00:00","value":0.0},{"at":"2026-09-27T08:45:00+00:00","value":0.0},{"at":"2026-09-27T09:00:00+00:00","value":0.0},{"at":"2026-09-27T09:15:00+00:00","value":-0.01},{"at":"2026-09-27T09:30:00+00:00","value":-0.09},{"at":"2026-09-27T09:45:00+00:00","value":-0.19},{"at":"2026-09-27T10:00:00+00:00","value":-1.01},{"at":"2026-09-27T10:15:00+00:00","value":-1.76},{"at":"2026-09-27T10:30:00+00:00","value":-2.02},{"at":"2026-09-27T10:45:00+00:00","value":-2.99},{"at":"2026-09-27T11:00:00+00:00","value":-2.21},{"at":"2026-09-27T11:15:00+00:00","value":-2.95},{"at":"2026-09-27T11:30:00+00:00","value":-2.76},{"at":"2026-09-27T11:45:00+00:00","value":-2.02},{"at":"2026-09-27T12:00:00+00:00","value":-2.0},{"at":"2026-09-27T12:15:00+00:00","value":-1.02},{"at":"2026-09-27T12:30:00+00:00","value":-0.21},{"at":"2026-09-27T12:45:00+00:00","value":-0.12},{"at":"2026-09-27T13:00:00+00:00","value":-0.01},{"at":"2026-09-27T13:15:00+00:00","value":-0.01},{"at":"2026-09-27T13:30:00+00:00","value":0.0},{"at":"2026-09-27T13:45:00+00:00","value":0.0},{"at":"2026-09-27T14:00:00+00:00","value":0.0},{"at":"2026-09-27T14:15:00+00:00","value":0.15},{"at":"2026-09-27T14:30:00+00:00","value":7.01},{"at":"2026-09-27T14:45:00+00:00","value":45.25},{"at":"2026-09-27T15:00:00+00:00","value":41.25},{"at":"2026-09-27T15:15:00+00:00","value":92.71},{"at":"2026-09-27T15:30:00+00:00","value":144.61},{"at":"2026-09-27T15:45:00+00:00","value":178.48},{"at":"2026-09-27T16:00:00+00:00","value":168.79},{"at":"2026-09-27T16:15:00+00:00","value":188.35},{"at":"2026-09-27T16:30:00+00:00","value":193.27},{"at":"2026-09-27T16:45:00+00:00","value":194.45},{"at":"2026-09-27T17:00:00+00:00","value":190.84},{"at":"2026-09-27T17:15:00+00:00","value":191.93},{"at":"2026-09-27T17:30:00+00:00","value":198.95},{"at":"2026-09-27T17:45:00+00:00","value":201.28},{"at":"2026-09-27T18:00:00+00:00","value":194.32},{"at":"2026-09-27T18:15:00+00:00","value":188.0},{"at":"2026-09-27T18:30:00+00:00","value":185.68},{"at":"2026-09-27T18:45:00+00:00","value":167.39},{"at":"2026-09-27T19:00:00+00:00","value":174.16},{"at":"2026-09-27T19:15:00+00:00","value":164.44},{"at":"2026-09-27T19:30:00+00:00","value":151.86},{"at":"2026-09-27T19:45:00+00:00","value":148.56},{"at":"2026-09-27T20:00:00+00:00","value":164.94},{"at":"2026-09-27T20:15:00+00:00","value":156.51},{"at":"2026-09-27T20:30:00+00:00","value":152.22},{"at":"2026-09-27T20:45:00+00:00","value":148.03},{"at":"2026-09-27T21:00:00+00:00","value":149.36},{"at":"2026-09-27T21:15:00+00:00","value":147.47},{"at":"2026-09-27T21:30:00+00:00","value":145.18},{"at":"2026-09-27T21:45:00+00:00","value":143.72},{"at":"2026-09-27T22:00:00+00:00","value":150.75},{"at":"2026-09-27T22:15:00+00:00","value":150.76},{"at":"2026-09-27T22:30:00+00:00","value":150.58},{"at":"2026-09-27T22:45:00+00:00","value":150.75},{"at":"2026-09-27T23:00:00+00:00","value":152.64},{"at":"2026-09-27T23:15:00+00:00","value":150.22},{"at":"2026-09-27T23:30:00+00:00","value":151.75},{"at":"2026-09-27T23:45:00+00:00","value":151.03},{"at":"2026-09-28T00:00:00+00:00","value":150.96},{"at":"2026-09-28T00:15:00+00:00","value":151.36},{"at":"2026-09-28T00:30:00+00:00","value":151.75},{"at":"2026-09-28T00:45:00+00:00","value":151.89},{"at":"2026-09-28T01:00:00+00:00","value":152.62},{"at":"2026-09-28T01:15:00+00:00","value":153.8},{"at":"2026-09-28T01:30:00+00:00","value":154.6},{"at":"2026-09-28T01:45:00+00:00","value":157.33},{"at":"2026-09-28T02:00:00+00:00","value":156.68},{"at":"2026-09-28T02:15:00+00:00","value":158.24},{"at":"2026-09-28T02:30:00+00:00","value":162.04},{"at":"2026-09-28T02:45:00+00:00","value":166.87},{"at":"2026-09-28T03:00:00+00:00","value":167.67},{"at":"2026-09-28T03:15:00+00:00","value":170.36},{"at":"2026-09-28T03:30:00+00:00","value":176.77},{"at":"2026-09-28T03:45:00+00:00","value":185.9},{"at":"2026-09-28T04:00:00+00:00","value":193.68},{"at":"2026-09-28T04:15:00+00:00","value":204.99},{"at":"2026-09-28T04:30:00+00:00","value":214.84},{"at":"2026-09-28T04:45:00+00:00","value":231.02},{"at":"2026-09-28T05:00:00+00:00","value":228.23},{"at":"2026-09-28T05:15:00+00:00","value":244.02},{"at":"2026-09-28T05:30:00+00:00","value":246.17},{"at":"2026-09-28T05:45:00+00:00","value":245.5},{"at":"2026-09-28T06:00:00+00:00","value":275.95},{"at":"2026-09-28T06:15:00+00:00","value":250.74},{"at":"2026-09-28T06:30:00+00:00","value":231.15},{"at":"2026-09-28T06:45:00+00:00","value":210.77},{"at":"2026-09-28T07:00:00+00:00","value":235.13},{"at":"2026-09-28T07:15:00+00:00","value":220.36},{"at":"2026-09-28T07:30:00+00:00","value":202.0},{"at":"2026-09-28T07:45:00+00:00","value":182.95},{"at":"2026-09-28T08:00:00+00:00","value":203.48},{"at":"2026-09-28T08:15:00+00:00","value":185.07},{"at":"2026-09-28T08:30:00+00:00","value":172.75},{"at":"2026-09-28T08:45:00+00:00","value":155.95},{"at":"2026-09-28T09:00:00+00:00","value":157.93},{"at":"2026-09-28T09:15:00+00:00","value":158.52},{"at":"2026-09-28T09:30:00+00:00","value":150.4},{"at":"2026-09-28T09:45:00+00:00","value":147.22},{"at":"2026-09-28T10:00:00+00:00","value":145.33},{"at":"2026-09-28T10:15:00+00:00","value":126.73},{"at":"2026-09-28T10:30:00+00:00","value":117.8},{"at":"2026-09-28T10:45:00+00:00","value":114.68},{"at":"2026-09-28T11:00:00+00:00","value":116.98},{"at":"2026-09-28T11:15:00+00:00","value":114.49},{"at":"2026-09-28T11:30:00+00:00","value":126.85},{"at":"2026-09-28T11:45:00+00:00","value":127.03},{"at":"2026-09-28T12:00:00+00:00","value":120.78},{"at":"2026-09-28T12:15:00+00:00","value":134.99},{"at":"2026-09-28T12:30:00+00:00","value":145.51},{"at":"2026-09-28T12:45:00+00:00","value":151.87},{"at":"2026-09-28T13:00:00+00:00","value":146.6},{"at":"2026-09-28T13:15:00+00:00","value":150.9},{"at":"2026-09-28T13:30:00+00:00","value":151.9},{"at":"2026-09-28T13:45:00+00:00","value":165.54},{"at":"2026-09-28T14:00:00+00:00","value":156.69},{"at":"2026-09-28T14:15:00+00:00","value":172.33},{"at":"2026-09-28T14:30:00+00:00","value":198.69},{"at":"2026-09-28T14:45:00+00:00","value":224.59},{"at":"2026-09-28T15:00:00+00:00","value":207.45},{"at":"2026-09-28T15:15:00+00:00","value":231.26},{"at":"2026-09-28T15:30:00+00:00","value":241.07},{"at":"2026-09-28T15:45:00+00:00","value":266.9},{"at":"2026-09-28T16:00:00+00:00","value":247.48},{"at":"2026-09-28T16:15:00+00:00","value":284.36},{"at":"2026-09-28T16:30:00+00:00","value":319.88},{"at":"2026-09-28T16:45:00+00:00","value":390.6},{"at":"2026-09-28T17:00:00+00:00","value":350.0},{"at":"2026-09-28T17:15:00+00:00","value":354.0},{"at":"2026-09-28T17:30:00+00:00","value":349.99},{"at":"2026-09-28T17:45:00+00:00","value":314.86},{"at":"2026-09-28T18:00:00+00:00","value":320.83},{"at":"2026-09-28T18:15:00+00:00","value":280.59},{"at":"2026-09-28T18:30:00+00:00","value":260.91},{"at":"2026-09-28T18:45:00+00:00","value":246.9},{"at":"2026-09-28T19:00:00+00:00","value":252.58},{"at":"2026-09-28T19:15:00+00:00","value":234.44},{"at":"2026-09-28T19:30:00+00:00","value":223.98},{"at":"2026-09-28T19:45:00+00:00","value":205.0},{"at":"2026-09-28T20:00:00+00:00","value":216.93},{"at":"2026-09-28T20:15:00+00:00","value":208.16},{"at":"2026-09-28T20:30:00+00:00","value":201.99},{"at":"2026-09-28T20:45:00+00:00","value":186.32},{"at":"2026-09-28T21:00:00+00:00","value":197.01},{"at":"2026-09-28T21:15:00+00:00","value":187.78},{"at":"2026-09-28T21:30:00+00:00","value":179.24},{"at":"2026-09-28T21:45:00+00:00","value":161.14},{"at":"2026-09-28T22:00:00+00:00","value":191.82},{"at":"2026-09-28T22:15:00+00:00","value":189.19},{"at":"2026-09-28T22:30:00+00:00","value":180.22},{"at":"2026-09-28T22:45:00+00:00","value":174.22},{"at":"2026-09-28T23:00:00+00:00","value":181.81},{"at":"2026-09-28T23:15:00+00:00","value":175.85},{"at":"2026-09-28T23:30:00+00:00","value":171.4},{"at":"2026-09-28T23:45:00+00:00","value":166.79},{"at":"2026-09-29T00:00:00+00:00","value":170.78},{"at":"2026-09-29T00:15:00+00:00","value":168.95},{"at":"2026-09-29T00:30:00+00:00","value":168.78},{"at":"2026-09-29T00:45:00+00:00","value":167.64},{"at":"2026-09-29T01:00:00+00:00","value":164.24},{"at":"2026-09-29T01:15:00+00:00","value":165.16},{"at":"2026-09-29T01:30:00+00:00","value":165.14},{"at":"2026-09-29T01:45:00+00:00","value":165.1},{"at":"2026-09-29T02:00:00+00:00","value":162.1},{"at":"2026-09-29T02:15:00+00:00","value":161.64},{"at":"2026-09-29T02:30:00+00:00","value":159.64},{"at":"2026-09-29T02:45:00+00:00","value":158.22},{"at":"2026-09-29T03:00:00+00:00","value":154.64},{"at":"2026-09-29T03:15:00+00:00","value":158.2},{"at":"2026-09-29T03:30:00+00:00","value":170.54},{"at":"2026-09-29T03:45:00+00:00","value":179.47},{"at":"2026-09-29T04:00:00+00:00","value":191.32},{"at":"2026-09-29T04:15:00+00:00","value":216.62},{"at":"2026-09-29T04:30:00+00:00","value":229.85},{"at":"2026-09-29T04:45:00+00:00","value":226.6},{"at":"2026-09-29T05:00:00+00:00","value":231.37},{"at":"2026-09-29T05:15:00+00:00","value":233.0},{"at":"2026-09-29T05:30:00+00:00","value":226.86},{"at":"2026-09-29T05:45:00+00:00","value":223.25},{"at":"2026-09-29T06:00:00+00:00","value":239.11},{"at":"2026-09-29T06:15:00+00:00","value":230.33},{"at":"2026-09-29T06:30:00+00:00","value":213.57},{"at":"2026-09-29T06:45:00+00:00","value":180.74},{"at":"2026-09-29T07:00:00+00:00","value":212.3},{"at":"2026-09-29T07:15:00+00:00","value":187.84},{"at":"2026-09-29T07:30:00+00:00","value":173.02},{"at":"2026-09-29T07:45:00+00:00","value":163.64},{"at":"2026-09-29T08:00:00+00:00","value":179.29},{"at":"2026-09-29T08:15:00+00:00","value":166.3},{"at":"2026-09-29T08:30:00+00:00","value":158.59},{"at":"2026-09-29T08:45:00+00:00","value":143.09},{"at":"2026-09-29T09:00:00+00:00","value":146.58},{"at":"2026-09-29T09:15:00+00:00","value":137.15},{"at":"2026-09-29T09:30:00+00:00","value":115.77},{"at":"2026-09-29T09:45:00+00:00","value":101.85},{"at":"2026-09-29T10:00:00+00:00","value":98.32},{"at":"2026-09-29T10:15:00+00:00","value":89.79},{"at":"2026-09-29T10:30:00+00:00","value":88.93},{"at":"2026-09-29T10:45:00+00:00","value":76.72},{"at":"2026-09-29T11:00:00+00:00","value":82.26},{"at":"2026-09-29T11:15:00+00:00","value":74.88},{"at":"2026-09-29T11:30:00+00:00","value":68.67},{"at":"2026-09-29T11:45:00+00:00","value":63.94},{"at":"2026-09-29T12:00:00+00:00","value":65.66},{"at":"2026-09-29T12:15:00+00:00","value":79.03},{"at":"2026-09-29T12:30:00+00:00","value":88.03},{"at":"2026-09-29T12:45:00+00:00","value":93.47},{"at":"2026-09-29T13:00:00+00:00","value":89.63},{"at":"2026-09-29T13:15:00+00:00","value":108.68},{"at":"2026-09-29T13:30:00+00:00","value":120.71},{"at":"2026-09-29T13:45:00+00:00","value":130.04},{"at":"2026-09-29T14:00:00+00:00","value":115.21},{"at":"2026-09-29T14:15:00+00:00","value":144.04},{"at":"2026-09-29T14:30:00+00:00","value":161.18},{"at":"2026-09-29T14:45:00+00:00","value":199.62},{"at":"2026-09-29T15:00:00+00:00","value":179.02},{"at":"2026-09-29T15:15:00+00:00","value":201.77},{"at":"2026-09-29T15:30:00+00:00","value":213.69},{"at":"2026-09-29T15:45:00+00:00","value":218.93},{"at":"2026-09-29T16:00:00+00:00","value":219.11},{"at":"2026-09-29T16:15:00+00:00","value":227.88},{"at":"2026-09-29T16:30:00+00:00","value":231.77},{"at":"2026-09-29T16:45:00+00:00","value":244.45},{"at":"2026-09-29T17:00:00+00:00","value":242.68},{"at":"2026-09-29T17:15:00+00:00","value":233.35},{"at":"2026-09-29T17:30:00+00:00","value":227.37},{"at":"2026-09-29T17:45:00+00:00","value":215.79},{"at":"2026-09-29T18:00:00+00:00","value":218.43},{"at":"2026-09-29T18:15:00+00:00","value":207.01},{"at":"2026-09-29T18:30:00+00:00","value":196.85},{"at":"2026-09-29T18:45:00+00:00","value":185.29},{"at":"2026-09-29T19:00:00+00:00","value":183.94},{"at":"2026-09-29T19:15:00+00:00","value":174.47},{"at":"2026-09-29T19:30:00+00:00","value":168.62},{"at":"2026-09-29T19:45:00+00:00","value":152.73},{"at":"2026-09-29T20:00:00+00:00","value":161.51},{"at":"2026-09-29T20:15:00+00:00","value":155.92},{"at":"2026-09-29T20:30:00+00:00","value":153.74},{"at":"2026-09-29T20:45:00+00:00","value":145.44},{"at":"2026-09-29T21:00:00+00:00","value":139.69},{"at":"2026-09-29T21:15:00+00:00","value":134.04},{"at":"2026-09-29T21:30:00+00:00","value":128.69},{"at":"2026-09-29T21:45:00+00:00","value":119.12},{"at":"2026-09-29T22:00:00+00:00","value":112.61},{"at":"2026-09-29T22:15:00+00:00","value":101.44},{"at":"2026-09-29T22:30:00+00:00","value":110.12},{"at":"2026-09-29T22:45:00+00:00","value":114.22},{"at":"2026-09-29T23:00:00+00:00","value":105.64},{"at":"2026-09-29T23:15:00+00:00","value":102.58},{"at":"2026-09-29T23:30:00+00:00","value":103.07},{"at":"2026-09-29T23:45:00+00:00","value":110.7},{"at":"2026-09-30T00:00:00+00:00","value":97.63},{"at":"2026-09-30T00:15:00+00:00","value":101.73},{"at":"2026-09-30T00:30:00+00:00","value":100.05},{"at":"2026-09-30T00:45:00+00:00","value":107.42},{"at":"2026-09-30T01:00:00+00:00","value":100.1},{"at":"2026-09-30T01:15:00+00:00","value":103.65},{"at":"2026-09-30T01:30:00+00:00","value":104.97},{"at":"2026-09-30T01:45:00+00:00","value":102.77},{"at":"2026-09-30T02:00:00+00:00","value":107.32},{"at":"2026-09-30T02:15:00+00:00","value":98.65},{"at":"2026-09-30T02:30:00+00:00","value":101.6},{"at":"2026-09-30T02:45:00+00:00","value":109.62},{"at":"2026-09-30T03:00:00+00:00","value":115.64},{"at":"2026-09-30T03:15:00+00:00","value":119.08},{"at":"2026-09-30T03:30:00+00:00","value":124.14},{"at":"2026-09-30T03:45:00+00:00","value":129.93},{"at":"2026-09-30T04:00:00+00:00","value":144.69},{"at":"2026-09-30T04:15:00+00:00","value":159.42},{"at":"2026-09-30T04:30:00+00:00","value":166.78},{"at":"2026-09-30T04:45:00+00:00","value":170.57},{"at":"2026-09-30T05:00:00+00:00","value":189.56},{"at":"2026-09-30T05:15:00+00:00","value":202.12},{"at":"2026-09-30T05:30:00+00:00","value":204.29},{"at":"2026-09-30T05:45:00+00:00","value":199.67},{"at":"2026-09-30T06:00:00+00:00","value":218.13},{"at":"2026-09-30T06:15:00+00:00","value":203.6},{"at":"2026-09-30T06:30:00+00:00","value":187.45},{"at":"2026-09-30T06:45:00+00:00","value":165.82},{"at":"2026-09-30T07:00:00+00:00","value":189.23},{"at":"2026-09-30T07:15:00+00:00","value":170.85},{"at":"2026-09-30T07:30:00+00:00","value":156.01},{"at":"2026-09-30T07:45:00+00:00","value":144.76},{"at":"2026-09-30T08:00:00+00:00","value":140.0},{"at":"2026-09-30T08:15:00+00:00","value":130.9},{"at":"2026-09-30T08:30:00+00:00","value":123.18},{"at":"2026-09-30T08:45:00+00:00","value":95.15},{"at":"2026-09-30T09:00:00+00:00","value":114.95},{"at":"2026-09-30T09:15:00+00:00","value":90.16},{"at":"2026-09-30T09:30:00+00:00","value":77.97},{"at":"2026-09-30T09:45:00+00:00","value":42.6},{"at":"2026-09-30T10:00:00+00:00","value":60.08},{"at":"2026-09-30T10:15:00+00:00","value":43.85},{"at":"2026-09-30T10:30:00+00:00","value":37.69},{"at":"2026-09-30T10:45:00+00:00","value":30.01},{"at":"2026-09-30T11:00:00+00:00","value":26.32},{"at":"2026-09-30T11:15:00+00:00","value":20.84},{"at":"2026-09-30T11:30:00+00:00","value":13.33},{"at":"2026-09-30T11:45:00+00:00","value":19.51},{"at":"2026-09-30T12:00:00+00:00","value":13.65},{"at":"2026-09-30T12:15:00+00:00","value":24.3},{"at":"2026-09-30T12:30:00+00:00","value":38.14},{"at":"2026-09-30T12:45:00+00:00","value":73.93},{"at":"2026-09-30T13:00:00+00:00","value":43.7},{"at":"2026-09-30T13:15:00+00:00","value":78.46},{"at":"2026-09-30T13:30:00+00:00","value":106.55},{"at":"2026-09-30T13:45:00+00:00","value":111.0},{"at":"2026-09-30T14:00:00+00:00","value":104.98},{"at":"2026-09-30T14:15:00+00:00","value":132.62},{"at":"2026-09-30T14:30:00+00:00","value":169.76},{"at":"2026-09-30T14:45:00+00:00","value":186.5},{"at":"2026-09-30T15:00:00+00:00","value":173.04},{"at":"2026-09-30T15:15:00+00:00","value":194.45},{"at":"2026-09-30T15:30:00+00:00","value":211.78},{"at":"2026-09-30T15:45:00+00:00","value":229.4},{"at":"2026-09-30T16:00:00+00:00","value":213.68},{"at":"2026-09-30T16:15:00+00:00","value":226.5},{"at":"2026-09-30T16:30:00+00:00","value":232.95},{"at":"2026-09-30T16:45:00+00:00","value":248.18},{"at":"2026-09-30T17:00:00+00:00","value":241.78},{"at":"2026-09-30T17:15:00+00:00","value":246.58},{"at":"2026-09-30T17:30:00+00:00","value":255.24},{"at":"2026-09-30T17:45:00+00:00","value":255.37},{"at":"2026-09-30T18:00:00+00:00","value":245.44},{"at":"2026-09-30T18:15:00+00:00","value":242.99},{"at":"2026-09-30T18:30:00+00:00","value":227.16},{"at":"2026-09-30T18:45:00+00:00","value":216.56},{"at":"2026-09-30T19:00:00+00:00","value":235.36},{"at":"2026-09-30T19:15:00+00:00","value":215.39},{"at":"2026-09-30T19:30:00+00:00","value":203.95},{"at":"2026-09-30T19:45:00+00:00","value":170.0},{"at":"2026-09-30T20:00:00+00:00","value":203.49},{"at":"2026-09-30T20:15:00+00:00","value":190.78},{"at":"2026-09-30T20:30:00+00:00","value":184.24},{"at":"2026-09-30T20:45:00+00:00","value":169.04},{"at":"2026-09-30T21:00:00+00:00","value":178.34},{"at":"2026-09-30T21:15:00+00:00","value":164.76},{"at":"2026-09-30T21:30:00+00:00","value":171.04},{"at":"2026-09-30T21:45:00+00:00","value":156.4}]},"licence":{"fr":"CC BY 4.0 (creativecommons.org/licenses/by/4.0) from Bundesnetzagentur | SMARD.de","de":"CC BY 4.0 (creativecommons.org/licenses/by/4.0) from Bundesnetzagentur | SMARD.de"}}
</script>
  <script>
    let snapshot = JSON.parse(document.getElementById('snapshot-data').textContent);
    let powerHistory = JSON.parse(document.getElementById('power-history-data').textContent);
    let powerPrices = JSON.parse(document.getElementById('power-price-data').textContent);
    let powerSpan = 7;
    let powerPriceSpan = 2;
    let powerMeasure = 'load';
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
        metal_copper:'Tonnage minier annuel : aucune conclusion de court terme sans inventaires et demande.',
        metal_aluminum:'Aluminium primaire mondial. Son coût marginal dépend notamment de l’électricité ; ce total annuel ne renseigne pas sur les stocks du jour.',
        ag_corn_condition:'Bon + excellent selon les enquêtes USDA ; comparer à la même semaine de l’année passée, pas au niveau des stocks.',
        ag_soy_condition:'La condition de culture reflète déjà une partie des effets météo sur le rendement potentiel.',
        ag_corn_harvest:'Avancement de récolte : l’écart à la moyenne cinq ans renseigne sur le rythme d’arrivée du grain.',
        ag_soy_harvest:'Comparer à la moyenne cinq ans ; une récolte rapide augmente temporairement les disponibilités.'
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
      box.append(line('COTATIONS EN SÉANCE · INDICATIVES', 'div', 'watch-group'));
      for (const [name,symbol,detail] of [
        ['Brent · OANDA','OANDA:BCOUSD','USD/baril · CFD indicatif, distinct du future ICE'],
        ['WTI · OANDA','OANDA:WTICOUSD','USD/baril · CFD indicatif'],
        ['Gaz US · OANDA','OANDA:NATGASUSD','USD/MMBtu · indicatif, distinct du spot Henry Hub']]) {
        const row = line('', 'div', 'quote-row');
        row.append(line(name, 'strong'));
        const widget = line('', 'div', 'quote-value');
        widget.style.width = '220px'; widget.style.height = '70px';
        row.append(widget,line(detail + ' · cours et horaire chez TradingView', 'small', 'quote-note'));
        box.append(row);
        embed(widget,'https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js',
          {symbol,width:'100%',locale:'fr',colorTheme:'dark',isTransparent:true});
      }
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
        {id:'ag_corn_condition',label:'Maïs US · état des cultures',market:'CBOT maïs',rising:'Part bon/excellent supérieure à N−1 : potentiel de rendement plus confortable.',falling:'Part bon/excellent inférieure à N−1 : récolte plus vulnérable ; surveiller météo et rendement final.'},
        {id:'ag_world_corn', label:'Stocks mondiaux de maïs', market:'Maïs', rising:'Révision des stocks à la hausse : pression potentielle à la baisse.', falling:'Révision des stocks à la baisse : pression potentielle à la hausse.'}],
      metals: [
        {id:'metal_aluminum',label:'Aluminium · offre mondiale annuelle',market:'Aluminium',rising:'Production 2025 supérieure à 2024 : offre structurelle plus abondante. Ce n’est pas un signal de séance.',falling:'Production annuelle plus faible : vérifier stocks LME et demande avant d’interpréter le prix.'}]
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
        card.append(line('Marché concerné : ' + rule.market + ' · ' +
          (selectedSector === 'metals' ? 'repère annuel, sans implication instantanée.' : 'scénario, pas une réaction de cours.'), 'small'));
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
      if (selectedSector === 'oil' && !history.oil_prices) {
        card.hidden = false;
        card.append(line('Brent et WTI · un an · cotations indicatives', 'h3'));
        card.append(line('Historique spot officiel temporairement indisponible. Ces deux courbes OANDA restent séparées et suivent le prix indicatif de leur fournisseur.', 'p', 'detail'));
        const duo = line('', 'div', 'chart-duo');
        for (const [name,symbol] of [['Brent','OANDA:BCOUSD'],['WTI','OANDA:WTICOUSD']]) {
          const panel = line('', 'div', 'widget');
          panel.style.height = '240px';
          duo.append(panel);
          embed(panel,'https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js',
            {symbols:[[name,symbol+'|1D']],dateRanges:['12m|1D'],colorTheme:'dark',isTransparent:true,
             locale:'fr',autosize:true,width:'100%',height:'100%',chartOnly:false});
        }
        card.append(duo); return;
      }
      if (selectedSector === 'oil' && history.oil_prices) {
        title = 'Brent vs WTI · 12 mois · clôtures spot officielles';
        a = history.oil_prices.brent || []; b = history.oil_prices.wti || [];
        unit = '$/bbl';
        note = 'Séries EIA historiques via ' + (snapshot.sources?.oil_price_history?.provenance || 'FRED') + ', publiées avec retard. Ce graphique ne remplace pas la cotation en séance au-dessus.';
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
      const preferred = selectedSector === 'oil' ? ['oil_crude','oil_cushing','oil_gasoline',
        'oil_refinery','oil_imports','oil_exports','oil_norway_liquids'] :
        selectedSector === 'gas' ? ['gas_fr','gas_fr_twh','gas_fr_net','lng_fr_sendout',
          'gas_eu','lng_fr_inventory','gas_us'] :
        selectedSector === 'agri' ? ['ag_corn_condition','ag_corn_harvest','ag_soy_condition',
          'ag_soy_harvest','ag_corn_stocks','ag_world_wheat','ag_soy_stocks'] :
        ['metal_copper','metal_aluminum'];
      const order = new Map(preferred.map((id, index) => [id, index]));
      const sorted = metrics.filter(metric => metric.sector === selectedSector)
        .sort((a, b) => (order.get(a.id) ?? 999) - (order.get(b.id) ?? 999));
      for (const item of sorted.filter(item => preferred.includes(item.id))) box.append(renderMetric(item));
      const others = sorted.filter(item => !preferred.includes(item.id));
      if (others.length) {
        const details = line('', 'details', 'card side-pad');
        details.style.gridColumn = '1 / -1';
        details.append(line('Autres mesures datées (' + others.length + ')', 'summary'));
        const extra = line('', 'div', 'metrics');
        for (const item of others) extra.append(renderMetric(item));
        details.append(extra); box.append(details);
      }
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

    const powerMeasures = [
      ['load', 'Demande', row => row.load],
      ['residual', 'Résiduelle calculée', row => Number.isFinite(row.eolien) && Number.isFinite(row.solaire) ?
        row.load - row.eolien - row.solaire : null],
      ['wind_solar', 'Éolien + solaire', row => Number.isFinite(row.eolien) && Number.isFinite(row.solaire) ?
        row.eolien + row.solaire : null],
      ['gaz', 'Gaz électrique', row => row.gaz],
      ['ech_physiques', 'Échanges nets', row => row.ech_physiques]
    ];

    function renderPowerHistory() {
      const chart = document.getElementById('power-history-chart');
      const meta = document.getElementById('power-history-meta');
      const reading = document.getElementById('power-history-reading');
      const span = document.getElementById('power-span');
      const series = document.getElementById('power-series');
      chart.replaceChildren(); span.replaceChildren(); series.replaceChildren();
      for (const [days, label] of [[1,'24 h'],[7,'7 j'],[30,'30 j'],[365,'1 an']]) {
        const button = line(label, 'button'); button.type = 'button';
        button.setAttribute('aria-pressed', String(powerSpan === days));
        button.addEventListener('click', () => { powerSpan = days; renderPowerHistory(); });
        span.append(button);
      }
      for (const [key, label] of powerMeasures) {
        const button = line(label, 'button'); button.type = 'button';
        button.setAttribute('aria-pressed', String(powerMeasure === key));
        button.addEventListener('click', () => { powerMeasure = key; renderPowerHistory(); });
        series.append(button);
      }
      const historic = Array.isArray(powerHistory?.points) && powerHistory.points.length ?
        powerHistory.points : snapshot.history?.power_fr || [];
      const ordered = historic.filter(row => row && Number.isFinite(row.load) && Number.isFinite(Date.parse(row.at)))
        .sort((a,b) => Date.parse(a.at) - Date.parse(b.at));
      if (ordered.length < 3) {
        chart.append(line('Historique RTE en attente : la prochaine collecte construira les séries.', 'span', 'empty'));
        meta.textContent = ''; reading.textContent = ''; return;
      }
      const last = Date.parse(ordered[ordered.length - 1].at);
      const start = last - powerSpan * 86400000;
      const read = powerMeasures.find(([key]) => key === powerMeasure)[2];
      const selected = ordered.filter(row => Date.parse(row.at) >= start)
        .map(row => ({at:Date.parse(row.at), value:read(row)}))
        .filter(row => Number.isFinite(row.value));
      if (selected.length < 2) {
        chart.append(line('Pas assez de mesures pour cette série.', 'span', 'empty'));
        meta.textContent = 'Dernière observation : ' + parisTime(ordered[ordered.length-1].at);
        reading.textContent = ''; return;
      }
      const values = selected.map(row => row.value);
      let min = Math.min(...values), max = Math.max(...values);
      const padding = Math.max(500, (max - min) * .1);
      min -= padding; max += padding;
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox','0 0 720 235'); svg.setAttribute('preserveAspectRatio','none');
      svg.setAttribute('role','img');
      svg.setAttribute('aria-label', powerMeasures.find(([key]) => key === powerMeasure)[1] +
        ' en MW sur ' + powerSpan + ' jour(s), selon les observations disponibles');
      const add = (tag, attrs) => {
        const node = document.createElementNS('http://www.w3.org/2000/svg',tag);
        for (const [key,value] of Object.entries(attrs)) node.setAttribute(key,String(value));
        svg.append(node); return node;
      };
      const x = stamp => 56 + 651 * (stamp - selected[0].at) /
        Math.max(1, selected[selected.length-1].at - selected[0].at);
      const y = value => 198 - 166 * (value-min) / (max-min);
      for (let i=0;i<=4;i++) {
        const level = min + (max-min)*i/4, ordinate = y(level);
        add('line',{x1:56,x2:707,y1:ordinate,y2:ordinate});
        add('text',{x:2,y:ordinate-4}).textContent = number(level,0);
      }
      if (min < 0 && max > 0) add('line',{x1:56,x2:707,y1:y(0),y2:y(0),class:'zero'});
      const stride = Math.max(1, Math.ceil(selected.length/700));
      const sampled = selected.filter((_,i) => i%stride===0 || i===selected.length-1);
      let segment = [], segments = [];
      for (let i=0;i<sampled.length;i++) {
        if (i && sampled[i].at-sampled[i-1].at > Math.max(2.5, stride*2.5)*3600000) {
          if (segment.length>1) segments.push(segment);
          segment = [];
        }
        segment.push(x(sampled[i].at).toFixed(1)+','+y(sampled[i].value).toFixed(1));
      }
      if (segment.length>1) segments.push(segment);
      for (const points of segments) add('polyline',{points:points.join(' ')});
      for (const [stamp, anchor] of [[selected[0].at,56],[selected[selected.length-1].at,602]])
        add('text',{x:anchor,y:222}).textContent = parisTime(stamp).replace(' · Paris','');
      chart.append(svg);
      const duration = Math.max(1, (last - Date.parse(ordered[0].at))/86400000);
      const expected = Math.max(1, Math.round((selected[selected.length-1].at-selected[0].at)/3600000)+1);
      const coverage = Math.min(100,Math.round(selected.length/expected*100));
      meta.textContent = 'RTE · observé provisoire · ' + selected.length + ' relevés · couverture ' +
        coverage + '% entre les premières et dernières mesures affichées · historique accumulé : ' +
        number(duration,1) + ' j / 365 j · dernier relevé : ' + parisTime(ordered[ordered.length-1].at);
      const recent = selected[selected.length-1];
      reading.textContent = 'Dernière mesure : ' + number(recent.value,0) + ' MW. ' +
        (powerMeasure === 'residual' ? 'Une résiduelle plus élevée peut augmenter le besoin de moyens pilotables ; aucun effet de prix instantané ne se déduit de ce seul chiffre.' :
         powerMeasure === 'ech_physiques' ? 'Solde négatif = exportations nettes ; positif = importations nettes. Ce flux ne donne pas le prix de marché.' :
         'Ce niveau physique est un repère observé, sans prévision automatique du prix.');
    }

    function renderPowerPrices() {
      const cards = document.getElementById('power-price-grid');
      const control = document.getElementById('power-price-span');
      const chart = document.getElementById('power-price-chart');
      const meta = document.getElementById('power-price-meta');
      const reading = document.getElementById('power-price-reading');
      const context = document.getElementById('power-price-context');
      const licence = document.getElementById('power-price-license');
      cards.replaceChildren(); control.replaceChildren(); chart.replaceChildren();
      context.textContent = '';
      const series = powerPrices?.series || {};
      const fr = Array.isArray(series.fr) ? series.fr.filter(point => Number.isFinite(point.value) &&
        Number.isFinite(Date.parse(point.at))) : [];
      const de = Array.isArray(series.de) ? series.de.filter(point => Number.isFinite(point.value) &&
        Number.isFinite(Date.parse(point.at))) : [];
      if (!fr.length) {
        chart.append(line('Prix day-ahead non publiés dans le cockpit : collecte ou licence de la source en attente.', 'span', 'empty'));
        meta.textContent = snapshot.sources?.power_price_fr?.status === 'error' ?
          'Source indisponible lors de la dernière collecte ; aucun prix inventé.' : 'Collecte des prix en attente.';
        reading.textContent = ''; return;
      }
      const attribution = powerPrices.licence?.fr;
      licence.textContent = attribution && attribution === powerPrices.licence?.de ?
        'Licence et attribution déclarées pour France et DE-LU : ' + attribution + '. ' :
        'Licence et attribution déclarées par la source : ' + (attribution || 'à vérifier') + '. ';
      for (const [days,label] of [[2,'48 h'],[7,'7 j'],[30,'30 j'],[365,'1 an']]) {
        const button = line(label,'button'); button.type='button';
        button.setAttribute('aria-pressed',String(powerPriceSpan===days));
        button.addEventListener('click',()=>{powerPriceSpan=days;renderPowerPrices();});
        control.append(button);
      }
      const localDay = at => new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Paris',year:'numeric',
        month:'2-digit',day:'2-digit'}).format(new Date(at));
      const today = localDay(Date.now());
      const tomorrow = localDay(Date.now()+86400000);
      const latestFor = (items, now) => [...items].reverse().find(p => Date.parse(p.at)<=now &&
        Date.parse(p.at)>=now-3600000);
      const now = Date.now(), current = latestFor(fr,now);
      const counterpart = current && de.find(p => p.at===current.at);
      const delivery = fr.filter(p => localDay(p.at)===tomorrow);
      const todayDelivery = fr.filter(p => localDay(p.at)===today);
      const todayAverage = todayDelivery.length >= 80 ?
        todayDelivery.reduce((sum,p)=>sum+p.value,0)/todayDelivery.length : null;
      const average = delivery.length ? delivery.reduce((sum,p)=>sum+p.value,0)/delivery.length : null;
      const peak = delivery.length ? delivery.reduce((a,b)=>a.value>b.value?a:b) : null;
      const countNegative = delivery.filter(p=>p.value<0).length;
      for (const [title,value,detail] of [
        ['France · période en cours',current ? number(current.value,2)+' €/MWh' : '—',
          current ? 'Livraison '+parisTime(current.at) : 'Prix de la période non publié'],
        ['France · demain, moyenne',average!==null ? number(average,2)+' €/MWh' : '—',
          average!==null ? delivery.length+' périodes de livraison' : 'Enchère en attente'],
        ['France − DE-LU · période',current&&counterpart ?
          number(current.value-counterpart.value,2)+' €/MWh' : '—',
          current&&counterpart ? 'Même créneau · positif = France plus chère' : 'Couplage des données en attente'],
        ['France · pic demain',peak ? number(peak.value,2)+' €/MWh' : '—',
          peak ? parisTime(peak.at)+' · '+countNegative+' périodes négatives' : 'À venir']
      ]) {
        const card=line('','article');
        card.append(line(title,'small'),line(value,'strong'),line(detail,'span'));
        cards.append(card);
      }
      const end = Math.max(Date.parse(fr[fr.length-1].at),de.length ? Date.parse(de[de.length-1].at) : 0);
      const start = end-powerPriceSpan*86400000;
      const f = fr.filter(p=>Date.parse(p.at)>=start), d = de.filter(p=>Date.parse(p.at)>=start);
      const values=[...f,...d].map(p=>p.value);
      if (f.length<2) {chart.append(line('Historique insuffisant pour cette période.','span','empty'));return;}
      let low=Infinity,high=-Infinity;
      for (const value of values) {if(value<low)low=value;if(value>high)high=value;}
      const pad=Math.max(10,(high-low)*.12);low-=pad;high+=pad;
      const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
      svg.setAttribute('viewBox','0 0 720 225');svg.setAttribute('preserveAspectRatio','none');
      svg.setAttribute('role','img');svg.setAttribute('aria-label','Prix day-ahead France et DE-LU en euros par MWh');
      const add=(tag,attrs)=>{const el=document.createElementNS('http://www.w3.org/2000/svg',tag);
        for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));svg.append(el);return el;};
      const t0=Math.min(Date.parse(f[0].at),d.length?Date.parse(d[0].at):Infinity);
      const t1=Math.max(Date.parse(f[f.length-1].at),d.length?Date.parse(d[d.length-1].at):0);
      const x=at=>55+650*(Date.parse(at)-t0)/Math.max(1,t1-t0);
      const y=value=>192-160*(value-low)/(high-low);
      for(let i=0;i<=4;i++){
        const v=low+(high-low)*i/4, ordinate=y(v);
        add('line',{x1:55,x2:705,y1:ordinate,y2:ordinate});
        add('text',{x:2,y:ordinate-4}).textContent=number(v,0);
      }
      if(low<0&&high>0)add('line',{x1:55,x2:705,y1:y(0),y2:y(0),class:'zero'});
      for(const [items,css] of [[f,''],[d,'secondary']]){
        const stride=Math.max(1,Math.ceil(items.length/700));
        const sample=items.filter((_,i)=>i%stride===0||i===items.length-1);
        let group=[],groups=[];
        for(let i=0;i<sample.length;i++){
          if(i&&Date.parse(sample[i].at)-Date.parse(sample[i-1].at)>Math.max(2,stride*2.5)*3600000){
            if(group.length>1)groups.push(group);group=[];
          }
          group.push(x(sample[i].at).toFixed(1)+','+y(sample[i].value).toFixed(1));
        }
        if(group.length>1)groups.push(group);
        for(const points of groups)add('polyline',{points:points.join(' '),class:css});
      }
      add('text',{x:55,y:218}).textContent=parisTime(t0).replace(' · Paris','');
      add('text',{x:585,y:218}).textContent=parisTime(t1).replace(' · Paris','');
      chart.append(svg);
      meta.textContent='France (vert) · DE-LU (orange) · même échelle €/MWh · '+f.length+
        ' périodes France affichées · première donnée '+parisTime(fr[0].at)+
        ' · dernière livraison '+parisTime(fr[fr.length-1].at)+
        (snapshot.sources?.power_price_fr?.status==='error'?' · source en erreur : archive':'');
      const rte = snapshot.history?.power_fr || [];
      const observed = rte[rte.length-1];
      const paired = observed && [...fr].reverse().find(p=>Date.parse(p.at)<=Date.parse(observed.at)&&
        Date.parse(p.at)>=Date.parse(observed.at)-3600000);
      reading.textContent=(peak ? 'Demain : pic day-ahead '+number(peak.value,2)+' €/MWh vers '+parisTime(peak.at)+
        '; '+countNegative+' périodes à prix négatif. ' : '')+
        (average!==null&&todayAverage!==null ? 'Moyenne demain '+
        (average>=todayAverage?'+':'')+number(average-todayAverage,2)+
        ' €/MWh face aux '+todayDelivery.length+' périodes d’aujourd’hui. ' : '')+
        (paired&&observed.eolien!==undefined&&observed.solaire!==undefined ?
        'Dernier créneau observé : prix fixé la veille '+number(paired.value,2)+' €/MWh ; demande résiduelle RTE '+
        number(observed.load-observed.eolien-observed.solaire,0)+' MW. Ces deux mesures ne prouvent pas un effet causal.' :
        'Prix et télémesures ont des dates et des définitions différentes : vérifier les créneaux avant comparaison.');
      const byTime = new Map(fr.map(p=>[Date.parse(p.at),p.value]));
      const historicRte = Array.isArray(powerHistory?.points) && powerHistory.points.length ?
        powerHistory.points : rte;
      const matched = historicRte.filter(p=>Date.parse(p.at)<=now&&Date.parse(p.at)>=now-7*86400000 &&
        Number.isFinite(p.load)&&Number.isFinite(p.eolien)&&Number.isFinite(p.solaire))
        .map(p=>({residual:p.load-p.eolien-p.solaire,price:byTime.get(Date.parse(p.at))}))
        .filter(p=>Number.isFinite(p.price));
      if(matched.length>=48){
        const ordered=matched.map(p=>p.residual).sort((a,b)=>a-b);
        const pivot=ordered[Math.floor(ordered.length/2)];
        const lower=matched.filter(p=>p.residual<pivot),upper=matched.filter(p=>p.residual>=pivot);
        const mean=items=>items.reduce((sum,p)=>sum+p.price,0)/items.length;
        context.textContent=lower.length&&upper.length ?
          'Sur '+matched.length+' créneaux appariés des 7 derniers jours : prix day-ahead moyen '+
          number(mean(upper),2)+' €/MWh quand la demande résiduelle observée est ≥ '+number(pivot,0)+
          ' MW (n='+upper.length+'), contre '+number(mean(lower),2)+' €/MWh en dessous (n='+lower.length+
          '). Lecture descriptive : prix fixé la veille, demande mesurée ensuite, autres facteurs non isolés.' :
          'Comparaison prix et demande résiduelle en cours de constitution.';
      } else {
        context.textContent='Comparaison prix et demande résiduelle : '+matched.length+
          ' créneaux exactement appariés sur 7 jours ; 48 requis pour afficher un repère.';
      }
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
      for (const [read, css] of [[row => row.load, 'demand-line'], [residual, 'residual-line']]) {
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
                        renderStories,renderSector,renderPower,renderPowerHistory,renderPowerPrices]) {
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
        try {
          const powerResponse = await fetch('https://raw.githubusercontent.com/TheoTaillandier/Test2/main/data/power_fr.json?t=' + Date.now(), {cache:'no-store'});
          if (powerResponse.ok) {
            const power = await powerResponse.json();
            if (power.schema === 1 && Array.isArray(power.points) && power.points.length &&
                Date.parse(power.last_at) >= Date.parse(powerHistory.last_at || 0)) powerHistory = power;
          }
        } catch (error) { console.warn('Historique Power non synchronisé :', error); }
        try {
          const priceResponse = await fetch('https://raw.githubusercontent.com/TheoTaillandier/Test2/main/data/power_prices.json?t=' + Date.now(), {cache:'no-store'});
          if (priceResponse.ok) {
            const prices = await priceResponse.json();
            if (prices.schema===1&&Array.isArray(prices.series?.fr)&&
                Date.parse(prices.generated_at)>=Date.parse(powerPrices.generated_at||0)) powerPrices=prices;
          }
        } catch (error) { console.warn('Prix Power non synchronisés :', error); }
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
