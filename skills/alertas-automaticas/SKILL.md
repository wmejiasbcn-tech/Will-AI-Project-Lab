---
name: alertas-automaticas
description: Arma alertas con hora de España, avisos previos y texto listo para el calendario y para Sentinel. Usar cuando William pida un recordatorio, una ventana de trabajo o que algo no se pase de hora.
---

# Alertas automáticas

Una alerta es un aviso que salta solo, a una hora fija, sin que alguien tenga que acordarse. Esta skill arma el paquete. No guarda contraseñas y no entra en cuentas ajenas.

## Cuándo usarla

Cuando haya una hora que no se puede perder: una ventana de una herramienta, un cierre, una revisión. No usarla para inventar avisos que nadie pidió.

## Reglas

1. La zona es `Europe/Madrid` salvo que William diga otra.
2. Si no dice los avisos previos, son dos: 30 minutos antes y 10 minutos antes, y otro a la hora.
3. El texto dice qué hay que hacer en cada aviso. No dice que el trabajo ya está hecho.
4. Tres sitios, y solo los que estén abiertos en esa sesión:
   - El calendario de Google, en la agenda principal, con aviso en el teléfono y por correo.
   - El aviso de esta conversación, que se borra después de sonar para que no se repita.
   - Un aviso a Sentinel, en el repositorio `wmejiasbcn-tech/SENTINEL`, como incidencia nueva. Si la casa pide confirmación, se le da a William el enlace ya relleno. No se dice que salió si no salió.
5. Sin secretos en el repositorio público.

## Cómo armarla

Desde esta carpeta:

```bash
python3 alerta.py \
  --cuando "2026-11-19 14:00" \
  --hasta "2026-11-20 14:00" \
  --titulo "MiniMax H3 — abrir Envato" \
  --enlace "https://elements.envato.com/lp/minimax-h3/" \
  --antes 30,10
```

El script escribe las horas y los dos textos. No llama a Google ni a GitHub. Quien tiene la cuenta pega el texto.

## Comprobación

- Las horas impresas coinciden con `--cuando` menos los minutos de `--antes`.
- El texto de Sentinel empieza por `DE: aether · PARA: sentinel`.
- No hay contraseñas ni tokens en el archivo.
