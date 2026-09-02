# HARNESS-MINIMUM-REGISTRY-001 — Registro mínimo materializado del Arnés

**Estado:** C — PROPUESTA / NO VALIDADA

## 1. Propósito

Registrar únicamente piezas físicamente localizadas que forman parte del materializado mínimo del Arnés, manteniendo separadas existencia, ejecutabilidad, operación y verificación.

## 2. Piezas registradas

| Pieza | Estado | Evidencia física | Integración Arnés |
|---|---|---|---|
| `HARNESS-SPEC-001.md` | A/B/C/D según sección | repositorio | documental |
| `HARNESS-SPEC-001-ERRATA-01.md` | A | repositorio | documental |
| `SCI-ARNES-CONTRACT-001.md` | A | repositorio | contractual |
| `GUIDE-ARNES-COMANDO-05.md` | C | repositorio + carga física acreditada | Guide de preparación materializada; contenido aún C |
| `06_SISTEMA_OPERATIVO/ARNES/harness_guide_loader.py` | A | repositorio + ejecución del workflow específico | A — mecanismo mínimo de carga/validación de Guide |
| `.github/workflows/harness-guide.yml` | A | workflow + ejecución | A — prueba automatizada de carga |
| `.github/workflows/integrity.yml` | A | workflow + ejecución | A — integración de verificación/feedback acreditada |
| `06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py` | A | ejecutable + ejecución | A — integrado como mecanismo de verificación del Harness |
| `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py` | A | repositorio + ejecución | A — sensor mínimo de feedback ejecutado |
| `HARNESS-VERIFICATION-INTEGRATION-001.md` | A | repositorio + ejecución | A — integración mínima acreditada |
| `HARNESS-SENSOR-FEEDBACK-001.md` | A | repositorio + ejecución | A — sensor mínimo acreditado |
| `HARNESS-INTEGRATION-TEST-001.md` | A | repositorio + ejecución real | A — prueba mínima acreditada |

## 3. Evidencia de ejecución previa

**A:** Workflow `Integridad canónica`, run `33596370801`, asociado al PR #35 y al commit de trabajo `0d4da531ff8d626384eeb1741fac69ab608792ec`.

La ejecución acreditó verificación, código de salida 0, sensor, feedback, artefacto y resumen del workflow.

## 4. Evidencia de carga de Guide

**A:** El mecanismo `harness_guide_loader.py` lee exclusivamente la Guide allowlisted `GUIDE-ARNES-COMANDO-05.md`, rechaza el path si es symlink, valida marcadores estructurales y genera `harness-feedforward.json` con hash SHA-256, estado `LOADED_FOR_PREPARATION`, ejecución `NOT_EXECUTED_BY_LOADER` y autoridad `NOT_GRANTED`.

**A:** `harness-guide.yml` ejecuta el loader, valida el registro generado y conserva la evidencia como artefacto.

La carga acreditada significa **preparación/feedforward**, no ejecución de la Guide ni concesión de autoridad.

## 5. Regla de no sobreinterpretación

La inclusión de una pieza demuestra únicamente la localización/evidencia indicada. No convierte una pieza C en canónica ni amplía jurisdicciones.

## 6. Estado de Sensors

**A — ACREDITADO para el mínimo implementado:** existe y se ejecutó el sensor mínimo de feedback.

**D — NO DETERMINADO:** catálogo completo de Sensors, cobertura general y arquitectura definitiva de feedback.

## 7. Estado del mecanismo ejecutable

**A:** existe mecanismo ejecutable de integridad, integración mínima y sensor mínimo acreditados mediante ejecución.

**A:** existe mecanismo mínimo de carga/validación de Guide y ejecución automatizada de su prueba.

Esto no demuestra por sí solo integración de Graphify, Positrón, Ollama, Vár/Yata ni ninguna pieza no acreditada.

## 8. Límite alcanzado

El mínimo físico previsto incorpora ahora también el mecanismo de carga/validación de Guide. No se declara con ello el Arnés completo como operativo.

Permanecen D la FSM interna completa, catálogo completo de Sensors, Context Engineering definitivo e integraciones no acreditadas. La Guide concreta mantiene C hasta su contraste/validación correspondiente.
