# Permisos
# chmod +x dev-tools/buildScripts/build-zip.sh
# Ejecucion desde la raiz el proyecto
# ./dev-tools/buildScripts/build-zip.sh

#!/usr/bin/env bash
set -euo pipefail

# Run from repo root (or auto-cd to repo root)
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

MODULE_JSON="module.json"
if [[ ! -f "$MODULE_JSON" ]]; then
  echo "ERROR: No se encuentra $MODULE_JSON en la raíz del repo."
  exit 1
fi

# Parse id + version (sin jq, compatible)
MOD_ID="$(node -p "require('./module.json').id" 2>/dev/null || true)"
MOD_VER="$(node -p "require('./module.json').version" 2>/dev/null || true)"

if [[ -z "${MOD_ID}" || -z "${MOD_VER}" ]]; then
  echo "ERROR: No se pudo leer id/version de module.json (¿tienes Node instalado?)."
  echo "Solución: instala Node o adapta el script para usar jq."
  exit 1
fi

DIST_DIR="dist"
mkdir -p "$DIST_DIR"

ZIP_NAME="${MOD_ID}-${MOD_VER}.zip"
ZIP_PATH="${DIST_DIR}/${ZIP_NAME}"

echo "Building clean zip: $ZIP_PATH"
git archive --format=zip --prefix="${MOD_ID}/" -o "$ZIP_PATH" HEAD

echo "OK: $(ls -lh "$ZIP_PATH" | awk '{print $5 "  " $9}')"