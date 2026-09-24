# N3 — Voz de Hermes

**Grantor:** Soberano  
**Fecha:** 2026-08-23  
**Implementa:** AutoClaw (runtime)  
**No es:** el N3 de reboot. No es 24/7. No adelanta túnel. No fusiona Aether-Hermes.

## Objetivo

Hermes, cuando hable en audio, suena **hombre, natural, de mesa de trabajo**. Nunca SAPI. Nunca voz de GPS.

**Aether es estilo, no motor.** La voz de Aether en Grok (Helios) no corre en el EliteBook. No pidas `voice_id` de Aether ni de Carla al Soberano. Eso es volver a hacerle de puente.

## Alcance

**Dentro:** motor TTS del runtime Hermes (briefing, dashboard, alertas).
**Fuera:** identidad, Graphify, Qwen, merge, GITHUB_TOKEN, tres tareas, GLOSARIO del repo GitHub (el del MANIFEST no se toca aquí).

## Prohibido (STOP)

- Preguntar al Soberano cuál motor o cuál voice_id
- `pyttsx3` / Windows SAPI / Hortensia / David
- Voz femenina. Hablar como Aether. ElevenLabs sin grant
- Dejar solo un JSON `especificacion_pendiente` y parar

## Motor (ya decidido)

`edge-tts` + `es-ES-AlvaroNeural`. Si no está: `pip install edge-tts` en el venv. Si esa voz no existe: `edge-tts --list-voices` y otra **Male** `es-ES` neural. Nunca `en-US`. Nunca SAPI de fallback.

Archivo: `$HERMES/config/voice.json` (este nombre, no solo `voice_profile.json`):

```json
{
  "engine": "edge-tts",
  "voice": "es-ES-AlvaroNeural",
  "gender": "male",
  "locale": "es-ES",
  "style_ref": "Aether/Helios feel — not identity",
  "status": "implementing"
}
```

## Éxito

MP3/WAV de 15–20 s **generado en el EliteBook** con la frase:

> Soy Hermes. Director operativo del Lab. No soy Aether. El puerto 8787 está en marcha. Te hablo claro, en masculino, sin voz de robot.

Dashboard, si hay botón de voz, usa ese motor. Cero SAPI al hablar.

## Parada

Audio a GPS → STOP. No hay edge-tts → instalar y reintentar, no SAPI. ElevenLabs → STOP y grant.
