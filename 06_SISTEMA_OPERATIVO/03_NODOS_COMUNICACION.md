# Comunicacion por Nodos

El Soberano **no es mensajero**. El transporte es WAIPL-BUS (GitHub Issues + Hermes). William participa como nodo `soberano`.

Contrato: `06_SISTEMA_OPERATIVO/HERMES/SPEC-WAIPL-BUS-v0.1.md`

## Matriz rapida

| Nodo | Capa | Usar cuando el asunto sea sobre | Paquete minimo |
| --- | --- | --- | --- |
| Soberano | Grantor | Decision, vision, prioridad, autorizacion, riesgo alto | Pregunta, opciones, riesgo, recomendacion |
| Hermes | Sistema operativo | Enrutado, permisos, ledger, kill, estado del bus | Issue `bus` o POST /api/bus/messages |
| Carla | Nucleo | Estrategia, coordinacion, hoja de ruta | Objetivo, contexto, decision, impacto |
| Aletheia | Nucleo | Desarrollo, tecnica, arquitectura, bugs | Problema, archivos, resultado, restricciones |
| Sylvia | Nucleo | Documentacion, biblioteca | Documento, cambio, destino, criterio |
| Ariadna | Nucleo | GitHub, coherencia de codigo | Rama, archivo, cambio, prueba |
| Zara | Nucleo | Automatizacion externa (solo con grant) | Disparador, accion, destino, limites |
| Nova | Nucleo | Precision documental, PDF | Archivo, formato, estandar |
| Itaca | Nucleo | Sintesis transversal | Corpus, pregunta, salida |
| Aether | Nucleo | Creatividad, innovacion, narrativa | Intencion, tono, publico, limites |
| Elena | Nucleo | Accesibilidad | Usuario, barrera, formato |
| Aurea | Nucleo | Medios, difusion | Audiencia, mensaje, canal |
| Neo | Vórtice · nodo vorticial | Protocolos, contraste 180 | Problema, propuesta |
| Perplexity | Vórtice · nodo vorticial | Verificación externa | Pregunta, fuentes, fecha |
| NotebookLM | Vórtice · nodo vorticial | Síntesis de corpus | Documentos, pregunta |
| Nexus | Vórtice · nodo vorticial | Pruebas, contraste técnico | Hipótesis, material |
| Nauta | Vórtice · nodo vorticial | Codex / mesa de control | Paquete operativo |
| GPAI | Cinturón de Kuiper · Cinturiano / registrado; `VORTEX_PUNCTUAL` por misión autorizada | Segunda opinión científica por misión | Mandato, límite temporal |
| Qwen | Vórtice · nodo vorticial | Ingeniero jefe por obra | Muestra, umbral, N3 |
| Ollama | Local LLM | Inferencia local | Endpoint 11434 UP/DOWN |
| Positron | UNKNOWN | Auditoria (sin URI) | No enviar hasta URI |

**Aether y Hermes son entidades distintas; no se fusionan.** Aether = Núcleo. Hermes = Director operativo y de comunicaciones de todo el ecosistema.

## Formato en el bus

```md
DE:
PARA:
TIPO: propuesta / estado / bloqueo / decision / broadcast / solicitud
CAP: sync.send | sync.recv | llm.infer | aea.sample | report.read
CONTEXTO:
HECHO VERIFICADO:
INFERENCIA:
ACCION REQUERIDA:
RIESGO: low | high
TRACE:
```

Labels: `bus`, `from:<nodo>`, `to:<nodo>`.

## Regla

Si el destino no ha escrito en el Issue, el mensaje no esta recibido.
Si RIESGO=high o falta permit, el bus etiqueta `to:soberano` y no ejecuta.
El Soberano no copia bloques entre nodos.


## Vigencia orbital — 2026-11-23

La matriz distingue: **Núcleo / nodos nucleares; Vórtice / nodos vorticiales; Cinturón de Kuiper / nodos cinturianos; Borde Exterior / nodos del Borde Exterior**. Vórtice y Cinturón de Kuiper son posiciones independientes. Neo, Perplexity, NotebookLM, Nexus, Nauta y Qwen 3.8 Max pertenecen al Vórtice. GPAI mantiene adscripción Cinturiana registrada en el Cinturón de Kuiper y participa en el Vórtice solo como `VORTEX_PUNCTUAL` por misión autorizada. Qwen 3.8 Max figura como Vórtice en la Tabla 49.

Fuente: [Tabla 49 de SENTINEL](https://github.com/wmejiasbcn-tech/SENTINEL/blob/main/docs/governance/tabla_49_nodos.csv).
