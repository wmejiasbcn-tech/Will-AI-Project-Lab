---
name: herramientas-diseno
description: "Herramientas y flujos de diseño para UI, consistencia visual, dark mode, jerarquía y prompts de imagen. Úsala ante diseño de interfaz, dark mode, estilo visual, componentes del Aula, prompt de imagen, o mejorar la apariencia de una pantalla."
type: workflow
lifecycle: active
---

# Herramientas de Diseño — Consistencia y claridad visual

Skill para decisiones de diseño de interfaz, especialmente en el contexto del Aula de Aprendizaje Guiado por IA y materiales que Will debe leer. Complementa la skill `diagram-design` (diagramas editoriales).

## Principios canónicos

- **Fondo oscuro obligatorio** para cualquier material que Will lea (ver skill `fondo-oscuro-canonico`): usar `#121212`.
- Preferir claridad sobre decoración.
- Máximo 1-2 colores de acento por pantalla.
- Jerarquía tipográfica clara (título → subtítulo → cuerpo).
- Espaciado generoso; evitar densidad excesiva.

## Flujo de diseño de pantalla

1. **Definir objetivo de la pantalla** (qué debe lograr el usuario en 5 segundos).
2. **Establecer jerarquía** (qué es lo más importante).
3. **Aplicar tokens** (ver `references/tokens-aula.md` si existe; en su defecto usar la tabla inferior).
4. **Verificar contraste y dark mode**.
5. **Entregar especificación** lista para implementar (valores exactos).

## Tokens base recomendados (Aula / dark)

| Rol | Valor sugerido | Uso |
|-----|----------------|-----|
| Fondo (materiales para Will) | `#121212` | Fondo principal obligatorio según fondo-oscuro-canonico |
| Fondo (interfaces Aula, alternativa) | `#0f172a` | Solo si no es un documento que Will deba leer directamente |
| Superficie | `#1e293b` | Cards, paneles |
| Texto primario | `#f1f5f9` | Títulos y cuerpo |
| Texto secundario | `#94a3b8` | Metadatos, hints |
| Acento | `#2563eb` | Botones primarios, links |
| Éxito | `#10b981` | Confirmaciones |
| Error | `#ef4444` | Errores |

## Cuándo usar editor visual vs. prompt

| Cambio | Herramienta | Créditos |
|--------|-------------|----------|
| Color, texto, spacing, orden | Editor visual de Lovable | 0 |
| Nuevo componente o lógica | Prompt optimizado (skill `optimizacion-prompts`) | Variable |
| Diagrama de arquitectura/flujo | Skill `diagram-design` | 0 |

## Output esperado

Al diseñar o revisar una pantalla entrega:
1. Tokens de color y tipografía a usar.
2. Jerarquía visual (qué destaca primero).
3. Especificación de cambios (lista concreta).
4. Si aplica, prompt optimizado para Lovable o instrucciones para el editor visual.
