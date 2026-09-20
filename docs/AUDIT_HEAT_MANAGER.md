# Heat Manager . Audit et suivi

## Objectif

Ce fichier sert de référence pour les audits et évolutions du projet Heat Manager.

Il permet à Codex de connaître les travaux déjà effectués sans devoir réanalyser l'ensemble du repository.

---

# Statuts

Utiliser les statuts suivants :

```text
[ ] non analysé
[~] analyse en cours
[!] problème identifié
[x] terminé / validé
[-] non applicable
```

---

# 1. Architecture générale

[ ] Identifier tous les fichiers réellement impliqués dans Heat Manager.

[ ] Identifier tous les helpers utilisés.

[ ] Identifier tous les scripts utilisés.

[ ] Identifier toutes les automatisations utilisées.

[ ] Identifier les templates utilisés.

[ ] Identifier les fichiers ou vues dashboard utilisés.

[ ] Vérifier qu'aucun ancien composant Heat Manager n'est encore actif inutilement.

---

# 2. Inventaire des vannes

[ ] Identifier les 13 vannes TRVZB.

[ ] Vérifier leurs `entity_id`.

[ ] Vérifier les noms affichés.

[ ] Vérifier leur disponibilité dans Home Assistant.

[ ] Vérifier les modes réellement disponibles.

[ ] Vérifier les températures minimale et maximale.

[ ] Vérifier le pas de réglage de température.

---

# 3. Groupes

## Chambres inoccupées

[ ] Chambre Julie

[ ] Chambre Pablo

[ ] Grande chambre d'amis

[ ] Petite chambre d'amis

[ ] Vérifier fonctionnement du groupe.

## Chambre Mathias

[ ] Vérifier configuration.

## SDB Mathias

[ ] Vérifier configuration.

## SDB Julie

[ ] Vérifier configuration.

## Chambre parents

[ ] Vérifier configuration.

## Dressing

[ ] Vérifier configuration.

## SDB parents

[ ] Vérifier configuration.

## Sous-sol

[ ] Atelier

[ ] Salle cinéma

[ ] Vérifier fonctionnement du groupe.

## Buanderie

[x] Groupe utilisé avec succès pour des tests initiaux.

[ ] Revalider après l'audit global.

---

# 4. Réglage de température

[ ] Vérifier plage 4 °C à 35 °C.

[ ] Vérifier pas de 0,5 °C.

[ ] Vérifier comportement sur chaque modèle d'entité climate.

[ ] Vérifier gestion des valeurs hors plage.

[ ] Vérifier absence de conversion ou arrondi incorrect.

---

# 5. Modes

[ ] Identifier précisément les modes exposés par TRVZB.

[ ] Vérifier les valeurs utilisées dans les scripts.

[ ] Vérifier les appels `climate.set_hvac_mode`.

[ ] Vérifier le mode utilisé pour le fonctionnement automatique.

[ ] Vérifier le comportement du mode off.

[ ] Vérifier qu'aucune valeur spécifique Zigbee2MQTT incorrecte n'est envoyée directement.

---

# 6. Override individuel

[ ] Identifier les helpers utilisés pour mémoriser un override.

[ ] Vérifier activation.

[ ] Vérifier modification de température.

[ ] Vérifier priorité sur la consigne de groupe.

[ ] Vérifier suppression de l'override.

[ ] Vérifier retour à l'automatisme.

[ ] Vérifier comportement après redémarrage Home Assistant.

---

# 7. Override groupe

[ ] Identifier les helpers utilisés.

[ ] Vérifier activation.

[ ] Vérifier température.

[ ] Vérifier propagation aux membres du groupe.

[ ] Vérifier suppression.

[ ] Vérifier retour à la consigne automatique.

[ ] Vérifier interaction avec un override individuel.

---

# 8. Priorité des consignes

Vérifier la hiérarchie réellement implémentée.

Hypothèse fonctionnelle cible :

```text
Override individuel
        ↓
Override groupe
        ↓
Consigne automatique groupe
        ↓
Consigne normale
```

[ ] Vérifier cette hiérarchie dans le code.

[ ] Documenter toute différence.

[ ] Vérifier qu'une automatisation ne réécrit pas immédiatement une consigne manuelle.

[ ] Vérifier les conditions évitant les boucles.

---

# 9. Automatisations

Pour chaque automatisation Heat Manager :

[ ] identifier son rôle ;

[ ] identifier ses triggers ;

[ ] identifier ses conditions ;

[ ] identifier ses actions ;

[ ] identifier les entités modifiées ;

[ ] vérifier les interactions avec les autres automatisations ;

[ ] rechercher les risques de boucle ;

[ ] rechercher les triggers trop larges ;

[ ] rechercher les appels inutiles ;

[ ] vérifier le comportement au redémarrage Home Assistant.

---

# 10. Scripts

Pour chaque script Heat Manager :

[ ] identifier les paramètres ;

[ ] identifier les entités ciblées ;

[ ] vérifier le comportement si une vanne est indisponible ;

[ ] vérifier les appels de services ;

[ ] vérifier les templates ;

[ ] rechercher les duplications évitables.

Ne refactorer les duplications que si elles posent réellement un problème de maintenance ou de fonctionnement.

---

# 11. Templates

[ ] Vérifier syntaxe.

[ ] Vérifier les références d'entités.

[ ] Vérifier les conversions numériques.

[ ] Vérifier gestion de `unknown`.

[ ] Vérifier gestion de `unavailable`.

[ ] Vérifier valeurs par défaut.

[ ] Vérifier absence de boucle entre capteurs template.

---

# 12. Home Assistant startup

[ ] Vérifier comportement après redémarrage HA.

[ ] Vérifier état initial des helpers.

[ ] Vérifier état initial des overrides.

[ ] Vérifier si une synchronisation automatique est nécessaire.

[ ] Vérifier qu'un redémarrage ne modifie pas les consignes de façon inattendue.

---

# 13. Zigbee2MQTT

L'audit Heat Manager ne doit pas devenir automatiquement un audit Zigbee.

Contrôler Zigbee2MQTT uniquement si un symptôme le justifie.

Si nécessaire :

[ ] vérifier disponibilité vanne ;

[ ] vérifier dernière communication ;

[ ] vérifier attributs exposés ;

[ ] vérifier erreurs répétitives ;

[ ] vérifier timeouts.

Ne pas modifier le réseau Zigbee ou le coordinateur sans diagnostic démontrant que cela est nécessaire.

---

# 14. Dashboard

Objectif :

interface mobile portrait claire et compacte.

[ ] Identifier la vue actuellement utilisée.

[ ] Distinguer vue de test et vue définitive.

[ ] Vérifier cartes Mushroom.

[ ] Vérifier affichage température actuelle.

[ ] Vérifier température de consigne.

[ ] Vérifier état automatique / override.

[ ] Vérifier commandes de groupe.

[ ] Vérifier commandes individuelles.

[ ] Vérifier comportement sur téléphone.

---

# 15. Cohérence avec la PAC

[ ] Vérifier qu'aucune logique Heat Manager ne suppose qu'une TRVZB peut directement déclencher la PAC si ce mécanisme n'existe pas.

[ ] Identifier éventuellement les informations PAC utilisées par Heat Manager.

[ ] Vérifier les dépendances avec les entités Atlantic.

[ ] Vérifier que les automatisations Heat Manager ne dépendent plus d'anciennes entités devenues obsolètes.

---

# 16. Entités obsolètes

[ ] Rechercher les anciennes références devenues inutiles.

[ ] Rechercher les helpers orphelins.

[ ] Rechercher les scripts non utilisés.

[ ] Rechercher les automatisations désactivées ou remplacées.

Ne supprimer aucun élément uniquement parce qu'aucune référence n'est trouvée dans une première recherche.

---

# 17. Tests fonctionnels

Effectuer les tests progressivement.

## Test 1 . Buanderie

[ ] changer température ;

[ ] vérifier TRVZB ;

[ ] activer override ;

[ ] changer override ;

[ ] supprimer override ;

[ ] vérifier retour automatique.

## Test 2 . Groupe multiple

Utiliser un groupe comportant plusieurs vannes.

[ ] changement de consigne ;

[ ] propagation ;

[ ] override individuel d'un membre ;

[ ] nouvelle consigne de groupe ;

[ ] vérifier priorité attendue ;

[ ] suppression override.

## Test 3 . Redémarrage

[ ] créer un état représentatif ;

[ ] redémarrer Home Assistant ;

[ ] vérifier conservation / reconstruction des états.

---

# 18. Performance

[ ] rechercher les automatisations déclenchées trop fréquemment ;

[ ] rechercher les templates recalculés inutilement ;

[ ] rechercher les appels de service envoyés alors que la valeur cible est déjà atteinte ;

[ ] vérifier absence de boucle de synchronisation.

Les optimisations de performance doivent être réalisées uniquement après validation fonctionnelle.

---

# 19. Documentation

[x] Création de `AGENTS.md`.

[x] Création de `docs/HEAT_MANAGER_ARCHITECTURE.md`.

[x] Création de `docs/AUDIT_HEAT_MANAGER.md`.

[ ] Mettre à jour l'architecture avec les vrais noms de fichiers.

[ ] Ajouter les vrais `entity_id`.

[ ] Ajouter les helpers réellement utilisés.

[ ] Ajouter les scripts et automatisations réellement utilisés.

---

# 20. Prochaine étape recommandée

Première tâche Codex :

```text
Lis AGENTS.md et docs/HEAT_MANAGER_ARCHITECTURE.md.

Effectue uniquement la section 1 "Architecture générale" de
docs/AUDIT_HEAT_MANAGER.md.

Objectif : cartographier la configuration Heat Manager existante.

Ne modifie aucune logique.
Ne parcours pas tout le repository sans nécessité.

Identifie :
- les fichiers concernés ;
- les helpers ;
- les scripts ;
- les automatisations ;
- les templates ;
- les dashboards ;
- les entités TRVZB.

Mets ensuite à jour uniquement :
- docs/HEAT_MANAGER_ARCHITECTURE.md
- docs/AUDIT_HEAT_MANAGER.md

Ne modifie aucun autre fichier.
```

Une fois cette cartographie terminée, traiter les sections suivantes séparément plutôt que de demander un audit global.
