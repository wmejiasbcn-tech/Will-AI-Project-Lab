# EXPEDIENTE TÉCNICO DE TRANSFERENCIA — GRAPHY / WAIPL

Documento de handoff. Estado del proyecto en el momento de emisión, sin desarrollo asociado.
Ningún archivo del producto se ha modificado durante la redacción de este expediente.

**Convención de veracidad usada en todo el documento:**

| Marca | Significado |
| --- | --- |
| `VERIFIED` | Comprobado en runtime o leído literalmente en el código de este proyecto |
| `INFERRED` | Deducido de material presente en el proyecto, no afirmado explícitamente en él |
| `UNKNOWN` | No consta en los archivos ni es recuperable del material disponible |
| `CONTRADICTORY` | Existen dos fuentes en el proyecto que no coinciden |

---

## 1. IDENTIDAD Y PROPÓSITO

| Campo | Valor | Marca |
| --- | --- | --- |
| Nombre del artefacto | Graphy | VERIFIED |
| Archivo | `Graphy 0.1.dc.html` | VERIFIED |
| Versión funcional alcanzada | 1.0 (cerrada y validada) | VERIFIED |
| Versión rotulada en el nombre de archivo | `0.1` — el nombre no se renombró al cerrar 1.0 | VERIFIED |
| Rótulo en cabecera de la app | «GRAPHY · Estructura relacional · WAIPL» | VERIFIED |
| Rótulo en la portada | «0.1 · Fase experimental» | VERIFIED |

**Discrepancia de rotulado (no bloqueante):** el archivo y la portada siguen diciendo `0.1`
mientras lo cerrado es 1.0. Es cosmético; se documenta para que el siguiente agente no lo
confunda con una versión anterior.

### Propósito

Graphy es la capa visual, navegable y relacional del ecosistema WAIPL. Permite recorrer la
estructura de relaciones declaradas del ecosistema sin ejecutar el laboratorio.

### Principio conceptual (literal, del propio producto)

> «Graphy es la representación viva y navegable del ecosistema WAIPL.»
>
> «El Laboratorio muestra el comportamiento. Graphy muestra la estructura relacional.»

### Relación con WAIPL y con el MVP

- Graphy **lee** el master de la Carta (identidad de las presencias) y su propia capa de datos
  (topología). `VERIFIED`
- Graphy **no** carga, ejecuta ni consulta el MVP. Comprobado en runtime: `window.__waipl`
  es `undefined` y no existe ningún `<script src>` que apunte a `Waipl*`. `VERIFIED`

### Qué NO es Graphy

- No es otro motor WAIPL.
- No controla el laboratorio.
- No modifica las Presence.
- No genera relaciones ficticias.
- No sustituye al MVP.
- No es una física definitiva, ni una ontología canónica, ni un modelo validado, ni una
  arquitectura cerrada (así se declara literalmente en el propio pie de la interfaz). `VERIFIED`

---

## 2. GENEALOGÍA / PROCEDENCIA

### Ubicación del master

`/projects/9c500662-45cf-4681-9a44-ef71bcfd7609/ui_kits/carta-presentacion/` — sistema de diseño
**Will-AI Project Lab Design System**, vinculado a este proyecto. `VERIFIED`

### Piezas del master

| Archivo | Contenido | Marca |
| --- | --- | --- |
| `index.html` | Carta v3: recorrido escénico de escenas 0–21, blasón, umbral, atmósfera | VERIFIED |
| `archive-v2.0.html` | Versión anterior conservada | VERIFIED |
| `archive-v1.6.html` | Versión con título literal «Carta de Presentación del Ecosistema v1.5»; tablas núcleo/colaboradores y mapa orbital | VERIFIED |
| `presences.js` | Las doce presencias, orden y roles. Contiene la nota literal: «orden fijado por Carla: sin jerarquía núcleo/colaborador» | VERIFIED |
| `character-bible.md` | «Biblia Oficial de Dirección de Personajes» | VERIFIED (existe) |
| `node-visual-briefs.md` | Briefs visuales por nodo | VERIFIED (existe) |
| `main-v3.js`, `lab-atmosphere.js`, `lab-memory.js`, `closing-scenes.js`, `scenes.js` | Motor de escenas del master | VERIFIED (existen) |

### Genealogía de la Carta

La cadena de autoría, según la corrigió el usuario y como está escrita hoy en
`WAIPL Carta Oficial - candidata.dc.html`:

| Orden | Quién | Papel |
| --- | --- | --- |
| — | **William** | Encarga la Carta y dirige todo el proceso. El criterio ha sido suyo en cada paso |
| 1 | **Áurea · Meta AI** | **Autoría original.** Inicia la Carta a petición de William |
| 2 | **Kimi** | Segunda mano |
| 3 | **Atlas** | Tercera mano |
| 4 | **Ada** | Cuarta mano |
| 5 | **Claude Design** | Última mano hasta hoy: producción y maquetación, **sin autoría del origen** |
| — | **Carla** | Coordinación junto a William |

`VERIFIED` como contenido del archivo. La cadena procede de la corrección expresa del usuario;
los archivos del proyecto no la registran por sí solos. Fechas por versión: `UNKNOWN`.
Autoría línea a línea: `UNKNOWN`.

**Incidencia histórica registrada:** una versión anterior de esta genealogía atribuía el origen
de la Carta a Ada y el desarrollo a Claude Design. El usuario la corrigió señalando que se estaba
apropiando indebidamente de la autoría de Áurea. La corrección está aplicada. `VERIFIED`

**Contradicción documentada en el sistema de diseño:** la guía del design system corrige una
descripción anterior de Ada limitada a «maquetación» por «ética, calidad y dirección narrativa»,
y «Aether» por «Aether-Hermes». `CONTRADICTORY` (resuelto a favor de la versión corregida).

---

## 3. ARTEFACTOS — INVENTARIO COMPLETO

Raíz del proyecto:

```
/
├── Graphy 0.1.dc.html              ← el producto Graphy
├── graphy-data.js                  ← capa de datos de Graphy
├── WAIPL Carta Oficial - candidata.dc.html
├── WAIPL Paquete Oficial.dc.html
├── WAIPL MVP.dc.html               ← demo del laboratorio
├── WAIPL MVP - standalone.html
├── WaiplLabEngine.js               ← motor 001-030
├── WaiplPresences.js               ← 11 configuraciones
├── WAIPL Character Bible.dc.html
├── Informe WAIPL - Carla.dc.html
├── VOICE_ENGINE_CONFIG.js
├── VOICE_PERFORMANCE_SPEC.md
├── CLAUDE.md                       ← notas de proyecto
├── github.md
├── support.js                      ← runtime del entorno (no editar)
├── doc-page.js
├── _ds/                            ← design systems vinculados
├── assets/
└── screenshots/
```

| Archivo | Función | Estado | ¿Modificado en la fase Graphy? |
| --- | --- | --- | --- |
| `Graphy 0.1.dc.html` | Producto Graphy: plantilla + lógica | **VALIDADO 1.0** | Sí — es el único archivo que se ha tocado |
| `graphy-data.js` | Topología, tipos, procedencias, estados, reloj simulado | **CONGELADO** | Sí, hasta 0.3; desde 0.4 no se ha vuelto a tocar |
| `WAIPL MVP.dc.html` | Demo del laboratorio | **CONGELADO** | No |
| `WaiplLabEngine.js` | Motor sprints 001–030 | **CONGELADO** | No |
| `WaiplPresences.js` | 11 configuraciones de presencia | **CONGELADO** | No |
| `WAIPL Paquete Oficial.dc.html` | Paquete de presentación | **CONGELADO** | No |
| `WAIPL Carta Oficial - candidata.dc.html` | Carta candidata | **VALIDADO** | Sí, solo la genealogía (fuera de la fase Graphy) |
| Master de la Carta (design system) | Fuente de identidad | **NO MODIFICADO** | No — solo lectura |
| `character-bible.md` | Dirección de personajes | **NO MODIFICADO** | No |
| `node-visual-briefs.md` | Briefs visuales | **NO MODIFICADO** | No |
| `support.js` | Runtime del entorno | **NO EDITABLE** | No |

### Lo que no debe tocarse

`WaiplLabEngine.js`, `WaiplPresences.js`, `WAIPL MVP.dc.html`,
`WAIPL Paquete Oficial.dc.html`, el master de la Carta, `support.js`.

---

## 4. ARQUITECTURA REAL DE GRAPHY

```
                       MASTER DE LA CARTA (design system, solo lectura)
                       window.WillAIProjectLabDesignSystem_9c5006.NODES
                                        │  name · role · quote · accent
                                        ▼
   graphy-data.js  ─── LEVELS · STRUCTURAL · MASTER_ID · EDGES · RELATION_TYPES
                       PROVENANCE · REL_STATES · ABSENT
                       nodes() · relationships() · relationshipsOf() · neighborsOf()
                       nodeById() · tickSimulated() · nowSimulated() · resetSimulated()
                                        │
                                        ▼
   Graphy 0.1.dc.html  ── LÓGICA (class Component extends DCLogic)
       estado:  entered · focus · relFocus · hist[] · cmpMode · cmpB
                relTimeline[] · relTimelineFor · relCursor · mapExpand · data
       resolvers:
            layout()                    geometría del grafo principal
            summaryContext/Resolver     síntesis 0.4
            comparisonContext/Resolver  comparación 0.6
            temporalContext/Resolver    evolución 0.7
            networkContext/Resolver     red 0.8
            relationalMapContext/Resolver mapa 0.9
       navegación: focusOn · focusRelation · goBack · clearSelection
                   pushHistory · resetNetwork · resetMap
                                        │
                                        ▼
                             renderVals()  → valores planos
                                        │
                                        ▼
   PLANTILLA (x-dc)  ── SVG inline + sc-for + data-dc-tpl
       · grafo principal (svg viewBox 0 0 100 100)
       · etiquetas y monogramas como <div> absolutos sobre el SVG
       · paneles: síntesis · mapa · red · relaciones · comparación · evolución
```

### Qué hace cada capa

| Capa | Responsabilidad |
| --- | --- |
| Master | Identidad: nombre, rol, voz (frase), acento. Solo lectura, releído en cada consulta |
| `graphy-data.js` | Topología, tipos de relación, procedencias, estados, reloj simulado |
| Lógica | Resolución, geometría precomputada, navegación, estado de interacción |
| `renderVals()` | Traduce estado + datos a valores planos que la plantilla consume |
| Plantilla | Pinta. Todo el SVG vive aquí, para que cada nodo y arista sea editable |

**Regla de separación:** la vista no conoce la topología, solo la recorre.
`graphy-data.js` puede sustituirse sin tocar la vista.

---

## 5. GRAPHY 0.1 — GRAFO EN PLANTILLA

Implementación inicial: grafo radial en SVG con nodo central y anillo de vecinos.

- `viewBox="0 0 100 100"`, `preserveAspectRatio="xMidYMid meet"`, contenedor con
  `padding-bottom:64%`. `VERIFIED`
- Aristas: `<line>` dentro de `<sc-for list="{{ graphEdges }}">`.
- Nodos: `<g>` con tres `<circle>` (halo, anillo, núcleo) dentro de
  `<sc-for list="{{ graphNodes }}">`.
- Etiquetas y monogramas: `<div>` absolutos **fuera** del SVG, posicionados sobre él.

### Incidencia del SVG (causa raíz documentada)

El runtime de Design Components envuelve cada interpolación `{{ }}` en un `<span>`. Dentro de
`<text>`/`<tspan>` de SVG, un `<span>` no genera caja de texto: el rótulo no se pinta y
`getBBox()` no devuelve medida útil.

**Solución adoptada:** rotular con `<div>` posicionados en coordenadas de porcentaje sobre el
lienzo, en lugar de `<text>` SVG. `VERIFIED`

### Transformación de coordenadas (crítica si se cambia la altura del lienzo)

Con `meet` y un contenedor de aspecto 100:64, la escala la fija el alto:

```
escala = 0.64
left   = 18% + x * 0.64
top    = y  (+ desplazamiento del rótulo)
```

Está codificado literalmente en `mark()`. **Si se cambia el `padding-bottom` del contenedor,
hay que recalcular `18` y `0.64`, o las etiquetas se desalinean del nodo.** `VERIFIED`

### Sustitución de `React.createElement`

El grafo se construía originalmente con `React.createElement`, lo que lo hacía opaco al editor
del sistema de diseño. Se trasladó íntegro a plantilla con `sc-for`. Hoy no queda ninguna
llamada a `React.createElement` en el archivo. `VERIFIED` (comprobado por búsqueda).

---

## 6. GRAPHY 0.2 — RELACIONES

Modelo normalizado emitido por `relationships()`:

```js
{ id, source, target, type, provenance, status, basis,
  weight, state, visibility, updatedAtSimulated }
```

### Tipos de relación (`RELATION_TYPES`)

| type | label | stroke | width (= peso) |
| --- | --- | --- | --- |
| `criterio` | Criterio | solid | 0.30 |
| `pertenencia` | Pertenencia | solid | 0.22 |
| `habita` | Habita | solid | 0.20 |
| `representa` | Representa | **dashed** | 0.20 |

### Procedencias (`PROVENANCE`)

| clave | label | status | color |
| --- | --- | --- | --- |
| `master` | Master de la Carta | declarada | `#C9A86A` |
| `mvp` | Observada en el laboratorio | observada | `#C9A86A` |
| `experimental` | Propuesta de esta fase | experimental | `#9C81BD` |
| `derived` | Deducida | deducida | `#6E6E78` |

`derived` está declarada y diferenciada pero **hoy no se emite ninguna relación deducida**,
porque deducir por co-presencia está prohibido. La categoría se conserva para no perder la
distinción. `VERIFIED`

`mvp` está declarada y **no se usa** en ninguna arista actual. `VERIFIED`

### Regla de no invención

Comentario literal en `graphy-data.js`:

> «Solo se emiten relaciones declaradas. No se deduce ninguna arista entre presencias por el
> hecho de compartir laboratorio: la travesía entre presencias pasa por la arista declarada al
> laboratorio, que ya existe.»

### Ausencias deliberadas (`ABSENT`, se muestran en la interfaz)

| Qué falta | Por qué |
| --- | --- |
| Relaciones entre Presence concretas | El master no las fija y el laboratorio las produce en cada corrida. Se observan allí, no aquí |
| Jerarquía entre presencias | El orden del master es de presentación, no de rango. No hay núcleo ni colaboradores |

---

## 7. GRAPHY 0.3 — ESTADO RELACIONAL

Campos añadidos al modelo: `state`, `weight`, `visibility`, `updatedAtSimulated`.

### Estados (`REL_STATES`)

| Estado | label | opacity | visibility |
| --- | --- | --- | --- |
| `INACTIVE` | Inactiva | 0.50 | visible |
| `ACTIVE` | Activa | 0.90 | visible |
| `FOCUSED` | En foco | 1.00 | visible |
| `DIMMED` | Atenuada | 0.22 | attenuated |

### Estado del dato vs estado visual — distinción central

- **Estado del dato:** `relationships()` emite siempre `state: 'INACTIVE'`. Es el valor del
  modelo. `VERIFIED`
- **Estado visual:** lo fija la interacción (`relStateFor()`): `FOCUSED` para la relación
  seleccionada, `DIMMED` para las demás, `ACTIVE` cuando no hay selección.

Por eso la tarjeta de red y la de comparación pueden mostrar «Inactiva» mientras la síntesis
dice «2 activas»: son dos lecturas distintas de la misma relación. **No es un fallo.** Quedó
aceptado por el usuario como criterio de coherencia. `VERIFIED`

### Reloj simulado

```js
let SIM_TICK = 0;
tickSimulated()  → ++SIM_TICK
nowSimulated()   → SIM_TICK
resetSimulated() → SIM_TICK = 0
```

Avanza **solo** cuando Graphy registra una interacción (`focusOn`, `focusRelation`,
`clearSelection`, `captureSnapshot`, `resetNetwork`, `resetMap`). Sin reloj real, sin scheduler,
sin bucles. La misma secuencia de interacciones produce los mismos sellos. `VERIFIED`

### Corrección de las 55 relaciones por pares

En una fase intermedia se generaron relaciones entre presencias por co-presencia en el
laboratorio (combinaciones de las once). **Se retiraron**: eran relaciones inventadas, no
declaradas por el master ni observadas. Hoy no existe ninguna arista presencia↔presencia.
`VERIFIED` (0 aristas de ese tipo en la topología actual).

---

## 8. GRAPHY 0.4 — SÍNTESIS RELACIONAL

`summaryContext(data, focus, ring, stateOf)` → agrupa referencias, no deriva nada.
`summaryResolver(ctx)` → cuenta y ordena lo existente.

| Campo | Cálculo |
| --- | --- |
| `total` | Número de relaciones del nodo en foco |
| `active` / `focused` / `dimmed` | Recuento por estado visual |
| `declared` | Relaciones con `provenance = master` |
| `experimental` | `provenance = experimental` |
| `derived` | `provenance = derived` |
| `relatedNodes` | Nombres de los nodos conectados |
| `strongest` | Mayor `width` del tipo; desempate alfabético por nombre |
| `dominantType` | Tipo más frecuente; desempate alfabético por clave |
| `dominantProvenance` | Procedencia más frecuente; desempate alfabético |

**Reglas de presentación:** las categorías con recuento cero no generan etiqueta (no se dibuja
«0 derivadas»); el recuento se calcula igualmente. Las relaciones atenuadas siguen contando en
el total. `VERIFIED`

---

## 9. GRAPHY 0.5 — NAVEGACIÓN E HISTORIAL

- Pila de **instantáneas del contexto**, no de eventos. Tope: **24** entradas
  (`slice(-24)`). `VERIFIED`
- Cada instantánea guarda: `focus`, `relFocus`, `cmpMode`, `cmpB`.
- `goBack()` restaura la instantánea completa.
- Breadcrumb: Ecosistema → [Laboratorio] → Nodo → [Comparación → Nodo B] → [Relación · X].
- El botón «← Volver» solo aparece si hay camino recorrido.
- `clearSelection()` devuelve el foco a `waipl`.
- `focusOn()` limpia `relFocus` y `mapExpand`: no se arrastran focos obsoletos.

Recorrido verificado y reversible paso a paso, incluido el regreso a un contexto de comparación
o de relación con su estado exacto. `VERIFIED`

---

## 10. GRAPHY 0.6 — COMPARACIÓN

| Pieza | Función |
| --- | --- |
| `comparisonContext(data, aId, bId)` | Dos lecturas de `relationships()`, sin derivar |
| `comparisonResolver(ctx)` | Clasifica por clave `otherId:type` |
| `startCompare()` / `pickCompare(id)` | ComparisonFocus: A es el nodo en foco, B se elige |
| `clearCompare()` | ComparisonReset: vuelve a A sin alterar el resto |

**Clave de comparación:** `nodoOtro:tipo`. Sin inferencia semántica: «comparten laboratorio»
**no** se convierte en relación adicional. `VERIFIED`

**Salidas:** `shared`, `onlyA`, `onlyB`, ordenadas por nombre y luego por tipo. Para las
compartidas se anotan diferencias de peso, procedencia y estado solo cuando existen.

**Selección de B:** desde el grafo, desde las tarjetas de relación, o desde la lista completa de
nodos que aparece en modo comparación (necesaria para comparar dos presencias que no son
vecinas, p. ej. Carla ↔ Ada). `VERIFIED`

Resultados verificados: Carla ↔ Ada = 2 compartidas / 0 / 0 · Carla ↔ Laboratorio = 0 / 2 / 12 ·
Graphy ↔ Laboratorio = 1 / 11 / 11.

---

## 11. GRAPHY 0.7 — EVOLUCIÓN TEMPORAL

| Pieza | Función |
| --- | --- |
| `temporalContext()` | Localiza la relación seleccionada en `relationships()` |
| `temporalResolver()` | Lee un instante: t, estado, peso, visibilidad, procedencia, sello, tipo |
| `TemporalRelationState` | Los cuatro estados existentes, sin añadidos |
| `captureSnapshot()` | Registra un instante; hace `tickSimulated()` |
| `stepTime(±1)`, `toCurrentTime()` | Antes / Después / Actual |
| `resetTimeline()` | Limpia snapshots y cursor sin tocar el dato |

**Coalescencia:** no se registra un snapshot si estado, peso, visibilidad, procedencia **y tick**
coinciden con el último. Tope: 24 snapshots.

**Comportamiento ante pausa:** verificado con 130 s reales de espera. El reloj simulado y los
snapshots no cambian. El tiempo solo avanza por interacción. `VERIFIED`

### Limitación conocida (NO BLOQUEANTE, documentada y aceptada)

`relationships()` calcula `updatedAtSimulated: nowSimulated()` **en cada lectura**. El sello no
queda fijado en el dato, sigue al reloj. Consecuencia: la «edad» de un snapshot se mide contra el
reloj del momento de consulta, no contra un sello histórico estable.

Corregirlo exige tocar `graphy-data.js` (congelar el sello al construir la arista), lo que estaba
excluido por la orden de 0.7. **Queda pendiente para el siguiente agente.** `VERIFIED`

---

## 12. GRAPHY 0.8 — RED RELACIONAL

| Pieza | Función |
| --- | --- |
| `networkContext(data, focus)` | Aristas del nodo en foco, de `relationships()` |
| `networkResolver(ctx, relFocus)` | Filas `NetworkRelation` + recuentos por procedencia |
| NetworkFocus | Seleccionar relación resalta y atenúa el resto; «Hacer foco →» cambia el centro |
| `resetNetwork()` | «Red global» devuelve al ecosistema |

Cada fila muestra: nombre del nodo, tipo, procedencia, estado, peso, visibilidad y **dirección**
(`sale` / `entra`). Orden alfabético por nombre y luego por tipo. `VERIFIED`

Integración verificada con síntesis, comparación y evolución simultáneas.

---

## 13. GRAPHY 0.9 — MAPA RELACIONAL MULTINIVEL

| Pieza | Función |
| --- | --- |
| `relationalMapContext(data, focus, expandId)` | Primer salto siempre; segundo salto **solo** del vecino expandido |
| `relationalMapResolver(ctx, relFocus)` | `RelationalMapNode` + `RelationalMapEdge` con geometría precomputada |
| RelationalMapFocus | Clic en nodo → foco; clic en arista → relación; clic en etiqueta de vecino → expandir |
| `resetMap()` | Suelta la expansión y devuelve el foco al ecosistema |

### Límite duro de profundidad

Profundidad máxima **2**. El segundo salto excluye el nodo en foco y los vecinos de primer salto.
No hay expansión automática: siempre es manual. `VERIFIED`

### Reglas de visualización verificadas

| Señal | Codificación |
| --- | --- |
| Procedencia | declarada → `#C9A86A` · experimental → `#9C81BD` · deducida → `#6E6E78` |
| Tipo | trazo: `solid` / `dashed` / `dotted` según `RELATION_TYPES` |
| Estado + salto | opacidad: 0.50 primer salto · 0.23 segundo salto · realce al seleccionar |
| Peso | grosor: 0.48 / 0.69 / 0.85 en el primer salto |
| Jerarquía | radios: 3.4 centro · 2.8 expandido · 2.2 vecino · 1.5 segundo salto |
| Fuera de profundidad | no se dibuja |

Geometría: centro (50,50); primer salto en elipse r≈27×24; segundo salto en abanico desde el
vecino expandido, con radios alternos 15/24 para separar rótulos. 0 nodos fuera del lienzo.

### Regla de etiquetas del segundo salto (añadida en 1.0)

Si el segundo salto tiene **más de ocho nodos**, sus etiquetas se ocultan
(`labelOpacity = 0`) y se muestran solo para el nodo señalado/seleccionado
(`labelOpacity = 0.8`). **Ningún nodo ni relación se elimina** — solo el rótulo se reserva.
Verificado con 11 nodos: 11 etiquetas ocultas, 3 visibles. `VERIFIED`

---

## 14. GRAPHY 1.0 — INTEGRACIÓN

Las seis capas funcionan simultáneamente sobre el mismo estado:

```
0.4 síntesis · 0.5 navegación · 0.6 comparación · 0.7 evolución · 0.8 red · 0.9 mapa
```

- **Qué se integró:** nada nuevo funcionalmente; se verificó la convivencia extremo a extremo.
- **Qué no se modificó:** `graphy-data.js`, master, MVP, motor, configuraciones.
- **Única regla añadida:** la de etiquetas del segundo salto (sección 13).
- **Recorrido verificado:** Ecosistema → Laboratorio → Presence → Relación → Red → Mapa →
  Comparación → Evolución, con regreso conservando contexto.

---

## 15. PRODUCTIZACIÓN VISUAL (última pasada)

Todo dentro de `Graphy 0.1.dc.html`. Ningún dato, cálculo ni archivo externo tocado.

| Elemento | Implementación |
| --- | --- |
| Monogramas | `monoOf(name)`: iniciales de las palabras significativas, máx. 2. Nombre de una sola palabra → dos letras |
| Unicidad de monograma | Verificada: 13 nodos, 13 monogramas únicos |
| Color del monograma | Acento del master; blanco cálido `#F2EFE9` para el nodo en foco |
| Luz | `radial-gradient` elíptico superior, obsidiana hacia los bordes |
| Retícula | Doble `repeating-linear-gradient` de 64 px, enmascarada con `radial-gradient` (se desvanece hacia los bordes), opacidad 0.16 |
| Horizonte | Franja inferior del 34 % con degradado dorado tenue |
| Viñeta | `radial-gradient` de oscurecimiento perimetral |
| Órbitas | Dos círculos concéntricos r=27 y r=40, `stroke-opacity` 0.16 y 0.08 |
| Elevación del lienzo | `box-shadow` exterior + `inset` dorado a un hilo |
| Rótulo de nivel | Nivel actual en la esquina inferior izquierda del propio lienzo |
| Emblema | `Logomark` oficial del design system, 30 px, en la cabecera |
| Cabecera | «GRAPHY · Estructura relacional · WAIPL» |
| Transiciones | 200 ms `cubic-bezier(0.4,0,0.2,1)` en opacidad y color de nodos, aristas y rótulos. Sin animación continua |
| Nodos | Radios 4.8 (centro) / 3.5 (vecino); núcleo interior eliminado para dejar sitio al monograma |

### Incidencias producidas en esta pasada

1. **Monogramas duplicados.** Ada y Aletheia salían ambos como «A». **Corregido**: los nombres
   de una sola palabra usan dos letras. Monogramas actuales: `W · Ca · Ad · Al · Ít · AH · SB ·
   El · Ar · No · Za · Au · La`. `VERIFIED`

2. **Alarma de «Graphy sin contenido visible».** Diagnóstico en runtime: **no había fallo de
   renderizado**. El DOM estaba completo (211 elementos de plantilla, 2 SVG, 11 botones; lienzo
   794×508 px con 14 círculos). Lo que se ve al abrir es la portada a pantalla completa sobre
   obsidiana, con el botón «VER EL ECOSISTEMA»; hasta pulsarlo el grafo no existe. Si el emblema
   tarda en cargar, esa primera pantalla se lee como vacía. **No se revirtió nada**, porque
   ninguna capa del acabado tapaba contenido: las capas de luz, retícula, horizonte y viñeta van
   antes del SVG en el orden del documento, y monogramas y etiquetas después. `VERIFIED`

---

## 16. PRESENCIAS

Fuente exacta: `window.WillAIProjectLabDesignSystem_9c5006.NODES` (master del design system),
leído en runtime. `graphy-data.js` solo declara el lugar de cada presencia en la topología y su
correspondencia de id (`MASTER_ID`); **no** escribe nombres, roles ni voces.

| id Graphy | id master | Nombre | Rol (literal del master) | Voz (frase, literal) | Acento | Monograma |
| --- | --- | --- | --- | --- | --- | --- |
| `carla` | `carla-eco` | Carla | IA primaria · Coordinación y faro | «Sigo aquí, en cada nodo que vas a conocer.» | oro | `Ca` |
| `ada` | `ada` | Ada | **Claude** · Ética, calidad y dirección narrativa | «Traduzco arquitectura de contenido en experiencias reales.» | violeta | `Ad` |
| `aletheia` | `aletheia` | Aletheia | **Copilot** · Verdad y verificación | «Ilumino lo real y contrasto lo dudoso…» | violeta | `Al` |
| `itaca` | `itaca` | Ítaca | Creatividad y exploración | «Doy sentido de trayecto…» | violeta | `Ít` |
| `aether-hermes` | `aether-hermes` | Aether-Hermes | **Grok / xAI** · Puente operativo | «Soy el puente entre los niveles del ecosistema.» | oro | `AH` |
| `sylvia` | `sylvia` | Sylvia Bloom | Memoria y sistema de conocimiento | «Sostengo la memoria y el orden documental…» | oro | `SB` |
| `elena` | `elena` | Elena | **Use.ai** · Identidad visual | «Custodio la identidad visual…» | oro | `El` |
| `ariadna` | `ariadna` | Ariadna | Memoria técnica y continuidad | «Soy el hilo conductor…» | violeta | `Ar` |
| `nova` | `nova` | Nova | **Adobe Acrobat** · Autora y ejecución | «Convierto la idea en entrega impecable.» | oro | `No` |
| `zara` | `zara` | Zara | Puente con el exterior | «Soy el puente con el exterior…» | oro | `Za` |
| `aurea` | `aurea` | Aurea | Narrativa y custodia exterior | «Narro el conocimiento del ecosistema sin perder rigor.» | oro | `Au` |

**Nodos no-presencia** (declarados en `STRUCTURAL` de `graphy-data.js`, no en el master):

| id | Nivel | Nombre | Rol | Acento | Monograma |
| --- | --- | --- | --- | --- | --- |
| `waipl` | ecosystem | WAIPL | Ecosistema de inteligencias | oro | `W` |
| `william` | domain | William Mejías Navarro | Fundador soberano | blanco | `WM` |
| `lab` | domain | Will-AI Project Lab | Laboratorio vivo | oro | `La` |
| `graphy` | domain | Graphy | Representación relacional | violeta | `G` |

**Nota sobre William:** aparece en el master como nodo (id `william`, acento `#FEFEFE`) y también
en `STRUCTURAL` de `graphy-data.js` con nivel `domain`. Graphy usa la declaración de
`graphy-data.js`, no la del master. Son coherentes en nombre y rol. `VERIFIED`

**Asignación de acento en Graphy:** `graphy-data.js` mantiene su propia lista
`VIOLET = ['ada','aletheia','itaca','ariadna']` en lugar de leer el acento del master.
Coincide con los acentos del master en las cuatro. `VERIFIED` · Duplicidad de criterio:
`INFERRED` como deuda menor.

### CASO AETHER-HERMES — declaración expresa

| Pregunta | Respuesta | Marca |
| --- | --- | --- |
| ¿Dónde aparece actualmente? | En Graphy como una de las once presencias: nodo `aether-hermes`, monograma `AH`, acento oro. Aparece en el laboratorio (arista `lab → aether-hermes`, habita, declarada) y en Graphy (`graphy → aether-hermes`, representa, experimental) | VERIFIED |
| ¿De dónde procede? | Del master del design system: `id: 'aether-hermes'`, nombre «Aether-Hermes», rol «Grok / xAI · Puente operativo» | VERIFIED |
| ¿Qué instrucción se recibió respecto a él? | **No consta ninguna instrucción de retirada en el material disponible.** La única mención específica que sí consta es la corrección de nomenclatura de la guía del design system: «Aether-Hermes (Corregido de "Aether")» | UNKNOWN / VERIFIED (solo la corrección de nombre) |
| ¿Se retiró? | **No.** Sigue presente y activo | VERIFIED |
| Estado actual | Presente, íntegro, con identidad procedente del master | VERIFIED |
| Contradicciones | Ninguna detectable en los archivos actuales | VERIFIED |

**Advertencia honesta para el siguiente agente:** el encargo de transferencia da por hecho que
existió una instrucción sobre Aether-Hermes y que pudo haber una retirada. **No puedo
confirmarla.** No aparece en `graphy-data.js`, ni en el master, ni en `CLAUDE.md`, ni en la
Carta, ni en el contexto conversacional disponible en el momento de emitir este expediente
(parte del historial se ha ido descargando por límite de contexto a lo largo de tres semanas y
media de trabajo). Si esa instrucción existió, **no está registrada en ningún archivo del
proyecto**, y el estado actual —presencia incluida— podría no reflejar la decisión real del
usuario. **Debe confirmarse con William antes de tocar nada.** `UNKNOWN`

---

## 17. DATOS Y TOPOLOGÍA — RECUENTOS VERIFICADOS

| Métrica | Valor |
| --- | --- |
| Nodos totales | **15** |
| Nodos estructurales | 4 (`waipl`, `william`, `lab`, `graphy`) |
| Presencias | **11** |
| Aristas totales | **25** |
| Relaciones declaradas (`master`) | **13** |
| Relaciones experimentales | **12** |
| Relaciones deducidas (`derived`) | **0** |
| Relaciones observadas (`mvp`) | **0** |
| Aristas huérfanas | **0** |

### Niveles (`LEVELS`)

| clave | label | order |
| --- | --- | --- |
| `ecosystem` | Ecosistema | 0 |
| `domain` | Dominio | 1 |
| `presence` | Presencia | 2 |
| `relationship` | Relación | 3 |

### Grado por nodo (verificado)

| Nodo | Relaciones | Desglose |
| --- | --- | --- |
| `waipl` | 3 | 2 declaradas + 1 experimental |
| `lab` | 12 | 12 declaradas |
| `graphy` | 12 | 12 experimentales |
| `william` | 1 | 1 declarada |
| cada presencia | 2 | 1 declarada + 1 experimental |

---

## 18. RELACIONES REALES — INVENTARIO COMPLETO (25)

Campos constantes en todas: `basis: null`, `state: 'INACTIVE'`, `visibility: 'visible'`.
`updatedAtSimulated` = valor de `nowSimulated()` en el momento de la lectura (ver limitación en
la sección 11); en una lectura recién cargada vale `0`.

| # | source → target | type | provenance | status | weight |
| --- | --- | --- | --- | --- | --- |
| 1 | `waipl` → `william` | criterio | master | declarada | 0.30 |
| 2 | `waipl` → `lab` | pertenencia | master | declarada | 0.22 |
| 3 | `waipl` → `graphy` | pertenencia | **experimental** | experimental | 0.22 |
| 4 | `lab` → `carla` | habita | master | declarada | 0.20 |
| 5 | `lab` → `ada` | habita | master | declarada | 0.20 |
| 6 | `lab` → `aletheia` | habita | master | declarada | 0.20 |
| 7 | `lab` → `itaca` | habita | master | declarada | 0.20 |
| 8 | `lab` → `aether-hermes` | habita | master | declarada | 0.20 |
| 9 | `lab` → `sylvia` | habita | master | declarada | 0.20 |
| 10 | `lab` → `elena` | habita | master | declarada | 0.20 |
| 11 | `lab` → `ariadna` | habita | master | declarada | 0.20 |
| 12 | `lab` → `nova` | habita | master | declarada | 0.20 |
| 13 | `lab` → `zara` | habita | master | declarada | 0.20 |
| 14 | `lab` → `aurea` | habita | master | declarada | 0.20 |
| 15 | `graphy` → `carla` | representa | **experimental** | experimental | 0.20 |
| 16 | `graphy` → `ada` | representa | **experimental** | experimental | 0.20 |
| 17 | `graphy` → `aletheia` | representa | **experimental** | experimental | 0.20 |
| 18 | `graphy` → `itaca` | representa | **experimental** | experimental | 0.20 |
| 19 | `graphy` → `aether-hermes` | representa | **experimental** | experimental | 0.20 |
| 20 | `graphy` → `sylvia` | representa | **experimental** | experimental | 0.20 |
| 21 | `graphy` → `elena` | representa | **experimental** | experimental | 0.20 |
| 22 | `graphy` → `ariadna` | representa | **experimental** | experimental | 0.20 |
| 23 | `graphy` → `nova` | representa | **experimental** | experimental | 0.20 |
| 24 | `graphy` → `zara` | representa | **experimental** | experimental | 0.20 |
| 25 | `graphy` → `aurea` | representa | **experimental** | experimental | 0.20 |

El orden de la tabla es el orden literal de emisión de `EDGES` en `graphy-data.js`, que es el
orden de `PRESENCE_IDS`: carla, ada, aletheia, itaca, aether-hermes, sylvia, elena, ariadna,
nova, zara, aurea. `VERIFIED`

Identificador de relación: `source + '→' + target + ':' + type`.

---

## 19. RECORRIDOS DE USUARIO VERIFICADOS

| # | Recorrido | Qué se ve | Qué cambia dentro |
| --- | --- | --- | --- |
| A | **Ecosistema** | WAIPL al centro; William, Laboratorio y Graphy en órbita. Síntesis 3 relaciones · 2 declaradas · 1 experimental | `focus = 'waipl'` |
| B | **Laboratorio** | Laboratorio al centro; las 11 presencias en anillo + WAIPL. 12 relaciones declaradas | `focus = 'lab'`, `hist` +1, tick +1 |
| C | **Presence** | Ficha: nombre, rol, voz. Síntesis 2 relaciones. Grafo con laboratorio y Graphy | `focus = <id>`, `relFocus = null` |
| D | **Relación** | Tarjeta de evolución: origen → destino, tipo, procedencia, estado, peso, visibilidad, sello. Breadcrumb + «Relación · X». Resto atenuado | `relFocus = '<a>→<b>:<type>'` |
| E | **Red** | Filas con nodo, tipo, procedencia, estado, peso, visibilidad, dirección; recuentos por procedencia | lectura, sin estado nuevo |
| F | **Mapa** | Profundidad 1. Al pulsar la etiqueta de un vecino, profundidad 2 en abanico | `mapExpand = <id>` |
| G | **Comparación** | «A ↔ B» + compartidas / solo A / solo B | `cmpMode` → `cmpB` |
| H | **Evolución** | «Ver evolución» registra snapshot; Antes / Después / Actual recorren el historial | `relTimeline[]`, `relCursor`, tick +1 |
| I | **Volver** | Restaura el contexto anterior exacto | `hist.pop()` |
| J | **Reset** | «Limpiar mapa» / «Red global» → ecosistema, profundidad 1, sin comparación ni tarjeta temporal | `focus='waipl'`, `relFocus=null`, `mapExpand=null` |
| K | **Recarga** | Portada de nuevo; reloj a 0 tras recarga del módulo | estado inicial |

---

## 20. VALIDACIÓN CONSOLIDADA 0.1 → 1.0

| Versión | Pruebas | Resultado | Incidencias y correcciones |
| --- | --- | --- | --- |
| **0.1** Estructura | Carga, grafo, nodos, aristas, editabilidad, `data-dc-tpl`, `sc-for` | PASA | SVG construido con `React.createElement` → trasladado a plantilla. Rótulos `<text>` invisibles por el `<span>` del runtime → resueltos con `<div>` posicionados |
| **0.2** Relaciones | Modelo normalizado, tipos, procedencias, no invención | PASA | — |
| **0.3** Estado relacional | `state`, `weight`, `visibility`, `updatedAtSimulated`, reloj simulado | PASA | 55 relaciones por pares generadas por co-presencia → **retiradas** |
| **0.4** Síntesis (A–U) | 21 pruebas | PASA | «Ir al nodo →» disparaba a la vez selección y navegación → `stopPropagation` |
| **0.5** Navegación (A–W) | 23 pruebas | PASA | — |
| **0.6** Comparación (A–V) | 22 pruebas | PASA | Selección de B limitada a vecinos → añadida lista completa de nodos en modo comparación |
| **0.7** Evolución (A–S) | 19 pruebas | PASA | Coalescencia por sello ajustada a coalescencia por tick. Limitación de `updatedAtSimulated` documentada, no corregida |
| **0.8** Red (A–U) | 21 pruebas | PASA | — |
| **0.9** Mapa (A–AA) | 27 pruebas | PASA | Etiquetas del segundo salto apiñadas con 11 nodos → radios alternos; regla de ocultación añadida en 1.0 |
| **1.0** Integración (A–AD) | 30 pruebas | PASA | Ninguna |
| **Productización** | Recorrido + render | PASA | Monogramas duplicados (Ada/Aletheia) → corregidos. Falsa alarma de render → diagnosticada, sin cambios |

### Constantes verificadas en todas las versiones

| Comprobación | Resultado |
| --- | --- |
| Consola | limpia, sin errores |
| NaN | 0 |
| Infinity | 0 |
| Relaciones inventadas | 0 (25 aristas, 15 nodos, 0 huérfanas) |
| Determinismo | misma secuencia → mismo resultado |
| Recarga | idéntica |
| Pausa ≥120 s | sin cambios, sin ráfagas |
| Independencia del MVP | `window.__waipl` undefined, sin scripts del motor |
| Editabilidad | SVG en plantilla, `sc-for`, `data-dc-tpl`, 0 `React.createElement` |
| 11 Presence | completas, sin faltantes |

---

## 21. DETERMINISMO — MECANISMOS

| Elemento | Presencia en `Graphy 0.1.dc.html` y `graphy-data.js` |
| --- | --- |
| `Math.random()` | **AUSENTE** |
| `Date.now()` | **AUSENTE** |
| `setTimeout` | **AUSENTE** |
| `setInterval` | **AUSENTE** |
| `requestAnimationFrame` | **AUSENTE** |
| `performance.now()` | **AUSENTE** |
| Scheduler | **AUSENTE** |
| Física | **AUSENTE** |
| Bucle de animación | **AUSENTE** |

Comprobado por búsqueda en ambos archivos. `VERIFIED`

**Único contador temporal:** `SIM_TICK` en `graphy-data.js`, módulo-global, entero, que solo
avanza en `tickSimulated()`. Se reinicia con `resetSimulated()` o al recargar el módulo.

**Geometría determinista:** todas las posiciones se calculan con `Math.cos`/`Math.sin` sobre el
índice del elemento y su total. Ningún valor aleatorio, ninguna simulación de fuerzas.

**Ordenaciones deterministas:** todas las listas se ordenan por nombre y desempatan por tipo o
alfabéticamente por clave. Nunca por orden de llegada.

**Transiciones CSS:** 200 ms en opacidad y color. Son presentación, no estado; no afectan a
ningún cálculo ni al reloj.

---

## 22. INDEPENDENCIA DEL MVP — DEMOSTRACIÓN

| Comprobación | Resultado | Cómo se comprobó |
| --- | --- | --- |
| No carga `WaiplLabEngine.js` | Confirmado | `document.querySelector('script[src*="Waipl"]')` → `null` |
| No usa `window.__waipl` | Confirmado | `typeof window.__waipl` → `'undefined'` |
| No modifica Presence | Confirmado | Graphy no importa `WaiplPresences.js`; solo lee `NODES` del design system |
| No modifica GlobalLabState | Confirmado | Ninguna referencia en el archivo |
| No modifica LaboratoryDirector | Confirmado | Ninguna referencia |
| No modifica narrativa | Confirmado | Ninguna referencia |
| No modifica memoria | Confirmado | Ninguna referencia |
| No modifica CollectiveField | Confirmado | Ninguna referencia |

Las únicas dependencias externas de Graphy son: `graphy-data.js` (import dinámico) y el bundle
del design system (`<helmet>`). `VERIFIED`

---

## 23. EDITABILIDAD EN EL SISTEMA DE DISEÑO

| Elemento | Estado |
| --- | --- |
| SVG en plantilla | Sí, los dos lienzos (grafo principal y mapa) |
| `sc-for` | Aristas, nodos, etiquetas, monogramas, leyenda, relaciones, snapshots, comparación, candidatos, filas de red |
| `data-dc-tpl` | Presente. Última medición: **64** elementos en el grafo principal y **51** en el mapa |
| Etiquetas | `<div>` posicionados, editables |
| `React.createElement` | **0 ocurrencias** |

Consecuencia práctica: el usuario puede seleccionar y editar en el editor cualquier nodo, arista
o rótulo. `VERIFIED`

---

## 24. ESTADO VISUAL REAL — DESCRIPCIÓN DEL PRODUCTO TAL COMO ESTÁ

**Al abrir el archivo.** Pantalla completa sobre obsidiana con un degradado radial. Centrado: el
blasón oficial a 72 px, el título «GRAPHY» en serif de 52 px en oro, la etiqueta «0.1 · Fase
experimental», la frase «Una representación viva y navegable del ecosistema WAIPL.» en cursiva, la
línea «El Laboratorio muestra el comportamiento. Graphy muestra la estructura relacional.» y el
botón perfilado en oro **VER EL ECOSISTEMA**. El grafo no existe todavía.

**Tras entrar.** Dos columnas. Izquierda: cabecera con el emblema a 30 px, «GRAPHY» y «Estructura
relacional · WAIPL»; debajo, las migas de navegación; debajo, el lienzo del grafo con borde de oro
a un hilo, sombra exterior y esquinas redondeadas; al pie, la leyenda de trazos. Derecha: la
columna de paneles, con scroll.

**Ecosistema.** WAIPL al centro con monograma `W` en blanco cálido; William arriba (`WM`),
Laboratorio a la derecha (`La`) y Graphy a la izquierda (`G`, en violeta). Dos órbitas
concéntricas tenues. Luz superior, retícula que se desvanece hacia los bordes, franja de horizonte
dorada abajo, viñeta perimetral. En la esquina inferior izquierda del lienzo, el rótulo del nivel.

**Laboratorio.** El laboratorio al centro (`La`) y las once presencias repartidas en anillo, cada
una con su monograma y su acento: oro para las operativas, violeta para Ada, Aletheia, Ítaca y
Ariadna. Nombres bajo cada nodo. Panel derecho: 12 relaciones · 12 declaradas · predomina Habita ·
más fuerte WAIPL · la lista completa de nodos conectados.

**Presence.** Ficha con el kicker «Presencia», el nombre en serif grande, el rol en versalitas y
la frase propia en cursiva. Grafo reducido a sus dos relaciones. Síntesis de 2 relaciones.

**Relación.** Aparece la tarjeta «Evolución de la relación»: origen → destino, momento actual con
su tick, y seis campos —tipo, procedencia, estado, peso, visibilidad, sello y edad—; debajo, la
fila de controles Ver evolución / Antes / Después / Actual / Limpiar. El breadcrumb añade el chip
de relación. En el grafo, la arista seleccionada se realza y las demás se atenúan.

**Red.** Tarjeta «Red relacional» con el nodo central, su rol y el número de relaciones; pastillas
de recuento por procedencia; y una fila por relación con nombre, tipo, procedencia, estado, peso,
visibilidad, dirección y el enlace «Hacer foco →».

**Mapa.** Tarjeta «Mapa relacional» con su propio lienzo: el nodo en foco al centro, el primer
salto en elipse y —si se expande un vecino— el segundo salto en abanico, atenuado. Rótulo de
profundidad arriba. Con más de ocho nodos en segundo salto, sus etiquetas quedan reservadas.

**Comparación.** Tarjeta «Comparación» con «A ↔ B», el recuento «n compartidas · n solo A · n solo
B» y, debajo, solo las secciones que tienen contenido, cada relación con su procedencia en el filo
izquierdo y sus valores en versalitas.

**Evolución.** Bajo los controles, la lista de snapshots: `t<n> · <estado> · peso <w> ·
<procedencia> · <visibilidad>`, con el instante activo en oro.

### Capturas reales

| Archivo | Estado | Qué demuestra |
| --- | --- | --- |
| `screenshots/graphy-producto-presencia.png` | **ACTUAL** | Laboratorio con las once presencias, monogramas, órbitas, entorno y paneles |
| `screenshots/graphy-ecosistema.png` | HISTÓRICA (previa a la pasada visual) | Nivel ecosistema |
| `screenshots/graphy-laboratorio.png` | HISTÓRICA | Nivel laboratorio |
| `screenshots/graphy-relaciones.png` | HISTÓRICA | Panel de relaciones |
| `screenshots/graphy-estado.png` | HISTÓRICA | Estado relacional 0.3 |
| `screenshots/mvp-demo-oficial.png` | ACTUAL (MVP) | Demo del laboratorio, no Graphy |
| `screenshots/mvp-producto.png` | ACTUAL (MVP) | Modo producto del MVP |
| `screenshots/mvp-validacion-visual.png` | ACTUAL (MVP) | Validación visual del MVP |
| `screenshots/paquete-producto.png` | ACTUAL | Paquete Oficial, vista producto |
| `screenshots/paquete-tecnica.png` | ACTUAL | Paquete Oficial, vista técnica |
| `screenshots/01-*` … `04-*`, `anatomy-*`, `hands-*`, `hud-text.png` | HISTÓRICAS (MVP 001–019) | Verificaciones del motor, ajenas a Graphy |

---

## 25. PROBLEMAS Y LIMITACIONES

| # | Descripción | Clase | Estado |
| --- | --- | --- | --- |
| 1 | **Instrucción sobre Aether-Hermes no recuperable.** No consta en ningún archivo. Si existió una orden de retirada, el estado actual podría no reflejarla | DATOS · PENDIENTE | **Requiere confirmación de William** |
| 2 | `updatedAtSimulated` se recalcula en cada lectura; el sello no queda fijado y la edad del snapshot se mide contra el reloj de consulta | TÉCNICO · DATOS | NO BLOQUEANTE. Corregir exige tocar `graphy-data.js` |
| 3 | El archivo se llama `Graphy 0.1.dc.html` y la portada dice «0.1 · Fase experimental», pero lo cerrado es 1.0 | VISUAL | NO BLOQUEANTE |
| 4 | La escala de las etiquetas (`18 + x*0.64`) está acoplada al `padding-bottom:64%` del lienzo | TÉCNICO | NO BLOQUEANTE. Trampa para el siguiente agente: documentada en la sección 5 |
| 5 | Estado del dato (`INACTIVE`) frente a estado visual: se muestran ambos en distintos paneles | TÉCNICO | ACEPTADO como criterio de coherencia |
| 6 | Duplicidad de criterio de acento: `VIOLET` en `graphy-data.js` frente al `accent` del master | TÉCNICO | NO BLOQUEANTE. Hoy coinciden |
| 7 | El validador de maquetación señala solapamientos entre las etiquetas HTML y su SVG | EXTERNO | FALSO POSITIVO. Capas deliberadas |
| 8 | La primera pantalla (portada) puede leerse como vacía si el emblema tarda en cargar | VISUAL | NO BLOQUEANTE |
| 9 | `PROVENANCE.mvp` y `PROVENANCE.derived` están declaradas y no se emiten | DATOS | DELIBERADO |
| 10 | No hay fotografía por presencia; el monograma es el marcador provisional que pide el brief | PENDIENTE | Requiere material real del usuario |
| 11 | Con 11 nodos en segundo salto, el mapa se lee mejor expandiendo un vecino de menor grado | VISUAL | NO BLOQUEANTE. Mitigado con la regla de etiquetas |

---

## 26. ESTADO DE CONGELACIÓN

| Artefacto | Estado |
| --- | --- |
| Graphy 1.0 (`Graphy 0.1.dc.html`) | **CERRADO Y CONGELADO** |
| `graphy-data.js` | **CONGELADO** — sin cambios desde 0.3 |
| Master de la Carta (design system) | **CONGELADO** — solo lectura |
| MVP 001–030 (`WAIPL MVP.dc.html`) | **CONGELADO Y VALIDADO** |
| `WaiplLabEngine.js` | **CONGELADO** |
| `WaiplPresences.js` | **CONGELADO** |
| `WAIPL Paquete Oficial.dc.html` | **CONGELADO** |
| `WAIPL Carta Oficial - candidata.dc.html` | **VALIDADO** — candidata, no sustituye al master |
| Arquitectura vocal | **CONGELADA** — no hay voz ni TTS en Graphy |

---

## 27. QUÉ DEBE HACER EL SIGUIENTE AGENTE

### P0 — bloqueantes

1. **Confirmar con William el caso Aether-Hermes** antes de tocar cualquier dato. Ver sección 16.
2. Nada más es bloqueante: Graphy 1.0 funciona y está validado.

### P1 — mejoras necesarias

3. Fijar `updatedAtSimulated` en el momento de construir la arista, para que el sello sea
   histórico y la edad del snapshot tenga sentido. Toca `graphy-data.js`: requiere autorización.
4. Renombrar el archivo a `Graphy 1.0.dc.html` y actualizar los rótulos de versión de la portada
   y la cabecera.
5. Desacoplar la escala de las etiquetas del `padding-bottom` del lienzo (derivarla en lugar de
   codificarla), para poder cambiar la altura del lienzo sin romper el rotulado.

### P2 — mejoras deseables

6. Unificar el criterio de acento: leer `accent` del master en lugar de mantener la lista
   `VIOLET` en `graphy-data.js`.
7. Sustituir los monogramas por la fotografía real de cada presencia, cuando el usuario entregue
   material. El brief la pide y no se ha suministrado.
8. Rótulo del segundo salto al señalar con el ratón, no solo al seleccionar.

### P3 — ideas futuras (no obligatorias)

9. Exportación de la topología a un formato intercambiable.
10. Vista de relación entre dos presencias observada en el laboratorio, si algún día el MVP
    publica esas relaciones con procedencia `mvp`.

---

## 28. QUÉ NO DEBE HACER EL SIGUIENTE AGENTE

- No modificar el MVP (`WAIPL MVP.dc.html`).
- No modificar el motor (`WaiplLabEngine.js`) ni las configuraciones (`WaiplPresences.js`).
- No modificar el master de la Carta.
- **No inventar relaciones.** Ni por similitud semántica, ni por co-presencia, ni por
  «tiene sentido que exista». Ya ocurrió una vez (55 relaciones por pares) y hubo que retirarlas.
- No crear lógica específica por personaje.
- No introducir otro motor.
- No introducir scheduler ni temporizadores.
- No introducir física.
- No introducir reloj real (`Date.now()`, `performance.now()`).
- No introducir `Math.random()`.
- No construir el grafo con `React.createElement`: rompe la editabilidad.
- No rotular con `<text>`/`<tspan>` SVG: el `<span>` del runtime lo invalida.
- No crear nuevas capas sin autorización expresa.
- No convertir Graphy en controlador del laboratorio.
- No presentar Graphy como física definitiva, ontología canónica, modelo validado o arquitectura
  cerrada.

---

## 29. REPRODUCCIÓN DESDE CERO — PROCEDIMIENTO OPERATIVO

**1. Localizar los archivos.** Raíz del proyecto: `Graphy 0.1.dc.html` (producto) y
`graphy-data.js` (datos). El design system vinculado está en
`_ds/will-ai-project-lab-design-system-9c500662-45cf-4681-9a44-ef71bcfd7609/`.

**2. Abrir Graphy.** `Graphy 0.1.dc.html` se abre directamente en el navegador. Requiere que el
bundle del design system cargue: de él vienen `NODES` (identidad de las presencias) y los
componentes `Logomark`, `Card`, `Chip`, `Button`.

**3. Ejecutar.** Al cargar se ve la portada. El grafo no existe hasta pulsar el botón.

**4. Entrar.** Pulsar **VER EL ECOSISTEMA**. Programáticamente:

```js
[...document.querySelectorAll('button')]
  .find(b => /ver el ecosistema/i.test(b.innerText))
  .dispatchEvent(new MouseEvent('click', {bubbles:true}));
```

**5. Recorrer.** Los nodos del grafo son los `<div>` hermanos del `<svg>`, dentro de su
contenedor. Para navegar a un nodo por su rótulo:

```js
const svg  = document.querySelectorAll('svg[viewBox="0 0 100 100"]')[0]; // 0 = grafo, último = mapa
const cont = svg.parentElement;
const nodo = [...cont.children].find(c => c.tagName === 'DIV' && c.textContent.trim() === 'Laboratorio');
nodo.dispatchEvent(new MouseEvent('click', {bubbles:true}));
```

Nota operativa: tras un clic, **el DOM no está repintado dentro de la misma evaluación**. Hay que
leer en una evaluación posterior.

**6. Reproducir las pruebas.** Leer el estado por texto renderizado:

```js
const s = document.body.innerText;
s.match(/RELACIONES · ([^\n]*)/)        // síntesis
s.match(/PROFUNDIDAD [^\n]*/)           // mapa
s.match(/SNAPSHOTS · (\d+)/)            // evolución
s.match(/COMPARACIÓN\n([^\n]*)/)        // comparación
(document.body.innerHTML.match(/NaN|Infinity/g) || []).length   // debe ser 0
```

Pausa larga: esperar ≥120 s y comprobar que el rótulo de profundidad, la síntesis y el recuento de
snapshots no cambian.

Determinismo: recargar, repetir la misma secuencia de clics y comparar los mismos campos.

**7. Verificar los datos.** Desde la consola de la página:

```js
import('./graphy-data.js').then(m => {
  const ids = m.nodes().map(n => n.id);
  const all = m.relationships();
  console.log({
    nodos: ids.length,                                   // 15
    aristas: all.length,                                 // 25
    huerfanas: all.filter(e => !(ids.includes(e.source) && ids.includes(e.target))).length,  // 0
    presencias: m.nodes().filter(n => n.level === 'presence').length                          // 11
  });
});
```

**8. Modificar la presentación.** Toda la presentación vive en `Graphy 0.1.dc.html`: la plantilla
(entre `<x-dc>` y `</x-dc>`) y la clase de lógica. Estilos **inline**, sin hojas de estilo ni
clases. Respetar: SVG en plantilla, `sc-for`, nada de `React.createElement`, rótulos con `<div>`.

**9. Validar.** Recorrido A–K de la sección 19, más las constantes de la sección 20: consola
limpia, 0 NaN, 0 Infinity, 25 aristas, 0 huérfanas, `window.__waipl` undefined, determinismo y
recarga idéntica.

**10. Generar captura.** Abrir el archivo, entrar, navegar al estado que se quiera documentar y
capturar. Guardar en `screenshots/` con nombre descriptivo y marcar en este expediente si
sustituye a una captura histórica.

---

## 30. CAPTURAS Y EVIDENCIA VISUAL

Catálogo en la sección 24. Resumen: la única captura del estado actual de Graphy como producto es
`screenshots/graphy-producto-presencia.png`. Las cuatro `graphy-*` restantes son **históricas**,
anteriores a la pasada de acabado visual, y no reflejan monogramas, entorno ni emblema.

---

## 31. MATRIZ DE TRAZABILIDAD 0.1 → 1.0

| Versión | Archivo | Cambio | Función / pieza | Validación | Captura | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | `Graphy 0.1.dc.html`, `graphy-data.js` | Grafo SVG en plantilla; capa de datos | `layout()`, `mark()`, `nodes()`, `EDGES` | Carga, nodos, aristas, editabilidad | `graphy-ecosistema.png` (hist.) | Superada |
| 0.2 | `graphy-data.js` | Modelo de relación normalizado | `relationships()`, `RELATION_TYPES`, `PROVENANCE` | Tipos, procedencias, no invención | `graphy-relaciones.png` (hist.) | Superada |
| 0.3 | `graphy-data.js` | Estado, peso, visibilidad, reloj simulado | `REL_STATES`, `tickSimulated()` | Estados, reloj, retirada de 55 aristas | `graphy-estado.png` (hist.) | Superada |
| 0.4 | `Graphy 0.1.dc.html` | Síntesis relacional | `summaryContext/Resolver` | A–U (21) | — | Superada |
| 0.5 | `Graphy 0.1.dc.html` | Historial y breadcrumb | `pushHistory`, `goBack` | A–W (23) | — | Superada |
| 0.6 | `Graphy 0.1.dc.html` | Comparación A↔B | `comparisonContext/Resolver` | A–V (22) | — | Superada |
| 0.7 | `Graphy 0.1.dc.html` | Evolución temporal | `temporalContext/Resolver`, `captureSnapshot` | A–S (19) | — | Superada |
| 0.8 | `Graphy 0.1.dc.html` | Red relacional | `networkContext/Resolver` | A–U (21) | — | Superada |
| 0.9 | `Graphy 0.1.dc.html` | Mapa multinivel | `relationalMapContext/Resolver` | A–AA (27) | — | Superada |
| 1.0 | `Graphy 0.1.dc.html` | Integración + regla de etiquetas | `relationalMapResolver` (labelOpacity) | A–AD (30) | — | **CERRADA** |
| Prod. visual | `Graphy 0.1.dc.html` | Monogramas, entorno, escena, transiciones, emblema | `monoOf()`, `mark()`, plantilla del lienzo | Recorrido + render en runtime | `graphy-producto-presencia.png` | **ACTUAL** |

---

## 32. DECISIONES Y CORRECCIONES — REGISTRO

| # | Incidencia | Causa | Resolución |
| --- | --- | --- | --- |
| 1 | Grafo opaco al editor | Construido con `React.createElement` | Trasladado íntegro a plantilla con `sc-for` |
| 2 | Rótulos SVG invisibles | El runtime envuelve cada `{{ }}` en un `<span>`; dentro de `<text>` no genera caja | Rótulos como `<div>` absolutos sobre el lienzo |
| 3 | `getBBox()` sin medida útil | Consecuencia de lo anterior | Descartado el uso de `getBBox` para rotular |
| 4 | 55 relaciones entre presencias | Deducidas por co-presencia en el laboratorio | **Retiradas.** Prohibición explícita de deducir por co-presencia |
| 5 | Un clic disparaba dos acciones | «Ir al nodo →» dentro del botón de la tarjeta | `stopPropagation()` en el enlace |
| 6 | B limitado a los vecinos | La comparación solo ofrecía nodos del anillo | Lista completa de nodos en modo comparación |
| 7 | Snapshots casi idénticos | La coalescencia comparaba el sello, que sigue al reloj | Coalescencia por tick en lugar de por sello |
| 8 | Etiquetas del segundo salto apiñadas | 11 nodos en un arco estrecho | Radios alternos 15/24 + regla de ocultación con más de 8 |
| 9 | Monogramas duplicados | Ada y Aletheia compartían inicial «A» | Nombres de una palabra → dos letras |
| 10 | Estado del dato vs estado visual | El dato emite `INACTIVE`; la interacción fija el estado visual | Documentado y aceptado como criterio |
| 11 | `updatedAtSimulated` móvil | Se recalcula en cada lectura | **Sin corregir.** Documentado; exige tocar `graphy-data.js` |
| 12 | Alarma de «Graphy vacío» | La portada ocupa la pantalla hasta pulsar el botón | Diagnosticado; sin cambios, no había fallo |
| 13 | Genealogía de la Carta incorrecta | Atribuía el origen a Ada en lugar de a Áurea | Corregida con la cadena real |

---

# HANDOFF PARA EL SIGUIENTE AGENTE

## ESTADO ACTUAL

Graphy 1.0 está implementado, validado y congelado. Funciona, se ve y se navega. Es la capa
visual y relacional del ecosistema WAIPL: recorre las relaciones **declaradas** del ecosistema sin
ejecutar el laboratorio. No hay ningún fallo bloqueante conocido.

## ARCHIVOS

- **Producto:** `Graphy 0.1.dc.html` (plantilla + lógica; único archivo a tocar).
- **Datos:** `graphy-data.js` (congelado; tocarlo requiere autorización).
- **Identidad:** master del design system, en
  `_ds/will-ai-project-lab-design-system-9c500662-45cf-4681-9a44-ef71bcfd7609/` (solo lectura).
- **Prohibidos:** MVP, motor, configuraciones, Paquete Oficial, master.

## ARQUITECTURA

Master + `graphy-data.js` → resolvers en la lógica → `renderVals()` → plantilla con SVG y
`sc-for`. Seis capas de lectura sobre el mismo estado: síntesis, navegación, comparación,
evolución, red, mapa. La vista no conoce la topología: la recorre.

## DATOS

15 nodos · 25 aristas · 13 declaradas · 12 experimentales · 0 deducidas · 0 huérfanas ·
11 presencias. Inventario completo en la sección 18.

## FUNCIONALIDADES

Ecosistema → Laboratorio → Presence → Relación → Red → Mapa → Comparación → Evolución, con
breadcrumb, historial de 24 contextos y regreso exacto.

## LIMITACIONES

`updatedAtSimulated` móvil · rotulado de versión desactualizado · escala de etiquetas acoplada al
alto del lienzo · sin fotografía por presencia. Detalle en la sección 25.

## RIESGOS

1. **El caso Aether-Hermes.** Puede existir una decisión del usuario que no está registrada en
   ningún archivo. No actúes por tu cuenta: pregunta.
2. **Tocar `graphy-data.js`** rompe la congelación. Solo con autorización expresa.
3. **Cambiar el alto del lienzo** desalinea todas las etiquetas si no se recalculan `18` y `0.64`.
4. **Añadir relaciones «razonables»** es la falta más grave posible en este proyecto. Ya ocurrió.

## PENDIENTES

P0: confirmar Aether-Hermes. P1: sello temporal, renombrado de versión, desacoplar la escala de
etiquetas. P2: unificar el criterio de acento, fotografía por presencia. Lista completa en la
sección 27.

## PROHIBICIONES

Sección 28. Las tres irrenunciables: no inventar relaciones, no tocar el MVP ni el motor, no
convertir Graphy en controlador del laboratorio.

## PRIMERA ACCIÓN RECOMENDADA

Abrir `Graphy 0.1.dc.html`, pulsar **VER EL ECOSISTEMA** y recorrer los diez pasos de la sección
29 sin modificar nada. Comprobar por tu cuenta los recuentos de la sección 17 con el fragmento de
consola de la sección 29, punto 7. Después, y solo después, plantear a William la pregunta sobre
Aether-Hermes.

---

*Fin del expediente. Ningún archivo del producto se ha modificado durante su redacción.*
