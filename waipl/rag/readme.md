# RAG — Dominio A (Will App)

Registro canónico del ciclo de control del conocimiento del ecosistema WAIPL.

- `knowledge_register.json` — estado de cada unidad de conocimiento:
  `Borrador → En revisión → { Aprobado | Pendiente confirmación humana |
  Aprobado con restricciones | Rechazado | Bloqueado }`.
- El gate es **DIKE (RGL-01)**: sin su dictamen nada transiciona a Aprobado
  (hiperarista `dike_compliance_gate` en Graphify).
- **Vár (VAC-01)** valida la coherencia factual de los dictámenes.
- Orquestación: `waipl/core/rag_pipeline.py` (único punto de escritura de este registro).
