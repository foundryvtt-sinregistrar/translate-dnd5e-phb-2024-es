# 🇬🇧 D&D 5e PHB 2024 -- Spanish Translation (Babele)

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green) ![dnd5e
6.0.3](https://img.shields.io/badge/dnd5e-6.0.3-blue) ![Babele
Required](https://img.shields.io/badge/Babele-required-orange) ![PHB2024](https://img.shields.io/badge/PHB2024-required-orange)
[![Latest Release](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Downloads Latest Release](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/latest/total?label=latest%20release%20downloads)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Downloads Total](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/total?label=total%20downloads)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases)

### This module is not affiliated with Wizards of the Coast.
### This module is an unofficial translation of the Player's Handbook 2024.

This module contains translations of content from the **Player's Handbook 2024**, which is proprietary material of Wizards of the Coast.

The translation is offered in compliance with the [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing).

Dungeons & Dragons Player's Handbook 2024 © Wizards of the Coast LLC. All rights reserved.

---

## 📦 Description

Spanish translation of the **Player's Handbook 2024** for the **dnd5e** system in Foundry VTT.

Version **1.14.2** updates compatibility and corrects remaining English text across the eight compendiums.

Translations are applied through **Babele**, using mappings and converters for nested documents.

------------------------------------------------------------------------

## 📦 Module Content

This module provides structured translations for the eight compendiums of the official Player’s Handbook (2024) module:

| Compendium | Status |
|-----------|:------:|
| Classes | ✅ |
| Spells | ✅ |
| Feats | ✅ |
| Equipment | ✅ |
| Characters and NPCs | ✅ |
| Origins | ✅ |
| Tables | ✅ |
| Rules (Journal Entries) | ✅ |

------------------------------------------------------------------------

## 🧠 Technical Architecture

Babele mappings select the translated fields. Eight converters handle activities, effects, advancements, journal pages and entries, actors and actor details, and roll-table results while preserving document IDs and references.

Registration uses `babele.init` and waits until `setup` to read the configured core language. Translations are registered automatically for Spanish (`es`) and regional variants such as `es-ES`.

See [DEVELOPER.md](DEVELOPER.md) for converter names, validation commands, and the translation workflow.

------------------------------------------------------------------------

## ⚙️ Requirements

- Foundry VTT: minimum 14.367; verified 14.368.
- dnd5e system: minimum 6.0.0; verified 6.0.3.
- Babele: minimum and verified version 2.9.1.
- Official Player’s Handbook (2024) module, installed and activated.
- Foundry core language set to Spanish (`es` or a regional variant).

------------------------------------------------------------------------

## 🚀 Installation

### 🔹 Option 1 — Download ZIP

1. Go to the **Releases** section of the repository.
2. Download the `.zip` file of the latest version.
3. Extract to:

   FoundryVTT/Data/modules/

4. Activate Babele, the official Player’s Handbook (2024), and this translation module in your world.
5. Select Spanish as Foundry’s core language and reload the world. The translation is registered automatically.

---

### 🔹 Option 2 — Direct installation from Foundry (URL)

1. In Foundry, go to **Add-on Modules → Install Module → Install from Manifest URL**.
2. Enter the following URL:

   https://raw.githubusercontent.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/main/module.json

3. Install the module.
4. Activate Babele, the official Player’s Handbook (2024), and this translation module. Select Spanish as Foundry’s core language and reload the world.

------------------------------------------------------------------------

## 📜 License

This project is an unofficial translation of content from the Player's Handbook 2024.

Consult the [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing) for more information on permissions and restrictions.

---

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md).

## 👤 Author

foundryvtt-sinregistrar