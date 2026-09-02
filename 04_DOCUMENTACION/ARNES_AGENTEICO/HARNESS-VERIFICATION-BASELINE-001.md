# HARNESS-VERIFICATION-BASELINE-001 — Línea base de verificación del Arnés

**Estado:** A — ACREDITADO como mecanismo de verificación existente e integración mínima específica con el Arnés acreditada por ejecución; no implica que constituya una meta-verificación ni una autoridad nueva.

## 1. Alcance

Este artefacto registra un mecanismo de verificación que ya existe físicamente en WAIPL y cuya integración mínima con el Arnés quedó acreditada mediante ejecución del workflow.

## 2. Mecanismo existente

El repositorio dispone del workflow `.github/workflows/integrity.yml`, denominado `Integridad canónica`.

El workflow se ejecuta en `push`, `pull_request` y `workflow_dispatch`, utiliza permisos de solo lectura sobre contenidos y ejecuta:

```text
python3 06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py
```

El script existente realiza comprobaciones SHA-256 sobre el manifiesto canónico y otras comprobaciones de integridad del repositorio.

## 3. Evidencia de integración

La integración mínima quedó acreditada mediante `HARNESS-INTEGRATION-TEST-001`, respaldado por la ejecución real del workflow registrada en el repositorio.

La ejecución demostró la cadena mínima:

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

## 4. Frontera epistemológica

Este artefacto distingue:

- **A:** el mecanismo de integridad existe y es ejecutable en el repositorio.
- **A:** su integración mínima con el Arnés está acreditada en el circuito documentado y probado.
- **D:** no está determinada una meta-verificación adicional ni una arquitectura completa de Sensors/observabilidad.

No se atribuye al mecanismo autoridad adicional ni integración con Graphify, Positrón, Ollama, Vár o Yata fuera de lo explícitamente acreditado.

## 5. Criterio de continuidad

El mecanismo puede utilizarse como punto de verificación del estado del repositorio dentro del circuito mínimo acreditado, manteniendo la separación entre verificación, feedback y autoridad.
