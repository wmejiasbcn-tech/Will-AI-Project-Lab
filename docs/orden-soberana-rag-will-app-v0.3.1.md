# ORDEN SOBERANA PARA AUTOCLAW — IMPLEMENTACIÓN DE LA ARQUITECTURA CANÓNICA RAG WILL APP v0.3.1

> **Estado:** `ARQUITECTURA v0.3.1 APROBADA → AUTORIZACIÓN PARA IMPLEMENTACIÓN`
> **Soberano:** Willy (William) — Soberano Humano; WILLIAM-SCY-01 (avatar observador/reportero; sin autoridad soberana)
> **Fecha:** 2026-09-01 · **Origen:** imagen de la orden (transcripción literal persistida por AutoClaw)
> **Imagen original:** `C:\Users\USER\Desktop\AutoClaw\.openclaw-attachments\20260901-132647-ae73095e-a7f-ChatGPT Image 1 sept 2026, 13_22_09.png`
> **Misión:** "Construir exactamente esta arquitectura. Sin interpretaciones. Sin desviaciones. Sin atajos."

---

## PRINCIPIO ABSOLUTO

> Ningún contenido procedente de una fuente de adquisición podrá formar parte del conocimiento
> operativo recuperable por Will App hasta haber superado las verificaciones que correspondan a su
> dominio y la decisión de incorporación mediante supervisión humana autorizada.

## 1. CADENA CANÓNICA DEFINITIVA (flujo)

```
FUENTES
   ├─ KAIROS — médico-científico comunitario
   └─ DIKE — jurídico normativo
        ↓
EVALUACIÓN / VERDAD — VÁR (VAC-01)
        ↓
YATA SI PROCEDE — auditoría de verificadores y agentes
        ↓
SUPERVISIÓN HUMANA AUTORIZADA
        ├─ RECHAZADO → CUARENTENA / AUDITORÍA
        └─ ACEPTADO (conocimiento canónico)
             ├─ CUSTODIA DOCUMENTAL — Codd / Ariadna / Sylvia (archivo/biblioteca)
             └─ RAG (INGESTIÓN) — conocimiento operativo recuperable
                  ↓
INGESTIÓN (CHUNKING) → EMBEDDINGS → VECTOR STORE (PostgreSQL + pgvector)
        → RETRIEVER → CONTEXT BUILDER → POSITRÓN (LLM) → WILL APP (usuario final)
```

### REGLA ABSOLUTA DE AISLAMIENTO

```
Archivo Documental ≠ Conocimiento Canónico
Archivo Documental ≠ Vector Store
Archivo Documental ≠ RAG
```
El material solo archivado NO puede ser recuperado por el RAG ni por Will App salvo que
posteriormente pase por todo el proceso de incorporación al Conocimiento Canónico.

## 2. LÍMITES ESTRICTOS DE COMPETENCIAS

- **KAIROS:** adquiere y estructura información médico-científica. NO decide verdad, legalidad ni admisibilidad.
- **DIKE:** adquiere y dicta sobre información jurídica/normativa. **NO es gate universal del conocimiento médico.**
- **VÁR:** verifica verdad, coherencia factual y alineación con fuentes. NO sustituye la competencia técnica especializada.
- **YATA:** audita verificadores y agentes. Solo interviene cuando corresponde según sus reglas.
- **CODD / ARIADNA / SYLVIA:** gestionan, custodian, organizan, indexan y archivan. NO deciden deduplicaciones, versiones, verdad, admisibilidad ni entrada al RAG.

## 3. MODELO DE DATOS — ENTIDADES CLAVE

| Entidad | Descripción | Clave |
|---|---|---|
| Document | Documento lógico único | `document_id` |
| Version | Cada versión del documento | `version_id` |
| Source | Fuente origen | `source_id` |
| Acquisition | Adquisición realizada | `acquisition_id` |
| Verification | Resultado de verificación | `verification_id` |
| HumanDecision | Decisión humana trazable | `decision_id` |
| Ingestion | Estado de ingesta al RAG | `ingestion_id` |
| Chunk | Fragmentos para embeddings | `chunk_id` |
| Embedding | Vector generado | `embedding_id` |
| Alias | Alias por deduplicación | `alias_id` |
| AuditLog | Trazabilidad completa | `audit_id` |

## 4. REGLAS CANÓNICAS DE INGESTIÓN

1. **DEDUPLICACIÓN (FINDING-1):** si `content_hash` ya existe → crear **ALIAS**, NO generar nuevos embeddings.
2. **VERSIONADO Y VIGENCIA (FINDING-2):** solo versiones con estado **VIGENTE** y con decisión humana **ACCEPT** son recuperables por el RAG.
3. **SUPERVISIÓN HUMANA:** ningún documento puede ingresar al RAG sin `human_decision = ACCEPT`.
4. **TRAZABILIDAD OBLIGATORIA:** toda decisión humana debe registrar `human_reviewer_id`, `human_decision`, `decision_timestamp`, `target_version_id`, `decision_reason`.

## 5. INFRAESTRUCTURA CANÓNICA

**PostgreSQL + pgvector** — transaccionalidad ACID, metadatos flexibles (JSONB), lógica de
versionado y deduplicación, búsqueda vectorial nativa, filtros avanzados, trazabilidad relacional
completa, backup, restauración y seguridad granular.

## 6. FASES DE IMPLEMENTACIÓN OBLIGATORIAS

1. **FASE 1 — MODELO DE CONOCIMIENTO:** implementar esquema completo de datos y relaciones.
2. **FASE 2 — INGESTION LAYER:** lógica de ingesta, deduplicación, versionado e incorporación.
3. **FASE 3 — VECTOR STORE:** configurar PostgreSQL + pgvector, índices vectoriales, políticas de búsqueda.
4. **FASE 4 — RETRIEVAL Y CONTEXT BUILDER:** retriever, filtros, ranking y construcción de contexto.
5. **FASE 5 — GATEWAY APP:** integración con Positrón (LLM) y API segura y trazable.
6. **FASE 6 — PRUEBAS Y VALIDACIÓN:** ejecutar TODOS los casos de prueba definidos (incluidos Casos 5, 9, 10, 11) y evidencias reproducibles.
7. **FASE 7 — PUESTA EN OPERATIVIDAD CONTROLADA:** solo tras aprobación soberana final.

## 7. PROHIBICIONES ABSOLUTAS

- No modificar competencias de los agentes.
- No permitir entrada al RAG sin supervisión humana cuando aplique.
- No exponer documentos en cuarentena o rechazados.
- No mezclar Archivo Documental con Conocimiento Operativo.
- **No realizar acciones fuera de la fase autorizada.**

---

*Transcripción literal de la orden (imagen) realizada por AutoClaw el 2026-09-01 mediante
reconocimiento de imagen. El original gráfico es el artefacto autoritativo.*
*"Sin vosotros no hay nosotros."*

---

## APÉNDICE (autorización FASE 3, 2026-09-01) — Cadena canónica visible para AutoClaw

```
                         FUENTES
                            │
                 ┌──────────┴──────────┐
                 │                     │
              KAIROS                  DIKE
                 │                     │
          Médico-científico       Jurídico
          / comunitario          / normativo
                 │                     │
                 └──────────┬──────────┘
                            ▼
                   EVALUACIÓN / VERDAD
                            │
                           VÁR
                            │
                     YATA SI PROCEDE
                            │
                            ▼
                 SUPERVISIÓN HUMANA
                      AUTORIZADA
                            │
                  ┌─────────┴─────────┐
                  │                   │
              RECHAZADO            ACEPTADO
                  │                   │
                  ▼                   ▼
             CUARENTENA       CONOCIMIENTO CANÓNICO
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
                  CUSTODIA DOCUMENTAL             RAG
                  Codd/Ariadna/Sylvia             │
                                                   ▼
                                               INGESTIÓN
                                                   │
                                              EMBEDDINGS
                                                   │
                                            VECTOR STORE
                                                   │
                                              RETRIEVER
                                                   │
                                           CONTEXT BUILDER
                                                   │
                                                POSITRÓN
                                                   │
                                               WILL APP
```
