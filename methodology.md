# Méthodologie du Commodity Cockpit

## Ce que signifient les chiffres

| Étiquette | Sens | Exemple |
|---|---|---|
| Observé provisoire | Mesure publiée, susceptible de révision | Consommation et production RTE éCO2mix |
| Calculé | Opération déterministe sur des mesures datées | Demande résiduelle = consommation − éolien − solaire |
| Indicateur tiers | Cotation fournie par un widget externe, avec ses horaires et délais | Brent indicatif OANDA via TradingView |
| Repère daté | Publication officielle différée, sans prétention de temps réel | Spot Brent EIA, stockage GIE, récoltes USDA |
| Structurel | Estimation annuelle, inadaptée à un signal de séance | Production minière USGS |

Les niveaux de stockage, les débits, les cotations CFD, les prix spot quotidiens et les contrats à terme sont des objets distincts. Le site ne calcule pas de variation de prix à partir d'un seul chiffre physique. Les sources sans droit de rediffusion vérifié, notamment les cours live TTF, PEG, JKM et certains prix électriques, restent des liens explicites.

## Power France

Source : [RTE éCO2mix national temps réel](https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-national-tr/). L'ETL lit les pages les plus récentes, trie et valide les observations, puis conserve le dernier relevé de chaque heure UTC. Le fichier `data/power_fr.json` accumule les heures réellement reçues sur 365 jours glissants. Il ne remplit pas les trous. La première collecte ne crée donc pas artificiellement un an d'histoire. La courbe indique la couverture entre sa première et sa dernière observation affichées.

| Champ du site | Origine | Unité | Interprétation |
|---|---|---|---|
| Demande | `consommation` RTE | MW | Charge nationale observée |
| Gaz électrique | `gaz` RTE | MW | Puissance électrique produite à partir de gaz |
| Éolien + solaire | `eolien + solaire` RTE | MW | Somme de deux filières observées |
| Demande résiduelle | `consommation − eolien − solaire` | MW | Indicateur calculé de besoin restant ; ni prix ni production thermique obligée |
| Échanges nets | `ech_physiques` RTE | MW | Négatif : exportateur net ; positif : importateur net |

Le graphique 24 h de la page Power utilise les relevés au quart d'heure de l'instantané. Le graphique historique utilise les relevés horaires accumulés. Chaque graphique porte sa propre échelle ; deux courbes de graphiques différents ne sont pas directement comparables en hauteur. Une interruption de collecte n'est pas interpolée. Un relevé ancien est signalé comme archive.

Prévisions : ENTSO-E A65/A01 pour la France et DE-LU, avec le jeton du dépôt. Le pic affiché est la demande prévue, pas une consommation déjà réalisée. Les prix day-ahead ne sont pas déduits de ces prévisions.

Prix day-ahead : l'API Fraunhofer ISE Energy-Charts fournit les périodes de livraison France et DE-LU en EUR/MWh. L'ETL valide la mention `CC BY 4.0` dans la réponse avant de publier ; il cite la source et indique que les graphiques et indicateurs sont des transformations. `data/power_prices.json` accumule les seules périodes effectivement reçues sur 365 jours glissants. La moyenne de demain est arithmétique sur les périodes disponibles, et l'écart France − DE-LU apparie exclusivement des timestamps identiques. Un prix négatif est compté par période, pas par heure. Les graphiques utilisent le même axe monétaire pour les deux zones.

Le day-ahead est fixé la veille pour une période future. Le prix d'une période en cours n'est donc pas une cotation en direct. Le flux intraday continu EPEX n'a pas été collecté : ENTSO-E 12.1.d ne rend sa publication que facultative, et l'accès public à un résultat sur un site n'autorise pas automatiquement sa récupération ni sa redistribution. Le prix d'équilibrage / de règlement des écarts est un autre marché et n'est pas substitué à l'intraday. Les comparaisons avec la demande résiduelle RTE sont descriptives et portent sur la même période de livraison, sans prétendre démontrer une causalité.

## Autres séries et mise à jour

- Pétrole : prix spot quotidiens EIA datés ; courbe Brent/WTI sur 12 mois par FRED ou miroir public des séries EIA, avec provenance et date. Les widgets OANDA ont une autre définition de produit.
- Gaz : stockage France/UE GIE AGSI+ en pourcentage, deux pages d'historique pour comparer la saison précédente ; terminaux GNL GIE ALSI en volume et en émission. Un soutirage net positif réduit le stock, une injection nette l'augmente.
- Agriculture : estimations mensuelles USDA WASDE ; conditions et avancement des récoltes USDA NASS, comparés respectivement à N−1 et à la moyenne cinq ans selon le champ du rapport. Les liens météo ne sont pas présentés comme des mesures de récolte.
- Métaux : production annuelle estimée par l'USGS ; pas de stock LME fabriqué ni de signal de marché issu d'une estimation annuelle.

GitHub Actions lance `scripts/update_data.py` toutes les deux heures. Chaque source a son statut et sa date. Si une collecte échoue, la dernière mesure valide est conservée et marquée comme telle. Le HTML téléchargeable contient un instantané des données et l'historique Power ; son bouton « Actualiser les données » récupère les JSON les plus récents depuis GitHub si le navigateur peut y accéder. Les jetons restent dans les secrets GitHub Actions.
