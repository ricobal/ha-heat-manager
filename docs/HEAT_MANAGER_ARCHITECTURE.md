# Architecture actuelle de Heat Manager

Cartographie statique du 20 septembre 2026, établie sur le sous-dépôt `ha-heat-manager`, révision `981ef44`. Elle décrit les déclarations présentes dans les fichiers, sans validation du fonctionnement sur Home Assistant.

Les deux documents demandés étaient absents lors de la première lecture ; ils ont été créés dans `ha-heat-manager/docs/`, à la demande confirmée de l’utilisateur. Initialement absent, `AGENTS.md` est maintenant disponible et a été lu lors de la reprise. Les copies de fichiers situées dans les dossiers homonymes du répertoire parent ne constituent pas la source de cette cartographie ; leur synchronisation et leur déploiement ne sont pas établis.

## Contexte déclaré dans AGENTS.md

L’installation décrite utilise Home Assistant OS dans une VM sur un NAS Synology DS218+, Zigbee2MQTT, Mosquitto et un coordinateur SLZB-06 en TCP/IP. Le chauffage repose sur une PAC Atlantic Alféa M Duo R290 triphasée, des radiateurs à eau et un thermostat Navilink 228 situé dans le salon, avec régulation Smart Adapt et consigne centrale habituelle proche de 19 °C. Tous les radiateurs ne disposent pas nécessairement d’une vanne connectée. L’interface cible est un téléphone en portrait.

Ces informations proviennent des consignes du projet et ne sont pas des observations d’une installation active. Les contrôles et overrides de groupes cités parmi les fonctionnalités attendues dans `AGENTS.md` ne prouvent pas leur implémentation : la cartographie ci-dessous décrit les commandes de pièce, le mode maison et les zones de synthèse effectivement déclarés dans les sources.

Les consignes imposent une lecture ciblée, la préservation des identifiants et des changements minimaux. Cette phase reste limitée à la documentation, sans audit fonctionnel ni modification de configuration.

## 1. Organisation du dépôt

| Fichier | Responsabilité | Nature |
|---|---|---|
| `packages/heat_manager_trvzb.yaml` | Helpers, synthèses, demande de chauffage, scripts des vannes et réaction au mode maison | Configuration Home Assistant écrite directement |
| `tools/generate_heat_manager_dashboard.py` | Inventaire des pièces, zones, entités PAC/ECS, construction et sérialisation des vues | Source du tableau de bord |
| `lovelace/heat_manager_mobile_views.yaml` | Ensemble de 38 vues à fusionner dans `lovelace-mobile` | Artefact généré, versionné |
| `examples/ecs_hours_offpeak_automation.yaml` | Autorisation ECS selon les heures creuses | Automatisation optionnelle à installer séparément |
| `README.md` | Présentation, dépendances et installation manuelle | Documentation |

Chacun des quatre dossiers prioritaires contient un seul fichier dans le dépôt observé. Il ne contient ni intégration Home Assistant personnalisée, ni définition des équipements Zigbee, ni suite de tests ou chaîne CI versionnée.

## 2. Composants et flux

```mermaid
flowchart TD
    G["Générateur Python : ROOMS, ZONES, constantes"] -->|génération locale| L["38 vues Lovelace"]
    L -->|boost et planning par pièce| S["Scripts du package"]
    L -->|thermostat de pièce| V["Entités des 13 vannes"]
    H["Helpers : profils, durée, plannings"] --> S
    M["Helper mode maison"] --> A["Automatisation sur changement"]
    A --> S
    S -->|services climate, text, number, select| V
    V --> Z["Zigbee2MQTT / SONOFF TRVZB"]
    V --> T["Templates de synthèse et demande"]
    T -->|affichage de la demande| L
    V -->|synthèses des zones calculées dans les cartes| L
    L -->|commandes et consultation| P["Entités Atlantic Alféa M : PAC, ECS, absence"]
    E["Exemple ECS : horaires et démarrage HA"] -->|autorisation ECS| P
    P -->|état du cycle ECS| E
```

Le package pilote les vannes par les services Home Assistant ; il ne publie pas directement sur MQTT. Les entités nécessaires sont fournies par l’installation. Les commandes PAC, ECS et absence du tableau de bord utilisent directement les entités Alféa M, sans passer par les scripts TRVZB.

Le capteur de demande des vannes est consommé par l’interface. Aucune automatisation de ce dépôt ne le relie à une commande de la PAC. L’absence PAC, elle, est propagée aux vannes par l’automatisation `chauffage_absence_pac_vers_vannes` (section 3) ; le sens inverse (mode maison → PAC) n’existe pas.

## 3. Package TRVZB

Le fichier porte l’en-tête `v2.1.0-beta.2`. Ses domaines racine sont `input_number`, `input_select`, `input_text`, `template`, `script` et `automation`.

### État conservé dans les helpers

| Domaine | Nombre | Rôle |
|---|---:|---|
| `input_boolean` | 1 | `chauffage_panneau_absence_pac` : affichage seulement, ouvre le panneau des dates d’absence PAC sur l’écran principal |
| `input_number` | 2 | Profil absence et durée du boost |
| `input_select` | 1 | `chauffage_mode_maison` : Auto, Absence, Arrêt (Confort et Nuit retirés le 2026-09-22 : les plannings par pièce les remplacent) |
| `input_text` | 28 | Deux plannings par pièce : semaine, week-end ; `chauffage_modes_vannes_avant_absence` (modes des vannes à restaurer après une absence) ; plus `chauffage_mode_avant_absence` (mode à restaurer après une absence PAC) |

Les valeurs de référence sont commentées ; aucun `initial:` actif n’est déclaré. La restauration des états est confiée à Home Assistant. Les plannings sont des chaînes stockées dans les helpers puis transmises explicitement aux entités `text` des vannes.

### Capteurs calculés

Le bloc `template` déclare dix capteurs de synthèse : maison, chambres inoccupées, chambre Mathias, SDB garçons, SDB Julie, chambre parents, dressing, SDB parents, sous-sol et buanderie. Ils lisent températures, modes, activité et batteries ; leurs regroupements ne correspondent pas exactement aux quatre zones de navigation.

Le capteur binaire de demande a pour `unique_id` `chauffage_demande_chauffage`. Son expression compte les vannes en `auto` ou `heat` dont la consigne dépasse la mesure de plus de 0,5 °C, avec un `delay_on` de quinze minutes. Ses attributs exposent les nombres de pièces en demande et en forte demande (écart supérieur à 1 °C), l’écart maximum, la pièce correspondante et la liste des pièces en demande. Le tableau de bord le référence comme `binary_sensor.chauffage_demande_chauffage` ; le registre réel d’entités n’a pas été consulté.

### Points d’entrée de commande

| Script | Exécution | Entrées et services utilisés |
|---|---|---|
| `chauffage_appliquer_planning_cible` | `queued` | `cible` → correspondance pièce/vanne/slug → deux helpers → contrôle de format → sept `text.set_value` ; le mode de la vanne n’est pas modifié |
| `chauffage_boost_cible` | `queued` | `cible` et helper de durée → `number.set_value` sur la durée temporaire → `select.select_option` avec `boost` |
| `chauffage_mode_maison_appliquer` | `restart` | Lecture du mode maison et des profils → commandes collectives des treize vannes |

Le script planning contient une expression régulière pour un à six changements `HH:MM/température`, le premier à 00:00 (exigence Zigbee2MQTT TRVZB), entre 4 et 35 °C par pas de 0,5 °C. La semaine est copiée du lundi au vendredi, le week-end sur samedi et dimanche. Cette description ne vaut pas validation exhaustive du format ou du comportement des appareils.

Pour le mode maison, la branche Auto envoie `auto` ; Arrêt envoie une durée temporaire nulle, une consigne de 7 °C puis `off` ; le profil Absence passe par `climate.set_temperature` avec `hvac_mode: heat`. Le mode maison se choisit sur l’écran principal (trois boutons sous « Vannes thermostatiques ») ; Absence est aussi activé automatiquement par l’absence de la PAC. L’automatisation transmet le mode précédent (`precedent`) au script : au passage Auto → Absence, le mode de chaque vanne est mémorisé dans `input_text.chauffage_modes_vannes_avant_absence` (13 codes `a`, `o` ou `h<consigne>` dans l’ordre de `toutes_vannes`) ; au passage Absence → Auto, chaque vanne retrouve ce mode, puis la mémoire est vidée. Sans mémoire valide, Auto met les treize vannes en `auto`. Pendant une absence, les pages pièce affichent un bandeau bleu.

L’automatisation `chauffage_mode_maison_sur_changement` appelle ce dernier script lors d’une transition entre deux modes valides distincts. Aucun déclencheur de démarrage ou de retour de disponibilité n’y figure.

L’automatisation `chauffage_absence_pac_vers_vannes` suit l’état du capteur `sensor.atlantic_alfea_m_duo_absence`. Au passage à « Activée » (depuis « Désactivée » ou « En attente ») et si le mode maison est Auto, elle mémorise ce mode dans `input_text.chauffage_mode_avant_absence` puis passe le mode maison sur Absence ; l’automatisation précédente applique alors le profil Absence aux vannes. Au passage de « Activée » à « Désactivée », elle restaure le mode mémorisé si le mode maison est encore Absence, puis vide le helper. Le mode Arrêt n’est jamais modifié, et les passages par indisponible ou inconnu ne déclenchent rien. Le capteur reflète la période d’absence de l’installation Atlantic (rafraîchie chaque minute) : il change donc quand la période démarre ou se termine, pas au moment où le switch est actionné.

## 4. Pièces, zones et conventions d’entités

Les zones sont définies dans `ZONES` et les pièces dans `ROOMS` du générateur. Le package possède ses propres listes et dictionnaires de correspondance : il n’est pas généré à partir de `ROOMS`.

| Zone d’interface | Clé de pièce / cible | Base des entités de vanne | Slug du planning |
|---|---|---|---|
| Parents | `chambre_parents` | `radiateur_parents` | `chambre_parents` |
| Parents | `dressing` | `radiateur_dressing` | `dressing` |
| Parents | `sdb_parents` | `radiateur_sdb_parents` | `sdb_parents` |
| 1er étage | `chambre_julie` | `radiateur_chambre_julie` | `chambre_julie` |
| 1er étage | `chambre_pablo` | `radiateur_chambre_pablo` | `chambre_pablo` |
| 1er étage | `grande_chambre_amis` | `radiateur_grande_chambre_amis` | `grande_chambre_amis` |
| 1er étage | `petite_chambre_amis` | `radiateur_petite_chambre_amis` | `petite_chambre_amis` |
| 1er étage | `chambre_mathias` | `radiateur_chambre_mathias` | `chambre_mathias` |
| 1er étage | `sdb_garcons` | `radiateur_sdb_garcons` | `sdb_mathias` |
| 1er étage | `sdb_julie` | `radiateur_sdb_julie` | `sdb_julie` |
| Buanderie | `buanderie` | `radiateur_buanderie` | `buanderie` |
| Sous-sol | `atelier` | `radiateur_atelier` | `atelier` |
| Sous-sol | `salle_cine` | `radiateur_salle_cine` | `salle_cine` |

Pour chaque base, les interfaces attendues sont `climate.<base>`, `sensor.<base>_battery`, `text.<base>_weekly_schedule_<jour anglais>`, `number.<base>_temporary_mode_duration` et `select.<base>_temporary_mode_select`. Les helpers suivent `input_text.chauffage_planning_<slug>_<semaine|weekend>`.

Le slug historique `sdb_mathias` et le `unique_id` de synthèse `chauffage_sdb_mathias_resume` sont conservés pour la SDB garçons. Les zones ne constituent pas des cibles de scripts. Il existe néanmoins un capteur de synthèse du sous-sol dans le package.

## 5. Tableau de bord et génération

Le générateur utilise uniquement la bibliothèque standard Python (`json`, `pathlib`, `typing`). `build_views()` compose les vues ; `dump_yaml()` et `scalar()` assurent la sérialisation ; `main()` écrit le fichier Lovelace sous la racine du dépôt. Il ne contacte pas Home Assistant. Le générateur n’a pas été exécuté lors de cette cartographie.

Les 36 vues déclarées se répartissent en sept vues générales, trois vues de zones à plusieurs pièces, treize vues de pièces et treize vues de planning. Elles utilisent les Sections, une seule colonne, Mushroom et card-mod.

| Groupe | Routes sous `/lovelace-mobile/` |
|---|---|
| Accueil et paramètres | `chauffage-v2`, `chauffage-parametres` |
| PAC | `chauffage-pac-technique`, `chauffage-pac-diagnostic` (commandes, consigne et absence sur `chauffage-v2`) |
| ECS | `chauffage-ecs`, `chauffage-ecs-planning`, `chauffage-ecs-historique` |
| Zones | `chauffage-zone-parents`, `chauffage-zone-premier-etage`, `chauffage-zone-sous-sol` |
| Pièces et planning | `chauffage-piece-<clé avec tirets>`, `chauffage-planning-piece-<clé avec tirets>` |

La buanderie est accessible directement comme pièce. Les cartes de zones calculent leurs synthèses depuis les entités `climate`. Chaque pièce présente un thermostat, la batterie, le boost et l’accès au planning. Les paramètres exposent le profil Absence et la durée du boost. L’état du mode maison apparaît dans la carte globale ; le helper et son automatisation appartiennent au package.

La fonction auxiliaire `mode_chips()` référence `script.chauffage_appliquer_mode_cible`, mais n’est pas appelée par la construction actuelle des vues. Elle doit être distinguée des points d’entrée réellement présents dans l’artefact.

Les constantes du générateur fixent les identifiants PAC/ECS/absence sous `atlantic_alfea_m_duo_*`. Le chauffage utilise notamment le `climate` du circuit 1 et le `number` de consigne générale. L’accès et la vue du planning global PAC ont été retirés ; les sept capteurs quotidiens restent conservés dans Home Assistant pour une éventuelle réactivation. Le mode de fonctionnement de la PAC n’est pas modifié. L’absence utilise un switch et deux entités `datetime`. L’historique ECS s’appuie sur une carte `history-graph` de 72 heures ; son stockage historique relève de l’installation Home Assistant.

Depuis le 2026-09-22, les pages `chauffage-pac` et `chauffage-absence` sont supprimées : tout est sur l’écran principal. Marche, Absence et Arrêt forment une grille de trois boutons jointifs ; card-mod colore le fond selon le mode réel du climate (orange, gris ardoise) ou l’absence active (bleu). Absence n’agit pas sur la PAC : il ouvre ou ferme un panneau (état, début, fin, activation) piloté par `input_boolean.chauffage_panneau_absence_pac`. La consigne générale n’apparaît que PAC en marche. Suivent les températures intérieure et extérieure, l’accès à l’état technique, puis l’eau chaude.

## 6. Automatisation ECS séparée

L’exemple déclare quatre horaires (00:54, 07:24, 11:54, 13:24) et un déclencheur au démarrage de Home Assistant. Il active l’autorisation ECS au début des plages, ou au démarrage si une plage est en cours. Dans la branche de désactivation, il attend la fin du cycle actif, au maximum 90 minutes, puis coupe le switch. Son mode est `restart`.

Ses dépendances sont `switch.atlantic_alfea_m_duo_eau_chaude` et `binary_sensor.atlantic_alfea_m_duo_cycle_ecs_capacite_99`. Le tableau de bord attend l’entité `automation.gestion_eau_chaude_alfea_heures_creuses`, définie par la constante `ECS_AUTOMATION`. L’existence de cet identifiant après import n’est pas établie ici.

## 7. Frontière de déploiement

Le README prévoit l’inclusion des packages par `homeassistant.packages`, la copie du package et la fusion manuelle des vues dans le tableau de bord en mode stockage. L’exemple ECS est installé indépendamment. Les prérequis déclarés sont Home Assistant avec Sections, Mushroom, card-mod, Zigbee2MQTT, treize SONOFF TRVZB et le composant Atlantic Alféa M (version minimale annoncée : 0.1.0).

Les intégrations, ressources Lovelace, registre des entités, états restaurés et automatisations réellement actives sont extérieurs à ce dépôt. Cette cartographie ne confirme ni leur présence ni leur configuration. Le cadrage de la suite est consigné dans [AUDIT_HEAT_MANAGER.md](AUDIT_HEAT_MANAGER.md).
