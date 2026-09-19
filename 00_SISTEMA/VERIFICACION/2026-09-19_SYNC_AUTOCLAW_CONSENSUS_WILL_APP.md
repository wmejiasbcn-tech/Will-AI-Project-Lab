# SYNC AutoClaw — cierre operativo del puente Consensus → Will App

**Fecha:** 2026-09-19  
**Naturaleza:** sincronización documental  
**Estado:** CONFORME / INFORMACIÓN  

## 1. Alcance

Esta entrada sincroniza el estado del puente operativo entre Consensus y Will App con el Lab/AutoClaw. No introduce cambios de código en el runtime de admisión.

## 2. Frontera arquitectónica

AutoClaw / Lab contiene la capa de **admisión** asociada a `RAGPipeline`. Ese circuito no es el circuito de consulta del usuario y no debe confundirse con él.

La consulta de usuario de Will App quedó cerrada operativamente en:

`/api/chat` → `ragQueryContext` → Consensus → modelo

El contexto externo se mantiene como `EXTERNAL_RETRIEVED_PENDING` y no constituye admisión al corpus canónico.

## 3. Estado operativo acreditado

- Producción: SHA `bbaf434`.
- Deployment: `dpl_2zqR4j5isLiZB7X3dCECbyNkMkqE`.
- Estado del deployment: `READY`.
- El contexto Consensus se inyecta al modelo; no se expone como bloque independiente en el JSON del chat.
- Fail-open: una incidencia de Consensus/RAG no debe tumbar `/api/chat`.

## 4. Custodia de evidencia

La evidencia primaria del cierre operativo está archivada en:

`WAIPL-RAG-CONSENSUS/04_EVIDENCIA/EVIDENCIA_RUNTIME_CONSENSUS_WILL_APP_2026-09-19.md`

La integración genérica permanece separada del adaptador específico de Consensus:

- `Will-App-WAIPL-RAG`: contrato genérico `ExternalRetrieval` / `ExternalSourceRegistry`.
- `WAIPL-RAG-CONSENSUS`: bridge/adaptador específico de Consensus y evidencia operativa.
- `Will-AI-Project-Lab` / AutoClaw: capa de admisión y componentes del ecosistema; no se incorpora Consensus directamente en `RAGPipeline` por este puente.

## 5. Sincronizaciones hermanas

- `Will-App-WAIPL-RAG`: Issue #1 — sincronización del cierre operativo del puente.
- `Agente-Will-App`: Issue #37 — sincronización del cierre operativo del puente.

## 6. Exclusiones

Este documento **no** autoriza ni realiza:

- cambios en `RAGPipeline` por este puente;
- cambios en `retriever.py` por este puente;
- admisión de resultados externos al corpus;
- modificaciones de la gobernanza de admisión;
- cambios en Kairos, DIKE, Vár o Yata;
- cambios en `master` por este trabajo;
- incorporación de JAMA en esta línea.

**JAMA queda aparcada hasta una línea expresa de trabajo.**

## 7. Regla de separación

`EXTERNAL_RETRIEVED_PENDING` ≠ admisión al corpus.

Este registro es exclusivamente de sincronización y custodia documental del estado del puente Consensus → Will App.
