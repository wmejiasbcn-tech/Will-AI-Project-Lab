# EVIDENCIA TÉCNICA — ACTUALIZACIÓN DE LA FICHA DIKE v2.2

**Expediente:** ACTA-DIKE-2026-11-12-001  
**Fecha:** 2026-11-12  
**Responsable de ejecución documental:** Carla  
**Estado:** ACTUALIZACIÓN DOCUMENTAL PUBLICADA EN `main` · GATE PENDIENTE

## 1. Fuentes contrastadas

1. Ficha canónica v2.1 en SENTINEL: `docs/governance/fichas/FICHA-DIKE-v2.1.md`, blob Git `c559dc0ae56cd8096950b0148c4562d073020f7b`.
2. Addendum funcional DIKE/KAIROS/Will App del 2026-10-31: `docs/governance/ADDENDUM-DIKE-KAIROS-WILL-APP-2026-10-31.md`, blob Git `47ce94fe388cbc6dea91e3ff3101e81494b27577`.
3. Registro operativo SENTINEL del 2026-10-19: `09_REGISTRO_OPERATIVO/2026-10-19_REGISTRO.md`. En su apartado de DIKE recoge que el índice final quedó en 14 documentos y que los nueve hashes históricos discrepantes se explicaron por CRLF/LF, sin alteración de contenido.
4. Informe de AutoClaw aportado por William en esta conversación, que detalla la composición del corpus: 9 documentos históricos + 5 entradas AI Act y sitúa la última verificación registrada en 2026-10-19.

## 2. Artefacto creado

- Ruta: `docs/governance/fichas/FICHA-DIKE-v2.2.md`.
- Blob Git actual en la rama de trabajo: `ec0e993d84b4d71cf65378675fac81eea49e816c`.
- SHA-256 del contenido UTF-8: `776797862cc8b4ffd5c7b766fbfce901088deac4769e1257bdeb1ed9ba4747d9`.
- Commit de creación: `bf534e8791d1b1adeb68b19b5c0daa1a3aa4ceb8`.
- Commit de precisión del estado documental/Gate: `cd01e6818dc76d9117bb385fe5e8d06dbb8a34a8`.

## 3. Registro de versión

Se actualizó `docs/governance/version.json` en la misma rama:
- versión del registro: `1.1.2`;
- fecha: `2026-11-12`;
- checksum de v2.2 incorporado: `776797862cc8b4ffd5c7b766fbfce901088deac4769e1257bdeb1ed9ba4747d9`;
- checksum preexistente de v2.1 conservado.

Commit de actualización de `version.json`: `beb6ba62cdf110143c92a6e3755130a493839dde`.

## 4. Límites de esta evidencia

La ficha v2.2 y el registro de versión se prepararon en la rama `dike-ficha-v2.2-2026-11-12` y se publicaron en `main` mediante SENTINEL PR #192, squash merge commit `c67c65e13c54320b12bb18f6a3acf5c8ce4bc513` (2026-11-12 20:51:55 Europe/Madrid). La acta y esta evidencia se publicaron en el Lab mediante PR #261, squash merge commit `71f7b43903579d448a754ed7702c3535d63f1d9e` (2026-11-12 20:51:59 Europe/Madrid). El dictamen de Gate Aether continúa pendiente y no se declara cierre formal.

No se ha cambiado el código de DIKE, no se ha declarado `APPROVED` y no se ha declarado despliegue.
