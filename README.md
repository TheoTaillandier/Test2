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
- TTF/PEG/JKM : liens vers sources de marché ; un flux de cotations automatisé et redistribué publiquement nécessite un droit de diffusion. ENTSO-E fournit des prévisions électriques ouvertes, ENTSOG des flux physiques de gaz, et GIE les stocks/terminaux.
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
    .chart, .watch, .calendar { display: flex; flex-direction: column; }
    .right { min-height: 0; display: grid; grid-template-rows: minmax(350px, 1.05fr) minmax(300px, .95fr); gap: 12px; }
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
      .physical-layout { grid-template-columns: 1fr; }
      .physical-side { grid-template-columns: 1fr 1fr; }
      .power-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .power-layout { grid-template-columns:1fr; }
    }
    @media (max-width: 680px) {
      .header { padding: 9px; flex-wrap: wrap; }
      .brand span { display: none; }
      .market-grid { display: block; padding: 8px; }
      .chart { height: 490px; margin-bottom: 9px; }
      .right { display: block; }
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
    <div class="ticker" id="ticker" aria-label="Repères de marché vérifiés"></div>
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
          <div class="bar"><h2>À surveiller · énergie et matières</h2><small>Prix datés / accès direct</small></div>
          <div class="watch-list" id="watch-list"></div>
          <div class="market-snapshot" id="market-snapshot"><h3>Repères physiques vérifiés · disponibles même sans cotations</h3></div>
          <div class="caption">Spot EIA : dernière observation publiée. TTF/PEG/JKM : ouvrir la source pour le prix en séance ; contrat et délai à vérifier sur le site.</div>
        </section>
        <section class="card calendar">
          <div class="bar"><h2>Prochaines publications · heure de Paris</h2><a href="https://www.eia.gov/petroleum/supply/weekly/schedule.php" target="_blank" rel="noopener noreferrer">Dates ↗</a></div>
          <div class="agenda" id="agenda"></div>
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
          <section><h2 class="section-heading" id="sector-heading">Pétrole · prix spot et stocks</h2><div class="metrics" id="metrics"></div><div class="card side-pad trend" id="trend" hidden><h3>Stocks commerciaux de brut US · 26 dernières semaines</h3><svg viewBox="0 0 400 110" preserveAspectRatio="none" role="img" aria-label="Évolution hebdomadaire des stocks commerciaux de brut US"><polyline id="trend-line" points=""></polyline></svg><div class="axis"><span id="trend-start"></span><span id="trend-end"></span></div></div></section>
        <aside class="physical-side">
          <section class="card side-pad" id="takeaways"><h3>Ce que disent les publications</h3><div id="takeaway-list"></div></section>
          <section class="card side-pad"><h3>Actualités qui éclairent le physique · EIA</h3><p>Production, stocks, raffinage et GNL. Les articles décrivent des faits publiés ; leur effet sur les prix reste à analyser.</p><div id="stories"></div></section>
          <section class="card side-pad"><h3>Couverture France et Europe</h3><p>Une <a href="https://agsi.gie.eu/account" target="_blank" rel="noopener noreferrer">clé GIE gratuite ↗</a> active AGSI + ALSI : remplissage et volume gaz France/UE, GNL en cuves et émission des terminaux. Sans clé, ces valeurs restent vides. <a href="https://transparency.entsog.eu/" target="_blank" rel="noopener noreferrer">ENTSOG ↗</a> complète avec les flux gaziers. Le cuivre USGS est annuel ; les <a href="https://www.lme.com/Market-data/Reports-and-data/Warehouse-and-stocks-reports" target="_blank" rel="noopener noreferrer">stocks LME ↗</a> ne sont pas chiffrés ici.</p></section>
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

  <p class="footer">Sources : EIA (prix spot datés, WPSR et WNGSR), USDA WASDE, USGS, Sodir (repère norvégien daté), GIE AGSI/ALSI si configuré. Les prix TTF, PEG et JKM consultables par lien ne sont pas des cotations publiées ici. Une source inaccessible conserve sa dernière valeur datée et est signalée.</p>

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
  "generated_at": "2026-09-25T14:17:54+00:00",
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
    ],
    "power_fr": [
      {
        "at": "2026-09-24T14:15:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -6903,
        "eolien": 715,
        "fioul": 35,
        "gaz": 898,
        "hydraulique": 3288,
        "load": 46982,
        "nucleaire": 36142,
        "pompage": -1622,
        "prevision_j": 47300,
        "prevision_j1": 46350,
        "solaire": 13432,
        "taux_co2": 16
      },
      {
        "at": "2026-09-24T14:30:00+00:00",
        "bioenergies": 996,
        "charbon": 0,
        "ech_physiques": -6860,
        "eolien": 779,
        "fioul": 35,
        "gaz": 1031,
        "hydraulique": 3567,
        "load": 46856,
        "nucleaire": 35956,
        "pompage": -1383,
        "prevision_j": 47100,
        "prevision_j1": 46100,
        "solaire": 12748,
        "taux_co2": 17
      },
      {
        "at": "2026-09-24T14:45:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -6931,
        "eolien": 798,
        "fioul": 35,
        "gaz": 1104,
        "hydraulique": 3641,
        "load": 46801,
        "nucleaire": 36459,
        "pompage": -1149,
        "prevision_j": 46950,
        "prevision_j1": 45850,
        "solaire": 11859,
        "taux_co2": 18
      },
      {
        "at": "2026-09-24T15:00:00+00:00",
        "bioenergies": 992,
        "charbon": 0,
        "ech_physiques": -6529,
        "eolien": 785,
        "fioul": 35,
        "gaz": 1361,
        "hydraulique": 3649,
        "load": 46672,
        "nucleaire": 36544,
        "pompage": -983,
        "prevision_j": 46800,
        "prevision_j1": 45600,
        "solaire": 10831,
        "taux_co2": 20
      },
      {
        "at": "2026-09-24T15:15:00+00:00",
        "bioenergies": 992,
        "charbon": 0,
        "ech_physiques": -5892,
        "eolien": 788,
        "fioul": 35,
        "gaz": 1717,
        "hydraulique": 3526,
        "load": 46916,
        "nucleaire": 36580,
        "pompage": -491,
        "prevision_j": 46650,
        "prevision_j1": 45600,
        "solaire": 9780,
        "taux_co2": 23
      },
      {
        "at": "2026-09-24T15:30:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -6903,
        "eolien": 802,
        "fioul": 35,
        "gaz": 2551,
        "hydraulique": 3783,
        "load": 46611,
        "nucleaire": 36651,
        "pompage": 0,
        "prevision_j": 46500,
        "prevision_j1": 45600,
        "solaire": 8696,
        "taux_co2": 30
      },
      {
        "at": "2026-09-24T15:45:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -7375,
        "eolien": 819,
        "fioul": 35,
        "gaz": 3428,
        "hydraulique": 4208,
        "load": 46573,
        "nucleaire": 36702,
        "pompage": 0,
        "prevision_j": 46950,
        "prevision_j1": 46200,
        "solaire": 7614,
        "taux_co2": 37
      },
      {
        "at": "2026-09-24T16:00:00+00:00",
        "bioenergies": 990,
        "charbon": 0,
        "ech_physiques": -6194,
        "eolien": 811,
        "fioul": 35,
        "gaz": 3624,
        "hydraulique": 4796,
        "load": 47094,
        "nucleaire": 36594,
        "pompage": -1,
        "prevision_j": 47400,
        "prevision_j1": 46800,
        "solaire": 6452,
        "taux_co2": 39
      },
      {
        "at": "2026-09-24T16:15:00+00:00",
        "bioenergies": 989,
        "charbon": 0,
        "ech_physiques": -5285,
        "eolien": 833,
        "fioul": 35,
        "gaz": 3697,
        "hydraulique": 5282,
        "load": 47466,
        "nucleaire": 36664,
        "pompage": 0,
        "prevision_j": 47850,
        "prevision_j1": 47400,
        "solaire": 5254,
        "taux_co2": 40
      },
      {
        "at": "2026-09-24T16:30:00+00:00",
        "bioenergies": 994,
        "charbon": 0,
        "ech_physiques": -4638,
        "eolien": 879,
        "fioul": 35,
        "gaz": 3805,
        "hydraulique": 6083,
        "load": 47942,
        "nucleaire": 36658,
        "pompage": 0,
        "prevision_j": 48300,
        "prevision_j1": 48000,
        "solaire": 4128,
        "taux_co2": 41
      },
      {
        "at": "2026-09-24T16:45:00+00:00",
        "bioenergies": 999,
        "charbon": 0,
        "ech_physiques": -4107,
        "eolien": 894,
        "fioul": 35,
        "gaz": 3878,
        "hydraulique": 6978,
        "load": 48474,
        "nucleaire": 36740,
        "pompage": -1,
        "prevision_j": 48900,
        "prevision_j1": 48750,
        "solaire": 3060,
        "taux_co2": 42
      },
      {
        "at": "2026-09-24T17:00:00+00:00",
        "bioenergies": 991,
        "charbon": 0,
        "ech_physiques": -3454,
        "eolien": 942,
        "fioul": 35,
        "gaz": 3950,
        "hydraulique": 7723,
        "load": 49185,
        "nucleaire": 36726,
        "pompage": -10,
        "prevision_j": 49500,
        "prevision_j1": 49500,
        "solaire": 2038,
        "taux_co2": 42
      },
      {
        "at": "2026-09-24T17:15:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -3995,
        "eolien": 1007,
        "fioul": 35,
        "gaz": 4223,
        "hydraulique": 8331,
        "load": 48843,
        "nucleaire": 36773,
        "pompage": -27,
        "prevision_j": 49350,
        "prevision_j1": 49350,
        "solaire": 1313,
        "taux_co2": 44
      },
      {
        "at": "2026-09-24T17:30:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -4402,
        "eolien": 1130,
        "fioul": 35,
        "gaz": 4261,
        "hydraulique": 8355,
        "load": 48281,
        "nucleaire": 36806,
        "pompage": -32,
        "prevision_j": 49200,
        "prevision_j1": 49200,
        "solaire": 747,
        "taux_co2": 45
      },
      {
        "at": "2026-09-24T17:45:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -3963,
        "eolien": 1266,
        "fioul": 35,
        "gaz": 4345,
        "hydraulique": 8483,
        "load": 48724,
        "nucleaire": 36804,
        "pompage": -39,
        "prevision_j": 49100,
        "prevision_j1": 49100,
        "solaire": 435,
        "taux_co2": 46
      },
      {
        "at": "2026-09-24T18:00:00+00:00",
        "bioenergies": 999,
        "charbon": 0,
        "ech_physiques": -3955,
        "eolien": 1379,
        "fioul": 35,
        "gaz": 4470,
        "hydraulique": 8459,
        "load": 48795,
        "nucleaire": 36840,
        "pompage": -39,
        "prevision_j": 49000,
        "prevision_j1": 49000,
        "solaire": 242,
        "taux_co2": 47
      },
      {
        "at": "2026-09-24T18:15:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -4617,
        "eolien": 1493,
        "fioul": 35,
        "gaz": 4633,
        "hydraulique": 8351,
        "load": 48290,
        "nucleaire": 36842,
        "pompage": -43,
        "prevision_j": 48600,
        "prevision_j1": 48600,
        "solaire": 200,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T18:30:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -5349,
        "eolien": 1699,
        "fioul": 35,
        "gaz": 4629,
        "hydraulique": 8114,
        "load": 47455,
        "nucleaire": 36822,
        "pompage": -46,
        "prevision_j": 48200,
        "prevision_j1": 48200,
        "solaire": 189,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T18:45:00+00:00",
        "bioenergies": 999,
        "charbon": 0,
        "ech_physiques": -6351,
        "eolien": 1919,
        "fioul": 35,
        "gaz": 4641,
        "hydraulique": 7927,
        "load": 46471,
        "nucleaire": 36838,
        "pompage": -48,
        "prevision_j": 47250,
        "prevision_j1": 47250,
        "solaire": 189,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T19:00:00+00:00",
        "bioenergies": 1002,
        "charbon": 0,
        "ech_physiques": -7234,
        "eolien": 2116,
        "fioul": 35,
        "gaz": 4648,
        "hydraulique": 7615,
        "load": 45542,
        "nucleaire": 36856,
        "pompage": 0,
        "prevision_j": 46300,
        "prevision_j1": 46300,
        "solaire": 180,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T19:15:00+00:00",
        "bioenergies": 1001,
        "charbon": 0,
        "ech_physiques": -7987,
        "eolien": 2368,
        "fioul": 35,
        "gaz": 4666,
        "hydraulique": 7415,
        "load": 44527,
        "nucleaire": 36971,
        "pompage": 0,
        "prevision_j": 45600,
        "prevision_j1": 45600,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T19:30:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -8402,
        "eolien": 2588,
        "fioul": 35,
        "gaz": 4617,
        "hydraulique": 6917,
        "load": 43700,
        "nucleaire": 36976,
        "pompage": -1,
        "prevision_j": 44900,
        "prevision_j1": 44900,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T19:45:00+00:00",
        "bioenergies": 1000,
        "charbon": 0,
        "ech_physiques": -8627,
        "eolien": 2830,
        "fioul": 36,
        "gaz": 4617,
        "hydraulique": 6592,
        "load": 43271,
        "nucleaire": 36969,
        "pompage": 0,
        "prevision_j": 44150,
        "prevision_j1": 44150,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T20:00:00+00:00",
        "bioenergies": 998,
        "charbon": 0,
        "ech_physiques": -9091,
        "eolien": 3055,
        "fioul": 36,
        "gaz": 4679,
        "hydraulique": 6206,
        "load": 42855,
        "nucleaire": 37000,
        "pompage": 0,
        "prevision_j": 43400,
        "prevision_j1": 43400,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T20:15:00+00:00",
        "bioenergies": 1003,
        "charbon": 0,
        "ech_physiques": -8363,
        "eolien": 3175,
        "fioul": 36,
        "gaz": 4654,
        "hydraulique": 5360,
        "load": 43080,
        "nucleaire": 37216,
        "pompage": -1,
        "prevision_j": 43950,
        "prevision_j1": 43950,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-24T20:30:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -8269,
        "eolien": 3284,
        "fioul": 36,
        "gaz": 4631,
        "hydraulique": 5155,
        "load": 43262,
        "nucleaire": 37441,
        "pompage": -1,
        "prevision_j": 44500,
        "prevision_j1": 44500,
        "solaire": 0,
        "taux_co2": 48
      },
      {
        "at": "2026-09-24T20:45:00+00:00",
        "bioenergies": 995,
        "charbon": 0,
        "ech_physiques": -7552,
        "eolien": 3394,
        "fioul": 36,
        "gaz": 4659,
        "hydraulique": 5071,
        "load": 44149,
        "nucleaire": 37565,
        "pompage": 0,
        "prevision_j": 44900,
        "prevision_j1": 44900,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-24T21:00:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -8252,
        "eolien": 3447,
        "fioul": 36,
        "gaz": 4633,
        "hydraulique": 4776,
        "load": 43323,
        "nucleaire": 37682,
        "pompage": -2,
        "prevision_j": 45300,
        "prevision_j1": 45300,
        "solaire": 0,
        "taux_co2": 49
      },
      {
        "at": "2026-09-24T21:15:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -8727,
        "eolien": 3542,
        "fioul": 36,
        "gaz": 4452,
        "hydraulique": 5020,
        "load": 43020,
        "nucleaire": 37696,
        "pompage": -1,
        "prevision_j": 44650,
        "prevision_j1": 44650,
        "solaire": 0,
        "taux_co2": 47
      },
      {
        "at": "2026-09-24T21:30:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": -8464,
        "eolien": 3627,
        "fioul": 36,
        "gaz": 4147,
        "hydraulique": 4327,
        "load": 42229,
        "nucleaire": 37690,
        "pompage": -1,
        "prevision_j": 44000,
        "prevision_j1": 44000,
        "solaire": 0,
        "taux_co2": 45
      },
      {
        "at": "2026-09-24T21:45:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": -8111,
        "eolien": 3723,
        "fioul": 35,
        "gaz": 3884,
        "hydraulique": 4341,
        "load": 42584,
        "nucleaire": 37723,
        "pompage": -1,
        "prevision_j": 43200,
        "prevision_j1": 43350,
        "solaire": 0,
        "taux_co2": 43
      },
      {
        "at": "2026-09-24T22:00:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -8424,
        "eolien": 3827,
        "fioul": 36,
        "gaz": 3717,
        "hydraulique": 3883,
        "load": 41590,
        "nucleaire": 37702,
        "pompage": -1,
        "prevision_j": 42400,
        "prevision_j1": 42700,
        "solaire": 0,
        "taux_co2": 42
      },
      {
        "at": "2026-09-24T22:15:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -8684,
        "eolien": 3891,
        "fioul": 36,
        "gaz": 3974,
        "hydraulique": 3769,
        "load": 41692,
        "nucleaire": 37766,
        "pompage": 0,
        "prevision_j": 41750,
        "prevision_j1": 41900,
        "solaire": 0,
        "taux_co2": 44
      },
      {
        "at": "2026-09-24T22:30:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -9710,
        "eolien": 3921,
        "fioul": 37,
        "gaz": 3534,
        "hydraulique": 3739,
        "load": 40347,
        "nucleaire": 37836,
        "pompage": 0,
        "prevision_j": 41100,
        "prevision_j1": 41100,
        "solaire": 0,
        "taux_co2": 41
      },
      {
        "at": "2026-09-24T22:45:00+00:00",
        "bioenergies": 997,
        "charbon": 0,
        "ech_physiques": -9909,
        "eolien": 3962,
        "fioul": 37,
        "gaz": 3407,
        "hydraulique": 3615,
        "load": 39586,
        "nucleaire": 37852,
        "pompage": 0,
        "prevision_j": 40400,
        "prevision_j1": 40400,
        "solaire": 0,
        "taux_co2": 40
      },
      {
        "at": "2026-09-24T23:00:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -10000,
        "eolien": 4013,
        "fioul": 37,
        "gaz": 3171,
        "hydraulique": 3380,
        "load": 39113,
        "nucleaire": 37869,
        "pompage": 0,
        "prevision_j": 39700,
        "prevision_j1": 39700,
        "solaire": 0,
        "taux_co2": 38
      },
      {
        "at": "2026-09-24T23:15:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -10336,
        "eolien": 4023,
        "fioul": 37,
        "gaz": 3310,
        "hydraulique": 3338,
        "load": 39234,
        "nucleaire": 37870,
        "pompage": 0,
        "prevision_j": 39900,
        "prevision_j1": 39900,
        "solaire": 0,
        "taux_co2": 39
      },
      {
        "at": "2026-09-24T23:30:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": -10196,
        "eolien": 4010,
        "fioul": 37,
        "gaz": 2915,
        "hydraulique": 3211,
        "load": 38697,
        "nucleaire": 37850,
        "pompage": -1,
        "prevision_j": 40100,
        "prevision_j1": 40100,
        "solaire": 0,
        "taux_co2": 36
      },
      {
        "at": "2026-09-24T23:45:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -9858,
        "eolien": 4000,
        "fioul": 36,
        "gaz": 2400,
        "hydraulique": 3058,
        "load": 38413,
        "nucleaire": 37866,
        "pompage": -8,
        "prevision_j": 39500,
        "prevision_j1": 39500,
        "solaire": 0,
        "taux_co2": 32
      },
      {
        "at": "2026-09-25T00:00:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": -9863,
        "eolien": 3886,
        "fioul": 37,
        "gaz": 2085,
        "hydraulique": 2981,
        "load": 37820,
        "nucleaire": 37885,
        "pompage": -174,
        "prevision_j": 38900,
        "prevision_j1": 38900,
        "solaire": 0,
        "taux_co2": 30
      },
      {
        "at": "2026-09-25T00:15:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -9919,
        "eolien": 3773,
        "fioul": 37,
        "gaz": 2248,
        "hydraulique": 3009,
        "load": 37536,
        "nucleaire": 37613,
        "pompage": -173,
        "prevision_j": 38100,
        "prevision_j1": 38100,
        "solaire": 0,
        "taux_co2": 31
      },
      {
        "at": "2026-09-25T00:30:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": -10278,
        "eolien": 3684,
        "fioul": 35,
        "gaz": 1760,
        "hydraulique": 2991,
        "load": 36395,
        "nucleaire": 37405,
        "pompage": -174,
        "prevision_j": 37300,
        "prevision_j1": 37300,
        "solaire": 0,
        "taux_co2": 27
      },
      {
        "at": "2026-09-25T00:45:00+00:00",
        "bioenergies": 1007,
        "charbon": 0,
        "ech_physiques": -11075,
        "eolien": 3649,
        "fioul": 37,
        "gaz": 1597,
        "hydraulique": 2850,
        "load": 35758,
        "nucleaire": 37979,
        "pompage": -191,
        "prevision_j": 36750,
        "prevision_j1": 36750,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-25T01:00:00+00:00",
        "bioenergies": 1005,
        "charbon": 0,
        "ech_physiques": -11480,
        "eolien": 3594,
        "fioul": 37,
        "gaz": 1517,
        "hydraulique": 2853,
        "load": 35253,
        "nucleaire": 38173,
        "pompage": -192,
        "prevision_j": 36200,
        "prevision_j1": 36200,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-25T01:15:00+00:00",
        "bioenergies": 1006,
        "charbon": 0,
        "ech_physiques": -11835,
        "eolien": 3514,
        "fioul": 35,
        "gaz": 1574,
        "hydraulique": 2907,
        "load": 35141,
        "nucleaire": 38203,
        "pompage": -253,
        "prevision_j": 35850,
        "prevision_j1": 35850,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-25T01:30:00+00:00",
        "bioenergies": 1014,
        "charbon": 0,
        "ech_physiques": -12139,
        "eolien": 3419,
        "fioul": 37,
        "gaz": 1567,
        "hydraulique": 2846,
        "load": 34661,
        "nucleaire": 38251,
        "pompage": -263,
        "prevision_j": 35500,
        "prevision_j1": 35500,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-25T01:45:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": -12356,
        "eolien": 3355,
        "fioul": 36,
        "gaz": 1464,
        "hydraulique": 2756,
        "load": 34441,
        "nucleaire": 38550,
        "pompage": -264,
        "prevision_j": 35250,
        "prevision_j1": 35250,
        "solaire": 0,
        "taux_co2": 24
      },
      {
        "at": "2026-09-25T02:00:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -12602,
        "eolien": 3326,
        "fioul": 36,
        "gaz": 1334,
        "hydraulique": 2803,
        "load": 34311,
        "nucleaire": 38918,
        "pompage": -496,
        "prevision_j": 35000,
        "prevision_j1": 35000,
        "solaire": 0,
        "taux_co2": 23
      },
      {
        "at": "2026-09-25T02:15:00+00:00",
        "bioenergies": 1013,
        "charbon": 0,
        "ech_physiques": -12371,
        "eolien": 3294,
        "fioul": 36,
        "gaz": 1522,
        "hydraulique": 2776,
        "load": 34369,
        "nucleaire": 39079,
        "pompage": -824,
        "prevision_j": 34900,
        "prevision_j1": 34900,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-25T02:30:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -12238,
        "eolien": 3289,
        "fioul": 36,
        "gaz": 1409,
        "hydraulique": 2714,
        "load": 34207,
        "nucleaire": 39105,
        "pompage": -755,
        "prevision_j": 34800,
        "prevision_j1": 34800,
        "solaire": 0,
        "taux_co2": 24
      },
      {
        "at": "2026-09-25T02:45:00+00:00",
        "bioenergies": 1008,
        "charbon": 0,
        "ech_physiques": -12678,
        "eolien": 3284,
        "fioul": 37,
        "gaz": 1555,
        "hydraulique": 2797,
        "load": 34240,
        "nucleaire": 39125,
        "pompage": -759,
        "prevision_j": 35150,
        "prevision_j1": 35150,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-25T03:00:00+00:00",
        "bioenergies": 1012,
        "charbon": 0,
        "ech_physiques": -12295,
        "eolien": 3283,
        "fioul": 37,
        "gaz": 1637,
        "hydraulique": 2793,
        "load": 34696,
        "nucleaire": 39115,
        "pompage": -751,
        "prevision_j": 35500,
        "prevision_j1": 35500,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-25T03:15:00+00:00",
        "bioenergies": 1014,
        "charbon": 0,
        "ech_physiques": -11520,
        "eolien": 3197,
        "fioul": 37,
        "gaz": 1716,
        "hydraulique": 2897,
        "load": 35473,
        "nucleaire": 39140,
        "pompage": -752,
        "prevision_j": 36050,
        "prevision_j1": 36050,
        "solaire": 0,
        "taux_co2": 26
      },
      {
        "at": "2026-09-25T03:30:00+00:00",
        "bioenergies": 1014,
        "charbon": 0,
        "ech_physiques": -11464,
        "eolien": 3145,
        "fioul": 35,
        "gaz": 1523,
        "hydraulique": 2834,
        "load": 35765,
        "nucleaire": 39150,
        "pompage": -343,
        "prevision_j": 36600,
        "prevision_j1": 36600,
        "solaire": 0,
        "taux_co2": 25
      },
      {
        "at": "2026-09-25T03:45:00+00:00",
        "bioenergies": 1018,
        "charbon": 0,
        "ech_physiques": -11404,
        "eolien": 3100,
        "fioul": 37,
        "gaz": 1957,
        "hydraulique": 2919,
        "load": 36409,
        "nucleaire": 39138,
        "pompage": -346,
        "prevision_j": 37450,
        "prevision_j1": 37450,
        "solaire": 0,
        "taux_co2": 28
      },
      {
        "at": "2026-09-25T04:00:00+00:00",
        "bioenergies": 1011,
        "charbon": 0,
        "ech_physiques": -11221,
        "eolien": 3075,
        "fioul": 37,
        "gaz": 2666,
        "hydraulique": 2980,
        "load": 37462,
        "nucleaire": 38967,
        "pompage": -21,
        "prevision_j": 38300,
        "prevision_j1": 38300,
        "solaire": 0,
        "taux_co2": 34
      },
      {
        "at": "2026-09-25T04:15:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -10930,
        "eolien": 3089,
        "fioul": 37,
        "gaz": 3028,
        "hydraulique": 3513,
        "load": 38745,
        "nucleaire": 38972,
        "pompage": -2,
        "prevision_j": 39400,
        "prevision_j1": 39400,
        "solaire": 0,
        "taux_co2": 37
      },
      {
        "at": "2026-09-25T04:30:00+00:00",
        "bioenergies": 1009,
        "charbon": 0,
        "ech_physiques": -10755,
        "eolien": 3089,
        "fioul": 37,
        "gaz": 3350,
        "hydraulique": 3997,
        "load": 39721,
        "nucleaire": 39004,
        "pompage": 0,
        "prevision_j": 40500,
        "prevision_j1": 40500,
        "solaire": 0,
        "taux_co2": 39
      },
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
      "as_of": "2026-09-25",
      "change": -987,
      "comparison": "vs ~1 h",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_load",
      "label": "Demande France",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 46801
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "export si négatif · import si positif",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_exchange",
      "label": "Solde des échanges physiques",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -8678
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_nucleaire",
      "label": "Nucléaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 34859
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_gaz",
      "label": "Gaz électrique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 601
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_eolien",
      "label": "Éolien",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 1823
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_solaire",
      "label": "Solaire",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 17152
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_hydraulique",
      "label": "Hydraulique",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 2240
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "production observée",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_bioenergies",
      "label": "Bioénergies",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 985
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "demande − éolien − solaire",
      "detail": "Calcul indicatif, sans jugement sur le prix ni l'appel au gaz. Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_residual",
      "label": "Demande résiduelle indicative",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 27826
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "production française",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_carbon",
      "label": "Intensité CO₂ estimée",
      "sector": "power",
      "source": "RTE éCO2mix",
      "unit": "g/kWh",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": 13
    },
    {
      "as_of": "2026-09-25",
      "change": null,
      "comparison": "réalisé − prévision réactualisée le jour même",
      "detail": "Observation 2026-09-25T14:00:00+00:00 UTC",
      "id": "power_load_gap",
      "label": "Écart à prévision de demande J",
      "sector": "power",
      "source": "Calcul sur RTE éCO2mix",
      "unit": "MW",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/",
      "value": -99
    },
    {
      "as_of": "2026-09-23",
      "change": 0.11,
      "comparison": "points vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu",
      "label": "Stockage gaz UE · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 70.35
    },
    {
      "as_of": "2026-09-23",
      "change": 1.277,
      "comparison": "vs veille",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_twh",
      "label": "Gaz stocké UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 796.108
    },
    {
      "as_of": "2026-09-23",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Estimé par les opérateurs",
      "id": "gas_eu_net",
      "label": "Soutirage net UE",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -1243.4
    },
    {
      "as_of": "2026-09-23",
      "change": 0.34,
      "comparison": "points vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr",
      "label": "Stockage gaz France · remplissage",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "%",
      "url": "https://agsi.gie.eu/",
      "value": 81.43
    },
    {
      "as_of": "2026-09-23",
      "change": 0.42,
      "comparison": "vs veille",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_twh",
      "label": "Gaz stocké France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "TWh",
      "url": "https://agsi.gie.eu/",
      "value": 100.871
    },
    {
      "as_of": "2026-09-23",
      "change": null,
      "comparison": "positif = soutirage ; négatif = injection",
      "detail": "Déclaré par les opérateurs",
      "id": "gas_fr_net",
      "label": "Soutirage net France",
      "sector": "gas",
      "source": "GIE AGSI+",
      "unit": "GWh/j",
      "url": "https://agsi.gie.eu/",
      "value": -420.1
    }
  ],
  "schema": 3,
  "sources": {
    "alsi": {
      "checked_at": "2026-09-25T14:17:54+00:00",
      "message": "Dernière donnée conservée ; source indisponible.",
      "status": "error",
      "url": "https://alsi.gie.eu/"
    },
    "alsi_fr": {
      "checked_at": "2026-09-25T14:17:54+00:00",
      "message": "Dernière donnée conservée ; source indisponible.",
      "status": "error",
      "url": "https://alsi.gie.eu/"
    },
    "brent": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm"
    },
    "entsoe_de": {
      "message": "Clé ENTSO-E requise pour la prévision J-1.",
      "status": "needs_key",
      "url": "https://transparency.entsoe.eu/"
    },
    "entsoe_fr": {
      "message": "Clé ENTSO-E requise pour la prévision J-1.",
      "status": "needs_key",
      "url": "https://transparency.entsoe.eu/"
    },
    "gas": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "status": "ok",
      "url": "https://ir.eia.gov/ngs/ngs.html"
    },
    "gie": {
      "as_of": "2026-09-23",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "gie_fr": {
      "as_of": "2026-09-23",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "status": "ok",
      "url": "https://agsi.gie.eu/"
    },
    "henry": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-25T14:17:54+00:00",
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
      "checked_at": "2026-09-25T14:17:54+00:00",
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
      "checked_at": "2026-09-25T14:17:54+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_flows": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "oil_history": {
      "as_of": "2026-09-18",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "published": "2026-09-23",
      "status": "ok",
      "url": "https://www.eia.gov/petroleum/supply/weekly/"
    },
    "rte_power": {
      "as_of": "2026-09-25T14:00:00+00:00",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "status": "ok",
      "url": "https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/"
    },
    "wasde": {
      "as_of": "2026-09",
      "checked_at": "2026-09-25T14:17:54+00:00",
      "message": "Dernière donnée conservée ; source indisponible.",
      "status": "error",
      "url": "https://www.usda.gov/oce/commodity/wasde/wasde0926.txt"
    },
    "wti": {
      "as_of": "2026-09-22",
      "checked_at": "2026-09-25T14:17:54+00:00",
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
      for (const [title, url] of [['TTF spot ↗',marketLinks[0].url],['PEG France ↗',marketLinks[2].url],
                                  ['JKM future ↗',marketLinks[3].url]]) {
        const anchor = document.createElement('a');
        anchor.href = url;
        anchor.target = '_blank';
        anchor.rel = 'noopener noreferrer';
        anchor.append(line(title, 'b'));
        anchor.append(line('Prix à consulter sur la source', 'small'));
        box.append(anchor);
      }
    }

    function renderWatch() {
      const box = document.getElementById('watch-list');
      box.append(line('PRIX SPOT · OBSERVATIONS EIA', 'div', 'watch-group'));
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
      box.append(line('GAZ EUROPÉEN ET GNL · COTATIONS', 'div', 'watch-group'));
      for (const item of marketLinks) {
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
      box.append(line('L’écart JKM–TTF exige deux échéances identiques et une conversion $/MMBtu ↔ €/MWh ; aucun spread fictif n’est affiché.', 'div', 'caption'));
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
    renderWatch();
    renderAgenda();
    renderMini();
    renderMarketSummary();
    renderReleases();
    renderStories();
    renderSector();
    renderPower();
  </script>
</body>
</html>

```
