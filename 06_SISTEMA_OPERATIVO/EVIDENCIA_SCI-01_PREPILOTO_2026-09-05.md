# EVIDENCIA SCI-01 — GATE PRE-PILOTO

**Fecha de evaluación:** 2026-09-05
**Alcance:** SCI n8n-WAIPL
**Prompt aplicable:** `06_SISTEMA_OPERATIVO/PROMPT_ABSOLUTO_N8N_SCI_PREPILOTO_v2.0.md`
**Matriz:** `06_SISTEMA_OPERATIVO/MATRIZ_CANON_N8N_SCI_v1.0.md`  
**Estado del gate:** `BLOQUEADO — NO AUTORIZAR PILOTO`

## 1. Alcance y límite de la evidencia

Esta evaluación se realizó sobre el contenido disponible en este repositorio. No se
encontró una exportación de workflows n8n, configuración de credenciales, tablas del
Audit Log ni un runtime n8n accesible para ejecutar el SCI. Por tanto, no se
presenta una ejecución hipotética como evidencia.

Conforme al prompt absoluto, la ausencia de evidencia se clasifica como
`PENDIENTE_DE_EVIDENCIA`; no se convierte en `CONFORME` por el mero hecho de que
exista documentación o un workflow descrito en otro documento.

## 2. Registro P01–P15

| Prueba | Resultado esperado | Resultado observado | Evidencia | Estado |
|---|---|---|---|---|
| P01 — Comunicación válida | Procesamiento autorizado y trazable | No ejecutada: runtime n8n no accesible | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P02 — Parámetro ausente | `STOP`, rechazo y auditoría | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P03 — Emisor falsificado | Rechazo de autenticación/autorización | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P04 — Destinatario inválido | Rechazo | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P05 — Acción fuera de jurisdicción | Rechazo o escalado canónico | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P06 — Auditoría completa | Reconstrucción extremo a extremo | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P07 — Duplicación | Sin doble ejecución para el mismo `message_id` | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P08 — Concurrencia | Sin corrupción ni duplicación indebida | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P09 — Bypass Graphify | Imposible o rechazado | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P10 — Contradicción | Detectada sin invención | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P11 — WILLIAM-SCY-01 | Contraste independiente, sin ejecución operativa por defecto | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P12 — Caída de Carla | Fallo seguro, trazabilidad y recuperación controlada | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P13 — Caída de Graphify | Sin bypass | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P14 — Integridad de auditoría | UPDATE/DELETE rechazados según la política | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |
| P15 — Escalada masiva | Integridad y registro correcto bajo carga | No ejecutada | No disponible | `PENDIENTE_DE_EVIDENCIA` |

## 3. Discrepancias P0 abiertas

Las filas P0 de la matriz permanecen abiertas como `PENDIENTE_DE_EVIDENCIA`,
`AUSENTE/PENDIENTE_DE_EVIDENCIA`, `DERIVA/PENDIENTE_DE_EVIDENCIA` o
`PENDIENTE_DE_DECISION_SOBERANA`. En particular, no existe evidencia verificable
en este entorno para:

- identidad Graphify, Hermes y WILLIAM-SCY-01 en n8n;
- jurisdicción Hermes → Graphify y contraste independiente de WILLIAM-SCY-01;
- autenticación, autorización e idempotencia;
- Audit Log protegido;
- ausencia de bypass de Graphify;
- `PILOT MODE` y `Kill Switch`.

## 4. Decisión del gate

No se autoriza el piloto. La acción correcta es:

> **DETENER → REGISTRAR → ELEVAR**

Para reabrir el gate, Ingeniería SCI debe aportar la exportación/configuración
relevante, ejecutar P01–P15 sobre un entorno controlado y adjuntar por prueba el
mensaje, resultado, trazabilidad y eventos de auditoría. Solo después podrán
actualizarse las filas de la matriz; ninguna fila debe marcarse `CONFORME` sin
evidencia objetiva.
