#!/usr/bin/env python3
"""Normalize curated partial-English labels missed by language-level checks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPENDIUM = ROOT / "compendium"


def load(pack: str) -> tuple[Path, dict]:
    path = COMPENDIUM / f"dnd-players-handbook.{pack}.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace(value: str, mapping: dict[str, str]) -> tuple[str, int]:
    changes = 0
    for source, target in mapping.items():
        if source in value:
            value = value.replace(source, target)
            changes += 1
    return value, changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    classes_path, classes = load("classes")
    content_path, content = load("content")
    spells_path, spells = load("spells")
    changes = 0

    animal_names = {
        "Bat": "Murciélago",
        "Cat": "Gato",
        "Frog": "Rana",
        "Hawk": "Halcón",
        "Lizard": "Lagarto",
        "Octopus": "Pulpo",
        "Owl": "Búho",
        "Rat": "Rata",
        "Raven": "Cuervo",
        "Spider": "Araña",
        "Weasel": "Comadreja",
    }
    familiar = spells["entries"]["phbsplFindFamili"]
    for source, target in animal_names.items():
        familiar["description"], count = replace(
            familiar["description"], {f"<strong>{source}</strong>": f"<strong>{target}</strong>"}
        )
        changes += count

    captions = {
        "Aberrant Spirit": "Espíritu aberrante",
        "Bestial Spirit": "Espíritu bestial",
        "Celestial Spirit": "Espíritu celestial",
        "Construct Spirit": "Espíritu constructo",
        "Draconic Spirit": "Espíritu dracónico",
        "Elemental Spirit": "Espíritu elemental",
        "Fey Spirit": "Espíritu feérico",
        "Fiendish Spirit": "Espíritu infernal",
        "Undead Spirit": "Espíritu no muerto",
    }
    for entry_id in (
        "phbsplSummonAber", "phbsplSummonBeas", "phbsplSummonCele",
        "phbsplSummonCons", "phbsplSummonDrag", "phbsplSummonElem",
        "phbsplSummonFey0", "phbsplSummonFien", "phbsplSummonUnde",
    ):
        entry = spells["entries"][entry_id]
        entry["description"], count = replace(
            entry["description"],
            {f"<caption>{source}</caption>": f"<caption>{target}</caption>" for source, target in captions.items()},
        )
        changes += count
        normalized = re.sub(r"(\d+) ft\.", r"\1 pies", entry["description"])
        if normalized != entry["description"]:
            entry["description"] = normalized
            changes += 1

    for entry_id in ("phbmnkDiscipline", "phbmnkMonksFocus", "phbmnkElementalA", "phbmnkShadowArts"):
        entry = classes["entries"][entry_id]
        entry["description"], count = replace(entry["description"], {"Focus Point": "Punto de enfoque"})
        changes += count
    elemental = classes["entries"]["phbmnkElementalA"]
    elemental["description"], count = replace(
        elemental["description"], {"End Attunement": "Finalizar sintonización"}
    )
    changes += count
    changes_map = elemental["effects"]["nYxy4BAjf1emFqtQ"]["changes"]
    if changes_map.get("activities[enchant].name") != "Finalizar sintonización":
        changes_map["activities[enchant].name"] = "Finalizar sintonización"
        changes += 1

    short_rest = content["entries"]["phbAppendixCRule"]["pages"]["wVuNbEADtC16ejAi"]
    short_rest["text"], count = replace(short_rest["text"], {"descanso corto (Short Rest)": "descanso corto"})
    changes += count

    class_labels = {
        "Regain Spell Slot": "Recuperar espacio de conjuro",
        "Regain Puntos de Hechicería": "Recuperar Puntos de Hechicería",
        "Reroll Saving Throw": "Repetir tirada de salvación",
        "Restore Use": "Recuperar uso",
        "Restore with Spell Slot": "Recuperar con espacio de conjuro",
        "Recharge with Spell Slot": "Recargar con espacio de conjuro",
        "Expend Spell Slot for Ward": "Gastar espacio de conjuro para la guarda",
        "Strength saving throw.": "Tirada de salvación de Fuerza.",
        "Charisma saving throw": "Tirada de salvación de Carisma",
    }
    for entry in classes["entries"].values():
        if "description" not in entry:
            continue
        entry["description"], count = replace(entry["description"], class_labels)
        changes += count

    glossary_replacements = {
        "dados de Puntos de Golpe (Hit Point Dice o Hit Dice)": "Dados de Puntos de Golpe",
        "tirada de salvación (Saving Throw)": "tirada de salvación",
        "puntos de golpe temporales (Temporary Hit Points)": "Puntos de Golpe temporales",
        "tirada de salvación contra la muerte (Death Saving Throw o salvación contra la muerte)":
            "tirada de salvación contra la muerte",
        "<p>Cantrip</p>": "<p>Truco</p>",
    }
    for entry in content["entries"].values():
        for page in entry.get("pages", {}).values():
            if "text" not in page:
                continue
            page["text"], count = replace(page["text"], glossary_replacements)
            changes += count

    table_replacements = {
        "<caption>Influence Checks</caption>": "<caption>Pruebas de Influencia</caption>",
        "<p>Ability Check</p>": "<p>Prueba de característica</p>",
        "<p>Interaction</p>": "<p>Interacción</p>",
        "Deceiving a monster that understands you": "Engañar a un monstruo que te entiende",
        "Intimidating a monster": "Intimidar a un monstruo",
        "Amusing a monster": "Entretener a un monstruo",
        "Persuading a monster that understands you": "Persuadir a un monstruo que te entiende",
        "Gently coaxing a Beast or Monstrosity": "Tratar con amabilidad a una Bestia o Monstruosidad",
        "<caption>Food Needs per Day</caption>": "<caption>Necesidades de comida por día</caption>",
        "<caption>Water Needs per Day</caption>": "<caption>Necesidades de agua por día</caption>",
        "<caption>Carrying Capacity</caption>": "<caption>Capacidad de carga</caption>",
        "<caption>Pergamino de conjuro Costs</caption>": "<caption>Costes de Pergamino de conjuro</caption>",
        "<p>Creature Size</p>": "<p>Tamaño de la criatura</p>",
        "<p>Size</p>": "<p>Tamaño</p>",
        "<p>Food</p>": "<p>Comida</p>",
        "<p>Water</p>": "<p>Agua</p>",
        "<p>Carry</p>": "<p>Transportar</p>",
        "<p>Drag/Lift/Push</p>": "<p>Arrastrar/levantar/empujar</p>",
        "Tiny": "Diminuto",
        "Small": "Pequeño",
        "Medium": "Mediano",
        "Large": "Grande",
        "Huge": "Enorme",
        "Gargantuan": "Gargantuesco",
        "Strength x": "Fuerza ×",
        "pounds": "libras",
        "pound": "libra",
        "gallons": "galones",
        "gallon": "galón",
        "lb.": "lb",
    }
    appendix = content["entries"]["phbAppendixCRule"]["pages"]
    for page_id in ("4V59Q1dlWjNhpJGo", "earBo4vQPC1ti4g7", "FZFvLNOX0lHaHZ1k", "xk9KqsS54w8EpbZn"):
        appendix[page_id]["text"], count = replace(appendix[page_id]["text"], table_replacements)
        changes += count
    crafting = content["entries"]["phbCraftingEquip"]["pages"]["8hAsl8JueZ3GvyS2"]
    crafting["text"], count = replace(crafting["text"], table_replacements)
    changes += count

    for entry_id in ("phbsplAuraofLife", "phbsplRegenerate"):
        entry = spells["entries"][entry_id]
        entry["description"], count = replace(entry["description"], {"1 Hit Point": "1 Punto de Golpe"})
        changes += count
        for effect in entry.get("effects", {}).values():
            effect["description"], count = replace(
                effect.get("description", ""), {"1 Hit Point": "1 Punto de Golpe"}
            )
            changes += count

    print(f"Residual labels updated: {changes}")
    if args.write and changes:
        save(classes_path, classes)
        save(content_path, content)
        save(spells_path, spells)


if __name__ == "__main__":
    main()
