# GRAPHY — Casa canónica (1.0)

**Estado:** 1.0 cerrado y validado. Archivo rotulado `Graphy 0.1.dc.html` (el nombre no se renombró al cerrar).
**Naturaleza:** capa visual, navegable y relacional del ecosistema WAIPL.
**No es:** el laboratorio, un motor, Graphify, un validador, ni autoridad sobre VÁR/YATA.

> El Laboratorio muestra el comportamiento. Graphy muestra la estructura relacional.

## Dónde está cada cosa

| Qué | Dónde |
| --- | --- |
| Producto | `producto/Graphy 0.1.dc.html` |
| Topología (única fuente de aristas) | `producto/graphy-data.js` |
| Runtime Design Components (no editar) | `producto/support.js` + `producto/_ds/` |
| Expediente de transferencia | `expediente/GRAPHY-TRANSFERENCIA.md` |
| Topología declarada (mapa) | `TOPOLOGIA.md` y `topologia.html` |

## Arquitectura real (3 capas)

1. **Master de la Carta** (design system, solo lectura) — identidad: nombre, rol, voz, acento.
2. **`graphy-data.js`** — topología, tipos, procedencia, reloj simulado. Congelado desde 0.3.
3. **`Graphy 0.1.dc.html`** — vista e interacción. No conoce la topología: la recorre.

Graphy **no** carga `WaiplLabEngine` ni el MVP.

## Prohibido

- Inventar relaciones entre Presence.
- Crear jerarquía núcleo / colaboradores. El orden es de presentación, no de rango.
- Mezclar Graphy con Graphify.
- Convertir aristas `experimental` en hechos del master.
- Publicar en Vercel este paquete como si sustituyera la Carta sin autorización soberana.

## Reloj

El reloj de Graphy es simulado. Avanza solo con interacción. No hay scheduler ni hora real.

## Nombre de Aether

Orden soberana 2026-09-07: Aether es solo Aether. Hermes es otro. Ver `ORDEN_SOBERANA_AETHER_2026-09-07.md`.

## Lectura para agentes

Primero fuente → después representación → después interpretación.

Si algo no está en `graphy-data.js` o en el expediente:

> No especificado en las fuentes proporcionadas.
