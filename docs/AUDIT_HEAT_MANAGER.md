# Suivi de l’analyse Heat Manager

## État au 20 septembre 2026

**Phase réalisée : cartographie statique de l’architecture uniquement. Audit fonctionnel complet non commencé.**

Périmètre : sous-dépôt `ha-heat-manager`, révision observée `981ef44`. Le détail des composants et des flux figure dans [HEAT_MANAGER_ARCHITECTURE.md](HEAT_MANAGER_ARCHITECTURE.md).

Les deux documents étaient absents lors de la première lecture. L’utilisateur a confirmé leur création dans `ha-heat-manager/docs/`. Initialement absent, `AGENTS.md` a été trouvé et lu lors de la reprise demandée par l’utilisateur. Aucun fichier de consignes n’a été créé ou modifié par cette intervention.

## Sources examinées

| Source | Lecture architecturale réalisée |
|---|---|
| `AGENTS.md` | Consignes de travail, contexte d’installation déclaré et distinction entre fonctionnalités attendues et implémentées |
| `packages/heat_manager_trvzb.yaml` | Domaines, helpers, templates, scripts, déclencheur et services appelés |
| `lovelace/heat_manager_mobile_views.yaml` | Structure des vues, navigation, références d’entités et actions exposées |
| `tools/generate_heat_manager_dashboard.py` | Constantes, inventaire pièces/zones, fonctions de construction, sérialisation et sortie |
| `examples/ecs_hours_offpeak_automation.yaml` | Déclencheurs, dépendances ECS et séparation du package |
| `README.md` et inventaire Git | Frontière du projet, prérequis déclarés et procédure d’installation |

## Résultats de cartographie

- Un package TRVZB : 44 helpers (4 nombres, 1 sélecteur, 39 textes), 10 capteurs de synthèse, 1 capteur binaire, 3 scripts et 1 automatisation.
- Treize pièces réparties dans quatre zones d’interface ; les commandes ciblées de boost et planning opèrent à la pièce.
- Un générateur Python et son artefact de 39 vues ; les listes du package et l’inventaire du générateur sont maintenus séparément.
- Des commandes PAC, ECS et absence directement reliées aux entités externes Alféa M.
- Un exemple ECS indépendant, avec son propre déclencheur au démarrage.
- Aucun lien de commande demande TRVZB → PAC défini dans les fichiers examinés.

Ces constats décrivent la structure présente. Ils ne sont ni des anomalies qualifiées, ni une validation fonctionnelle.

La reprise après lecture de `AGENTS.md` complète le contexte d’installation dans le document d’architecture. Les fonctionnalités de contrôle et d’override de groupes mentionnées comme attentes ne sont pas assimilées à des fonctions implémentées. Aucun audit supplémentaire n’a été entrepris.

## Frontières à conserver pour une analyse ultérieure

| Interface | Éléments repérés ; vérification fonctionnelle différée |
|---|---|
| Package ↔ entités des vannes | Identifiants, services `climate`, `text`, `number`, `select` et capacités effectivement exposées |
| Planning ↔ helpers ↔ vanne | Trois champs par pièce, sept écritures quotidiennes et passage en Auto |
| Commandes globales ↔ commandes de pièce | Modes `restart` / `queued`, profils, boost et consignes |
| Générateur ↔ YAML versionné | Source Python et sortie distinctes ; régénération et équivalence non vérifiées |
| Interface ↔ package | Références des cartes, helpers affichés et scripts effectivement utilisés ; auxiliaire `mode_chips()` hors construction actuelle |
| Identifiants historiques ↔ registre HA | `sdb_garcons` associé au planning `sdb_mathias` et `unique_id` historique de synthèse |
| ECS ↔ installation | Import optionnel et identifiant d’automatisation attendu par `ECS_AUTOMATION` |
| Dépôt ↔ configuration déployée | Copies homonymes dans le répertoire parent ; synchronisation et activation non établies |

Cette liste conserve les points de jonction de l’architecture pour une éventuelle phase suivante. Elle ne constitue pas un audit de ces interfaces et ne propose aucune correction.

## Vérifications et limites de cette phase

L’inventaire et les dénombrements reposent sur la lecture des sources et des déclarations de vues. Aucun scénario métier, template Jinja ou service Home Assistant n’a été exécuté. Aucune vérification de configuration Home Assistant, simulation de panne, commande matérielle, consultation du registre réel ou validation visuelle Lovelace n’a été réalisée.

Le générateur n’a pas été lancé et aucun fichier de code, de configuration ou d’artefact généré n’a été modifié. Les seuls fichiers créés pour cette phase sont les deux documents dans `docs/`. Aucun déploiement ou redémarrage n’a été effectué. Aucun verdict de conformité ou de bon fonctionnement n’est rendu.
