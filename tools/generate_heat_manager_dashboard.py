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

ACTIVE_ORANGE = "rgb(194, 75, 0)"
ACTIVE_BLUE = "rgb(21, 101, 192)"
# Same page background as every lovelace-mobile view, so white cards stand out.
VIEW_BACKGROUND = "#e4e9f0"
FULL_WIDTH = {"columns": "full", "rows": "auto"}
HALF_WIDTH = {"columns": 6, "rows": "auto"}
NAVIGATION_CARD_STYLE = """ha-card {
  border: 1px solid var(--divider-color);
  border-radius: 16px;
  box-shadow: none;
  min-height: 72px;
}
ha-state-icon {
  --mdc-icon-size: 24px;
}
"""
TALL_NAVIGATION_CARD_STYLE = NAVIGATION_CARD_STYLE.replace("min-height: 72px", "min-height: 96px")


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
        "rooms": ["chambre_parents", "dressing", "sdb_parents"],
    },
    {
        "key": "premier_etage",
        "title": "1er étage",
        "icon": "mdi:home-floor-1",
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
        "rooms": ["buanderie"],
    },
    {
        "key": "sous_sol",
        "title": "Sous-sol",
        "icon": "mdi:home-floor-negative-1",
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


def full_width(
    card: dict[str, Any],
    styled: bool = False,
    active_condition: str | None = None,
    active_background: str = ACTIVE_ORANGE,
) -> dict[str, Any]:
    """Make a Sections card occupy the complete mobile content width.

    When `active_condition` (a Jinja expression) is given, the card gets a coloured
    background while the condition is true.
    """
    result = dict(card)
    result["grid_options"] = FULL_WIDTH
    if styled or active_condition:
        style = NAVIGATION_CARD_STYLE
        if active_condition:
            style = style.replace(
                "  min-height: 72px;\n",
                "  min-height: 72px;\n" + _active_css(active_condition, active_background),
            )
        result["card_mod"] = {"style": style}
    return result


def _active_css(condition: str, background: str) -> str:
    return (
        "  {% if " + condition + " %}\n"
        f"  background: {background};\n"
        "  --primary-text-color: white;\n"
        "  --secondary-text-color: rgba(255, 255, 255, 0.85);\n"
        "  --card-primary-color: white;\n"
        "  --card-secondary-color: rgba(255, 255, 255, 0.85);\n"
        "  {% endif %}\n"
    )


def half_width(card: dict[str, Any], active_condition: str | None = None) -> dict[str, Any]:
    """Make a Sections card occupy half the width (two cards side by side), taller than the default.

    When `active_condition` (a Jinja expression) is given, the card gets the orange "Marche"
    background of the heat pump view while the condition is true.
    """
    result = dict(card)
    result["grid_options"] = HALF_WIDTH
    style = TALL_NAVIGATION_CARD_STYLE
    if active_condition:
        active_css = (
            "  {% if " + active_condition + " %}\n"
            "  background: rgb(194, 75, 0);\n"
            "  --primary-text-color: white;\n"
            "  --secondary-text-color: rgba(255, 255, 255, 0.85);\n"
            "  --card-primary-color: white;\n"
            "  --card-secondary-color: rgba(255, 255, 255, 0.85);\n"
            "  {% endif %}\n"
        )
        style = style.replace("  min-height: 96px;\n", "  min-height: 96px;\n" + active_css)
    result["card_mod"] = {"style": style}
    return result


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
    entities = [ROOMS[key]["entity"] for key in zone["rooms"]]
    entity_list = repr(entities).replace('"', "'")
    room_count = len(zone["rooms"])
    demand_template = (
        "{% set entities = " + entity_list + " %}\n"
        "{% set ns = namespace(total=0, temperatures=[]) %}\n"
        "{% for entity in entities %}"
        "{% set target = state_attr(entity, 'temperature') %}"
        "{% set current = state_attr(entity, 'current_temperature') %}"
        "{% if current is number %}{% set ns.temperatures = ns.temperatures + [current] %}{% endif %}"
        "{% if states(entity) in ['auto','heat'] and target is number and current is number and target-current > 0.5 %}"
        "{% set ns.total = ns.total + 1 %}{% endif %}{% endfor %}\n"
        "{% set moyenne = (ns.temperatures | sum / ns.temperatures | count) | round(1) if ns.temperatures | count else none %}"
        "{{ ns.total }} sur " + str(room_count) + " en demande · {{ moyenne ~ ' °C' if moyenne is not none else 'température indisponible' }}"
    )
    destination = (
        f"chauffage-piece-{zone['rooms'][0].replace('_', '-')}"
        if len(zone["rooms"]) == 1
        else f"chauffage-zone-{zone_route(zone['key'])}"
    )
    return {
        "type": "custom:mushroom-template-card",
        "entity": entities[0],
        "primary": zone["title"],
        "secondary": demand_template,
        "icon": zone["icon"],
        "icon_color": "{{ 'deep-orange' if expand(" + entity_list + ") | selectattr('attributes.hvac_action', 'eq', 'heating') | list | count > 0 else 'disabled' }}",
        "tap_action": nav(destination)
    }


def navigation_chips() -> dict[str, Any]:
    """Back/home chips, same as the other lovelace-mobile pages."""
    return {
        "type": "custom:mushroom-chips-card",
        "chips": [
            {"type": "back"},
            {"type": "action", "tap_action": {"action": "navigate", "navigation_path": f"{DASHBOARD}/0"}, "icon": "mdi:home"},
        ],
    }


def make_view(title: str, path: str, cards: list[dict[str, Any]], back: str | None = None, icon: str | None = None) -> dict[str, Any]:
    cards = [navigation_chips(), *cards]
    cards = [card if "grid_options" in card else full_width(card) for card in cards]
    result: dict[str, Any] = {
        "title": title,
        "path": path,
        "type": "sections",
        "max_columns": 1,
        "sections": [{"type": "grid", "cards": cards}],
        "background": VIEW_BACKGROUND,
    }
    if icon:
        result["icon"] = icon
    if back:
        # Hidden from the tab bar rather than a subview: navigation relies on the
        # back/home chips, like the other lovelace-mobile pages.
        result["visible"] = False
    return result


SETPOINT_STYLE = "ha-card { border: 1px solid rgba(0, 188, 212, 0.45); border-left: 4px solid #00acc1; background: rgba(0, 188, 212, 0.07); box-shadow: none; }"
SETPOINT_TOP_STYLE = "ha-card { border: 1px solid rgba(0, 188, 212, 0.45); border-left: 4px solid #00acc1; border-bottom: none; border-radius: 12px 12px 0 0; background: rgba(0, 188, 212, 0.07); box-shadow: none; }"
SETPOINT_BOTTOM_STYLE = "ha-card { border: 1px solid rgba(0, 188, 212, 0.45); border-left: 4px solid #00acc1; border-top: none; border-radius: 0 0 12px 12px; background: rgba(0, 188, 212, 0.07); box-shadow: none; margin-top: -8px; }"


ABSENCE_PANEL = "input_boolean.chauffage_panneau_absence_pac"


def pac_level1_buttons() -> dict[str, Any]:
    """Marche / Absence / Arrêt de la PAC. Absence ouvre ou ferme le panneau des dates."""
    grid = hvac_mode_buttons(PAC_CLIMATE, (
        ("Marche", "heat", "mdi:fire", "194, 75, 0"),
        ("Absence", "absence", "mdi:home-export-outline", "21, 101, 192"),
        ("Arrêt", "off", "mdi:power", "85, 99, 112"),
    ))
    absence = grid["cards"][1]
    active = "is_state('" + ABSENCE_SWITCH + "', 'on')"
    # Pendant une absence, la PAC reste en « off » : seul le bouton Absence doit être allumé.
    for button, mode in ((grid["cards"][0], "heat"), (grid["cards"][2], "off")):
        # Le script désactive d'abord une absence en cours.
        button["tap_action"] = perform("script.chauffage_pac_mode", {"mode": mode})
        condition = "is_state('" + PAC_CLIMATE + "', '" + mode + "')"
        button["card_mod"]["style"] = button["card_mod"]["style"].replace(condition, "(" + condition + " and not " + active + ")")
    absence["entity"] = ABSENCE_SWITCH
    absence["tap_action"] = perform("input_boolean.toggle")
    absence["tap_action"]["target"] = {"entity_id": ABSENCE_PANEL}
    absence["card_mod"]["style"] = (
        absence["card_mod"]["style"]
        .replace("is_state('" + PAC_CLIMATE + "', 'absence')", active)
        .removesuffix("}")
        + "{% if is_state('" + ABSENCE_PANEL + "', 'on') %}border: 2px solid rgb(21, 101, 192); {% endif %}}"
    )
    return grid


def absence_entities() -> list[dict[str, Any]]:
    return [
        {"entity": "sensor.atlantic_alfea_m_duo_absence", "name": "État"},
        {"entity": ABSENCE_START, "name": "Début"},
        {"entity": ABSENCE_END, "name": "Fin"},
        {"entity": ABSENCE_SWITCH, "name": "Activer l’absence"},
    ]


def absence_panel() -> dict[str, Any]:
    close = perform("input_boolean.turn_off")
    close["target"] = {"entity_id": ABSENCE_PANEL}
    return {
        "type": "conditional",
        "conditions": [{"condition": "state", "entity": ABSENCE_PANEL, "state": "on"}],
        "card": {
            "type": "entities", "title": "Absence de la PAC", "show_header_toggle": False,
            "entities": absence_entities() + [
                {"type": "button", "name": "Fermer le panneau", "icon": "mdi:close", "action_name": "Fermer", "tap_action": close},
            ],
            "card_mod": {"style": "ha-card { border: 1px solid rgba(21, 101, 192, 0.6); border-left: 4px solid rgb(21, 101, 192); box-shadow: none; }"},
        },
    }


def pac_setpoint_card() -> dict[str, Any]:
    return {"type": "vertical-stack", "cards": [
        {"type": "custom:mushroom-template-card", "entity": PAC_SETPOINT, "primary": "Consigne générale", "secondary": "Température actuelle = {{ states('" + PAC_THERMOSTAT + "') | replace('.', ',') }} °C", "icon": "mdi:thermostat", "icon_color": "cyan", "tap_action": {"action": "more-info"}, "hold_action": {"action": "none"}, "card_mod": {"style": SETPOINT_TOP_STYLE}},
        {"type": "custom:mushroom-number-card", "entity": PAC_SETPOINT, "display_mode": "buttons", "primary_info": "none", "secondary_info": "none", "icon_type": "none", "card_mod": {"style": SETPOINT_BOTTOM_STYLE}},
    ]}


def pac_info_cards() -> list[dict[str, Any]]:
    return [
        {"type": "horizontal-stack", "cards": [
            {"type": "custom:mushroom-template-card", "entity": PAC_THERMOSTAT, "primary": "{{ states('" + PAC_THERMOSTAT + "') }} °C", "secondary": "Temp. intérieure", "icon": "mdi:home-thermometer-outline"},
            {"type": "custom:mushroom-template-card", "entity": PAC_OUTDOOR, "primary": "{{ states('" + PAC_OUTDOOR + "') }} °C", "secondary": "Temp. extérieure", "icon": "mdi:thermometer"},
        ]},
        {"type": "custom:mushroom-template-card", "primary": "État technique", "secondary": "Pression et températures", "icon": "mdi:gauge", "tap_action": nav("chauffage-pac-technique")},
    ]


def trv_mode_buttons(entity: str) -> dict[str, Any]:
    return hvac_mode_buttons(entity, (
        ("Auto", "auto", "mdi:thermostat-auto", "0, 131, 143"),
        ("Manuel", "heat", "mdi:fire", "194, 75, 0"),
        ("Arrêt", "off", "mdi:power", "85, 99, 112"),
    ))


def house_mode_buttons() -> dict[str, Any]:
    return hvac_mode_buttons("input_select.chauffage_mode_maison", (
        ("Auto", "Auto", "mdi:thermostat-auto", "0, 131, 143"),
        ("Absence", "Absence", "mdi:home-export-outline", "21, 101, 192"),
        ("Arrêt", "Arrêt", "mdi:power", "85, 99, 112"),
    ), service=("input_select.select_option", "option"))


def hvac_mode_buttons(
    entity: str,
    modes: tuple[tuple[str, str, str, str], ...],
    service: tuple[str, str] = ("climate.set_hvac_mode", "hvac_mode"),
) -> dict[str, Any]:
    buttons = []
    for index, (label, mode, icon, rgb) in enumerate(modes):
        radius = "14px 0 0 14px" if index == 0 else "0 14px 14px 0" if index == len(modes) - 1 else "0"
        action = perform(service[0], {service[1]: mode})
        action["target"] = {"entity_id": entity}
        active = "is_state('" + entity + "', '" + mode + "')"
        buttons.append({
            "type": "button", "entity": entity, "name": label, "icon": icon,
            "show_state": False, "icon_height": "24px",
            "tap_action": action, "hold_action": {"action": "none"},
            "card_mod": {"style": (
                "ha-card { height: 76px; border-radius: " + radius + "; "
                "box-shadow: none; border: 1px solid var(--divider-color); "
                "background: {{ 'rgb(" + rgb + ")' if " + active + " else 'var(--card-background-color)' }}; "
                "color: {{ 'white' if " + active + " else 'var(--primary-text-color)' }}; "
                "--state-icon-color: {{ 'white' if " + active + " else 'var(--secondary-text-color)' }}; "
                "--state-icon-active-color: {{ 'white' if " + active + " else 'var(--secondary-text-color)' }}; }"
            )},
        })
    return {
        "type": "grid", "columns": len(buttons), "square": False, "cards": buttons,
        "card_mod": {"style": "ha-card { --grid-card-gap: 0px; } :host { --grid-card-gap: 0px; }"},
    }


def global_view() -> dict[str, Any]:
    demand = "binary_sensor.chauffage_demande_chauffage"
    ecs_card = half_width({
            "type": "custom:mushroom-template-card",
            "entity": ECS_TEMPERATURE,
            "primary": "Eau chaude",
            "secondary": "{{ states('" + ECS_TEMPERATURE + "') }} °C · {{ 'autorisée' if is_state('" + ECS_SWITCH + "', 'on') else 'désactivée' }} · cycle {{ 'actif' if is_state('" + ECS_CYCLE + "', 'on') else 'inactif' }}",
            "icon": "mdi:water-boiler",
            "icon_color": "{{ '#ff6f22' if is_state('" + ECS_CYCLE + "', 'on') else 'cyan' }}",
            "badge_icon": "{{ 'mdi:fire' if is_state('" + ECS_CYCLE + "', 'on') else 'mdi:clock-outline' }}",
            "badge_color": "{{ 'deep-orange' if is_state('" + ECS_CYCLE + "', 'on') else 'grey' }}",
            "tap_action": nav("chauffage-ecs"),
            "multiline_secondary": True,
        }, active_condition="is_state('" + ECS_CYCLE + "', 'on')")
    temperatures, technical = pac_info_cards()
    cards: list[dict[str, Any]] = [
        full_width(title_card("PAC")),
        full_width(pac_level1_buttons()),
        full_width(absence_panel()),
        # La consigne générale n'est utile que PAC en marche.
        full_width({"type": "conditional", "conditions": [{"condition": "state", "entity": PAC_CLIMATE, "state": "heat"}], "card": pac_setpoint_card()}),
        full_width(temperatures),
        # Eau chaude et état technique côte à côte, même hauteur.
        ecs_card,
        half_width(technical),
        full_width(title_card("Vannes thermostatiques")),
        # Sous-titre et bouton Paramètres sur une même ligne (8 + 4 colonnes).
        # Marges négatives : rapproche cette ligne du titre « Vannes thermostatiques ».
        {**title_card("", "Contrôle de toutes les vannes"), "card_mod": {"style": "ha-card { margin-top: -16px; }"}, "grid_options": {"columns": 8, "rows": "auto"}},
        {
            "type": "custom:mushroom-chips-card",
            "alignment": "end",
            "chips": [action_chip("Paramètres", "mdi:cog-outline", nav("chauffage-parametres"))],
            "card_mod": {"style": "ha-card { margin-top: -6px; }"},
            "grid_options": {"columns": 4, "rows": "auto"},
        },
        full_width(house_mode_buttons()),
        full_width(title_card("", "Contrôles par pièce")),
    ]
    cards.extend(full_width(zone_card(zone), styled=True) for zone in ZONES)
    cards.append(full_width({
        "type": "custom:mushroom-template-card",
        "entity": demand,
        "primary": "Vannes thermostatiques · {{ states('input_select.chauffage_mode_maison') }}",
        "secondary": "{{ state_attr('" + demand + "', 'nombre_pieces_en_demande') | int(0) }} pièces demandent du chauffage · écart max. {{ state_attr('" + demand + "', 'ecart_maximum') | float(0) }} °C",
        "icon": "mdi:radiator",
        "icon_color": "{{ 'deep-orange' if is_state('" + demand + "', 'on') else 'disabled' }}",
        "badge_icon": "{{ 'mdi:fire-alert' if state_attr('" + demand + "', 'nombre_pieces_forte_demande') | int(0) > 0 else 'mdi:chevron-right' }}",
        "badge_color": "{{ 'deep-orange' if state_attr('" + demand + "', 'nombre_pieces_forte_demande') | int(0) > 0 else 'grey' }}",
        "tap_action": nav("chauffage-parametres"),
        "multiline_secondary": True,
    }, styled=True))
    return make_view("Chauffage", "chauffage-v2", cards, icon="mdi:radiator")


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
    return make_view("État technique", "chauffage-pac-technique", cards, "chauffage-v2")


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
            "type": "conditional",
            "conditions": [{"condition": "state", "entity": "input_select.chauffage_mode_maison", "state": "Absence"}],
            "card": {
                "type": "custom:mushroom-template-card",
                "entity": "input_select.chauffage_mode_maison",
                "primary": "Absence maison : {{ states('input_number.chauffage_profil_absence') | replace('.', ',') }} °C imposés",
                "secondary": "Chaque vanne retrouvera son mode d’avant l’absence au retour",
                "icon": "mdi:home-export-outline",
                "icon_color": "white",
                "multiline_secondary": True,
                "tap_action": {"action": "none"},
                "hold_action": {"action": "none"},
                "card_mod": {"style": "ha-card { background: rgb(21, 101, 192); border: none; box-shadow: none; --primary-text-color: white; --secondary-text-color: rgba(255, 255, 255, 0.85); --card-primary-color: white; --card-secondary-color: rgba(255, 255, 255, 0.85); }"},
            },
        },
        title_card("", "COMMANDES"),
        trv_mode_buttons(entity),
        # La TRVZB quitte le planning si sa consigne change en Auto : réglage réservé au mode Manuel.
        {
            "type": "conditional",
            "conditions": [{"condition": "state", "entity": entity, "state": "heat"}],
            # Mushroom impose « mode · température » sous le nom : en-tête séparé + commandes seules.
            "card": {"type": "vertical-stack", "cards": [
                {
                    "type": "custom:mushroom-template-card",
                    "entity": entity,
                    "primary": "Consigne",
                    "secondary": "Température actuelle : {{ state_attr('" + entity + "', 'current_temperature') | string | replace('.', ',') }} °C",
                    "icon": "mdi:thermostat",
                    "icon_color": "{{ 'deep-orange' if state_attr('" + entity + "', 'hvac_action') == 'heating' else 'cyan' }}",
                    "tap_action": {"action": "more-info"},
                    "hold_action": {"action": "none"},
                    "card_mod": {"style": SETPOINT_TOP_STYLE},
                },
                {
                    "type": "custom:mushroom-climate-card",
                    "entity": entity,
                    "primary_info": "none",
                    "secondary_info": "none",
                    "icon_type": "none",
                    "show_temperature_control": True,
                    "collapsible_controls": False,
                    "card_mod": {"style": SETPOINT_BOTTOM_STYLE},
                },
            ]},
        },
        {
            "type": "conditional",
            "conditions": [{"condition": "state", "entity": entity, "state": "auto"}],
            "card": {
                "type": "custom:mushroom-template-card",
                "entity": entity,
                "primary": "Consigne de planning : {{ state_attr('" + entity + "', 'temperature') | string | replace('.', ',') }} °C",
                "secondary": (
                    "Température actuelle : {{ state_attr('" + entity + "', 'current_temperature') | string | replace('.', ',') }} °C\n"
                    "{% set j = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'][now().weekday()] %}"
                    "{% set p = states('text." + room["base"] + "_weekly_schedule_' ~ j) %}"
                    "{% set ns = namespace(out=[], last='') %}"
                    "{% for t in p.split(' ') if '/' in t %}{% if t != ns.last %}"
                    "{% set ns.out = ns.out + ['à ' ~ t.split('/')[0] ~ ' = ' ~ t.split('/')[1] ~ '°C'] %}"
                    "{% endif %}{% set ns.last = t %}{% endfor %}"
                    "Planning : {{ ns.out | join(', ') if ns.out else 'indisponible' }}"
                ),
                "icon": "mdi:calendar-clock",
                "icon_color": "cyan",
                "multiline_secondary": True,
                "tap_action": {"action": "none"},
                "hold_action": {"action": "none"},
                "card_mod": {"style": SETPOINT_STYLE},
            },
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
    return make_view(
        room["title"],
        f"chauffage-piece-{room_key.replace('_', '-')}",
        cards,
        back_path,
    )


def planning_view(title: str, path: str, target: str, planning_slug: str, parent_path: str) -> dict[str, Any]:
    entities = [
        {"entity": f"input_text.chauffage_planning_{planning_slug}_semaine", "name": "Semaine"},
        {"entity": f"input_text.chauffage_planning_{planning_slug}_weekend", "name": "Week-end"},
    ]
    cards: list[dict[str, Any]] = [
        title_card(f"Planning · {title}", "1 à 6 changements, le premier à 00:00"),
        {
            "type": "markdown",
            "content": "Format : `HH:MM/température`, séparé par des espaces. Exemple : `00:00/17 06:30/19 22:30/17`.",
        },
        {"type": "entities", "show_header_toggle": False, "entities": entities},
        {
            "type": "custom:mushroom-template-card",
            "primary": "Enregistrer",
            "secondary": "Copie le planning vers la vanne sans changer son mode",
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
    return make_view(f"Planning {title}", path, cards, parent_path)


def settings_view() -> dict[str, Any]:
    cards: list[dict[str, Any]] = [
        title_card("Paramètres Vannes", "Valeurs conservées après redémarrage"),
        title_card("Profils maison"),
    ]
    for entity, name, icon in (
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
    return make_view("Paramètres chauffage", "chauffage-parametres", cards, "chauffage-v2")


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
                # Bloc littéral : les retours à la ligne sont conservés (markdown, Jinja).
                lines.append(f"{prefix}{key}: |-")
                lines.extend(f"{' ' * (indent + 2)}{line}" for line in item.splitlines())
            else:
                lines.append(f"{prefix}{key}: {scalar(item)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(dump_yaml(item, indent + 2))
            elif isinstance(item, str) and "\n" in item:
                lines.append(f"{prefix}- |-")
                lines.extend(f"{' ' * (indent + 2)}{line}" for line in item.splitlines())
            else:
                lines.append(f"{prefix}- {scalar(item)}")
    return lines


def build_views() -> list[dict[str, Any]]:
    views: list[dict[str, Any]] = [
        global_view(),
        ecs_view(),
        ecs_schedule_view(),
        ecs_history_view(),
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
        "# Dépendances : Mushroom et card-mod installés et enregistrés dans Lovelace.",
        "",
    ]
    output = header + dump_yaml({"views": build_views()})
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT} with {len(build_views())} views")


if __name__ == "__main__":
    main()
