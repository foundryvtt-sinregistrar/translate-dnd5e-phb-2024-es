import json, os, re, copy
from collections import Counter, defaultdict

base = os.path.dirname(__file__) or '.'
es_path = os.path.join(base, 'dnd-players-handbook.spells.json')
en_old_path = os.path.join(base, 'dnd-players-handbook.spells-en.json')

with open(es_path, encoding='utf-8') as f:
    es = json.load(f)
with open(en_old_path, encoding='utf-8') as f:
    en_old = json.load(f)

def s(v):
    return v if isinstance(v, str) else ''

translation_memory = defaultdict(Counter)
for stem in ['classes', 'equipment', 'feats', 'origins', 'spells']:
    enf = os.path.join(base, f'dnd-players-handbook.{stem}-en.json')
    esf = os.path.join(base, f'dnd-players-handbook.{stem}.json')
    if not (os.path.exists(enf) and os.path.exists(esf)):
        continue
    with open(enf, encoding='utf-8') as f:
        en_doc = json.load(f)
    with open(esf, encoding='utf-8') as f:
        es_doc = json.load(f)
    for eid, en_entry in en_doc.get('entries', {}).items():
        es_entry = es_doc.get('entries', {}).get(eid, {})
        for aid, en_act in en_entry.get('activities', {}).items():
            en_name = s(en_act.get('name'))
            es_name = s(es_entry.get('activities', {}).get(aid, {}).get('name'))
            if en_name and es_name:
                translation_memory[en_name][es_name] += 1

manual_name_map = {k: v.most_common(1)[0][0] for k, v in translation_memory.items()}
manual_name_map.update({
    'Attack': 'Ataque',
    'Save': 'Salvación',
    'Heal': 'Curar',
    'Summon': 'Invocar',
    'Cast': 'Lanzar',
    'Use': 'Lanzar',
    'Damage': 'Daño',
    'Create Door': 'Crear puerta',
    'Move Hound': 'Mover sabueso',
    'Create Lights': 'Crear luces',
    'Move Lights': 'Mover luces',
    'Create Illusion': 'Crear ilusión',
    'Beckon Element': 'Invocar elemento',
    'Sculpt Element': 'Esculpir elemento',
    'Summon Steed': 'Invocar corcel',
    'Summon Flying Steed': 'Invocar corcel volador',
    'Hurl Fire': 'Lanzar fuego',
    'Imbue Weapon': 'Imbuir arma'
})

manual_overrides = {
    ('phbutlMagicalBer','dnd5eactivity000'): {'name': 'Curar'},
    ('phbsplAcidSplash','eOJpSDmq0JkmzpAV'): {'name': 'Salvación','target':'5 sphere','range':'60 ft'},
    ('phbsplBladeWard0','1wca3rjsdb0agWqk'): {'name': 'Lanzar','duration':'1 minute'},
    ('phbFaithfulHound','oXwEMXLXZLw2Ub0g'): {'name': 'Invocar','range':'30 ft','duration':'8 hour'},
    ('phbFaithfulHound','vIOe9RHtAUBrnsR6'): {'range':'30 ft'},
    ('phbPrivateSanctu','MoyU67fLjbEiZLGE'): {'name': 'Lanzar','target':'100 cube','range':'120 ft','duration':'24 hour'},
    ('phbsplPrayerofHe','dnd5eactivity000'): {'name': 'Curar','range':'30 ft'},
    ('phbsplProtection','dnd5eactivity000'): {'name': 'Lanzar','duration':'1 hour'},
    ('phbsplGuidance00','R6Fs3rsgXlgHPOFn'): {'name': 'Lanzar','duration':'1 minute'},
    ('phbsplFear000000','dnd5eactivity000'): {'name': 'Salvación','target':'30 cone','duration':'1 minute'},
    ('phbsplFindTraps0','dnd5eactivity000'): {'name': 'Lanzar','range':'120 ft'},
    ('phbsplFindSteed0','dnd5eactivity000'): {'name': 'Invocar corcel','range':'30 ft'},
    ('phbsplFindSteed0','o4YsONnsS8rOOEaS'): {'name': 'Invocar corcel volador','range':'30 ft'},
}

def strip_html(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&amp;', '&')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def infer_name(entry_id, aid, es_entry, es_act, en_entry, en_act):
    ov = manual_overrides.get((entry_id, aid))
    if ov and 'name' in ov:
        return ov['name'], 'manual_override'
    if s(es_act.get('name')):
        return s(es_act.get('name')), None

    en_name = s(en_act.get('name'))
    if en_name:
        return manual_name_map.get(en_name, en_name), 'old_en_map'

    spell_name_es = s(es_entry.get('name'))
    desc_en = strip_html(s(en_entry.get('description'))).lower()
    desc_es = strip_html(s(es_entry.get('description'))).lower()
    other_names = [s(a.get('name')) for k, a in es_entry.get('activities', {}).items() if k != aid and s(a.get('name'))]

    if 'Mover sabueso' in other_names:
        return 'Invocar', 'context_move_hound'
    if any('Dados de Golpe' in n for n in other_names):
        return 'Lanzar', 'context_hit_dice'
    if spell_name_es.startswith('Portal arcano'):
        return 'Crear puerta', 'specific_arcane_gate'
    if spell_name_es.startswith('Santuario privado de Mordenkainen'):
        return 'Lanzar', 'specific_private_sanctum'
    if spell_name_es.startswith('Sabueso fiel de Mordenkainen'):
        return 'Invocar', 'specific_faithful_hound'
    if spell_name_es.startswith('Bayas Mágicas'):
        return 'Curar', 'specific_magical_berries'
    if spell_name_es.startswith('Protección contra'):
        return 'Lanzar', 'specific_protection'

    if re.search(r'\bmake (?:a|an) (?:melee|ranged)? ?spell attack\b', desc_en) or re.search(r'\bmake (?:a|an) (?:melee|ranged) attack\b', desc_en):
        return 'Ataque', 'attack_make'
    if re.search(r'\bmust (?:succeed on|make) a [a-z]+ saving throw\b', desc_en) or re.search(r'\beach creature .* (?:must )?make[s]? a [a-z]+ saving throw\b', desc_en):
        if 'at the start of each of its turns' in desc_en:
            return 'Salvación al inicio del turno', 'save_start_of_turn'
        if 'at the end of each of its turns' in desc_en:
            return 'Salvación al final del turno', 'save_end_of_turn'
        return 'Salvación', 'save_pattern'
    if 'regains' in desc_en or 'regain hit points' in desc_en or ('recupera' in desc_es and 'puntos de golpe' in desc_es):
        return 'Curar', 'heal_pattern'
    if any(x in desc_en for x in ['you conjure', 'you summon', 'appears in an unoccupied space', 'spectral hand appears', 'watchdog', 'hound remains', 'spectral sword']):
        return 'Invocar', 'summon_pattern'
    if spell_name_es.lower().startswith('crear '):
        return spell_name_es, 'spell_name_create'
    if spell_name_es.lower().startswith('animar a los muertos'):
        return 'Animar cadáveres', 'specific_animate_dead'
    if spell_name_es.lower().startswith('muro de '):
        return spell_name_es, 'spell_name_wall'

    return 'Lanzar', 'default'

out = copy.deepcopy(es)
report = {
    '_meta': {
        'method': 'best_effort_backfill_from_validated_v3_examples_plus_conservative_name_inference',
        'note': 'Only exact structured fields confirmed in reviewed V3 snippets were backfilled. Activity names were completed conservatively from validated V3 patterns, project translation memory, and spell descriptions.'
    },
    'counts': Counter(),
    'examples': defaultdict(list)
}

for eid, es_entry in out.get('entries', {}).items():
    en_entry = en_old.get('entries', {}).get(eid, {})
    for aid, es_act in es_entry.get('activities', {}).items():
        en_act = en_entry.get('activities', {}).get(aid, {})
        if not s(es_act.get('name')):
            name, source = infer_name(eid, aid, es_entry, es_act, en_entry, en_act)
            es_act['name'] = name
            report['counts']['activities.name'] += 1
            if len(report['examples']['activities.name']) < 25:
                report['examples']['activities.name'].append({'entry': eid, 'activity': aid, 'value': name, 'source': source})

        ov = manual_overrides.get((eid, aid), {})
        for field in ['target', 'range', 'duration']:
            if field in ov and not s(es_act.get(field)):
                es_act[field] = ov[field]
                report['counts'][f'activities.{field}'] += 1
                if len(report['examples'][f'activities.{field}']) < 25:
                    report['examples'][f'activities.{field}'].append({'entry': eid, 'activity': aid, 'value': ov[field], 'source': 'manual_override'})

report['counts'] = dict(report['counts'])
report['examples'] = dict(report['examples'])

with open(os.path.join(base, 'dnd-players-handbook.spells.es.backfilled.from-en-v3.best-effort.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
with open(os.path.join(base, 'spells_backfill_v3_best_effort_report.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(report['counts'])
