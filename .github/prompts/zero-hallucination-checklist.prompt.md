---
mode: agent
description: "Ejecuta una comprobación previa a la entrega, rápida y basada en evidencia, para cualquier respuesta, plan o documento usando el flujo de trabajo zero-hallucination del repositorio."
---

# Lista de comprobación Zero Hallucination

Usa la skill del repositorio en [.github/skills/zero-hallucination/SKILL.md](../skills/zero-hallucination/SKILL.md) como el método rector de verificación.

## Objetivo

Realizar una puerta de seguridad previa a la entrega, rápida y conservadora.

## Lista de comprobación

- [ ] ¿Cuál es la superficie exacta de la afirmación?
- [ ] ¿Qué afirmaciones están directamente soportadas por evidencia en el repositorio o por una fuente externa inspeccionada?
- [ ] ¿Qué afirmaciones son supuestos, hipótesis o inferencias en lugar de hechos verificados?
- [ ] ¿Qué afirmaciones están bloqueadas porque falta la evidencia necesaria?
- [ ] ¿Cuál es la puntuación de confianza entre 0.0 y 1.0?
- [ ] ¿Está la confianza por encima del umbral por defecto de entrega (0.60)?
- [ ] Si la salida es de alto riesgo, ¿la confianza está en 0.75 o superior?
- [ ] ¿Se ha trazado cada afirmación de alto impacto a evidencia o se ha etiquetado explícitamente como no soportada?
- [ ] Si la confianza es baja, ¿se redujo, bloqueó o corrigió el contenido antes de la entrega?

## Forma de respuesta requerida

Devuelve solo:

1. Objetivo
2. Fuente de la verdad
3. Hallazgos verificados
4. Hallazgos no soportados / supuestos
5. Puntuación de confianza
6. Acción requerida antes de la entrega final

## Reglas estrictas

- No inventar hechos.
- Separar las afirmaciones verificadas de los supuestos y elementos bloqueados.
- Si falta evidencia, no presentar la afirmación como verdad establecida.
- Usar el umbral WAIPL por defecto de 0.60 para entrega segura.
- Para afirmaciones técnicas o arquitectónicas de alto riesgo, exigir 0.75+ antes de permitir la entrega.
