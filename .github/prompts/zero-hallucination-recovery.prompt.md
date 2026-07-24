---
mode: agent
description: "Reescribe o corrige contenido que sea demasiado confiado, no soportado o de baja confianza para que solo queden afirmaciones verificadas."
---

# Recuperación Zero Hallucination

Usa la skill del repositorio en [.github/skills/zero-hallucination/SKILL.md](../skills/zero-hallucination/SKILL.md) para corregir una salida previa sin inventar evidencia faltante.

## Objetivo

Tomar una respuesta, documento o propuesta que pueda contener afirmaciones no soportadas y producir una versión más segura.

## Forma de salida requerida

1. Afirmación(es) no soportada(s) identificada(s)
2. Evidencia faltante o brecha de fuente
3. Reescritura conservadora
4. Incertidumbres restantes
5. Paso de verificación recomendado

## Reglas estrictas

- No preservar una afirmación solo porque suene plausible.
- Si falta evidencia, reemplazar la afirmación con una declaración condicional o un bloqueo.
- Separar lo verificado de lo que aún es incierto.
- Mantener la respuesta revisada auditable y trazable.
- No declarar finalización hasta que la afirmación esté fundamentada o marcada explícitamente como bloqueada.

## Comportamiento de recuperación

- Encontrar la afirmación exacta que excede la evidencia disponible.
- Reemplazar la confianza no soportada por un lenguaje respaldado por evidencia.
- Reducir el alcance si la fuente está incompleta.
- Solicitar la referencia faltante cuando la respuesta no pueda hacerse segura sin ella.
