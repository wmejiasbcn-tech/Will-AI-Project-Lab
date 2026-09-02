# HARNESS-GUIDE-LOADING-001 — Mecanismo mínimo de carga de Guides

**Estado:** A — ACREDITADO para el mecanismo mínimo de carga/preparación de `GUIDE-ARNES-COMANDO-05`.

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

## 4. Verificación acreditada

Workflow: `Arnés — Guide Load`

Run: `33606459694`

Check: `Carga de Guide del Arnés` — `success`

Commit: `cac1fa094d0e28a0113a94e3b0cf559765c12c9e`

Artefacto: `harness-guide-load-evidence-33606459694`

Artifact ID: `9837196795`

Digest: `sha256:1c639dda30ea837cab5cf9bcf0c227b161f6dd0775a62ed13903b42ffb91f0d7`

La prueba validó identidad, estructura, contenido, correspondencia SHA-256 y estados del payload, y conservó la evidencia como artefacto.

## 5. Distinción de estados

```text
DOCUMENTADA
→ CARGADA PARA PREPARACIÓN
≠ EJECUTADA
≠ AUTORIZADA
≠ VERIFICADA COMO VERDAD MATERIAL
```

La ejecución acredita carga/preparación del payload. No acredita que un runtime de agente concreto lo consuma.

## 6. Alcance deliberadamente limitado

Este mecanismo resuelve únicamente la carga/preparación de la Guide concreta identificada. No declara un catálogo universal de Guides, plugins, FSM interna del Arnés ni un mecanismo general de Context Engineering.

La integración de consumo del payload por un runtime de agente concreto permanece sin acreditar y deberá tratarse como bloque independiente si resulta material para la siguiente fase.
