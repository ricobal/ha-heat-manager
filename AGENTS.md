# AGENTS.md

## Projet

Ce dépôt contient la configuration Home Assistant utilisée notamment pour le projet **Heat Manager**.

Heat Manager a pour objectif de gérer le chauffage pièce par pièce à partir de vannes thermostatiques Zigbee, tout en conservant une logique cohérente avec le chauffage central piloté par une PAC Atlantic Alféa M Duo.

L'objectif principal lors des interventions Codex est de réaliser des modifications **minimales, sûres, lisibles et réversibles**.

---

## Structure principale du repository

Le projet Heat Manager est principalement organisé dans :

- `packages/` : logique Home Assistant / packages Heat Manager
- `lovelace/` : interface utilisateur Heat Manager
- `examples/` : exemples de configuration ou d'utilisation
- `tools/` : outils de génération ou maintenance

Pour toute tâche Heat Manager :

1. commencer par lire `docs/HEAT_MANAGER_ARCHITECTURE.md` ;
2. identifier ensuite le sous-dossier concerné ;
3. ne pas explorer les autres dossiers sans dépendance réelle.

Ne pas supposer que la configuration Home Assistant globale
(`configuration.yaml`, `automations.yaml`, etc.) est présente dans ce repository.


## Environnement

### Home Assistant

* Home Assistant OS
* Installation dans une VM sur NAS Synology DS218+
* Configuration principalement en YAML
* Interface principalement utilisée sur téléphone en mode portrait
* Thème/interface basée sur Mushroom lorsque pertinent

### Zigbee / MQTT

* Zigbee2MQTT
* Mosquitto MQTT
* Coordinateur Zigbee : SLZB-06 connecté en TCP/IP
* Environ 40 à 50 équipements Zigbee
* Environ 13 vannes thermostatiques Sonoff TRVZB utilisées par Heat Manager

### Chauffage

* PAC Atlantic Alféa M Duo R290 triphasée
* Radiateurs à eau
* Thermostat central Navilink 228
* Thermostat principal situé dans le salon
* Régulation Atlantic en mode Smart Adapt
* Consigne centrale habituelle : environ 19 °C
* Certaines pièces disposent de vannes thermostatiques connectées
* Tous les radiateurs ne disposent pas nécessairement d'une vanne connectée

Heat Manager ne pilote pas directement la logique interne de régulation de la PAC sauf si cela est explicitement prévu dans les fichiers concernés.

---

## Principe de travail

Avant toute modification :

1. identifier précisément la fonctionnalité concernée ;
2. identifier les fichiers strictement nécessaires ;
3. lire uniquement ces fichiers et leurs dépendances directes ;
4. comprendre le fonctionnement actuel ;
5. proposer ou réaliser le changement minimal ;
6. vérifier la syntaxe YAML ;
7. vérifier les références aux entités, scripts, helpers et groupes concernés ;
8. éviter toute modification non nécessaire.

Ne pas parcourir l'ensemble du repository par défaut.

Ne lire d'autres fichiers que lorsqu'une dépendance réelle a été identifiée.

---

## Priorité à l'économie de contexte

Le repository peut contenir beaucoup de configuration Home Assistant sans rapport direct avec Heat Manager.

Pour toute tâche Heat Manager :

* commencer par `docs/HEAT_MANAGER_ARCHITECTURE.md`;
* consulter `docs/AUDIT_HEAT_MANAGER.md` si la tâche concerne l'audit ou un problème déjà identifié ;
* rechercher ensuite uniquement les fichiers cités par ces documents ou nécessaires à la fonctionnalité demandée ;
* ne pas reconstruire l'architecture complète du projet à chaque tâche.

Lorsqu'une information importante sur l'architecture est découverte ou modifiée, mettre à jour `docs/HEAT_MANAGER_ARCHITECTURE.md`.

Lorsqu'un point d'audit est traité, mettre à jour `docs/AUDIT_HEAT_MANAGER.md`.

---

## Règles de modification

### Toujours

* préserver les `entity_id` existants sauf nécessité démontrée ;
* préserver les noms des scripts, helpers et groupes lorsqu'ils sont déjà utilisés ailleurs ;
* privilégier un changement local plutôt qu'un refactoring global ;
* conserver le fonctionnement existant qui n'est pas directement concerné par la demande ;
* utiliser une indentation YAML correcte ;
* privilégier les fonctions natives Home Assistant ;
* commenter uniquement lorsque le commentaire apporte une information durable.

### Ne jamais faire sans demande explicite

* refactorer tout le projet ;
* réorganiser tous les fichiers YAML ;
* renommer massivement les entités ;
* modifier la configuration Zigbee2MQTT ;
* modifier le réseau Zigbee ;
* modifier Mosquitto ;
* modifier le coordinateur SLZB-06 ;
* modifier la configuration de la PAC ;
* supprimer une automatisation ou un helper simplement parce qu'il semble inutilisé ;
* réécrire un fichier complet lorsqu'une modification de quelques lignes suffit.

---

## Sécurité des modifications

Les changements doivent être réversibles.

En cas de doute entre plusieurs solutions :

1. privilégier celle qui modifie le moins de composants ;
2. éviter les dépendances supplémentaires ;
3. éviter les comportements implicites difficiles à diagnostiquer ;
4. privilégier une logique observable dans Home Assistant.

Ne jamais effectuer un changement risqué uniquement pour "essayer".

---

## Fichiers potentiellement importants

Selon la structure réelle du dépôt :

* `configuration.yaml`
* `automations.yaml`
* `scripts.yaml`
* `groups.yaml`
* `template.yaml`
* `sensors.yaml`
* dashboards YAML éventuels
* packages Home Assistant éventuels
* fichiers spécifiques Heat Manager

Ne pas supposer que tous ces fichiers sont nécessaires à chaque tâche.

Effectuer une recherche ciblée avant de les lire.

---

## Groupes fonctionnels Heat Manager

La configuration comporte ou doit pouvoir gérer les zones suivantes :

* Chambres inoccupées

  * Chambre Julie
  * Chambre Pablo
  * Grande chambre d'amis
  * Petite chambre d'amis

* Chambre Mathias

* SDB Mathias / garçons

* SDB Julie

* Chambre parents

* Dressing

* SDB parents

* Sous-sol

  * Atelier
  * Salle cinéma

* Buanderie

La liste exacte des `entity_id` doit être obtenue depuis la configuration du repository et non inventée.

---

## Fonctionnalités attendues

Heat Manager doit permettre, selon l'état d'avancement réel du projet :

* contrôle des vannes individuellement ;
* contrôle par groupes de pièces ;
* réglage d'une température de consigne ;
* plage de température approximative de 4 °C à 35 °C ;
* pas de réglage de 0,5 °C lorsque l'équipement le permet ;
* choix de modes compatibles avec les TRVZB ;
* gestion d'un override individuel ;
* gestion d'un override de groupe ;
* retour au fonctionnement automatique ;
* interface adaptée à un écran mobile en portrait.

Toujours vérifier la configuration réelle avant de considérer qu'une fonctionnalité est déjà implémentée.

---

## Audit

Lorsqu'une tâche demande un audit :

1. ne modifier aucun fichier dans un premier temps ;
2. identifier les fichiers réellement concernés ;
3. analyser la logique existante ;
4. classer les observations selon :

   * critique ;
   * important ;
   * amélioration ;
5. distinguer :

   * bug réel ;
   * risque potentiel ;
   * dette technique ;
   * amélioration esthétique ;
6. fournir les références précises aux fichiers et sections concernées.

Un comportement inhabituel n'est pas nécessairement un bug.

Ne pas proposer de refactoring tant qu'une correction locale est suffisante.

---

## Diagnostic Home Assistant

En cas de problème de fonctionnement, distinguer :

* symptôme ;
* cause probable ;
* conséquence ;
* erreur secondaire.

Si des logs sont disponibles, rechercher en priorité :

* erreurs répétitives ;
* timeouts ;
* entités indisponibles ;
* appels de services échoués ;
* automatisations déclenchées mais non exécutées ;
* templates en erreur ;
* conflits entre automatisations ;
* boucles de changement d'état.

Ne pas considérer automatiquement une erreur Zigbee ou MQTT comme la cause principale d'un problème Heat Manager.

---

## Validation

Après une modification :

1. vérifier le YAML ;
2. rechercher les références aux éléments modifiés ;
3. vérifier que les `entity_id` référencés existent ;
4. vérifier les appels de services Home Assistant ;
5. vérifier les templates ;
6. vérifier les conditions et déclencheurs ;
7. indiquer clairement ce qui a été modifié ;
8. indiquer ce qui n'a pas été testé.

Ne pas lancer un audit général du repository après une petite modification locale.

---

## Format des réponses Codex

Pour une analyse :

### Diagnostic

Résumé en quelques lignes.

### Fichiers concernés

Liste courte.

### Cause

Explication technique.

### Correction proposée

Modification minimale.

### Risques

Seulement les risques réellement identifiés.

Pour une modification :

### Modifications

Résumé des changements.

### Validation

Tests ou contrôles réalisés.

### À tester dans Home Assistant

Étapes courtes permettant de vérifier le comportement réel.

Éviter les longues explications lorsqu'elles ne sont pas nécessaires.
