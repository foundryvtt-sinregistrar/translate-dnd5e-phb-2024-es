#!/usr/bin/env python3
"""Restore malformed Reference macros from the aligned English source files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
COMPENDIUM = ROOT / "compendium"
ENGLISH = ROOT / "dev-tools" / "export" / "data"
TERMS = json.loads(Path(__file__).with_name("official-terms.es.json").read_text(encoding="utf-8"))
REFERENCE = re.compile(r"&(?:amp;)?Reference(?:\[[^\]]*\](?:\{[^}]*\})?)?")
VALID_REFERENCE = re.compile(r"&(?:amp;)?Reference\[(?P<key>[^\]]*)\](?:\{[^}]*\})?")

LABELS = {
    **TERMS["conditions"],
    **TERMS["actions"],
    "Advantage": "Ventaja",
    "Burning": "Ardiendo",
    "Cover": "Cobertura",
    "Dehydration": "Deshidratación",
    "DifficultTerrain": "Terreno difícil",
    "Disadvantage": "Desventaja",
    "Falling": "Caída",
    "Malnutrition": "Malnutrición",
    "OpportunityAttack": "Ataque de oportunidad",
    "Speed": "Velocidad",
    "Suffocation": "Asfixia",
}
MISMATCHES: list[str] = []
OVERRIDES = {
    "content.entries.phbSpeciesDescri.pages.4zCNgk0JSKVzv9Y9.text": ["Poisoned"],
}


def source_path(pack: str) -> Path:
    return ENGLISH / f"dnd-players-handbook.{pack}" / "en" / f"dnd-players-handbook.{pack}-en.json"


def repair_string(spanish: str, english: str, location: str) -> tuple[str, int]:
    spanish_tokens = list(REFERENCE.finditer(spanish))
    if not any("[" not in match.group(0) for match in spanish_tokens):
        return spanish, 0
    english_tokens = list(VALID_REFERENCE.finditer(english))
    if len(spanish_tokens) != len(english_tokens):
        override_keys = list(OVERRIDES.get(location, []))
        if override_keys and len(override_keys) == sum("[" not in row.group(0) for row in spanish_tokens):
            output = []
            cursor = 0
            changes = 0
            for match in spanish_tokens:
                output.append(spanish[cursor : match.start()])
                token = match.group(0)
                if "[" not in token:
                    key = override_keys.pop(0)
                    label = LABELS.get(key)
                    token = f"&amp;Reference[{key}]" + (f"{{{label}}}" if label else "")
                    changes += 1
                output.append(token)
                cursor = match.end()
            output.append(spanish[cursor:])
            return "".join(output), changes
        MISMATCHES.append(
            f"{location}: ES={len(spanish_tokens)}, EN={len(english_tokens)}"
        )
        return spanish, 0
    output = []
    cursor = 0
    changes = 0
    for spanish_match, english_match in zip(spanish_tokens, english_tokens):
        output.append(spanish[cursor : spanish_match.start()])
        token = spanish_match.group(0)
        if "[" not in token:
            key = english_match.group("key")
            base_key = key.split()[0]
            label = LABELS.get(base_key)
            token = f"&amp;Reference[{key}]" + (f"{{{label}}}" if label else "")
            changes += 1
        output.append(token)
        cursor = spanish_match.end()
    output.append(spanish[cursor:])
    return "".join(output), changes


def repair_value(spanish: Any, english: Any, location: str) -> tuple[Any, int]:
    if isinstance(spanish, dict) and isinstance(english, dict):
        changes = 0
        result = dict(spanish)
        for key in spanish.keys() & english.keys():
            result[key], count = repair_value(spanish[key], english[key], f"{location}.{key}")
            changes += count
        return result, changes
    if isinstance(spanish, list) and isinstance(english, list):
        changes = 0
        result = list(spanish)
        for index, (spanish_row, english_row) in enumerate(zip(spanish, english)):
            result[index], count = repair_value(spanish_row, english_row, f"{location}[{index}]")
            changes += count
        return result, changes
    if isinstance(spanish, str) and isinstance(english, str):
        return repair_string(spanish, english, location)
    return spanish, 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    total = 0
    for path in sorted(COMPENDIUM.glob("dnd-players-handbook.*.json")):
        pack = path.stem.rsplit(".", 1)[-1]
        spanish = json.loads(path.read_text(encoding="utf-8"))
        english = json.loads(source_path(pack).read_text(encoding="utf-8"))
        repaired, changes = repair_value(spanish, english, pack)
        total += changes
        print(f"{pack}: {changes} restored Reference macros")
        if args.write and changes:
            path.write_text(json.dumps(repaired, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Total: {total} restored Reference macros")
    if MISMATCHES:
        print("Skipped ambiguous fields:")
        for mismatch in MISMATCHES:
            print(f"- {mismatch}")


if __name__ == "__main__":
    main()
