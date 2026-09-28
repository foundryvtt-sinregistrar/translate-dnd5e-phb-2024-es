# D&D 5e Player's Handbook (2024) — Traducción al español

**Español** | [English](README.en.md)

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green)
![dnd5e 6.0.3](https://img.shields.io/badge/dnd5e-6.0.3-blue)
![Babele requerido](https://img.shields.io/badge/Babele-required-orange)
![PHB 2024 requerido](https://img.shields.io/badge/PHB2024-required-orange)
[![Última versión](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Descargas de la última versión](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/latest/total?label=descargas%20%C3%BAltima%20release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest)
[![Descargas totales](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/total?label=descargas%20totales)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases)

Traducción no oficial al español del módulo **Player's Handbook (2024)** para Foundry VTT y el sistema **dnd5e**. Utiliza **Babele** para aplicar las traducciones a los compendios del producto oficial, que debe estar instalado y activado.

## Estado

Versión del módulo: **1.14.3**. Incluye traducciones para los ocho compendios del manual y correcciones de textos que permanecían en inglés.

Hay pruebas automatizadas de registro, selección del idioma y cobertura de convertidores. La revisión visual de una muestra se registra a continuación; estas pruebas no acreditan una revisión funcional completa del contenido.

Consulta [CHANGELOG.md](CHANGELOG.md) para conocer los cambios de cada versión.

Comprobación del 28 de septiembre de 2026 en Foundry 14.368, dnd5e 6.0.3 y Babele 2.9.1: lectura de 1548 documentos en 8 compendios, comprobación de nombres y campos de texto explícitos e importación y revisión visual de una muestra. No es una revisión lingüística ni funcional exhaustiva; permanecen algunas etiquetas inglesas del contenido original.

## Requisitos

Compatibilidad declarada para esta versión:

| Dependencia | Versión mínima | Versión verificada |
|---|---|---|
| Foundry VTT | 14.367 | 14.368 |
| Sistema dnd5e | 6.0.0 | 6.0.3 |
| Babele | 2.9.1 | 2.9.1 |

También se necesita el módulo oficial **Player's Handbook (2024)** (`dnd-players-handbook`), instalado y activado, y las dependencias de Babele. El producto oficial está declarado como dependencia obligatoria en el manifiesto; debes adquirirlo e instalarlo por separado. Aún no se ha establecido una versión mínima ni verificada del producto oficial para esta traducción.

La traducción se activa al seleccionar español como idioma de Foundry (`es` o una variante regional como `es-ES`).

## Instalación

### Desde Foundry mediante manifiesto

1. En la pantalla de configuración de Foundry, abre **Add-on Modules → Install Module**.
2. Introduce esta URL en el campo de manifiesto e instala el módulo:

   ```text
   https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest/download/module.json
   ```

3. Sigue los pasos de [activación](#activación).

Esta URL utiliza el manifiesto adjunto a la última release estable. Si ese adjunto todavía no está disponible, utiliza la instalación desde ZIP.

### Desde un ZIP

1. Abre la [última versión publicada](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/releases/latest).
2. Descarga el archivo `translate-dnd5e-phb-2024-es.zip`.
3. Con Foundry detenido, extrae la carpeta del módulo dentro de `Data/modules/`, en el directorio de datos de usuario de tu instalación. El manifiesto debe quedar en `Data/modules/translate-dnd5e-phb-2024-es/module.json`.
4. Inicia Foundry y sigue los pasos de [activación](#activación).

## Activación

1. Abre un mundo que utilice el sistema dnd5e.
2. Activa Babele y sus dependencias, el módulo oficial Player's Handbook (2024) y esta traducción.
3. Selecciona **Español** como idioma de Foundry y recarga el mundo.
4. Abre uno de los compendios del manual para comprobar la traducción.

El registro de la traducción es automático para español y sus variantes regionales. Con otros idiomas no se aplica la traducción española.

## Actualización

Actualiza el módulo desde la administración de módulos de Foundry y recarga el mundo. Si lo instalaste manualmente, descarga el ZIP de la nueva versión y sustituye la carpeta del módulo con Foundry detenido.

Antes de actualizar Foundry, dnd5e o el producto oficial, consulta los requisitos y las notas de la versión de esta traducción.

Actualizar el módulo no sincroniza automáticamente las copias de documentos ya importadas al mundo o incorporadas a personajes. Compara esas copias con la entrada actual del compendio antes de sustituirlas, especialmente si tienen cambios propios.

## Contenido incluido

La traducción cubre los siguientes compendios del módulo oficial:

- Clases.
- Conjuros.
- Dotes.
- Equipo.
- Personajes y PNJ.
- Orígenes.
- Tablas.
- Reglas y diarios.

Los mapeos y convertidores de Babele aplican los textos a documentos y elementos anidados conservando sus identificadores y referencias.

## Limitaciones

- Se requiere el producto oficial; este módulo proporciona las traducciones que Babele aplica a sus compendios.
- Las versiones verificadas son las indicadas en la tabla de requisitos. La compatibilidad con otras combinaciones necesita comprobación.
- La presencia de traducciones en los ocho compendios no implica que toda la revisión visual y funcional esté completada. El estado de esa revisión figura al inicio de este documento.
- Las copias ya importadas requieren la revisión descrita en [Actualización](#actualización).

## Soporte y contribuciones

Comunica errores de traducción o funcionamiento en las [incidencias del repositorio](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/issues). Incluye:

- Versiones de esta traducción, Foundry, dnd5e, Babele y el módulo oficial.
- Nombre del compendio y del documento afectado.
- Pasos para reproducir el problema, resultado observado y resultado esperado.
- Si ocurre al abrir el compendio o en una copia ya importada.

Las propuestas de corrección pueden enviarse mediante una pull request al repositorio.

## Desarrollo

La [guía de desarrollo](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phb-2024-es/blob/main/DEVELOPER.md) explica la estructura, los convertidores, las reglas de traducción y los comandos de validación. Está disponible en el repositorio; se excluye del ZIP instalable.

## Licencia y créditos

La licencia MIT incluida en el repositorio se puede consultar en [LICENSE.md](LICENSE.md).

Este proyecto contiene traducciones de material del **Player's Handbook (2024)**, propiedad de Wizards of the Coast. Es una traducción no oficial y no está afiliada a Wizards of the Coast. Consulta también la [Wizards of the Coast Fan Content Policy](https://dnd.wizards.com/en/digital-tools-licensing).

Dungeons & Dragons Player's Handbook 2024 © Wizards of the Coast LLC. Todos los derechos reservados.

Autor del módulo: [foundryvtt-sinregistrar](https://github.com/foundryvtt-sinregistrar).
