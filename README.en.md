# 🇬🇧 D&D 5e PHB 2024 -- English (Babele)

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green) ![dnd5e
6.0.3](https://img.shields.io/badge/dnd5e-6.0.3-blue) ![Babele
Required](https://img.shields.io/badge/Babele-required-orange) ![PHB
2024](https://img.shields.io/badge/Babele-required-orange)
[![Latest Release](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Downloads Latest Release](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/latest/total?label=descargas%20%C3%BAltima%20release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Downloads Total](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/total?label=descargas%20totales)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases)

### This module is not affiliated with Wizards of the Coast.
### This module is an unofficial translation of the Player's Handbook 2024.

This module contains translations of content from the **Player's Handbook 2024**, which is proprietary material of Wizards of the Coast.

The translation is offered in compliance with the [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing).

Dungeons & Dragons Player's Handbook 2024 © Wizards of the Coast LLC. All rights reserved.

---

## 📦 Description

Spanish translation of the **Player's Handbook 2024** for the **dnd5e** system in Foundry VTT.

Implemented using **Babele** with architecture:

Mapping First → Converter Second → Normalization Layer

------------------------------------------------------------------------

## 📦 Module Content

This module provides structured translations for the main compendiums of the dnd5e system:

| Compendium | Status |
|-----------|:------:|
| Classes | ✅ |
| Spells | ✅ |
| Feats | ✅ |
| Equipment | ✅ |
| Traits | ✅ |
| Characters and NPCs | ✅ |
| Origins | ✅ |
| Tables | ✅ |
| Rules (Journal Entries) | ✅ |

------------------------------------------------------------------------

## 🧠 Technical Architecture

Mapping First → Converter Second → Normalization Layer

### Converters

- activities
- mergeEffects
- advancementById

### Normalization

- Canonical EN→ES glossary
- Macro protection (@UUID, &Reference, @Embed, \[\[/r ...\]\])
- HTML table and structural heading protection
- Semantic Title Case in structural fields

------------------------------------------------------------------------

## ⚙️ Requirements

- Foundry VTT 14.367+ (14.368)
- Sistema dnd5e 6.0.3
- Babele 2.9.1+
- Player's Handbook (2024)

------------------------------------------------------------------------

## 🚀 Installation

### 🔹 Option 1 — Download ZIP

1. Go to the **Releases** section of the repository.
2. Download the `.zip` file of the latest version.
3. Extract to:

   FoundryVTT/Data/modules/

4. Activate the module from Foundry.
5. Enable the translation from Babele.

---

### 🔹 Option 2 — Direct installation from Foundry (URL)

1. In Foundry, go to **Add-on Modules → Install Module → Install from Manifest URL**.
2. Enter the following URL:

   https://raw.githubusercontent.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/main/module.json

3. Install the module.
4. Activate it and enable the translation from Babele.

------------------------------------------------------------------------

## 📜 License

This project is an unofficial translation of content from the Player's Handbook 2024.

Consult the [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing) for more information on permissions and restrictions.

---

## 📜 Changelog

See: **CHANGELOG.md**

## 👤 Author

foundryvtt-sinregistrar