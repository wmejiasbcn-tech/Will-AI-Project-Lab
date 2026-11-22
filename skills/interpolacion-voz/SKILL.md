---
name: interpolacion-voz
description: "Técnicas de interpolación de voz para suavizar transiciones entre locución original y fragmentos sintéticos, control de crossfade y normalización de timbre. Úsala ante interpolar voz, suavizar unión, crossfade de audio, transición voz sintética o continuidad de timbre."
type: workflow
lifecycle: active
---

# Interpolación de Voz — Transiciones suaves

Skill de técnicas de interpolación para unir voz original y fragmentos sintéticos sin cortes bruscos. Complementa `sincronizacion-voz` y `voice-creator-waipl`.

## Cuándo activar

- Uniones entre voz humana y voz sintética (Descript, Voice Creator, etc.).
- Necesidad de crossfade o normalización de timbre.
- Revisión de continuidad acústica en puntos de edición.

## Técnicas

1. **Crossfade corto**  
   Aplica un crossfade de 40-80 ms en el punto de unión. Evita valores >150 ms que generen solapamiento audible.

2. **Normalización de volumen**  
   Iguala el RMS del fragmento sintético al del segmento original adyacente antes de unir.

3. **EQ ligero**  
   Si el timbre sintético es más brillante, atenúa levemente 3-6 kHz para acercarlo. Documenta el ajuste.

4. **Corte en silencio**  
   Prefiere el punto de corte en una pausa o respiración. La interpolación no sustituye un mal punto de corte.

5. **Marcador de revisión**  
   Anota el timestamp y el tipo de interpolación aplicada.

## Coherencia con dictámenes de Carla

- No certifiques continuidad sin reproducción.
- Distingue “ausencia en transcripción” de “eliminación física en composición”.
- Registra si el fragmento quedó con voz sintética predeterminada.

## Output esperado

- Timestamp de la unión.
- Técnica aplicada (crossfade / normalización / EQ).
- Estado: HECHO (aplicado) / PENDIENTE (requiere reproducción).
- Limitación residual documentada.
