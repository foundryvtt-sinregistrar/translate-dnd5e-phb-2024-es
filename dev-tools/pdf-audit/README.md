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
