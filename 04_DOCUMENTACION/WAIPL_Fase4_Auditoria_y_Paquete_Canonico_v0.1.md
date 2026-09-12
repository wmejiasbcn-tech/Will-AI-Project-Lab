# WAIPL / Will App
# FASE 4 — AUDITORÍA DE COHERENCIA Y PAQUETE CANÓNICO v0.1

Fecha: 2026-09-09
Ámbito: Knowledge + Content / RAG
Estado de la auditoría: EJECUTADA
Estado de implementación de Fase 4: IMPLEMENTED + TESTED + OPERATIVE IN SIMULATION
Estado de validación de infraestructura real: PENDIENTE

---

## 1. VEREDICTO EJECUTIVO

La arquitectura de Fase 4 es conceptualmente coherente con las Fases 1–3 y con el modelo de gobernanza establecido.

No se detecta necesidad de crear otro RAG ni de rediseñar Fase 4.

Sí se detectan cuatro puntos que deben quedar cerrados antes del cierre técnico definitivo:

1. **Predicado canónico de recuperabilidad**: el Retriever debe usar los estados y campos reales de Fases 1–3. No debe depender de campos heredados/propuestos que no formen parte del contrato canónico.
2. **Semántica de T25**: un `SKIP` por ausencia de `psycopg` no equivale a un PASS de Fase 3. La evidencia histórica 32/32 del 2026-09-01 no sustituye la ejecución actual.
3. **Closed-world Context Builder**: el Context Builder solo puede ensamblar elementos procedentes del conjunto autorizado entregado por el Retriever/Evidence Assessment; no puede completar huecos con conocimiento propio.
4. **Separación de funciones**: Query Analysis no diagnostica ni perfila; Reranker no autoriza, revoca ni decide verdad/legalidad; Evidence Assessment clasifica evidencia pero no modifica estados de gobernanza.

Conclusión:
**NO HAY BLOQUEO CONCEPTUAL DE FASE 4.**
El bloqueo restante es de validación técnica real de infraestructura y de evidencia de cierre.

---

# 2. ARQUITECTURA CANÓNICA

La cadena queda fijada como:

CONSULTA
→ QUERY ANALYSIS
→ GOVERNED RETRIEVER
→ PRE-FILTERS
→ VECTOR SEARCH
→ RERANKING
→ EVIDENCE ASSESSMENT
→ CONTEXT BUILDER
→ CONTEXT PACKET
→ POSITRÓN

La arquitectura es acumulativa:

FASE 1 — Knowledge Model
↓
FASE 2 — Ingestion Layer
↓
FASE 3 — PostgreSQL + pgvector
↓
FASE 4 — Retriever + Context Builder
↓
FASE 5 — Integración con Positrón / Will App

No se crea `rag_v2`, `rag_new`, `rag_final` ni una arquitectura paralela.

---

# 3. AUDITORÍA DE LOS 14 REQUISITOS

| # | Requisito | Veredicto | Condición de cierre |
|---|---|---|---|
| 1 | Query Analysis | COHERENTE | Debe producir necesidad de recuperación, nunca perfil/diagnóstico |
| 2 | Pre-filters | COHERENTE | Filtrar autorización/estado antes de similitud |
| 3 | Recall | COHERENTE | Medir recuperación pertinente con consultas exactas y semánticas |
| 4 | Precision/noise | COHERENTE | Reranking solo sobre candidatos autorizados |
| 5 | Reranking | COHERENTE | Solo ordenar; no decidir epistemología/legalidad/autorización |
| 6 | Evidence sufficiency | COHERENTE | Clasificación explícita de suficiencia |
| 7 | Absence | COHERENTE | `NO_EVIDENCE` es resultado válido |
| 8 | Partial | COHERENTE | Conservar dimensiones no cubiertas |
| 9 | Contradictory | COHERENTE | Conservar evidencias y provenance de ambas |
| 10 | Context Builder | COHERENTE | Construcción cerrada sobre evidencia autorizada |
| 11 | Provenance | COHERENTE | Cadena reconstruible hasta la fuente |
| 12 | Grounding | COHERENTE | Positrón debe poder reconstruir qué evidencia recibió |
| 13 | Leakage | COHERENTE | Estados no recuperables no pueden llegar al Context Packet |
| 14 | Versioning | COHERENTE | Gobernanza precede a similitud; versión obsoleta no gana a vigente |

Los 14 requisitos no se amplían.

---

# 4. CONTRATO CANÓNICO DE QUERY ANALYSIS

Entrada:
- consulta original.

Salida mínima:

- `query`
- `normalized_query`
- `concepts`
- `entities`
- `domain`
- `subdomain`
- `context`
- `territory`
- `jurisdiction`
- `temporal_constraints`
- `information_intent`

Regla negativa absoluta:

> Query Analysis no diagnostica ni perfila a la persona.

Incorrecto:
`"habla de X" → "esta persona es Y"`

Correcto:
`"¿Qué se sabe sobre X?" → concepto X → recuperación de conocimiento pertinente`

Query Analysis no decide:
- riesgo personal;
- diagnóstico;
- intención psicológica;
- identidad;
- legalidad;
- verdad;
- autorización de conocimiento.

---

# 5. CONTRATO CANÓNICO DEL GOVERNED RETRIEVER

## 5.1 Regla de entrada

Antes de vector search deben quedar excluidos los contenidos que no sean simultáneamente:

- `VIGENTE`;
- autorizados por la decisión humana correspondiente;
- recuperables.

Después pueden aplicarse, cuando correspondan:

- dominio;
- subdominio;
- jurisdicción;
- territorio;
- fecha;
- vigencia;
- tipo de fuente;
- versión;
- restricciones.

## 5.2 Regla de prioridad

La gobernanza precede a la similitud.

Ejemplo:

v1 = `OBSOLETA`, similarity 0.94
v2 = `VIGENTE`, similarity 0.91

Resultado permitido:
v2.

Resultado prohibido:
v1 por tener mayor similitud.

## 5.3 Regla de campos

No introducir como requisito canónico campos de documentos anteriores o propuestas históricas si no forman parte del modelo real de Fases 1–3.

En particular, expresiones históricas como:

`dike_verdict`
`var_status`
`is_vigente`

solo pueden utilizarse si existen realmente en el esquema/contrato vigente.

El contrato canónico debe derivarse de los estados y relaciones ya construidos.

---

# 6. VECTOR SEARCH

Función:

> localizar candidatos potencialmente pertinentes.

No significa:

> seleccionar la respuesta.

Entrada conceptual:
- embedding de consulta;
- conjunto previamente filtrado.

Salida:
- candidatos;
- score de similitud;
- metadatos necesarios para reranking y provenance.

`top_k_candidates` debe ser configurable.

No se fija arbitrariamente un valor productivo sin medición.

---

# 7. CONTRATO DEL RERANKER

El Reranker puede ordenar candidatos utilizando señales de pertinencia, por ejemplo:

- similitud semántica;
- coincidencia conceptual;
- correspondencia con dominio/subdominio;
- correspondencia contextual;
- adecuación a la consulta;
- redundancia.

Puede considerar metadatos autorizados para mejorar el orden.

No puede:

- aprobar conocimiento;
- rechazar conocimiento por motivos epistemológicos;
- revocar;
- cambiar estados;
- decidir legalidad;
- sustituir a Vár;
- sustituir a DIKE;
- crear evidencia;
- convertir un candidato no autorizado en autorizado.

Regla:

> **El Reranker ordena. No gobierna.**

---

# 8. CONTRATO DE EVIDENCE ASSESSMENT

Estados mínimos:

- `SUFFICIENT`
- `PARTIAL`
- `INSUFFICIENT`
- `NO_EVIDENCE`
- `CONTRADICTORY`

## 8.1 NO_EVIDENCE

Si no existe evidencia suficiente:

`retrieval/evidence status = NO_EVIDENCE`

No se permite:

`NO_EVIDENCE → generación libre → afirmación presentada como conocimiento`

Regla:

> **NO EVIDENCIA ≠ PERMISO PARA FABRICAR.**

## 8.2 PARTIAL

Debe conservar:

- qué dimensión está cubierta;
- qué dimensión no está cubierta;
- evidencia disponible;
- provenance.

## 8.3 CONTRADICTORY

Debe conservar:

- evidencia A;
- evidencia B;
- provenance A;
- provenance B;
- naturaleza de la contradicción, cuando pueda determinarse.

No se debe ocultar una contradicción por seleccionar silenciosamente una de las fuentes.

Evidence Assessment no cambia el estado canónico del conocimiento.

---

# 9. CONTRATO CLOSED-WORLD DEL CONTEXT BUILDER

Principio:

> El Context Builder no añade conocimiento externo al conjunto autorizado recuperado.

Entrada:
- candidatos ya autorizados;
- resultado de reranking;
- evaluación de evidencia;
- provenance.

Salida: `ContextPacket`.

Estructura mínima:

```json
{
  "query": "...",
  "retrieval_status": "...",
  "evidence_status": "...",
  "items": [],
  "provenance": [],
  "limitations": [],
  "contradictions": [],
  "version_information": []
}
```

Cada item debe conservar, cuando exista:

- `document_id`
- `version_id`
- `chunk_id`
- `content_hash`
- `content`
- `state`
- provenance
- información de versión relevante.

Regla crítica:

> Si un dato no fue recuperado/autorizado, el Context Builder no puede introducirlo.

---

# 10. PROVENANCE Y GROUNDING

La cadena mínima reconstruible es:

FUENTE
→ DOCUMENTO
→ VERSIÓN
→ CHUNK
→ CONTENIDO
→ ESTADO
→ VERIFICACIÓN/DECISIÓN
→ CONTEXT PACKET

El objetivo no es únicamente devolver texto relevante.

El objetivo es poder reconstruir:

> qué conocimiento recibió Positrón, de dónde salió y bajo qué estado/versionado llegó.

Grounding se entiende aquí como trazabilidad del contexto utilizado, no como garantía automática de que el modelo final siempre razone correctamente.

---

# 11. ANTI-LEAKAGE

Estados que no deben aparecer en retrieval/context:

- `OBSOLETA`
- `REVOCADA`
- `CUARENTENA`
- `PENDIENTE_DECISION_HUMANA`
- cualquier otro estado que el modelo canónico marque como no recuperable.

La similitud nunca puede saltarse esta barrera.

Caso crítico:

contenido CUARENTENA con similarity 0.95
→ debe quedar fuera.

---

# 12. VERSIONADO

Regla:

> Gobernanza antes que similitud.

Para una misma cadena de versiones:

v1 → v2 → v3

si v1/v2 están obsoletas y v3 vigente:

- v1: no recuperable;
- v2: no recuperable;
- v3: recuperable.

`replaces_a` debe mantenerse como relación histórica.

La recuperación no debe reconstruir una versión obsoleta como si siguiera vigente.

---

# 13. DEDUPLICACIÓN

La deduplicación pertenece al modelo acumulativo anterior y debe conservarse en Fase 4.

Mismo `content_hash`:

→ alias
→ no nueva representación física
→ no embedding duplicado.

En Context Packet:

→ deduplicar resultados redundantes.

Esto no debe alterar la provenance de las fuentes que apuntan al mismo conocimiento.

---

# 14. MATRIZ DE PRUEBAS CANÓNICA FASE 4

T01 — consulta exacta
T02 — consulta semánticamente equivalente
T03 — consulta ambigua
T04 — consulta multidominio
T05 — restricción temporal
T06 — restricción territorial
T07 — vigente vs obsoleta
T08 — revocado
T09 — cuarentena
T10 — pendiente de decisión
T11 — duplicados
T12 — evidencia parcial
T13 — ausencia de evidencia
T14 — evidencia contradictoria
T15 — resultados ruidosos
T16 — provenance completo
T17 — leakage
T18 — contexto duplicado
T19 — grounding
T20 — consulta sin evidencia
T21 — concurrencia
T22 — persistencia
T23 — regresión F1
T24 — regresión F2
T25 — regresión F3

Cada test debe conservar:

- INPUT
- EXPECTED
- ACTUAL
- RESULT
- evidencia suficiente para reconstrucción.

Un contador `25/25` por sí solo no es evidencia suficiente.

---

# 15. AUDITORÍA ESPECÍFICA DEL ESTADO ACTUAL

Existe una diferencia crítica entre:

A) `25/25 PASS` en una batería donde determinados tests utilizaron mocks;

y
B) `25/25 PASS` con PostgreSQL + pgvector reales y regresión real de Fase 3 ejecutada en la misma validación.

La primera demuestra funcionamiento de la implementación bajo simulación.

La segunda demuestra la integración con infraestructura real.

Por tanto:

**El resultado documentado de Fase 4 como IMPLEMENTED + TESTED + OPERATIVE IN SIMULATION es coherente.**

No es legítimo elevarlo a:

- INTEGRATED;
- APPROVED;
- DEPLOYED;
- PRODUCTION.

---

# 16. T25 — PUNTO DE CONTROL ESPECIAL

El historial de ejecución muestra que T25 llegó a ser marcado como PASS después de introducir una condición para saltar la ejecución cuando `psycopg` no estaba disponible.

Eso puede ser correcto como mecanismo para que la batería no falle artificialmente por una dependencia ausente, pero tiene una consecuencia:

> `SKIP por entorno ≠ PASS funcional de Fase 3`.

Por tanto, para el cierre definitivo:

`T25 = PASS`

solo debe contar como validación de regresión actual cuando los 32 tests de Fase 3 se hayan ejecutado realmente.

El 32/32 histórico del 2026-09-01 debe conservarse como evidencia histórica, pero no sustituye la ejecución requerida actualmente.

---

# 17. BENCHMARK MISTRAL

Mistral se mantiene como:

**BENCHMARK EXTERNO DE COMPORTAMIENTO**

No es dependencia arquitectónica.

Se utilizará para comprobar el núcleo:

documento
→ indexación/procesamiento
→ retrieval
→ respuesta grounded

y, especialmente:

- consulta concreta;
- comprobación de detalles concretos;
- grounding;
- reducción de respuestas genéricas.

No sustituye:
- gobernanza WAIPL;
- estados;
- decisión humana;
- provenance;
- aliases;
- versionado;
- AuditLog;
- Vár;
- DIKE;
- Kairos.

---

# 18. DEFINITION OF DONE — FASE 4

Fase 4 queda técnicamente cerrada cuando exista evidencia de:

1. Query Analysis funcionando sin diagnóstico/perfil.
2. Filtros previos de autorización y estado.
3. Retrieval pertinente.
4. Control de ruido.
5. Reranking limitado a ordenar.
6. Evaluación de suficiencia.
7. NO_EVIDENCE.
8. PARTIAL.
9. CONTRADICTORY.
10. Context Packet estructurado.
11. Provenance reconstruible.
12. Grounding trazable.
13. Ausencia de leakage.
14. Versionado respetado.
15. Deduplicación preservada.
16. T15–T19 ejecutados sobre PostgreSQL + pgvector reales.
17. Fase 3: 32/32 ejecutada ahora.
18. Regresión completa:
   - F1 42/42
   - F2 57/57
   - F3 32/32
   - F4 25/25
   - Graphify 34/34
   - Kairos 28/28
   - DIKE 40/40
   - Smoke 21/21

---

# 19. ESTADO FINAL DE ESTA AUDITORÍA

## VERDE

- Arquitectura acumulativa.
- Alcance de 14 requisitos.
- Separación de funciones.
- Gobernanza antes de similitud.
- No evidencia como resultado válido.
- Partial y contradictory explícitos.
- Provenance.
- Anti-leakage.
- Versionado.
- Deduplicación.
- Context Builder como capa de ensamblaje, no de conocimiento autónomo.
- Mistral como benchmark externo.

## ÁMBAR / PENDIENTE DE EVIDENCIA REAL

- PostgreSQL + pgvector en la ejecución actual de AutoClaw.
- T15–T19 contra infraestructura real.
- Fase 3 actual 32/32.
- Regresión completa actual.
- Cierre final con hashes/evidencias de la ejecución.

## ROJO

Ningún bloqueo conceptual detectado.

---

# 20. DECISIÓN OPERATIVA

No se modifica la arquitectura.

No se crea una nueva fase conceptual.

No se inicia Fase 5.

No se da por cerrado el RAG productivo.

El trabajo que queda es estrictamente de **validación técnica real y evidencia de cierre**.

Cuando AutoClaw recupere crédito, debe continuar desde su punto de bloqueo:

PostgreSQL real
→ pgvector real
→ T15–T19 reales
→ Fase 3 actual 32/32
→ Fase 4 25/25
→ regresión completa
→ informe de cierre con evidencia y hashes.

---

# 21. CRITERIO RECTOR

> **RAG proporciona conocimiento. No toma decisiones.**

Y:

> **La gobernanza precede a la similitud.**

Y:

> **No evidencia no autoriza fabricación.**

Y:

> **Lo que no ha sido autorizado no puede llegar al Context Packet.**

Y:

> **No se declara PASS aquello que no se ha ejecutado realmente.**
