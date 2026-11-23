---
name: agotamiento-vias-revision
description: "Obliga a agotar todas las vías posibles e improbables antes de declarar BLOQUEADO o parar una revisión con el Revisor Arquitectónico. Usar siempre que se aplique el revisor, se declare falta de acceso, se cierre una revisión como PARCIAL o BLOQUEADO, o se vaya a preguntar al soberano por una solución. No se termina ninguna revisión sin haber agotado las vías."
type: workflow
lifecycle: active
---

# Agotamiento de vías — condición permanente de cierre

Orden soberana de William Mejías Navarro, 23 de noviembre de 2026.

No se termina una revisión con el Revisor Arquitectónico si no se han agotado todas y cada una de las vías posibles e improbables para obtener la información. Solo después de agotarlas se para y se explica la situación para que el soberano busque una solución.

## Relación soberana con el Revisor

El Revisor Arquitectónico y de Procesos v1.2.0 y esta skill son una sola unidad. La una sin la otra es inaceptable. Ambas se aplican siempre juntas, sin excepción. El criterio de cierre del Revisor no se cumple si queda una vía no intentada según esta skill.

## Cuándo activar

- Al aplicar el Revisor Arquitectónico (cualquier versión).
- Al declarar una fuente BLOQUEADA por falta de acceso.
- Al cerrar una revisión como PARCIAL o BLOQUEADO.
- Antes de preguntar al soberano por una solución de acceso.

## Regla

1. Identifica la fuente que no se ha podido inspeccionar.
2. Enumera y ejecuta todas las vías de acceso disponibles en la sesión: conectores, GitHub, browse, browser, bots, APIs públicas, caché, copias locales, ramas, commits, metadatos, búsqueda en repositorio madre, búsqueda en issues, búsqueda en conversaciones previas.
3. Incluye vías improbables como subdominios, endpoints de preview, dumps, logs públicos, webhooks, exportaciones y copias de seguridad mencionadas en commits, issues o comentarios. **La exploración y búsqueda de estas vías es obligatoria, pero cualquier acceso o intento de ejecución queda limitado a métodos autorizados, seguros y de solo lectura cuando proceda. No se deben activar webhooks ni ejecutar procesos que puedan causar efectos secundarios, acceder a dumps con datos sensibles, eludir controles de acceso ni realizar acciones destructivas. Si una vía no es segura o no está autorizada, documenta su descubrimiento y la limitación; busca alternativas seguras equivalentes.**
4. Registra cada intento: vía, resultado, motivo de fallo o restricción de seguridad/autorización.
5. Solo cuando la lista de intentos esté completa y todas las vías aplicables, seguras y autorizadas hayan fallado, clasifica como BLOQUEADO y para. Explica qué se intentó y qué queda fuera de alcance. Entonces pregunta al soberano.

## Prohibido

- Declarar BLOQUEADO o PARCIAL por falta de acceso sin haber ejecutado la lista de vías seguras y autorizadas.
- Usar «no reconsultado por mí», «pendiente de verificación» o equivalentes como cierre.
- Preguntar al soberano antes de agotar las vías.
- Eludir controles de acceso, provocar efectos secundarios no autorizados o acceder/ejecutar recursos sensibles o destructivos para cumplir el agotamiento de vías.

## Salida obligatoria cuando se para

```
VÍAS AGOTADAS
- [vía 1]: resultado
- [vía 2]: resultado
...
BLOQUEADO: [fuente]. Causa: [motivo exacto].
Pregunta al soberano: [qué acceso o dato haría posible continuar].
```
