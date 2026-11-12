# ACTA DE CORRECCIÓN DE INTEGRIDAD — CRLF/LF EN INGESTA

**ID:** ACTA-INTEGRIDAD-2026-11-12-001  
**Fecha:** 12 de noviembre de 2026  
**Estado:** ACTA Y EVIDENCIA PUBLICADAS EN `main` · KIT P1 PUBLICADO · PRUEBAS UNITARIAS LINUX 5/5 PASS · GATE `AMARILLO/BLOCKED`

## 1. Objeto

Corregir el defecto de integridad de la ingesta por el que el SHA-256 se calcula sobre el texto codificado con saltos LF, mientras que la escritura en modo texto en Windows puede transformar los saltos a CRLF. La finalidad es que el hash registrado corresponda exactamente a los bytes físicos escritos.

## 2. Causa y antecedente documentado

El expediente de SENTINEL del 2026-10-19 documenta nueve discrepancias históricas de SHA-256 explicadas por CRLF/LF, sin pérdida de contenido. La comparación registrada indica que, al normalizar a LF, los nueve contenidos coincidían con sus hashes históricos. Los hashes históricos se conservaron sin modificar en aquel cierre.

En la copia de código examinada, la función `ingest_corpus_document()` calcula el hash con `hashlib.sha256(content_text.encode("utf-8"))` y luego escribe `content_text` mediante `open(..., "w", encoding="utf-8")`. En Windows, el modo texto puede traducir los saltos de línea durante la escritura. El hash previo y los bytes finalmente escritos pueden diferir.

## 3. Corrección técnica autorizada

La corrección propuesta para la fuente activa consiste en codificar una sola vez, calcular el hash sobre esos mismos bytes y escribirlos sin traducción de saltos:

```python
content_bytes = content_text.encode("utf-8")
doc_hash = hashlib.sha256(content_bytes).hexdigest()

with open(corpus_file, "wb") as f:
    f.write(content_bytes)
```

La prueba de regresión comprobará que el SHA-256 calculado sobre `Path(corpus_file).read_bytes()` coincide exactamente con el hash registrado, tanto en Windows como en Linux, incluyendo contenido UTF-8 no ASCII, LF, CRLF, saltos mixtos y salto final.

## 4. Alcance y preservación

- Corregir la función de ingesta de la fuente activa de DIKE.
- Reemitir los nueve hashes afectados a partir de los bytes físicos de los nueve artefactos identificados.
- Registrar evidencia de antes/después y el método reproducible.
- No alterar el contenido semántico de los documentos.
- No sobrescribir ni borrar la procedencia original.
- Preservar la procedencia original de SENTINEL `85c811e1…7963`.
- Mantener los hashes históricos anteriores como evidencia histórica; los nuevos valores se registrarán como reemisión, con vínculo explícito a cada valor anterior.

## 5. Estado de ejecución y bloqueo técnico

La inspección del código y la preparación de la corrección están realizadas. **La modificación de la fuente activa no está ejecutada.** El repositorio accesible contiene la copia de código bajo `_HISTORICO-MASTER`; la evidencia de SENTINEL identifica esa copia como coincidente con el código del nodo central en la ejecución del 2026-10-19. La fuente activa reside en el entorno local del nodo central y no está expuesta en los repositorios accesibles desde esta sesión.

Tampoco están disponibles aquí los nueve archivos físicos y el inventario individual completo de los nueve hashes para reemitirlos con una comparación byte a byte. Por tanto, no se declara aplicada la corrección ni reemitidos los nueve hashes. La copia histórica no se modificará para simular una corrección del original activo.

## 6. Autorización soberana

- Autoridad: William Mejías Navarro — Soberano Human de WAIPL.
- Fecha: 12-11-2026.
- Expresión de autorización: «Adelante», interpretada en el intercambio de opciones A–D como autorización de las dos actuaciones por separado.
- Decisión: P1 de integridad CRLF/LF AUTORIZADA.

## 7. Gate y cierre

## 7. Gate y cierre

- **Gate designado:** Aether.
- **Respuesta recibida:** 12-11-2026, 23:28 Europe/Madrid, remitida por William a Carla en WAIPL-BUS #269.
- **Acta:** `ACTA-INTEGRIDAD-2026-11-12-001`.
- **gate_ref:** `AETHER-GATE-P1-CRLF-LF-2026-11-12-001`.
- **Objeto final emitido:** `state=AMARILLO`, `closed=false`, `open=true`, `result_status=AUSENTE`, `evidence_status=INSUFICIENTE`, `verification_status=PARCIAL`, `dictamen_status=NO_CERRABLE`, `gate_status=BLOCKED`.
- **Requisitos declarados por Aether:** corrección no aplicada a fuente activa; nueve hashes no reemitidos; regresión Windows/Linux no ejecutada; persistencia receipts/SENTINEL no disponible.
- **Autorización:** `AUTHORIZED` no emitido.
- **Receipt HMAC:** no acreditado como emitido ni persistido.

Carla archivó el objeto en SENTINEL/main: [captura de los tres dictámenes](https://github.com/wmejiasbcn-tech/SENTINEL/blob/main/07_ACCIONES_Y_VERIFICACIONES/GATE/cases/2026-11-12_AETHER_GATE_DICTAMENES_CAPTURA.md). Esta captura no es receipt HMAC.

**Contrato aplicable:** `WAIPL_VERIFICATION_GATE_v1.0_FINAL_STATE_CONTRACT.md`. La respuesta de Gate mantiene el expediente P1 abierto y bloqueado.
## 8. Estado

- Autorización soberana: HECHA.
- Diagnóstico del patrón CRLF/LF en el código disponible: HECHO.
- Corrección técnica preparada: HECHA.
- Kit ejecutable `tools/p1_dike_crlf_lf/` publicado en Will-App-WAIPL-RAG mediante PR #6: HECHO.
- Cinco pruebas unitarias del kit ejecutadas por Carla en Linux: **5/5 PASS** (Python 3.13.5; Linux 6.18.57 x86_64). Esta prueba no sustituye una ejecución funcional en Windows.
- Aplicación a la fuente activa del nodo central: NO EJECUTADA.
- Identificación y reemisión byte a byte de los nueve hashes: NO EJECUTADAS.
- Evidencia antes/después en fuente activa: NO DISPONIBLE.
- Publicación de este expediente en `main`: HECHA mediante PR #262, merge commit `bd7ccb1d5546779a38aceaf6e7d3d0ba412fe3d6` (2026-11-12 20:52:03 Europe/Madrid).
- Dictamen de Gate Aether: **RECIBIDO — AMARILLO/BLOCKED**.
- Receipt HMAC y persistencia del objeto primario: **NO DISPONIBLES, según Aether**.
- Cierre formal: **BLOQUEADO**.
