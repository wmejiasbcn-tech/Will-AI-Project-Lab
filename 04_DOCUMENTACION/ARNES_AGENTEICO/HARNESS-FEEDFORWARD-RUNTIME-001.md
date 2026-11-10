# HARNESS-FEEDFORWARD-RUNTIME-001 — Consumidor runtime mínimo

**Estado:** A — ACREDITADO. Criterio de la §5 cumplido por los runs 33621691846 (2026-09-02, 12:52:22 CEST) y 35987054626 (2026-09-24, 12:24:41 CEST) en `main`, artefacto `harness-feedforward-runtime-evidence-35987054626`. El consumidor no ejecuta la Guide (`GUIDE-ARNES-COMANDO-05.md` permanece en C) ni concede autoridad (`authority = NOT_GRANTED`).

## 1. Propósito

Materializar el consumidor mínimo del payload `harness-feedforward.json` generado por el loader del Arnés.

## 2. Alcance

El consumidor:

1. lee el payload ya materializado;
2. valida su estructura mínima;
3. vuelve a calcular SHA-256 sobre `guide_content`;
4. rechaza discrepancias de integridad;
5. incorpora el contenido del Guide a `harness-runtime-context.json`;
6. marca `CONSUMED_FOR_RUNTIME_CONTEXT`.

## 3. Límites

El consumidor no:

- ejecuta la Guide;
- concede autoridad;
- decide permisos;
- comunica por SCI;
- sustituye Vár/Yata;
- establece integración física con Graphy, Positrón, Ollama, Emily o Hermes;
- define una FSM interna del Arnés.

## 4. Artefactos

- `06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime.py`
- `06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime_test.py`
- `.github/workflows/harness-feedforward-runtime.yml`
- entrada: `harness-feedforward.json`
- salida: `06_SISTEMA_OPERATIVO/ARNES/harness-runtime-context.json`

## 5. Criterio de acreditación

La pieza solo pasa a A cuando una ejecución real demuestra carga del payload, validación de integridad, consumo en contexto runtime y conservación de evidencia.
