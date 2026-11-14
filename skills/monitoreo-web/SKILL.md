---
name: monitoreo-web
description: Comprueba páginas públicas —si responden, cuánto tardan, si cambiaron y cuántos días le quedan al candado— y deja un informe de fondo oscuro. Usar para la vigilancia de waipl.dev y de cualquier dirección que William añada.
---

# Monitoreo web

Monitorear es mirar una página desde fuera, sin entrar en ella, y anotar si está viva. El candado es el certificado que cifra la visita: si caduca, el navegador avisa de que el sitio no es seguro. La detección de cambios compara esta mirada con la anterior y dice si el contenido o el estado se movieron.

## Cuándo usarla

Cuando haya que saber si una dirección pública responde, si tardó de más, si cambió y si el candado sigue vigente. No sirve para entrar en cuentas, ni para medir lo que ocurre dentro de un panel privado.

## Umbrales de tardanza

La tardanza se mide en milisegundos: mil milisegundos son un segundo.

| Umbral | Valor | Qué hace |
|---|---|---|
| Aviso | 800 ms | Marca la fila. La vigilancia no falla solo por esto. |
| Corte | 2000 ms | Marca la fila y la vigilancia falla. |

Están en `umbrales.txt`. Se cambian ahí, o en la llamada con `--aviso` y `--corte`. El corte no puede ser menor que el aviso.

## Reglas

1. Solo direcciones públicas. Una por línea en `objetivos.txt`. Lo que empieza por `#` no se mira.
2. De cada una se anota: el estado (200 es respuesta normal), los milisegundos, los días de candado y el cambio.
3. La primera mirada dice «primera mirada». La siguiente dice «igual», «cambió el contenido» o «estado A → B». Un reloj o un contador no cuenta como cambio. Un cambio de palabras, sí.
4. La referencia queda en `estado.json`, al lado del script. No se deposita en el repositorio: es de la máquina que vigila, no del canon.
5. Si el candado tiene menos de 14 días, se marca. El número se cambia con `--dias`.
6. El informe lleva fondo `#121212`. Lo dice la skill `fondo-oscuro-canonico`.
7. Si una dirección no responde, el candado está corto o se pasa el corte de tardanza, el script termina con error. Un cambio de contenido se dice; no se disfraza de fallo.
8. Sin secretos en el repositorio público.

## Cómo correrla

```bash
python3 vigilar.py --salida informe.html
python3 vigilar.py --aviso 500 --corte 1500
```

La lista de partida es `objetivos.txt`: `https://waipl.dev` y `https://graph.waipl.dev`. Para añadir otra, una línea nueva.

## Comprobación

- El HTML abre con fondo `#121212` y tiene columna Cambio.
- La segunda pasada, sin tocar la página, dice «igual».
- Si se altera la huella guardada, la siguiente pasada dice «cambió el contenido».
- Una tardanza de 800 ms o más se marca. Una de 2000 ms o más hace fallar la vigilancia.
- El script no pide contraseña.
