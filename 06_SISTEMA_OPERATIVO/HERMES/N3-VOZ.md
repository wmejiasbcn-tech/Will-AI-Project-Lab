# N3 — Voz de Hermes

**Grantor:** Soberano  
**Fecha:** 2026-08-23  
**Implementa:** AutoClaw (runtime)  
**No es:** el N3 de reboot. No es 24/7. No adelanta túnel.

## Objetivo

Hermes, cuando hable en audio, suena **hombre, natural, de mesa de trabajo**. Como se habla con Carla o con Aether. Nunca SAPI. Nunca voz de GPS.

## Alcance

**Dentro:** motor TTS del runtime Hermes (briefing, dashboard, alertas habladas).
**Fuera:** cambiar identidad, Graphify, Qwen, merge del PR, GITHUB_TOKEN, tres tareas.

## Prohibido (STOP)

- `pyttsx3` / Windows SAPI / `Microsoft Hortensia` / `David` / cualquier voz *desktop* de Windows
- Pitch de robot, rate 200, beep al arrancar, «Sistema operativo listo»
- Voz femenina
- Hablar en nombre de Aether
- ElevenLabs u otra API de pago **sin grant** (clave fuera de git si se concede después)

## Motor (este N3, sin grant extra)

`edge-tts`, voz neural **es-ES**, masculina. Primera candidata: `es-ES-AlvaroNeural`. Si no existe en la máquina, listar `edge-tts --list-voices` y elegir otra **Male** `es-ES` neural. No improvisar una voz `en-US`.

Registro hablado: castellano de España, ritmo de conversación (~1.0), sin énfasis teatral. Frases cortas. Cero jerga de bootloader.

Texto escrito de Hermes (logs, Issue, dashboard): el mismo registro. No «afirmativo, unidad lista».

## Éxito

1. Un WAV/MP3 de 15–20 s con la frase de prueba, generado **en el EliteBook**, no un clip de Grok.
2. En el HTML/dashboard, si hay botón de voz, usa ese motor. Cero SAPI en el árbol de procesos al hablar.
3. Config en `$HERMES/config/voice.json`: `{ "engine": "edge-tts", "voice": "es-ES-AlvaroNeural", "gender": "male", "locale": "es-ES" }`. Nada de secretos.

Frase de prueba (literal):

> Soy Hermes. Director operativo del Lab. No soy Aether. El puerto 8787 está en marcha. Te hablo claro, en masculino, sin voz de robot.

## Parada

- Si el primer audio suena a GPS → STOP, no lo dejes cableado.
- Si no hay `edge-tts` → instalarlo en el venv y reintentar. No caer a SAPI.
- Si hace falta ElevenLabs → STOP y grant del Soberano.

## Evidencia

Ruta del archivo de audio + `voice.json` + una línea: proceso que habla (nombre del exe). Sin Issue GitHub si no hay token. El Soberano oye el archivo; no hace de puente de texto.
