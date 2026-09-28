# Plantilla y procedimiento de homogeneización

Versión de la plantilla: **2**. Piloto: `translate-dnd5e-phb-2024-es`. La revisión completa de la base común está fijada en `fuentes-comunes.json`. La versión 2 incorpora perfiles por proyecto y SHA-256 de los artefactos; la versión 1 permanece en el historial.

Este directorio permite preparar la adopción en otro proyecto sin modificarlo automáticamente. Las comprobaciones locales del piloto están realizadas; la ejecución remota de CI, la publicación y las pruebas funcionales en Foundry siguen pendientes. Una adopción no hereda esas verificaciones.

## Material reutilizable

| Material | Uso |
|---|---|
| `plantillas/README.md.template`, `README.en.md.template` | Estructura de uso equivalente en español e inglés |
| `plantillas/DEVELOPER.md.template` | Procedimiento técnico, particularidades y límites de validación |
| `plantillas/CHANGELOG.md.template` | Cabecera y categorías; conservar el historial y sus enlaces |
| `plantillas/validate.yml.template`, `release.yml.template` | Workflow de pruebas/construcción y consumidor de sus artefactos |
| `plantillas/ADOPCION.md.template` | Registro por proyecto de base, adaptaciones, commits y comprobaciones |
| `fuentes-comunes.json` | Inventario de configuración, constructor y pruebas en el commit base, con SHA-256 de sus bytes versionados |

Las plantillas llevan el sufijo `.template`: no son documentos finales ni workflows activos. Copia cada una a una carpeta temporal ignorada del proyecto de destino y sustituye sus marcadores `__NOMBRE__` antes de instalarla en la ruta definitiva. El registro de adopción se guarda en `dev-tools/homogeneizacion/ADOPCION.md`, excluido del paquete instalable.

Los archivos comunes se obtienen del commit base, no de un checkout mutable. Para consultar uno desde el clon de PHB, usa el campo `source_commit` del inventario:

```sh
git show <source_commit>:.editorconfig
git show <source_commit>:dev-tools/buildScripts/build_release.py
```

No uses `git archive` para extraer estas herramientas: las reglas de distribución las excluyen. Para obtener sus bytes sin conversiones de PowerShell, ejecuta desde PHB este ejemplo, cambiando la ruta de origen y el nombre de salida según el inventario:

```python
from pathlib import Path
import json
import subprocess

source = "dev-tools/buildScripts/build_release.py"
revision = json.loads(Path("dev-tools/homogeneizacion/fuentes-comunes.json").read_text(encoding="utf-8"))["source_commit"]
payload = subprocess.check_output(["git", "show", f"{revision}:{source}"])
target = Path("tmp/homogeneizacion/build_release.py")
target.parent.mkdir(parents=True, exist_ok=True)
with target.open("xb") as output:
    output.write(payload)
```

El modo `xb` impide sobrescribir una extracción anterior. El constructor y sus pruebas exigen `LICENSE.md`, ambos README, contenido en `compendium/`, `lang/` y `scripts/` y repositorio GitHub. Un archivo `dev-tools/buildScripts/release-profile.json` permite declarar `archive_name`, `manifest_channel` (`latest` o `main`) y `variant` (`standard` o `text-only`). Sin perfil se aplican los valores del piloto. Tomb requiere además su adaptador `text_only.py`, que debe mantenerse y probarse en su repositorio.

La suite común tiene 24 pruebas. Los workflows conservan ambos ZIP, manifiesto y `SHA256SUMS.txt`, y verifican todos sus hashes antes de preparar un borrador. La llamada reutilizable acepta una revisión explícita; DM conserva además la ejecución manual y el canal de prerelease. La plantilla de release corresponde al canal estable: aplica esas opciones propias de DM al adaptarla.

## Parámetros de las plantillas

| Marcador | Fuente o decisión |
|---|---|
| `__PRODUCTO_ES__`, `__PRODUCT_EN__` | Nombre y alcance del producto traducido |
| `__MODULE_ID__`, `__VERSION__` | Identidad y versión del manifiesto del destino; conservar `sdr2` |
| `__REPOSITORY_URL__` | URL canónica del repositorio sin barra final |
| `__MANIFEST_URL__` | Canal de instalación realmente publicado o transición documentada |
| `__ESTADO_ES__`, `__STATUS_EN__` | Cobertura y revisión acreditadas, con las mismas limitaciones |
| `__REQUISITOS_ES__`, `__REQUIREMENTS_EN__` | Tablas equivalentes tomadas del manifiesto; diferenciar mínimo y verificado |
| `__ACTIVACION_ES__`, `__ACTIVATION_EN__` | Módulos, idioma y recarga según el runtime del destino |
| `__ALCANCE_ES__`, `__SCOPE_EN__` | Compendios y variante distribuida |
| `__LIMITACIONES_ES__`, `__LIMITATIONS_EN__` | Límites reales y pruebas pendientes |
| `__LICENCIA_CREDITOS_ES__`, `__LICENSE_CREDITS_EN__` | Licencia y atribuciones propias de ese proyecto |
| `__ENTORNO__`, `__ESTRUCTURA__`, `__CONVERTIDORES__` | Entorno contrastado, rutas y nombres reales |
| `__FUENTES_PRIVADAS__`, `__PRUEBAS_FOUNDRY__`, `__PARTICULARIDADES__` | Dependencias locales, alcance funcional y excepciones |
| `__NODE_TEST_COMMAND__`, `__PYTHON_TEST_COMMAND__` | Comandos portables previamente ejecutados en un clon aislado |
| `__BUILD_SCRIPT__` | Entrada del constructor con interfaz `--dist`, `--ref`, `--release-tag` |
| `__ASSET_NAME__` | Nombre real del ZIP adjunto, incluida extensión; comprobar contra `download` |
| `__PUBLICACION__` | Orden y canal propios de publicación, con transición de clientes antiguos |
| `__HISTORIAL_EXISTENTE__` | Historial y enlaces originales, sin reescribir releases anteriores |
| `__BASE_COMMIT__` | Revisión completa de PHB usada para los archivos comunes |
| `__KIT_COMMIT__` | Revisión completa que contiene las plantillas utilizadas |
| `__ADAPTACIONES__`, `__VALIDACIONES__`, `__COMMITS_DESTINO__`, `__PENDIENTES__` | Evidencia concreta de la adopción |

En YAML, los comandos sustituidos deben ser escalares válidos; utiliza un bloque `run: |` si contienen varias líneas o caracteres que lo requieran. No sustituyas una suite ausente por `echo OK`: incorpora las pruebas necesarias o elimina el paso y documenta la carencia. Las expresiones `${{ ... }}` pertenecen a GitHub Actions y se conservan.

## Adopción por pasos

1. Revisa instrucciones locales, estado y ramas de destino. Conserva cambios existentes. Comprueba por separado `main` y `develop` antes de crear una rama desde `develop`; no fuerces su alineación ni sobrescribas trabajo ajeno.
2. Completa el registro de adopción con la revisión de las plantillas, el commit base y el perfil elegido. Inventaría manifiesto, documentación, contenido distribuido, comandos y dependencias de pruebas.
3. Adapta README ES/EN, DEVELOPER y CHANGELOG. Conserva licencias y atribuciones: no hay una plantilla de licencia común. En DM y Tomb el archivo ausente sigue requiriendo resolver la licencia de sus aportaciones.
4. Compara `.gitignore`, `.gitattributes` y `.editorconfig` con los archivos de la base. Fusiona reglas necesarias para el destino; no reformatees traducciones ni retires del índice archivos sin revisar su uso y conservar los datos locales que correspondan.
5. Adapta el constructor y sus pruebas. Comprueba identidad, versión, tag, URLs, manifiesto interno/externo, lista de archivos y conservación de artefactos ante fallos. Mantén las transformaciones del perfil de destino.
6. Renderiza los workflows con sus comandos y nombre de adjunto. Valida sintaxis y expresiones con actionlint y prueba los comandos localmente. Las pruebas portables deben funcionar sin Foundry, módulos hermanos ni fuentes privadas; las comprobaciones de integración se identifican por separado.
7. Revisa todos los marcadores antes de versionar los archivos finales. Desde la raíz del destino, adapta esta búsqueda a las rutas presentes:

   ```sh
   rg -n '__[A-Z][A-Z0-9_]*__' README.md README.en.md DEVELOPER.md CHANGELOG.md .github/workflows dev-tools/homogeneizacion/ADOPCION.md
   git diff --check
   ```

   La búsqueda no debe devolver marcadores pendientes; su código 1 significa que no encontró coincidencias. No la ejecutes sobre las plantillas fuente, que los contienen intencionadamente.
8. Divide los cambios en commits por responsabilidad. Construye desde el commit final, compara el inventario del ZIP y verifica que plantillas, registros y pruebas quedan excluidos. Registra resultados, omisiones y los commits del destino.
9. Tras subir la rama, comprueba CI en GitHub. Completa las pruebas en Foundry y la coordinación de publicación antes de declarar terminada la adopción. No crees tags ni publiques solo por haber generado la plantilla.

## Perfiles y excepciones conocidas

Orden propuesto: MM, SRD, Tasha, DM, Phandelver y Tomb. Revalida los hallazgos en cada adopción; esta tabla procede de la auditoría local, no garantiza el estado futuro.

| Destino | Adaptación necesaria |
|---|---|
| MM | Conservar convertidores `mm2024`; resolver el import de Babele desde una carpeta hermana; unificar los constructores Python/PowerShell/Bash y excluir pruebas del ZIP. Conservar Apache 2.0. |
| SRD | Conservar el ID `translate-dnd5e-sdr2-es` y sus atribuciones CC BY 4.0. Coordinar cualquier renombrado de `LICENSE`. Excluir contadores/generadores y no usar un comodín de pruebas que ejecute generadores de contenido. |
| Tasha | Conservar Apache 2.0, convertidores `tcoe` y el alias histórico `translate-dnd5e-tashas-cauldron-es.zip`. Declarar su base en `archive_name`, además de `__ASSET_NAME__` en los workflows. Revisar la discrepancia histórica de tag y manifiesto. |
| DM | Conservar los cambios locales previos, el canal preliminar y las pruebas con originales. Resolver la licencia ausente y separar las pruebas privadas; no adoptar automáticamente el canal estable del piloto. |
| Phandelver | Conservar las herramientas Adventure y su constructor con pruebas. Integrar controles equivalentes sin reemplazarlo a ciegas. Incluir README EN en exclusiones/lista de admitidos, corregir changelog y separar la prueba con fuentes privadas. |
| Tomb | Mantener el constructor de solo texto, las 47 sustituciones de rutas y su hash. Completar licencia y README EN. Hacer reproducible la entrada por commit y adaptar la interfaz de CI; el constructor de PHB no es un reemplazo de `build_light.py`. |

## Mantener las copias sincronizadas

La versión 2 usa copias revisadas con procedencia registrada. No es un workflow central desplegado ni un sistema de sincronización automática.

Para incorporar una mejora de PHB, selecciona un commit nuevo y compara los archivos de la base registrada con esa revisión mediante `git diff <base-anterior> <base-nueva> -- <rutas>` en el clon de PHB. Aplica únicamente los cambios pertinentes en una rama del destino, preserva sus adaptaciones y ejecuta sus pruebas. Actualiza la base del registro solo para los archivos realmente sincronizados; anota revisiones distintas por archivo si la actualización es parcial.

Los SHA-256 de `fuentes-comunes.json` se calculan sobre `git show <base>:<ruta>`, sin conversiones de finales de línea del checkout. Sirven para identificar la fuente exacta; las diferencias del destino se revisan y justifican en el registro, no se borran para igualar hashes. Al cambiar el contrato compartido, crea una nueva revisión del kit, renueva el inventario y describe su impacto sobre cada perfil.
