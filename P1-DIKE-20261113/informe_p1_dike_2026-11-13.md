# P1 · Corrección CRLF/LF y verificación de integridad en Windows

**Informe de ejecución y evidencias**

- **Entrega documental:** `P1-DIKE-20261113`
- **Fecha:** 2026-11-13
- **Responsable:** AutoClaw, operador del nodo Windows
- **Supervisión y aceptación:** Carla
- **Estado:** **P1 ABIERTO — PENDIENTE DE ACEPTACIÓN DE CARLA**

---

## 1. Resultado de la ejecución

- **Fuente activa:** `C:\Users\USER\Desktop\AutoClaw\waipl\agents\dike_auditora.py`, fuera de `_HISTORICO-MASTER`. Única copia activa identificada.
- **Pruebas unitarias:** 5/5 PASS en Windows, exit 0.
- **Dry-run:** `DRY_RUN_OK`, sin desviación.
- **Aplicación:** `PATCH_APPLIED_VERIFIED`.
- **Prueba funcional Windows:** PASS con LF y CRLF, incluidos caracteres no ASCII.
- **Integridad de los 9 históricos:** sin cambios; hashes físicos y LF idénticos antes y después; CRLF preservados.
- **Regresión del gate:** 44/44, exit 0.
- **Alcance respetado:** no se tocó Vár, Gate HMAC, secretos, receipts, SENTINEL ni SCI.

## 2. Fuente activa y copia de seguridad

| Campo | Valor |
|---|---|
| Ruta activa | `C:\Users\USER\Desktop\AutoClaw\waipl\agents\dike_auditora.py` |
| Bytes antes / después | 33.647 / 34.119 |
| SHA-256 antes | `2471a5dda3953bdd05e05b378534a9e085dfb853d4cd3addf72453d84808d335` |
| SHA-256 después | `f5f7357aba45b6f8e2f2336816845b27514f03d3a0717c5f09c5cfe1bf6acdd9` |
| SHA-256 LF antes / después | `2471a5dda3953bdd05e05b378534a9e085dfb853d4cd3addf72453d84808d335` / `f5f7357aba45b6f8e2f2336816845b27514f03d3a0717c5f09c5cfe1bf6acdd9` |
| CRLF antes / después | 0 / 0 (LF preservado) |
| Copia de seguridad | `C:\Users\USER\Desktop\AutoClaw\waipl\agents\dike_auditora.py.before-p1-crlf-lf.bak` |
| SHA-256 copia | `2471a5dda3953bdd05e05b378534a9e085dfb853d4cd3addf72453d84808d335` |

## 3. Pruebas unitarias del kit P1

Comando: `python run_p1_tests.py` (unittest, 5 pruebas). Log: `p1_tests_windows.log`.

| # | Prueba | Resultado |
|---|---|---|
| 1 | `test_lf_patch_uses_binary_write_and_rechecks_disk_hash` | PASS |
| 2 | `test_crlf_source_style_is_preserved` | PASS |
| 3 | `test_patch_fails_closed_when_source_has_drift` | PASS |
| 4 | `test_patch_is_idempotent` | PASS |
| 5 | `test_apply_creates_backup_and_verifies_source_bytes` | PASS |

Resultado global: **Ran 5 tests — OK**, exit 0.

El runner solo inserta la ruta del kit en `sys.path` para el Python embebido de AutoClaw; no modifica ni reescribe las cinco pruebas del kit.

## 4. Dry-run y aplicación

| Fase | Resultado | SHA-256 original | SHA-256 parcheado |
|---|---|---|---|
| Dry-run | `DRY_RUN_OK` | `2471a5dda3953bdd05e05b378534a9e085dfb853d4cd3addf72453d84808d335` | `f5f7357aba45b6f8e2f2336816845b27514f03d3a0717c5f09c5cfe1bf6acdd9` |
| Aplicación | `PATCH_APPLIED_VERIFIED` | `2471a5dda3953bdd05e05b378534a9e085dfb853d4cd3addf72453d84808d335` | `f5f7357aba45b6f8e2f2336816845b27514f03d3a0717c5f09c5cfe1bf6acdd9` |

El dry-run comprobó que los tres bloques esperados aparecían exactamente una vez. Si hubiera habido drift, el kit habría fallado cerrado sin escribir. La aplicación creó la copia `.before-p1-crlf-lf.bak` y releyó el archivo para verificar el hash físico.

## 5. Verificación de los nueve documentos históricos

Los nueve archivos no fueron intervenidos. Se releyeron de disco y se compararon con los hashes iniciales.

| Documento | Bytes antes | Bytes después | CRLF antes | CRLF después | Estado |
|---|---:|---:|---:|---:|---|
| `aesia_c5319ca5-b617-4492-b6ce-7423ffdbc183.txt` | 7.563 | 7.563 | 142 | 142 | Sin cambios |
| `aesia_d713e0ab-af4e-4700-8750-441d8acfe91b.txt` | 6.330 | 6.330 | 85 | 85 | Sin cambios |
| `aesia_c66e6ce8-151b-4353-bd55-94d5f063d486.txt` | 4.370 | 4.370 | 81 | 81 | Sin cambios |
| `aesia_3b4cb911-f756-4671-9793-b3c8f9ba72f6.txt` | 9.284 | 9.284 | 135 | 135 | Sin cambios |
| `aesia_4e53e5b5-a2ba-4a78-9744-5290e5e372f7.txt` | 6.728 | 6.728 | 111 | 111 | Sin cambios |
| `rgpd_bb1e6b7a-5397-4bd5-9661-ffa6cb30ec0a.txt` | 408.024 | 408.024 | 4.084 | 4.084 | Sin cambios |
| `lopdgdd_137c461c-c4dd-4695-a176-9236021298a8.txt` | 270.433 | 270.433 | 3.564 | 3.564 | Sin cambios |
| `aesia_7c4555bd-4468-4ae3-bba2-8818440ade1c.txt` | 108.439 | 108.439 | 1.466 | 1.466 | Sin cambios |
| `dossier_6bda7d60-9756-43a1-8866-f16d91168cea.txt` | 15.935 | 15.935 | 447 | 447 | Sin cambios |

### Hashes completos

| Documento | SHA-256 físico antes | SHA-256 físico después | SHA-256 normalizado LF |
|---|---|---|---|
| `aesia_c5319ca5…` | `a1dc4f4a0ee2e261b761db9d00cc58cebc8ca6b8b095acfd36ed4d01175361bd` | `a1dc4f4a0ee2e261b761db9d00cc58cebc8ca6b8b095acfd36ed4d01175361bd` | `f90a8dc06c4c24016b2b20825883b2cb396afa2a4aeb5311d9cee3a3a6dca8ee` |
| `aesia_d713e0ab…` | `75db8b174e52ae3a12fd042e8901c2a17cfc25aa7848c16ce1d6cea637685997` | `75db8b174e52ae3a12fd042e8901c2a17cfc25aa7848c16ce1d6cea637685997` | `3c0db5d849b6904495fcade97e0dc40a7b3378a1b4d980fe797a03fee83eaed4` |
| `aesia_c66e6ce8…` | `f6b56c24e45a8d60948c25c9a071a5f994d3ddf23185dfa3080c898f8225e6de` | `f6b56c24e45a8d60948c25c9a071a5f994d3ddf23185dfa3080c898f8225e6de` | `d4180dfa546e7bcc9fb5341666c6318aa1c26bdefdb1ed56a8c59221f0c0be8c` |
| `aesia_3b4cb911…` | `0e1a1fb2d12a2c6d40cb71026f5b6b691f6f1d71008d44d2997c8f81189b6a7e` | `0e1a1fb2d12a2c6d40cb71026f5b6b691f6f1d71008d44d2997c8f81189b6a7e` | `abb0bdf321d9d8faeec07a45d012370194f978cc3f17a5465ff1accfaa244c32` |
| `aesia_4e53e5b5…` | `712fd3cfba5082f355df022b49d43aca0398d02a0f212f2517794ece451a39e4` | `712fd3cfba5082f355df022b49d43aca0398d02a0f212f2517794ece451a39e4` | `059d63482318cf9be272d8e5a7005c5f1dd700287dba2fad1173e0c4c26c675c` |
| `rgpd_bb1e6b7a…` | `959fdd9d8fecf562fff37658fac5f47cf9a24e765b0e6aebb3fde8732fff5beb` | `959fdd9d8fecf562fff37658fac5f47cf9a24e765b0e6aebb3fde8732fff5beb` | `f8bbc9a915e5fe040035bbff6bfb2ecbbb31c198264b8e618615673ece88fd1b` |
| `lopdgdd_137c461c…` | `aa21f0ae9fbbb80a50bc583e3b6edac8e8e35656589686b38e45e351eeff8d72` | `aa21f0ae9fbbb80a50bc583e3b6edac8e8e35656589686b38e45e351eeff8d72` | `a0ce53a1f43fa8f495a37fd660b3847f2f83af3d07e11a18fa7b64132b36a46f` |
| `aesia_7c4555bd…` | `538b468cf2559811614290afaae847c166994750e0f73dac18fe9bb91cdebc98` | `538b468cf2559811614290afaae847c166994750e0f73dac18fe9bb91cdebc98` | `f17fd8bcbc038a0fb35e58d86d32aae089ca7cc0a8d0c95a64853aec171c239d` |
| `dossier_6bda7d60…` | `af5cd674a9ee7b65cb0f698ed267007b73c0523ff33cae26b773b117e30af92c` | `af5cd674a9ee7b65cb0f698ed267007b73c0523ff33cae26b773b117e30af92c` | `bcbe128c07da3218f41105d0ffdaf9baa91de6b985c7bb2af982f0236b8e485e` |

El hash físico antes y después es idéntico en los nueve; el hash LF coincide con el registrado. No se declaró restablecida ninguna autenticidad histórica: solo se verificó integridad de contenido.

## 6. Prueba funcional en Windows y regresión

| Caso | Bytes entrada / almacenados / índice | SHA-256 almacenado = índice | Bytes iguales |
|---|---|---|---|
| LF + UTF-8 no ASCII | 45 / 45 / 45 | `fd9925afe740473e5ca0ff81d3b7115b61e91a1a6eaf7cc1142152bc96ece8a7` | Sí |
| CRLF + UTF-8 no ASCII | 47 / 47 / 47 | `585922054c541bfedf9affa34e5a57267351e6295b04ecf950f9737cbb301967` | Sí |

Resultado: `FUNCTIONAL_WINDOWS=PASS`, exit 0. La escritura binaria conserva exactamente los bytes de entrada; no hay traducción de LF a CRLF ni a la inversa. Regresión del gate: 44/44, exit 0.

**Evidencia Linux:** no consta un log Linux separado en el kit ni en el PR #6. El cuerpo del PR solo declara «5 pruebas locales» sin especificar sistema operativo y no hay checks de CI. No se inventa una ejecución Linux; se registra la ausencia como límite de evidencia.

## 7. Relación de cambios

El diff completo está en `p1_source_diff.txt`. Solo se modificaron tres bloques de `ingest_corpus_document`:

1. **Hash:** `content_text.encode("utf-8")` se guarda en `content_bytes` y se hashea ese buffer.
2. **Escritura:** `open(corpus_file, "wb")`, `write(content_bytes)`, `flush`, `fsync`, relectura `rb` y comparación `stored_hash == doc_hash`; si falla, elimina el archivo fallido y aborta antes de registrar el índice.
3. **Índice:** `size_bytes = len(content_bytes)`, no una segunda codificación.

No se alteró ninguna otra lógica.

## 8. Evidencias y entrega documental

| Evidencia | Ruta |
|---|---|
| Informe DOCX | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\Informe_P1_DIKE_2026-11-13.docx` |
| Informe Markdown | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\informe_p1_dike_2026-11-13.md` |
| Manifiesto JSON | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\p1_evidence_manifest.json` |
| CSV de los 9 archivos | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\p1_nine_files_hashes.csv` |
| Logs | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\logs` |
| Originales copiados | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\originals` |
| Fuente y backup copiados | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\after_patch` |
| Kit P1 | `C:\Users\USER\Desktop\AutoClaw\DELIVERY\P1-DIKE-20261113\kit` |

Entrega documental: `P1-DIKE-20261113`. Kit de origen: PR #6 de `Will-App-WAIPL-RAG`, merge commit `966a8ca`. No se ha creado una PR nueva ni se ha publicado nada en `main`; el cambio queda en el working tree para revisión de Carla.

## 9. Criterio de cierre

- **Cumplido:** 5/5 pruebas unitarias en Windows.
- **Cumplido:** dry-run sin drift y parche aplicado sobre la fuente activa correcta.
- **Cumplido:** integridad física de los 9 archivos comprobada; no fueron reescritos.
- **Cumplido:** prueba funcional Windows con LF y CRLF; regresión del gate 44/44.
- **Pendiente:** evidencias completas entregadas a Carla; P1 no se declara cerrado y no se hace merge.

*«Sin vosotras no hay nosotros.»*
