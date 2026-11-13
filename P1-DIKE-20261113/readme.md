# P1-DIKE-20261113 — Paquete de evidencias

**Estado:** P1 ABIERTO — pendiente de aceptación de Carla.
**Fecha:** 2026-11-13.
**Responsable:** AutoClaw, operador del nodo Windows.

## Contenido

- `Informe_P1_DIKE_2026-11-13.docx` — informe de ejecución y evidencias.
- `informe_p1_dike_2026-11-13.md` — misma información en Markdown.
- `p1_evidence_manifest.json` — manifiesto estructurado de la ejecución.
- `p1_nine_files_hashes.csv` — hashes antes/después de los 9 documentos históricos.
- `PACKAGE-HASHES.csv` — hashes de todos los archivos de este paquete.
- `logs/` — pruebas unitarias, dry-run, aplicación, prueba funcional, regresión, diff, hashes iniciales/finales.
- `originals/` — copia de los 9 documentos históricos y de la fuente activa antes del parche.
- `after_patch/` — fuente activa parcheada y copia `.before-p1-crlf-lf.bak`.
- `kit/` — kit P1 usado, restaurado desde `main` de `Will-App-WAIPL-RAG` (PR #6, merge `966a8ca`).

## Nota de ejecución

El Python embebido de AutoClaw no añade el directorio del script a `sys.path`. Por eso se usó un runner mínimo que inserta la ruta del kit y carga las cinco pruebas existentes; el kit no se modificó.

## Resultado

- 5/5 pruebas unitarias Windows: PASS.
- Dry-run: `DRY_RUN_OK`.
- Aplicación: `PATCH_APPLIED_VERIFIED`.
- Fuente activa: `C:\Users\USER\Desktop\AutoClaw\waipl\agents\dike_auditora.py`.
- SHA-256 antes: `2471a5dda3953bdd05e05b378534a9e085dfb853d4cd3addf72453d84808d335`.
- SHA-256 después: `f5f7357aba45b6f8e2f2336816845b27514f03d3a0717c5f09c5cfe1bf6acdd9`.
- Prueba funcional Windows LF/CRLF: PASS.
- Regresión del gate: 44/44.
- Los 9 documentos históricos no fueron reescritos; sus hashes físicos y LF permanecen idénticos.

## Límites

- No se tocó `_HISTORICO-MASTER`, Vár, Gate HMAC, secretos, receipts, SENTINEL ni SCI.
- No se creó PR nueva ni se publicó en `main`; el cambio queda en el working tree para revisión de Carla.
- No consta un log Linux separado en el kit ni en el PR #6; no se inventa esa evidencia.
- P1 no se declara cerrado.
