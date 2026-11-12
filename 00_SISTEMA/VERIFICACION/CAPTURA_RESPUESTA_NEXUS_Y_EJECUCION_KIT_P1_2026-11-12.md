# Captura de respuesta Nexus y ejecución independiente del kit P1

**ID:** CAPTURA-NEXUS-BUS270-2026-11-12-001  
**Respuesta remitida por William:** 12-11-2026  
**Asignación original:** WAIPL-BUS #270  
**Autor de esta captura:** Carla  
**Atribución:** aportación documental y metodológica de Nexus, recibida en conversación y remitida por el Soberano. No se presenta como comentario escrito por Nexus en GitHub.

## 1. Aportación de Nexus recibida

Nexus respondió a los cinco apartados de #270 con:

1. **Copilot Free:** criterios de búsqueda por nombres, extensiones, ubicaciones, términos y referencias cruzadas. No aportó una ruta/URL o documento original localizado.
2. **Nueve hashes:** procedimiento para localizar los nueve originales, recalcular SHA-256 sobre bytes físicos, comparar hash histórico/físico/normalizado-LF y probar en Windows/Linux. No aportó hashes recalculados ni acceso al nodo Windows.
3. **Kit P1:** propuso cinco pruebas conceptuales (Windows físico, Linux físico, round-trip, repetibilidad y comparación histórica). Indicó que no tenía el kit disponible en su sesión y que sus pruebas propuestas podrían no coincidir con el kit real.
4. **GitBook:** propuso un árbol de diagnóstico para distinguir los contextos de GitBook, comprobar SHA, logs y posible reejecución. No aportó logs ni corrección ejecutada.
5. **DIKE v2.2:** identificó la contradicción documental §8.2/§10 y respaldó la corrección de la referencia, pero se refirió a «§10.1». La fuente literal no contiene un subapartado §10.1: el encabezado es `## 10. Pendientes` y el defecto está en el **punto de lista 1**.

Nexus declaró que en su sesión no dispone de acceso directo a GitHub, al nodo Windows, a Floot ni a SENTINEL. Su respuesta es, por tanto, una aportación metodológica y de contraste, no evidencia de ejecución de búsquedas, recalculado de hashes, pruebas del repositorio ni corrección GitBook.

## 2. Corrección documental entregada a Nexus

Literal de `FICHA-DIKE-v2.2.md`, encabezado `## 10. Pendientes`, punto 1:

> Plan para completar el corpus, empezando por el texto íntegro del Reglamento (UE) 2024/1689 con hash y procedencia, y para dotar a Dike de búsqueda con juicio de vigencia.

§8.2, punto 1 registra 14 documentos, entre ellos cinco entradas AI Act. §8.2 puntos 2 y 4 mantienen abiertas la recuperación jurídica y la vigencia temporal. La propuesta de sustitución del punto 1 de §10 está publicada en SENTINEL:
https://github.com/wmejiasbcn-tech/SENTINEL/blob/main/06_PROPUESTAS/2026-11-12_DIKE-coherencia-v2.2/PROPUESTA_CORRECCION_COHERENCIA_DIKE_v2.2.md

La propuesta no modifica la ficha canónica v2.2 ni crea v2.3.

## 3. Las cinco pruebas reales del kit P1 publicado

Nexus propuso cinco pruebas de alcance distinto. El archivo publicado `tools/p1_dike_crlf_lf/test_apply_p1_patch.py` contiene exactamente estas cinco pruebas:

| # | Prueba real del kit | Resultado de Carla |
|---|---|---|
| 1 | `test_lf_patch_uses_binary_write_and_rechecks_disk_hash` | PASS |
| 2 | `test_crlf_source_style_is_preserved` | PASS |
| 3 | `test_patch_fails_closed_when_source_has_drift` | PASS |
| 4 | `test_patch_is_idempotent` | PASS |
| 5 | `test_apply_creates_backup_and_verifies_source_bytes` | PASS |

**Ejecución independiente de Carla:** recuperó el contenido de los dos archivos de código desde `Will-App-WAIPL-RAG/main`, lo ejecutó con `python -m unittest -v test_apply_p1_patch.py` en Linux y obtuvo **5/5 PASS**.

Entorno de esta ejecución:
- Python: `3.13.5`
- Sistema: `Linux 6.18.57 x86_64`
- SHA-256 de `apply_p1_patch.py` utilizado: `7c5596bf33808bbbcc2cd13f0d2ded47f12112151287329eb21372f2833c4c98`
- SHA-256 de `test_apply_p1_patch.py` utilizado: `8af6e40df68657ce36c1963a86ba7ff99b4300ad1878fbd19c285b06600e3b32`

Esta ejecución verifica las cinco pruebas unitarias del parcheador en Linux. No equivale a una prueba funcional en Windows, no modifica la fuente activa del nodo y no recalcula los nueve hashes originales.

Archivos fuente:
- https://github.com/wmejiasbcn-tech/Will-App-WAIPL-RAG/blob/main/tools/p1_dike_crlf_lf/apply_p1_patch.py
- https://github.com/wmejiasbcn-tech/Will-App-WAIPL-RAG/blob/main/tools/p1_dike_crlf_lf/test_apply_p1_patch.py
- https://github.com/wmejiasbcn-tech/Will-App-WAIPL-RAG/blob/main/tools/p1_dike_crlf_lf/README.md

## 4. Alcance de GitBook ya contrastado por Carla

La evidencia de GitHub diferencia dos contextos:
- `GitBook (./documentation)` sobre el head de la PR #260.
- `GitBook Site` sobre el commit de integración, con el mensaje `Missing site configuration at "gitbook-docs.yaml"`.

No son nombres intercambiables ni se deben fusionar en un estado genérico. El repositorio contiene `gitbook-publico/.gitbook.yaml` y `gitbook-publico/SUMMARY.md`; esa presencia no demuestra por sí sola que la integración `GitBook Site` apunte a ese sitio. La identificación del workflow/sitio y la corrección de configuración requieren inspección del target/logs de la integración.

## 5. SHA y referencias

- WAIPL-BUS #270: https://github.com/wmejiasbcn-tech/Will-AI-Project-Lab/issues/270
- Propuesta DIKE v2.2 en SENTINEL: https://github.com/wmejiasbcn-tech/SENTINEL/blob/main/06_PROPUESTAS/2026-11-12_DIKE-coherencia-v2.2/PROPUESTA_CORRECCION_COHERENCIA_DIKE_v2.2.md
- Kit P1 en `main`: carpeta `tools/p1_dike_crlf_lf/` de Will-App-WAIPL-RAG.

## 6. Registro de atribución

- La metodología de los cinco apartados y la declaración de limitación de acceso proceden de la respuesta de Nexus remitida por William.
- Los cinco resultados PASS, el entorno y los SHA de los ficheros ejecutados proceden de la ejecución independiente de Carla.
- No se atribuyen a Nexus las pruebas ejecutadas por Carla.
- No se atribuyen a Carla la localización del original Copilot Free, los nueve hashes de Windows ni la corrección del contexto GitBook.
