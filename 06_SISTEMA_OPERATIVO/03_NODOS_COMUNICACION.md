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
| Neo | Vortice / Kuiper | Protocolos, contraste 180 | Problema, propuesta |
| Perplexity | Vortice / Kuiper | Verificacion externa | Pregunta, fuentes, fecha |
| NotebookLM | Vortice / Kuiper | Sintesis de corpus | Documentos, pregunta |
| Nexus | Vortice / Kuiper | Pruebas, contraste tecnico | Hipotesis, material |
| Nauta | Vortice / Kuiper | Codex / mesa de control | Paquete operativo |
| GPAI | Borde puntual | Participacion puntual 2026-08-18 | Mandato, limite temporal |
| Qwen | Ingeniero jefe | Auditoria AEA | Sample, umbral, N3 |
| Ollama | Local LLM | Inferencia local | Endpoint 11434 UP/DOWN |
| Positron | UNKNOWN | Auditoria (sin URI) | No enviar hasta URI |

**Aether-Hermes no existe.** Aether = Nucleo. Hermes = director operativo.

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
