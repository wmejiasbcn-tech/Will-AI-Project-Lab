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
| `06_SISTEMA_OPERATIVO/ARNES/harness_guide_loader.py` | C | repositorio | mecanismo físico de carga/preparación, pendiente de ejecución real |
| `.github/workflows/harness-guide.yml` | C | repositorio | prueba automatizada de carga, pendiente de ejecución real |
| `HARNESS-GUIDE-LOADING-001.md` | C | repositorio | especificación del mecanismo de carga |
| `HARNESS-GUIDE-LOADING-TEST-001.md` | C | repositorio | criterios de aceptación pendientes de ejecución |
| `.github/workflows/integrity.yml` | A | workflow + ejecución | A — integración de verificación/feedback acreditada por ejecución |
| `06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py` | A | ejecutable + ejecución | A — integrado como mecanismo de verificación del Harness |
| `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py` | A | repositorio + ejecución | A — sensor mínimo de feedback ejecutado |
| `HARNESS-VERIFICATION-INTEGRATION-001.md` | C | repositorio | propuesta documental de integración |
| `HARNESS-SENSOR-FEEDBACK-001.md` | C | repositorio | especificación documental del sensor |
| `HARNESS-INTEGRATION-TEST-001.md` | A | repositorio + ejecución real | A — prueba mínima acreditada |

## 3. Evidencia de ejecución existente

**A:** Workflow `Integridad canónica`, run `33596370801`, asociado al PR #35 y al commit de trabajo `0d4da531ff8d626384eeb1741fac69ab608792ec`.

La ejecución acreditó verificación de integridad, código de salida 0, sensor, feedback, artefacto y resumen del workflow.

## 4. Evidencia de carga de Guide

La carga de Guide se encuentra materializada documental y físicamente, pero **todavía no acreditada por una ejecución real del workflow específico**.

El loader:

- usa una ruta allowlisted fija;
- rechaza la Guide si es symlink;
- valida marcadores estructurales;
- calcula SHA-256;
- incluye el contenido cargado en `harness-feedforward.json`;
- declara `LOADED_FOR_PREPARATION`;
- declara `NOT_EXECUTED_BY_LOADER`;
- declara `NOT_GRANTED`;
- escribe la salida mediante reemplazo atómico y comprueba que el destino sea un archivo regular.

El workflow valida identidad, estructura, contenido, hash y estados del payload y conserva el artefacto.

La evidencia de ejecución real será necesaria antes de elevar estos elementos a A.

## 5. Regla de no sobreinterpretación

La inclusión de una pieza en este registro demuestra únicamente su localización/evidencia correspondiente. No convierte una pieza C en canónica ni amplía las jurisdicciones del Arnés.

El sensor observa el resultado del verificador; no lo sustituye ni añade autoridad epistemológica.

## 6. Estado de Sensors

**A — ACREDITADO para el mínimo implementado:** existe y se ejecutó `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py`, integrado en `Integridad canónica` y conservado como parte del artefacto de evidencia.

**D — NO DETERMINADO:** catálogo completo de Sensors, cobertura general de observabilidad y arquitectura definitiva de feedback del Arnés.

## 7. Estado del mecanismo ejecutable

**A:** Existe un mecanismo ejecutable de integridad y una integración mínima acreditada mediante ejecución del workflow.

**A:** Existe un sensor mínimo de feedback acreditado mediante la misma ejecución.

**A:** La prueba mínima de integración está documentada en `HARNESS-INTEGRATION-TEST-001.md` y respaldada por ejecución real.

**C:** El mecanismo de carga de Guide está materializado pero pendiente de su primera ejecución real y evidencia asociada.

Esto no demuestra por sí solo integración de Graphify, Positrón, Ollama, Vár/Yata ni ninguna otra pieza no acreditada.

## 8. Límite alcanzado

El mínimo físico ya acreditado cubre estructura documental/contractual, contrato SCI ↔ Arnés, Guide documental, Sensors/Feedback mínimo, verificación e integración mínima.

El mecanismo físico específico de carga/preparación de Guide queda abierto exclusivamente hasta su ejecución real. Además, este mecanismo no demuestra por sí mismo que un runtime de agente concreto consuma el payload; esa integración requerirá evidencia específica.

No se crea un bloque adicional sin una necesidad material acreditada.
