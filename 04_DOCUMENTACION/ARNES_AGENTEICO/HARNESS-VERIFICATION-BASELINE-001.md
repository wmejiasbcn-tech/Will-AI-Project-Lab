# HARNESS-VERIFICATION-BASELINE-001 — Línea base de verificación del Arnés

**Estado:** A — ACREDITADO como mecanismo de verificación existente; la integración específica con el Arnés permanece D.

## 1. Alcance

Este artefacto registra un mecanismo de verificación que ya existe físicamente en WAIPL y que puede aportar evidencia al desarrollo del Arnés sin atribuirle una integración que todavía no está acreditada.

## 2. Mecanismo existente

El repositorio dispone del workflow `.github/workflows/integrity.yml`, denominado `Integridad canónica`.

El workflow se ejecuta en `push`, `pull_request` y `workflow_dispatch`, utiliza permisos de solo lectura sobre contenidos y ejecuta:

```text
python3 06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py
```

El script existente realiza comprobaciones SHA-256 sobre el manifiesto canónico y otras comprobaciones de integridad del repositorio.

## 3. Evidencia de ejecución

En el commit `8ea9a2fe475b4c7166b2f23ead482c357e335704` de `repo-cleanup-github` existe estado global `success` en GitHub. Esta evidencia incluye estados de Buildkite y despliegues Vercel satisfactorios.

**Nota:** el estado citado no se interpreta por sí mismo como prueba de una integración Arnés específica.

## 4. Frontera epistemológica

Este artefacto distingue:

- **A:** el mecanismo de integridad existe y es ejecutable en el repositorio.
- **D:** no está acreditado todavía que el Arnés lo invoque, consuma su resultado o lo incorpore como sensor interno.

No se crea un adaptador, sensor ni nueva integración para cerrar artificialmente ese vacío.

## 5. Criterio de continuidad

La siguiente materialización puede utilizar este mecanismo como evidencia externa de verificación del estado del repositorio mientras no exista una decisión válida que establezca una integración específica con el Arnés.
