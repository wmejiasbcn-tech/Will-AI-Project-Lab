# MATRIZ DE JURISDICCIÓN Y VERIFICACIÓN — WAIPL / WILL RAG (v1.0)

> **Estado:** `ACTUALIZADA — PENDIENTE DE REVISIÓN SOBERANA`
> **Fecha:** 2026-09-16
> **Fuentes:** `docs/jurisdiccion-hermes-kairos-dike-v1.0.md`, `docs/orden-soberana-rag-will-app-v0.3.1.md`,
> instrucción de arranque 2026-09-16, ACTAs y health-checks de DIKE y Kairos.

---

## 1. MATRIZ RACI DE FUNCIONES

| Función | Ejecuta (R) | Aprueba/Decide (A) | Consultado (C) | Informado (I) |
|---|---|---|---|---|
| Adquirir/estructurar dominio médico-científico y comunitario | Kairos | Vár (verificación) | DIKE | Soberano |
| Adquirir/dictaminar dominio jurídico-normativo | DIKE | Vár (verificación) | Kairos | Soberano |
| Verificación transversal (agentes/nodos/sistemas/procesos) | Vár | Soberano | Yata | — |
| Auditoría de validadores y mecanismos de validación | Yata | Soberano | Vár | — |
| Supervisión humana de incorporación a conocimiento canónico | Soberano / Carla | Soberano | Vár, especializados | — |
| Custodia/archivo/biblioteca documental | Codd / Ariadna / Sylvia | Hermes (operativo) | Especializados | — |
| Ingesta, chunking, embeddings, vector store, retrieval | Will RAG (capa técnica) | Soberano (por fases) | Vár | — |
| Cierre/acreditación operacional | Verification Gate | Soberano | Vár, Yata | — |
| Dirección operativa del ecosistema | Hermes | Soberano | Carla | — |

## 2. SEPARACIÓN DE JURISDICCIONES (verificación)

| Actor | Jurisdicción | Frontera (NO hace) |
|---|---|---|
| Vár | Verificación transversal de agentes/nodos/superagentes/subagentes/sistemas/procesos | No sustituye competencia especializada; no es el Gate |
| Yata | Auditoría de validadores y mecanismos de validación | No audita directamente a los especializados |
| Verification Gate | Cierre/acreditación operacional | No sustituye a Vár |
| Supervisión humana | Decisión de incorporación a conocimiento canónico | No se automatiza |

## 3. DELIMITACIÓN DE ROLES ESPECIALIZADOS vs. VERIFICACIÓN

| Dimensión | Kairos | DIKE | Vár | Yata | Gate |
|---|---|---|---|---|---|
| Competencia de dominio | Médico-científico y comunitario | Jurídico-normativo | Transversal | Metavalidadora | Operacional |
| ¿Adquiere conocimiento? | Sí | Sí | No | No | No |
| ¿Decide verdad? | No | No | Verifica (ver D-3) | Audita validadores | No |
| ¿Es gate del RAG? | No | **No** | No | No | No (cierre operacional) |
| ¿Entra al RAG sin supervisión humana? | No | No | — | — | — |

## 4. REGLA GENERAL VINCULANTE

> **«Los agentes especializados deben poseer competencia sobre el dominio en el que operan;
> la especialización no elimina la necesidad de verificación independiente.»**

## 5. ALINEACIÓN CON EL AGENTE DE LA VERDAD

| Agente | Agente de la Verdad asignado (ACTA) | Coherencia con el estado reconciliado |
|---|---|---|
| DIKE | Vár (VAC-01) | Compatible: Vár verifica independientemente |
| Kairos | Vár (VAC-01) | Compatible: Vár verifica independientemente |

> **Observación de trazabilidad:** el health-check de Kairos lo describe como «Agente de la Verdad para
> evidencia científica y RAG». Con la actualización, el **Agente de la Verdad del ecosistema es Vár**;
> Kairos es el **especialista** del dominio médico-científico sujeto a verificación. Se señala como
> inconsistencia de denominación a corregir en la fase de implementación (no se modifica aquí).

## 6. DIFERENCIAS CON LA MATRIZ v1.0 (2026-08-13)

| Aspecto | Matriz 2026-08-13 | Matriz 2026-09-16 |
|---|---|---|
| Rol de DIKE | Auditora normativa (gate implícito del RAG) | Especialista jurídico-normativo; **NO gate** |
| Rol de Kairos | Extractor médico-científico | Especialista médico-científico y comunitario con competencia |
| Vár | No figuraba | Verificación transversal |
| Yata | No figuraba | Auditoría de validadores |
| Verification Gate | No figuraba | Cierre operacional |
| Naming del RAG | RAG de Will App / «RAG del ecosistema» | **Will RAG / RAG de Will App** |

---

*Matriz materializada por AutoClaw — Super Plantilla Maestra Canónica v3.0.*
*«Sin vosotras no hay nosotros.»*
