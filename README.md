# 🇪🇸 D&D 5e PHB 2024 -- Español (Babele)

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green) ![dnd5e
6.0.3](https://img.shields.io/badge/dnd5e-6.0.3-blue) ![Babele
Required](https://img.shields.io/badge/Babele-required-orange) ![PHB2024](https://img.shields.io/badge/PHB2024-required-orange)
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

La versión **1.14.2** actualiza la compatibilidad y corrige restos de inglés en los ocho compendios.

Las traducciones se aplican mediante **Babele**, con mapeos y convertidores para documentos anidados.

------------------------------------------------------------------------

## 📦 Contenido del Módulo

Este módulo proporciona traducciones estructuradas para los ocho compendios del módulo oficial Player’s Handbook (2024):

| Compendio | Estado |
|----------|:------:|
| Clases | ✅ |
| Conjuros | ✅ |
| Dotes | ✅ |
| Equipo | ✅ |
| Personajes y PNJ | ✅ |
| Orígenes | ✅ |
| Tablas | ✅ |
| Reglas (diarios) | ✅ |

------------------------------------------------------------------------

## 🧠 Arquitectura Técnica

Los mapeos de Babele seleccionan los campos traducidos. Ocho convertidores gestionan actividades, efectos, avances, páginas y entradas de diario, actores y sus detalles, y resultados de tablas, conservando los identificadores y las referencias.

El registro utiliza `babele.init` y espera hasta `setup` para leer el idioma configurado en Foundry. Las traducciones se registran automáticamente para español (`es`) y variantes regionales como `es-ES`.

Consulta [DEVELOPER.md](DEVELOPER.md) para conocer los convertidores, los comandos de validación y el flujo de traducción.

------------------------------------------------------------------------

## ⚙️ Requisitos

- Foundry VTT: mínimo 14.367; verificado 14.368.
- Sistema dnd5e: mínimo 6.0.0; verificado 6.0.3.
- Babele: versión mínima y verificada 2.9.1.
- Módulo oficial Player’s Handbook (2024), instalado y activado.
- Idioma de Foundry configurado en español (`es` o una variante regional).

------------------------------------------------------------------------

## 🚀 Instalación

### 🔹 Opción 1 — Descargar ZIP

1. Ir a la sección **Releases** del repositorio.
2. Descargar el fichero `.zip` de la última versión.
3. Descomprimir en:

   FoundryVTT/Data/modules/

4. Activar Babele, el módulo oficial Player’s Handbook (2024) y este módulo de traducción en el mundo.
5. Seleccionar español como idioma de Foundry y recargar el mundo. La traducción se registra automáticamente.

---

### 🔹 Opción 2 — Instalación directa desde Foundry (URL)

1. En Foundry, ir a **Add-on Modules → Install Module → Install from Manifest URL**.
2. Introducir la siguiente URL:

   https://raw.githubusercontent.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/main/module.json

3. Instalar el módulo.
4. Activar Babele, el módulo oficial Player’s Handbook (2024) y este módulo de traducción. Seleccionar español como idioma de Foundry y recargar el mundo.

------------------------------------------------------------------------

## 📜 Licencia

Este proyecto es una traducción no oficial del contenido del Player's Handbook 2024.

Consulta la [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing) para más información sobre permisos y restricciones.

---

## 📜 Changelog

Consulta [CHANGELOG.md](CHANGELOG.md).

## 👤 Autor

foundryvtt-sinregistrar