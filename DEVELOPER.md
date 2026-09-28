# Guía de desarrollo

Esta guía describe cómo mantener `translate-dnd5e-phb-2024-es` con las herramientas actuales del repositorio. Para instalar y utilizar el módulo, consulta [README.md](README.md) o [README.en.md](README.en.md).

## Entorno y compatibilidad

La versión declarada es **1.14.2**. [module.json](module.json) es la referencia para identidad, versión, compatibilidad, idiomas y archivos de entrada.

| Dependencia de ejecución | Mínima | Verificada |
|---|---|---|
| Foundry VTT | 14.367 | 14.368 |
| dnd5e | 6.0.0 | 6.0.3 |
| Babele | 2.9.1 | 2.9.1 |

El módulo oficial **Player's Handbook (2024)** (`dnd-players-handbook`) y Babele están declarados en `relationships.requires`. Para utilizar la traducción y hacer pruebas dentro de Foundry, instala y activa ambos y las dependencias de Babele. El producto oficial se adquiere e instala por separado.

La dependencia del producto oficial se declara por su ID y tipo, sin URL de descarga ni límites de versión. Foundry permite resolver una dependencia por su ID en el directorio de paquetes, según su [documentación de manifiestos](https://foundryvtt.com/article/module-development/). La copia local consultada durante esta homogeneización era la **2.2.0**; su presencia no acredita una versión mínima ni una versión verificada de la traducción. Añade esos límites solo cuando haya evidencia de compatibilidad y registra las versiones utilizadas en la comprobación funcional.

| Herramienta de desarrollo | Uso | Referencia de entorno |
|---|---|---|
| Git | Historial, revisión y construcción con `git archive` | Disponible en la terminal |
| Node.js | Pruebas con `node:test` | CI usa la serie 24; comprobadas localmente con 24.17.0 |
| Python | Validación JSON, construcción del ZIP y pruebas del constructor | CI usa 3.11; comprobadas localmente con 3.14.6 |

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
| `tests/test_build_release.py` | Pruebas del constructor con repositorios Git temporales |
| `dev-tools/buildScripts/build_release.py` | Construcción desde una referencia Git |
| `.github/workflows/validate.yml` | Pruebas y construcción para PR, pushes y releases |
| `.github/workflows/release.yml` | Validación y creación de una release en borrador al subir un tag |
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

Para cambios de empaquetado, ejecuta también la suite Python. Crea repositorios Git temporales y comprueba selección de commits, cambios locales, etiquetas, manifiestos, exclusiones y conservación de artefactos anteriores cuando falla una validación:

```sh
python -B -m unittest discover -s tests -p 'test_build_release.py' -v
```

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

### Validación automática en GitHub

[validate.yml](.github/workflows/validate.yml) se ejecuta en pull requests y pushes a cualquier rama. También acepta llamadas desde [release.yml](.github/workflows/release.yml) mediante un [workflow reutilizable de GitHub Actions](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

En un runner Ubuntu con Node 24 y Python 3.11:

1. Extrae el commit de la ejecución con su historial y etiquetas.
2. Ejecuta `node --test tests/*.test.mjs`.
3. Ejecuta `python -B -m unittest discover -s tests -p 'test_*.py' -v`.
4. Construye y valida el paquete desde ese commit. En releases añade `--release-tag` para comprobar la etiqueta, la versión y el changelog.
5. Guarda el ZIP sin versión y su manifiesto externo como artefacto `module-package`, disponible durante siete días para inspección.

Los pushes a tags `v*` entran por el workflow de release y llaman a esa misma validación. No crean una segunda ejecución independiente de `Validate` para el tag. En una pull request, las comprobaciones usan el commit de integración preparado por GitHub.

La validación tiene permisos de lectura del repositorio. Las nuevas ejecuciones de validación de una misma referencia sustituyen a las anteriores en curso; las releases de un mismo tag se serializan sin cancelar la ejecución activa. Si una comprobación falla, no se crea el borrador de release.

Los workflows quedan activos en GitHub al subir estos cambios. Hacer obligatorio el resultado para fusionar una pull request requiere configurar por separado las reglas de protección del repositorio. La CI ejecuta las comprobaciones portables y de empaquetado; las pruebas funcionales en Foundry siguen siendo una revisión aparte.

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

El [constructor](dev-tools/buildScripts/build_release.py) resuelve `--ref` a un commit y utiliza `git archive`. Tanto los metadatos como los archivos proceden de ese mismo commit. Para construir la versión del checkout, confirma los cambios que quieras incluir y comprueba que el árbol esté limpio:

```sh
git status --short
python dev-tools/buildScripts/build_release.py --dist dist --ref HEAD
```

Con el identificador y la versión actuales genera:

- `dist/translate-dnd5e-phb-2024-es-1.14.2.zip`.
- `dist/translate-dnd5e-phb-2024-es.zip`.
- `dist/module.json`.

Los dos ZIP son copias idénticas y contienen una carpeta raíz `translate-dnd5e-phb-2024-es/`. El manifiesto externo es una copia exacta del incluido en el ZIP; el workflow adjunta ese archivo de `dist/`.

Puedes seleccionar otro commit o tag con `--ref` sin cambiar el checkout. El nombre del ZIP y el manifiesto se obtienen de la referencia seleccionada. `--allow-dirty` permite una previsualización del contenido confirmado aunque haya cambios locales: no incorpora modificaciones del índice, del árbol de trabajo ni archivos sin seguimiento. Para preparar releases, utiliza el árbol limpio.

Al seleccionar un tag, se exige que sea `v<version>` y que exista una entrada de esa versión en `CHANGELOG.md`. Si construyes por SHA, usa además `--release-tag v<version>` para comprobar que esa etiqueta coincide con la versión y apunta al commit elegido. El workflow utiliza esta opción.

`--no-alias` omite el ZIP sin versión. `--name` cambia solamente la base del nombre de los ZIP: la carpeta interna conserva el identificador del módulo. Estas opciones no eliminan artefactos de ejecuciones anteriores.

Antes de reemplazar archivos de salida, el constructor valida en un directorio temporal:

- Estructura e integridad del ZIP, sin rutas anómalas ni enlaces simbólicos.
- Presencia de `module.json`, ambos README, `CHANGELOG.md` y `LICENSE.md`.
- Contenido limitado a esos archivos y a `compendium/`, `lang/` y `scripts/`.
- Sintaxis de todos los JSON y presencia de scripts e idiomas declarados.
- Coincidencia del manifiesto empaquetado con el del commit, permitiendo diferencias de finales de línea LF/CRLF; el manifiesto externo se copia del ZIP sin modificaciones.

Una referencia histórica que incluya archivos ajenos a esa lista no supera las comprobaciones. Si la validación falla, los artefactos existentes se conservan.

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
5. Crea una etiqueta anotada `v<version>` en el commit validado de `main`. Construye con `--ref` apuntando a esa etiqueta para comprobar su versión y la entrada de changelog antes de subirla.
6. Sube la rama y la etiqueta cuando corresponda publicar. El push de un tag `v*` dispara el workflow de release.
7. Revisa el borrador generado: versión, notas, ZIP y `module.json` adjunto. El manifiesto adjunto debe coincidir con el incluido en el ZIP.
8. Publica el borrador después de comprobar sus archivos y el acceso a las URLs de instalación y descarga. Coordina el manifiesto estable con la release disponible.

El [workflow de release](.github/workflows/release.yml) llama a la validación compartida con el tag de la publicación. Una vez superadas las pruebas y la construcción, otro job descarga el artefacto `module-package` de esa misma ejecución y adjunta el alias sin versión y `dist/module.json` a una **release en borrador**, con notas automáticas. Ese job consume los archivos ya validados, sin reconstruirlos, y es el único que recibe permiso de escritura sobre el repositorio.

La release queda bloqueada si fallan las suites Node/Python, la relación entre tag, commit y versión, la validación del paquete o la descarga de sus artefactos. La falta de cualquiera de los dos adjuntos también impide completar el job de publicación. El borrador requiere una revisión antes de publicarlo.

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
