# VÁR — VAC-01 · Casa Operativa

## Estado actual

**DRAFT IMPLEMENTADO · NO PUBLICADO · PENDIENTE DE AUTORIZACIÓN SOBERANA**

VÁR es el Agente/Nodo de Validación de la Verdad Canónica WAIPL. Su identificador operativo es **VAC-01**.

Esta carpeta constituye la **casa documental específica de VÁR dentro de `06_SISTEMA_OPERATIVO`**. Aquí se concentra el estado actual, la especificación operativa, las correcciones semánticas, la implementación n8n y los límites que deben conservarse cuando otros proyectos, agentes o sistemas consuman información sobre VÁR.

## Documentos de esta casa

- `VAR_DOSSIER_MAESTRO_ESTADO_2026-09-07.md` — informe maestro de estado y transferencia de contexto.
- `VAR_CANON_SEMANTICO_NO_DERIVA.md` — reglas de interpretación y conservación semántica.
- `VAR_IMPLEMENTACION_N8N_ESTADO.md` — estado de la implementación VÁR/VAC-01 en n8n.
- `YATA_ESTADO_Y_FRONTERA_CON_VAR.md` — estado de YATA y frontera funcional VÁR ↔ YATA.

## Regla de lectura

> **PRIMERO FUENTE → DESPUÉS REPRESENTACIÓN → DESPUÉS INTERPRETACIÓN.**

Nunca convertir una interpretación en una nueva fuente de verdad.

Cuando la documentación disponible no permita resolver una cuestión:

> **No especificado en las fuentes proporcionadas.**

## Fronteras críticas

- VÁR valida la verdad canónica dentro de su jurisdicción.
- YATA audita validadores de agentes, nodos, procesos y sistemas agénticos.
- VÁR y YATA son independientes.
- **YATA no audita VÁR.**
- WILLIAM-SCY-01 es el avatar del Soberano, no un distribuidor ni gateway.
- En el draft actual, la conexión técnica representada es **VÁR → WILLIAM-SCY-01**.
- Positrón, Hermes, Graphy, Ollama y Carla permanecen como destinos previstos sin conexión activa en el estado actual de F7.

## Fuente de verdad documental

El repositorio GitHub es la fuente documental del proyecto. Esta casa no crea una arquitectura paralela: organiza y hace explícito el estado actual de VÁR para que los demás proyectos puedan consumirlo sin reconstruirlo por memoria o inferencia.
