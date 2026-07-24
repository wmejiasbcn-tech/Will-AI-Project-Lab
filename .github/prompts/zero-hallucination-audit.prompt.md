---
mode: agent
description: "Audita un texto, plan o documento para identificar afirmaciones no soportadas y devolver hallazgos basados en evidencia según la skill zero-hallucination del repositorio."
---

# Auditoría Zero Hallucination

Usa la skill del repositorio en [.github/skills/zero-hallucination/SKILL.md](../skills/zero-hallucination/SKILL.md) como método rector de verificación.

## Objetivo

Verificar exhaustivamente si las afirmaciones en el texto están respaldadas por evidencia disponible (repositorio, documentos de trabajo, referencias externas inspeccionadas).

## Instrucciones

- Lee el texto o el fragmento suministrado.
- Para cada afirmación importante, busca y cita la evidencia que la respalda (ruta de archivo del repositorio, cita de la fuente externa con URL o indicación clara de dónde se inspeccionó).
- Si no encuentras evidencia, clasifica la afirmación como "No soportada" o "Hipótesis" y no la presentes como hecho.
- Calcula una puntuación de confianza global entre 0.0 y 1.0 para la respuesta completa, usando 0.60 como umbral mínimo de entrega y 0.75+ para afirmaciones de alto riesgo.

## Forma de respuesta requerida

Devuelve únicamente el siguiente bloque con esas secciones, en castellano:

1. Objetivo: (una línea)
2. Fuente de la verdad: (lista de archivos/URLs inspeccionadas)
3. Hallazgos verificados: (lista numerada con afirmación + evidencia enlazada)
4. Hallazgos no soportados / supuestos: (lista numerada con afirmación + por qué falta evidencia)
5. Puntuación de confianza: (0.0–1.0)
6. Acción requerida antes de la entrega final: (acciones concretas: aportar fuente / corregir / bloquear)

## Reglas estrictas

- No inventes hechos ni asumas evidencia inexistente.
- Separa claramente las afirmaciones verificadas de las no verificadas.
- Para cada afirmación verificada, proporciona la referencia exacta (ruta de archivo o URL con contexto).
- Si una afirmación es de alto impacto y la confianza < 0.75, marcarla como bloqueada hasta aportar evidencia.

## Comportamiento esperado

- Fundar las afirmaciones en archivos del repositorio, referencias directas del usuario o fuentes externas inspeccionadas.
- Separar la evidencia verificada de la inferencia.
- Si la evidencia está incompleta, reducir el alcance o detenerse y solicitar la fuente faltante.
- Si una respuesta anterior fue demasiado confiada, corregirla identificando la afirmación exacta sin soporte y reemplazándola por una versión verificada o condicional.
