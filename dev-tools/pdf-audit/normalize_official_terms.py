#!/usr/bin/env python3
"""Normalize high-confidence visible terminology without changing macro keys."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
COMPENDIUM = ROOT / "compendium"
TERMS_FILE = Path(__file__).with_name("official-terms.es.json")
PROTECTED = re.compile(
    r"(?P<prefix>@(?:UUID|Embed|Check|Damage|Template|Prompt)|&(?:amp;)?(?:Reference|Trait|Activity))"
    r"(?P<key>\[[^\]]*\])(?P<label>\{[^}]*\})?"
    r"|(?P<roll>\[\[/[^\]]*\]\])"
    r"|(?P<tag><[^>]+>)"
)


def replacements() -> dict[str, str]:
    terms = json.loads(TERMS_FILE.read_text(encoding="utf-8"))
    mapping = {
        **terms["conditions"],
        **terms["actions"],
        **terms["other"],
        **terms["deprecatedSpanish"],
    }
    return mapping


def normalize_plain(text: str, mapping: dict[str, str]) -> str:
    # Remove bilingual annotations before applying individual replacements.
    aliases = {**mapping, **{target: target for target in mapping.values()}}
    for outer, target in aliases.items():
        for inner, inner_target in aliases.items():
            if target != inner_target or outer == inner:
                continue
            text = re.sub(
                rf"\b{re.escape(outer)}\s*\(\s*{re.escape(inner)}\s*\)",
                target,
                text,
                flags=re.IGNORECASE,
            )
    for source in sorted(mapping, key=len, reverse=True):
        target = mapping[source]
        if source == target:
            continue
        text = re.sub(rf"\b{re.escape(source)}\b", target, text, flags=re.IGNORECASE)
    return text


def normalize_text(text: str, mapping: dict[str, str]) -> str:
    output = []
    cursor = 0
    for match in PROTECTED.finditer(text):
        output.append(normalize_plain(text[cursor : match.start()], mapping))
        if match.group("roll") or match.group("tag"):
            output.append(match.group(0))
        else:
            label = match.group("label")
            if label:
                label = "{" + normalize_plain(label[1:-1], mapping) + "}"
            output.append(match.group("prefix") + match.group("key") + (label or ""))
        cursor = match.end()
    output.append(normalize_plain(text[cursor:], mapping))
    return "".join(output)


def normalize_value(
    value: Any, mapping: dict[str, str], path: tuple[str, ...] = ()
) -> tuple[Any, int]:
    if isinstance(value, dict):
        changed = 0
        result = {}
        for key, child in value.items():
            result[key], count = normalize_value(child, mapping, (*path, key))
            changed += count
        return result, changed
    if isinstance(value, list):
        changed = 0
        result = []
        for index, child in enumerate(value):
            normalized, count = normalize_value(child, mapping, (*path, str(index)))
            result.append(normalized)
            changed += count
        return result, changed
    if isinstance(value, str):
        if path and path[-1] in {"folder", "src"}:
            return value, 0
        if value.startswith(("modules/", "systems/")) or re.search(
            r"\.(?:webp|png|jpe?g|svg)$", value, re.IGNORECASE
        ):
            return value, 0
        normalized = normalize_text(value, mapping)
        return normalized, int(normalized != value)
    return value, 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Update compendium files")
    args = parser.parse_args()
    mapping = replacements()
    total = 0
    for path in sorted(COMPENDIUM.glob("dnd-players-handbook.*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        normalized, changed = normalize_value(data, mapping)
        total += changed
        print(f"{path.name}: {changed} changed strings")
        if args.write and changed:
            path.write_text(
                json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    print(f"Total: {total} changed strings")


if __name__ == "__main__":
    main()
