# HARNESS-GUIDE-LOADING-TEST-001 — Prueba de carga de Guide

**Estado:** A — ACREDITADO por ejecución automatizada del workflow `Arnés — Guide Load`.

## Criterios

- la ruta allowlisted existe;
- la ruta no es symlink;
- los marcadores estructurales mínimos existen;
- se genera `harness-feedforward.json`;
- el registro identifica `GUIDE-ARNES-COMANDO-05`;
- el hash SHA-256 tiene 64 caracteres;
- el registro declara `LOADED_FOR_PREPARATION`;
- el loader declara `NOT_EXECUTED_BY_LOADER`;
- el loader declara `NOT_GRANTED`;
- la evidencia se conserva como artefacto.

La prueba acredita carga/preparación, no ejecución ni autorización de la Guide.
