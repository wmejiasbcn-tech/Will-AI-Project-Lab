# HARNESS-FEEDFORWARD-RUNTIME-TEST-001 — Prueba mínima

**Estado:** C — PROPUESTA / NO VALIDADA hasta ejecución real.

## Prueba

La prueba ejecuta el consumidor después del loader y comprueba:

- payload presente;
- contexto runtime materializado;
- `guide_id` conservado;
- SHA-256 conservado y coincidente;
- contenido del Guide conservado;
- estado `CONSUMED_FOR_RUNTIME_CONTEXT`;
- `execution = NOT_EXECUTED_BY_CONSUMER`;
- `authority = NOT_GRANTED`.

## Evidencia

La evidencia será el artefacto del workflow `Arnés — Feedforward Runtime`.
