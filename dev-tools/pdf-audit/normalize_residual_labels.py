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

    print(f"Residual labels updated: {changes}")
    if args.write and changes:
        save(classes_path, classes)
        save(content_path, content)
        save(spells_path, spells)


if __name__ == "__main__":
    main()
