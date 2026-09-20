# Heat Manager . Architecture

## 1. Objectif

Heat Manager est le système de gestion du chauffage pièce par pièce dans Home Assistant.

Il complète le système de chauffage central existant sans remplacer la régulation interne de la PAC Atlantic.

Le projet doit notamment permettre :

* le pilotage des vannes thermostatiques connectées ;
* la création de groupes fonctionnels ;
* le réglage de consignes par pièce ou groupe ;
* des overrides manuels ;
* le retour simple au fonctionnement automatique ;
* une utilisation facile depuis un smartphone.

---

# 2. Architecture chauffage

## Production de chaleur

PAC :

**Atlantic Alféa M Duo R290**

Caractéristiques principales :

* installation triphasée ;
* chauffage par radiateurs à eau ;
* production ECS intégrée ;
* régulation Atlantic en mode Smart Adapt.

## Thermostat central

Thermostat :

**Atlantic Navilink 228**

Localisation :

**salon**

La zone salon est ouverte ou fortement connectée avec :

* salon ;
* salle à manger ;
* cuisine.

Consigne centrale habituelle :

**19 °C environ**

Le thermostat central reste un élément important de la demande globale de chauffage faite à la PAC.

Heat Manager ne doit donc pas être considéré comme un système pouvant demander directement de la chaleur à la PAC dans chaque pièce, sauf si une telle fonction est explicitement développée.

---

# 3. Vannes thermostatiques

Environ 13 vannes thermostatiques connectées sont utilisées.

Modèle principal :

**Sonoff TRVZB**

Transport :

```text
TRVZB
  ↓
Zigbee
  ↓
Zigbee2MQTT
  ↓
MQTT
  ↓
Home Assistant
  ↓
Heat Manager
```

Coordinateur Zigbee :

**SLZB-06**

Connexion :

**TCP/IP**

Broker :

**Mosquitto MQTT**

---

# 4. Groupes fonctionnels

Les vannes sont organisées en groupes correspondant aux usages de la maison.

## Chambres inoccupées

* Chambre Julie
* Chambre Pablo
* Grande chambre d'amis
* Petite chambre d'amis

## Chambre Mathias

* Chambre Mathias

## SDB Mathias

* Salle de bain Mathias / garçons

## SDB Julie

* Salle de bain Julie

## Chambre parents

* Chambre parents

## Dressing

* Dressing

## SDB parents

* Salle de bain parents

## Sous-sol

* Atelier
* Salle cinéma

## Buanderie

* Buanderie

Les noms exacts des entités Home Assistant doivent être récupérés depuis la configuration.

Ce document ne doit pas servir à inventer les `entity_id`.

---

# 5. Principes de contrôle

Heat Manager doit distinguer deux niveaux.

## Contrôle individuel

Une vanne peut être pilotée indépendamment :

* mode ;
* température ;
* override manuel.

## Contrôle de groupe

Une commande appliquée à un groupe doit pouvoir agir sur les vannes appartenant à ce groupe.

Exemples :

* régler les chambres inoccupées à une température donnée ;
* réduire le chauffage du sous-sol ;
* imposer temporairement une température à la buanderie.

---

# 6. Modes

Les modes réellement disponibles doivent être dérivés des entités Zigbee2MQTT / Home Assistant.

Les modes utilisés historiquement dans le projet comprennent notamment des notions de :

* off ;
* heat ;
* auto ;

ou modes équivalents exposés par les vannes.

Ne jamais coder en dur un mode avant d'avoir vérifié qu'il est réellement accepté par l'entité concernée.

---

# 7. Température de consigne

Plage cible utilisée pour l'interface Heat Manager :

```text
4 °C → 35 °C
```

Pas :

```text
0,5 °C
```

La valeur minimale de 4 °C permet notamment de conserver une logique hors-gel.

Les limites réelles de chaque appareil restent prioritaires.

---

# 8. Override

L'architecture Heat Manager doit pouvoir gérer deux types d'override.

## Override individuel

Permet de prendre temporairement le contrôle d'une vanne particulière.

Exemple :

```text
Groupe Chambres inoccupées = 16 °C

mais

Chambre Julie = 19 °C en override
```

La logique de groupe ne doit pas immédiatement écraser cet override si le système prévoit explicitement sa conservation.

## Override groupe

Permet de modifier temporairement le comportement de toutes les vannes d'un groupe.

Exemple :

```text
Sous-sol
Override = 15 °C
```

L'override doit pouvoir être supprimé pour revenir au fonctionnement automatique.

---

# 9. Hiérarchie logique cible

Lorsqu'elle est implémentée, la logique doit rester explicite.

Une hiérarchie possible est :

```text
Override individuel
        ↓
Override groupe
        ↓
Consigne automatique du groupe
        ↓
Consigne normale de la vanne
```

Cette hiérarchie doit toutefois être vérifiée dans la configuration réelle avant toute modification.

Codex ne doit pas considérer ce schéma comme nécessairement déjà implémenté.

---

# 10. Interface utilisateur

L'utilisation principale est sur smartphone en mode portrait.

Les principes d'interface sont :

* affichage compact ;
* lisibilité immédiate ;
* actions principales visibles sans ouvrir plusieurs sous-menus ;
* température affichée avec virgule lorsque possible ;
* cohérence avec les cartes Mushroom ;
* distinction claire entre fonctionnement automatique et override.

Une ancienne vue appelée **Chauffage** a servi de vue de test.

Elle ne doit pas être considérée automatiquement comme l'architecture UI définitive.

---

# 11. Intégration avec la PAC

La PAC et Heat Manager constituent deux niveaux différents.

```text
PAC + Navilink
        ↓
température de l'eau / chauffage central

Heat Manager
        ↓
débit autorisé dans chaque radiateur équipé
```

Une vanne TRVZB fermée réduit ou coupe le débit dans son radiateur.

Une vanne ouverte ne garantit pas que le radiateur chauffe.

Il faut également que :

* la PAC soit en fonctionnement ;
* le circuit fournisse de l'eau suffisamment chaude ;
* le débit hydraulique soit disponible.

---

# 12. Limitation fondamentale

Heat Manager ne connaît pas nécessairement directement la demande de chaleur de toutes les pièces du point de vue de la PAC.

Exemple :

```text
Salon = 19 °C
Navilink satisfait

Chambre = 17 °C
TRVZB demande 20 °C
```

Il est possible que la vanne de la chambre reste ouverte sans que la PAC continue à produire suffisamment de chaleur si la logique Navilink considère que la demande principale est satisfaite.

Ce point doit être conservé à l'esprit lors du diagnostic de comportements Heat Manager.

---

# 13. Architecture Home Assistant

Les éléments Heat Manager peuvent être répartis entre plusieurs types de configuration :

```text
helpers
templates
groups
scripts
automations
dashboard
```

Avant toute modification, rechercher les références réelles dans le repository.

Ne pas supposer l'emplacement d'une fonction à partir de son nom.

---

# 14. Tests

Un test simple déjà utilisé dans le projet concerne le groupe :

**Buanderie**

La buanderie peut servir de groupe pilote pour tester :

* changement de température ;
* mode ;
* override ;
* retour automatique.

Lorsqu'un test peut être réalisé sur une seule vanne ou un seul groupe, préférer ce test à une modification globale.

---

# 15. Principes d'évolution

Toute évolution Heat Manager doit respecter les règles suivantes :

1. modification minimale ;
2. fonctionnalité testable isolément ;
3. absence de dépendance inutile ;
4. comportement observable dans Home Assistant ;
5. possibilité de revenir facilement à la configuration précédente.

---

# 16. Documentation

Lorsqu'une évolution modifie :

* un groupe ;
* une hiérarchie d'override ;
* un helper ;
* une automatisation centrale ;
* l'architecture générale ;

mettre à jour ce document.

Les problèmes ponctuels, bugs et actions restantes doivent être consignés dans :

```text
docs/AUDIT_HEAT_MANAGER.md
```
