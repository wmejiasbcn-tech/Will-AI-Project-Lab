# Aula de Aprendizaje Guiado por IA

**Proyecto aplicativo del ecosistema WAIPL**, vinculado al Laboratorio **I+D+I+e+A** en sus dimensiones de **e-Learning** e **Inteligencia Artificial**. Se concibe como proyecto embrionario y precursor del futuro **Campus IA de WAIPL**, manteniendo autonomía funcional y documental.

Este directorio contiene únicamente documentación institucional. **El código fuente y la documentación técnica de desarrollo no están en este repositorio.**

## Identidad y denominación

- **Nombre oficial del proyecto:** Aula de Aprendizaje Guiado por IA.
- **Texto que todavía aparece en la entrada de la aplicación:** Aula de Aprendizaje.
- La armonización del nombre en la plataforma queda pendiente; este README establece la denominación institucional, pero no afirma que la interfaz ya se haya renombrado.

## Qué es

Un entorno digital de aprendizaje guiado, desarrollado inicialmente para organizar un itinerario formativo en español sobre el **Hugging Face Agents Course**, comenzando por fundamentos de Python.

La primera aplicación reúne planificación formativa, sesiones, contenidos, seguimiento, comprobaciones y registro del progreso. Su uso inicial es personal y sirve como experiencia aplicada para investigar y mejorar metodologías de aprendizaje digital.

### Capacidad actual y orientación de IA

La denominación expresa la dirección estratégica del proyecto. **La versión actualmente verificada mantiene el tutor en «modo guiado fijo, sin IA» y no tiene ningún proveedor de IA conectado.** Por tanto, no se atribuye a la aplicación una tutorización generativa ni una capacidad de IA que todavía no está implementada.

La futura incorporación de capacidades de IA requerirá investigación, diseño, pruebas, evaluación, autorización expresa y documentación independiente.

## Vinculación con I+D+I+e+A

El proyecto se vincula al corpus propio del Laboratorio I+D+I+e+A:

- **e — e-Learning:** educación, formación, transferencia de conocimiento y aprendizaje mediante entornos y metodologías digitales.
- **A — Inteligencia Artificial:** estudio de agentes, tutorización asistida, personalización, evaluación y sistemas basados en IA.

La definición vigente del laboratorio es **Investigación, Desarrollo, Innovación, e-Learning e Inteligencia Artificial**, conforme a su [Acta Fundacional canonizada](https://github.com/wmejiasbcn-tech/I-D-I-e-A/blob/main/00_GOBERNANZA/ACTA_FUNDACIONAL_IDIEA_WAIPL-2026-09-11_v01_APPROVED.md).

La relación es de adscripción temática, investigación aplicada y posible transferencia de conocimiento. El Aula conserva su autonomía como proyecto aplicativo. Sus datos personales de estudio no se incorporan al corpus de I+D+I+e+A.

La existencia de esta relación no transfiere automáticamente resultados, prototipos ni capacidades al núcleo canónico de WAIPL.

## Proyección: proyecto precursor del Campus IA

El Aula se identifica como **proyecto embrionario y experiencia piloto precursora del futuro Campus IA de WAIPL**. Permite disponer de una primera experiencia concreta sobre la que investigar, diseñar y evaluar aspectos de una futura plataforma formativa más amplia.

Como líneas potenciales de evolución e investigación —no como capacidades ya existentes— se contemplan:

- itinerarios formativos adaptativos y personalizados;
- tutorización y acompañamiento mediante IA, con supervisión humana;
- organización y recuperación contextual de materiales de aprendizaje;
- evaluación de competencias y evidencias de aprendizaje;
- seguimiento del progreso y recomendaciones pedagógicas;
- experiencias formativas sobre agentes, sistemas multiagente y otras tecnologías de IA;
- transferencia de métodos y componentes validados hacia el futuro Campus IA.

El Aula **no es el Campus IA**, no constituye por sí sola su arquitectura ni presupone que el diseño futuro esté aprobado. Su condición de precursor identifica una línea de evolución y aprendizaje del ecosistema.

## Alcance funcional de la primera versión

- Itinerario de aprendizaje de 20 semanas.
- Organización de sesiones y bloques diarios de estudio.
- Recursos y referencias formativas en español.
- Comprobación semanal y revisión del progreso.
- Registro de actividades y seguimiento.
- Tutor de funcionamiento guiado determinista, sin proveedor de IA conectado.

Los contenidos, calendarios, hitos y datos personales de progreso pertenecen al entorno de la aplicación. Este README no reproduce registros personales ni datos de acceso.

## Plataforma y arquitectura técnica conocida

- Plataforma de construcción y alojamiento actual: Lovable.
- Aplicación desarrollada con TanStack Start, React y TypeScript.
- Supabase para PostgreSQL y autenticación.
- Drizzle para esquema y migraciones.
- Vitest para pruebas automatizadas.

La documentación técnica detallada, el código fuente, las decisiones de arquitectura, los procedimientos de desarrollo y el expediente de evolución se custodiarán en un **repositorio propio privado**. Ese repositorio ya está creado (16-11-2026) y es privado.

Las credenciales, claves, tokens y otros secretos operativos no se almacenarán en archivos versionados, tampoco en un repositorio privado. Se custodiarán mediante mecanismos seguros de secretos y variables de entorno, con permisos restringidos.

## Estado y trazabilidad

**Estado documentado a 16-11-2026:**

- Proyecto construido en Lovable y disponible en [Aula de Aprendizaje](https://aula-progreso-guiado.lovable.app/). El acceso a la aplicación requiere autenticación.
- Último cambio funcional verificado: **Bloque 1** (16-11-2026).
- Las comprobaciones registradas para el Bloque 1 incluyeron 103 pruebas Vitest superadas, lint sin errores y comprobación de tipos sin errores.
- La consulta de integridad del Bloque 1 confirmó 120 sesiones: 100 de estudio y 20 revisiones semanales. No se reproducen aquí sus datos individuales.
- **Bloque 1-bis:** pendiente de ejecución. No se considera implementado ni verificado.
- **Prioridades B y C:** no iniciadas.

### Hitos principales

| Fecha | Hito |
|---|---|
| 15-11-2026 | Creación e implementación inicial del Aula en Lovable. |
| 15-11-2026 | Aprobación y aplicación del plan del Aula unificada, calendario de 20 semanas y comprobación semanal. |
| 16-11-2026 | Prioridad A: bienvenida, tarea diaria de la primera semana y detalle de semana actual. |
| 16-11-2026 | Bloque 1: ajustes de bienvenida, comprobación, textos de botones, gráfico y navegación accesible. |

## Clasificación dentro de WAIPL

| Campo | Clasificación |
|---|---|
| Ecosistema | WAIPL |
| Laboratorio vinculado | I+D+I+e+A |
| Dimensiones | e-Learning e Inteligencia Artificial |
| Tipo | Proyecto aplicativo autónomo |
| Ámbito | Aprendizaje personal, educación digital y formación en IA |
| Proyección | Proyecto embrionario precursor del futuro Campus IA |
| Plataforma actual | Lovable |
| Repositorio de código propio | Privado y creado (16-11-2026) |
| Registro institucional | `05_PROYECTOS/AULA_APRENDIZAJE_GUIADO_POR_IA/` |

## Gobernanza y límites

- **William:** autoridad de decisión y autorización del proyecto.
- **Carla:** coordinación, construcción y documentación dentro del alcance autorizado.
- **SENTINEL:** verificación de entregas y contraste de evidencias.
- Coste objetivo: **0 €**. No se compran créditos ni se amplían planes sin autorización expresa.
- No se conecta un proveedor de IA ni se habilitan capacidades de IA sin autorización expresa.
- No se publican nuevas versiones ni se alteran permisos, audiencia o accesos sin autorización.
- Los datos personales de aprendizaje se mantienen en el entorno correspondiente y no se trasladan al corpus del laboratorio.
- Los cambios y resultados se documentan distinguiendo lo propuesto, implementado, probado, validado y autorizado.

## Dónde reside cada parte

- **Registro institucional:** este directorio del repositorio madre `Will-AI-Project-Lab`.
- **Investigación y relación metodológica:** corpus del Laboratorio I+D+I+e+A, sin incorporación automática de datos personales.
- **Aplicación en ejecución:** proyecto Lovable.
- **Código fuente y expediente técnico-comercial:** repositorio GitHub propio y privado, creado el 16-11-2026.

Este README es una ficha institucional de proyecto; no sustituye al código, al expediente técnico ni a la documentación operativa privada.
