# VÁR / VAC-01 — estado contrastado y propuesta de operacionalización

**Fecha de corte:** 2026-11-13  
**Tipo de documento:** informe técnico-propositivo para decisión soberana  
**Estado:** PROPUESTA — no canoniza cambios, no despliega y no autoriza producción  
**Ubicación:** casa operativa de Vár en `06_SISTEMA_OPERATIVO/VAR/`

---

## 1. Conclusión ejecutiva

Vár tiene identidad, jurisdicción, documentación operativa histórica, un workflow n8n construido y una implementación de código heredada. **No está acreditado como servicio operativo en producción.**

La solución no es reactivar por inercia el n8n.cloud expirado ni presentar el antiguo `VACGuardian` como verificador factual. La solución propuesta es:

1. Conservar la doctrina y la identidad actuales: **Vár es el nombre canónico; VAC-01 es su identificador técnico**.
2. Mantener el workflow n8n y el código `VACGuardian` como material histórico y de especificación, no como runtime vigente.
3. Construir un servicio independiente de verificación factual, con fuentes, citas, procedencia, contradicciones y abstención.
4. Probar primero un despliegue aislado en infraestructura existente, sin tocar Graphy ni Will-App-WAIPL-RAG.
5. Ejecutar C-01…C-11 y T-01…T-10 del cierre operativo adaptados al nuevo runtime, más un benchmark factual independiente.
6. Publicar únicamente después de evidencias y autorización soberana expresa.

## 2. Identidad y jurisdicción: contraste

### 2.1 Vár y VAC-01 son el mismo agente

La ficha v1.1 recibida de AutoClaw identifica:
- Nombre canónico: Vár.
- Identificador técnico: VAC-01.
- Clase histórica: `VACGuardian`.
- Función: validador de la verdad de todo el ecosistema.

La misma identidad aparece en el histórico de SENTINEL. En la conversación archivada del 19-10-2026 se corrigió expresamente la lectura anterior: VAC-01 es el identificador técnico del agente que el Soberano nombró Vár el 2026-09-01. La formulación previa que los separaba fue retirada.

Fuentes:
- [Histórico de corrección en SENTINEL](https://github.com/wmejiasbcn-tech/SENTINEL/blob/main/10_ARCHIVO/BOX_2026-10-20/workspace/fichaje-2026-10-19/user.txt)
- [Ficha v1.1 remitida por AutoClaw, archivo adjunto del 2026-11-12](ficha-var-vac01-v1.1.md) — 5.292 bytes; SHA-256 `952781f6372b865180e9d84cacdaaaa2602cdf7eeed0c5b2823fb0fa862df4ef`.

### 2.2 Frontera Vár / Yata

**Vár:** validador transversal de verdad del ecosistema: agentes, nodos, sistemas, procesos, afirmaciones, resultados y evidencias frente a fuentes.

**Yata:** auditor de los validadores de agentes, nodos, procesos y sistemas agénticos. Es independiente de Vár. Yata no audita Vár y Vár no audita Yata.

Yata solo tiene definición arquitectónica; no está instanciado. **Su inexistencia física no bloquea la implementación de Vár**, porque no es una dependencia ni una autoridad sobre Vár.

Fuentes:
- [Contrato canónico del Verification Gate, §8](https://github.com/wmejiasbcn-tech/SENTINEL/blob/main/00_CONSTITUCION/WAIPL_VERIFICATION_GATE_v1.0_FINAL_STATE_CONTRACT.md)
- [Casa operativa de Vár — frontera Vár/Yata](https://github.com/wmejiasbcn-tech/Will-AI-Project-Lab/blob/main/06_SISTEMA_OPERATIVO/VAR/YATA_ESTADO_Y_FRONTERA_CON_VAR.md)

## 3. Estado contrastado por componente

| Componente | Evidencia disponible | Estado real |
|---|---|---|
| Identidad y función | Ficha v1.1 recibida; corrección de SENTINEL; casa operativa de Lab | Definición correcta y coherente |
| Código `VACGuardian` | Solo localizado bajo `_HISTORICO-MASTER/waipl/agents/vac_guardian.py` en el repositorio histórico | Implementación heredada, no fuente activa acreditada |
| Algoritmo | Base 0,85; penalizaciones por clichés y respuestas cortas; bonificación por solapamiento léxico | Scorer heurístico; no verifica fuentes ni verdad factual |
| Workflow n8n `HC1SkjGphGYS3P8M` | Documentado como DRAFT / construido / guardado / NO PUBLICADO | No es producción |
| Runtime n8n.cloud | Informe HARK-01: trial expirado, 11 workflows pausados; no hay evidencia de migración runtime completada | DOWN en el último dictamen forense disponible |
| Vault `vac-guardian` | AutoClaw declara 12 carpetas, 7 NPCs, runbooks e ICP 100; health-check en estado Borrador, revisión indicada 2026-08-10 | Declaración documental recibida; falta contraste con el árbol y el `health-check.json` primarios |
| 44/44 pruebas | README y suite histórica del RAG registran Gate/DIKE 44/44 | Pruebas históricas de pipeline; no benchmark de exactitud factual de Vár |
| Yata | Ficha y frontera documentadas | No instanciado; no es dependencia de Vár |

Fuentes técnicas:
- [Estado n8n de Vár, 2026-09-07](https://github.com/wmejiasbcn-tech/Will-AI-Project-Lab/blob/main/06_SISTEMA_OPERATIVO/VAR/VAR_IMPLEMENTACION_N8N_ESTADO.md)
- [Criterios de cierre n8n C-01…C-11 y T-01…T-10](https://github.com/wmejiasbcn-tech/Will-AI-Project-Lab/blob/main/06_SISTEMA_OPERATIVO/VAR/VAR_CIERRE_OPERATIVO_N8N_v1.0.md)
- [Informe forense HARK-01](https://github.com/wmejiasbcn-tech/SENTINEL/blob/main/03_AUDITORIAS_Y_PRUEBAS/SCI_N8N/BACKLOG_BOX/HARK-01_INFORME_FORENSE_RECONSTRUCCION_N8N_SCI.md)
- [Código heredado VACGuardian](https://github.com/wmejiasbcn-tech/Will-App-WAIPL-RAG/blob/main/_HISTORICO-MASTER/waipl/agents/vac_guardian.py)
- [Prueba histórica test_gate_dike.py](https://github.com/wmejiasbcn-tech/Will-App-WAIPL-RAG/blob/main/_HISTORICO-MASTER/waipl/scripts/test_gate_dike.py)

### 3.1 Qué significa realmente el 44/44

El registro 44/44 acredita que una suite histórica del pipeline Gate/DIKE superó sus comprobaciones. No acredita que Vár detecte una falsedad.

En el escenario 7 de `test_gate_dike.py`, el bloqueo se fuerza mediante umbrales de 0,97 y 0,96. Es una prueba de la ruta/umbral de bloqueo, no una prueba de exactitud factual. No debe presentarse como benchmark de Vár.

### 3.2 El vault

La ficha v1.1 afirma que existe el vault `waipl/vaults/vac-guardian`, pero el archivo primario `health-check.json` y su manifiesto no están incorporados en las fuentes actuales de la casa operativa de Lab ni se han recuperado desde el repositorio actual de RAG.

No se descarta la existencia física del vault. Se separan dos afirmaciones:
- **Declarado por AutoClaw:** estructura ICP 100, 12 carpetas, 7 NPCs.
- **No acreditado en repositorio actual:** contenido físico, hash, fecha de revisión y salud actual.

No utilizar ICP 100 como evidencia de producción, disponibilidad o validez factual del servicio.

## 4. Por qué no se debe desplegar el código heredado

La implementación `VACGuardian` calcula un score a partir de:
- puntuación base 0,85;
- penalización por frases como «como modelo de lenguaje» o «no tengo acceso a datos»;
- penalización por respuesta muy corta;
- bonificación por solapamiento de palabras con el contexto.

No consulta fuentes, no comprueba si una URL existe, no valida que la cita respalde la afirmación, no detecta una fuente obsoleta ni resuelve contradicciones. Un texto falso, largo y con solapamiento léxico puede superar el umbral.

**Decisión técnica propuesta:** conservar este código como referencia histórica y no reutilizar su score como veredicto de verdad. La nueva implementación debe basarse en evidencia trazable.

## 5. Solución técnica propuesta

### 5.1 Servicio independiente

Construir `Vár / VAC-01` como servicio Python independiente, con API HTTP y almacenamiento persistente de evidencias. El primer candidato de prueba será un proyecto Vercel separado; no se alojará dentro de:
- `waipl-graphy` (proyecto de Graphy);
- `agente-will-app` (proyecto de Will App);
- el runtime del RAG de Will App.

Si Vercel no supera las pruebas de duración, persistencia o ejecución programada, el destino alternativo será un contenedor Docker en un host WAIPL ya disponible (Nodo Central o VPS existente), sin contratar n8n.cloud ni nueva infraestructura por inercia.

Esta selección respeta el plan SCI existente, que prioriza reutilizar infraestructura de coste cero y exige smoke antes de declarar aptitud. El plan `PLAN-SCI-NV-MIG-01 v0.1` sigue siendo DRAFT; no se declara aprobado ni ejecutado.

### 5.2 Contrato funcional

**Entrada propuesta:**
- `request_id`, nodo solicitante y objeto de verificación;
- afirmaciones atómicas a comprobar;
- ámbito y fecha de referencia;
- evidencias aportadas;
- referencias de fuentes, versión, fecha y hash cuando aplique.

**Cadena de verificación:**
1. Descomponer el texto en afirmaciones atómicas.
2. Recuperar fuentes admisibles dentro de la jurisdicción.
3. Comprobar identidad, autoría, fecha, versión y disponibilidad de cada fuente.
4. Extraer el fragmento exacto que respalda o contradice la afirmación.
5. Contrastar fuentes independientes cuando la materia lo requiera.
6. Detectar contradicción, obsolescencia, ausencia de evidencia y límites de acceso.
7. Emitir VAD con trazabilidad por afirmación y abstención explícita cuando no exista base suficiente.

**Salida propuesta:** dictamen VAD con cada afirmación clasificada como HECHO / INFERENCIA / HIPÓTESIS / INCERTIDUMBRE / CONTRADICCIÓN, fuentes, citas exactas, fechas, hashes, límites y justificación.

El LLM (NVIDIA NIM u otro proveedor autorizado) podrá ayudar a extraer y comparar afirmaciones. **El modelo no constituye la evidencia ni puede aprobar una afirmación por su propia confianza.**

### 5.3 Persistencia

- Registro append-only de solicitudes, afirmaciones, fuentes, verificaciones y VAD.
- Versionado del adaptador de fuente y del modelo utilizado.
- Hash de cada evidencia incorporada.
- Registro de errores, abstenciones y contradicciones.
- Ninguna incorporación automática a conocimiento canónico: se mantiene la supervisión humana prevista por la arquitectura.

## 6. Plan de ejecución y responsables

| Fase | Trabajo exacto | Responsable | Evidencia de salida |
|---|---|---|---|
| F0 — Consolidación documental | Integrar la ficha AutoClaw v1.1 en la casa operativa de Lab; contrastar el vault con manifiesto, árbol, `health-check.json` y hashes | Carla; AutoClaw aporta el paquete físico del vault | Ficha accesible en Lab; manifest y health-check contrastados |
| F1 — Contrato API | Definir JSON de entrada/salida VAD, estados por afirmación, reglas de abstención y adaptadores de fuentes | Carla | Especificación versionada y OpenAPI |
| F2 — Implementación | Crear el servicio independiente en `06_SISTEMA_OPERATIVO/VAR/runtime/`; dejar `VACGuardian` heredado intacto | Carla | Código, tests unitarios, Dockerfile y CI |
| F3 — Smoke de alojamiento | Probar Vercel aislado: HTTPS, secreto, persistencia, llamada NIM y duración; si falla, probar host propio con Docker | Carla + administrador de infraestructura | Informe de smoke con resultados y costes |
| F4 — Benchmark factual | Construir conjunto etiquetado de afirmaciones verdaderas, falsas, ambiguas, obsoletas, contradictorias y adversariales | Carla prepara; especialistas de dominio y supervisión humana etiquetan | Dataset versionado, matriz de confusión, precisión, recall, abstención y falsos positivos |
| F5 — Pruebas de aceptación | Adaptar C-01…C-11 y T-01…T-10 al servicio nuevo; ejecutar pruebas funcionales y regresión | Carla; SENTINEL contrasta evidencias | Logs, hashes, resultados y dictamen de verificación |
| F6 — Piloto en sombra | Ejecutar Vár sin admisión automática y comparar VAD con revisión humana | Carla + especialistas; Soberano supervisa | Informe de discrepancias y límites |
| F7 — Publicación | Presentar resultados y solicitar autorización expresa de despliegue | Soberano decide; Carla prepara el expediente | Orden soberana y evidencia del despliegue autorizado |

### 6.1 Responsabilidades y límites

- **Carla:** coordinación, especificación, implementación, pruebas, integración y documentación.
- **Administrador de infraestructura:** crear el proyecto/entorno aislado, provisionar secretos y ejecutar el despliegue técnico autorizado. No necesita que el Soberano actúe como mensajero entre nodos.
- **AutoClaw:** aportar el árbol/manifest/health-check del vault que declara haber construido. No es propietario del runtime SCI ni decide la publicación de Vár.
- **SENTINEL:** contrastar evidencia y estado de Gate; no sustituye a Vár ni implementa su lógica.
- **Yata:** no participa en la cadena de ejecución de Vár. Cuando sea instanciado, auditará validadores de agentes de forma independiente.
- **Soberano:** aprobar el destino de runtime y autorizar la entrada en producción cuando las pruebas estén acreditadas.

## 7. Criterios de aceptación para Vár operativo

Vár no se declarará operativo por existir código, vault, workflow o pruebas de pipeline. La aceptación exige simultáneamente:

1. Identidad Vár/VAC-01 y fronteras de jurisdicción respetadas.
2. Fuente verificable por cada afirmación marcada HECHO.
3. Cita exacta y procedencia reproducible.
4. Detección de contradicciones y fuentes obsoletas.
5. Abstención ante ausencia de evidencia o falta de acceso.
6. Benchmark factual independiente con datos etiquetados y resultados publicados.
7. Pruebas T-01…T-10 adaptadas al runtime elegido.
8. Persistencia y observabilidad verificadas.
9. Supervisión humana para admisión a conocimiento canónico.
10. Autorización soberana expresa para publicación.

## 8. Restricciones

- No reactivar ni pagar n8n.cloud por inercia.
- No confundir NVIDIA NIM (inferencia) con el runtime de orquestación.
- No ubicar Vár dentro del runtime de Graphy ni del RAG de Will App.
- No usar `VACGuardian` como verificador factual de producción.
- No tratar 44/44 como benchmark factual.
- No tratar el ICP 100 del vault como salud actual sin leer el health-check primario.
- No hacer depender Vár de Yata.
- No marcar APPROVED, DEPLOYED o producción sin pruebas y autorización.

## 9. Decisión soberana solicitada

Autorizar la preparación de F1–F3: contrato API, implementación aislada y smoke del candidato Vercel, con Docker en infraestructura ya poseída como alternativa si el smoke no alcanza. El trabajo se desarrolla en la casa operativa de Vár y no altera la arquitectura canónica ni habilita producción.

La publicación queda fuera de esta autorización y requiere una decisión soberana posterior basada en F4–F6.
