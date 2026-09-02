# HARNESS-GUIDE-LOADING-001 — Mecanismo mínimo de carga de Guides

**Estado:** A — ACREDITADO para el mecanismo mínimo de carga/preparación de la Guide identificada.

## 1. Objetivo

Cerrar el vacío material relativo a cómo una Guide del Arnés pasa de existir como documento a estar disponible como feedforward de preparación antes de una ejecución.

## 2. Mecanismo

El mecanismo físico es:

`06_SISTEMA_OPERATIVO/ARNES/harness_guide_loader.py`

El loader:

1. accede únicamente a la ruta allowlisted de `GUIDE-ARNES-COMANDO-05.md`;
2. rechaza la Guide si la ruta es un symlink;
3. carga el contenido UTF-8;
4. comprueba marcadores estructurales mínimos;
5. calcula SHA-256 del contenido cargado;
6. genera `harness-feedforward.json`;
7. marca el estado como `LOADED_FOR_PREPARATION`.

## 3. Límite de autoridad

El loader no ejecuta la Guide, no interpreta sus reglas, no concede autorización y no sustituye al Soberano, SCI, Aletheia, Vár, Yata, Graphify, Positrón u Ollama.

`authority = NOT_GRANTED`

## 4. Verificación

`.github/workflows/harness-guide.yml` ejecuta el loader en cada `push`, `pull_request` y `workflow_dispatch`, valida el registro de salida y conserva `harness-feedforward.json` como artefacto.

## 5. Distinción de estados

```text
DOCUMENTADA
→ CARGADA PARA PREPARACIÓN
≠ EJECUTADA
≠ AUTORIZADA
≠ VERIFICADA COMO VERDAD MATERIAL
```

La carga queda acreditada únicamente como preparación/feedforward.

## 6. Alcance deliberadamente limitado

Este mecanismo resuelve la brecha de carga identificada para la Guide concreta. No declara un catálogo universal de Guides, un sistema dinámico de plugins, una FSM interna del Arnés ni un mecanismo general de Context Engineering.

Esos elementos permanecen D — NO DETERMINADOS hasta disponer de evidencia específica.
