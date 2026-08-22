Comando exacto: merge selectivo (solo lo necesario)
Desde main:
```
git checkout main
git pull origin main

# Trae solo lo imprescindible para release infra
git checkout develop -- \
  .gitattributes \
  .github/workflows/release.yml \
  dev-tools/buildScripts/build_release.py \
  CHANGELOG.md

git status
git commit -m "Release infra: workflow + build script + attributes + changelog"
git push origin main
```



proyecto open-source mantenible a largo plazo, con flujo profesional real.

Te estructuro todo en 4 bloques:

1️⃣ Convención de Versionado Oficial

Tu esquema ya es sólido:

MAJOR.FOUNDRY.PATCH

Ejemplo actual:

1.13.0

Significa:

1 → Versión estructural del módulo

13 → Compatible con Foundry v13

0 → Iteración interna

📌 Reglas futuras
Caso	Nueva versión
Corrección menor	1.13.1
Mejora sin romper estructura	1.13.2
Cambios estructurales internos	2.13.0
Compatibilidad Foundry 14	1.14.0
2️⃣ Convención de Commits Profesional

Usaremos estilo Conventional Commits, compatible con generación automática de changelog.

📘 Formato
type(scope): description
📦 Types permitidos
Tipo	Uso
feat	Nueva funcionalidad
fix	Corrección
refactor	Cambio interno sin modificar comportamiento
docs	Cambios en documentación
perf	Mejora de rendimiento
chore	Tareas internas
build	Cambios en packaging
compat	Cambios de compatibilidad Foundry
🔎 Ejemplos reales para tu proyecto
feat(normalization): add v7 structural title-case policy
fix(spells): preserve inline roll macros during translation
compat(foundry13): align module version with v13.x
docs(readme): add dual installation section
refactor(converters): stabilize mergeEffects handling
3️⃣ Generación Automática de Changelog

Con esto puedes generar changelog automáticamente en cada release.

Opción recomendada: semantic-release + conventional commits

Pero como proyecto Foundry, mejor algo más simple:

📦 Alternativa ligera: release workflow con GitHub Actions

Archivo: .github/workflows/release.yml

name: Release

on:
push:
tags:
- "v*"

jobs:
build:
runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            module.json
            README.md
            README.en.md
            Changelog.txt
4️⃣ Flujo Profesional de Release
🔹 Paso 1 — Actualizar versión

En module.json:

"version": "1.13.1"
🔹 Paso 2 — Actualizar Changelog

Mover cambios de [Unreleased] → nueva versión.

🔹 Paso 3 — Commit estructurado
chore(release): prepare v1.13.1
🔹 Paso 4 — Crear tag
git tag v1.13.1
git push origin v1.13.1

GitHub generará automáticamente la release.

5️⃣ Estructura Recomendada Final
translate-dnd5e-sdr2-es/
│
├── module.json
├── README.md
├── README.en.md
├── CHANGELOG.md
├── DEVELOPER.md
│
├── compendiums/
├── normalization/
├── scripts/
│
└── .github/
└── workflows/
└── release.yml
6️⃣ Estándar de Proyecto

Ahora tu módulo ya cumple:

✔ Versionado claro

✔ Changelog estándar

✔ Compatibilidad explícita

✔ Instalación dual

✔ Arquitectura documentada

✔ Preparado para CI/CD

✔ Escalable a Foundry 14

🚀 Siguiente Nivel (Opcional)

Podemos añadir:

🔁 Generación automática de ZIP en cada release

📦 Validación automática de module.json

🧪 Script de validación de macros antes de publicar

🔍 Script de comparación EN/ES previo a release

🏷 Badge dinámico de última versión