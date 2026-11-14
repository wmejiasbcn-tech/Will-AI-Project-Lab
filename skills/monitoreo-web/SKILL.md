---
name: monitoreo-web
description: Comprueba páginas públicas —si responden, cuánto tardan y cuántos días le quedan al candado— y deja un informe de fondo oscuro. Usar para la vigilancia de waipl.dev y de cualquier dirección que William añada.
---

# Monitoreo web

Monitorear es mirar una página desde fuera, sin entrar en ella, y anotar si está viva. El candado es el certificado que cifra la visita: si caduca, el navegador avisa de que el sitio no es seguro.

## Cuándo usarla

Cuando haya que saber si una dirección pública responde y si el candado sigue vigente. No sirve para entrar en cuentas, ni para medir lo que ocurre dentro de un panel privado.

## Reglas

1. Solo direcciones públicas. Una por línea en `objetivos.txt`. Lo que empieza por `#` no se mira.
2. De cada una se anota: el estado (200 es respuesta normal), los milisegundos que tardó y los días que le quedan al candado.
3. Si el candado tiene menos de 14 días, se marca. El número se cambia con `--dias`.
4. El informe lleva fondo `#121212`. Lo dice la skill `fondo-oscuro-canonico`.
5. Si una dirección falla, el informe lo dice y el script termina con error. No se escribe que todo está bien.
6. Sin secretos en el repositorio público.

## Cómo correrla

```bash
python3 vigilar.py --salida informe.html
python3 vigilar.py --url https://waipl.dev --dias 30
```

La lista de partida es `objetivos.txt`: `https://waipl.dev` y `https://graph.waipl.dev`. Para añadir otra, una línea nueva. No hace falta tocar el script.

## Comprobación

- El HTML abre con fondo `#121212`.
- Una dirección apagada no sale como correcta.
- El script no pide contraseña.
