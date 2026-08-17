# Auditoría global de compendios PHB 2024 ES/EN

Base analizada: archivos `dnd-players-handbook.*.json` y sus equivalentes `-en` actualmente subidos en `/mnt/data`.

## Resumen ejecutivo

- **Bien alineados en estructura**: `classes`, `feats`, `equipment`, `content`.

- **Pendientes estructurales**: `origins`, `spells`, `tables`.

- **Mayor deuda de referencias/labels EN**: `actors`, `origins`, `spells`.

- **Remates menores aún visibles**: `classes`, `equipment`, `content`.


## Estado por compendio

### actors

- Entries: **146**

- UUID labels potencialmente sin traducir: **192**

- Coincidencias de inglés sospechoso: **44**

- Mapping ES: `{"items": {"path": "items", "converter": "phb2024ActorFullById"}}`

- Muestras de labels EN pendientes:

  - `entries.phbprgFighter000.biography` → `Fighter` debería ser `Guerrero`

  - `entries.phbprgFighter000.biography` → `Soldier` debería ser `Soldado`

  - `entries.phbprgFighter000.biography` → `Dwarf` debería ser `Enano`

  - `entries.phbprgFighter000.biography` → `Fighter` debería ser `Guerrero`

  - `entries.phbprgFighter000.items.8jWxAwM0A9lpspWN.description` → `Spear` debería ser `Lanza`

- Tokens EN más repetidos detectados:

  - `Grappled` × 15

  - `Aasimar` × 5

  - `Incapacitated` × 4

  - `Opportunity Attack` × 4

  - `Invisible` × 4

  - `Prone` × 4

  - `Poisoned` × 2

  - `Unconscious` × 2


### classes

- Entries: **522**

- UUID labels potencialmente sin traducir: **9**

- Coincidencias de inglés sospechoso: **31**

- Mapping ES: `{"activities": {"path": "system.activities", "converter": "phb2024ActivitiesById"}, "effects": {"path": "effects", "converter": "phb2024MergeEffects"}, "advancement": {"path": "system.advancement", "converter": "phb2024AdvancementById"}}`

- Muestras de labels EN pendientes:

  - `entries.phbbrdBardicInsp.description` → `Font of Inspiration` debería ser `Fuente de inspiración`

  - `entries.phbDivineStrike0.description` → `Improved Blessed Strikes` debería ser `Golpes Bendecidos Mejorados`

  - `entries.phbdrdWrathOfThe.description` → `Aquatic Affinity` debería ser `Afinidad Acuática`

  - `entries.phbFuryPrimalStr.description` → `Improved Elemental Fury` debería ser `Furia Elemental Mejorada`

  - `entries.phbinvPactTome00.description` → `Book of Shadows` debería ser `Libro de las Sombras`

- Tokens EN más repetidos detectados:

  - `Prone` × 6

  - `Save` × 4

  - `Incapacitated` × 4

  - `Frightened` × 3

  - `Charmed` × 3

  - `Ritual` × 2

  - `Truesight` × 2

  - `Unconscious` × 2


### content

- Entries: **47**

- UUID labels potencialmente sin traducir: **0**

- Coincidencias de inglés sospechoso: **44**

- Mapping ES: `{"pages": {"path": "pages", "converter": "phb2024JournalPagesById"}}`

- Tokens EN más repetidos detectados:

  - `Ritual` × 8

  - `Aasimar` × 7

  - `Invisible` × 5

  - `Prone` × 4

  - `Grappled` × 3

  - `Incapacitated` × 2

  - `Dash` × 2

  - `Restrained` × 2


### equipment

- Entries: **258**

- UUID labels potencialmente sin traducir: **2**

- Coincidencias de inglés sospechoso: **1**

- Mapping ES: `{"activities": {"path": "system.activities", "converter": "phb2024ActivitiesById"}, "effects": {"path": "effects", "converter": "phb2024MergeEffects"}, "advancement": {"path": "system.advancement", "converter": "phb2024AdvancementById"}}`

- Muestras de labels EN pendientes:

  - `entries.phbtulCarpenters.description` → `Barrel` debería ser `Barril`

  - `entries.phbtulCarpenters.description` → `Ladder` debería ser `Escalera`

- Tokens EN más repetidos detectados:

  - `Three-Dragon Ante` × 1


### feats

- Entries: **77**

- UUID labels potencialmente sin traducir: **0**

- Coincidencias de inglés sospechoso: **14**

- Mapping ES: `{"activities": {"path": "system.activities", "converter": "phb2024ActivitiesById"}, "effects": {"path": "effects", "converter": "phb2024MergeEffects"}, "advancement": {"path": "system.advancement", "converter": "phb2024AdvancementById"}}`

- Tokens EN más repetidos detectados:

  - `Poisoned` × 4

  - `Grappled` × 3

  - `Incapacitated` × 2

  - `Prone` × 2

  - `Invisible` × 1

  - `Dash` × 1

  - `Ritual` × 1


### origins

- Entries: **79**

- UUID labels potencialmente sin traducir: **128**

- Coincidencias de inglés sospechoso: **22**

- Mapping ES: `{"activities": {"path": "system.activities", "converter": "activities"}, "effects": {"path": "effects", "converter": "phb2024MergeEffects"}, "advancement": {"path": "system.advancement", "converter": "phb2024AdvancementById"}}`

- Muestras de labels EN pendientes:

  - `entries.phbbgAcolyte0000.description` → `Magic Initiate` debería ser `Iniciado en la magia`

  - `entries.phbbgAcolyte0000.description` → `Book` debería ser `Libro`

  - `entries.phbbgAcolyte0000.description` → `Parchment` debería ser `Pergamino`

  - `entries.phbbgAcolyte0000.description` → `Robe` debería ser `Toga o hábito`

  - `entries.phbbgArtisan0000.description` → `Crafter` debería ser `Artesano`

- Tokens EN más repetidos detectados:

  - `Aasimar` × 6

  - `Tiefling` × 5

  - `Charmed` × 4

  - `Frightened` × 3

  - `Grappled` × 2

  - `Prone` × 2


### spells

- Entries: **392**

- UUID labels potencialmente sin traducir: **32**

- Coincidencias de inglés sospechoso: **164**

- Mapping ES: `{"activities": {"path": "system.activities", "converter": "activities"}, "effects": {"path": "effects", "converter": "phb2024MergeEffects"}, "advancement": {"path": "system.advancement", "converter": "phb2024AdvancementById"}}`

- Muestras de labels EN pendientes:

  - `entries.phbsplAntimagicF.description` → `Dispel Magic` debería ser `Disipar magia`

  - `entries.phbsplBefuddleme.description` → `Greater Restoration` debería ser `Restauración mayor`

  - `entries.phbsplBefuddleme.description` → `Heal` debería ser `Sanar`

  - `entries.phbsplBefuddleme.description` → `Wish` debería ser `Deseo`

  - `entries.phbsplBefuddleme.effects.KjjRlnccDwmAY7gG.description` → `Greater Restoration` debería ser `Restauración mayor`

- Tokens EN más repetidos detectados:

  - `Charmed` × 29

  - `Invisible` × 18

  - `Blinded` × 18

  - `Dodge` × 13

  - `Restrained` × 13

  - `Prone` × 9

  - `Frightened` × 8

  - `Unconscious` × 8


### tables

- Entries: **27**

- UUID labels potencialmente sin traducir: **0**

- Coincidencias de inglés sospechoso: **7**

- Mapping ES: `{}`

- Tokens EN más repetidos detectados:

  - `Tiefling` × 3

  - `Aasimar` × 1

  - `Incapacitated` × 1

  - `Invisible` × 1

  - `Frightened` × 1


## Prioridades recomendadas

### Crítico

- Subir origins.json al esquema nuevo de activities y cambiar su converter a phb2024ActivitiesById.

- Integrar spells-v004 como nueva base de spells.json, porque el base analizado aún arrastra el modelo viejo y muchos labels EN.

- Añadir mapping.results a tables.json para alinearlo con tables-en.json y phb2024RollTableResultsById.


### Alto

- Revisar UUID labels aún en inglés en actors.json y origins.json.

- Actualizar classes.json y equipment.json con los remates finales que ya hiciste en v010/v005 si todavía no están volcados en la base.


### Medio

- Uniformar los -en para que usen el mismo converter que la base ES cuando ya hay activities anidadas (por ejemplo classes-en).

- Pasada final editorial en content.json para nombres propios/criterios (Aasimar, Tiflin/Tiefling, Noble, Criminal, etc.).


## Conclusión

La base actual ya tiene una parte importante estabilizada, pero **no todos los compendios están en el mismo nivel de cierre**. El mejor siguiente bloque es: `origins` → `spells` base → `tables` → `actors`.
