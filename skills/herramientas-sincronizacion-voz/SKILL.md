---
name: herramientas-sincronizacion-voz
description: "Herramientas y checklist de sincronización de voz: medición de duración, verificación de uniones, control de voz sintética y registro de limitaciones. Úsala ante herramientas de sincronización, checklist de audio, revisar uniones o auditar continuidad de voz en vídeo."
type: workflow
lifecycle: active
---

# Herramientas de Sincronización de Voz — Checklist operativo

Skill de herramientas prácticas y checklist para sincronización de voz. Complementa `sincronizacion-voz` e `interpolacion-voz`.

## Cuándo activar

- Revisión post-edición de vídeo con fragmentos modificados.
- Necesidad de checklist de continuidad acústica.
- Auditoría de duración y uniones.

## Checklist

| Ítem | Verificación | Estado posible |
|------|--------------|----------------|
| Duración original vs. actual | Medir archivo renderizado (no solo marca de transcripción) | HECHO / PENDIENTE |
| Punto de corte | En silencio o respiración | HECHO / PENDIENTE |
| Voz del fragmento | Humana / sintética predeterminada / interpolada | Documentado |
| Continuidad de volumen | RMS comparable | HECHO / PENDIENTE |
| Continuidad de timbre | Sin salto brusco | NO ACREDITADO hasta reproducción |
| Frase silenciada | Ausente en texto y no recuperable en timeline | NO ACREDITADO hasta inspección de composición |
| Reproducción de uniones | Escuchada | NO REALIZADA / HECHO |

## Coherencia con dictámenes de Carla

- La marca temporal de la transcripción (ej. 7:30) no certifica la duración del vídeo renderizado.
- Silenciar una frase no equivale a eliminarla físicamente del proyecto.
- No declarar validación final del vídeo sin reproducción completa.

## Output esperado

- Checklist rellenado con estados.
- Lista de puntos PENDIENTE / NO ACREDITADO.
- Recomendación: publicar / revisar / rehacer.
