# HARNESS-SPEC-001 — ERRATA 01

**Estado:** PROPUESTA DE CORRECCIÓN — pendiente de contraste independiente por Aletheia.

**Propósito:** fijar las tres correcciones materiales señaladas en el contraste de Aletheia del BLOQUE 02, sin rediseñar la especificación ni introducir nuevas capacidades.

## 1. Frontera Arnés ↔ SCI

El flujo del Arnés describe el procesamiento interno a partir de una entrada transportada por SCI y la preparación de información que SCI podrá transportar posteriormente.

El Arnés **consume la entrada transportada por SCI y prepara su resultado para SCI; no define, implementa ni gestiona el transporte, registro o flujo de comunicación de SCI**.

## 2. Estados de fallo de interfaz

Los cuatro estados:

- `AGENTE_NO_DISPONIBLE`
- `AGENTE_DISPONIBLE_RECHAZA`
- `AGENTE_EJECUTA_FALLA`
- `AGENTE_EJECUTA_RESULTADO_NO_VERIFICABLE`

son **estados de la interfaz SCI ↔ Arnés**. No constituyen ni implican automáticamente una FSM interna del Arnés.

La FSM interna completa del Arnés permanece **D — NO DETERMINADA**.

## 3. Vacíos explícitos

Todo elemento cuya existencia física, implementación, ubicación, carga, integración o cobertura no esté acreditada debe permanecer clasificado como **D — NO DETERMINADO**. La documentación de una pieza no constituye evidencia de su existencia física u operación.

## 4. Alcance de esta errata

Esta errata no crea nuevas jurisdicciones, permisos, capacidades, agentes, sensores, guías, FSM ni mecanismos de transporte. Su única función es hacer explícitas las fronteras y estados ya establecidos para evitar interpretaciones indebidas.

**Relación:** forma parte del expediente de materialización del Arnés y debe leerse junto con `HARNESS-SPEC-001.md` hasta que el contraste independiente determine su estado.
