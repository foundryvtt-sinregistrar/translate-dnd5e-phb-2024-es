# PHB PDF terminology audit

This directory contains the reproducible terminology audit used to compare the
Foundry translation with the official Spanish Player's Handbook PDFs.

The PDFs are local reference material and are never copied into generated
reports. The audit preserves Foundry macros and checks only visible text.

Run from the repository root:

```powershell
python dev-tools/pdf-audit/audit_phb_translation.py `
  --json dev-tools/pdf-audit/reports/phb-pdf-audit.json `
  --markdown dev-tools/pdf-audit/reports/phb-pdf-audit.md
```

Install `pypdf` to include PDF extraction statistics. Structural, reference and
terminology checks do not otherwise require third-party dependencies.

Apply only the high-confidence mappings recorded in `official-terms.es.json`:

```powershell
python dev-tools/pdf-audit/normalize_official_terms.py --write
```

The normalizer preserves macro keys and inline rolls. It may update the visible
label attached to a macro when that label uses deprecated terminology.

Synchronize translations embedded in example actors with their canonical class
and origin entries:

```powershell
python dev-tools/pdf-audit/sync_embedded_translations.py --write
```
