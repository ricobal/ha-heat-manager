"""Generate the local Lovelace proposal for Heat Manager.

The generated file is a bundle of views to merge later into the existing
storage-mode ``lovelace-mobile`` dashboard.  It never writes to Home Assistant.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "lovelace" / "heat_manager_mobile_views.yaml"
DASHBOARD = "/lovelace-mobile"

PAC_CLIMATE = "climate.atlantic_alfea_m_duo_chauffage_circuit_1"
PAC_SETPOINT = "number.atlantic_alfea_m_duo_temperature_de_consigne"
PAC_THERMOSTAT = "sensor.atlantic_alfea_m_duo_temperature_thermostat_z1"
PAC_OUTDOOR = "sensor.atlantic_alfea_m_duo_temperature_exterieure"
ECS_SWITCH = "switch.atlantic_alfea_m_duo_eau_chaude"
ECS_BOOST = "switch.atlantic_alfea_m_duo_boost_ecs"
ECS_CYCLE = "binary_sensor.atlantic_alfea_m_duo_cycle_ecs_capacite_99"
ECS_TEMPERATURE = "sensor.atlantic_alfea_m_duo_temperature_ecs"
ABSENCE_SWITCH = "switch.atlantic_alfea_m_duo_absence"
ABSENCE_START = "datetime.atlantic_alfea_m_duo_debut_absence"
ABSENCE_END = "datetime.atlantic_alfea_m_duo_fin_absence"
ECS_AUTOMATION = "automation.gestion_eau_chaude_alfea_heures_creuses"


ROOMS = {
    "chambre_parents": {
        "title": "Chambre parents",
        "entity": "climate.radiateur_parents",
        "base": "radiateur_parents",
        "planning": "chambre_parents",
        "icon": "mdi:bed-king-outline",
    },
    "dressing": {
        "title": "Dressing",
        "entity": "climate.radiateur_dressing",
        "base": "radiateur_dressing",
        "planning": "dressing",
        "icon": "mdi:hanger",
    },
    "sdb_parents": {
        "title": "SDB parents",
        "entity": "climate.radiateur_sdb_parents",
        "base": "radiateur_sdb_parents",
        "planning": "sdb_parents",
        "icon": "mdi:shower-head",
    },
    "chambre_julie": {
        "title": "Chambre Julie",
        "entity": "climate.radiateur_chambre_julie",
        "base": "radiateur_chambre_julie",
        "planning": "chambre_julie",
        "icon": "mdi:bed-outline",
    },
    "chambre_pablo": {
        "title": "Chambre Pablo",
        "entity": "climate.radiateur_chambre_pablo",
        "base": "radiateur_chambre_pablo",
        "planning": "chambre_pablo",
        "icon": "mdi:bed-outline",
    },
    "grande_chambre_amis": {
        "title": "Grande chambre amis",
        "entity": "climate.radiateur_grande_chambre_amis",
        "base": "radiateur_grande_chambre_amis",
        "planning": "grande_chambre_amis",
        "icon": "mdi:bed-empty",
    },
    "petite_chambre_amis": {
        "title": "Petite chambre amis",
        "entity": "climate.radiateur_petite_chambre_amis",
        "base": "radiateur_petite_chambre_amis",
        "planning": "petite_chambre_amis",
        "icon": "mdi:bed-empty",
    },
    "chambre_mathias": {
        "title": "Chambre Mathias",
        "entity": "climate.radiateur_chambre_mathias",
        "base": "radiateur_chambre_mathias",
        "planning": "chambre_mathias",
        "icon": "mdi:bed",
    },
    "sdb_garcons": {
        "title": "SDB garçons",
        "entity": "climate.radiateur_sdb_garcons",
        "base": "radiateur_sdb_garcons",
        "planning": "sdb_mathias",
        "icon": "mdi:shower-head",
    },
    "sdb_julie": {
        "title": "SDB Julie",
        "entity": "climate.radiateur_sdb_julie",
        "base": "radiateur_sdb_julie",
        "planning": "sdb_julie",
        "icon": "mdi:shower-head",
    },
    "buanderie": {
        "title": "Buanderie",
        "entity": "climate.radiateur_buanderie",
        "base": "radiateur_buanderie",
        "planning": "buanderie",
        "icon": "mdi:washing-machine",
    },
    "atelier": {
        "title": "Atelier",
        "entity": "climate.radiateur_atelier",
        "base": "radiateur_atelier",
        "planning": "atelier",
        "icon": "mdi:tools",
    },
    "salle_cine": {
        "title": "Salle ciné",
        "entity": "climate.radiateur_salle_cine",
        "base": "radiateur_salle_cine",
        "planning": "salle_cine",
        "icon": "mdi:movie-open",
    },
}


ZONES = [
    {
        "key": "zone_parents",
        "title": "Zone parents",
        "icon": "mdi:bed-king-outline",
        "summary": "sensor.chauffage_zone_parents",
        "consigne": "input_number.chauffage_consigne_zone_parents",
        "planning": "zone_parents",
        "rooms": ["chambre_parents", "dressing", "sdb_parents"],
    },
    {
        "key": "premier_etage",
        "title": "1er étage",
        "icon": "mdi:home-floor-1",
        "summary": "sensor.chauffage_premier_etage",
        "consigne": "input_number.chauffage_consigne_premier_etage",
        "planning": "premier_etage",
        "rooms": [
            "chambre_julie",
            "chambre_pablo",
            "grande_chambre_amis",
            "petite_chambre_amis",
            "chambre_mathias",
            "sdb_garcons",
            "sdb_julie",
        ],
    },
    {
        "key": "buanderie",
        "title": "Buanderie",
        "icon": "mdi:washing-machine",
        "summary": "sensor.chauffage_buanderie",
        "consigne": "input_number.chauffage_consigne_buanderie",
        "planning": "buanderie",
        "rooms": ["buanderie"],
    },
    {
        "key": "sous_sol",
        "title": "Sous-sol",
        "icon": "mdi:home-floor-negative-1",
        "summary": "sensor.chauffage_sous_sol",
        "consigne": "input_number.chauffage_consigne_sous_sol",
        "planning": "sous_sol",
        "rooms": ["atelier", "salle_cine"],
    },
]


def nav(path: str) -> dict[str, Any]:
    return {"action": "navigate", "navigation_path": f"{DASHBOARD}/{path}"}


def zone_route(key: str) -> str:
    return key.removeprefix("zone_").replace("_", "-")


def perform(action: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"action": "perform-action", "perform_action": action}
    if data:
        result["data"] = data
    return result


def title_card(title: str, subtitle: str | None = None) -> dict[str, Any]:
    card: dict[str, Any] = {"type": "custom:mushroom-title-card", "title": title}
    if subtitle:
        card["subtitle"] = subtitle
    return card


def action_chip(label: str, icon: str, tap_action: dict[str, Any], color: str | None = None) -> dict[str, Any]:
    chip: dict[str, Any] = {
        "type": "template",
        "content": label,
        "icon": icon,
        "tap_action": tap_action,
    }
    if color:
        chip["icon_color"] = color
    return chip


def mode_chips(target: str, states_entity: str | None = None) -> dict[str, Any]:
    chips = []
    for label, mode, icon, color in (
        ("Auto", "auto", "mdi:radiator", "cyan"),
        ("Chauffage", "heat", "mdi:fire", "deep-orange"),
        ("Éteint", "off", "mdi:power", "disabled"),
    ):
        icon_color = color
        if states_entity:
            icon_color = "{{ '" + color + "' if is_state('" + states_entity + "', '" + mode + "') else 'disabled' }}"
        chips.append(
            action_chip(
                label,
                icon,
                perform(
                    "script.chauffage_appliquer_mode_cible",
                    {"cible": target, "mode_chauffage": mode},
                ),
                icon_color,
            )
        )
    return {"type": "custom:mushroom-chips-card", "alignment": "justify", "chips": chips}


def room_secondary(entity: str) -> str:
    return (
        "{% set current = state_attr('" + entity + "', 'current_temperature') %}\n"
        "{% set target = state_attr('" + entity + "', 'temperature') %}\n"
        "{{ (current | round(1) ~ ' °C') if current is number else 'Température indisponible' }}"
        " · cible {{ (target | round(1) ~ ' °C') if target is number else '—' }}"
        " · {{ {'auto':'Auto','heat':'Chauffage','off':'Éteint'}.get(states('" + entity + "'), states('" + entity + "')) }}"
    )


def room_card(room_key: str) -> dict[str, Any]:
    room = ROOMS[room_key]
    entity = room["entity"]
    return {
        "type": "custom:mushroom-template-card",
        "entity": entity,
        "primary": room["title"],
        "secondary": room_secondary(entity),
        "icon": room["icon"],
        "icon_color": "{{ 'deep-orange' if state_attr('" + entity + "', 'hvac_action') == 'heating' else 'disabled' }}",
        "badge_icon": "{{ 'mdi:alert-circle' if states('" + entity + "') in ['unknown', 'unavailable'] else '' }}",
        "badge_color": "red",
        "tap_action": nav(f"chauffage-piece-{room_key.replace('_', '-')}")
    }


def zone_card(zone: dict[str, Any]) -> dict[str, Any]:
    summary = zone["summary"]
    room_count = len(zone["rooms"])
    demand_template = (
        "{% set entities = " + repr([ROOMS[key]["entity"] for key in zone["rooms"]]).replace('"', "'") + " %}\n"
        "{% set ns = namespace(total=0) %}\n"
        "{% for entity in entities %}"
        "{% set target = state_attr(entity, 'temperature') %}"
        "{% set current = state_attr(entity, 'current_temperature') %}"
        "{% if states(entity) in ['auto','heat'] and target is number and current is number and target-current > 0.5 %}"
        "{% set ns.total = ns.total + 1 %}{% endif %}{% endfor %}\n"
        "{{ ns.total }} sur " + str(room_count) + " en demande · {{ states('" + summary + "') }} °C"
    )
    destination = (
        f"chauffage-piece-{zone['rooms'][0].replace('_', '-')}"
        if len(zone["rooms"]) == 1
        else f"chauffage-zone-{zone_route(zone['key'])}"
    )
    return {
        "type": "custom:mushroom-template-card",
        "entity": summary,
        "primary": zone["title"],
        "secondary": demand_template,
        "icon": zone["icon"],
        "icon_color": "{{ 'deep-orange' if state_attr('" + summary + "', 'en_chauffe') | int(0) > 0 else 'disabled' }}",
        "tap_action": nav(destination)
    }


def make_view(title: str, path: str, cards: list[dict[str, Any]], back: str | None = None, icon: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "title": title,
        "path": path,
        "type": "sections",
        "max_columns": 1,
        "sections": [{"type": "grid", "cards": cards}],
    }
    if icon:
        result["icon"] = icon
    if back:
        result["subview"] = True
        result["back_path"] = f"{DASHBOARD}/{back}"
    return result


def pac_mode_chips() -> dict[str, Any]:
    chips = []
    for label, mode, icon, color in (
        ("Auto", "auto", "mdi:autorenew", "cyan"),
        ("Marche", "heat", "mdi:fire", "deep-orange"),
        ("Arrêt", "off", "mdi:power", "grey"),
    ):
        action = perform("climate.set_hvac_mode", {"hvac_mode": mode})
        action["target"] = {"entity_id": PAC_CLIMATE}
        chips.append(action_chip(label, icon, action, "{{ '" + color + "' if is_state('" + PAC_CLIMATE + "', '" + mode + "') else 'disabled' }}"))
    return {"type": "custom:mushroom-chips-card", "alignment": "justify", "chips": chips}


def global_view() -> dict[str, Any]:
    demand = "binary_sensor.chauffage_demande_chauffage"
    cards: list[dict[str, Any]] = [
        {
            "type": "custom:mushroom-template-card",
            "entity": PAC_CLIMATE,
            "primary": "Pompe à chaleur",
            "secondary": "{{ states('" + PAC_CLIMATE + "') | title }} · consigne {{ states('" + PAC_SETPOINT + "') }} °C · ambiance {{ states('" + PAC_THERMOSTAT + "') }} °C",
            "icon": "mdi:heat-pump",
            "icon_color": "{{ 'deep-orange' if not is_state('" + PAC_CLIMATE + "', 'off') else 'disabled' }}",
            "badge_icon": "{{ 'mdi:fire' if not is_state('" + PAC_CLIMATE + "', 'off') else 'mdi:power' }}",
            "badge_color": "{{ 'deep-orange' if not is_state('" + PAC_CLIMATE + "', 'off') else 'grey' }}",
            "tap_action": nav("chauffage-pac"),
        },
        {
            "type": "custom:mushroom-template-card",
            "entity": ECS_TEMPERATURE,
            "primary": "Eau chaude",
            "secondary": "{{ states('" + ECS_TEMPERATURE + "') }} °C · {{ 'autorisée' if is_state('" + ECS_SWITCH + "', 'on') else 'désactivée' }} · cycle {{ 'actif' if is_state('" + ECS_CYCLE + "', 'on') else 'inactif' }}",
            "icon": "mdi:water-boiler",
            "icon_color": "{{ 'deep-orange' if is_state('" + ECS_CYCLE + "', 'on') else 'cyan' }}",
            "tap_action": nav("chauffage-ecs"),
        },
        {
            "type": "custom:mushroom-template-card",
            "entity": ABSENCE_SWITCH,
            "primary": "Absence",
            "secondary": "{{ states('sensor.atlantic_alfea_m_duo_absence') }}{% if is_state('" + ABSENCE_SWITCH + "', 'on') %} · jusqu’au {{ states('" + ABSENCE_END + "') }}{% endif %}",
            "icon": "mdi:home-export-outline",
            "icon_color": "{{ 'cyan' if is_state('" + ABSENCE_SWITCH + "', 'on') else 'disabled' }}",
            "tap_action": nav("chauffage-absence"),
        },
        {
            "type": "custom:mushroom-template-card",
            "entity": demand,
            "primary": "Vannes thermostatiques · {{ states('input_select.chauffage_mode_maison') }}",
            "secondary": "{{ state_attr('" + demand + "', 'nombre_pieces_en_demande') | int(0) }} pièces demandent du chauffage",
            "icon": "mdi:radiator",
            "icon_color": "{{ 'deep-orange' if is_state('" + demand + "', 'on') else 'disabled' }}",
            "tap_action": {"action": "more-info"},
        },
        {"type": "custom:mushroom-select-card", "entity": "input_select.chauffage_mode_maison", "name": "Mode maison", "icon": "mdi:home-thermometer-outline"},
        {
            "type": "custom:mushroom-template-card",
            "entity": demand,
            "primary": "Plus forte demande",
            "secondary": "{{ state_attr('" + demand + "', 'piece_ecart_maximum') }} · {{ state_attr('" + demand + "', 'ecart_maximum') }} °C sous la consigne",
            "icon": "mdi:chart-line-variant",
            "icon_color": "{{ 'deep-orange' if state_attr('" + demand + "', 'ecart_maximum') | float(0) > 0.5 else 'disabled' }}",
            "tap_action": {"action": "more-info"},
        },
        title_card("Zones", "Synthèse uniquement · commandes dans chaque pièce"),
    ]
    cards.extend(zone_card(zone) for zone in ZONES)
    cards.append({"type": "custom:mushroom-template-card", "primary": "Paramètres", "secondary": "Profils maison · durée du boost", "icon": "mdi:cog-outline", "tap_action": nav("chauffage-parametres")})
    return make_view("Chauffage", "chauffage-v2", cards, icon="mdi:radiator")


def pac_view() -> dict[str, Any]:
    cards = [
        title_card("Chauffage", "Commandes générales de la pompe à chaleur"),
        pac_mode_chips(),
        {"type": "custom:mushroom-number-card", "entity": PAC_SETPOINT, "name": "Consigne générale", "icon": "mdi:thermostat", "display_mode": "buttons"},
        {"type": "horizontal-stack", "cards": [
            {"type": "custom:mushroom-template-card", "entity": PAC_THERMOSTAT, "primary": "{{ states('" + PAC_THERMOSTAT + "') }} °C", "secondary": "Thermostat Z1", "icon": "mdi:home-thermometer-outline"},
            {"type": "custom:mushroom-template-card", "entity": PAC_OUTDOOR, "primary": "{{ states('" + PAC_OUTDOOR + "') }} °C", "secondary": "Extérieur", "icon": "mdi:thermometer"},
        ]},
        {"type": "custom:mushroom-template-card", "primary": "Planning chauffage global", "secondary": "Programme utilisé en mode Auto", "icon": "mdi:calendar-clock", "tap_action": nav("chauffage-pac-planning")},
        {"type": "custom:mushroom-template-card", "primary": "État technique", "secondary": "Pression et températures", "icon": "mdi:gauge", "tap_action": nav("chauffage-pac-technique")},
    ]
    return make_view("Pompe à chaleur", "chauffage-pac", cards, "chauffage-v2")


def pac_schedule_view() -> dict[str, Any]:
    days = [("lundi", "Lundi"), ("mardi", "Mardi"), ("mercredi", "Mercredi"), ("jeudi", "Jeudi"), ("vendredi", "Vendredi"), ("samedi", "Samedi"), ("dimanche", "Dimanche")]
    entities = [{"entity": f"sensor.atlantic_alfea_m_duo_{slug}_programme_chauffage", "name": name} for slug, name in days]
    cards = [
        title_card("Planning chauffage global", "Programme lu depuis l’Alféa M"),
        {"type": "entities", "show_header_toggle": False, "entities": entities},
        {"type": "markdown", "content": "**Écriture non disponible actuellement.** Les intégrations Alféa M et Cozytouch exposent ces programmes en lecture, sans action d’écriture. Une future version du composant devra ajouter un service dédié avant d’afficher un bouton Enregistrer."},
    ]
    return make_view("Planning chauffage", "chauffage-pac-planning", cards, "chauffage-pac")


def ecs_view() -> dict[str, Any]:
    cards = [
        title_card("Eau chaude", "Commandes et état du ballon"),
        {"type": "custom:mushroom-entity-card", "entity": ECS_SWITCH, "name": "Eau chaude autorisée", "icon": "mdi:water-boiler", "tap_action": {"action": "toggle"}},
        {"type": "custom:mushroom-entity-card", "entity": ECS_BOOST, "name": "Boost ECS", "icon": "mdi:fire", "tap_action": {"action": "toggle"}},
        {"type": "horizontal-stack", "cards": [
            {"type": "custom:mushroom-template-card", "entity": ECS_TEMPERATURE, "primary": "{{ states('" + ECS_TEMPERATURE + "') }} °C", "secondary": "Température ECS", "icon": "mdi:thermometer-water"},
            {"type": "custom:mushroom-template-card", "entity": ECS_CYCLE, "primary": "{{ 'Actif' if is_state('" + ECS_CYCLE + "', 'on') else 'Inactif' }}", "secondary": "Cycle ECS", "icon": "mdi:progress-clock", "icon_color": "{{ 'deep-orange' if is_state('" + ECS_CYCLE + "', 'on') else 'disabled' }}"},
        ]},
        {"type": "custom:mushroom-template-card", "primary": "Plages heures creuses", "secondary": "00:54–07:24 · 11:54–13:24", "icon": "mdi:calendar-clock", "tap_action": nav("chauffage-ecs-planning")},
        {"type": "custom:mushroom-template-card", "primary": "Historique ECS", "secondary": "Autorisation et température sur trois jours", "icon": "mdi:chart-line", "tap_action": nav("chauffage-ecs-historique")},
    ]
    return make_view("Eau chaude", "chauffage-ecs", cards, "chauffage-v2")


def ecs_schedule_view() -> dict[str, Any]:
    cards = [
        title_card("Planning eau chaude", "Automatisation des heures creuses"),
        {"type": "entities", "show_header_toggle": False, "entities": [{"entity": ECS_AUTOMATION, "name": "Gestion ECS automatique"}]},
        {"type": "markdown", "content": "**Nuit :** 00:54 → 07:24  \n**Midi :** 11:54 → 13:24  \nSi un cycle est actif à la fin d’une plage, l’automatisation attend sa fin pendant 90 minutes au maximum avant de couper l’autorisation ECS."},
    ]
    return make_view("Planning eau chaude", "chauffage-ecs-planning", cards, "chauffage-ecs")


def ecs_history_view() -> dict[str, Any]:
    cards = [
        title_card("Historique ECS", "Trois derniers jours"),
        {"type": "history-graph", "title": "Autorisation et température de l’eau", "hours_to_show": 72, "entities": [{"entity": ECS_SWITCH, "name": "ECS autorisée"}, {"entity": ECS_TEMPERATURE, "name": "Température ECS"}]},
        {"type": "entities", "show_header_toggle": False, "entities": [ECS_CYCLE, "sensor.atlantic_alfea_m_duo_consommation_2"]},
    ]
    return make_view("Historique ECS", "chauffage-ecs-historique", cards, "chauffage-ecs")


def absence_view() -> dict[str, Any]:
    cards = [
        title_card("Absence", "Période globale transmise à l’Alféa M"),
        {"type": "entities", "show_header_toggle": False, "entities": [
            {"entity": "sensor.atlantic_alfea_m_duo_absence", "name": "État"},
            {"entity": ABSENCE_START, "name": "Début"},
            {"entity": ABSENCE_END, "name": "Fin"},
            {"entity": ABSENCE_SWITCH, "name": "Activer l’absence"},
        ]},
    ]
    return make_view("Absence", "chauffage-absence", cards, "chauffage-v2")


def technical_view() -> dict[str, Any]:
    cards = [
        title_card("État technique", "Mesures principales de la pompe à chaleur"),
        {"type": "entities", "show_header_toggle": False, "entities": [
            "sensor.atlantic_alfea_m_duo_pression_deau",
            "sensor.atlantic_alfea_m_duo_temperature_chaudiere",
            "sensor.atlantic_alfea_m_duo_temperature_echappement",
            PAC_OUTDOOR,
            PAC_THERMOSTAT,
        ]},
        {"type": "custom:mushroom-template-card", "primary": "Diagnostic et consommations", "secondary": "Connexion, Wi-Fi, compteurs et identification", "icon": "mdi:dots-horizontal-circle-outline", "tap_action": nav("chauffage-pac-diagnostic")},
    ]
    return make_view("État technique", "chauffage-pac-technique", cards, "chauffage-pac")


def diagnostics_view() -> dict[str, Any]:
    cards = [
        title_card("Diagnostic PAC"),
        {"type": "entities", "show_header_toggle": False, "entities": [
            "binary_sensor.atlantic_alfea_m_duo_connexion_cozytouch",
            "sensor.atlantic_alfea_m_duo_signal_wi_fi",
            "sensor.atlantic_alfea_m_duo_zone_1",
            ECS_CYCLE,
            "binary_sensor.atlantic_alfea_m_duo_mode_boost",
            "sensor.atlantic_alfea_m_duo_consommation_1",
            "sensor.atlantic_alfea_m_duo_consommation_2",
            "sensor.atlantic_alfea_m_duo_modele",
            "sensor.atlantic_alfea_m_duo_fuseau_horaire",
        ]},
    ]
    return make_view("Diagnostic PAC", "chauffage-pac-diagnostic", cards, "chauffage-pac-technique")


def zone_view(zone: dict[str, Any]) -> dict[str, Any]:
    cards: list[dict[str, Any]] = [title_card(zone["title"], "Synthèse de la zone · commandes dans chaque pièce"), title_card("Pièces")]
    cards.extend(room_card(room_key) for room_key in zone["rooms"])
    return make_view(zone["title"], f"chauffage-zone-{zone_route(zone['key'])}", cards, "chauffage-v2")


def room_view(room_key: str, zone_key: str) -> dict[str, Any]:
    room = ROOMS[room_key]
    entity = room["entity"]
    battery = f"sensor.{room['base']}_battery"
    cards: list[dict[str, Any]] = [
        title_card(room["title"]),
        {
            "type": "custom:mushroom-climate-card",
            "entity": entity,
            "name": room["title"],
            "icon": room["icon"],
            "show_temperature_control": True,
            "collapsible_controls": False,
            "hvac_modes": ["off", "heat", "auto"],
        },
        {
            "type": "custom:mushroom-template-card",
            "entity": entity,
            "primary": "{{ 'Demande de chauffage' if states('" + entity + "') in ['auto','heat'] and state_attr('" + entity + "', 'temperature') is number and state_attr('" + entity + "', 'current_temperature') is number and state_attr('" + entity + "', 'temperature') - state_attr('" + entity + "', 'current_temperature') > 0.5 else 'Aucune demande' }}",
            "secondary": "Batterie {{ states('" + battery + "') }} % · {{ states('" + entity + "') }}",
            "icon": "mdi:radiator",
            "icon_color": "{{ 'deep-orange' if state_attr('" + entity + "', 'hvac_action') == 'heating' else 'disabled' }}",
            "tap_action": {"action": "more-info"},
        },
        {
            "type": "custom:mushroom-chips-card",
            "alignment": "justify",
            "chips": [
                action_chip("Boost", "mdi:fire", perform("script.chauffage_boost_cible", {"cible": room_key}), "deep-orange"),
                action_chip("Planning", "mdi:calendar-clock", nav(f"chauffage-planning-piece-{room_key.replace('_', '-')}")),
            ],
        },
    ]
    back_path = "chauffage-v2" if room_key == "buanderie" else f"chauffage-zone-{zone_route(zone_key)}"
    return {
        "title": room["title"],
        "path": f"chauffage-piece-{room_key.replace('_', '-')}",
        "subview": True,
        "back_path": f"{DASHBOARD}/{back_path}",
        "type": "sections",
        "max_columns": 1,
        "sections": [{"type": "grid", "cards": cards}],
    }


def planning_view(title: str, path: str, target: str, planning_slug: str, parent_path: str) -> dict[str, Any]:
    entities = [
        {"entity": f"input_text.chauffage_planning_{planning_slug}_semaine", "name": "Semaine"},
        {"entity": f"input_text.chauffage_planning_{planning_slug}_samedi", "name": "Samedi"},
        {"entity": f"input_text.chauffage_planning_{planning_slug}_dimanche", "name": "Dimanche"},
    ]
    cards: list[dict[str, Any]] = [
        title_card(f"Planning · {title}", "Six changements requis par type de journée"),
        {
            "type": "markdown",
            "content": "Format : `HH:MM/température`, séparé par des espaces. Exemple : `00:00/17 06:30/19 08:30/16 12:00/16 17:30/19 22:30/17`.",
        },
        {"type": "entities", "show_header_toggle": False, "entities": entities},
        {
            "type": "custom:mushroom-template-card",
            "primary": "Enregistrer et appliquer",
            "secondary": "Copie le planning vers les vannes puis active Auto",
            "icon": "mdi:calendar-check",
            "icon_color": "cyan",
            "tap_action": perform("script.chauffage_appliquer_planning_cible", {"cible": target}),
            "hold_action": {"action": "none"},
        },
        {
            "type": "custom:mushroom-template-card",
            "primary": "Retour",
            "icon": "mdi:arrow-left",
            "tap_action": nav(parent_path),
        },
    ]
    return {
        "title": f"Planning {title}",
        "path": path,
        "subview": True,
        "back_path": f"{DASHBOARD}/{parent_path}",
        "type": "sections",
        "max_columns": 1,
        "sections": [{"type": "grid", "cards": cards}],
    }


def settings_view() -> dict[str, Any]:
    cards: list[dict[str, Any]] = [
        title_card("Paramètres chauffage", "Valeurs conservées après redémarrage"),
        title_card("Profils maison"),
    ]
    for entity, name, icon in (
        ("input_number.chauffage_profil_confort", "Confort", "mdi:home-thermometer"),
        ("input_number.chauffage_profil_nuit", "Nuit", "mdi:weather-night"),
        ("input_number.chauffage_profil_absence", "Absence", "mdi:home-export-outline"),
        ("input_number.chauffage_duree_boost", "Durée du boost", "mdi:timer-outline"),
    ):
        cards.append(
            {
                "type": "custom:mushroom-number-card",
                "entity": entity,
                "name": name,
                "icon": icon,
                "display_mode": "buttons",
            }
        )
    cards.append({"type": "markdown", "content": "Les consignes, boosts et plannings des vannes se règlent dans chaque pièce. Les zones restent des synthèses sans commande commune."})
    return {
        "title": "Paramètres chauffage",
        "path": "chauffage-parametres",
        "subview": True,
        "back_path": f"{DASHBOARD}/chauffage-v2",
        "type": "sections",
        "max_columns": 1,
        "sections": [{"type": "grid", "cards": cards}],
    }


def scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def dump_yaml(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(dump_yaml(item, indent + 2))
            elif isinstance(item, str) and "\n" in item:
                lines.append(f"{prefix}{key}: >-")
                lines.extend(f"{' ' * (indent + 2)}{line}" for line in item.splitlines())
            else:
                lines.append(f"{prefix}{key}: {scalar(item)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(dump_yaml(item, indent + 2))
            elif isinstance(item, str) and "\n" in item:
                lines.append(f"{prefix}- >-")
                lines.extend(f"{' ' * (indent + 2)}{line}" for line in item.splitlines())
            else:
                lines.append(f"{prefix}- {scalar(item)}")
    return lines


def build_views() -> list[dict[str, Any]]:
    views: list[dict[str, Any]] = [
        global_view(),
        pac_view(),
        pac_schedule_view(),
        ecs_view(),
        ecs_schedule_view(),
        ecs_history_view(),
        absence_view(),
        technical_view(),
        diagnostics_view(),
        settings_view(),
    ]
    for zone in ZONES:
        if len(zone["rooms"]) > 1:
            views.append(zone_view(zone))
    zone_by_room = {
        room_key: zone["key"]
        for zone in ZONES
        for room_key in zone["rooms"]
    }
    for room_key, room in ROOMS.items():
        views.append(room_view(room_key, zone_by_room[room_key]))
        views.append(
            planning_view(
                room["title"],
                f"chauffage-planning-piece-{room_key.replace('_', '-')}",
                room_key,
                room["planning"],
                f"chauffage-piece-{room_key.replace('_', '-')}",
            )
        )
    return views


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "# Heat Manager mobile v2.1 — vues générées",
        "# Fusionner les éléments de `views` dans le tableau de bord lovelace-mobile après validation.",
        "# Dépendance : Mushroom déjà installé.",
        "",
    ]
    output = header + dump_yaml({"views": build_views()})
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT} with {len(build_views())} views")


if __name__ == "__main__":
    main()
