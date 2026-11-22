---
name: sincronizacion-voz
description: "Técnicas de sincronización de voz, alineación labial, continuidad acústica y control de duración en edición de vídeo y locución. Úsala ante sincronizar voz, lip-sync, continuidad de audio, fragmentos con voz sintética, duración del vídeo o revisión acústica."
type: workflow
lifecycle: active
---

# Sincronización de Voz — Continuidad y control

Skill para técnicas de alineación de voz, control de duración y verificación acústica en edición de vídeo, especialmente cuando se insertan fragmentos con voz sintética (Descript, Voice Creator, etc.).

Complementa `voice-creator-waipl`. No sustituye la guía de Nova.

## Cuándo activar

- Inserción de fragmentos con voz sintética en un vídeo existente.
- Problemas de continuidad de voz o labial.
- Desviación de duración tras edición.
- Revisión acústica de segmentos editados.

## Técnicas principales

1. **Alineación temporal**  
   Mantén el punto de corte en silencio o en respiración. Evita cortes a mitad de palabra.

2. **Continuidad de timbre**  
   Si el fragmento es sintético, documenta la diferencia y, si es posible, aplica normalización de volumen y EQ ligero para acercarlo al original.

3. **Control de duración**  
   Mide duración original vs. final. Si aumenta >10 s, valora acortar pausas o reformular frases más cortas.

4. **Verificación acústica**  
   Reproduce los puntos de unión. No certifiques continuidad sin reproducción.

5. **Marcadores de revisión**  
   Anota timestamps de fragmentos modificados para revisión posterior.

## Flujo recomendado

1. Identifica fragmentos editados y su origen (humano / sintético).
2. Mide duración antes y después.
3. Reproduce uniones.
4. Documenta limitaciones (voz predeterminada, silencio residual, etc.).
5. Entrega informe corto: HECHO / PENDIENTE por segmento.

## Output esperado

- Tabla de segmentos editados con timestamp, tipo de voz y estado.
- Duración original vs. actual.
- Lista de uniones que requieren revisión acústica.
- Recomendación: publicar / revisar / rehacer fragmento.
