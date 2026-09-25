"""Generate the « arrosage » view of the lovelace-mobile dashboard (Etherain irrigation).

The view is written to `lovelace/arrosage_view.yaml`; replacing the `arrosage`
view of the storage-mode dashboard is done separately.  It never writes to
Home Assistant.  It relies on the rest sensors of `packages/remplacement_nodered.yaml`,
on `packages/arrosage_manuel.yaml`, on Browser Mod (zone pop-up) and on the Mushroom,
numberbox and card-mod (mod-card) cards.
"""

import json
from pathlib import Path

from generate_heat_manager_dashboard import dump_yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "lovelace" / "arrosage_view.yaml"

# Ordre du cycle : l'Etherain arrose les zones dans cet ordre.
ZONES = [(1, "Bureau", "mdi:briefcase", "bureau"), (2, "Salon", "mdi:sofa", "salon"),
         (3, "Cèdre", "mdi:pine-tree", "cedre"), (4, "Chambre", "mdi:bed", "chambre"),
         (5, "Gouttes", "mdi:water-opacity", "gouttes")]
BLUE = "33,150,243"

# Variables communes à tous les modèles : arrosage en cours, zone en cours, cycle actif.
PRE = ("{% set run = is_state('sensor.etherain_statut_irrigation','Arrosage en cours') %}"
       "{% set cur = states('sensor.etherain_derniere_zone_arrosee')|int(0) if run else 0 %}"
       "{% set cyc = 'court' if is_state('input_boolean.etherain_cycle_court','on') else 'moyen' "
       "if is_state('input_boolean.etherain_cycle_moyen','on') else 'long' "
       "if is_state('input_boolean.etherain_cycle_long','on') else '' %}")
DUR = "states('input_number.etherain_temps_arrosage_cycle_' ~ cyc ~ '_zone_{z}')|int(0)"
NOMS = "{% set noms = " + json.dumps(["", *[z[1] for z in ZONES]], ensure_ascii=False) + " %}"
PULSE = ".shape { animation: pulse 1.4s ease-in-out infinite; }" \
        "@keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.15); } }"


def tpl_card(**kw):
    card = {"type": "custom:mushroom-legacy-template-card"}
    card.update(kw)
    return card


def mod_grid(grid):
    # card-mod ne s'applique pas directement à une grille : on l'enveloppe dans mod-card.
    css = grid.pop("card_mod")["style"]
    return {"type": "custom:mod-card", "card": grid,
            "card_mod": {"style": {"hui-grid-card$": css,
                                   ".": "ha-card { background: none; border: none; box-shadow: none; }"}}}


def header_row():
    # Barre toujours affichée : proportionnelle aux durées pendant un cycle, 5 segments égaux sinon.
    bar = PRE + "{% set ns = namespace(pos=0, tot=0, g=[]) %}"
    bar += "{% if run and cyc %}{% for z in range(1,6) %}{% set ns.tot = ns.tot + (states('input_number.etherain_temps_arrosage_cycle_' ~ cyc ~ '_zone_' ~ z)|int(0)) %}{% endfor %}{% endif %}"
    bar += ("{% set parcycle = run and cyc and ns.tot > 0 %}{% for z in range(1,6) %}"
            "{% set d = (states('input_number.etherain_temps_arrosage_cycle_' ~ cyc ~ '_zone_' ~ z)|int(0)) if parcycle else 1 %}"
            "{% set a = ns.pos %}{% set ns.pos = ns.pos + d / (ns.tot if parcycle else 5) * 100 %}"
            f"{{% set col = 'rgb({BLUE})' if (parcycle and z < cur) else 'rgba({BLUE},0.45)' if z == cur else 'rgba(0,0,0,0.10)' %}}"
            "{% set b = [ns.pos - 1, a]|max %}"
            "{% set ns.g = ns.g + [col ~ ' ' ~ a|round(2) ~ '%', col ~ ' ' ~ b|round(2) ~ '%', 'transparent ' ~ b|round(2) ~ '%', 'transparent ' ~ ns.pos|round(2) ~ '%'] %}"
            "{% endfor %}"
            "ha-card:after { content: ''; display: block; height: 6px; margin: 0 14px 14px; border-radius: 3px;"
            " background: linear-gradient(to right, {{ ns.g|join(', ') }}); }"
            f"{{% if run %}}ha-card {{ border: 1.5px solid rgb({BLUE}); }}{{% endif %}}")
    header = tpl_card(
        entity="sensor.etherain_statut_irrigation",
        icon=PRE + "{{ 'mdi:water' if run else 'mdi:water-off' }}",
        icon_color=PRE + "{{ 'blue' if run else ('amber' if is_state('sensor.etherain_statut_irrigation','Arrosage programmé') else 'grey') }}",
        primary="{{ states('sensor.etherain_statut_irrigation') }}",
        secondary=PRE + NOMS +
        "{% if run and cyc %}Cycle {{ cyc }} · zone {{ cur }} sur 5 · {{ noms[cur] if cur <= 5 else '' }}"
        "{% elif run %}Arrosage manuel · {{ noms[cur] if 1 <= cur <= 5 else 'zone ' ~ cur }}"
        "{% else %}Dernier arrosage : {{ states('sensor.etherain_resultat_commande_irrigation') }}{% endif %}",
        tap_action={"action": "none"}, hold_action={"action": "none"},
        card_mod={"style": {"mushroom-shape-icon$": PRE + "{% if run %}" + PULSE + "{% endif %}", ".": bar}})
    stop = tpl_card(
        icon="mdi:stop", icon_color=PRE + "{{ 'red' if run else 'grey' }}",
        layout="vertical", primary="", secondary="",
        tap_action={"action": "perform-action", "perform_action": "script.etherain_arreter_arrosage_boolean_a_off",
                    "confirmation": {"text": "Arrêter l'arrosage ?"}},
        card_mod={"style": {".": "ha-card { height: 100% !important; justify-content: center; }"}})
    return mod_grid({"type": "grid", "columns": 2, "square": False, "cards": [header, stop],
                     "card_mod": {"style": "#root { grid-template-columns: 1fr 72px !important; align-items: stretch; }\n"
                                           "#root > hui-card { display: block; height: 100%; }\n"
                                           "#root > hui-card > * { display: block; height: 100%; }"}})


def cycles():
    title = mod_grid({"type": "grid", "columns": 2, "square": False, "cards": [
        {"type": "custom:mushroom-title-card", "subtitle": "Lancer un cycle"},
        {"type": "custom:mushroom-chips-card", "alignment": "end", "card_mod": {"style": "ha-card { padding-bottom: 6px; }"},
         "chips": [{"type": "action", "icon": "mdi:cog", "tap_action": {"action": "navigate", "navigation_path": "parametres-arrosage"}}]}],
        "card_mod": {"style": "#root { grid-template-columns: 1fr auto !important; align-items: end; }"}})
    cards = []
    for c, label, icon in (("court", "Court", "mdi:timer-sand"), ("moyen", "Moyen", "mdi:timer-outline"),
                           ("long", "Long", "mdi:timer-plus-outline")):
        total = " + ".join(f"states('input_number.etherain_temps_arrosage_cycle_{c}_zone_{z}')|int(0)" for z in range(1, 6))
        on = f"is_state('input_boolean.etherain_cycle_{c}','on')"
        cards.append(tpl_card(
            entity=f"input_boolean.etherain_cycle_{c}", primary=label, secondary="{{ " + total + " }} min",
            icon=icon, icon_color="{{ 'blue' if " + on + " else 'grey' }}", layout="vertical",
            tap_action={"action": "toggle"}, hold_action={"action": "none"},
            card_mod={"style": {".": "{% if " + on + " %}" + f"ha-card {{ border: 2px solid rgb({BLUE}); background: rgba({BLUE},0.08); }}" + "{% endif %}"}}))
    return [title, {"type": "grid", "columns": 3, "square": False, "cards": cards}]


DUREE = "input_number.etherain_duree_manuelle"
POPUP_CSS = (
    "ha-card { background: none; box-shadow: none; border: none; padding: 12px 0 8px; }\n"
    ".cur-box { display: flex; align-items: center; justify-content: center; gap: 28px; }\n"
    ".cur-num { font-size: 40px !important; font-weight: 500 !important; margin: 0 !important; line-height: 1.2 !important; }\n"
    ".cur-unit { font-size: 18px !important; margin-left: 4px; opacity: 0.6; }\n"
    "ha-icon { --mdc-icon-size: 28px; width: 52px; height: 52px; display: flex; align-items: center; justify-content: center;"
    f" border-radius: 50%; background: rgba({BLUE},0.12); color: rgb({BLUE}); cursor: pointer; padding: 0 !important; }}")


def zone_popup(z, nom):
    # Fenêtre Browser Mod : durée remise à 1 min, − / +, Annuler et Arroser.
    return {"action": "fire-dom-event", "browser_mod": {"service": "browser_mod.sequence", "data": {"sequence": [
        {"service": "input_number.set_value", "data": {"entity_id": DUREE, "value": 1}},
        {"service": "browser_mod.popup", "data": {
            "title": nom,
            "content": {"type": "custom:numberbox-card", "entity": DUREE, "name": False, "icon": False,
                        "border": False, "unit": "min", "card_mod": {"style": POPUP_CSS}},
            "right_button": "Arroser", "right_button_variant": "brand", "right_button_appearance": "accent",
            "right_button_action": {"service": "script.etherain_arroser_duree_choisie", "data": {"zone": z}},
            "left_button": "Annuler", "left_button_variant": "neutral", "left_button_appearance": "plain"}}]}}}


def zones():
    cards = [{"type": "custom:mushroom-title-card", "subtitle": "Zones"}]
    for z, nom, icon, _ in ZONES:
        d = DUR.format(z=z)
        st = PRE + f"{{% set st = 'cours' if cur == {z} else ('fait' if cyc and run and cur > {z} else ('avenir' if cyc and run else 'repos')) %}}"
        cards.append(tpl_card(
            entity=f"binary_sensor.etherain_etat_zone_{z}", primary=nom,
            secondary=st + "{% if st == 'cours' %}En cours{{ ' · ' ~ " + d + " ~ ' min' if cyc else '' }}"
            "{% elif st == 'fait' %}Terminé · {{ " + d + " }} min"
            "{% elif st == 'avenir' %}À venir · {{ " + d + " }} min"
            f"{{% else %}}Zone {z}{{% endif %}}",
            icon=st + f"{{{{ 'mdi:check' if st == 'fait' else '{icon}' }}}}",
            icon_color=st + "{{ 'blue' if st == 'cours' else ('green' if st == 'fait' else 'grey') }}",
            tap_action=zone_popup(z, nom),
            hold_action={"action": "none"},
            card_mod={"style": {
                "mushroom-shape-icon$": st + "{% if st == 'cours' %}" + PULSE + "{% endif %}",
                ".": st + f"{{% if st == 'cours' %}}ha-card {{ border: 2px solid rgb({BLUE}); background: rgba({BLUE},0.08); }}"
                "{% elif st == 'fait' %}ha-card { opacity: 0.75; }{% endif %}"}}))
    return cards


def build():
    chips = {"type": "custom:mushroom-chips-card", "chips": [
        {"type": "back"}, {"type": "action", "tap_action": {"action": "navigate", "navigation_path": "/lovelace-mobile/0"}, "icon": "mdi:home"}]}
    return {"theme": "Backend-selected", "title": "arrosage", "path": "arrosage", "badges": [], "background": "#e4e9f0",
            "cards": [{"type": "grid", "columns": 1, "square": False,
                       "cards": [chips, header_row(), *cycles(), *zones()]}]}


if __name__ == "__main__":
    header = [
        "# Arrosage — vue générée par tools/generate_arrosage_dashboard.py",
        "# Remplacer la vue « arrosage » du tableau de bord lovelace-mobile après validation.",
        "",
    ]
    OUTPUT.write_text("\n".join(header + dump_yaml({"views": [build()]})) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT}")
