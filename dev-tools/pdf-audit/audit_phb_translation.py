#!/usr/bin/env python3
"""Audit PHB translations against source structure and official terminology.

The PDF files are optional. When pypdf and the local PDF directory are
available, the report also records corpus extraction statistics. No extracted
book text is written to disk.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[2]
COMPENDIUM = ROOT / "compendium"
ENGLISH = ROOT / "dev-tools" / "export" / "data"
PDF_DIR = ROOT / "dev-tools" / "export" / "_data" / "pdf"
TERMS_FILE = Path(__file__).with_name("official-terms.es.json")

PROTECTED = re.compile(
    r"(?:@(?:UUID|Embed|Check|Damage|Template|Prompt)\[[^\]]*\](?:\{[^}]*\})?)"
    r"|(?:&(?:amp;)?(?:Reference|Trait|Activity)\[[^\]]*\](?:\{[^}]*\})?)"
    r"|(?:\[\[/[^\]]*\]\])"
)
PHB_REFERENCE = re.compile(
    r"@(?:UUID|Embed)\[Compendium\.dnd-players-handbook\.([^.\]]+)\."
    r"(?:Item|Actor|JournalEntry|RollTable)\.([^.#\]\s]+)"
)
ENGLISH_MARKERS = {
    "a", "all", "an", "and", "any", "are", "as", "at", "attack", "be", "before",
    "bonus", "by", "can", "check", "choose", "creature", "creatures", "damage", "do",
    "does", "during", "each", "effect", "feature", "for", "from", "gain", "grants",
    "has", "have", "if", "in", "into", "is", "it", "its", "known", "level", "long",
    "make", "no", "not", "of", "on", "or", "rest", "saving", "short", "source",
    "spell", "target", "than", "that", "the", "their", "them", "then", "they", "this",
    "throw", "to", "turn", "until", "use", "using", "was", "were", "when", "whenever",
    "while", "with", "within", "without", "you", "your",
}


def walk(value: Any, path: str = "") -> Iterator[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


def visible_text(value: str) -> str:
    value = PROTECTED.sub(" ", value)
    value = re.sub(r"<[^>]+>", " ", value)
    return html.unescape(value)


def load_packs() -> dict[str, dict[str, Any]]:
    packs = {}
    for path in sorted(COMPENDIUM.glob("dnd-players-handbook.*.json")):
        pack = path.stem.rsplit(".", 1)[-1]
        packs[pack] = json.loads(path.read_text(encoding="utf-8"))
    return packs


def source_path(pack: str) -> Path:
    return ENGLISH / f"dnd-players-handbook.{pack}" / "en" / f"dnd-players-handbook.{pack}-en.json"


def pdf_statistics() -> dict[str, Any]:
    paths = sorted(PDF_DIR.glob("*.pdf"))
    result: dict[str, Any] = {"files": len(paths), "characters": None, "blankFiles": None}
    if not paths:
        return result
    try:
        from pypdf import PdfReader
    except ImportError:
        result["warning"] = "Install pypdf to extract local PDF statistics."
        return result
    characters = 0
    blank = 0
    for path in paths:
        text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        characters += len(text)
        blank += not bool(text.strip())
    result.update(characters=characters, blankFiles=blank)
    return result


def run_audit() -> dict[str, Any]:
    packs = load_packs()
    terms = json.loads(TERMS_FILE.read_text(encoding="utf-8"))
    canonical = {**terms["conditions"], **terms["actions"], **terms["other"]}
    deprecated = terms["deprecatedSpanish"]
    identifiers = {pack: set(data.get("entries", {})) for pack, data in packs.items()}
    structure = {}
    residues = []
    deprecated_hits = []
    probable_english = []
    references = 0
    invalid_references = []

    for pack, data in packs.items():
        source = json.loads(source_path(pack).read_text(encoding="utf-8"))
        es_ids = identifiers[pack]
        en_ids = set(source.get("entries", {}))
        structure[pack] = {
            "englishEntries": len(en_ids),
            "spanishEntries": len(es_ids),
            "missing": sorted(en_ids - es_ids),
            "extra": sorted(es_ids - en_ids),
        }
        for path, value in walk(data):
            for target_pack, entry_id in PHB_REFERENCE.findall(value):
                references += 1
                if target_pack not in identifiers or entry_id not in identifiers[target_pack]:
                    invalid_references.append(
                        {"pack": pack, "path": path, "targetPack": target_pack, "entryId": entry_id}
                    )
            visible = visible_text(value)
            for english, spanish in canonical.items():
                if english.casefold() == spanish.casefold() or path.endswith((".src", ".folder")):
                    continue
                if re.search(rf"\b{re.escape(english)}\b", visible, re.IGNORECASE):
                    residues.append(
                        {"pack": pack, "path": path, "found": english, "expected": spanish}
                    )
            for old, new in deprecated.items():
                if re.search(rf"\b{re.escape(old)}\b", visible, re.IGNORECASE):
                    deprecated_hits.append(
                        {"pack": pack, "path": path, "found": old, "expected": new}
                    )
            if not path.endswith((".src", ".folder")):
                words = re.findall(r"[A-Za-z']+", visible.casefold())
                marker_count = sum(word in ENGLISH_MARKERS for word in words)
                if marker_count >= 4 and marker_count / max(1, len(words)) > 0.18:
                    probable_english.append(
                        {"pack": pack, "path": path, "markers": marker_count, "words": len(words)}
                    )

    return {
        "pdf": pdf_statistics(),
        "structure": structure,
        "references": {"checked": references, "invalid": invalid_references},
        "englishResidues": residues,
        "deprecatedSpanish": deprecated_hits,
        "probableEnglishFields": probable_english,
        "summary": {
            "missingEntries": sum(len(row["missing"]) for row in structure.values()),
            "extraEntries": sum(len(row["extra"]) for row in structure.values()),
            "invalidReferences": len(invalid_references),
            "englishResidues": len(residues),
            "deprecatedSpanish": len(deprecated_hits),
            "probableEnglishFields": len(probable_english),
            "residuesByPack": dict(Counter(row["pack"] for row in residues)),
            "deprecatedByPack": dict(Counter(row["pack"] for row in deprecated_hits)),
        },
    }


def markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# PHB 2024 PDF terminology audit",
        "",
        "## Summary",
        "",
        f"- Missing Spanish entries: {summary['missingEntries']}",
        f"- Extra Spanish entries: {summary['extraEntries']}",
        f"- Invalid internal references: {summary['invalidReferences']}",
        f"- Visible English terminology residues: {summary['englishResidues']}",
        f"- Deprecated Spanish terminology occurrences: {summary['deprecatedSpanish']}",
        f"- Probable untranslated English fields: {summary['probableEnglishFields']}",
        "",
        "## Pack structure",
        "",
        "| Pack | English | Spanish | Missing | Extra |",
        "|---|---:|---:|---:|---:|",
    ]
    for pack, row in report["structure"].items():
        lines.append(
            f"| {pack} | {row['englishEntries']} | {row['spanishEntries']} | "
            f"{len(row['missing'])} | {len(row['extra'])} |"
        )
    lines.extend(["", "## Visible terminology findings", ""])
    for row in report["englishResidues"]:
        lines.append(f"- `{row['pack']}:{row['path']}`: `{row['found']}` -> `{row['expected']}`")
    lines.extend(["", "## Deprecated Spanish terminology", ""])
    for row in report["deprecatedSpanish"]:
        lines.append(f"- `{row['pack']}:{row['path']}`: `{row['found']}` -> `{row['expected']}`")
    lines.extend(["", "## Probable untranslated English fields", ""])
    for row in report["probableEnglishFields"]:
        lines.append(
            f"- `{row['pack']}:{row['path']}`: {row['markers']} English markers in {row['words']} words"
        )
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, help="Write the full JSON report")
    parser.add_argument("--markdown", type=Path, help="Write a readable Markdown report")
    args = parser.parse_args()
    report = run_audit()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
