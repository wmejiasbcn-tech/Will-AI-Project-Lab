# Positrón — Integración SCI/n8n

**Fuente:** INFORME DE INTEGRACIÓN ARNÉS AGÉNTICO WAIPL ↔ SCI/n8n (48 secciones, 2026-08-29)

## Posición arquitectónica

```
WAIPL → ADN → GRAPHIFY → HARNESS + SCI → POSITRÓN → OLLAMA → AGENTES → GRAPHIFY
```

Positrón es el **cerebro operativo**. Recibe del Arnés+SCI, procesa, devuelve a Graphify.

## Responsabilidad (Sección 45)

| Capa | Responsabilidad |
|------|----------------|
| Graphify | Cartografía/contexto relacional |
| Harness | Contexto, reglas, autoridad, preparación, verificación |
| SCI | Comunicación, coordinación, transporte, trazabilidad |
| n8n | Orquestación/ejecución del flujo SCI |
| **Positrón** | **Procesamiento operativo** |
| Ollama | Infraestructura/modelo local |
| Agente | Decisión/acción dentro de su jurisdicción |

## Reglas que Positrón debe cumplir

### Principios cero (Sección 3)

- DOCUMENTADO no es EXISTENTE no es EJECUTABLE no es OPERATIVO
- CAPACIDAD TÉCNICA no es PERMISO no es AUTORIZACIÓN
- ACK no es RESULTADO; RESULTADO no es VERIFICACIÓN

### No fabricación de telemetría (Sección 5)

Positrón no puede presentar como telemetría primaria una ejecución hipotética, simulada o esperada.

Estados correctos:
- NO ACCESIBLE DESDE ESTE ENTORNO
- NO DETERMINADO
- EJECUTADO / RESULTADO NO VERIFICADO
- EJECUTADO / VERIFICADO

### Estados que Positrón debe representar (Sección 29)

DOCUMENTED | EXISTS | ACCESSIBLE | AUTHORIZED | READY | EXECUTING | EXECUTED | VERIFIED | REJECTED | BLOCKED | FAILED | NOT_DETERMINED | NOT_ACCESSIBLE | ESCALATED

## SCI ya activo (Sección 43) — lo que Positrón puede consumir

El SCI/n8n ya tiene operativo:

1. Emily funcionando como puente
2. Autenticación/autorización en desarrollo
3. Integridad SHA-256 del payload SCI
4. Idempotencia (DUPLICATE_REJECTED)
5. Kill Switch (sin bypass)
6. Audit Log operativo
7. Contingencia DS-07 (escalada a WILLIAM-SCY-01)
8. Nomenclatura Graphify/Graphy corregida
9. Ejecución E2E con respuesta de Carla
10. Canal Emily → OpenAI → Carla ve
rificado

Positrón NO debe duplicar estos mecanismos. Debe consumirlos via contrato SCI (Sección 44).

## Contrato mínimo SCI para Positrón (Sección 28 + 39)

```json
{
  "message_id": "SCI-...",
  "correlation_id": "COR-...",
  "operation_id": "OP-...",
  "protocol_version": "SCI-WAIPL-1.0",
  "sender_node": "R...",
  "target_node": "positron",
  "intent": "...",
  "purpose": "...",
  "urgency_level": "N1",
  "authorization": { "status": "AUTHORIZED", "source": "...", "scope": "..." },
  "context": { "graphify_reference": "...", "harness_profile": "...", "relevant_rules": [] },
  "integrity": "...",
  "execution": { "status": "...", "result": "...", "evidence": [] },
  "verification": { "status": "...", "method": "..." },
  "audit": { "event_id": "...", "timestamp": "..." }
}
```

## Semántica canónica Emily → Carla (Sección 8)

```
a_quien = Carla (destinatario real)
por_que = sender_node (nodo origen/detonante)
cuando = N1 / N2 / N3 (nivel de urgencia)
```

No reinterpretar sender_node como destinatario.

## Retry/contingencia (Sección 12)

```
intento → reintento 1 → reintento 2 → reintento 3 → escalada a WILLIAM-SCY-01
```

Si Carla no responde, WILLIAM-SCY-01 actúa como contingencia.

## Nomenclatura (Sección 6)

- Graphify = App/Plataforma
- Graphy = agente/sistema
- "Graficar" = prohibido en este contexto

## Divergencia graph/ vs graphify-out/ (Sección 33)

El informe confirma: se describió graph/ pero físicamente se encontro graphify-out/.
Esto demuestra DOCUMENTADO no es EXISTENTE.
El SCI debe poder transportar esa incertidumbre sin convertirla en falso hecho.

## Implicaciones para la migración a Vercel

1. Positrón en Vercel debe poder recibir mensajes del SCI (n8n webhooks)
2. Las rutas /api/* ya tienen headers no-store (ver vercel.json)
3. Necesita endpoint para recibir webhook SCI: POST /api/sci/webhook
4. Necesita validar integridad SHA-256 del payload SCI
5. Necesita respetar Kill Switch (consultar estado antes de procesar)
6. Necesita escribir al 
Audit Log (tabla en DB o via SCI)
7. NO debe duplicar: idempotencia, Kill Switch, Audit Log (ya en SCI)
8. Debe devolver estados SCI correctos (no simular)

## CANON-CIERRE

| Casilla | Valor |
|----------|-------|
| Orquesta | Positrón WAIPL |
| Spec/N3 | N1 — integración SCI |
| Superficie | INFORME_INTEGRACION_ARNES_AGENTE_SCI_n8n.md (48 secciones) |
| Runtime | No ejecutado |
| Prueba | Lectura completa del informe de integración |
| Parada | Requisitos SCI extraídos. Pendiente: implementar endpoints SCI en Positrón. |
| No es | No es implementación. Es análisis de requisitos. |
