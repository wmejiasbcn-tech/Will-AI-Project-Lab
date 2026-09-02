# HARNESS-GUIDE-LOADING-TEST-001 — Prueba de carga de Guide

**Estado:** A — ACREDITADA por ejecución real del workflow `Arnés — Guide Load`.

## Resultado

- Workflow: `Arnés — Guide Load`
- Run: `33606459694`
- Check: `Carga de Guide del Arnés` — `success`
- Commit: `cac1fa094d0e28a0113a94e3b0cf559765c12c9e`
- Artefacto: `harness-guide-load-evidence-33606459694`
- Artifact ID: `9837196795`
- Digest: `sha256:1c639dda30ea837cab5cf9bcf0c227b161f6dd0775a62ed13903b42ffb91f0d7`

## Criterios de aceptación acreditados

- la ruta allowlisted existe;
- la ruta no es symlink;
- los marcadores estructurales mínimos existen;
- se genera `harness-feedforward.json`;
- el registro identifica `GUIDE-ARNES-COMANDO-05`;
- el payload contiene el contenido de la Guide;
- el SHA-256 corresponde exactamente al contenido cargado;
- el estado es `LOADED_FOR_PREPARATION`;
- el loader declara `NOT_EXECUTED_BY_LOADER`;
- el loader declara `NOT_GRANTED`;
- la salida es un archivo regular;
- la evidencia se conserva como artefacto.

La prueba acredita carga/preparación del payload, no ejecución, autorización ni verificación de verdad material de la Guide.
