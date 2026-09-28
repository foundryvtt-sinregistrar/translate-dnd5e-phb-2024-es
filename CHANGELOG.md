# Changelog

Este archivo registra los cambios relevantes del proyecto. Las nuevas entradas se redactan en español; el historial anterior conserva su contenido, fechas e idioma original.

Los cambios pendientes de publicación se agrupan en `[Unreleased]`, con las categorías `Added`, `Changed` y `Fixed` según corresponda. Al preparar una release, se trasladan a una sección `[X.Y.Z] - YYYY-MM-DD`, con la misma versión que `module.json` y la etiqueta `vX.Y.Z`, y se actualizan los enlaces al final del archivo.

## [Unreleased]

### Changed

- Homogeneizada la estructura de `README.md` y `README.en.md`, con requisitos alineados con el manifiesto, instalación, activación, actualización, soporte y enlaces entre idiomas. Se aclaran la verificación visual pendiente y el alcance sobre documentos ya importados.
- Ampliada y redactada en español la guía `DEVELOPER.md`: entorno, estructura, reglas de traducción, convertidores, comandos de validación, construcción, publicación y diagnóstico. Se documentan las limitaciones actuales del empaquetado y la automatización.
- Establecida la convención de nuevas entradas del changelog en español, manteniendo las categorías y el historial de versiones existentes.

## [1.14.2] - 2026-09-21

### Added
- Regression tests for Babele startup, Spanish language variants, and converter coverage across all eight PHB compendiums.

### Changed
- Updated compatibility to Foundry VTT 14.368, dnd5e 6.0.3 and Babele 2.9.1 (minimum Foundry 14.367 and dnd5e 6.0.0).

### Fixed
- Translated remaining English text across all eight PHB compendiums, including descriptions, activity labels, journal pages, equipment names, spell references, and table tooltips and accessibility labels.
- Standardized plane names and terminology while preserving document IDs, link destinations, roll formulas, and numeric values.
- Register compendiums and converters through babele.init, deferring language checks to setup so registration does not depend on init hook order.
- Restrict Spanish translations to Spanish and its regional variants, using the configured core language.

---

## [1.14.1] - 2026-08-22

### Changed
- Improved Spanish localization across PHB 2024 classes, backgrounds, equipment, origins, rules, and features.
- Standardized terminology for actions, abilities, conditions, and Foundry activities.
- Updated activity and automation labels to Spanish.

### Fixed
- Fixed missing Foundry references for conditions, actions, areas, and cover.
- Fixed untranslated text and English leftovers in class features and background advancements.
- Fixed incomplete translations in rules tables and compendium content.
- Fixed broken or incomplete cross-references in PHB 2024 compendium entries.

---

## [1.14.0] - 2026-08-21

### Added
- Added Foundry VTT 14 compatibility.
- Added support for dnd5e 5.3.x.
- Added the PHB 2024 Spanish translation workflow and automated release packaging.
- Added structured translation passes for the v4 and v4.1 dataset refinement stages.

### Changed
- Updated module metadata for Foundry VTT 14.
- Improved translation normalization and data processing.
- Standardized validation across classes, feats, equipment, content, spells, origins, and tables.
- Updated the release process for module packaging and GitHub publication.

### Fixed
- Corrected untranslated references in the classes dataset.
- Corrected untranslated text and missing keys in the feats dataset.
- Corrected equipment entries, formatting, and metadata issues.
- Corrected content entries and cross-reference mismatches.
- Corrected spell text, activity metadata, and mapping issues.
- Corrected origins references and mappings.
- Corrected table labels, counts, and translation mappings.
- Corrected cross-reference integrity issues across the handbook files.
- Corrected v4 and v4.1 refinement issues in the final translation pipeline.

---

## Version Links

[Unreleased]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/compare/v1.14.2...HEAD
[1.14.2]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.2
[1.14.1]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.1
[1.14.0]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.0
