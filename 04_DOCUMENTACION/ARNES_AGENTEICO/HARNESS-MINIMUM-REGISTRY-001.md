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
| `GUIDE-ARNES-COMANDO-05.md` | C | repositorio | Guide propuesta |
| `.github/workflows/integrity.yml` | A | workflow + ejecución | A — integración de verificación/feedback acreditada por ejecución |
| `06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py` | A | ejecutable + ejecución | A — integrado como mecanismo de verificación del Harness |
| `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py` | A | repositorio + ejecución | A — sensor mínimo de feedback ejecutado |
| `HARNESS-VERIFICATION-INTEGRATION-001.md` | C | repositorio | propuesta documental de integración |
| `HARNESS-SENSOR-FEEDBACK-001.md` | C | repositorio | especificación documental del sensor |
| `HARNESS-INTEGRATION-TEST-001.md` | A | repositorio + ejecución real | A — prueba mínima acreditada |

## 3. Evidencia de ejecución

**A:** Workflow `Integridad canónica`, run `33596370801`, asociado al PR #35 y al commit de trabajo `0d4da531ff8d626384eeb1741fac69ab608792ec`.

La ejecución acreditó:

- verificación de integridad: `success`;
- código de salida del verificador: `0`;
- ejecución del sensor: `success`;
- estado observado: `VERIFICATION_OBSERVED_SUCCESS`;
- generación y conservación de `harness-feedback.json`;
- artefacto de evidencia finalizado correctamente;
- reflejo del resultado en el resumen del workflow.

## 4. Regla de no sobreinterpretación

La inclusión de una pieza en este registro demuestra únicamente su localización/evidencia correspondiente. No convierte una pieza C en canónica ni amplía las jurisdicciones del Arnés.

El sensor observa el resultado del verificador; no lo sustituye ni añade autoridad epistemológica.

## 5. Estado de Sensors

**A — ACREDITADO para el mínimo implementado:** existe y se ejecutó `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py`, integrado en `Integridad canónica` y conservado como parte del artefacto de evidencia.

**D — NO DETERMINADO:** catálogo completo de Sensors, cobertura general de observabilidad y arquitectura definitiva de feedback del Arnés.

## 6. Estado del mecanismo ejecutable

**A:** Existe un mecanismo ejecutable de integridad y una integración mínima acreditada mediante ejecución del workflow.

**A:** Existe un sensor mínimo de feedback acreditado mediante la misma ejecución.

**A:** La prueba mínima de integración está documentada en `HARNESS-INTEGRATION-TEST-001.md` y respaldada por ejecución real.

Esto no demuestra por sí solo integración de Graphify, Positrón, Ollama, Vár/Yata ni ninguna otra pieza no acreditada.

## 7. Límite alcanzado

El materializado mínimo previsto en la secuencia explícita de `HARNESS-SPEC-001` ha quedado cubierto en sus seis bloques funcionales: estructura documental/contractual, contrato SCI ↔ Arnés, Guide mínima, Sensors/Feedback mínimo, mecanismo de verificación e integración mínima.

El registro completo continúa como **C — PROPUESTA / NO VALIDADA** porque contiene piezas documentales C y porque el cierre del mínimo no convierte automáticamente el Arnés completo en operativo.

No se crea un bloque adicional sin una necesidad material acreditada.
