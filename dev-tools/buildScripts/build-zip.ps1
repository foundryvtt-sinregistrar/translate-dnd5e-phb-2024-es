# Ejecucion desde la raiz el proyecto
# powershell -ExecutionPolicy Bypass -File .\dev-tools\buildScriptsºbuild-zip.ps1
#Requires -Version 5.1
$ErrorActionPreference = "Stop"

# Run from repo root (or auto-cd to repo root)
$repoRoot = (git rev-parse --show-toplevel).Trim()
Set-Location $repoRoot

$moduleJson = Join-Path $repoRoot "module.json"
if (-not (Test-Path $moduleJson)) {
  throw "No se encuentra module.json en la raíz del repo."
}

$module = Get-Content $moduleJson -Raw | ConvertFrom-Json
if (-not $module.id -or -not $module.version) {
  throw "module.json no contiene id/version."
}

$distDir = Join-Path $repoRoot "dist"
if (-not (Test-Path $distDir)) { New-Item -ItemType Directory -Path $distDir | Out-Null }

$zipName = "{0}-{1}.zip" -f $module.id, $module.version
$zipPath = Join-Path $distDir $zipName

Write-Host "Building clean zip: $zipPath"
git archive --format=zip --prefix="$($module.id)/" -o $zipPath HEAD | Out-Null

$fi = Get-Item $zipPath
Write-Host ("OK: {0:N2} MB  {1}" -f ($fi.Length/1MB), $fi.FullName)