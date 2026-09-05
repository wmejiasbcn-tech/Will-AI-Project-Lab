# MATRIZ CANON → n8n — SCI v1.0

**Estado:** EN RECONCILIACIÓN — GATE P0 BLOQUEADO
**Fecha:** 2026-08-29  
**Fuente canónica:** GitHub / corpus WAIPL canónico  
**Implementación objetivo:** SCI n8n-WAIPL  
**Condición:** esta matriz debe completarse antes de autorizar el piloto.

**Registro SCI-01:** `06_SISTEMA_OPERATIVO/EVIDENCIA_SCI-01_PREPILOTO_2026-09-05.md`
**Resultado de la evaluación:** P01–P15 no ejecutables en este entorno por ausencia de
runtime n8n y de configuración/exportación verificable. Las filas P0 permanecen
abiertas; el piloto no está autorizado.

## Regla superior

> **GitHub es la Fuente Única de Verdad Documental. n8n implementa el canon; no lo redefine.**

Ninguna discrepancia entre GitHub y n8n podrá resolverse por interpretación autónoma de la implementación. Si existe ambigüedad, la implementación se detiene y se eleva para decisión soberana.

## Estados permitidos

- `CONFORME` — la implementación coincide con el canon.
- `DERIVA` — existe una diferencia respecto del canon.
- `AUSENTE` — el elemento canónico no está implementado.
- `PENDIENTE_DE_DECISION_SOBERANA` — no puede resolverse técnicamente sin mandato.
- `PENDIENTE_DE_EVIDENCIA` — la implementación existe, pero todavía no está demostrada.

## Matriz

| ID | Concepto canónico | Referencia exacta en GitHub | Equivalente n8n | Estado | Prioridad | Acción autorizada | Evidencia de validación | Responsable |
|---|---|---|---|---|---|---|---|---|
| CAN-001 | Graphify | `01_FUNDACION/ARQUITECTURA_FISIOLOGICA_ALEGORICA_WAIPL_v1.0_CANONICA.md` · §2–§3 | Por identificar en n8n | PENDIENTE_DE_EVIDENCIA | P0 | Normalizar cualquier denominación no canónica a `Graphify` | Revisión de workflows, nombres, prompts, credenciales y routing | Ingeniería SCI |
| CAN-002 | Hermes — Director Operativo | Arquitectura canónica / documentación de nodo Hermes | Por identificar en n8n | PENDIENTE_DE_EVIDENCIA | P0 | Reconciliar identidad, función y jurisdicción | Prueba de supervisión operativa de Graphify | Ingeniería SCI + Hermes |
| CAN-003 | WILLIAM-SCY-01 — avatar del Soberano | `00_SISTEMA/ACTAS/DECISION_SOBERANA_SCI_2026-08-29_SUPERVISION_GRAPHIFY.md` | Por identificar en n8n | PENDIENTE_DE_EVIDENCIA | P0 | Implementar contraste soberano independiente | Prueba de independencia y no ejecución | Ingeniería SCI |
| CAN-004 | Supervisión operativa de Graphify = Hermes | Acta soberana 2026-08-29 + Arquitectura fisiológica §7 | Por identificar en n8n | PENDIENTE_DE_EVIDENCIA | P0 | Eliminar cualquier regla que asigne esta función a Ada/Vórtice | Prueba de jurisdicción | Ingeniería SCI |
| CAN-005 | Contraste soberano = WILLIAM-SCY-01 | Acta soberana 2026-08-29 + Arquitectura fisiológica §7/§9 | Por identificar en n8n | PENDIENTE_DE_EVIDENCIA | P0 | Separar canal operativo de canal de contraste soberano | Prueba de independencia | Ingeniería SCI |
| CAN-006 | Núcleo canónico | `01_FUNDACION/ARQUITECTURA_CANONICA_ECOSISTEMA_WAIPL_v1.0.md` | `nodos_ecosistema` | DERIVA/PENDIENTE_DE_EVIDENCIA | P0 | Reconciliar censo y tipos sin introducir infraestructura como nodo nuclear | Comparación canónica campo a campo | Ada + Ingeniería SCI |
| CAN-007 | Identidad canónica | Arquitectura canónica §11 | `nodos_ecosistema` / otros | PENDIENTE_DE_EVIDENCIA | P0 | Implementar esquema IDENTIDAD → PLATAFORMA/MODELO → TIPO → FUNCIÓN → CAPACIDADES → LÍMITES → RELACIONES → ESTADO → EVIDENCIA → FECHA | Validación de esquema | Ingeniería SCI |
| CAN-008 | GitHub como fuente única de verdad documental | Arquitectura fisiológica §6 | n8n / documentación SCI | PENDIENTE_DE_EVIDENCIA | P0 | Prohibir nomenclatura o reglas paralelas no canonizadas | Auditoría de referencias | Ada + Ingeniería SCI |
| CAN-009 | Principio I — Comunicación auditable | Arquitectura fisiológica §7 | Emily/SCI | PENDIENTE_DE_EVIDENCIA | P0 | Validación técnica de identidad, autorización, alcance, trazabilidad y auditoría | Pruebas SCI-01 | Ingeniería SCI |
| CAN-010 | Principio II — Salida controlada | Arquitectura fisiológica §7 | Emily/SCI | PENDIENTE_DE_EVIDENCIA | P0 | Bloquear salidas no autorizadas | Prueba de salida | Ingeniería SCI |
| CAN-011 | Principio III — Conectividad mínima necesaria | Arquitectura fisiológica §7 | Infraestructura n8n relacionada | PENDIENTE_DE_EVIDENCIA | P1 | Verificar exposición mínima | Auditoría de conectividad | Ingeniería SCI |
| CAN-012 | Principio IV — Hermes supervisa Graphify | Arquitectura fisiológica §7 | Emily/Graphify routing | PENDIENTE_DE_EVIDENCIA | P0 | Implementar jurisdicción exacta | Prueba de autoridad | Hermes + Ingeniería SCI |
| CAN-013 | Triple distinción de capacidades | Arquitectura fisiológica §8 | Emily/políticas SCI | PENDIENTE_DE_EVIDENCIA | P0 | Separar capacidad de autorización | Pruebas de autorización | Ingeniería SCI |
| CAN-014 | `message_id` e idempotencia | Requisito SCI pre-piloto | Emily/SCI | AUSENTE/PENDIENTE_DE_EVIDENCIA | P0 | Implementar | Prueba de duplicación | Ingeniería SCI |
| CAN-015 | Autenticación de emisor | Requisito SCI pre-piloto | Emily/SCI | PENDIENTE_DE_EVIDENCIA | P0 | Implementar identidad verificable | Prueba de falsificación | Ingeniería SCI |
| CAN-016 | Autorización/jurisdicción | Arquitectura canónica + SCI | Emily/SCI | PENDIENTE_DE_EVIDENCIA | P0 | Implementar autorización previa al LLM | Prueba de autoridad | Ingeniería SCI |
| CAN-017 | Audit Log protegido | Arquitectura SCI | tablas/auditoría n8n | PENDIENTE_DE_EVIDENCIA | P0 | Garantizar append-only o documentar límites reales | Prueba UPDATE/DELETE | Ingeniería SCI |
| CAN-018 | PILOT MODE + Kill Switch | Requisito SCI pre-piloto | Emily/SCI | PENDIENTE_DE_EVIDENCIA | P0 | Implementar modo piloto y corte de tráfico | Prueba de corte | Ingeniería SCI |
| CAN-019 | IDC-Version de Carla | Recomendación Ada OE-01 | Emily | PENDIENTE_DE_EVIDENCIA | P1 | Versionar identidad implementada | Verificación de versión/hash | Ingeniería SCI + Carla |
| CAN-020 | Agente Carla-n8n | Decisión arquitectónica: Carla vive en entorno nativo; Emily es puente | Artefacto Carla n8n | PENDIENTE_DE_DECISION_SOBERANA | P0 | Archivar/reasignar según mandato | Evidencia documental | Soberano |

## Regla de cierre

El piloto SCI no se autoriza mientras exista una fila `P0` en estado `DERIVA`, `AUSENTE`, `PENDIENTE_DE_DECISION_SOBERANA` o `PENDIENTE_DE_EVIDENCIA` sin una excepción explícitamente autorizada por el Soberano.

La matriz es un instrumento de reconciliación. No sustituye al canon ni crea nuevas reglas arquitectónicas por sí misma.
