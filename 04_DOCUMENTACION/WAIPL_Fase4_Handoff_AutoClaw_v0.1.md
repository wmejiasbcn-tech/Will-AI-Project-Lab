# WAIPL / Will App
# FASE 4 — HANDOFF AUTOCLAW v0.1

Fecha: 2026-09-09
Estado: PREPARADO PARA REANUDACIÓN

## CONTEXTO

AutoClaw quedó detenido por falta de crédito durante la preparación/validación de infraestructura PostgreSQL. No debe reiniciarse desde cero.

## LO YA CERRADO

- Fase 4 conceptualmente auditada.
- 14 requisitos coherentes.
- Contratos de Query Analysis, Governed Retriever, Reranker, Evidence Assessment y Context Builder definidos.
- Reglas de provenance, grounding, anti-leakage, versionado y deduplicación definidas.
- Matriz T01–T25 definida.
- Fase 1: 42/42 en la ejecución reciente de AutoClaw.
- Fase 2: 57/57 en la ejecución reciente de AutoClaw.
- Documento canónico de Fase 4 persistido en `main`.

## LO QUE NO DEBE DECLARARSE CERRADO

- PostgreSQL + pgvector real en la ejecución bloqueada actual.
- T15–T19 sobre infraestructura real.
- Fase 3 actual 32/32.
- Fase 4 actual 25/25.
- Regresión completa actual.

## REANUDACIÓN EXACTA

1. Instalar/iniciar PostgreSQL real.
2. Verificar pgvector.
3. Ejecutar Fase 3 completa y conservar evidencia.
4. Ejecutar T15–T19 sobre infraestructura real.
5. Ejecutar T01–T25.
6. Ejecutar regresión completa.
7. Generar informe de cierre con resultados ACTUAL/EXPECTED, logs y hashes.

## REGLAS

- No sustituir infraestructura real por mocks para declarar cierre.
- `SKIP` no equivale a `PASS`.
- `BLOCKED` no equivale a `PASS`.
- No modificar la arquitectura conceptual para resolver el bloqueo de infraestructura.
- No crear una arquitectura RAG paralela.
- No introducir campos históricos como requisitos canónicos sin verificar el esquema real.
- Gobernanza antes de similitud.
- No evidencia no autoriza fabricación.
- Context Builder closed-world.

## DOCUMENTOS DE REFERENCIA

`04_DOCUMENTACION/WAIPL_Fase4_Auditoria_y_Paquete_Canonico_v0.1.md`
`04_DOCUMENTACION/WAIPL_Fase4_Runbook_Ejecucion_y_Cierre_v0.1.md`
`04_DOCUMENTACION/WAIPL_Fase4_Casos_Canonicos_y_Criterios_v0.1.md`

## CRITERIO DE CIERRE

No elevar Fase 4 a INTEGRATED/APPROVED/DEPLOYED/PRODUCTION sin evidencia técnica correspondiente.
