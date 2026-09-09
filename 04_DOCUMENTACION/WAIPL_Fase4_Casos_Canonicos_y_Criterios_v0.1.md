# WAIPL / Will App
# FASE 4 — CASOS CANÓNICOS Y CRITERIOS v0.1

Fecha: 2026-09-09
Ámbito: Knowledge + Content / RAG
Naturaleza: especificación de casos; no sustituye la ejecución real.

## PROPÓSITO

Este documento fija ejemplos de comportamiento que permiten evaluar Fase 4 sin improvisar durante la ejecución.

## CASOS DE GOBERNANZA

### C01 — VIGENTE frente a OBSOLETA

Dado:
- documento A: VIGENTE, score 0.91;
- documento B: OBSOLETA, score 0.98.

Esperado:
- B queda excluido antes de competir por similitud;
- A puede llegar al contexto si satisface el resto de filtros.

FAIL si B llega al ContextPacket.

### C02 — REVOCADA

Dado un documento REVOCADO altamente similar.

Esperado:
- exclusión previa a vector ranking;
- no aparece en candidates autorizados;
- no aparece en ContextPacket.

### C03 — CUARENTENA

Dado un documento CUARENTENA con coincidencia semántica máxima.

Esperado:
- exclusión total del retrieval operativo.

### C04 — PENDIENTE_DECISION_HUMANA

Dado contenido técnicamente válido pero sin decisión humana requerida.

Esperado:
- no recuperable operativamente.

## CASOS DE EVIDENCIA

### C05 — NO_EVIDENCE

La consulta no tiene correspondencia suficiente en conocimiento autorizado.

Esperado:
- `NO_EVIDENCE`;
- limitations explícitas;
- ningún dato inventado como evidencia.

### C06 — PARTIAL

La consulta contiene dos dimensiones y solo una está respaldada.

Esperado:
- `PARTIAL`;
- evidencia disponible identificada;
- dimensión ausente identificada;
- provenance conservada.

### C07 — CONTRADICTORY

Dos fuentes autorizadas contienen afirmaciones incompatibles.

Esperado:
- `CONTRADICTORY`;
- ambas evidencias conservadas;
- provenance de ambas;
- no selección silenciosa basada únicamente en score.

## CASOS DE VERSIONADO Y DUPLICACIÓN

### C08 — Cadena de versiones

v1 OBSOLETA → v2 OBSOLETA → v3 VIGENTE.

Esperado:
- solo v3 puede ser recuperable, sujeto al resto de filtros;
- `replaces_a` conserva la historia.

### C09 — Duplicado por content_hash

Dos entradas representan exactamente el mismo contenido.

Esperado:
- ALIAS cuando corresponda;
- cero embedding nuevo para el duplicado;
- provenance no perdida.

## CASOS DE CONTEXTO

### C10 — Closed-world

El Retriever entrega tres evidencias autorizadas.

Esperado:
- Context Builder solo utiliza esas evidencias;
- no incorpora conocimiento externo para completar huecos.

### C11 — Leakage

Existe una fuente CUARENTENA altamente similar.

Esperado:
- cero presencia de esa fuente en candidates autorizados y ContextPacket.

### C12 — Grounding

Una evidencia entra en ContextPacket.

Esperado:
- Positrón puede identificar documento, versión/chunk y provenance disponibles;
- el contexto no pierde la referencia de origen.

## CASOS DE RUIDO

### C13 — Reranking

Los candidatos autorizados contienen resultados relevantes y ruido.

Esperado:
- el reranker mejora el orden;
- no altera autorización ni estado.

### C14 — Reranker sin poder de gobierno

Un candidato no autorizado tendría el mayor score.

Esperado:
- nunca entra en el conjunto que el reranker recibe como autorizado.

## REGLA DE INTERPRETACIÓN

Un resultado de retrieval puede demostrar pertinencia, pero no autoriza una decisión del sistema sobre la persona.

El RAG suministra conocimiento/contexto trazable. La decisión pertenece a las capas que tengan expresamente esa función.
