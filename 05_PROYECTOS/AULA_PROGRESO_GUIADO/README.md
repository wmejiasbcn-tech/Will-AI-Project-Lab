# Aula Progreso Guiado

Proyecto del ecosistema WAIPL registrado por decisión de William (16-11-2026). Este directorio contiene solo este README: el código del proyecto no está en este repositorio.

## Qué es

Una plataforma personal de aprendizaje, en español, para estudiar el **Hugging Face Agents Course** empezando por Python desde cero. Organiza el plan de estudio, la sesión de cada día, la comprobación semanal y el registro del progreso.

El tutor de la aplicación se presenta como **«modo guiado fijo, sin IA»**: no hay ningún proveedor de IA configurado.

## Para quién

Para William. Es un espacio privado de un solo usuario: para entrar hace falta iniciar sesión con su cuenta.

## Estado actual

A fecha de 16-11-2026, 03:09 (hora de Madrid):

- Proyecto Lovable «Aula Progreso Guiado», creado el 15-11-2026 a las 14:22 (hora de Madrid).
- Último commit: `61b7e2bb04ed40567c350387be59684a62a09a41` (16-11-2026, 03:09, hora de Madrid). Solo añade el plan del siguiente bloque (`.lovable/plan.md`); no cambia código.
- Último cambio funcional: Bloque 1, commit `7ec3721bea1663d409fc2c3cfe40d8bc74f983f4`.
- Publicado en <https://aula-progreso-guiado.lovable.app>. La dirección es pública, pero para entrar hace falta iniciar sesión con la cuenta de William.
- Sesiones cargadas: 120 (100 de estudio y 20 revisiones semanales), ninguna de demostración, todas en estado «planificada».

## Cómo funciona

- **Duración:** 20 semanas, del lunes 16-11-2026 al viernes 02-04-2027.
- **Sesión diaria:** de lunes a viernes, de 16:00 a 16:45 (hora de Madrid), en cuatro bloques:
  1. 5 minutos: recordar lo hecho y situar la tarea del día.
  2. 20 minutos: aprender el contenido del día, en español.
  3. 15 minutos: practicar o hacer la comprobación que toque.
  4. 5 minutos: registrar lo aprendido, la práctica, la dificultad y el siguiente paso.
- **Comprobación semanal:** el viernes de cada semana.
- **Revisión semanal:** el domingo a las 18:00 (hora de Madrid), del 22-11-2026 al 04-04-2027.
- **Primera semana:** el lunes 16-11 es la bienvenida (presentación del curso y del Aula, sin Python). Python empieza el martes 17-11, en Google Colab.
- **Fases del plan:**
  - Semanas 1–4: Python desde cero, solo en Google Colab.
  - Semanas 5–8: unidades 0 y 1; certificado de fundamentos en la semana 8.
  - Semanas 9–14: smolagents, LlamaIndex y LangGraph, dos semanas cada uno.
  - Semanas 15–16: unidad 3, RAG con agentes.
  - Semanas 17–20: unidad 4, proyecto GAIA y certificado de finalización.
- **Hitos:** semanas 4, 8, 14, 16 y 20.

## Arquitectura

- Construido en Lovable.
- TanStack Start (React y TypeScript).
- Supabase (base de datos PostgreSQL e inicio de sesión).
- Drizzle para el esquema y las migraciones (`0000` a `0010`).
- Pruebas automáticas con Vitest.

Este README no incluye claves, direcciones internas ni datos de acceso.

## Qué se ha hecho

Horas en hora de Madrid.

| Fecha | Hora | Hecho | Commit |
|---|---|---|---|
| 15-11-2026 | 14:22 | Creación del proyecto en Lovable. | — |
| 15-11-2026 | 14:45 | Primera versión completa de la aplicación, con reglas en base de datos, pruebas y documentación. | `9a6791f6` |
| 15-11-2026 | 18:13 | William autoriza el plan del Aula unificada (documento `docs/11-plan-aula-unificada.md` del proyecto). | `20d44dd9` |
| 15-11-2026 | 18:23–19:36 | Aplicación del plan: tema oscuro por defecto, tutor «modo guiado fijo, sin IA», contenido y calendario de las 20 semanas (migraciones `0008` y `0009`) y registro de la comprobación semanal (migración `0010`). | `71b2b3bb` a `97f10029` |
| 16-11-2026 | 02:21 | **Prioridad A:** bienvenida dentro del Aula, tarea concreta de cada día de la semana 1 en Inicio y detalle de la semana actual en Itinerario. | `e97726bc` |
| 16-11-2026 | 02:47 | **Bloque 1:** fecha de la comprobación semanal visible, enlaces de práctica ocultos el día de bienvenida, género correcto en los botones «Nuevo/Nueva», nombre completo del itinerario en su gráfico y «Empieza aquí» sin animaciones. | `7ec3721b` |
| 16-11-2026 | 03:09 | Plan del siguiente bloque registrado, sin cambios de código. | `61b7e2bb` |

Resultados registrados en el informe del Bloque 1 (`tests/reports/2026-11-16-bloque1.md` del proyecto):

- Vitest: 11 archivos y 103 pruebas superadas.
- Lint: 0 errores.
- Comprobación de tipos: sin errores.
- Las 120 sesiones siguen intactas antes y después del cambio.

## Gobernanza y límites

- **Roles:** Carla construye y documenta en Lovable. SENTINEL verifica cada entrega y da su dictamen. William decide y autoriza.
- **Coste: 0 €.** Sin pagos, compras, créditos adicionales ni ampliaciones. Si algo pide pago, se para y se avisa a William.
- **Nada se publica** sin el sí expreso de William. Tampoco se cambian audiencia, permisos, accesos ni contraseñas.
- **Sin IA conectada.** Ningún proveedor de IA se activa sin el sí expreso de William.
- **No se borra nada:** lo que sobra se oculta.
- **Nada blanco:** sin superficies blancas ni destellos claros en ninguna pantalla.
- **FREEZE:** este registro es documentación, permitida durante el FREEZE (`FREEZE_STATE.md`).

## Dónde está el código

- En Lovable, proyecto `eb435952-20bd-4104-8ceb-bf38048470f7`.
- A fecha de 16-11-2026 no tiene repositorio propio en GitHub.
