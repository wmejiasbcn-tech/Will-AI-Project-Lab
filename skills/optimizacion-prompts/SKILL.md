---
name: optimizacion-prompts
description: "Optimiza prompts para reducir consumo de créditos y mejorar precisión en Lovable, Claude, Grok y otros agentes. Úsala ante optimizar prompt, reducir créditos, prompt para Lovable, batch de cambios, prompt de construcción, o mejorar instrucciones al agente."
type: workflow
lifecycle: active
---

# Optimización de Prompts — Menos créditos, más precisión

Skill para transformar solicitudes vagas o iterativas en prompts únicos, específicos y de bajo costo. Especialmente útil en Lovable (Build credits) y en cualquier agente que cobre por complejidad o por mensaje.

## Cuándo activar

- Usuario pide optimizar un prompt.
- Se va a enviar un cambio a Lovable con pocos créditos.
- Hay riesgo de bucles de corrección.
- Se necesita agrupar varios cambios en uno solo.

## Flujo principal

1. **Captura la intención**  
   Extrae: qué cambiar, dónde (archivo/componente), estado actual, estado deseado, restricciones.

2. **Decide modo**  
   - Investigación o decisión de enfoque → Plan mode (1 crédito fijo, no cambia código).  
   - Cambio concreto → Build mode con prompt único.

3. **Aplica reglas de optimización** (ver tabla abajo).

4. **Genera el prompt final**  
   Entrega un único bloque listo para copiar, con:
   - Alcance exacto
   - Cambios listados
   - Restricciones explícitas
   - Criterio de éxito

5. **Estima impacto**  
   Indica si es bajo / medio / alto consumo esperado y por qué.

## Reglas de optimización (prioridad alta → baja)

| Regla | Acción | Ahorro típico |
|-------|--------|---------------|
| **Batching** | Agrupa 3+ cambios relacionados en un solo prompt | 60-80% vs. mensajes separados |
| **Especificidad** | Nombra archivo, componente, valores exactos, restricciones | Evita 1-3 correcciones |
| **Plan primero** | Usa Plan mode para aclarar antes de Build | Evita rehacer en Build |
| **Visual free** | Deriva a editor visual cambios de texto/color/spacing | 0 créditos |
| **Try to fix** | Recuerda botón gratuito antes de nuevo prompt | 100% en errores |
| **Stop early** | Si falla, no reintentes igual; reformula o para | Evita bucles |

## Plantilla de prompt optimizado (Lovable Build)

```
[Alcance]
Modifica únicamente [archivo o componente exacto].

[Cambios]
1. [Cambio 1 con valor exacto]
2. [Cambio 2]
3. [Cambio 3]

[Restricciones]
- No modifiques [X]
- Mantén [Y] intacto
- Usa [Z] existente

[Criterio de éxito]
El cambio está completo cuando [resultado verificable].
```

## Anti-patrones a evitar

- Prompts vagos ("mejora el diseño", "arregla el login").
- Múltiples mensajes pequeños consecutivos sobre el mismo elemento.
- Reintentos con el mismo texto tras un error.
- Mezclar cambios visuales simples con lógica compleja en el mismo prompt sin separarlos.

## Notas de costes (orientativas)

- Plan mode: 1 crédito fijo.
- Build mode: variable según complejidad (típicamente 0.5–2+ créditos).
- Editor visual y “Try to fix”: 0 créditos.

## Output esperado

Siempre entrega:
1. Prompt final listo para usar.
2. Breve justificación de por qué es óptimo.
3. Estimación de créditos (bajo/medio/alto).
4. Alternativa gratuita si existe (visual editor, Try to fix).
