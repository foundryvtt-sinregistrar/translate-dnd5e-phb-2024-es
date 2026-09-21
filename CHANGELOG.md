# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Regression tests for Babele startup, Spanish language variants, and converter coverage across all eight PHB compendiums.

### Changed
- Updated compatibility to Foundry VTT 14.368, dnd5e 6.0.3 and Babele 2.9.1 (minimum Foundry 14.367 and dnd5e 6.0.0).

### Fixed
- Register compendiums and converters through babele.init, deferring language checks to setup so registration does not depend on init hook order.
- Restrict Spanish translations to Spanish and its regional variants, using the configured core language.

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

[Unreleased]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/compare/v1.14.0...HEAD
[1.14.0]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.0