#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
python_count_entry_countkey.py

Lee un JSON con estructura tipo Babele/Foundry que contenga una clave raíz
"entries", cuenta cuántos elementos hay dentro de estas keys de cada entry:

- activities
- effects
- advancement
- items
- pages
- results

Después:

1. Sustituye cada una de esas keys por su número de elementos
   (solo si la key existía en el entry original).
2. Añade una nueva key "countkey" con la suma total.
3. Ordena todos los elementos de "entries" de forma descendente por "countkey".
4. Guarda el resultado en un nuevo JSON normalizado.

Uso
===

1) Indicando fichero de salida:
   py python_count_entry_countkey.py input.json -o salida.json

   Ejemplos:
   py python_count_entry_countkey.py dnd-players-handbook.origins-en.json -o dnd-players-handbook.origins-countkey.json
   py python_count_entry_countkey.py dnd-players-handbook.classes-en.json -o out.json

2) Sin indicar -o:
   py python_count_entry_countkey.py input.json

   En este caso se genera automáticamente un archivo en la misma ruta
   que el fichero de entrada, añadiendo "_countkey" al nombre:

   input.json -> input_countkey.json

   Ejemplos:
   py python_count_entry_countkey.py dnd-players-handbook.origins-en.json
   -> dnd-players-handbook.origins-en_countkey.json

   py python_count_entry_countkey.py dnd-players-handbook.classes-en.json
   -> dnd-players-handbook.classes-en_countkey.json

Comportamiento
==============

Para cada entry:
- Si una key de conteo no existe, cuenta como 0 para la suma.
- Si existe y es dict o list, usa len(...)
- Si existe pero no es dict/list, cuenta como 0
- "countkey" = suma de todas las keys configuradas en COUNT_KEYS

Ordenación
==========

Los entries se ordenan así:
- Primero por "countkey" descendente
- En caso de empate, por entry_id ascendente

Errores
=======

- Si el fichero de entrada no existe, el script termina con error.
- Si el JSON no contiene una clave raíz "entries" de tipo objeto/dict,
  el script termina con error.
"""

import json
import argparse
from collections import OrderedDict
from pathlib import Path

COUNT_KEYS = ["activities", "effects", "advancement", "items", "pages", "results"]


def safe_len(value):
    """
    Devuelve el número de elementos de un dict/list.
    Si no existe o no es contenedor, devuelve 0.
    """
    if isinstance(value, (dict, list)):
        return len(value)
    return 0


def build_default_output_path(in_path: Path) -> Path:
    """
    Genera la ruta de salida por defecto en la misma carpeta del fichero
    de entrada, añadiendo '_countkey' antes de la extensión.

    Ejemplo:
      dnd-players-handbook.origins-en.json
      -> dnd-players-handbook.origins-en_countkey.json
    """
    return in_path.with_name(f"{in_path.stem}_countkey{in_path.suffix}")


def transform_entries(data):
    entries = data.get("entries", {})
    transformed_entries = []

    for entry_key, entry_value in entries.items():
        if not isinstance(entry_value, dict):
            new_entry = OrderedDict()
            new_entry["countkey"] = 0
            transformed_entries.append((entry_key, new_entry))
            continue

        new_entry = OrderedDict()
        total = 0

        # Copiar primero todas las keys que NO sean las de conteo
        for k, v in entry_value.items():
            if k not in COUNT_KEYS:
                new_entry[k] = v

        # Calcular conteos y suma total
        key_counts = {}
        for ck in COUNT_KEYS:
            count = safe_len(entry_value.get(ck))
            key_counts[ck] = count
            total += count

        # Añadir countkey
        new_entry["countkey"] = total

        # Añadir cada key de conteo con su número solo si existía en el original
        for ck in COUNT_KEYS:
            if ck in entry_value:
                new_entry[ck] = key_counts[ck]

        transformed_entries.append((entry_key, new_entry))

    # Orden descendente por countkey; en empate, entry_id ascendente
    transformed_entries.sort(key=lambda x: (-x[1].get("countkey", 0), x[0]))

    data["entries"] = OrderedDict(transformed_entries)
    return data


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Cuenta activities/effects/advancement/items/pages/results en entries, "
            "añade countkey y ordena entries desc."
        )
    )
    parser.add_argument("input_json", help="Ruta del JSON de entrada")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help=(
            "Ruta del JSON de salida. "
            "Si no se indica, se genera en la misma ruta del input "
            "con sufijo '_countkey'."
        ),
    )
    args = parser.parse_args()

    input_path = Path(args.input_json)
    if not input_path.exists():
        raise SystemExit(f"ERROR: No existe el fichero: {input_path}")

    output_path = Path(args.output) if args.output else build_default_output_path(input_path)

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries")
    if not isinstance(entries, dict):
        raise SystemExit("ERROR: El JSON no tiene un objeto 'entries' (o no es dict).")

    result = transform_entries(data)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Archivo generado: {output_path}")


if __name__ == "__main__":
    main()