# D&D 5e Player's Handbook (2024) — Spanish Translation

[Español](README.md) | **English**

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green)
![dnd5e 6.0.3](https://img.shields.io/badge/dnd5e-6.0.3-blue)
![Babele required](https://img.shields.io/badge/Babele-required-orange)
![PHB 2024 required](https://img.shields.io/badge/PHB2024-required-orange)
[![Latest release](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Latest release downloads](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/latest/total?label=latest%20release%20downloads)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Total downloads](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/total?label=total%20downloads)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases)

Unofficial Spanish translation of the **Player's Handbook (2024)** module for Foundry VTT and the **dnd5e** system. It uses **Babele** to apply translations to the official product's compendiums. The official module must be installed and enabled.

## Status

Module version: **1.14.3**. Includes translations for all eight handbook compendiums and corrections to text that remained in English.

Automated tests cover registration, language selection, and converter coverage. **Visual verification of the latest corrections in Foundry is still pending**; these tests do not establish that all content has undergone a full functional review.

See [CHANGELOG.md](CHANGELOG.md) for the changes in each version.

## Requirements

Declared compatibility for this version:

| Dependency | Minimum version | Verified version |
|---|---|---|
| Foundry VTT | 14.367 | 14.368 |
| dnd5e system | 6.0.0 | 6.0.3 |
| Babele | 2.9.1 | 2.9.1 |

The official **Player's Handbook (2024)** module (`dnd-players-handbook`) must also be installed and enabled, along with Babele's dependencies. The manifest declares the official product as a required dependency; you must purchase and install it separately. A minimum or verified version of the official product has not yet been established for this translation.

The translation activates when Foundry's language is set to Spanish (`es` or a regional variant such as `es-ES`).

## Installation

### Through Foundry using the manifest

1. On Foundry's Setup screen, open **Add-on Modules → Install Module**.
2. Enter this URL in the manifest field and install the module:

   ```text
   https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest/download/module.json
   ```

3. Follow the [activation](#activation) steps.

This URL uses the manifest attached to the latest stable release. If that asset is not available yet, use the ZIP installation method.

### From a ZIP

1. Open the [latest published release](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest).
2. Download `translate-dnd5e-phb-2024-es.zip`.
3. With Foundry stopped, extract the module folder into `Data/modules/` within your installation's user data directory. The manifest should be at `Data/modules/translate-dnd5e-phb-2024-es/module.json`.
4. Start Foundry and follow the [activation](#activation) steps.

## Activation

1. Open a world that uses the dnd5e system.
2. Enable Babele and its dependencies, the official Player's Handbook (2024) module, and this translation.
3. Select **Spanish** as Foundry's language and reload the world.
4. Open a handbook compendium to check the translation.

The translation registers automatically for Spanish and its regional variants. The Spanish translation is not applied when another language is selected.

## Updating

Update the module through Foundry's module management and reload the world. For a manual installation, download the new version's ZIP and replace the module folder with Foundry stopped.

Before updating Foundry, dnd5e, or the official product, check this translation's requirements and release notes.

Updating the module does not automatically synchronize document copies already imported into the world or added to characters. Compare those copies with the current compendium entry before replacing them, especially if they contain your own changes.

## Included content

The translation covers the following compendiums from the official module:

- Classes.
- Spells.
- Feats.
- Equipment.
- Characters and NPCs.
- Origins.
- Tables.
- Rules and journals.

Babele mappings and converters apply the text to documents and nested elements while preserving their identifiers and references.

## Limitations

- The official product is required; this module provides the translations that Babele applies to its compendiums.
- Verified versions are listed in the requirements table. Compatibility with other combinations needs to be checked.
- Having translations in all eight compendiums does not mean that every visual and functional review is complete. The review status appears near the start of this document.
- Previously imported copies need the review described under [Updating](#updating).

## Support and contributions

Report translation errors or technical problems through the [repository's issues](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/issues). Include:

- Versions of this translation, Foundry, dnd5e, Babele, and the official module.
- The affected compendium and document names.
- Steps to reproduce the problem, the observed result, and the expected result.
- Whether it occurs in the compendium or in an imported copy.

Proposed corrections can be submitted as a pull request to the repository.

## Development

The [developer guide](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/blob/main/DEVELOPER.md) explains the structure, converters, translation rules, and validation commands. It is available in the repository and excluded from the installable ZIP.

## License and credits

The MIT license included in the repository is available in [LICENSE.md](LICENSE.md).

This project contains translations of **Player's Handbook (2024)** material owned by Wizards of the Coast. It is an unofficial translation and is not affiliated with Wizards of the Coast. See also the [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing).

Dungeons & Dragons Player's Handbook 2024 © Wizards of the Coast LLC. All rights reserved.

Module author: [foundryvtt-sinregistrar](https://github.com/foundryvtt-sinregistrar).
