# Guía de desarrollo

Esta guía describe cómo mantener `translate-dnd5e-phb-2024-es` con las herramientas actuales del repositorio. Para instalar y utilizar el módulo, consulta [README.md](README.md) o [README.en.md](README.en.md).

## Entorno y compatibilidad

La versión declarada es **1.14.2**. [module.json](module.json) es la referencia para identidad, versión, compatibilidad, idiomas y archivos de entrada.

| Dependencia de ejecución | Mínima | Verificada |
|---|---|---|
| Foundry VTT | 14.367 | 14.368 |
| dnd5e | 6.0.0 | 6.0.3 |
| Babele | 2.9.1 | 2.9.1 |

Las pruebas dentro de Foundry requieren además el módulo oficial **Player's Handbook (2024)** (`dnd-players-handbook`), instalado y activado, y las dependencias de Babele. El manifiesto de esta traducción todavía no declara el producto oficial en `relationships.requires`; hay que instalarlo por separado.

| Herramienta de desarrollo | Uso | Referencia de entorno |
|---|---|---|
| Git | Historial, revisión y construcción con `git archive` | Disponible en la terminal |
| Node.js | Pruebas con `node:test` | Comprobadas localmente con 24.17.0 |
| Python | Validación JSON y construcción del ZIP | Validación JSON comprobada con 3.14.6; el workflow de release usa 3.11 |

Estas versiones describen los entornos utilizados; no constituyen una matriz completa de compatibilidad de las herramientas.

No hay `package.json` ni dependencias Python externas para los comandos de esta guía. Las pruebas de registro usan módulos incluidos en Node y simulan los hooks: se pueden ejecutar sin instalar Foundry, Babele ni el producto oficial.

## Preparación del trabajo

Ejecuta los comandos desde la raíz del repositorio, donde está `module.json`.

```sh
git status --short --branch
node --version
python --version
```

Para esta homogeneización, crea las ramas de trabajo desde `develop` después de alinearla con `main`. Agrupa cada paso en un commit revisable y conserva los cambios locales ajenos a ese paso.

Para comprobar cambios dentro de Foundry, coloca el módulo en `Data/modules/translate-dnd5e-phb-2024-es/` de los datos de usuario y utiliza un mundo de prueba dnd5e. Activa Babele, sus dependencias, el producto oficial y la traducción; selecciona español y recarga.

## Estructura del repositorio

| Ruta | Responsabilidad |
|---|---|
| `module.json` | Identidad, compatibilidad, dependencias, idiomas y puntos de entrada |
| `compendium/` | Ocho archivos JSON de traducción Babele |
| `lang/en.json`, `lang/es.json` | Mensajes de interfaz propios del módulo |
| `scripts/babele-register.js` | Registro de los compendios para español |
| `scripts/converters.js` | Registro de convertidores |
| `scripts/converters/` | Traducción de estructuras anidadas |
| `tests/babele-registration.test.mjs` | Pruebas de registro, idioma y cobertura de convertidores |
| `dev-tools/buildScripts/build_release.py` | Construcción desde una referencia Git |
| `.github/workflows/release.yml` | Construcción y creación de una release en borrador al subir un tag |
| `.gitattributes` | Exclusiones de `git archive` |
| `.gitignore` | Exclusiones de nuevos archivos locales |
| `README.md`, `README.en.md` | Documentación de uso en español e inglés |
| `CHANGELOG.md`, `LICENSE.md` | Historial y licencia incluida |
| `dist/` | ZIP generados; directorio ignorado por Git |

Los archivos de `compendium/` tienen el prefijo `dnd-players-handbook.`:

| Sufijo | Contenido |
|---|---|
| `actors.json` | Personajes y PNJ, incluidos sus elementos anidados |
| `classes.json` | Clases |
| `content.json` | Reglas y diarios |
| `equipment.json` | Equipo |
| `feats.json` | Dotes |
| `origins.json` | Orígenes |
| `spells.json` | Conjuros |
| `tables.json` | Tablas |

`dev-tools/_toDoo.md` conserva notas históricas. No es el procedimiento vigente de publicación.

## Registro e idioma

`module.json` carga `scripts/converters.js` y `scripts/babele-register.js`. Ambos escuchan `babele.init` y posponen el registro hasta `setup`, cuando está disponible `game.settings.get("core", "language")`, antes de la sesión de traducción de Babele en `ready`.

Los convertidores se registran solo para español. Los compendios se registran para el idioma configurado y su código base, eliminando duplicados: `es-ES` registra `es-ES` y `es`; `es` se registra una sola vez. Otros idiomas no activan la traducción española. Los cambios de idioma requieren recargar el mundo.

## Convertidores

Los nombres que pueden utilizar los mappings son los registrados en [scripts/converters.js](scripts/converters.js):

| Nombre registrado | Alcance |
|---|---|
| `phb2024ActivitiesById` | Actividades |
| `phb2024MergeEffects` | Efectos |
| `phb2024AdvancementById` | Avances |
| `phb2024JournalPagesById` | Páginas de diario |
| `phb2024JournalEntryFullById` | Entradas de diario |
| `phb2024ActorFullById` | Actores y datos anidados |
| `phb2024ActorDetails` | Detalles del actor |
| `phb2024RollTableResultsById` | Resultados de tablas |

Utiliza los mappings de Babele para campos simples y los convertidores existentes para datos anidados. Si cambias un nombre o añades un convertidor, actualiza su registro, los mappings que lo usan y las pruebas pertinentes.

Las pruebas actuales comprueban que los convertidores referenciados existen; no verifican de forma exhaustiva el comportamiento de cada convertidor.

## Edición y revisión de traducciones

1. Identifica el compendio y el documento afectado y registra las versiones de las fuentes utilizadas si han cambiado.
2. Edita los valores de texto españoles. Conserva las claves de búsqueda, los IDs y la estructura esperada por el mapping.
3. Contrasta la terminología con las entradas relacionadas de los ocho compendios.
4. Revisa el diff y ejecuta las comprobaciones portables.
5. Si afecta a contenido visible, mappings o convertidores, comprueba documentos representativos en Foundry.
6. Anota los cambios en `CHANGELOG.md`, bajo `[Unreleased]`. Actualiza ambos README cuando cambien requisitos, instalación, alcance o estado de revisión.

Durante la traducción:

- Conserva IDs, destinos UUID, rutas de recursos, parámetros de macros, fórmulas, números y campos mecánicos.
- Mantén `@UUID`, `@Embed`, `&Reference`, tiradas en línea y atributos técnicos del HTML.
- Puedes traducir las etiquetas visibles de referencias y los textos literales de ayuda o accesibilidad. Conserva claves de localización como `EDITOR.DND5E.Inline.ApplyStatus`.
- Respeta la estructura HTML y los nombres españoles ya utilizados para conjuros, rasgos y actividades enlazadas.
- La normalización terminológica y tipográfica se realiza al preparar los textos; el manifiesto no carga una capa independiente de normalización.

No hay un exportador de fuentes ni una cadena OCR versionados en este proyecto. Las referencias originales deben mantenerse fuera del contenido distribuible. No copies bases de datos del producto oficial, PDF ni exportaciones completas a `compendium/`.

El informe local `dev-tools/_Informes/INFORME-CONTENIDO-INGLES.md`, cuando esté disponible, es una referencia de auditoría con seguimientos de correcciones. Su directorio está ignorado por Git y no forma parte de un clon ni de la documentación distribuida. Las instrucciones esenciales deben permanecer en archivos versionados.

## Validación

### Comprobaciones portables

Ejecuta las pruebas existentes:

```sh
node --test tests/babele-registration.test.mjs
```

La suite actual contiene 11 pruebas: registro diferido, variantes de español, exclusión de otros idiomas y existencia de los convertidores usados en los ocho compendios. No necesita fuentes privadas ni una instalación adyacente de Babele.

Comprueba la sintaxis de los 11 JSON de distribución: el manifiesto, los ocho compendios y los dos archivos de idioma. Este comando usa la biblioteca estándar de Python y no modifica archivos:

```sh
python -c "import json; from pathlib import Path; paths = [Path('module.json'), *Path('compendium').glob('*.json'), *Path('lang').glob('*.json')]; [json.loads(p.read_text(encoding='utf-8')) for p in paths]; print(len(paths), 'JSON validos')"
```

Revisa los cambios y sus espacios:

```sh
git diff --check
git diff --stat
git diff
```

Si ya has preparado los archivos para un commit, revisa también `git diff --cached --check` y `git diff --cached`. Un JSON sintácticamente válido no demuestra integridad de IDs, referencias, fórmulas, valores numéricos ni HTML: compara esos elementos en los cambios de contenido.

### Comprobación funcional en Foundry

Para cambios de contenido o código de ejecución:

1. Anota las versiones de Foundry, dnd5e, Babele, el producto oficial y la traducción.
2. Recarga el mundo de prueba en español.
3. Abre documentos de los compendios afectados y revisa nombres, texto, páginas de diario, actividades, efectos y controles de tablas.
4. Importa documentos representativos y comprueba enlaces, elementos anidados y tiradas.
5. Si cambias el registro, comprueba también que otro idioma no activa las traducciones españolas.
6. Registra el alcance, resultado y comprobaciones pendientes junto al cambio.

Actualizar el módulo no sincroniza automáticamente las copias ya importadas al mundo o incorporadas a personajes. Utiliza entradas del compendio o copias nuevas para comprobar una corrección sin confundirla con datos anteriores.

La verificación visual de las últimas correcciones de traducción sigue pendiente. El resultado de las pruebas portables no sustituye esa comprobación.

## Construcción del paquete

El [constructor actual](dev-tools/buildScripts/build_release.py) utiliza `git archive`. Para construir la versión del checkout, confirma los cambios que quieras incluir y comprueba que el árbol esté limpio:

```sh
git status --short
python dev-tools/buildScripts/build_release.py --dist dist --ref HEAD
```

Con el identificador y la versión actuales genera:

- `dist/translate-dnd5e-phb-2024-es-1.14.2.zip`.
- `dist/translate-dnd5e-phb-2024-es.zip`.

Ambos contienen una carpeta raíz `translate-dnd5e-phb-2024-es/`. El builder no genera un manifiesto externo en `dist/`; el workflow adjunta el `module.json` del checkout.

El constructor lee `id` y `version` del archivo local, pero extrae los archivos de la referencia indicada. Para construir otra versión, cambia primero al commit correspondiente y utiliza `--ref HEAD` con el árbol limpio. `--allow-dirty` evita la comprobación de limpieza, pero no incorpora al archivo Git los cambios sin commit y puede desalinear los nombres del ZIP con su contenido; no lo utilices para preparar releases.

Inspecciona el archivo antes de publicarlo:

```sh
python -m zipfile -l dist/translate-dnd5e-phb-2024-es.zip
python -m zipfile -t dist/translate-dnd5e-phb-2024-es.zip
```

La segunda comprobación detecta problemas de integridad del ZIP, no valida su funcionamiento en Foundry. Comprueba además el manifiesto incluido, los scripts e idiomas declarados y la instalación del paquete en un entorno de prueba.

### Exclusiones de distribución

`.gitattributes` establece LF para fuentes, JSON y documentación, y excluye herramientas, pruebas, configuración local, temporales y `DEVELOPER.md` de `git archive`. Los README, CHANGELOG y LICENSE se incluyen. Los archivos ya versionados estaban normalizados a LF; estas reglas mantienen ese criterio para cambios y checkouts posteriores.

`tests/` sigue versionado para ejecutar las comprobaciones, pero queda fuera del ZIP. `staged.txt` es un archivo auxiliar local: se ha retirado del índice conservando la copia de trabajo, y está ignorado y excluido de distribución.

`.gitignore` protege las fuentes de `dev-tools/export/_data/` y `dev-tools/export/data/`, así como los informes locales de `dev-tools/_Informes/`. Permite versionar `dev-tools/export/data/.gitkeep` si se utiliza. Las exclusiones son explícitas; un archivo nuevo no queda oculto simplemente por empezar por `_`.

Se conservan las excepciones de IDE para estilos, configuraciones de ejecución y archivos seleccionados de VS Code. Revisa cualquier archivo compartido antes de añadirlo al índice. `.gitignore` no retira archivos ya versionados y no determina el contenido de `git archive`; inspecciona el ZIP después de cambiar las exclusiones.

## Preparación y publicación de una versión

La versión actual pertenece a la serie `1.14.x`. Las notas del proyecto utilizan la convención propia `MAJOR.FOUNDRY.PATCH`; la compatibilidad efectiva se declara en `module.json`. Conserva el historial de versiones y utiliza una nueva etiqueta para cada publicación.

Procedimiento para preparar la siguiente release:

1. Prepara la release en una rama de trabajo desde `develop`: establece la versión en `module.json` y una entrada con esa misma versión y fecha en `CHANGELOG.md`; actualiza los enlaces del historial, ambos README y esta guía cuando corresponda.
2. Ejecuta las comprobaciones portables y las pruebas funcionales pertinentes. Revisa los enlaces y dependencias del manifiesto y las exclusiones de distribución descritas arriba.
3. Confirma los cambios, construye desde ese commit con el árbol limpio e inspecciona el contenido del ZIP.
4. Integra los cambios revisados en `develop` y después en `main`. Comprueba que el commit que vas a etiquetar contiene los archivos validados; si la integración modifica su contenido, repite las comprobaciones afectadas y la construcción.
5. Crea una etiqueta anotada `v<version>` en el commit validado de `main`. Comprueba que coincide exactamente con `module.json.version` antes de subirla.
6. Sube la rama y la etiqueta cuando corresponda publicar. El push de un tag `v*` dispara el workflow de release.
7. Revisa el borrador generado: versión, notas, ZIP y `module.json` adjunto. El manifiesto adjunto debe coincidir con el incluido en el ZIP.
8. Publica el borrador después de comprobar sus archivos y el acceso a las URLs de instalación y descarga. Coordina el manifiesto estable con la release disponible.

El [workflow actual](.github/workflows/release.yml) extrae el commit etiquetado, prepara Python 3.11, construye el ZIP y adjunta el alias sin versión y `module.json` a una **release en borrador**, con notas automáticas.

Actualmente no ejecuta la suite Node, no compara tag y versión y no hay un workflow de validación para PR o push ordinarios. Las comprobaciones anteriores deben realizarse antes de subir el tag hasta que se incorporen a CI.

El manifiesto de instalación apunta a `main/module.json` y la descarga al alias de la última release. Adelantar la versión del manifiesto estable a una release aún no publicada puede desincronizarlos; la homogeneización del proceso de publicación deberá resolver esa coordinación.

## Diagnóstico

| Síntoma | Comprobación |
|---|---|
| El compendio aparece en inglés | Producto oficial, Babele y traducción activos; idioma español; recarga del mundo |
| Error al consultar `core.language` | Mantener la lectura del idioma en `setup`; ejecutar las pruebas de registro |
| Falta un convertidor | Revisar nombre en el mapping, exportación/importación y registro en `scripts/converters.js` |
| Una copia importada mantiene texto anterior | Compararla con la entrada actual del compendio; no esperar sincronización automática |
| El builder rechaza el árbol de trabajo | Revisar `git status --short` y confirmar o apartar deliberadamente los cambios pendientes |
| El ZIP contiene archivos de desarrollo | Revisar lo versionado y las reglas `export-ignore`; `.gitignore` por sí solo no limpia el archivo |
