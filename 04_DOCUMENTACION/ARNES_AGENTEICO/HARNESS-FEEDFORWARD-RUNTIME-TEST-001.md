# HARNESS-FEEDFORWARD-RUNTIME-TEST-001 — Prueba mínima

**Estado:** A — ACREDITADO.

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

La evidencia es el artefacto `harness-feedforward-runtime-evidence-35987054626` del workflow `Arnés — Feedforward Runtime` (runs `33621691846`, 2026-09-02, 12:52:22 CEST, y `35987054626`, 2026-09-24, 12:24:41 CEST). La prueba imprimió `FEEDFORWARD_RUNTIME_CONSUMED`. El consumidor no ejecuta la Guide (`GUIDE-ARNES-COMANDO-05.md` permanece en C) ni concede autoridad (`authority = NOT_GRANTED`).
