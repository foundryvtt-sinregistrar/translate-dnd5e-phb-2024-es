# Informe de revisión del PHB 2024 mediante los PDF oficiales

## Objetivo

Revisar la traducción de `translate-dnd5e-phb-2024-es` utilizando como fuente
terminológica los PDF españoles del Manual del Jugador 2024, sin modificar los
identificadores ni la estructura documental de Foundry VTT.

La revisión se ejecutó sobre la rama `develop`. Los PDF y demás materiales de
referencia de `dev-tools/export/_data` se mantuvieron fuera de Git.

## Corpus examinado

- PDF procesados: 384.
- Caracteres extraídos: 1.277.520.
- PDF sin capa de texto aprovechable: 12.
- Compendios examinados: 8.
- Entradas inglesas y españolas comparadas: 1.548 por idioma.
- Referencias internas `UUID` y `Embed` verificadas: 3.298.

La extracción se utilizó únicamente para búsquedas y comprobaciones. El texto
completo del libro no se incorporó a los informes ni al repositorio.

## Línea base

La estructura ya estaba completa antes de esta revisión: todos los identificadores
de las entradas inglesas tenían una entrada española correspondiente. Sin embargo,
se detectaron los siguientes problemas de calidad:

- 74 residuos visibles de los términos ingleses inicialmente auditados.
- 79 apariciones de variantes españolas incompatibles con la edición oficial.
- Campos de progresión y condiciones completamente en inglés dentro de actores.
- Tablas de reglas y etiquetas parciales sin traducir.
- 114 macros `Reference` que habían perdido su clave entre corchetes.
- Nombres de actividades de Foundry mezclados en inglés y español.
- Listas de competencias de clase conservadas en inglés.
- Uso de `Tiflin`, `Aterrorizado`, `Atemorizado` y `Restringido` como términos
  mecánicos, en lugar de las formas documentadas en el PDF.

## Criterios terminológicos

Se adoptaron como formas canónicas, entre otras:

| Inglés | Forma canónica |
|---|---|
| Tiefling | tiefling |
| Frightened | Asustado |
| Restrained | Apresado |
| Blinded | Cegado |
| Charmed | Hechizado |
| Grappled | Agarrado |
| Poisoned | Envenenado |
| Prone | Derribado |
| Stunned | Aturdido |
| Unconscious | Inconsciente |
| Bonus Action | Acción adicional |
| Long Rest | Descanso largo |

También se normalizaron las dieciocho competencias y `Herbalism Kit`. Se mantuvo
`Dungeon Master`, ya que esa es la denominación empleada por la edición española.

## Cambios realizados

### Infraestructura de auditoría

- Se añadió un glosario pequeño y verificable basado en el PDF.
- Se creó una auditoría estructural, terminológica y de referencias.
- Se añadieron estadísticas opcionales de extracción PDF mediante `pypdf`.
- Se generaron informes JSON y Markdown reproducibles.
- Se añadió detección de campos probablemente ingleses y macros malformadas.

### Normalización terminológica

- Se normalizaron 145 cadenas en el primer lote de términos oficiales.
- Se tradujeron condiciones inglesas visibles sin modificar las claves de macro.
- Se sustituyó `Tiflin` por `tiefling`.
- Se unificaron las variantes de la condición Asustado.
- Se normalizaron Apresado, acciones, competencias y herramientas.

### Actores y contenido incrustado

- Se sincronizaron las progresiones de personajes de ejemplo con las entradas
  canónicas de clases y orígenes.
- Se corrigieron progresiones de brujo, aasimar y varios trasfondos.
- Se tradujeron Daño en grupo y las condiciones de los elementales conjurados.
- Se sincronizaron el dracónido, Arma de aliento y Bolas de rodamiento.

### Clases y actividades

- Se tradujo por completo la automatización de Explosión repelente.
- Se normalizaron nombres visibles de actividades, entre ellos Golpe de ráfaga,
  Paso del viento, Chispa divina, pasos feéricos y actividades de familiares.
- Se tradujeron etiquetas de salvaciones y restauración de espacios de conjuro.

### Conjuros

- Se tradujeron las formas animales de Encontrar familiar.
- Se tradujeron pies de tabla de los espíritus invocados.
- Se normalizaron las unidades visibles de esas tablas.
- Se corrigieron etiquetas de Puntos de Golpe y Ráfaga de viento.

### Contenido y reglas

- Se tradujeron las tablas de Influencia, necesidades de comida y agua,
  capacidad de carga y costes de pergaminos.
- Se tradujeron tipos de criatura, tamaños, áreas de efecto y peligros.
- Se sincronizaron las etiquetas de la lista de equipo con el compendio canónico.
- Se eliminaron anotaciones inglesas redundantes del glosario.

### Reparación de macros

Se restauraron 114 macros `Reference` utilizando las claves y el orden del JSON
inglés correspondiente:

- 47 macros en clases.
- 67 macros en contenido.

La única discrepancia de recuento fue Resiliencia enana. El origen inglés tenía
`Poisoned` como texto normal y la traducción contenía una macro vacía. Se resolvió
explícitamente como `Reference[Poisoned]` con la etiqueta `Envenenado`.

## Commits del proceso

| Commit | Descripción |
|---|---|
| `acc298d` | Añade la auditoría terminológica basada en PDF. |
| `815d1f9` | Alinea la terminología principal con el PHB español. |
| `6d96088` | Repara textos incrustados en actores y clases. |
| `5f5d82a` | Traduce etiquetas residuales y tablas de conjuros. |
| `880a78a` | Traduce tablas de reglas y etiquetas en línea. |
| `b730baf` | Sincroniza etiquetas del equipo en los diarios. |
| `c804413` | Restaura macros y secciones del glosario. |
| `99770f5` | Normaliza nombres de actividades de Foundry. |
| `ebb53a4` | Estandariza competencias y herramientas. |

## Validación final

| Comprobación | Resultado |
|---|---:|
| Entradas españolas ausentes | 0 |
| Entradas españolas adicionales | 0 |
| Referencias internas inválidas | 0 |
| Macros `Reference` malformadas | 0 |
| Residuos del glosario inglés auditado | 0 |
| Terminología española obsoleta auditada | 0 |
| Campos probablemente ingleses | 0 |
| Archivos JSON inválidos | 0 |

Todos los normalizadores son idempotentes: una segunda ejecución produce cero
cambios.

## Limitaciones y trabajo futuro

- Doce páginas ilustradas no tienen texto extraíble y requerirían OCR si se desea
  auditar sus rótulos gráficos.
- La detección automática no sustituye una corrección editorial frase por frase.
- El registro de cambios incluido en el compendio contiene nombres técnicos de
  versiones antiguas de Foundry; algunos se conservan para poder identificar los
  objetos y actividades a los que se refieren.
- Las traducciones de nombres propios y términos de ambientación deben mantenerse
  según la grafía oficial aunque coincidan con el inglés.
- Una actualización futura del módulo oficial debe comenzar ejecutando la auditoría
  estructural antes de reutilizar estas correcciones.

## Reproducción

Desde la raíz del repositorio:

```powershell
python dev-tools/pdf-audit/normalize_official_terms.py --write
python dev-tools/pdf-audit/sync_embedded_translations.py --write
python dev-tools/pdf-audit/normalize_residual_labels.py --write
python dev-tools/pdf-audit/repair_reference_macros.py --write
python dev-tools/pdf-audit/audit_phb_translation.py `
  --json dev-tools/pdf-audit/reports/phb-pdf-audit.json `
  --markdown dev-tools/pdf-audit/reports/phb-pdf-audit.md
```
