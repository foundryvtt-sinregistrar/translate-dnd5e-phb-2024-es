#!/usr/bin/env python3
"""Repair embedded translations by reusing canonical translated entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPENDIUM = ROOT / "compendium"


def load(pack: str) -> tuple[Path, dict]:
    path = COMPENDIUM / f"dnd-players-handbook.{pack}.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_advancement(target: dict, source: dict) -> int:
    changes = 0
    for advancement_id, target_row in target.get("advancement", {}).items():
        source_row = source.get("advancement", {}).get(advancement_id, {})
        for field in ("title", "hint"):
            if field in source_row and target_row.get(field) != source_row[field]:
                target_row[field] = source_row[field]
                changes += 1
    return changes


def sync_item(target: dict, source: dict) -> int:
    changes = sync_advancement(target, source)
    for field in ("name", "description"):
        if field in source and target.get(field) != source[field]:
            target[field] = source[field]
            changes += 1
    return changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    actors_path, actors = load("actors")
    classes_path, classes = load("classes")
    _, origins = load("origins")
    changes = 0

    links = [
        ("phbprgWarlock000", "59ehZ8UPSlKtZyhr", classes["entries"]["phbwlkWarlock000"]),
        ("phbprgWizard0000", "TFT8UNrGYn8Ythyd", origins["entries"]["phbspAasimar0000"]),
        ("phbprgRogue00000", "AhwkVFcqeRPgX61K", origins["entries"]["phbbgCriminal000"]),
        ("phbprgSorcerer00", "LGWHP5FKV4LckYqx", origins["entries"]["phbbgCharlatan00"]),
        ("phbprgWarlock000", "9KBKviUbm9kRtBFb", origins["entries"]["phbbgAcolyte0000"]),
        ("phbprgWizard0000", "lO0Yo3nkf503lr7P", origins["entries"]["phbbgScribe00000"]),
    ]
    for actor_id, item_id, source in links:
        target = actors["entries"][actor_id]["items"][item_id]
        changes += sync_item(target, source)

    pack_damage = actors["entries"]["phbSpectralAnima"]["items"]["phbcftPackDamage"]
    translated_pack_damage = (
        "<p>Siempre que la manada se mueva a 10 pies o menos de una criatura que puedas ver "
        "y siempre que una criatura que puedas ver entre en un espacio a 10 pies o menos de "
        "la manada o termine su turno allí, puedes obligar a esa criatura a realizar una "
        "tirada de salvación de Destreza. En una salvación fallida, la criatura recibe 3d10 "
        "de daño cortante. Una criatura realiza esta tirada de salvación solo una vez por turno.</p>"
    )
    if pack_damage["description"] != translated_pack_damage:
        pack_damage["description"] = translated_pack_damage
        changes += 1

    elemental = actors["entries"]["phbsplConjuredEl"]["items"]["1sm4KQqflaDX7MEu"]
    translated_condition = (
        "una criatura que puedas ver entra en el espacio del espíritu o empieza su turno "
        "a 5 pies o menos de él"
    )
    for activity in elemental.get("activities", {}).values():
        if activity.get("condition") != translated_condition:
            activity["condition"] = translated_condition
            changes += 1

    repelling = classes["entries"]["phbinvRepellingB"]
    activity = repelling["activities"]["OXhI1TDQxORrGAgc"]
    if activity["name"] != "Aplicar Explosión repelente":
        activity["name"] = "Aplicar Explosión repelente"
        changes += 1
    effect = repelling["effects"]["DShZGDAUy0w9RUzS"]
    translated_effect = (
        "<p>Elige uno de tus trucos de brujo conocidos que requiera una tirada de ataque. "
        "Cuando impactas a una criatura Grande o más pequeña con ese truco, puedes empujar "
        "a la criatura hasta 10 pies directamente alejándola de ti.</p>"
    )
    if effect["description"] != translated_effect:
        effect["description"] = translated_effect
        changes += 1
    note = repelling["description"]
    updated_note = note.replace("Make Repelling", "Aplicar Explosión repelente").replace(
        '", Repelling"', '", repelente"'
    )
    if note != updated_note:
        repelling["description"] = updated_note
        changes += 1

    print(f"Embedded fields updated: {changes}")
    if args.write and changes:
        save(actors_path, actors)
        save(classes_path, classes)


if __name__ == "__main__":
    main()
