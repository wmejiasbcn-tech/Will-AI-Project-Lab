# HARNESS-GUIDE-LOADING-001 — Mecanismo mínimo de carga de Guides

**Estado:** C — PROPUESTA / NO VALIDADA hasta ejecución real del workflow específico.

## 1. Objetivo

Materializar el paso físico entre la Guide documental y un payload de preparación/feedforward disponible para una ejecución posterior, sin ejecutar la Guide ni conceder autoridad.

## 2. Mecanismo

El mecanismo físico es:

`06_SISTEMA_OPERATIVO/ARNES/harness_guide_loader.py`

El loader:

1. accede únicamente a la ruta allowlisted de `GUIDE-ARNES-COMANDO-05.md`;
2. rechaza la Guide si la ruta es un symlink;
3. carga el contenido UTF-8;
4. comprueba marcadores estructurales mínimos;
5. calcula SHA-256 del contenido cargado;
6. genera `harness-feedforward.json` incluyendo el contenido cargado y su hash;
7. marca el estado como `LOADED_FOR_PREPARATION`;
8. escribe la salida mediante reemplazo atómico y comprueba que el destino sea un archivo regular.

## 3. Límite de autoridad

El loader no ejecuta la Guide, no interpreta sus reglas, no concede autorización y no sustituye al Soberano, SCI, Aletheia, Vár, Yata, Graphify, Positrón u Ollama.

`authority = NOT_GRANTED`

## 4. Verificación

`.github/workflows/harness-guide.yml` ejecuta el loader, valida identidad, estructura, contenido, hash y estados del payload, y conserva `harness-feedforward.json` como artefacto.

La ejecución real del workflow es necesaria para elevar este documento de C a A respecto del mecanismo físico acreditado.

## 5. Distinción de estados

```text
DOCUMENTADA
→ CARGADA PARA PREPARACIÓN
≠ EJECUTADA
≠ AUTORIZADA
≠ VERIFICADA COMO VERDAD MATERIAL
```

## 6. Alcance deliberadamente limitado

Este mecanismo resuelve únicamente la carga/preparación de la Guide concreta identificada. No declara un catálogo universal de Guides, plugins, FSM interna del Arnés ni un mecanismo general de Context Engineering.

La existencia de un payload preparado tampoco acredita que un runtime de agente concreto lo consuma; esa integración requerirá evidencia específica antes de declararse.
