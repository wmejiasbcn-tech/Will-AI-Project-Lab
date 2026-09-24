# HARNESS-VERIFICATION-INTEGRATION-001 — Integración mínima de verificación del Arnés

**Estado:** C — PROPUESTA / NO VALIDADA

## 1. Propósito

Documentar la integración mínima y explícita entre el mecanismo ejecutable de integridad ya existente en WAIPL y el Arnés Agéntico, sin crear un segundo verificador ni atribuir capacidades adicionales.

## 2. Punto de integración

El punto de integración es el workflow existente:

`.github/workflows/integrity.yml`

El workflow continúa ejecutando como verificador:

`06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py`

La integración añadida hace que el resultado de esa ejecución produzca evidencia identificable del Arnés en la propia ejecución de GitHub Actions.

## 3. Evidencia producida

La ejecución genera:

- `harness-verification-evidence.json`
- `harness-verification.log`
- `harness-verification-exit-code.txt`

Estos archivos se conservan como artefacto de la ejecución con identificador:

`harness-verification-evidence-${{ github.run_id }}`

El resumen de la ejecución también refleja commit, resultado del verificador y referencia al artefacto.

## 4. Semántica de la evidencia

La evidencia identifica, como mínimo:

- tipo de evidencia: `HARNESS_VERIFICATION`;
- verificador ejecutado;
- workflow;
- `run_id`;
- commit;
- resultado de la ejecución;
- archivos de log y código de salida.

La evidencia demuestra la ejecución del mecanismo en ese run. No demuestra por sí sola autorización, verdad material de los contenidos verificados, integración con Graphify, Positrón u Ollama, ni funcionamiento de sensores del Arnés.

## 5. Límites

No se crea:

- una FSM nueva del Arnés;
- un sensor nuevo;
- un segundo mecanismo de integridad;
- una sustitución de SCI;
- una nueva autoridad de verificación;
- una inferencia sobre Aletheia.

Aletheia mantiene su jurisdicción independiente de contraste.

## 6. Criterio de validación pendiente

Este documento permanece en C hasta disponer de una ejecución del workflow que acredite físicamente:

1. ejecución del verificador;
2. generación de la evidencia;
3. conservación del artefacto;
4. reflejo del resultado en el resumen de GitHub Actions.

Si la ejecución falla, se conserva la evidencia del fallo y se analiza únicamente la incidencia material correspondiente.

## 7. Regla de continuidad

No se considerará cerrada la integración por el mero hecho de que el código o la documentación existan. La clasificación podrá elevarse únicamente con evidencia de ejecución suficiente.
