# Changelog

Este archivo registra los cambios relevantes del proyecto. Las nuevas entradas se redactan en español; el historial anterior conserva su contenido, fechas e idioma original.

Los cambios pendientes de publicación se agrupan en `[Unreleased]`, con las categorías `Added`, `Changed` y `Fixed` según corresponda. Al preparar una release, se trasladan a una sección `[X.Y.Z] - YYYY-MM-DD`, con la misma versión que `module.json` y la etiqueta `vX.Y.Z`, y se actualizan los enlaces al final del archivo.

## [Unreleased]

## [1.14.3] - 2026-09-28

### Added

- Añadidos perfiles de publicación por proyecto, SHA-256 de los artefactos y pruebas de alias, canal y referencia del perfil. La validación reutilizable conserva ambos ZIP y permite seleccionar explícitamente una revisión.
- Añadida una plantilla de homogeneización con documentación bilingüe, workflows parametrizados, inventario de fuentes comunes y procedimiento de adopción y actualización por proyecto, conservando sus excepciones.
- Añadido `.editorconfig` con UTF-8, LF e indentación por tipo de archivo, conservando los espacios finales de Markdown. Se documenta su uso sin reformatear las traducciones ni el código existente.
- Añadida validación automática en pull requests y pushes a ramas: pruebas Node/Python, construcción del paquete y conservación del ZIP y manifiesto validados como artefacto de la ejecución durante siete días.
- Añadidas pruebas del constructor con repositorios Git temporales para referencias históricas, cambios locales, etiquetas, validación del ZIP y conservación de artefactos ante fallos.
- Generado `dist/module.json` como copia exacta del manifiesto incluido en el ZIP y utilizado como adjunto en el workflow de release.

### Changed

- Preparado el canal de instalación mediante el manifiesto adjunto a la última release estable, con la descarga del ZIP fijada a la etiqueta de su versión. Documentada la publicación antes de actualizar `main`, conservando la entrada anterior durante la transición.
- La release reutiliza el workflow de validación y crea el borrador únicamente después de superar las comprobaciones, adjuntando el paquete ya validado. El permiso de escritura queda limitado al job que crea el borrador.
- Homogeneizada la estructura de `README.md` y `README.en.md`, con requisitos alineados con el manifiesto, instalación, activación, actualización, soporte y enlaces entre idiomas. Se aclaran la verificación visual pendiente y el alcance sobre documentos ya importados.
- Ampliada y redactada en español la guía `DEVELOPER.md`: entorno, estructura, reglas de traducción, convertidores, comandos de validación, construcción, publicación y diagnóstico. Se documentan las limitaciones actuales del empaquetado y la automatización.
- Establecida la convención de nuevas entradas del changelog en español, manteniendo las categorías y el historial de versiones existentes.
- Simplificado `.gitignore` con reglas explícitas para artefactos, cachés, fuentes e informes locales, conservando las excepciones de configuración compartida del IDE. Se eliminan las exclusiones genéricas de nombres que empiezan por `_`.
- Definidos finales de línea LF para fuentes, JSON y documentación en `.gitattributes`, manteniendo la normalización existente en Git.
- Normalizado el título Markdown de `LICENSE.md`, conservando el texto de la licencia MIT.
- El constructor valida los archivos admitidos, los JSON, los documentos obligatorios y las entradas del manifiesto antes de reemplazar los artefactos. `--name` cambia el nombre del ZIP conservando la carpeta interna con el identificador del módulo.

### Fixed

- El constructor rechaza releases con URLs de manifiesto o descarga incoherentes y opciones que omitan el ZIP anunciado. Añadidas pruebas para estos casos, las referencias históricas y la conservación de artefactos ante fallos.
- Declarado el módulo oficial `dnd-players-handbook` como dependencia obligatoria en `module.json`, de acuerdo con los requisitos de ambos README. Los límites de versión del producto oficial quedan pendientes de comprobación funcional.
- Corregida la construcción con `--ref`: identidad, versión, manifiesto y contenido proceden del mismo commit, incluso con un checkout distinto o cambios locales permitidos. Se comprueba la correspondencia entre etiqueta, versión, commit y entrada de changelog al preparar releases.
- Completado el aviso de copyright de `LICENSE.md` con `2026 foundryvtt-sinregistrar`, sustituyendo los marcadores de plantilla.
- Corregido el enlace de licencia de `module.json` para apuntar al archivo existente `LICENSE.md`.
- Excluidos del ZIP instalable las pruebas y los archivos auxiliares de desarrollo. `staged.txt` deja de versionarse y conserva su copia local; se mantienen en el paquete ambos README, el changelog y la licencia.

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

[Unreleased]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/compare/v1.14.3...HEAD
[1.14.3]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.3
[1.14.2]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.2
[1.14.1]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.1
[1.14.0]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/tag/v1.14.0
