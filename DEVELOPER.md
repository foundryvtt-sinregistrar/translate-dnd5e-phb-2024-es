# Developer Documentation

## Version and Compatibility

Module version: **1.14.2**. `module.json` is the source of truth for release metadata.

| Dependency | Minimum | Verified |
|------------|---------|----------|
| Foundry VTT | 14.367 | 14.368 |
| dnd5e | 6.0.0 | 6.0.3 |
| Babele | 2.9.1 | 2.9.1 |

The official Player’s Handbook (2024) module must be installed and activated in the world.

## Design Goals

- Preserve original IDs, JSON keys, document structure, and numeric values.
- Preserve Foundry references and roll expressions (`@UUID`, `@Embed`, `&Reference`, inline rolls).
- Use Babele mappings first and converters for nested data.
- Keep Spanish terminology consistent across the eight compendiums.

## Startup and Language Selection

`module.json` loads `scripts/converters.js` and `scripts/babele-register.js`.
Both subscribe to `babele.init` and defer registration until `setup`, when `game.settings.get("core", "language")` is available and before Babele loads its translation session at `ready`.

Converters are registered only for Spanish. Compendiums are registered for the configured Spanish language and its base code (`es`), with duplicates removed. For example, `es-ES` registers both `es-ES` and `es`; other languages do not activate the Spanish translation.

## Converters

The implementations live in `scripts/converters/`; the exact registered names are:

| Converter | Scope |
|-----------|-------|
| `phb2024ActivitiesById` | Activities |
| `phb2024MergeEffects` | Effects |
| `phb2024AdvancementById` | Advancement blocks |
| `phb2024JournalPagesById` | Journal pages |
| `phb2024JournalEntryFullById` | Journal entries |
| `phb2024ActorFullById` | Actors and embedded data |
| `phb2024ActorDetails` | Actor details |
| `phb2024RollTableResultsById` | Roll-table results |

Mappings in `compendium/dnd-players-handbook.*.json` reference these names. The eight files cover actors, classes, content (journals), equipment, feats, origins, spells, and tables.

## Translation Workflow

Edit the Spanish string values in the compendium JSON files. Keep lookup keys, IDs, UUID destinations, macro parameters, roll expressions, and technical HTML attributes unchanged. Visible reference labels and literal tooltip or accessibility text may be translated; localization keys such as `EDITOR.DND5E.Inline.ApplyStatus` must remain intact.

Terminology and typographic normalization are part of preparing the translation files, not a separate runtime layer loaded by the manifest. Preserve HTML structure and use the existing Spanish names of linked spells, features, and activities.

The local audit report is `dev-tools/_Informes/INFORME-CONTENIDO-INGLES.md`. Its original findings are retained as a snapshot, with follow-up sections recording corrections. This directory is ignored by Git and the report is not part of the tracked release documentation.

## Validation

From the module root, run the startup regression checks:

```sh
node --test tests/babele-registration.test.mjs
git diff --check
```

The tests check deferred registration, Spanish language variants, exclusion of other languages, and converter coverage for the eight compendiums. For translation changes, also parse the JSON and compare keys, IDs, references, formulas, numeric values, and HTML structure against the previous version.

Automated checks do not replace validation in Foundry. With the required modules active and the core language set to Spanish, reload the world and inspect translated compendium entries, embedded activities, journal pages, and table controls. Visual verification of the latest translation corrections remains pending.

## Release Documentation

Keep `module.json`, `CHANGELOG.md`, `README.md`, and `README.en.md` aligned when changing versions or compatibility. Record changes under the release version and update the changelog links. Documentation updates alone do not publish a release or create a Git tag.
