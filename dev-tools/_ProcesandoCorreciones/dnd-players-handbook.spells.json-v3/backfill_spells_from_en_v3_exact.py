import json, os, re, copy
from collections import Counter, defaultdict

BASE = os.path.dirname(__file__)
EN_PATH = os.path.join(BASE, "dnd-players-handbook.spells-en.v3.json")
ES_PATH = os.path.join(BASE, "dnd-players-handbook.spells.json")
OUT_JSON = os.path.join(BASE, "dnd-players-handbook.spells.es.backfilled.from-en-v3.exact.json")
OUT_REPORT = os.path.join(BASE, "spells_backfill_v3_exact_report.json")

with open(EN_PATH, "r", encoding="utf-8") as f:
    en = json.load(f)
with open(ES_PATH, "r", encoding="utf-8") as f:
    es = json.load(f)

pair_specs = [
    ("dnd-players-handbook.feats-en.json", "dnd-players-handbook.feats.json", "item"),
    ("dnd-players-handbook.equipment-en.json", "dnd-players-handbook.equipment.json", "item"),
    ("dnd-players-handbook.origins-en.json", "dnd-players-handbook.origins.json", "item"),
    ("dnd-players-handbook.classes-en-v3.json", "dnd-players-handbook.classes.json", "item"),
    ("dnd-players-handbook.spells-en.json", "dnd-players-handbook.spells.json", "item"),
    ("dnd-players-handbook.actors-en.json", "dnd-players-handbook.actors.json", "actor"),
]
mem = defaultdict(lambda: defaultdict(Counter))
for enfile, esfile, kind in pair_specs:
    p1 = os.path.join(BASE, enfile)
    p2 = os.path.join(BASE, esfile)
    if not (os.path.exists(p1) and os.path.exists(p2)):
        continue
    with open(p1, encoding="utf-8") as f:
        e = json.load(f)
    with open(p2, encoding="utf-8") as f:
        s = json.load(f)
    if kind == "item":
        for eid, en_entry in e.get("entries", {}).items():
            es_entry = s.get("entries", {}).get(eid)
            if not es_entry:
                continue
            for aid, en_act in (en_entry.get("activities") or {}).items():
                es_act = (es_entry.get("activities") or {}).get(aid)
                if not es_act:
                    continue
                for field in ["name", "target", "range", "duration"]:
                    en_v = en_act.get(field)
                    es_v = es_act.get(field)
                    if isinstance(en_v, str) and en_v and isinstance(es_v, str) and es_v:
                        mem[f"activities.{field}"][en_v][es_v] += 1
                en_v = ((en_act.get("activation") or {}).get("condition"))
                es_v = ((es_act.get("activation") or {}).get("condition"))
                if isinstance(en_v, str) and en_v and isinstance(es_v, str) and es_v:
                    mem["activities.activation.condition"][en_v][es_v] += 1
    else:
        for eid, en_entry in e.get("entries", {}).items():
            es_entry = s.get("entries", {}).get(eid)
            if not es_entry:
                continue
            for iid, en_item in (en_entry.get("items") or {}).items():
                es_item = (es_entry.get("items") or {}).get(iid)
                if not es_item:
                    continue
                for aid, en_act in (en_item.get("activities") or {}).items():
                    es_act = (es_item.get("activities") or {}).get(aid)
                    if not es_act:
                        continue
                    for field in ["name", "target", "range", "duration", "condition"]:
                        en_v = en_act.get(field)
                        es_v = es_act.get(field)
                        if isinstance(en_v, str) and en_v and isinstance(es_v, str) and es_v:
                            mem[f"activities.{field}"][en_v][es_v] += 1

def is_blank(v):
    return v is None or (isinstance(v, str) and v == "")

name_map = {
    "Use": "Usar",
    "Save": "Salvación",
    "Summon": "Invocar",
    "Attack": "Ataque",
    "Heal": "Curar",
    "Damage": "Daño",
    "Transform": "Transformar",
    "Enchant": "Encantar",
}
for k in list(name_map):
    if mem["activities.name"].get(k):
        name_map[k] = mem["activities.name"][k].most_common(1)[0][0]

target_shape_map = {
    "sphere": "esfera",
    "radius": "radio",
    "cylinder": "cilindro",
    "cube": "cubo",
    "wall": "muro",
    "circle": "círculo",
    "cone": "cono",
    "line": "línea",
    "square": "cuadrado",
}
unit_map_singular = {
    "minute": "minuto",
    "hour": "hora",
    "day": "día",
    "round": "asalto",
    "turn": "turno",
}
unit_map_plural = {
    "minute": "minutos",
    "hour": "horas",
    "day": "días",
    "round": "asaltos",
    "turn": "turnos",
}

condition_map = {
    "only at night": "solo por la noche",
    "immediately after hitting a creature with a Melee weapon or an Unarmed Strike": "inmediatamente después de impactar a una criatura con un arma cuerpo a cuerpo o un Golpe sin armas",
    "when you see a creature within range casting a spell with Verbal, Somatic, or Material components": "cuando veas a una criatura dentro del alcance lanzar un conjuro con componentes verbales, somáticos o materiales",
    "immediately after hitting or missing a target with a ranged attack using a weapon": "inmediatamente después de impactar o fallar a un objetivo con un ataque a distancia con un arma",
    "Immediately after hitting a target with a Melee weapon or an Unarmed Strike": "Inmediatamente después de impactar a un objetivo con un arma cuerpo a cuerpo o un Golpe sin armas",
    "Immediately after hitting a creature with a weapon": "Inmediatamente después de impactar a una criatura con un arma",
    "when you or a creature you can see within 60 feet of you falls": "cuando tú o una criatura que puedas ver a 60 pies o menos de ti caigáis",
    "immediately after hitting a creature with a Ranged weapon": "inmediatamente después de impactar a una criatura con un arma a distancia",
    "taking damage from a creature that you can see within 60 feet of yourself": "al recibir daño de una criatura que puedas ver a 60 pies o menos de ti",
    "immediately after hitting a target with a Melee weapon or an Unarmed Strike": "inmediatamente después de impactar a un objetivo con un arma cuerpo a cuerpo o un Golpe sin armas",
    "when you are hit by an attack roll or targeted by the Magic Missile spell": "cuando una tirada de ataque te impacte o seas objetivo del conjuro Proyectil mágico",
    "a bit of fleece": "un poco de vellón",
}

def translate_range(v: str) -> str:
    if mem["activities.range"].get(v):
        best = mem["activities.range"][v].most_common(1)[0][0]
        if re.fullmatch(r"\d+\s*ft", v) and re.fullmatch(r"\d+\s+pies", best):
            return best
    m = re.fullmatch(r"(\d+)\s*ft", v)
    if m:
        return f"{m.group(1)} pies"
    m = re.fullmatch(r"(\d+)\s*mi", v)
    if m:
        n = int(m.group(1))
        return f"{n} milla" if n == 1 else f"{n} millas"
    return v

def translate_duration(v: str) -> str:
    if mem["activities.duration"].get(v):
        best = mem["activities.duration"][v].most_common(1)[0][0]
        if re.fullmatch(r"\d+\s+\w+", v):
            return best
    m = re.fullmatch(r"(\d+)\s+([A-Za-z]+)", v)
    if m:
        n = int(m.group(1))
        unit = m.group(2).lower()
        if unit in unit_map_singular:
            return f"{n} {unit_map_singular[unit] if n == 1 else unit_map_plural[unit]}"
    return v

def translate_target(v: str) -> str:
    if mem["activities.target"].get(v):
        best = mem["activities.target"][v].most_common(1)[0][0]
        if re.fullmatch(r"\d+\s+[A-Za-z]+", v):
            if re.search(r"(esfera|radio|cilindro|cubo|muro|círculo|cono|línea|cuadrado)", best):
                return best
    m = re.fullmatch(r"(\d+)\s+([A-Za-z]+)", v)
    if m:
        n = m.group(1)
        shape = m.group(2).lower()
        es_shape = target_shape_map.get(shape)
        if es_shape:
            return f"{es_shape} de {n}"
    return v

def translate_condition(v: str) -> str:
    if v in condition_map:
        return condition_map[v]
    if mem["activities.activation.condition"].get(v):
        return mem["activities.activation.condition"][v].most_common(1)[0][0]
    out = v
    replacements = [
        ("Melee weapon", "arma cuerpo a cuerpo"),
        ("Ranged weapon", "arma a distancia"),
        ("Unarmed Strike", "Golpe sin armas"),
        ("Magic Missile", "Proyectil mágico"),
        ("Verbal, Somatic, or Material components", "componentes verbales, somáticos o materiales"),
        ("within range", "dentro del alcance"),
        ("60 feet", "60 pies"),
        ("30 feet", "30 pies"),
        ("target", "objetivo"),
        ("creature", "criatura"),
    ]
    for a, b in replacements:
        out = out.replace(a, b)
    return out

patched = copy.deepcopy(es)
report = {
    "source_en": "dnd-players-handbook.spells-en.v3.json",
    "source_es": "dnd-players-handbook.spells.json",
    "output": "dnd-players-handbook.spells.es.backfilled.from-en-v3.exact.json",
    "patched_counts": Counter(),
    "examples": defaultdict(list),
}
for eid, en_entry in en["entries"].items():
    es_entry = patched["entries"].get(eid)
    if not es_entry:
        continue
    en_acts = en_entry.get("activities") or {}
    es_acts = es_entry.setdefault("activities", {})
    for aid, en_act in en_acts.items():
        es_act = es_acts.setdefault(aid, {})
        if not is_blank(en_act.get("name")) and is_blank(es_act.get("name")):
            tr = name_map.get(en_act["name"], en_act["name"])
            es_act["name"] = tr
            report["patched_counts"]["activities.name"] += 1
        if not is_blank(en_act.get("target")) and is_blank(es_act.get("target")):
            tr = translate_target(en_act["target"])
            es_act["target"] = tr
            report["patched_counts"]["activities.target"] += 1
        if not is_blank(en_act.get("range")) and is_blank(es_act.get("range")):
            tr = translate_range(en_act["range"])
            es_act["range"] = tr
            report["patched_counts"]["activities.range"] += 1
        if not is_blank(en_act.get("duration")) and is_blank(es_act.get("duration")):
            tr = translate_duration(en_act["duration"])
            es_act["duration"] = tr
            report["patched_counts"]["activities.duration"] += 1
        en_cond = ((en_act.get("activation") or {}).get("condition"))
        es_activation = es_act.setdefault("activation", {}) if isinstance(es_act.get("activation"), dict) else {}
        if not is_blank(en_cond) and is_blank(es_activation.get("condition")):
            tr = translate_condition(en_cond)
            es_activation["condition"] = tr
            es_act["activation"] = es_activation
            report["patched_counts"]["activities.activation.condition"] += 1

remaining = Counter()
for eid, en_entry in en["entries"].items():
    es_entry = patched["entries"][eid]
    for aid, en_act in (en_entry.get("activities") or {}).items():
        es_act = (es_entry.get("activities") or {}).get(aid, {})
        for field in ["name", "target", "range", "duration"]:
            if not is_blank(en_act.get(field)) and is_blank(es_act.get(field)):
                remaining[f"activities.{field}"] += 1
        en_cond = ((en_act.get("activation") or {}).get("condition"))
        es_cond = ((es_act.get("activation") or {}).get("condition"))
        if not is_blank(en_cond) and is_blank(es_cond):
            remaining["activities.activation.condition"] += 1

report["patched_counts"] = dict(report["patched_counts"])
report["remaining_missing_vs_en_v3"] = dict(remaining)
report["name_map_used"] = name_map
report["condition_map_used"] = condition_map

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(patched, f, ensure_ascii=False, indent=2)
with open(OUT_REPORT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("OK", OUT_JSON, OUT_REPORT)