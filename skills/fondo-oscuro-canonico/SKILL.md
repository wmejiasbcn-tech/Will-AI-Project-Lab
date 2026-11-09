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

**Cómo repetirlo en cada página (Chromium/Playwright):** envolver todo el contenido en una tabla de maquetación cuya **cabecera (`thead`) se repite** en cada página impresa, con el blasón **incrustado** en el HTML (`data:image/png;base64,…` leído del archivo oficial). No usar `position:fixed` con una ruta `file://`: en la prueba del 09-11-2026 el blasón no apareció en ninguna página. La cabecera repetida reserva además el espacio superior en todas las páginas, no solo en la primera.

```html
<body>
<table class="layout">
  <thead><tr><td><div class="hdr"><img src="data:image/png;base64,BASE64_DEL_BLASON_OFICIAL" alt="Blasón WAIPL"></div></td></tr></thead>
  <tbody><tr><td><!-- contenido del informe --></td></tr></tbody>
  <tfoot><tr><td><div class="ftr"></div></td></tr></tfoot>
</table>
</body>
```

```css
table.layout,table.layout>thead>tr>td,table.layout>tbody>tr>td,table.layout>tfoot>tr>td{border:0;padding:0;background:#121212;margin:0;font-size:10.5pt}
table.layout{width:100%;border-collapse:collapse}
.hdr{height:30mm;position:relative}
.hdr img{position:absolute;top:6mm;left:-6mm;width:20mm;height:20mm}
.ftr{height:12mm}
/* las filas pares oscuras solo para las tablas de contenido */
table:not(.layout) tr:nth-child(even) td{background:#181818}
```

Con esta maqueta, el `padding` del body pasa a ser `0 14mm` (el espacio superior e inferior lo dan `.hdr` y `.ftr`).

## Reglas obligatorias (sin ellas sale blanco)

1. `@page{size:210mm 297mm;margin:0}` — tamaño explícito en milímetros y margen de la hoja a cero; si hay margen, Chrome lo pinta en blanco.
2. `html` y `body` con `background:#121212`. El margen visual lo da el `padding` del body: `16mm 14mm`.
3. Impresión con fondos incluidos:
   - **Chromium / Playwright** `page.pdf`: `preferCSSPageSize:true`, `printBackground:true` y márgenes `'0'`. **No usar `format:'A4'`.**
   - **WeasyPrint**: además `background:#121212` **dentro** de `@page` (WeasyPrint pinta la hoja desde ahí).
   - **Navegador a mano**: márgenes «Ninguno» + casilla «Gráficos de fondo» activada.
   - **ReportLab**: en cada página, rectángulo de relleno `#121212` a página completa **antes** de dibujar nada más.

### Por qué no `format:'A4'` (corrección del 09-11-2026)

Con `format:'A4'` Chrome crea una hoja de 595,92 × 842,88 pt, pero solo pinta el fondo sobre 595,5 × 842,25 pt y lo desplaza 0,75 pt hacia abajo. Queda una **franja sin pintar de unos 0,4–0,75 pt (≈1 px a 100 ppp) en el borde superior y en el derecho**, que los visores muestran en blanco. Con `@page{size:210mm 297mm;margin:0}` y `preferCSSPageSize:true` la hoja (594,96 × 841,92 pt) coincide con el área pintada: 0 píxeles blancos en los bordes, comprobado a 72, 100, 150 y 300 ppp.

## CSS canónico

```css
@page{size:210mm 297mm;margin:0}
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
@page{size:210mm 297mm;margin:0;background:#121212}
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
  preferCSSPageSize: true, // toma el tamaño de @page{size:210mm 297mm}; NO usar format:'A4'
  printBackground: true,
  margin: { top: '0', bottom: '0', left: '0', right: '0' },
})
await browser.close()
```

Flujo habitual: Markdown → HTML (p. ej. `marked`) con el CSS de arriba → `page.pdf` con las tres reglas obligatorias.

## Equivalencias

| Herramienta | Qué no olvidar |
|---|---|
| Playwright / Chromium | `@page{size:210mm 297mm;margin:0}` + `preferCSSPageSize:true` + `printBackground:true` + márgenes `'0'`; blasón en `thead` repetido |
| WeasyPrint | `background:#121212` también dentro de `@page` |
| Impresión manual del navegador | Márgenes «Ninguno» + «Gráficos de fondo» |
| ReportLab | `canvas.setFillColor(HexColor('#121212'))` y `canvas.rect(0,0,*A4,fill=1,stroke=0)` antes de dibujar |

## Verificación antes de entregar

1. Renderizar **todas** las páginas a PNG a **varias resoluciones**: 72, 100, 150 y 300 ppp (`pdftoppm -r N -png`). Una franja de menos de 1 pt solo aparece a algunas resoluciones.
2. Leer los **bordes completos** de cada página: primera y última fila, primera y última columna, no solo las cuatro esquinas.
3. **Ningún píxel de los bordes puede ser `#FFFFFF`** en ninguna página ni resolución. Las esquinas deben ser `#121212`.
4. Comprobar el blasón en **cada página**: la zona superior izquierda debe ser igual en todas, y la imagen incrustada (`pdfimages -png`) igual al PNG oficial en píxeles visibles y canal alfa.

```python
import subprocess, glob, numpy as np
from PIL import Image
for r in (72, 100, 150, 300):
    subprocess.run(['pdftoppm', '-r', str(r), '-png', 'INFORME.pdf', f'/tmp/v/r{r}'])
blancos = 0
for f in glob.glob('/tmp/v/*.png'):
    a = np.array(Image.open(f).convert('RGB')); m = (a == 255).all(2)
    blancos += int(m[0].sum() + m[-1].sum() + m[:, 0].sum() + m[:, -1].sum())
assert blancos == 0, f'{blancos} píxeles blancos en los bordes'
```

Si aparece blanco, las causas habituales son: `format:'A4'` en lugar de `@page{size:210mm 297mm}` + `preferCSSPageSize:true` (franja de 1 px arriba y a la derecha), falta `printBackground`, hay margen en `@page` o en `page.pdf`, o WeasyPrint no lleva el fondo dentro de `@page`.

## Prohibiciones

- Fondo blanco o claro en cualquier página que William deba leer.
- Retocar el blasón oficial.
- Entregar un PDF sin la verificación de píxeles de borde cuando el nodo genera el PDF.
