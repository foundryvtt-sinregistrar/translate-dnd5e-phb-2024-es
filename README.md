# 🇪🇸 D&D 5e PHB 2024 -- Español (Babele)

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green) ![dnd5e
5.3.x](https://img.shields.io/badge/dnd5e-5.3.x-blue) ![Babele
Required](https://img.shields.io/badge/Babele-required-orange) ![PHB
2024](https://img.shields.io/badge/Babele-required-orange)
[![Latest Release](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Downloads Latest Release](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/latest/total?label=descargas%20%C3%BAltima%20release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Downloads Total](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/total?label=descargas%20totales)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases)

### Este módulo no está afiliado a Wizards of the Coast.
### Este módulo es una traducción no oficial del Player's Handbook 2024.

Este módulo contiene traducciones de contenido del **Player's Handbook 2024**, que es material propietario de Wizards of the Coast.

La traducción se ofrece de conformidad con la [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing).

Dungeons & Dragons Player's Handbook 2024 © Wizards of the Coast LLC. Todos los derechos reservados.

---

## 📦 Descripción

Traducción al español del **Player's Handbook 2024** del sistema **dnd5e** para Foundry VTT.

Implementado mediante **Babele** con arquitectura:

Mapping First → Converter Second → Normalization Layer

------------------------------------------------------------------------

## 📦 Contenido del Módulo

Este módulo proporciona traducciones estructuradas para los principales compendios del sistema dnd5e:

| Compendio | Estado |
|----------|:------:|
| Clases | ✅ |
| Conjuros | ✅ |
| Dotes | ✅ |
| Equipo | ✅ |
| Rasgos | ✅ |
| Personajes y PNJ | ✅ |
| Orígenes | ✅ |
| Tablas | ✅ |
| Reglas (Journal Entries) | ✅ |

------------------------------------------------------------------------

## 🧠 Arquitectura Técnica

Mapping First → Converter Second → Normalization Layer

### Convertidores

- activities
- mergeEffects
- advancementById

### Normalización

- Glosario EN→ES canónico
- Protección de macros (@UUID, &Reference, @Embed, \[\[/r ...\]\])
- Protección de tablas HTML y encabezados estructurales
- Title Case semántico en campos estructurales

------------------------------------------------------------------------

## ⚙️ Requisitos

- Foundry VTT v13
- Foundry VTT v14+
- Sistema dnd5e 5.3.x
- Babele
- Player's Handbook (2024)

------------------------------------------------------------------------

## 🚀 Instalación

### 🔹 Opción 1 — Descargar ZIP

1. Ir a la sección **Releases** del repositorio.
2. Descargar el fichero `.zip` de la última versión.
3. Descomprimir en:

   FoundryVTT/Data/modules/

4. Activar el módulo desde Foundry.
5. Activar la traducción desde Babele.

---

### 🔹 Opción 2 — Instalación directa desde Foundry (URL)

1. En Foundry, ir a **Add-on Modules → Install Module → Install from Manifest URL**.
2. Introducir la siguiente URL:

   https://raw.githubusercontent.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/main/module.json

3. Instalar el módulo.
4. Activarlo y habilitar la traducción desde Babele.

------------------------------------------------------------------------

## 📜 Licencia

Este proyecto es una traducción no oficial del contenido del Player's Handbook 2024.

Consulta la [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing) para más información sobre permisos y restricciones.

---

## 📜 Changelog

Consulta: **CHANGELOG.md**

## 👤 Autor

foundryvtt-sinregistrar