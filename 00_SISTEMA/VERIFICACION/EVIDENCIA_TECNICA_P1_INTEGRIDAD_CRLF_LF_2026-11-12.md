# EVIDENCIA TÉCNICA — P1 INTEGRIDAD CRLF/LF DE DIKE

**Expediente:** ACTA-INTEGRIDAD-2026-11-12-001  
**Fecha:** 2026-11-12  
**Responsable del diagnóstico y preparación documental:** Carla  
**Estado:** DEFECTO LOCALIZADO · CORRECCIÓN PREPARADA · FUENTE ACTIVA NO MODIFICADA

## 1. Código inspeccionado

Repositorio: `wmejiasbcn-tech/Will-App-WAIPL-RAG`  
Ruta: `_HISTORICO-MASTER/waipl/agents/dike_auditora.py`  
Blob Git: `ce99618a8d3f46078c7303d519325f2cb38ab9d9`  
SHA-256 de la copia: `2471a5dda3953bdd05e05b378534a9e085dfb853d4cd3addf72453d84808d335`

En `ingest_corpus_document()` se observan estas operaciones:

1. Cálculo previo:
   `doc_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()`
2. Escritura posterior en modo texto:
   `with open(corpus_file, "w", encoding="utf-8") as f: f.write(content_text)`

En Windows, la escritura de texto con traducción de nueva línea puede convertir LF en CRLF. En ese caso, el hash del texto codificado antes de la escritura no representa los bytes físicos que quedan en disco.

## 2. Contraste con evidencia histórica

- `SENTINEL/04_EVIDENCIAS/DIKE/2026-10-19_DIKE_T10_EJECUCION.md` identifica la copia examinada como coincidente con el código utilizado por Carla y registra su SHA-256 y blob.
- `SENTINEL/09_REGISTRO_OPERATIVO/2026-10-19_REGISTRO.md` recoge que nueve discrepancias históricas se explicaron por CRLF/LF, sin alteración del contenido, y que el informe/manifiesto final de AutoClaw registró 14 documentos y nueve hashes coincidentes tras la comprobación.
- El mismo registro deja constancia de que los hashes históricos se conservaron sin modificar.

## 3. Corrección preparada (NO APLICADA)

Cambio de implementación propuesto para la fuente activa:

```python
content_bytes = content_text.encode("utf-8")
doc_hash = hashlib.sha256(content_bytes).hexdigest()

with open(corpus_file, "wb") as f:
    f.write(content_bytes)
```

Criterio de regresión:

```python
stored_bytes = Path(corpus_file).read_bytes()
assert hashlib.sha256(stored_bytes).hexdigest() == entry["sha256"]
assert stored_bytes == content_bytes
```

La batería de regresión deberá ejecutarse en Windows y Linux con casos LF, CRLF, mixtos, caracteres UTF-8 no ASCII y salto final.

## 4. Límite de acceso y no ejecución

El código accesible en GitHub está bajo `_HISTORICO-MASTER`. El documento de evidencia de SENTINEL lo identifica como copia del código del nodo central en la prueba del 2026-10-19; no es el archivo activo del equipo Windows.

La fuente activa se encuentra en el entorno local del nodo central, que no está conectado a las herramientas disponibles en esta sesión. No he modificado la copia histórica ni he afirmado que el nodo central haya sido corregido.

El inventario individual y los bytes originales de los nueve artefactos afectados tampoco están disponibles en el repositorio accesible para recalcular y reemitir cada hash con evidencia antes/después. Por ello:

- corrección en fuente activa: **PENDIENTE**;
- reemisión de nueve hashes: **PENDIENTE**;
- pruebas reales Windows/Linux: **PENDIENTE**.

## 5. Resultado

El defecto de implementación está localizado en la secuencia hash-texto / escritura en modo texto de `ingest_corpus_document()` en la copia identificada. La corrección está preparada, pero no aplicada a la fuente activa. El P1 permanece abierto y no se solicita cierre hasta disponer de la ejecución real, la reemisión verificable de los nueve hashes y el dictamen de Aether.
