# PR Review Checklist — Integración Super Plantilla v3.0

Antes de aprobar el PR, confirmar lo siguiente:

- [ ] graph.json: campo `integrated` = true
  - [ ] `integrated_at` presente y con timestamp ISO
  - [ ] `integrated_by` = "wmejiasbcn-tech"
  - [ ] nota de provenance incluida en `integration_note`

- [ ] 00_SISTEMA/PR_DESCRIPTION_CIERRE_INSPECCION.md: contenido consistente con la directiva.
- [ ] 00_SISTEMA/CHECKLISTS/: checklists añadidos y no destructivos.
- [ ] No hay modificaciones no autorizadas en archivos marcados EN_CURSO.
- [ ] Todas las referencias a la Super Plantilla v3.0 y Prompting 2026 aparecen en los metadatos.
- [ ] Confirmar revisores asignados: Ariadna, Sylvia Bloom, Nova, Will, Carla.
- [ ] Confirmar que el PR tiene etiqueta `governance` y `high-priority` (recomendado).

Criterio de aceptación:
- Cumplir todos los checks anteriores o documentar excepciones en el PR.
