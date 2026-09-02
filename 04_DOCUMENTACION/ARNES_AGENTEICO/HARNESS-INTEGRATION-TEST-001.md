# HARNESS-INTEGRATION-TEST-001 — Prueba mínima de integración del Arnés

**Estado:** A — ACREDITADO
**Responsable operativo:** Carla
**Capa de contraste:** Aletheia

## 1. Objetivo

Acreditar la integración mínima entre:

```text
verificador existente
      ↓
evidencia Harness
      ↓
sensor de feedback
      ↓
artefacto persistente
      ↓
resumen del workflow
```

Sin introducir una segunda batería de verificación.

## 2. Ejecución acreditada

**Workflow:** `Integridad canónica`

**Run:** `33596370801`

**PR:** `#35`

**Commit de la rama:** `0d4da531ff8d626384eeb1741fac69ab608792ec`

## 3. Resultado observado

**A:** El job `verify` terminó con `success`.

**A:** El verificador `06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py` terminó correctamente con código `0` y reportó `--- INTEGRIDAD OK ---`.

**A:** La etapa `Publicar evidencia del Arnés` terminó correctamente.

**A:** El sensor `06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py` terminó correctamente y produjo:

`feedback_state = VERIFICATION_OBSERVED_SUCCESS`

con `verification_exit_code = 0`.

**A:** La etapa de conservación confirmó la subida de cuatro ficheros al artefacto de GitHub Actions:

- `harness-verification-evidence.json`;
- `harness-verification.log`;
- `harness-verification-exit-code.txt`;
- `harness-feedback.json`.

**A:** El artefacto quedó finalizado correctamente con ID `9833526639` y digest SHA-256 `e5f965f884afe0798e328614ea0b5c574c8afe04d91ee8943c51093ab9f7cd52`.

**A:** El workflow reflejó el resultado de verificación y la presencia del sensor en `GITHUB_STEP_SUMMARY`.

## 4. Qué acredita esta prueba

Acredita únicamente la integración mínima ejecutada entre verificación, evidencia, feedback y persistencia dentro del workflow.

## 5. Qué NO acredita

No acredita:

- integración física Graphify ↔ Arnés;
- integración física Positrón ↔ Arnés;
- integración física Ollama ↔ Arnés;
- operación de Vár/Yata dentro de este circuito;
- catálogo completo de Sensors;
- arquitectura definitiva de Context Engineering;
- nueva autoridad o permiso;
- FSM interna completa del Arnés;
- operación general del Arnés fuera de este circuito mínimo.

## 6. Criterio de cierre

El mínimo definido para la prueba de integración queda **acreditado** por ejecución real observable y persistencia de evidencia.

El cierre de esta prueba no equivale a declarar el Arnés completo como operativo ni a convertir las piezas documentales C en canónicas.
