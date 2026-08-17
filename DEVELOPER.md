# Developer Documentation

## Design Goals

- Preserve original IDs and document structure
- Preserve Foundry macros (`@UUID`, `@Embed`, `&Reference`, inline rolls)
- Keep translations resilient to upstream dnd5e updates
- Prefer *mapping-first* + *converter-second* for maintainability

## Converters

- `activities` — translate activities by ID while preserving structure
- `mergeEffects` — merge effects without breaking IDs
- `advancementById` — translate advancement blocks by ID

## Normalization

Normalization is applied after translation to enforce canonical terminology and safe typographic cleanup while protecting:
- Macros and inline rolls
- `<table>` blocks and headings
