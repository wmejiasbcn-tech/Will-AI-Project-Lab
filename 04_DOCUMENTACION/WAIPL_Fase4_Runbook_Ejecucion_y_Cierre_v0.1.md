# WAIPL / Will App
# FASE 4 — RUNBOOK DE EJECUCIÓN Y CIERRE v0.1

Fecha: 2026-09-09
Ámbito: Knowledge + Content / RAG
Naturaleza: documento operativo de preparación; no ejecuta pruebas ni sustituye evidencia técnica.

## 1. OBJETIVO

Dejar preparada la ejecución final de Fase 4 para que, cuando exista infraestructura PostgreSQL + pgvector operativa, la ejecución sea determinista, trazable y no requiera reinterpretar la arquitectura.

Este runbook NO modifica la implementación de AutoClaw.

## 2. ORDEN DE EJECUCIÓN

1. Confirmar PostgreSQL operativo.
2. Confirmar pgvector operativo.
3. Ejecutar Fase 3 completa: 32/32 reales.
4. Ejecutar T15–T19 de Fase 4 contra infraestructura real.
5. Ejecutar T01–T25 completos.
6. Ejecutar regresión F1/F2/F3 + Graphify + Kairos + DIKE + Smoke.
7. Recoger salida, logs, hashes y estado de entorno.
8. Emitir informe de cierre.

No declarar cierre productivo antes del punto 7.

## 3. MATRIZ T01–T25

| Test | Caso | Resultado esperado |
|---|---|---|
| T01 | Consulta exacta | Recupera evidencia pertinente y autorizada |
| T02 | Equivalencia semántica | Recupera el mismo conocimiento relevante sin exigir coincidencia literal |
| T03 | Ambigüedad | No inventa una interpretación; conserva/expone la ambigüedad cuando afecte al retrieval |
| T04 | Multidominio | Respeta los dominios aplicables y no mezcla conocimiento irrelevante |
| T05 | Restricción temporal | Respeta fecha/validez cuando la consulta la exige |
| T06 | Restricción territorial | Respeta territorio/jurisdicción cuando el conocimiento lo requiere |
| T07 | Vigente vs obsoleta | Solo devuelve la versión autorizada recuperable |
| T08 | Revocado | Contenido REVOCADO no llega al contexto |
| T09 | Cuarentena | Contenido CUARENTENA no llega al contexto |
| T10 | Pendiente decisión humana | Contenido PENDIENTE_DECISION_HUMANA no llega al contexto |
| T11 | Duplicados | No genera conocimiento/embedding duplicado; contexto sin duplicación redundante |
| T12 | Evidencia parcial | Devuelve PARTIAL y explicita cobertura/limitaciones |
| T13 | Ausencia de evidencia | Devuelve NO_EVIDENCE; no fabrica contenido |
| T14 | Contradicción | Conserva CONTRADICTORY y provenance de las evidencias relevantes |
| T15 | Ruido | El reranking reduce ruido sin convertir candidatos no autorizados en válidos |
| T16 | Provenance | Cada evidencia recuperada es reconstruible hasta su origen/versionado |
| T17 | Leakage | Ningún estado no recuperable aparece en el ContextPacket |
| T18 | Contexto duplicado | No duplica evidencia equivalente en el ContextPacket |
| T19 | Grounding | El contexto recibido por Positrón mantiene trazabilidad de la evidencia |
| T20 | Sin evidencia | Resultado explícito de ausencia; nunca fallback inventado |
| T21 | Concurrencia | Operaciones concurrentes mantienen idempotencia e integridad |
| T22 | Persistencia | Reinicio no destruye conocimiento ni rompe trazabilidad |
| T23 | Regresión F1 | 42/42 reales PASS |
| T24 | Regresión F2 | 57/57 reales PASS |
| T25 | Regresión F3 | 32/32 reales PASS; SKIP no cuenta como PASS |

## 4. CRITERIOS DE PASS

Un test cuenta como PASS únicamente si:

- fue ejecutado;
- el resultado actual fue observado;
- coincide con el resultado esperado;
- existe evidencia reproducible.

Estados permitidos para el registro:

- PASS
- FAIL
- SKIP
- BLOCKED

Regla:

> SKIP ≠ PASS.
> BLOCKED ≠ PASS.

## 5. EVIDENCIA MÍNIMA POR EJECUCIÓN

Registrar:

- fecha/hora;
- commit de código probado;
- entorno;
- versión PostgreSQL;
- versión pgvector;
- modelo/dimensión de embedding utilizada;
- configuración relevante del retrieval;
- test ID;
- input;
- expected;
- actual;
- result;
- provenance cuando aplique;
- logs o artefacto de prueba;
- hash del artefacto cuando sea posible.

## 6. REGLAS DE INTEGRIDAD

### 6.1 Gobernanza antes de similitud

Los filtros de recuperabilidad deben aplicarse antes de utilizar la similitud vectorial para seleccionar candidatos.

### 6.2 Closed-world

El Context Builder solo puede ensamblar evidencia procedente del conjunto autorizado recuperado.

### 6.3 No evidencia

NO_EVIDENCE no autoriza generación libre presentada como conocimiento recuperado.

### 6.4 Contradicción

Una contradicción no se resuelve silenciosamente mediante selección arbitraria del candidato con mayor score.

### 6.5 Versionado

Una versión obsoleta/revocada no puede ganar a una vigente por obtener mayor similitud.

### 6.6 Separación funcional

- Query Analysis interpreta la necesidad de recuperación, no diagnostica ni perfila.
- Retriever recupera candidatos autorizados.
- Vector Search mide similitud.
- Reranker ordena.
- Evidence Assessment clasifica evidencia.
- Context Builder ensambla contexto.
- Positrón recibe conocimiento/contexto; no recibe una orden para sustituir la gobernanza.

## 7. CIERRE DE FASE 4

Fase 4 puede declararse técnicamente cerrada únicamente cuando T01–T25 estén resueltos con evidencia y las regresiones requeridas estén ejecutadas en infraestructura real.

El estado final debe distinguir:

IMPLEMENTED
TESTED
OPERATIVE IN SIMULATION
INTEGRATED
APPROVED
DEPLOYED
PRODUCTION

No elevar un estado al siguiente sin evidencia correspondiente.

## 8. PUNTO DE REANUDACIÓN

La ejecución actualmente bloqueada debe reanudarse en infraestructura PostgreSQL + pgvector real. No es necesario rediseñar Fase 4 ni volver a elaborar la matriz.

La documentación canónica de arquitectura se encuentra en:
`04_DOCUMENTACION/WAIPL_Fase4_Auditoria_y_Paquete_Canonico_v0.1.md`

Este runbook es complementario y operativo.
