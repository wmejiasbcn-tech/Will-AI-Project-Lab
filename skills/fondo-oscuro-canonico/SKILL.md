---
name: fondo-oscuro-canonico
description: Orden permanente de William (09-11-2026, in aeternum) — ningún documento que él deba leer puede tener fondo blanco. Estándar #121212 hasta el borde, método Chromium/Playwright o WeasyPrint. Usar al generar PDF, HTML o cualquier informe para lectura de William.
---

# Fondo oscuro canónico WAIPL

## Orden soberana (in aeternum)

Orden permanente de William Mejías Navarro (09-11-2026): **ningún documento o informe que él deba leer puede tener fondo blanco**. Fondo siempre oscuro por salud visual (fotosensibilidad).

Esta skill es la referencia técnica para nodos y agentes del WAIPL. No sustituye el [CANON_IDENTIDAD_VISUAL_DOCUMENTAL_WAIPL_v1.0](../../00_SISTEMA/GOBERNANZA/CANON_IDENTIDAD_VISUAL_DOCUMENTAL_WAIPL_v1.0.md); lo completa en el punto del fondo de página y del método de impresión a PDF.

## Estándar de color

| Elemento | Hex |
|---|---|
| Página y cuerpo | `#121212` |
| Texto | `#E6E6E6` |
| h1 | `#FFFFFF` |
| h2 | `#9CC9FF` |
| h3 | `#B8D8FF` |
| Enlaces | `#8AB4F8` |
| Código (fondo / texto) | `#1F1F1F` / `#F0C674` |
| Bloque `pre` | `#1A1A1A` |
| Cabecera de tabla (`th`) | `#232323` |
| Filas pares | `#181818` |
| Bordes | `#333` / `#3A3A3A` |

## Blasón

El blasón oficial va **arriba a la izquierda** en cada página, **byte-idéntico** al archivo oficial, nunca retocado (geometría, proporciones, colores, tipografía integrada, efectos).

## Reglas obligatorias (sin ellas sale blanco)

1. `@page{size:A4;margin:0}` — el margen de la hoja a cero; si no, Chrome pinta ese margen en blanco.
2. `html` y `body` con `background:#121212`. El margen visual lo da el `padding` del body: `16mm 14mm`.
3. Impresión con fondos incluidos:
   - **Chromium / Playwright** `page.pdf`: `printBackground:true` y márgenes `'0'`.
   - **WeasyPrint**: además `background:#121212` **dentro** de `@page` (WeasyPrint pinta la hoja desde ahí).
   - **Navegador a mano**: márgenes «Ninguno» + casilla «Gráficos de fondo» activada.
   - **ReportLab**: en cada página, rectángulo de relleno `#121212` a página completa **antes** de dibujar nada más.

## CSS canónico

```css
@page{size:A4;margin:0}
html{background:#121212}
body{margin:0;padding:16mm 14mm;background:#121212;color:#E6E6E6;font-family:'DejaVu Sans',Arial,sans-serif;font-size:10.5pt;line-height:1.45}
h1{color:#FFFFFF;font-size:19pt;border-bottom:2px solid #3A3A3A;padding-bottom:6px}
h2{color:#9CC9FF;font-size:14pt;margin-top:20px;border-bottom:1px solid #2E2E2E;padding-bottom:3px}
h3{color:#B8D8FF;font-size:12pt}
a{color:#8AB4F8}
code{background:#1F1F1F;color:#F0C674;padding:1px 4px;border-radius:3px;font-size:9pt}
pre{background:#1A1A1A;border:1px solid #333;padding:8px;border-radius:4px;white-space:pre-wrap;font-size:8.6pt}
pre code{background:none;color:#D0D0D0}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:9pt}
th{background:#232323;color:#FFFFFF}
th,td{border:1px solid #3A3A3A;padding:4px 6px;vertical-align:top}
tr:nth-child(even) td{background:#181818}
strong{color:#FFFFFF}
img{max-width:100%;border:1px solid #333;margin:6px 0}
hr{border:0;border-top:1px solid #333}
```

Para WeasyPrint, añadir también dentro de `@page`:

```css
@page{size:A4;margin:0;background:#121212}
```

## Script mínimo Playwright (Node.js)

Sin rutas ni secretos del entorno de ejecución. Sustituir las rutas por las del propio nodo.

```js
import { chromium } from 'playwright-core'

const browser = await chromium.launch({
  // executablePath: ruta al Chrome/Chromium del entorno
  args: ['--no-sandbox'],
})
const page = await browser.newPage()
await page.goto('file:///ruta/INFORME.html')
await page.pdf({
  path: '/ruta/INFORME.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '0', bottom: '0', left: '0', right: '0' },
})
await browser.close()
```

Flujo habitual: Markdown → HTML (p. ej. `marked`) con el CSS de arriba → `page.pdf` con las tres reglas obligatorias.

## Equivalencias

| Herramienta | Qué no olvidar |
|---|---|
| Playwright / Chromium | `printBackground:true` + márgenes `'0'` + `@page margin:0` |
| WeasyPrint | `background:#121212` también dentro de `@page` |
| Impresión manual del navegador | Márgenes «Ninguno» + «Gráficos de fondo» |
| ReportLab | `canvas.setFillColor(HexColor('#121212'))` y `canvas.rect(0,0,*A4,fill=1,stroke=0)` antes de dibujar |

## Verificación antes de entregar

1. Renderizar cada página a PNG (`pdftoppm` u equivalente).
2. Leer los píxeles de las cuatro esquinas y del borde.
3. **Ningún píxel de esquinas o bordes puede ser `#FFFFFF`.**

Si aparece blanco: casi siempre falta `printBackground`, o hay margen en `@page` / en `page.pdf`, o WeasyPrint no lleva el fondo dentro de `@page`.

## Prohibiciones

- Fondo blanco o claro en cualquier página que William deba leer.
- Retocar el blasón oficial.
- Entregar un PDF sin la verificación de píxeles de borde cuando el nodo genera el PDF.
