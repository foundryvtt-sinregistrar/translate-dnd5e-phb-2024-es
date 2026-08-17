#!/usr/bin/env python3
import json, copy
from collections import Counter, defaultdict
from pathlib import Path

base = Path('.')
SRC_ES = base / 'dnd-players-handbook.actors.json'
SRC_EN = base / 'dnd-players-handbook.actors-en.v2.json'
OUT = base / 'dnd-players-handbook.actors.es.backfilled.from-en-v2.json'
REPORT = base / 'actors_backfill_report.json'

activity_name_manual = {
  "Attack": "Ataque",
  "Activate": "Activar",
  "Save": "Salvación",
  "Heal": "Curar",
  "Use": "Usar",
  "Damage": "Daño",
  "Summon": "Invocar",
  "Check": "Prueba"
}
condition_manual = {
  "start of its turn": "al comienzo de su turno",
  "any other creature that starts its turn within range": "cualquier otra criatura que comience su turno dentro del alcance",
  "the spirit takes damage from a creature": "el espíritu recibe daño de una criatura",
  "A creature that hits the spirit with a melee attack or that starts its turn in a grapple with the spirit": "una criatura que golpee al espíritu con un ataque cuerpo a cuerpo o que comience su turno en un agarre con el espíritu",
  "start of its turn, if it has at least 1 Hit Point": "al comienzo de su turno, si tiene al menos 1 punto de golpe",
  "start of your turn": "al comienzo de tu turno",
  "the sphinx or another creature within 30 feet makes an ability check or a saving throw": "la esfinge u otra criatura a 30 pies o menos realiza una prueba de característica o una tirada de salvación",
  "immediately after hitting a target with a Melee weapon or an Unarmed Strike": "inmediatamente después de golpear a un objetivo con un arma cuerpo a cuerpo o un Golpe sin armas",
  "Immediately after hitting a creature with a weapon": "inmediatamente después de golpear a una criatura con un arma",
  "when you or a creature you can see within 60 feet of you falls": "cuando tú o una criatura que puedas ver a 60 pies o menos de ti caiga",
  "visible creature moves or ends its turn within 10 feet of the pack": "una criatura visible se mueve o termina su turno a 10 pies o menos de la manada",
  "Bonus Action used by summoner": "acción adicional usada por el invocador",
  "upon appearing": "al aparecer",
  "Any creature ends its turn within range": "cualquier criatura termina su turno dentro del alcance"
}
adv_title_manual = {
  "Ability Score Improvement": "Mejora de característica",
  "Size": "Tamaño",
  "Subclass": "Subclase",
  "Hit Points": "Puntos de golpe",
  "Grant Items": "Conceder objetos",
  "Epic Boon": "Don épico",
  "Skills": "Habilidades",
  "Saving Throws": "Tiradas de salvación"
}
adv_hint_manual = {
  "Intelligence, Wisdom, or Charisma can be chosen for your spellcasting ability.": "Puede elegirse Inteligencia, Sabiduría o Carisma como característica de lanzamiento de conjuros."
}

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

actors_es = load(SRC_ES)
actors_en = load(SRC_EN)
patched = copy.deepcopy(actors_es)
stats = Counter()
untranslated = defaultdict(Counter)

for k, v in actors_en.get('folders', {}).items():
    if k not in patched['folders']:
        patched['folders'][k] = patched['folders'].get(k, k)
        stats['folders_added'] += 1

for aid, a_es in patched['entries'].items():
    a_en = actors_en['entries'].get(aid, {})
    if 'description' not in a_es or a_es.get('description') in [None, '']:
        src = a_es.get('biography') if a_es.get('biography') not in [None, ''] else a_en.get('description', '')
        if src not in [None, '']:
            a_es['description'] = src
            stats['actor.description_filled'] += 1

    for iid, i_es in a_es.get('items', {}).items():
        i_en = a_en.get('items', {}).get(iid, {})

        for act_id, act_es in i_es.get('activities', {}).items():
            act_en = i_en.get('activities', {}).get(act_id, {})
            if not act_en:
                continue

            if (act_es.get('name') in [None, '']) and act_en.get('name'):
                tr = activity_name_manual.get(act_en['name'])
                if tr:
                    act_es['name'] = tr
                    stats['activity.name_filled'] += 1
                else:
                    untranslated['activity.name'][act_en['name']] += 1

            for field in ['range', 'duration']:
                if (act_es.get(field) in [None, '']) and act_en.get(field) not in [None, '']:
                    act_es[field] = act_en[field]
                    stats[f'activity.{field}_filled'] += 1

            if (act_es.get('condition') in [None, '']) and act_en.get('condition'):
                tr = condition_manual.get(act_en['condition'])
                if tr:
                    act_es['condition'] = tr
                    stats['activity.condition_filled'] += 1
                else:
                    untranslated['activity.condition'][act_en['condition']] += 1

        for adv_id, adv_es in i_es.get('advancement', {}).items():
            adv_en = i_en.get('advancement', {}).get(adv_id, {})
            if not adv_en:
                continue

            if (adv_es.get('title') in [None, '']) and adv_en.get('title'):
                tr = adv_title_manual.get(adv_en['title'])
                if tr:
                    adv_es['title'] = tr
                    stats['advancement.title_filled'] += 1
                else:
                    untranslated['advancement.title'][adv_en['title']] += 1

            if (adv_es.get('hint') in [None, '']) and adv_en.get('hint'):
                tr = adv_hint_manual.get(adv_en['hint'])
                if tr:
                    adv_es['hint'] = tr
                    stats['advancement.hint_filled'] += 1
                else:
                    untranslated['advancement.hint'][adv_en['hint']] += 1

patched['folders'] = {k: patched['folders'][k] for k in sorted(patched['folders'])}
patched['entries'] = {k: patched['entries'][k] for k in sorted(patched['entries'])}
for aid, a in patched['entries'].items():
    if 'items' in a and isinstance(a['items'], dict):
        a['items'] = {k: a['items'][k] for k in sorted(a['items'])}
        for iid, item in a['items'].items():
            for sec in ['activities', 'effects', 'advancement']:
                if sec in item and isinstance(item[sec], dict):
                    item[sec] = {k: item[sec][k] for k in sorted(item[sec])}

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(patched, f, ensure_ascii=False, indent=2)

with open(REPORT, 'w', encoding='utf-8') as f:
    json.dump({
        'source_es': SRC_ES.name,
        'source_en': SRC_EN.name,
        'output': OUT.name,
        'stats': dict(stats),
        'manual_translation_maps': {
            'activity_name': activity_name_manual,
            'condition': condition_manual,
            'advancement_title': adv_title_manual,
            'advancement_hint': adv_hint_manual,
        },
        'untranslated_remaining': {k: dict(v) for k, v in untranslated.items() if v}
    }, f, ensure_ascii=False, indent=2)

print('OK', OUT.name)
print(json.dumps(dict(stats), ensure_ascii=False, indent=2))
