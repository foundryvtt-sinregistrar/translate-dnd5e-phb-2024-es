#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
python_count_entry_countChars.py

Cuenta los caracteres de cada elemento dentro de la clave raíz "entries"
y genera un JSON con esta estructura:

{
  "entryIdConMasCaracteres": 5678,
  "entryIdConMenosCaracteres": 123
}

El conteo se realiza serializando cada entry a JSON compacto:
- ensure_ascii=False   -> cuenta caracteres reales (á, ñ, etc.)
- separators=(",", ":") -> evita espacios extra al contar

Además, el resultado se ordena de forma descendente por número de caracteres.

Uso
===

1) Indicando fichero de salida:
   py python_count_entry_countChars.py input.json -o salida.json

2) Sin indicar -o:
   py python_count_entry_countChars.py input.json

   En este caso se genera automáticamente un archivo en la misma ruta
   que el fichero de entrada, añadiendo "_countChars" al nombre:

   input.json -> input_countChars.json

Ejemplos:
   py python_count_entry_countChars.py dnd5e.actors24-en_sorted.json
   py python_count_entry_countChars.py dnd-players-handbook.actors-en.json -o out_counts.json
"""

import argparse
import json
from pathlib import Path


def count_chars_of_entry(entry_obj) -> int:
    """
    Cuenta los caracteres de un entry serializándolo a JSON compacto.
    """
    s = json.dumps(entry_obj, ensure_ascii=False, separators=(",", ":"))
    return len(s)


def build_default_output_path(in_path: Path) -> Path:
    """
    Genera la ruta de salida por defecto en la misma carpeta del fichero
    de entrada, añadiendo '_countChars' antes de la extensión.
    """
    return in_path.with_name(f"{in_path.stem}_countChars{in_path.suffix}")


def main():
    ap = argparse.ArgumentParser(
        description=(
            "Cuenta caracteres del contenido de cada clave dentro de 'entries' "
            "y ordena el resultado de mayor a menor."
        )
    )
    ap.add_argument("input", help="Ruta del JSON de entrada")
    ap.add_argument(
        "-o",
        "--output",
        default=None,
        help=(
            "Ruta del JSON de salida. "
            "Si no se indica, se genera en la misma ruta del input "
            "con sufijo '_countChars'."
        ),
    )
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise SystemExit(f"ERROR: No existe el fichero: {in_path}")

    out_path = Path(args.output) if args.output else build_default_output_path(in_path)

    with in_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries")
    if not isinstance(entries, dict):
        raise SystemExit("ERROR: El JSON no tiene un objeto 'entries' (o no es dict).")

    result = {}
    for entry_id, entry_obj in entries.items():
        result[entry_id] = count_chars_of_entry(entry_obj)

    # Ordenación DESC por número de caracteres; en empate, entry_id ASC
    sorted_result = dict(sorted(result.items(), key=lambda x: (-x[1], x[0])))

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(sorted_result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"OK: generado {out_path} ({len(sorted_result)} entries)")


if __name__ == "__main__":
    main()