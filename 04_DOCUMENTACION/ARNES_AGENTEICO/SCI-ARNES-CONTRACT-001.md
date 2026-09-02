# SCI-ARNES-CONTRACT-001 — Contrato de Integración SCI ↔ Arnés

**Estado:** A — ACREDITADO como contrato documental/contractual; la implementación física completa de cada extremo/campo no queda declarada por este documento.

## 1. Propósito

Definir la interfaz que permite al Arnés consumir la comunicación ya proporcionada por SCI y devolver estado, resultado, evidencia y trazabilidad sin duplicar mecanismos internos de SCI.

## 2. Dirección

La interfaz es bidireccional:

```text
SCI → ARNÉS
ARNÉS → SCI
```

El canal lógico se mantiene **HÍBRIDO**: síncrono + asíncrono según el caso contractual.

## 3. SCI → ARNÉS

SCI transporta hacia Arnés, cuando corresponda:

### Identidad
- `sender_node`
- `target_node`
- `message_id`
- `correlation_id`
- `protocol_version`

### Comunicación
- `que`
- `a_quien`
- `por_que`
- `para_que`
- `como`
- `cuando`
- `urgency_level`

### Contexto / intención / autorización
- contexto disponible;
- intención declarada;
- información de autorización disponible para la decisión dentro de jurisdicción del Arnés.

### Resultado / evidencia / verificación
- estado;
- `fault_state`;
- `result_claim`;
- `evidence_ref`;
- `verification_status`;
- `audit_ref`;
- `return_timestamp` cuando corresponda.

## 4. ARNÉS → SCI

Arnés devuelve hacia SCI, cuando corresponda:

- identidad;
- correlación;
- estado de recepción;
- estado de ejecución;
- autorización/resultado de control de autoridad;
- resultado;
- `fault_state`;
- evidencia o referencia a evidencia;
- estado de verificación;
- feedback;
- error;
- timestamp;
- `audit_ref` cuando exista.

## 5. Responsabilidades de SCI

SCI conserva la responsabilidad sobre:

- transporte;
- identidad del mensaje;
- `message_id`;
- `correlation_id`;
- canal;
- mecanismos propios de autorización del canal;
- idempotencia del canal;
- Kill Switch del canal;
- PILOT MODE del canal;
- Audit Log del canal;
- trazabilidad del intercambio.

## 6. Responsabilidades del Arnés

Arnés conserva, dentro de su jurisdicción:

- interpretación del contexto operativo;
- aplicación de reglas;
- evaluación de autoridad/autorización aplicable;
- preparación;
- ejecución;
- verificación de su propia jurisdicción;
- generación del resultado;
- generación/referencia de evidencia;
- feedback hacia SCI.

## 7. No duplicación

Arnés no crea mecanismos paralelos para:

- Envelope SCI;
- `message_id` del canal;
- `correlation_id` del canal;
- transporte SCI;
- Audit Log del canal;
- Kill Switch del canal;
- whitelist del canal;
- idempotencia del canal;
- retry del canal;
- clasificación propia de errores de SCI;
- Gateway SCI.

SCI no absorbe:

- reglas internas del Arnés;
- lógica interna de ejecución;
- autoridad propia del Arnés;
- preparación interna;
- funciones de Vár/Yata;
- funciones de WILLIAM-SCY-01.

## 8. Estados de fallo de interfaz

El contrato distingue:

- `AGENTE_NO_DISPONIBLE`
- `AGENTE_DISPONIBLE_RECHAZA`
- `AGENTE_EJECUTA_FALLA`
- `AGENTE_EJECUTA_RESULTADO_NO_VERIFICABLE`

Estos estados describen la interfaz SCI ↔ Arnés y no determinan por sí mismos una FSM interna del Arnés.

## 9. Distinciones obligatorias

```text
DOCUMENTADO ≠ EXISTENTE ≠ EJECUTABLE ≠ OPERATIVO
CAPACIDAD TÉCNICA ≠ PERMISO ≠ AUTORIZACIÓN
AFIRMACIÓN ≠ EVIDENCIA ≠ RESULTADO ≠ VERIFICACIÓN
ACK ≠ RESULTADO
RESULTADO ≠ VERIFICACIÓN
```

## 10. Regla de vacío

Si falta información material para ejecutar de forma autorizada y gobernada, el Arnés no completa el vacío mediante inferencia.

```text
DETENER → IDENTIFICAR → HACER VISIBLE → ESCALAR/CONSULTAR → VALIDAR → CONTINUAR
```

## 11. Límite

Este documento materializa el contrato lógico de integración. No declara que exista todavía una implementación física completa de cada extremo o de cada campo.
