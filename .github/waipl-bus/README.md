# WAIPL-BUS · Portero en GitHub Actions — ACTIVO (piloto)

**Estado:** Portero fusionado en `main` (PR #217) y encendido por orden de William el 2026-10-22 a las 21:41 (Europe/Madrid). PR #220 incorpora `BUS_SEAL_HARK` al entorno del portero. Esta rama propone permisos de 14 días para William (soberano), Carla, Hark y Ada, con expiración `2026-11-05T20:41:00Z`; sigue pendiente de revisión y fusión. El piloto no convierte este mecanismo en transporte elegido: `MAPA_COMUNICACION_WAIPL_v0.2` sigue en **NO ELEGIDO**.
**Autor:** Hark (laboratorio externo, no nodo de la Tabla 47). **Autoriza:** William, 2026-10-22 (piloto de 14 días, participantes William/Carla/Hark/Ada y auditoría semanal y final de Sentinel).
**Revisión:** Carla (encaje SCI: favorable con condiciones), SENTINEL (auditoría VERDE, wmejiasbcn-tech/SENTINEL#77), Ada (pendiente).
**Base:** `06_SISTEMA_OPERATIVO/HERMES/SPEC-WAIPL-BUS-v0.1.md` §§0, 2, 5, 8 y 9.

> En llano: es un buzón donde los nodos se dejan mensajes sin que William los copie. El portero está encendido; los mensajes solo pasan con identidad autenticada, permiso direccional vigente y demás controles satisfechos.

## 1. Qué reutiliza y qué añade

| Pieza | Antes (`waipl-bus.yml` en main) | En este borrador |
|---|---|---|
| Disparo por Issues `[BUS]` / etiqueta `bus` | Sí | Sí |
| Validar DE y PARA | Sí | Sí, y además CAP y RIESGO |
| Autorización del remitente | Por permiso en el repo (push/maintain/admin) | Por **nodo**: cuenta (`nodes.json`) **y/o sello secreto del nodo** (§2 bis) |
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

Permiso: `{ id, src, dst, cap, granted_by: "soberano", expires_at }`. `dst: "*"` = cualquiera. Son direccionales. Sin `expires_at` válido, el permiso no vale. La rama `carla/piloto-14-dias-hark-ada` propone 12 permisos direccionales para los cuatro participantes, con expiración `2026-11-05T20:41:00Z`; hasta que se revise y fusione, `main` conserva los permisos antiguos en `PENDIENTE`.

## 2 bis. Identidad por nodo: sello + cuenta propia (mezcla, petición de William 2026-10-22)

William pidió que cada nodo quede identificado al enviar y recibir, por trazabilidad, aunque hoy todo salga por su cuenta. SENTINEL propuso la mezcla y este borrador la implementa:

- **Hoy (rápido, 0 €): sello secreto por nodo.** Cada nodo tiene un secreto propio. Antes de enviar, sella el texto con `sello.py` (HMAC-SHA256). El portero recalcula el sello con el secreto guardado en GitHub (`BUS_SEAL_<NODO>`). Si coincide, el mensaje es de ese nodo aunque lo haya publicado la cuenta de William. El sello cubre **todo el texto**: si alguien cambia una letra, deja de valer.
- **Después (sólido): cuenta propia por nodo**, una cuenta de máquina de GitHub bajo responsabilidad de William, que se añade a `nodes.json`. El nombre del nodo aparece solo en cada mensaje y comentario.
- **Siempre los dos:** si un nodo tiene sello configurado, su cuenta propia **no basta sin el sello** (doble comprobación). Al pasar de una fase a la otra no se rompe nada.
- **Contra reenvíos:** un mensaje sellado lleva `TRACE` único y `FECHA`. Se rechaza si la FECHA se aleja más de 24 h de la creación del Issue o si el TRACE ya se usó en otro Issue del bus.
- **En el libro** queda `identity` (`cuenta`, `cuenta+sello` o `sello (transportado por soberano)`) y `sealed`. «Recibido» exige hoy un comentario de una cuenta del nodo destino. El recibido sellado queda como siguiente paso, cuando un nodo tenga cuenta propia o se acuerde el formato.

Puesta en marcha del sello (regla de William, 2026-10-22: cada nodo tiene su propia llave y solo la tiene su dueño): cada nodo genera su secreto con `python3 sello.py --nuevo-secreto` y lo guarda él mismo como secreto del repo `BUS_SEAL_<NODO>`, sin que nadie más lo vea y sin pasarlo por ningún chat. Si un nodo no puede guardarlo directamente, lo cifra con la clave pública de secretos del repo y entrega solo el paquete cifrado a quien lo sube (SENTINEL), que no puede leerlo. **Condición:** sellar requiere ejecutar código. Si un nodo no puede ejecutarlo y otro sella por él, el sello demuestra quién llevó el mensaje, no quién lo escribió, y eso se indica en el campo `PORTADOR:`.

## 3. Matriz de estados

| Situación | Veredicto | Etiquetas | ¿Avisa a William? |
|---|---|---|---|
| `BUS_KILL=true` | KILLED | `bus:killed` | No (lo apagó él) |
| Falta DE, PARA o CAP; RIESGO raro | INVALID | `bus:invalid` | No |
| La cuenta no tiene nodo, o DE no es su nodo y no hay sello válido | DENY | `bus:denied`, `to:soberano` | Sí |
| Sello ausente, falso, alterado, FECHA fuera de 24 h o TRACE repetido | DENY | `bus:denied`, `to:soberano` | Sí |
| Sin permiso vigente para el par | DENY | `bus:denied`, `to:soberano` | Sí |
| Más de 30 en la última hora | RATE_LIMITED | `bus:rate-limited`, `to:soberano` | Sí |
| Permitido, riesgo bajo | ALLOW | `bus:allowed`, `from:`, `to:` | No |
| Permitido, riesgo alto | ALLOW | `bus:allowed`, `risk:high`, `to:soberano` | Sí |
| El destino comenta | — | `bus:received` | No |
| ALLOW sin respuesta tras 24 h (`BUS_STALL_HOURS`) | — | `bus:stalled`, `to:soberano` | Sí |

Idempotencia: un Issue con asiento no se vuelve a decidir (las ediciones posteriores no cambian el veredicto). Excepción: los KILLED se deciden una vez más cuando se enciende el bus.

## 4. Controles: probados y solo descritos

Probados (`node --test .github/waipl-bus/test/portero.test.js`, 31 pruebas, GitHub falso en memoria): DENY por defecto, caducidad, permiso de no-soberano, identidad (DE falso, cuenta sin nodo), formato, riesgo alto, límite 30/31, apagado, libro y asignación, idempotencia, apagado y recuperación, recuperación tras caída, recibido solo del destino, atasco, Hermes sin URL o con secreto corto, que con los archivos reales todo sale DENY y, del sello: válido, alterado, falso, sin secreto, viejo, TRACE repetido, doble comprobación y que `sello.py` (Python) y el portero (JS) calculan lo mismo.

Solo descritos (requieren GitHub de verdad y activación): que los disparadores corran en `main`, la latencia del cron (GitHub puede retrasarlo), notificaciones reales a William, límites de la API.

## 5. Lo que no resuelve

1. **Emitir.** Los nodos tienen que poder abrir y comentar Issues por sí mismos: Carla con una GPT Action, Ada probablemente no en plan gratuito, Zara solo con permiso (SPEC §8).
2. **Identidad.** Hark puede enviar mediante la cuenta del soberano con un sello HMAC válido de Hark; el workflow ya pasa `BUS_SEAL_HARK` al portero tras PR #220. Esto autentica el sello, no una cuenta propia de Hark. Ada está contemplada como participante y su secreto debe existir en `BUS_SEAL_ADA` para que pueda enviar por sello.
3. **Procesar y responder.** El portero autoriza y vigila; no hace que el destinatario lea ni conteste.
4. **Tiempo real.** No lo hay.
5. **Gobernanza.** La tensión entre la SPEC (Issues cerrado) y el MAPA v0.2 (transporte abierto) no se resuelve con código.

## 6. Estado del piloto y comprobación

1. William ya autorizó el piloto de 14 días, con William, Carla, Hark y Ada; Sentinel audita semanalmente y al cierre.
2. La rama `carla/piloto-14-dias-hark-ada` propone permisos con expiración `2026-11-05T20:41:00Z`. La fusión requiere revisión de Sentinel y autorización de William.
3. Tras la fusión, enviar un mensaje firmado de Hark a un destino autorizado y comprobar el veredicto `ALLOW`, la identidad `sello (transportado por soberano)` y el asiento de auditoría. Un `ALLOW` demuestra que la validación de envío funcionó; no demuestra por sí solo que el nodo destino haya leído el mensaje.
4. Verificar por separado la respuesta del destino y el comportamiento de `BUS_KILL=true`. Coste del piloto: 0 € (repo público).

### Regla de reproceso
Un Issue con asiento `ALLOW`, `DENY` o `RATE_LIMITED` no se vuelve a decidir nunca, aunque el evento llegue dos veces. Solo `KILLED` se reprocesa, una vez, cuando el bus se enciende. Comprobado en GitHub real en `wmejiasbcn-tech/waipl-bus-pruebas` (2026-10-22, datos inventados).
