# PHB mini correctiva automática de referencias v1

## Ficheros generados

- `dnd-players-handbook.actors.json` → `dnd-players-handbook.actors.es.mini-correctiva.refs.v1.json`
- `dnd-players-handbook.feats.json` → `dnd-players-handbook.feats.es.mini-correctiva.refs.v1.json`
- `dnd-players-handbook.content.json` → `dnd-players-handbook.content.es.mini-correctiva.refs.v1.json`

## Reemplazos aplicados

### dnd-players-handbook.actors.json
- Total: **11**
  - `Compendium.dnd-players-handbook.classes.Item.phbclcCleric00000` → `Compendium.dnd-players-handbook.classes.Item.phbclcCleric0000` (4)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagPergamino00` → `Compendium.dnd-players-handbook.equipment.Item.phbagParchment00` (3)
  - `Compendium.dnd-players-handbook.spells.Item.phbsplFalseLife000` → `Compendium.dnd-players-handbook.spells.Item.phbsplFalseLife0` (2)
  - `Compendium.dnd-players-handbook.spells.Item.phbsplRayofEnfeeb` → `Compendium.dnd-players-handbook.spells.Item.phbsplRayofEnfee` (2)

### dnd-players-handbook.feats.json
- Total: **16**
  - `Compendium.dnd-players-handbook.equipment.Item.phbagAbrojos000` → `Compendium.dnd-players-handbook.equipment.Item.phbagCaltrops000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagAntorcha000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagTorch000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagBolsa000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagPouch000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagCampana0000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagBell0000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagCesta00000` → `Compendium.dnd-players-handbook.equipment.Item.phbagBasket00000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagCubo00000` → `Compendium.dnd-players-handbook.equipment.Item.phbagBucket00000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagCuerda0000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagRope0000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagEscalera00000` → `Compendium.dnd-players-handbook.equipment.Item.phbagLadder00000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagJarra00000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagJug00000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagLámpara0000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagLamp0000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagPala00000` → `Compendium.dnd-players-handbook.equipment.Item.phbagShovel00000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagRed00000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagNet00000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagTienda de campaña0000000` → `Compendium.dnd-players-handbook.equipment.Item.phbagTent0000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbagYesquero00` → `Compendium.dnd-players-handbook.equipment.Item.phbagTinderbox00` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbwepGarrote000000` → `Compendium.dnd-players-handbook.equipment.Item.phbwepClub000000` (1)
  - `Compendium.dnd-players-handbook.equipment.Item.phbwepGran garrote0` → `Compendium.dnd-players-handbook.equipment.Item.phbwepGreatclub0` (1)

### dnd-players-handbook.content.json
- Total: **1**
  - `Compendium.dnd5e.content24.JournalEntry.phbAppendixDRule.JournalEntryPage.JxboWb0XHo2GwqD0` → `Compendium.dnd5e.content24.JournalEntry.phbAppendixDRule.JournalEntryPage.qAFzmGZKhVvAEUF3` (1)

## Resumen

- Referencias internas corregidas: **27 ocurrencias / 20 refs únicas**
- Referencias externas corregidas: **1 ocurrencia / 1 ref única**
- Reemplazos totales aplicados: **28**

## Externas no corregidas automáticamente

- `Compendium.dnd5e.content24.JournalEntry.phbAppendixDRule.JournalEntryPage.ldmA1PbnEGVkmE11` — **Darkvision**. No existe ese pageId en dnd5e.content24 y el destino exacto no es determinista con el export disponible.
- `Compendium.dnd5e.content24.JournalEntry.phbAppendixDRule.JournalEntryPage.r64UrNusMhwJVnxb` — **Tremorsense**. No existe ese pageId en dnd5e.content24 y el destino exacto no es determinista con el export disponible.
- `Compendium.dnd5e.content24.JournalEntry.phbAppendixDRule.JournalEntryPage.sacjsfm9ZXnw4Tqc` — **Blindsight**. No existe ese pageId en dnd5e.content24 y el destino exacto no es determinista con el export disponible.

## Nota

La correctiva es deliberadamente conservadora: solo aplica cambios con destino exacto verificable o inequívoco por nombre.