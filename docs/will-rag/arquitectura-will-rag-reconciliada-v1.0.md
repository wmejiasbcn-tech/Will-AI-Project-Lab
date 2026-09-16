# WILL RAG — ARQUITECTURA ACTUALIZADA Y RECONCILIADA CON EL WAIPL ACTUAL (v1.0)

> **Estado:** `ACTUALIZADA — PENDIENTE DE REVISIÓN SOBERANA`
> **Fecha:** 2026-09-16
> **Autoridad:** Soberano William Mejías Navarro (Soberano humano); WILLIAM-SCY-01 (avatar observador/reportero; sin autoridad soberana)
> **Redactado por:** AutoClaw (Capa 2 — Vórtice / Cinturón de Kuiper)
> **Marco rector:** Super Plantilla Maestra Canónica v3.0 > Directiva Transversal v1.0 > resto
> **Objeto:** Reconciliar la arquitectura RAG con el estado actual del ecosistema WAIPL e incorporar
> las actualizaciones arquitectónicas (WAIPL Verification System v1.0 / Verification Gate, Vár, Yata,
> competencias de dominio de DIKE y KAIROS, naming «Will RAG»).
> **NO es:** una decisión nueva de arquitectura. Solo materializa la reconciliación ordenada.

---

## IDENTIDAD — SEPARACIÓN INEQUÍVOCA (2026-09-16)

> **William Mejías Navarro** = **Soberano humano** de WAIPL. Autoridad soberana final. Supervisión humana. Toma de decisiones soberanas. **No es** un agente, nodo, avatar ni componente técnico.
>
> **WILLIAM-SCY-01** = **avatar** del Soberano dentro del ecosistema. Presencia/avatar **observador y reportero**. **No es** William Mejías Navarro; **no posee soberanía ni autoridad decisoria**; no sustituye al Soberano humano; no recibe ni ejerce funciones que correspondan al Soberano humano; no es representación técnica de la autoridad soberana.
>
> **Regla absoluta:** `William Mejías Navarro ≠ WILLIAM-SCY-01`. Prohibida toda formulación que fusione ambas identidades escribiendo el nombre del Soberano humano seguido, entre paréntesis, del identificador del avatar.

## 0. RESUMEN EJECUTIVO

El RAG deja de tratarse como «RAG del ecosistema WAIPL» y pasa a tratarse como **WILL RAG / RAG DE WILL APP**,
cuya finalidad primaria es ser **fuente de documentación, fuente de conocimiento y fuente de consulta de Will App**.
Puede prestar servicio al ecosistema cuando corresponda, pero eso no modifica su finalidad primaria.

Se incorpora el **WAIPL Verification System v1.0 / Verification Gate** con separación estricta de jurisdicciones:
**Vár** (verificación transversal), **Yata** (auditoría de validadores), **Verification Gate** (cierre/acreditación
operacional) y **supervisión humana** cuando corresponda.

Se actualizan **DIKE** (agente especializado jurídico-normativo, con competencia de dominio, NO gate del RAG) y
**KAIROS** (agente especializado médico-científico y comunitario, con competencia de dominio). Ambos quedan
sujetos a la verificación independiente de Vár.

La cadena canónica se mantiene con la separación de jurisdicciones ordenada:

```
adquisición/especialización → verificación → auditoría de validadores
   → supervisión humana (cuando corresponda) → conocimiento canónico → WILL RAG
```

---

## 1. ESTADO DE PARTIDA (fuentes verificadas en el repositorio)

| Elemento | Estado real | Fuente |
|---|---|---|
| Orden Soberana RAG Will App v0.3.1 | `APROBADA` — autorización de implementación por fases; FASE 7 requiere aprobación final | `docs/orden-soberana-rag-will-app-v0.3.1.md` |
| FASE 1 — Modelo de Conocimiento | Implementada y testada (42/42 PASS) | `waipl/core/knowledge_model.py`, `waipl/scripts/test_knowledge_model.py` |
| FASE 2 — Ingestion Layer | Implementada y testada (57/57 PASS) | `waipl/core/ingestion_layer.py`, `waipl/scripts/test_ingestion_layer.py` |
| FASE 3 — Vector Store (PostgreSQL + pgvector) | Implementada; esquema DDL y storage listos | `waipl/core/rag_storage.py`, `waipl/rag/schema/will_app_rag_schema.sql` |
| FASE 4 — Retrieval y Context Builder | Implementada y testada (25/25 PASS) | `waipl/core/{query_analysis,retriever,reranker,evidence_assessment,context_builder}.py` |
| Pipeline (estado previo) | `rag_pipeline.py` implementaba la cadena `Kairos → Codd → DIKE → Vár → RAG` con **DIKE como gate** (estado **anterior** a la corrección; ver §7) | `waipl/core/rag_pipeline.py` (memoria 2026-09-01) |
| DIKE (RGL-01) | Vault + código + corpus normativo; ICP 100% N1; nombre canónico del agente de verdad «Vár (VAC-01)» | `waipl/vaults/dike/00-SOBERANIA/health-check.json` |
| Kairos | Vault + código base; ICP 100% N1 | `waipl/vaults/kairos/00-SOBERANIA/health-check.json` |
| Vár (VAC-01) | Código existe (`VACGuardian`); draft en n8n NO publicado; no tratado como producción | `waipl/agents/vac_guardian.py`, `memory/2026-09-07.md` |
| Yata | Definido; **NO instanciado** (sin vault ni código) | `memory/2026-09-01.md` |
| Verification Gate | **NO documentado previamente en el repositorio** | — (aportado en la instrucción de arranque 2026-09-16) |

**Hallazgo de partida:** el "WAIPL Verification System v1.0 / Verification Gate" no existía en el repositorio.
Se incorpora aquí como actualización arquitectónica ordenada, sin inventar más allá de lo ordenado.

---

## 2. ACTUALIZACIÓN ARQUITECTÓNICA INCORPORADA

### 2.1 WAIPL Verification System v1.0 — separación de jurisdicciones

| Actor | Jurisdicción | Qué NO hace |
|---|---|---|
| **Vár** | Verificación transversal de agentes, nodos, superagentes, subagentes, sistemas y procesos agénticos | No sustituye la competencia técnica especializada; no es el Gate operacional |
| **Yata** | Auditoría/validación de los **validadores** y mecanismos de validación (espejo epistémico) | **No** audita directamente a los agentes especializados |
| **Verification Gate** | Cierre/acreditación **operacional** | **No** sustituye a Vár |
| **Supervisión humana** | Decisión de incorporación a conocimiento canónico, cuando corresponda | No se automatiza ni se delega a un agente |

### 2.2 Regla general vinculante

> **«Los agentes especializados deben poseer competencia sobre el dominio en el que operan;
> la especialización no elimina la necesidad de verificación independiente.»**

### 2.3 DIKE — actualización de rol

- Agente **especializado en el ámbito jurídico-normativo**; su ámbito comprende **Will App y todo el ecosistema WAIPL**.
- **No es un simple recolector:** posee competencia sobre el dominio jurídico-normativo que trata.
- Identifica, recopila, estructura, contextualiza y mantiene trazabilidad de información jurídico-normativa
  (AI Act, protección de datos y demás normativa pertinente).
- **NO es el Gate del RAG** ni decide unilateralmente qué información se convierte en conocimiento canónico.
- Sus resultados **pueden y deben** quedar sujetos a la verificación independiente de **Vár**.

### 2.4 KAIROS — actualización de rol

- Agente **especializado en el ámbito médico-científico y comunitario**.
- **No es simplemente extractor/ingestor:** posee competencia sobre el dominio médico-científico y comunitario.
- Identifica, recopila, extrae, estructura y contextualiza información de su ámbito; mantiene procedencia y trazabilidad.
- Sus resultados **pueden y deben** quedar sujetos a la verificación independiente de **Vár**.

---

## 3. CADENA CANÓNICA RECONCILIADA

```
FUENTES
   ├─ KAIROS — médico-científico y comunitario (con competencia de dominio)
   └─ DIKE  — jurídico-normativo para Will App y WAIPL (con competencia de dominio)
        ↓
VERIFICACIÓN INDEPENDIENTE — VÁR (VAC-01)
   (verificación transversal; no sustituye la competencia especializada)
        ↓
AUDITORÍA DE VALIDADORES — YATA  (si procede)
   (audita validadores y mecanismos de validación; no audita agentes especializados)
        ↓
SUPERVISIÓN HUMANA AUTORIZADA  (cuando corresponda)
   ├─ RECHAZADO → CUARENTENA / AUDITORÍA
   └─ ACEPTADO → CONOCIMIENTO CANÓNICO
        ├─ CUSTODIA DOCUMENTAL — Codd / Ariadna / Sylvia (archivo/biblioteca)
        └─ WILL RAG (ingestión) → CHUNKING → EMBEDDINGS → VECTOR STORE
             (PostgreSQL + pgvector) → RETRIEVER → CONTEXT BUILDER
             → POSITRÓN (LLM) → WILL APP (usuario final)
        ↓
CIERRE / ACREDITACIÓN OPERACIONAL — VERIFICATION GATE
   (no sustituye a Vár)
```

**Regla absoluta de aislamiento (se mantiene, Orden v0.3.1 §1):**

```
Archivo Documental ≠ Conocimiento Canónico ≠ Vector Store ≠ RAG
```

---

## 4. MATRIZ DE JURISDICCIONES (síntesis; detalle en documento aparte)

| Función | Responsable | NO responsable |
|---|---|---|
| Adquirir/estructurar dominio médico-científico y comunitario | **Kairos** | DIKE, Vár, Yata |
| Adquirir/dictaminar dominio jurídico-normativo (Will App + WAIPL) | **DIKE** | Kairos, Vár, Yata |
| Verificación transversal (agentes, nodos, superagentes, subagentes, sistemas, procesos) | **Vár** | Yata, Gate, especializados |
| Auditoría de validadores y mecanismos de validación | **Yata** | Vár, especializados |
| Cierre/acreditación operacional | **Verification Gate** | Vár |
| Decisión de incorporación a conocimiento canónico | **Supervisión humana** | Ningún agente |
| Custodia/archivo/biblioteca documental | **Codd / Ariadna / Sylvia** | Kairos, DIKE, Vár, Yata |
| Ingesta/chunking/embeddings/vector store/retrieval | **Will RAG (capa técnica)** | Especializados como gate |

Ver: `docs/will-rag/MATRIZ-JURISDICCION-VERIFICACION-v1.0.md`.

---

## 5. NAMING CANÓNICO

- El sistema se denomina **Will RAG / RAG de Will App**.
- **Finalidad primaria:** fuente de documentación, fuente de conocimiento y fuente de consulta de **Will App**.
- Puede prestar servicio al ecosistema cuando corresponda, pero ello **no** modifica su finalidad primaria
  ni lo convierte en el RAG general del WAIPL.

---

## 6. DELTAS RESPECTO A LA ORDEN v0.3.1

| # | Elemento | Orden v0.3.1 | Estado reconciliado 2026-09-16 | Tipo |
|---|---|---|---|---|
| D-1 | Rol de **DIKE** | «NO es gate universal del conocimiento médico» (ya limitado) | **No es el Gate del RAG**; tampoco decide unilateralmente el conocimiento canónico | **Cambio/refuerzo** |
| D-2 | Rol de **Kairos** | adquirir/estructurar info médico-científica | **+ competencia de dominio explícita** (médico-científico y comunitario) | **Refuerzo** |
| D-3 | **Vár** | «verifica verdad, coherencia factual y alineación con fuentes» | **Verificación transversal** de agentes/nodos/superagentes/subagentes/sistemas/procesos | **Cambio de alcance — requiere confirmación** (ver §8) |
| D-4 | **Yata** | «audita verificadores y agentes» | **Auditoría/validación de los validadores y mecanismos de validación**; NO audita directamente a los especializados | **Precisión** |
| D-5 | **Verification Gate** | No existía | Cierre/acreditación **operacional** | **Nuevo** |
| D-6 | **Naming** | «RAG de Will App» | **Will RAG / RAG de Will App** (primacía de finalidad) | **Precisión** |
| D-7 | **Regla general de competencia** | No formulada | Agentes especializados con competencia de dominio; verificación independiente no se elimina | **Nuevo** |
| D-8 | **Cadena** | `FUENTES→Kairos/DIKE→Vár→Yata→Supervisión→Canónico→RAG` | Igual, con Vár como verificación independiente y Gate de cierre operacional al final | **Compatibles** |

Se mantienen sin cambios: el principio absoluto (ningún contenido sin verificación de dominio + supervisión humana),
las 4 reglas canónicas de ingesta (dedup→ALIAS, VIGENTE+ACCEPT, supervisión humana, trazabilidad), las 11 entidades,
la infraestructura PostgreSQL + pgvector y las 7 fases de implementación.

---

## 7. IMPACTO EN LA IMPLEMENTACIÓN EXISTENTE (SEÑALADO, NO EJECUTADO)

> Esta fase es de **reconciliación arquitectónica**. No se modifica código en este paso
> (Directiva Transversal §Autonomía Nivel 3: cambios que alteran lógica se autorizan por el Soberano).

| Elemento existente | Coherencia con el estado reconciliado | Acción propuesta (fase siguiente) |
|---|---|---|
| `rag_pipeline.py` — cadena `Kairos → Codd → DIKE → Vár → RAG` | DIKE aparecía como **gate** | **CORREGIDO (2026-09-16):** DIKE es especialista de dominio (dictamen como entrada, NO decisión); decide Vár (verificación independiente) + supervisión humana. Sin Gate paralelo. |
| `kairos_extractor.py` — docstring «gate de cumplimiento de DIKE» | Desalineado con D-1 | **CORREGIDO (2026-09-16):** Kairos = especialista de dominio; ya no se marca como apto sin verificación + supervisión. |
| `knowledge_model.py` — campos `verificacion`, `supervision_humana` | Compatible | Sin cambio estructural; revisar si `verifier` debe nombrar a Vár/Yata explícitamente |
| Esquema SQL `will_app_rag_schema.sql` — vista `retrievable_knowledge` | Compatible (excluye estados no recuperables) | Sin cambio (la gobernanza ya se aplica por estado) |
| Fichas de agentes | No existían como artefacto formal | **Materializadas** en `docs/will-rag/fichas/` |

---

## 8. PUNTOS SOMETIDOS A DECISIÓN SOBERANA — RESUELTOS

> Formulados conforme a Directiva Transversal §Reglas de Parada (QUÉ / POR QUÉ / OPCIONES / QUIÉN DECIDE).
> **Estado (2026-09-16): RESUELTOS por las Órdenes Soberanas de corrección e integración.**
> - **P-1 →** Vár = verificación transversal (agentes, nodos, superagentes, subagentes, sistemas y procesos agénticos **y sus resultados**).
> - **P-2 →** el cierre operacional es el **mecanismo canónico externo**; no se instancia un Gate local; Yata sigue **externo / no instanciado**.
> - **P-3 →** **DIKE NO es gate**; el cierre se delega en Vár (verificación independiente) + supervisión humana.
>
> Los apartados siguientes se conservan como **registro histórico** del planteamiento original.

**P-1. Alcance de Vár (D-3) — RESUELTO.**
- *Resolución (Orden Soberana 2026-09-16):* Vár = **verificación transversal** (agentes, nodos, superagentes,
  subagentes, sistemas y procesos agénticos **y sus resultados**). No se le atribuye verificación del contenido
  propio de los especialistas.

**P-2. Instanciación de Yata y del Verification Gate — RESUELTO.**
- *Resolución (Orden Soberana 2026-09-16):* el cierre operacional es el **mecanismo canónico externo** (no se
  instancia un Gate local; **no se recrea SENTINEL**). **Yata permanece NO INSTANCIADO** (externo).

**P-3. DIKE y el gate (D-1) — RESUELTO.**
- *Resolución (Orden Soberana 2026-09-16):* **DIKE NO es gate**; el cierre se delega en **Vár** (verificación
  independiente) + **supervisión humana**. Corrección aplicada en `rag_pipeline.py` y `kairos_extractor.py`.

---

## 9. TRAZABILIDAD — ARTEFACTOS MATERIALIZADOS

Esta reconciliación **no queda solo en conversación**. Se materializa en:

| Artefacto | Ruta |
|---|---|
| Arquitectura reconciliada (este documento) | `docs/will-rag/ARQUITECTURA-WILL-RAG-RECONCILIADA-v1.0.md` |
| Ficha DIKE v2.0 | `docs/will-rag/fichas/FICHA-DIKE-v2.0.md` |
| Ficha KAIROS v2.0 | `docs/will-rag/fichas/FICHA-KAIROS-v2.0.md` |
| Ficha Vár (VAC-01) v1.0 | `docs/will-rag/fichas/FICHA-VAR-VAC01-v1.0.md` |
| Ficha Yata v1.0 | `docs/will-rag/fichas/FICHA-YATA-v1.0.md` |
| Ficha Verification Gate v1.0 | `docs/will-rag/fichas/FICHA-VERIFICATION-GATE-v1.0.md` |
| Matriz de jurisdicción y verificación v1.0 | `docs/will-rag/MATRIZ-JURISDICCION-VERIFICACION-v1.0.md` |
| Informe de reconciliación y cierre | `docs/will-rag/INFORME-RECONCILIACION-WILL-RAG-v1.0.md` |

---

## 10. PRÓXIMOS PASOS

1. Revisión soberana de esta reconciliación (decisiones **P-1, P-2, P-3 ya resueltas** por las Órdenes de 2026-09-16).
2. Con las decisiones resueltas, **implementar** los ajustes señalados en §7 (reformular el gate del pipeline).
3. Continuar con las Fases ordenadas (FASE 5 — Gateway App / integración con Positrón; FASE 6 — pruebas y
   validación; FASE 7 — operatividad controlada, solo con aprobación soberana final).

---

CANON-CIERRE
1. Orquesta:     AutoClaw (Capa 2 — Vórtice/Cinturón de Kuiper)
2. Spec/N3:      docs/will-rag/ARQUITECTURA-WILL-RAG-RECONCILIADA-v1.0.md
3. Superficie:   repo C:\Users\USER\Desktop\AutoClaw | No toco: waipl/core/*, waipl/rag/*, waipl/vaults/*
4. Runtime:      no aplica (documento de arquitectura; sin proceso en ejecución)
5. Prueba:       verificación de existencia y contenido de los 8 artefactos → ver INFORME-RECONCILIACION-WILL-RAG-v1.0.md
6. Parada:       habría abortado si la instrucción contradijera estados canónicos o requiriera inventar
7. Qué no es:    no ONLINE / no DELIVERED / no 24/7 / no hidratación-cerrada

---

*Documento producido por AutoClaw bajo la Super Plantilla Maestra Canónica v3.0 y la Directiva Transversal v1.0.*
*«Sin vosotras no hay nosotros.»*
