# HARNESS-FEEDFORWARD-RUNTIME-001 — Consumidor runtime mínimo

**Estado:** C — PROPUESTA / NO VALIDADA hasta ejecución real y contraste.

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
- establece integración física con Graphify, Positrón, Ollama, Emily o Hermes;
- define una FSM interna del Arnés.

## 4. Artefactos

- `06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime.py`
- `06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime_test.py`
- `.github/workflows/harness-feedforward-runtime.yml`
- entrada: `harness-feedforward.json`
- salida: `06_SISTEMA_OPERATIVO/ARNES/harness-runtime-context.json`

## 5. Criterio de acreditación

La pieza solo pasa a A cuando una ejecución real demuestra carga del payload, validación de integridad, consumo en contexto runtime y conservación de evidencia.
