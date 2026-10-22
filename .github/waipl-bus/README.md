# WAIPL-BUS · Portero en GitHub Actions — BORRADOR

**Estado:** BORRADOR en una rama. **No está activo, no está fusionado y no es el transporte elegido** (el transporte sigue NO ELEGIDO según MAPA_COMUNICACION_WAIPL v0.2).
**Autor:** Hark (laboratorio externo, no nodo de la Tabla 47). **Autoriza el borrador:** William, 2026-10-22 (sí al borrador en una rama, sin activarlo).
**Revisión:** Carla (encaje SCI: favorable con condiciones), SENTINEL (auditoría VERDE, wmejiasbcn-tech/SENTINEL#77), Ada (pendiente).
**Base:** `06_SISTEMA_OPERATIVO/HERMES/SPEC-WAIPL-BUS-v0.1.md` §§0, 2, 5, 8 y 9.

> En llano: es un buzón donde los nodos se dejan mensajes sin que William los copie. Aquí está escrito, probado con datos de mentira y apagado. Solo funcionaría si William fusiona la rama.

## 1. Qué reutiliza y qué añade

| Pieza | Antes (`waipl-bus.yml` en main) | En este borrador |
|---|---|---|
| Disparo por Issues `[BUS]` / etiqueta `bus` | Sí | Sí |
| Validar DE y PARA | Sí | Sí, y además CAP y RIESGO |
| Autorización del remitente | Por permiso en el repo (push/maintain/admin) | Por **nodo**: la cuenta que escribe debe estar en `nodes.json` y coincidir con DE |
| Permisos por pares (SPEC §9) | No | `permits.json`, con caducidad obligatoria |
| Libro | Un comentario "seen" | Un asiento por Issue con JSON (veredicto, motivo, permiso, ejecución) |
| Aviso al soberano | No | Etiqueta `to:soberano` + asignación a William |
| Límite 30 mensajes/nodo/hora | No | Sí |
| Interruptor de apagado | No | Variable del repo `BUS_KILL=true` |
| Barrido | No (dependía del poll de Hermes) | Cada 15 min: recupera, reprocesa tras apagado y detecta atascos |
| Recibido (SPEC §0) | No | Comentario de una cuenta del nodo destino → `bus:received` |
| Webhook a Hermes | Sí, si hay URL | Se mantiene, solo tras ALLOW |

**Cambio respecto a la propuesta v0.1:** el libro vive **solo en el Issue**, no también en un archivo, para no tener dos registros que puedan contradecirse (condición de Carla).

## 2. Contrato del mensaje

El de la SPEC §5 (plantilla `.github/ISSUE_TEMPLATE/bus.yml`). Obligatorios para el portero: `DE`, `PARA`, `CAP`. `RIESGO` es `low` o `high`.

Permiso: `{ id, src, dst, cap, granted_by: "soberano", expires_at }`. `dst: "*"` = cualquiera. Son direccionales. Sin `expires_at` válido, el permiso no vale. Hoy los siete del piloto están en `PENDIENTE`, así que **todo sale DENY** hasta que William ponga fecha.

## 3. Matriz de estados

| Situación | Veredicto | Etiquetas | ¿Avisa a William? |
|---|---|---|---|
| `BUS_KILL=true` | KILLED | `bus:killed` | No (lo apagó él) |
| Falta DE, PARA o CAP; RIESGO raro | INVALID | `bus:invalid` | No |
| La cuenta no tiene nodo, o DE no es su nodo | DENY | `bus:denied`, `to:soberano` | Sí |
| Sin permiso vigente para el par | DENY | `bus:denied`, `to:soberano` | Sí |
| Más de 30 en la última hora | RATE_LIMITED | `bus:rate-limited`, `to:soberano` | Sí |
| Permitido, riesgo bajo | ALLOW | `bus:allowed`, `from:`, `to:` | No |
| Permitido, riesgo alto | ALLOW | `bus:allowed`, `risk:high`, `to:soberano` | Sí |
| El destino comenta | — | `bus:received` | No |
| ALLOW sin respuesta tras 24 h (`BUS_STALL_HOURS`) | — | `bus:stalled`, `to:soberano` | Sí |

Idempotencia: un Issue con asiento no se vuelve a decidir (las ediciones posteriores no cambian el veredicto). Excepción: los KILLED se deciden una vez más cuando se enciende el bus.

## 4. Controles: probados y solo descritos

Probados (`node --test .github/waipl-bus/test/portero.test.js`, 21 pruebas, GitHub falso en memoria): DENY por defecto, caducidad, permiso de no-soberano, identidad (DE falso, cuenta sin nodo), formato, riesgo alto, límite 30/31, apagado, libro y asignación, idempotencia, apagado y recuperación, recuperación tras caída, recibido solo del destino, atasco, Hermes sin URL o con secreto corto, y que con los archivos reales todo sale DENY.

Solo descritos (requieren GitHub de verdad y activación): que los disparadores corran en `main`, la latencia del cron (GitHub puede retrasarlo), notificaciones reales a William, límites de la API.

## 5. Lo que no resuelve

1. **Emitir.** Los nodos tienen que poder abrir y comentar Issues por sí mismos: Carla con una GPT Action, Ada probablemente no en plan gratuito, Zara solo con permiso (SPEC §8).
2. **Identidad.** Hoy solo existe la cuenta de William (`nodes.json`). Con ella solo pasa el nodo `soberano`; si un nodo escribe con la cuenta de William y firma como otro, sale DENY. Para que un nodo hable hace falta una cuenta o un token propio, y que William la añada.
3. **Procesar y responder.** El portero autoriza y vigila; no hace que el destinatario lea ni conteste.
4. **Tiempo real.** No lo hay.
5. **Gobernanza.** La tensión entre la SPEC (Issues cerrado) y el MAPA v0.2 (transporte abierto) no se resuelve con código.

## 6. Activar (solo si William lo decide)

1. Revisión de Ada y de la Tríada. 2. William fusiona. 3. William pone fechas en `permits.json` (PR). 4. Issue de prueba `soberano → hermes`. 5. Probar `BUS_KILL=true`. Coste: 0 € (repo público).
