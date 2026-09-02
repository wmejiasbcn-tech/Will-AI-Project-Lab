# HARNESS-GUIDE-LOADING-TEST-001 — Prueba de carga de Guide

**Estado:** C — NO VALIDADA hasta ejecución real del workflow `Arnés — Guide Load`.

## Criterios de aceptación

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
