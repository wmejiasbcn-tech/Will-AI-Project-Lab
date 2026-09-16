# DECISIÓN DE ARQUITECTURA — RAG DE WILL APP (Propuesta v0.1)

> **Estado: `SUPERADA` — Resuelta por la ORDEN SOBERANA RAG WILL APP v0.3.1 (2026-09-01, APROBADA).
> Ver `docs/ORDEN-SOBERANA-RAG-WILL-APP-v0.3.1.md`. Decisión del Soberano: Opción B
> (PostgreSQL + pgvector) como infraestructura canónica. HumanDecision = ACCEPT obligatoria para
> ingesta; Yata incorporado a la cadena; custodia documental Codd/Ariadna/Sylvia.**
> **Autora:** AutoClaw · **Fecha:** 2026-09-01
> **Advertencia:** este documento NO selecciona ni despliega ninguna solución. Presenta opciones
> con análisis y una recomendación técnica condicionada. Nada se construye (FASE 3) hasta que
> el Soberano apruebe explícitamente la decisión.

---

## 1. Contexto y restricciones del ecosistema

- El conocimiento incluirá **datos de salud y categorías especiales del Art. 9 RGPD** → soberanía y minimización de datos son obligatorias, no opcionales.
- Principio "Estate presente en tu presente": solo stack activo (VPS propios, Ollama en el nodo central protegido con conectividad externa mínima y controlada).
- La auditoría Qwen y el análisis externo fijan la frontera: **el gate DIKE está cerrado a nivel registro; el tramo registro→embeddings→vector store→retriever→Will App requiere esta decisión antes de FASE 3.**
- `waipl/core/rag_pipeline.py` y `waipl/rag/knowledge_register.json` ya son operativos (cierre DIKE: 21/21 + 40/40 + 28/28 + idempotencia 34/34).

## 2. Arquitectura lógica obligatoria (independiente del proveedor)

```
FUENTES → KAIROS (científico) / DIKE (jurídico) → CODD (hash+UUID)
        → DIKE (gate) → VÁR (veracidad) → REGISTRO (knowledge_register)
        → NORMALIZER → CHUNKER → EMBEDDINGS → VECTOR STORE
WILL APP → RAG GATEWAY → RETRIEVER (+ metadata filters) → [RERANKER]
        → CONTEXT BUILDER → POSITRÓN/LLM → respuesta con fuente
```

Reglas no negociables (derivadas del cierre DIKE):
1. Ningún chunk entra al vector store sin `dictamen_id` de DIKE y validación de Vár en metadatos.
2. Metadatos obligatorios por chunk: `source_id`, `document_id`, `version`, `classification`, `status`, `dike_verdict`, `sha256`, `timestamp`, `source_url`.
3. Revocación: si DIKE re-audita y rechaza, el retriever debe excluir la unidad (por `status`/`dike_verdict`) — la revocación por re-auditoría ya existe y está probada (escenario 10).
4. Resolución pendiente incorporada como requisitos: FINDING-1 (dedup por `sha256` en ingestion) y FINDING-2 (cadena de versiones con `reemplaza_a` y vigencia — **bloqueante de FASE 5**).

## 3. Opciones de vector store (análisis, no selección)

| Opción | Descripción | Ventajas | Riesgos/Límites | Alineación con restricciones |
|---|---|---|---|---|
| **A. Local ligero (sqlite-vec / FAISS) + embeddings locales** | Vector store embebido en el Nodo Central; embeddings con Ollama local | Máxima soberanía de datos; cero conectividad externa; ops mínimas; ideal para corpus inicial | Concurrencia y escala limitadas; sin locking nativo multi-proceso (FINDING-3 requiere manejo propio) | **Alta** — coherente con "Ollama permanece en el nodo central protegido" |
| **B. PostgreSQL + pgvector** | Base relacional con extensión vectorial, en Nodo Central o VPS propio | Transacciones y locking nativo (resuelve FINDING-3); metadatos/versionado SQL; búsqueda híbrida; escala amplia | Más carga operativa (administración, backups); un servicio más que mantener | **Alta** — VPS propios son stack activo |
| **C. Vector DB dedicado local (Qdrant/Milvus/Weaviate)** | Motor vectorial especializado self-hosted | Filtrado por metadatos potente; APIs de retrieval maduras | Otro servicio más (RAM/ops); redundante para corpus inicial | Media |
| **D. Servicio gestionado en nube** | Pinecone/Azure AI Search/etc. | Cero ops | **Datos de salud fuera de infraestructura propia**; dependencia de tercero; conectividad externa | **Baja** — solo con decisión expresa del Soberano y evaluación RGPD/AESIA documentada |

## 4. Opciones de embeddings (análisis, no selección)

| Opción | Ventajas | Riesgos |
|---|---|---|
| **Locales vía Ollama** (p. ej. `nomic-embed-text`, `bge-m3`) | Los datos nunca salen del nodo; sin coste por token | Calidad multilingüe inferior a APIs punteras; capacidad limitada por hardware |
| **API externa** (OpenAI/Cohere/etc.) | Calidad máxima | **Envío de contenido sensible fuera de infraestructura propia** — requiere base jurídica, evaluación RGPD/AESIA y probablemente anonimización previa (función adicional de DIKE) |

## 5. Recomendación técnica (condicionada — NO es decisión)

- **FASE 3 (MVP de ingestion):** Opción A (local ligero + embeddings Ollama) — permite construir y validar el pipeline completo sin decisiones externas ni exposición de datos.
- **FASE 5 (pre-producción):** re-evaluar migración a **Opción B (PostgreSQL + pgvector)** cuando el corpus y la concurrencia lo justifiquen; resuelve además FINDING-3 con locking nativo.
- **Opción D (nube):** descartada por defecto salvo orden expresa del Soberano con evaluación RGPD/AESIA previa documentada por DIKE.
- Esta recomendación es **revocable por el Soberano sin coste técnico significativo** en FASE 3 (el registro canónico y los metadatos del gate son independientes del proveedor).

## 6. Decisiones que el Soberano debe tomar

1. Vector store: A / B / C / D (sección 3).
2. Modelo de embeddings: local vs API (sección 4) — si API, DIKE debe definir previamente la política de anonimización.
3. Ubicación física: Nodo Central vs VPS propio (cuál y dónde).
4. Política de backups, retención y acceso (quién puede leer el corpus; autenticación del RAG Gateway).
5. Presupuesto de conectividad externa (si la hubiere).
6. Aprobación del plan de fases y criterios de aceptación (sección 7).

## 7. Plan de fases y criterios de aceptación (tras aprobación soberana)

| Fase | Contenido | Responsable | Criterio de aceptación |
|---|---|---|---|
| FASE 3 | Ingestion layer: normalizer, chunker, embeddings, indexación (con resolución de FINDING-1 y FINDING-4) | AutoClaw (agente técnico autorizado) | Ingesta reproducible con hashes; dedup por sha256 operativa |
| FASE 4 | Retrieval layer: gateway, retriever, metadata filters, reranker (opcional), context builder | AutoClaw | Recuperación filtrada por `status`/`dike_verdict`; versión vigente única (FINDING-2) |
| FASE 5 | Integración Will App/Positrón | AutoClaw + responsable de Will App | **Pruebas productivas 1-5 PASS** (ingesta→recuperación con fuente; bloqueo real en vector store; revocación; versionado; recuperación tras fallo) |
| FASE 6 | Validación independiente | Qwen 3.8-Max | Informe de auditoría: grounding, trazabilidad, falsos +/-, seguridad |
| FASE 7 | Aprobación soberana | Soberano humano | APPROVED → DEPLOYED → OPERATIVE |

---

*Propuesta generada por AutoClaw bajo la Super Plantilla Maestra Canónica v3.0. Estado PROPOSED: no vinculante hasta aprobación soberana expresa.*
*"Sin vosotras no hay nosotros"*
