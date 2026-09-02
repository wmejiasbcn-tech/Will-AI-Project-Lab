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
| `GUIDE-ARNES-COMANDO-05.md` | C | repositorio | Guide propuesta; carga/preparación acreditada |
| `06_SISTEMA_OPERATIVO/ARNES/harness_guide_loader.py` | A | repositorio + ejecución real | A — mecanismo físico de carga/preparación |
| `.github/workflows/harness-guide.yml` | A | workflow + ejecución real | A — prueba automatizada de carga |
| `HARNESS-GUIDE-LOADING-001.md` | A | repositorio + ejecución real | A — especificación acreditada del mecanismo |
| `HARNESS-GUIDE-LOADING-TEST-001.md` | A | repositorio + ejecución real | A — prueba mínima acreditada |
| `.github/workflows/integrity.yml` | A | workflow + ejecución | A — integración de verificación/feedback acreditada por ejecución |
| `06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py` | A | ejecutable + ejecución | A — integrado como mecanismo de verificación del Harness |
| `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py` | A | repositorio + ejecución | A — sensor mínimo de feedback ejecutado |
| `HARNESS-VERIFICATION-INTEGRATION-001.md` | C | repositorio | propuesta documental de integración |
| `HARNESS-SENSOR-FEEDBACK-001.md` | C | repositorio | especificación documental del sensor |
| `HARNESS-INTEGRATION-TEST-001.md` | A | repositorio + ejecución real | A — prueba mínima acreditada |

## 3. Evidencia de ejecución existente

**A:** Workflow `Integridad canónica`, run `33596370801`, asociado al PR #35 y al commit de trabajo `0d4da531ff8d626384eeb1741fac69ab608792ec`.

La ejecución acreditó verificación de integridad, código de salida 0, sensor, feedback, artefacto y resumen del workflow.

**A:** Workflow `Arnés — Guide Load`, run `33606459694`, sobre `main` en commit `cac1fa094d0e28a0113a94e3b0cf559765c12c9e`.

La ejecución acreditó el loader, validación del payload, correspondencia SHA-256 y conservación del artefacto `harness-guide-load-evidence-33606459694` (ID `9837196795`, digest `sha256:1c639dda30ea837cab5cf9bcf0c227b161f6dd0775a62ed13903b42ffb91f0d7`).

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

**A:** Existe y se ejecutó el mecanismo mínimo de carga/preparación de Guide, con evidencia automatizada y artefacto retenido.

Esto no demuestra por sí solo integración de Graphify, Positrón, Ollama, Vár/Yata ni ninguna otra pieza no acreditada.

## 7. Límite alcanzado

El mínimo físico ya acreditado cubre estructura documental/contractual, contrato SCI ↔ Arnés, Guide documental, carga/preparación de Guide, Sensors/Feedback mínimo, verificación e integración mínima.

La carga/preparación de Guide queda cerrada como mecanismo físico acreditado. **No queda cerrada la integración de consumo del payload por un runtime de agente concreto**, porque la ejecución realizada no demuestra ese consumo.

Permanecen D la FSM interna completa, catálogo completo de Sensors, Context Engineering definitivo e integraciones no acreditadas.

No se crea un bloque adicional sin una necesidad material acreditada.
