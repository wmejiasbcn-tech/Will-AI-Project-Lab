name: zero-hallucination
user-invocable: true
description: "Usar cuando necesites producir o revisar salidas de IA con un flujo de trabajo 'evidencia-primero' y zero-hallucination. Aplica esta skill a planes, documentos, especificaciones técnicas, afirmaciones y decisiones que deben ser verificables, auditables y seguras de confiar."
---

# Zero Hallucination Verification Skill

## Alcance

Esta es una skill con alcance de workspace para el repositorio WAIPL. Está destinada a usarse cuando una respuesta, plan o documento debe ser fiable antes de su entrega.

## Propósito

Usa este flujo de trabajo para garantizar que el contenido generado esté fundamentado en evidencia real, claramente separado entre hechos verificados y suposiciones, y sea seguro de entregar sin inventar información.

Esta skill está diseñada para el patrón WAIPL de:
- evidencia antes de las afirmaciones
- validación por umbrales
- trazabilidad transparente
- recuperación correctiva cuando la confianza es baja

## Cuándo usarla

Usa esta skill cuando:
- la respuesta debe ser precisa, trazable y no especulativa
- estés redactando planes, documentación técnica, notas de arquitectura o decisiones de proyecto
- necesites validar si una respuesta o documento es fiable
- quieras evitar que afirmaciones no soportadas se presenten como hechos

## Flujo central

### Ramas de decisión

- Si la afirmación está soportada por evidencia directa en el workspace o una fuente externa verificada, márcala como `Verificada`.
- Si la afirmación es plausible pero no tiene origen directo, márcala como `Suposición` o `Hipótesis`.
- Si la afirmación es crítica y falta evidencia, bloquear la entrega y solicitar la fuente faltante.
- Si la evidencia es parcial, reducir el alcance y expresar la afirmación de forma condicional hasta que pueda verificarse.

### 1. Definir la superficie de la afirmación
Identifica exactamente qué debe ser verdadero, prometido o recomendado.

Preguntas útiles:
- ¿Qué pide el usuario que se concluya?
- ¿Qué enunciados son hechos y cuáles interpretaciones?
- ¿Qué evidencia haría confiable cada enunciado?

### 2. Fundar cada afirmación importante en material fuente-de-verdad
Antes de afirmar un hecho, verifícalo contra una de las siguientes fuentes:
- un archivo del repositorio
- un documento fuente en el workspace
- una referencia proporcionada por el usuario
- una fuente externa claramente identificada que se haya obtenido e inspeccionado

Si una afirmación no tiene fuente verificable, márcala como:
- suposición
- hipótesis
- pendiente de verificación

### 3. Separar contenido verificado, incierto y bloqueado
Estructura la salida con etiquetas claras:
- Verificado
- No soportado / Sin evidencia
- Suposición
- Rechazado / Necesita corrección

No mezcles silenciosamente estas categorías.

### 4. Aplicar una puerta de confianza
Para cualquier salida destinada a entregarse de forma autónoma:
- puntúa la confianza entre 0.0 y 1.0
- exige evidencia para cada enunciado de alto impacto
- bloquear o revisar contenido si la confianza está por debajo del umbral acordado

Valores recomendados por defecto:
- umbral para entrega: 0.60
- decisiones de alto riesgo o afirmaciones técnicas: 0.75+

### 5. Si la confianza es baja, detenerse y recuperar
Cuando la evidencia es incompleta:
- no inventar detalles faltantes
- pedir la fuente que falta
- reducir el alcance de la afirmación
- reformular en condicional hasta que exista verificación

### 6. Producir una respuesta final trazable
La respuesta final debe mostrar:
- la base verificada para la conclusión
- las suposiciones que permanezcan
- la puntuación de confianza
- qué se bloqueó y por qué

## Criterios de calidad

Un resultado cumple esta skill cuando se verifica todo lo siguiente:
- cada afirmación factual tiene una fuente o está claramente marcada como no verificada
- no se presenta información no soportada como verdad establecida
- la ambigüedad se preserva en lugar de ocultarse
- la confianza y la evidencia son explícitas
- el flujo de trabajo es auditable posteriormente

## Lista de comprobación de finalización

Usa esta checklist antes de finalizar:
- [ ] ¿Qué afirmaciones están verificadas?
- [ ] ¿Qué afirmaciones son suposiciones?
- [ ] ¿Qué afirmaciones fueron bloqueadas por falta de evidencia?
- [ ] ¿Cuál es la puntuación de confianza?
- [ ] ¿Qué habría que corregir antes de que la salida sea segura de confiar?
- [ ] ¿Cada enunciado de alto impacto tenía una fuente o una etiqueta explícita de sin-evidencia?
- [ ] Si la confianza estuvo por debajo del umbral, ¿se redujo, bloqueó o corrigió la salida?

## Patrón práctico de salida

Al aplicar esta skill, prefiere una forma de respuesta como la siguiente:

1. Objetivo
2. Fuente de la verdad
3. Hallazgos verificados
4. Hallazgos no verificados / suposiciones
5. Puntuación de confianza
6. Acción requerida antes de la entrega final

## Patrón de recuperación

Si una respuesta previa fue incorrecta o demasiado confiada:
1. Identificar la afirmación exacta no soportada
2. Localizar la evidencia faltante
3. Reescribir la afirmación de forma conservadora
4. Registrar la corrección en la memoria de trabajo o en el registro del proyecto
5. Solo entonces reanudar el flujo de trabajo principal

## Evitar los anti-patrones de esta skill

No hacer:
- presentar una inferencia como un hecho
- ocultar la falta de evidencia bajo una redacción confiada
- declarar finalizado sin un paso de verificación
- confiar sólo en la memoria cuando existe un archivo fuente
- tratar “parece razonable” como prueba

## Prompts sugeridos

- “Verifica este plan técnico contra las fuentes del workspace y marca cada afirmación no soportada.”
- “Revisa este documento en busca de alucinaciones y produce una checklist de evidencia con puntuación de confianza.”
- “Reescribe esta respuesta para que solo queden afirmaciones respaldadas por evidencia.”
- “Comprueba si esta propuesta de implementación está fundamentada en el repo e identifica qué debe validarse antes de ejecutarla.”
