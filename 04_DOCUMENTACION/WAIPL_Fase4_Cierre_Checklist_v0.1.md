# WAIPL / Will App — Fase 4
## Checklist de cierre v0.1

### Infraestructura real
- [ ] PostgreSQL operativo
- [ ] pgvector operativo
- [ ] versión PostgreSQL registrada
- [ ] versión pgvector registrada
- [ ] embedding model/dimension registrados

### Fase 3
- [ ] 32/32 ejecutados realmente
- [ ] persistencia/restart comprobados
- [ ] concurrencia/idempotencia comprobadas
- [ ] gobernanza de estados comprobada
- [ ] provenance/multimodal comprobados

### Fase 4
- [ ] T01–T25 ejecutados realmente
- [ ] T15–T19 ejecutados contra PostgreSQL + pgvector reales
- [ ] NO_EVIDENCE probado
- [ ] PARTIAL probado
- [ ] CONTRADICTORY probado
- [ ] leakage probado
- [ ] versionado probado
- [ ] deduplicación probada
- [ ] provenance probado
- [ ] grounding probado

### Regresión
- [ ] Graphify 34/34
- [ ] Kairos 28/28
- [ ] DIKE 40/40
- [ ] Knowledge Model 42/42
- [ ] Ingestion 57/57
- [ ] Smoke 21/21
- [ ] Fase 3 32/32
- [ ] Fase 4 25/25

### Evidencia
- [ ] INPUT / EXPECTED / ACTUAL / RESULT por test
- [ ] logs conservados
- [ ] hashes conservados
- [ ] commit probado identificado
- [ ] entorno identificado
- [ ] no hay SKIP contabilizados como PASS

### Estado final
- [ ] IMPLEMENTED
- [ ] TESTED
- [ ] OPERATIVE IN SIMULATION
- [ ] INTEGRATED
- [ ] APPROVED
- [ ] DEPLOYED
- [ ] PRODUCTION

Cada estado debe estar respaldado por evidencia específica. No se presupone el siguiente estado por haber alcanzado el anterior.
