"""Generate the « Paramètres techniques » views of the lovelace-mobile dashboard.

The views are written to `lovelace/technical_views.yaml`; merging them into the
storage-mode dashboard is done separately.  It never writes to Home Assistant.
They rely on `packages/monitoring.yaml` and `custom_templates/monitoring.jinja`
(sensor.resume_technique, sensor.batteries_zigbee_faibles, ...) and on the
Mushroom, card-mod, bar-card and auto-entities cards.
"""

from pathlib import Path

from generate_heat_manager_dashboard import dump_yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "lovelace" / "technical_views.yaml"
D = "/lovelace-mobile"
BG = "#e4e9f0"
FULL = {"columns": "full", "rows": "auto"}
HALF = {"columns": 6, "rows": "auto"}
BATTERY_SOURCES = "(integration_entities('mqtt') + integration_entities('hue')) | select('match', 'sensor\\..*_(battery|batterie)$') | expand | selectattr('attributes.device_class', 'eq', 'battery')"


def nav(path):
    return {"action": "navigate", "navigation_path": f"{D}/{path}"}


def more(entity):
    return {"action": "more-info", "entity": entity}


def chips():
    return {"type": "custom:mushroom-chips-card", "chips": [
        {"type": "back"},
        {"type": "action", "tap_action": {"action": "navigate", "navigation_path": f"{D}/0"}, "icon": "mdi:home"},
    ]}


def title(text, sub=None):
    c = {"type": "custom:mushroom-title-card", "title": text}
    if sub:
        c["subtitle"] = sub
    return c


def section(text):
    return {"type": "custom:mushroom-title-card", "subtitle": text}


def tpl(primary, secondary, icon, color, tap=None, entity=None, half=False, multiline=False):
    c = {"type": "custom:mushroom-template-card", "primary": primary, "secondary": secondary,
         "icon": icon, "icon_color": color}
    if entity:
        c["entity"] = entity
    c["tap_action"] = tap or ({"action": "more-info"} if entity else {"action": "none"})
    if multiline or half:
        c["multiline_secondary"] = True
    c["grid_options"] = HALF if half else FULL
    return c


def bar(entities, title_=None, warn=70, alert=85, max_=100, severity=None):
    """Percentage bars: green, orange from `warn`, red from `alert` (or an explicit `severity`)."""
    c = {"type": "custom:bar-card", "entities": entities, "positions": {"icon": "off", "indicator": "off"},
         "height": 26, "max": max_, "severity": severity or [
             {"from": 0, "to": warn, "color": "#639922"},
             {"from": warn, "to": alert, "color": "#EF9F27"},
             {"from": alert, "to": max_, "color": "#E24B4A"}]}
    if title_:
        c["title"] = title_
    c["grid_options"] = FULL
    return c


def view(title_, path, cards, icon=None):
    v = {"title": title_, "path": path, "type": "sections", "max_columns": 1,
         "sections": [{"type": "grid", "cards": [dict(chips(), grid_options=FULL), dict(title(title_), grid_options=FULL), *cards]}],
         "background": BG, "visible": False}
    if icon:
        v["icon"] = icon
    return v


def ok_color(cond_ok, cond_warn="false"):
    return "{{ 'green' if " + cond_ok + " else 'orange' if " + cond_warn + " else 'red' }}"


# ---------------------------------------------------------------- main page
RESUME = "sensor.resume_technique"
ALERT_BANNER = {
    "type": "conditional",
    "conditions": [{"condition": "state", "entity": RESUME, "state": "alerte"}],
    "card": {"type": "custom:mushroom-template-card", "entity": RESUME, "primary": "À traiter",
             "secondary": "{{ state_attr('" + RESUME + "', 'alertes') | join('\\n') }}",
             "multiline_secondary": True, "icon": "mdi:alert", "icon_color": "red",
             "card_mod": {"style": "ha-card { background: #FCEBEB; --primary-text-color: #791F1F; --secondary-text-color: #A32D2D; }"}},
    "grid_options": FULL,
}


def main_view():
    pct = lambda e: "states('" + e + "') | float(0)"
    tiles = [
        tpl("Serveur HA",
            "CPU {{ states('sensor.home_assistant_core_pourcentage_du_processeur') | float(0) | round(0) }} % · disque {{ states('sensor.disque_serveur_ha_utilise') }} %",
            "mdi:home-assistant", ok_color(pct("sensor.disque_serveur_ha_utilise") + " <= 85"), nav("technique-serveur"), half=True),
        tpl("NAS", "{{ 'Normal' if is_state('sensor.nas_eric_status', 'normal') else states('sensor.nas_eric_status') }} · {{ states('sensor.nas_eric_volume_used') | float(0) | round(0) }} %",
            "mdi:nas", ok_color("is_state('sensor.nas_eric_status', 'normal') and " + pct("sensor.nas_eric_volume_used") + " <= 85"), nav("technique-nas"), half=True),
        tpl("Onduleur", "{{ 'Secteur' if states('sensor.ups_code_d_etat').startswith('OL') else 'Sur batterie' }} · {{ (states('sensor.ups_autonomie_de_la_batterie') | float(0) / 60) | round(0) }} min",
            "mdi:power-plug-battery", ok_color("states('sensor.ups_code_d_etat').startswith('OL')"), nav("technique-onduleur"), half=True),
        tpl("Batteries", "{% set n = states('sensor.batteries_zigbee_faibles') | int(0) %}{{ 'Toutes OK' if n == 0 else n ~ ' à remplacer' }}",
            "mdi:battery-heart-variant", ok_color("states('sensor.batteries_zigbee_faibles') | int(0) == 0"), nav("technique-batteries"), half=True),
        tpl("Zigbee", "{{ 'Connecté' if is_state('binary_sensor.zigbee2mqtt_bridge_connection_state', 'on') else 'Déconnecté' }} · {{ states('sensor.appareils_zigbee_indisponibles') }} hors ligne",
            "mdi:zigbee", ok_color("is_state('binary_sensor.zigbee2mqtt_bridge_connection_state', 'on') and states('sensor.appareils_zigbee_indisponibles') | int(0) == 0",
                                   "is_state('binary_sensor.zigbee2mqtt_bridge_connection_state', 'on')"), nav("technique-zigbee"), half=True),
        tpl("Mises à jour", "{% set n = states('sensor.mises_a_jour_en_attente') | int(0) %}{{ 'À jour' if n == 0 else n ~ ' en attente' }}",
            "mdi:package-up", "{{ 'green' if states('sensor.mises_a_jour_en_attente') | int(0) == 0 else 'orange' }}", nav("technique-mises-a-jour"), half=True),
        tpl("Sauvegardes", "{% set t = state_attr('sensor.backup_state', 'last_backup') %}{{ 'Dernière ' ~ (as_datetime(t) | as_local).strftime('%d/%m %H:%M') if t else states('sensor.backup_state') }}",
            "mdi:cloud-upload", "{{ 'red' if is_state('binary_sensor.backups_stale', 'on') else 'green' }}", nav("technique-sauvegardes"), half=True),
        tpl("Santé config", "{% set w = states('sensor.watchman_missing_entities') | int(0) %}{{ 'Aucune anomalie' if w == 0 else w ~ ' entités manquantes' }}",
            "mdi:stethoscope", "{{ 'green' if states('sensor.watchman_missing_entities') | int(0) == 0 else 'orange' }}", nav("technique-sante"), half=True),
    ]
    return view("Paramètres techniques", "technique", [ALERT_BANNER, *tiles], icon="mdi:server")


# ---------------------------------------------------------------- sub pages
def serveur_view():
    return view("Serveur HA", "technique-serveur", [
        section("Ressources de la VM"),
        bar([{"entity": "sensor.home_assistant_core_pourcentage_du_processeur", "name": "CPU Home Assistant"},
             {"entity": "sensor.home_assistant_core_pourcentage_de_memoire", "name": "Mémoire Home Assistant"},
             {"entity": "sensor.disque_serveur_ha_utilise", "name": "Disque"}]),
        tpl("Disque", "{{ states('sensor.home_assistant_host_taille_du_disque_utilise') }} Go utilisés sur {{ states('sensor.home_assistant_host_taille_total_du_disque') }} Go · {{ states('sensor.home_assistant_host_taille_du_disque_libre') }} Go libres",
            "mdi:harddisk", "blue", entity="sensor.home_assistant_host_taille_du_disque_libre"),
        section("Versions"),
        tpl("Core HA", "{{ state_attr('update.home_assistant_core_update', 'installed_version') }}{{ ' → ' ~ state_attr('update.home_assistant_core_update', 'latest_version') if is_state('update.home_assistant_core_update', 'on') }}",
            "mdi:home-assistant", "{{ 'orange' if is_state('update.home_assistant_core_update', 'on') else 'green' }}", entity="update.home_assistant_core_update", half=True),
        tpl("Système (OS)", "{{ state_attr('update.home_assistant_operating_system_update', 'installed_version') }}{{ ' → ' ~ state_attr('update.home_assistant_operating_system_update', 'latest_version') if is_state('update.home_assistant_operating_system_update', 'on') }}",
            "mdi:linux", "{{ 'orange' if is_state('update.home_assistant_operating_system_update', 'on') else 'green' }}", entity="update.home_assistant_operating_system_update", half=True),
        tpl("Supervisor", "{{ state_attr('update.home_assistant_supervisor_update', 'installed_version') }}",
            "mdi:cog-outline", "{{ 'orange' if is_state('update.home_assistant_supervisor_update', 'on') else 'green' }}", entity="update.home_assistant_supervisor_update", half=True),
        tpl("Accès distant", "{{ 'Nabu Casa actif' if is_state('binary_sensor.remote_ui', 'on') else 'Inactif' }}",
            "mdi:cloud-lock-outline", "{{ 'green' if is_state('binary_sensor.remote_ui', 'on') else 'red' }}", entity="binary_sensor.remote_ui", half=True),
        section("Modules complémentaires"),
        tpl("Zigbee2MQTT", "{{ 'En marche' if is_state('binary_sensor.zigbee2mqtt_en_cours_d_execution', 'on') else 'Arrêté' }}",
            "mdi:zigbee", "{{ 'green' if is_state('binary_sensor.zigbee2mqtt_en_cours_d_execution', 'on') else 'red' }}", entity="binary_sensor.zigbee2mqtt_en_cours_d_execution", half=True),
        tpl("Mosquitto", "{{ 'En marche' if is_state('binary_sensor.mosquitto_broker_en_cours_d_execution', 'on') else 'Arrêté' }}",
            "mdi:message-processing-outline", "{{ 'green' if is_state('binary_sensor.mosquitto_broker_en_cours_d_execution', 'on') else 'red' }}", entity="binary_sensor.mosquitto_broker_en_cours_d_execution", half=True),
    ], icon="mdi:home-assistant")


def nas_view():
    disk = lambda i, sfx: tpl(f"Disque {i}", "{{ states('sensor.nas_eric_temperature" + sfx + "') }} °C · {{ 'normal' if is_state('sensor.nas_eric_status" + sfx + "', 'normal') else states('sensor.nas_eric_status" + sfx + "') }}",
                              "mdi:harddisk", "{{ 'green' if is_state('sensor.nas_eric_status" + sfx + "', 'normal') and states('sensor.nas_eric_temperature" + sfx + "') | float(0) < 50 else 'red' }}",
                              entity="sensor.nas_eric_temperature" + sfx, half=True)
    return view("NAS Synology", "technique-nas", [
        tpl("État", "{{ 'Normal' if is_state('sensor.nas_eric_status', 'normal') else states('sensor.nas_eric_status') }} · DSM {{ 'à mettre à jour' if is_state('update.nas_eric_dsm_update', 'on') else 'à jour' }}",
            "mdi:nas", "{{ 'green' if is_state('sensor.nas_eric_status', 'normal') else 'red' }}", entity="sensor.nas_eric_status"),
        section("Ressources"),
        bar([{"entity": "sensor.nas_eric_cpu_utilization_total", "name": "CPU"},
             {"entity": "sensor.nas_eric_memory_usage_real", "name": "Mémoire"},
             {"entity": "sensor.nas_eric_volume_used", "name": "Volume"},
             {"entity": "sensor.nas_eric_usb_disk_1_partition_1_partition_utilisee", "name": "Disque USB"}]),
        section("Disques"),
        disk(1, ""), disk(2, "_2"), disk(3, "_3"),
        tpl("Santé disques", "{{ 'Aucun secteur défectueux, durée de vie OK' if is_state('binary_sensor.nas_eric_exceeded_max_bad_sectors', 'off') and is_state('binary_sensor.nas_eric_exceeded_max_bad_sectors_2', 'off') and is_state('binary_sensor.nas_eric_below_min_remaining_life', 'off') and is_state('binary_sensor.nas_eric_below_min_remaining_life_2', 'off') else 'Problème détecté' }}",
            "mdi:heart-pulse", "{{ 'green' if is_state('binary_sensor.nas_eric_exceeded_max_bad_sectors', 'off') and is_state('binary_sensor.nas_eric_exceeded_max_bad_sectors_2', 'off') and is_state('binary_sensor.nas_eric_below_min_remaining_life', 'off') and is_state('binary_sensor.nas_eric_below_min_remaining_life_2', 'off') else 'red' }}",
            entity="binary_sensor.nas_eric_exceeded_max_bad_sectors", half=True),
        section("Actions", ),
        {"type": "custom:mushroom-template-card", "primary": "Redémarrer", "secondary": "Appui long", "icon": "mdi:restart", "icon_color": "orange",
         "entity": "button.nas_eric_reboot", "tap_action": {"action": "none"},
         "hold_action": {"action": "perform-action", "perform_action": "button.press", "target": {"entity_id": "button.nas_eric_reboot"},
                         "confirmation": {"text": "Redémarrer le NAS ? Home Assistant (VM) sera arrêté pendant le redémarrage."}},
         "grid_options": HALF},
        {"type": "custom:mushroom-template-card", "primary": "Éteindre", "secondary": "Appui long", "icon": "mdi:power", "icon_color": "red",
         "entity": "button.nas_eric_shutdown", "tap_action": {"action": "none"},
         "hold_action": {"action": "perform-action", "perform_action": "button.press", "target": {"entity_id": "button.nas_eric_shutdown"},
                         "confirmation": {"text": "Éteindre le NAS ? Home Assistant (VM) s'arrêtera et ne redémarrera pas seul."}},
         "grid_options": HALF},
    ], icon="mdi:nas")


def onduleur_view():
    return view("Onduleur", "technique-onduleur", [
        tpl("État", "{{ states('sensor.ups_etat') }} ({{ states('sensor.ups_code_d_etat') }})", "mdi:power-plug-battery",
            "{{ 'green' if states('sensor.ups_code_d_etat').startswith('OL') else 'red' }}", entity="sensor.ups_etat"),
        bar([{"entity": "sensor.ups_charge_de_la_batterie", "name": "Charge de la batterie"}], severity=[
            {"from": 0, "to": 20, "color": "#E24B4A"}, {"from": 20, "to": 50, "color": "#EF9F27"}, {"from": 50, "to": 100, "color": "#639922"}]),
        tpl("Autonomie", "{{ (states('sensor.ups_autonomie_de_la_batterie') | float(0) / 60) | round(0) }} min", "mdi:timer-sand", "blue",
            entity="sensor.ups_autonomie_de_la_batterie", half=True),
        tpl("Charge de sortie", "{{ states('sensor.ups_charge') }} %", "mdi:gauge", "blue", entity="sensor.ups_charge", half=True),
        tpl("Tension", "{{ states('sensor.ups_tension_de_sortie') }} V", "mdi:sine-wave", "blue", entity="sensor.ups_tension_de_sortie", half=True),
        tpl("Délai d'arrêt", "{{ states('sensor.ups_delai_d_arret_de_l_onduleur') }} s", "mdi:timer-off-outline", "grey",
            entity="sensor.ups_delai_d_arret_de_l_onduleur", half=True),
        tpl("Seuil bas", "{{ states('sensor.ups_consigne_de_batterie_faible') }} %", "mdi:battery-alert-variant-outline", "grey",
            entity="sensor.ups_consigne_de_batterie_faible", half=True),
        tpl("Batterie", "{{ states('sensor.ups_chimie_de_la_batterie') }} (plomb)", "mdi:car-battery", "grey",
            entity="sensor.ups_chimie_de_la_batterie", half=True),
    ], icon="mdi:power-plug-battery")


def battery_group(label, cond):
    """auto-entities list of Zigbee batteries whose level matches `cond` (Jinja on `lvl`)."""
    template = (
        "{% set seuil = states('input_number.seuil_alerte_batterie') | float(20) %}"
        "{% set ns = namespace(l=[]) %}"
        "{% for s in " + BATTERY_SOURCES + " %}"
        "{% set lvl = s.state | float(-1) %}"
        "{% if " + cond + " %}{% set ns.l = ns.l + [{'lvl': lvl, 'entity': s.entity_id, 'name': s.name | regex_replace(' (Batterie|Battery)$', '')}] %}{% endif %}"
        "{% endfor %}"
        "{% set out = namespace(l=[]) %}"
        "{% for b in ns.l | sort(attribute='lvl') %}{% set out.l = out.l + [{'entity': b.entity, 'name': b.name}] %}{% endfor %}"
        "{{ out.l }}"
    )
    return {"type": "custom:auto-entities", "show_empty": False,
            "card": {"type": "custom:bar-card", "title": label, "positions": {"icon": "off", "indicator": "off"}, "height": 26,
                     "severity": [{"from": 0, "to": 20, "color": "#E24B4A"}, {"from": 20, "to": 40, "color": "#EF9F27"}, {"from": 40, "to": 100, "color": "#639922"}]},
            "filter": {"template": template},
            "grid_options": FULL}


def batteries_view():
    return view("Batteries", "technique-batteries", [
        {"type": "custom:mushroom-number-card", "entity": "input_number.seuil_alerte_batterie", "name": "Seuil d'alerte",
         "icon_color": "red", "display_mode": "buttons", "grid_options": FULL},
        tpl("Alerte quotidienne", "Résumé à 19:00 sur l'iPhone si une batterie est sous le seuil", "mdi:bell-outline", "grey",
            entity="automation.alerte_batteries_zigbee_faibles"),
        battery_group("À remplacer", "lvl >= 0 and lvl < seuil"),
        battery_group("À surveiller", "lvl >= seuil and lvl < 40"),
        battery_group("OK", "lvl >= 40 and lvl >= seuil"),
        battery_group("Sans nouvelles", "lvl < 0"),
    ], icon="mdi:battery-heart-variant")


def zigbee_view():
    slzb = lambda n, label: tpl(f"SLZB {label}",
                                "{{ states('sensor.slzb_06_" + n + "_connection_mode') }} · puce {{ states('sensor.slzb_06_" + n + "_temperature_de_la_puce_zigbee') | float(0) | round(0) }} °C",
                                "mdi:router-wireless", "{{ 'orange' if is_state('update.slzb_06_" + n + "_zigbee_firmware', 'on') or is_state('update.slzb_06_" + n + "_core_firmware', 'on') else 'green' }}",
                                entity="sensor.slzb_06_" + n + "_temperature_de_la_puce_zigbee", half=True)
    return view("Zigbee", "technique-zigbee", [
        tpl("Zigbee2MQTT", "{{ 'Connecté' if is_state('binary_sensor.zigbee2mqtt_bridge_connection_state', 'on') else 'Déconnecté' }} · version {{ states('sensor.zigbee2mqtt_bridge_version') }}",
            "mdi:zigbee", "{{ 'green' if is_state('binary_sensor.zigbee2mqtt_bridge_connection_state', 'on') else 'red' }}", entity="binary_sensor.zigbee2mqtt_bridge_connection_state"),
        tpl("Hors ligne", "{% set n = states('sensor.appareils_zigbee_indisponibles') | int(0) %}{{ 'Aucun' if n == 0 else n }}",
            "mdi:lan-disconnect", "{{ 'green' if states('sensor.appareils_zigbee_indisponibles') | int(0) == 0 else 'orange' }}", entity="sensor.appareils_zigbee_indisponibles", half=True),
        tpl("Appairage", "{{ 'OUVERT' if is_state('switch.zigbee2mqtt_bridge_permit_join', 'on') else 'Fermé' }}",
            "mdi:link-variant", "{{ 'red' if is_state('switch.zigbee2mqtt_bridge_permit_join', 'on') else 'grey' }}", entity="switch.zigbee2mqtt_bridge_permit_join",
            tap={"action": "toggle"}, half=True),
        section("Coordinateurs"),
        slzb("cave", "cave"), slzb("avant", "avant"), slzb("debarras", "débarras"),
        section("Actions"),
        {"type": "custom:mushroom-template-card", "primary": "Redémarrer Zigbee2MQTT", "secondary": "Appui long", "icon": "mdi:restart", "icon_color": "orange",
         "entity": "button.zigbee2mqtt_bridge_restart", "tap_action": {"action": "none"},
         "hold_action": {"action": "perform-action", "perform_action": "button.press", "target": {"entity_id": "button.zigbee2mqtt_bridge_restart"},
                         "confirmation": {"text": "Redémarrer Zigbee2MQTT ? Les appareils Zigbee seront injoignables une minute."}},
         "grid_options": FULL},
    ], icon="mdi:zigbee")


def updates_view():
    return view("Mises à jour", "technique-mises-a-jour", [
        {"type": "custom:auto-entities", "show_empty": True,
         "card": {"type": "entities", "state_color": True},
         "filter": {"include": [{"domain": "update", "state": "on"}]},
         "sort": {"method": "name"},
         "else": {"type": "custom:mushroom-template-card", "primary": "Tout est à jour", "icon": "mdi:check-circle", "icon_color": "green"},
         "grid_options": FULL},
        tpl("Installer", "Touche une ligne pour voir les notes de version et installer", "mdi:information-outline", "grey"),
    ], icon="mdi:package-up")


def backups_view():
    a = lambda k: "state_attr('sensor.backup_state', '" + k + "')"
    return view("Sauvegardes", "technique-sauvegardes", [
        tpl("Google Drive Backup", "{{ 'Sauvegarde trop ancienne' if is_state('binary_sensor.backups_stale', 'on') else 'À jour' }}",
            "mdi:google-drive", "{{ 'red' if is_state('binary_sensor.backups_stale', 'on') else 'green' }}", entity="binary_sensor.backups_stale"),
        tpl("Dernière", "{{ (as_datetime(" + a("last_backup") + ") | as_local).strftime('%d/%m à %H:%M') if " + a("last_backup") + " else '—' }}",
            "mdi:history", "blue", entity="sensor.backup_state", half=True),
        tpl("Prochaine", "{{ (as_datetime(" + a("next_backup") + ") | as_local).strftime('%d/%m à %H:%M') if " + a("next_backup") + " else '—' }}",
            "mdi:calendar-clock", "blue", entity="sensor.backup_state", half=True),
        tpl("Sur Google Drive", "{{ " + a("backups_in_google_drive") + " }} sauvegardes · {{ " + a("size_in_google_drive") + " }}",
            "mdi:cloud-check-outline", "blue", entity="sensor.backup_state", half=True),
        tpl("Sur la VM", "{{ " + a("backups_in_home_assistant") + " }} sauvegardes · {{ " + a("size_in_home_assistant") + " }}",
            "mdi:harddisk", "grey", entity="sensor.backup_state", half=True),
    ], icon="mdi:cloud-upload")


def sante_view():
    return view("Santé de la configuration", "technique-sante", [
        tpl("Résumé", "{% set l = (state_attr('" + RESUME + "', 'alertes') or []) + (state_attr('" + RESUME + "', 'avertissements') or []) %}{{ l | join('\\n') if l else 'Tout est normal' }}",
            "mdi:clipboard-pulse-outline", "{{ {'ok': 'green', 'attention': 'orange'}.get(states('" + RESUME + "'), 'red') }}", entity=RESUME, multiline=True),
        section("Watchman"),
        tpl("Entités", "{{ states('sensor.watchman_missing_entities') }}", "mdi:shape-outline",
            "{{ 'green' if states('sensor.watchman_missing_entities') | int(0) == 0 else 'orange' }}", entity="sensor.watchman_missing_entities", half=True),
        tpl("Actions", "{{ states('sensor.watchman_missing_actions') }}", "mdi:function-variant",
            "{{ 'green' if states('sensor.watchman_missing_actions') | int(0) == 0 else 'orange' }}", entity="sensor.watchman_missing_actions", half=True),
        tpl("Dernière analyse", "{{ (as_datetime(states('sensor.watchman_last_updated')) | as_local).strftime('%d/%m à %H:%M') if states('sensor.watchman_last_updated') not in ['unknown', 'unavailable'] else '—' }}",
            "mdi:magnify-scan", "grey", entity="sensor.watchman_last_updated"),
    ], icon="mdi:stethoscope")


HOME_CARD = {
    "type": "custom:mushroom-template-card", "entity": RESUME, "primary": "Paramètres techniques",
    "secondary": "{% set l = (state_attr('" + RESUME + "', 'alertes') or []) + (state_attr('" + RESUME + "', 'avertissements') or []) %}{{ l | join(' · ') if l else 'Tout est normal' }}",
    "icon": "mdi:server", "icon_color": "{{ {'ok': 'green', 'attention': 'orange'}.get(states('" + RESUME + "'), 'red') }}",
    "tap_action": nav("technique"), "hold_action": nav("technique"), "double_tap_action": nav("technique"),
}


def build():
    return [main_view(), serveur_view(), nas_view(), onduleur_view(), batteries_view(), zigbee_view(), updates_view(), backups_view(), sante_view()]


if __name__ == "__main__":
    header = [
        "# Paramètres techniques — vues générées par tools/generate_technical_dashboard.py",
        "# Remplacer les vues technique* du tableau de bord lovelace-mobile après validation.",
        "# La carte d'accès de l'accueil est HOME_CARD dans le générateur.",
        "",
    ]
    views = build()
    OUTPUT.write_text("\n".join(header + dump_yaml({"views": views})) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT} with {len(views)} views")
