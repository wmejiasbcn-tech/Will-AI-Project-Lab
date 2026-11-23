# Skills propias WAIPL

Carpeta pública de skills del ecosistema Will-AI Project Lab (WAIPL).

## Convención

- Una subcarpeta por skill.
- Cada skill contiene un `SKILL.md` con frontmatter (`name`, `description`) y el cuerpo en español.
- Sin secretos, tokens ni datos sensibles (este repositorio es público).
- El `name` coincide con el nombre de la carpeta: minúsculas y guiones.
- El índice de abajo enlaza cada ficha que exista. `type`, `lifecycle` y `version` son opcionales: unas fichas los traen y otras no.
- La comprobación automática está en `.github/workflows/validar-skills.yml`. Corre al cambiar esta carpeta. No publica el sitio.

## Índice

| Skill | Estado | Descripción breve |
|---|---|---|
| [fondo-oscuro-canonico](fondo-oscuro-canonico/SKILL.md) | Activa | Orden permanente: documentos para William con fondo `#121212` hasta el borde; método Chromium/WeasyPrint. |
| [alertas-automaticas](alertas-automaticas/SKILL.md) | Activa | Arma avisos a hora fija, con 30 y 10 minutos antes, y el texto para el calendario y para Sentinel. |
| [monitoreo-web](monitoreo-web/SKILL.md) | Activa | Mira páginas públicas: respuesta, tiempo, cambios y días de candado; aplica umbrales configurables. |
| [escritura-creativa](escritura-creativa/SKILL.md) | Canonizada | Didáctica y educativa de técnicas de escritura creativa para Aether: estructura, voz, inmersión, transmedia y restricción. Canonizada por orden soberana 17-11-2026. |
| [revisor-arquitectonico-procesos](revisor-arquitectonico-procesos/SKILL.md) · [README](revisor-arquitectonico-procesos/README.md) | Incorporada · v1.3.0 | Control transversal con agotamiento obligatorio de vías, PRE-FLIGHT/POST-FLIGHT, inspección recursiva, cobertura, trazabilidad, contraste y contraverificación. [Aplicación web](https://waipl-revisor-arquitectonico-332ulo.v2.appdeploy.ai/). **Integra agotamiento de vías y conserva [agotamiento-vias-revision](agotamiento-vias-revision/SKILL.md) como refuerzo inseparable.** |
| [agotamiento-vias-revision](agotamiento-vias-revision/SKILL.md) | Activa | Obliga a agotar todas las vías posibles e improbables antes de declarar BLOQUEADO o parar una revisión del Revisor. **Refuerzo adicional inseparable del Revisor v1.3.0. El agotamiento de vías ya está integrado en el núcleo del Revisor.** |
| [co-director-waipl](co-director-waipl/SKILL.md) | Canónica | Dirección de vídeo narrativo por fases. Adaptación de Co-Director (Song et al., Google, arXiv:2604.24842, CC BY 4.0). Declarada el 19-11-2026, 17:39 h, Barcelona. No es un nodo. |
| [optimizacion-prompts](optimizacion-prompts/SKILL.md) · [README](optimizacion-prompts/README.md) | Activa | Optimiza prompts para reducir consumo de créditos y mejorar precisión en Lovable y otros agentes. |
| [herramientas-diseno](herramientas-diseno/SKILL.md) · [README](herramientas-diseno/README.md) | Activa | Herramientas y flujos de diseño para UI, consistencia visual, dark mode y jerarquía. |
| [sincronizacion-voz](sincronizacion-voz/SKILL.md) · [README](sincronizacion-voz/README.md) | Activa | Técnicas de sincronización de voz, continuidad acústica y control de duración. |
| [auditoria-codigo](auditoria-codigo/SKILL.md) · [README](auditoria-codigo/README.md) | Activa | Flujos de auditoría de código con separación HECHO/PROPUESTO/PENDIENTE y trazabilidad de estados. |
| [interpolacion-voz](interpolacion-voz/SKILL.md) · [README](interpolacion-voz/README.md) | Activa | Técnicas de interpolación de voz para suavizar uniones humano-sintético. |
| [herramientas-sincronizacion-voz](herramientas-sincronizacion-voz/SKILL.md) · [README](herramientas-sincronizacion-voz/README.md) | Activa | Checklist operativo de sincronización de voz y controles audiovisuales. |
| diagram-design | Pendiente | (contenido aún no depositado aquí) |
| lineas-pr | Pendiente | (contenido aún no depositado aquí) |

## Origen

Orden soberana de William Mejías Navarro, 09-11-2026 (mensaje t993u): crear esta carpeta en el repositorio público principal y depositar la skill de fondo oscuro canónico, dejando sitio para más skills propias.
