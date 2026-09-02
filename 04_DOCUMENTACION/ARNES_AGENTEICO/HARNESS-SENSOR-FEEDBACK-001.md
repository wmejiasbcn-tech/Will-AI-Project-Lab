# HARNESS-SENSOR-FEEDBACK-001 — Sensor mínimo de Feedback del Arnés Agéntico WAIPL

**Estado:** A — ACREDITADO para el sensor mínimo implementado y ejecutado.
**Responsable operativo:** Carla
**Capa de contraste:** Aletheia
**Jurisdicción:** Arnés Agéntico WAIPL

## 1. Propósito

Materializar el mínimo físico de Sensors/Feedback requerido por `HARNESS-SPEC-001`, sin crear una segunda verificación ni atribuir al sensor autoridad epistemológica o de gobernanza.

El sensor **observa** el resultado ya producido por el mecanismo de verificación existente y genera un registro de feedback identificable.

## 2. Artefacto físico

**A:** `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py`

El sensor consume únicamente:

- `harness-verification-exit-code.txt`;
- resultado de la etapa `integrity` del workflow;
- `run_id`;
- commit ejecutado.

Produce:

- `harness-feedback.json`.

## 3. Integración física mínima

**A:** `.github/workflows/integrity.yml` invoca el sensor mediante el paso `Capturar feedback del Arnés` con `if: always()`.

**A:** El workflow conserva `harness-feedback.json` mediante un artefacto de GitHub Actions.

**A:** El fallo del sensor no constituye una condición de validez del mecanismo de integridad; el paso del sensor y la conservación de su feedback son no bloqueantes.

## 4. Semántica

El sensor distingue como mínimo:

- `VERIFICATION_OBSERVED_SUCCESS`;
- `VERIFICATION_OBSERVED_FAILURE`;
- `VERIFICATION_FEEDBACK_NOT_AVAILABLE`.

Estas etiquetas describen lo observado por el sensor. No constituyen por sí mismas una decisión de autorización, una declaración de verdad material ni una nueva verificación.

## 5. Límites de jurisdicción

El sensor:

- no ejecuta `verify_integrity.py` por sí mismo;
- no sustituye al verificador;
- no concede permisos;
- no decide autoridad;
- no determina verdad epistemológica;
- no sustituye a Vár/Yata;
- no modifica Graphify, Positrón u Ollama;
- no crea una FSM interna del Arnés;
- no define nuevas reglas de gobernanza.

## 6. Evidencia de operación

`HARNESS-INTEGRATION-TEST-001` acredita mediante ejecución real:

1. ejecución del verificador;
2. generación del código de salida;
3. ejecución del sensor;
4. generación de `harness-feedback.json`;
5. conservación del registro como artefacto;
6. reflejo del resultado en el resumen del workflow.

Por ello, el sensor mínimo implementado queda **A — ACREDITADO**.

## 7. No ampliación de alcance

Este sensor resuelve únicamente el vacío mínimo de observabilidad/feedback identificado en la especificación. No se declara con ello un catálogo completo de Sensors ni una arquitectura definitiva de observabilidad del Arnés.

El catálogo completo, la cobertura general y la arquitectura definitiva de feedback permanecen **D — NO DETERMINADOS**.
