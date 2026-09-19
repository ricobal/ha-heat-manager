# Heat Manager pour Home Assistant

Heat Manager réunit dans une interface mobile la pompe à chaleur Atlantic Alféa M, l’eau chaude sanitaire et 13 vannes SONOFF TRVZB pilotées par Zigbee2MQTT.

Le projet est préparé pour l’installation Home Assistant décrite ci-dessous. Vérifiez les identifiants d’entités avant de l’utiliser sur une autre installation.

## Fonctions

- commandes générales de la PAC : `Auto`, `Marche` et `Arrêt` ;
- réglage de la consigne générale Alféa M ;
- consultation du planning chauffage global ;
- commande d’autorisation et de Boost de l’ECS ;
- historique ECS sur 72 heures avec autorisation et température de l’eau ;
- programmation du mode absence avec dates de début et de fin ;
- pression, températures, connexion, Wi-Fi et consommations de la PAC ;
- mode global des 13 vannes : Auto, Confort, Nuit, Absence ou Arrêt ;
- boost et planning propres à chaque pièce ;
- synthèse des zones sans commande commune.

## Navigation mobile

La page principale montre la PAC, l’ECS, l’absence, la demande des vannes et quatre zones :

1. Zone parents ;
2. 1er étage ;
3. Buanderie ;
4. Sous-sol.

Une zone contenant plusieurs pièces ouvre uniquement leur liste. Toutes les commandes sont effectuées dans la pièce. Comme la zone Buanderie ne contient qu’une pièce, elle ouvre directement le thermostat de la buanderie.

Les synthèses de zone sont calculées directement dans les cartes à partir des entités `climate`. Le package ne crée aucun helper, planning, script ou capteur de commande au niveau d’une zone.

## Contenu du dépôt

- `packages/heat_manager_trvzb.yaml` : helpers, capteurs, scripts et automatisation globale des vannes ;
- `lovelace/heat_manager_mobile_views.yaml` : 39 vues Lovelace générées ;
- `tools/generate_heat_manager_dashboard.py` : source du tableau de bord ;
- `examples/ecs_hours_offpeak_automation.yaml` : automatisation ECS optionnelle.

Le fichier Lovelace est généré. Modifiez le générateur puis relancez-le au lieu d’éditer directement le fichier YAML produit.

## Prérequis

- Home Assistant avec prise en charge des vues Sections ;
- Mushroom installé par HACS ;
- Zigbee2MQTT et les 13 vannes SONOFF TRVZB ;
- composant personnalisé [Atlantic Alféa M](https://github.com/ricobal/ha-alfea-m), version `0.1.0` ou ultérieure ;
- inclusion des packages Home Assistant :

```yaml
homeassistant:
  packages: !include_dir_named packages
```

## Installation

1. Créez une sauvegarde complète de Home Assistant.
2. Copiez `packages/heat_manager_trvzb.yaml` dans `/config/packages/`.
3. Lancez **Outils de développement > YAML > Vérifier la configuration**.
4. Redémarrez Home Assistant uniquement si la vérification réussit.
5. Renseignez les profils et les plannings des pièces avant de les appliquer.
6. Dans la configuration brute du tableau de bord `lovelace-mobile`, fusionnez les éléments placés sous `views:` dans `lovelace/heat_manager_mobile_views.yaml`.

Le package ne contient aucun `initial:` actif et n’envoie aucune commande aux vannes au démarrage.

## Automatisation ECS

L’exemple `examples/ecs_hours_offpeak_automation.yaml` autorise l’ECS pendant :

- 00:54 à 07:24 ;
- 11:54 à 13:24.

Si un cycle est encore actif à la fin d’une plage, il attend son arrêt pendant 90 minutes au maximum avant de couper l’autorisation ECS.

L’automatisation est volontairement séparée du package. Si une automatisation équivalente existe déjà, conservez-en une seule. Le tableau de bord s’attend à l’identifiant :

```text
automation.gestion_eau_chaude_alfea_heures_creuses
```

Adaptez la constante `ECS_AUTOMATION` du générateur si Home Assistant lui a attribué un autre identifiant.

## Planning global de la PAC

Les sept programmes quotidiens de l’Alféa M sont affichés dans le tableau de bord. Les composants `alfea_m` et `cozytouch` les exposent actuellement comme capteurs en lecture seule. Le tableau de bord ne prétend donc pas pouvoir les enregistrer.

Une modification depuis Home Assistant nécessitera l’ajout et la validation d’un service d’écriture dans le composant Alféa M. En attendant, le planning global doit être modifié dans Cozytouch.

## Plannings des vannes

Chaque pièce dispose de trois champs : semaine, samedi et dimanche. Chaque champ contient exactement six changements au format Zigbee2MQTT :

```text
00:00/17 06:30/19 08:30/16 12:00/16 17:30/19 22:30/17
```

Le script valide les heures, les températures de 4 à 35 °C et les pas de 0,5 °C. Il copie ensuite le planning vers les sept jours de la vanne et active son mode Auto.

## Développement

Regénérez les vues avec :

```powershell
python tools/generate_heat_manager_dashboard.py
```

Avant publication, contrôlez la configuration dans Home Assistant. Le dépôt ne contient pas Home Assistant Core et ne peut donc pas reproduire localement la validation complète de sa configuration.
