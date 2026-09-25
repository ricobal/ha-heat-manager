# Arrosage Etherain et radio Russound (sans Node-RED)

Depuis le 2026-09-25, Node-RED n'est plus nécessaire : l'arrosage Etherain et les stations de radio Russound sont gérés directement par Home Assistant.

## Contenu du dépôt

- `packages/remplacement_nodered.yaml` : capteurs `rest` de l'état Etherain et action `shell_command.russound_touche` ;
- `packages/arrosage_manuel.yaml` : arrosage d'une zone pour une durée choisie depuis l'écran Arrosage ;
- `shell/russound_touche.py` : envoi des touches chiffre au Russound (à copier dans `/config/shell/`) ;
- `tools/generate_arrosage_dashboard.py` : source de la vue `arrosage` du tableau de bord `lovelace-mobile` ;
- `lovelace/arrosage_view.yaml` : vue générée.

Le fichier Lovelace est généré. Modifiez le générateur puis relancez-le au lieu d'éditer directement le fichier YAML produit.

## Etherain (192.168.1.81)

La page `result.cgi?xs` est lue toutes les 10 s. Les codes sont cherchés par leur nom (`os:`, `cs:`, `rz:`, `ri:`) et non par position : la page masque un champ quand aucune session n'est ouverte, ce qui décalait les positions utilisées par Node-RED.

| Capteur | Code | Valeurs |
|---|---|---|
| `sensor.etherain_statut_irrigation` | `os` | Arrêté, Arrosage programmé, Arrosage en cours |
| `sensor.etherain_statut_commande_irrigation` | `cs` | Ok, Erreur, Non autorisée |
| `sensor.etherain_resultat_commande_irrigation` | `rz` | Ok, Interrompu par pluie, Problème valve, Interrompu |
| `sensor.etherain_derniere_zone_arrosee` | `ri` + 1 | 1 à 5 |

Les capteurs ont été créés avec le suffixe « HA » puis renommés vers les `entity_id` de Node-RED : les capteurs binaires `binary_sensor.etherain_etat_zone_*` (`template.yaml`) et les automatisations des cycles n'ont pas changé.

Les commandes restent dans la configuration globale (`rest.yaml`, non versionné) : connexion, arrêt et cycles court, moyen et long. La connexion contient le mot de passe de l'Etherain et ne doit pas être publiée.

## Écran Arrosage

- bandeau d'état avec bouton Stop (confirmation) et barre d'avancement des 5 zones, toujours affichée ;
- cycles Court, Moyen et Long avec leur durée totale ; la roue crantée ouvre les durées des cycles ;
- zones dans l'ordre du cycle : Bureau, Salon, Cèdre, Chambre, Gouttes. Pendant un cycle, chaque zone est « Terminé », « En cours » ou « À venir » ;
- un appui sur une zone ouvre un sélecteur de durée, initialisé à 1 min. « Arroser » arrête un éventuel cycle puis lance la zone.

card-mod ne s'applique pas directement à une carte `grid` du tableau de bord : les grilles stylées sont enveloppées dans `custom:mod-card`.

## Radio Russound (passerelle RNET 192.168.1.74:4999)

Les 12 scripts `radio_*` de `scripts.yaml` (configuration globale) appellent :

```yaml
- action: shell_command.russound_touche
  data:
    touche: "10590"
```

Toutes les touches partent sur une seule connexion, à 5 ms d'intervalle. Un envoi d'une touche par appel (~270 ms entre deux touches) ne change pas de station.

## Supprimé le 2026-09-25

- 5 durées manuelles `input_number.etherain_temps_arrosage_zone_*` ;
- 5 interrupteurs `switch.etherain_zone_*` (`template.yaml`) ;
- 5 scripts `etherain_demarrer_zone_*` et 5 commandes `rest_command.etherain_irrigation_zone_*` ;
- 5 booléens `input_boolean.etherain_zone_*` et le script « Etherain tous off » ;
- section « Arrosage manuel par zone » de la page des paramètres d'arrosage.
