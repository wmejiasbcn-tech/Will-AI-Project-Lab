# HARNESS-SPEC-001 — Especificación Operativa del Arnés Agéntico WAIPL

**Estado del documento:** PROPUESTA DE MATERIALIZACIÓN — pendiente de contraste independiente y validación soberana cuando corresponda.

**Responsable operativo:** Carla
**Capa de contraste:** Aletheia
**Sistema de comunicación de integración:** SCI-WAIPL-1.0

---

## 0. Regla de evidencia

Este documento separa explícitamente:

- **A — ACREDITADO:** existe evidencia suficiente.
- **B — REQUIERE REVISIÓN:** existe, pero presenta una cuestión material.
- **C — PROPUESTA / NO VALIDADA:** diseño o intención todavía no validada.
- **D — NO DETERMINADO:** falta evidencia suficiente.

La presencia de una sección en este documento no demuestra por sí misma su implementación física ni su operación.

---

## 1. Objetivo

**A:** Materializar una especificación operativa del Arnés Agéntico WAIPL que permita integrar contexto, reglas, autoridad, preparación, ejecución, verificación, evidencia, feedback y trazabilidad dentro de su jurisdicción, utilizando los contratos ya establecidos con SCI sin duplicar sus funciones.

---

## 2. Jurisdicción

**A:** El Arnés trabaja sobre contexto operativo, reglas, autoridad, preparación, ejecución y verificación dentro de su jurisdicción.

**A:** SCI mantiene la jurisdicción de comunicación, transporte, identidad, correlación, trazabilidad y registro/transportación del estado.

**A:** El Arnés no absorbe las funciones propias de SCI, Vár o Yata.

---

## 3. Entradas del Arnés

**A:** El Arnés debe poder trabajar con la información contractual que SCI transporta hacia él.

### Identidad y correlación

- `sender_node`
- `target_node`
- `message_id`
- `correlation_id`
- `protocol_version`

### Parámetros de comunicación

- `que`
- `a_quien`
- `por_que`
- `para_que`
- `como`
- `cuando`
- `urgency_level`

### Estado / resultado

- estado de recepción/ejecución/resultado
- `fault_state`
- `result_claim`
- `return_timestamp`

### Evidencia / verificación

- `evidence_ref`
- `verification_status`
- `audit_ref`

**Aclaración:** estos campos representan el contrato de integración documentado para SCI ↔ Arnés; no implican que todos estén físicamente conectados al Arnés en este momento.

---

## 4. Flujo operativo mínimo

**A:** La secuencia funcional definida es:

```text
ENTRADA SCI
    ↓
RECEPCIÓN
    ↓
CONTEXTO
    ↓
REGLAS
    ↓
AUTORIDAD
    ├── no autorizado → RECHAZO + TRAZABILIDAD
    ↓
PREPARACIÓN
    ↓
EJECUCIÓN
    ├── fallo → RESULTADO DE FALLO
    ↓
VERIFICACIÓN
    ↓
RESULTADO + EVIDENCIA
    ↓
FEEDBACK
    ↓
SALIDA → SCI
```

Esta secuencia describe el flujo operativo; no demuestra todavía una implementación física de cada etapa.

---

## 5. Estados de fallo de la interfaz SCI ↔ Arnés

**A:** Se mantienen los cuatro estados de fallo definidos para la interfaz:

1. `AGENTE_NO_DISPONIBLE`
2. `AGENTE_DISPONIBLE_RECHAZA`
3. `AGENTE_EJECUTA_FALLA`
4. `AGENTE_EJECUTA_RESULTADO_NO_VERIFICABLE`

**D:** No queda determinada en esta especificación la máquina de estados interna completa del Arnés. Estos cuatro estados no se convierten automáticamente en su FSM interna.

---

## 6. Salida del Arnés hacia SCI

**A:** La respuesta del Arnés debe proporcionar, cuando corresponda al contrato, información suficiente para que SCI transporte y registre:

- identidad;
- contexto relevante;
- intención;
- autorización/estado de autorización;
- estado de ejecución;
- resultado;
- evidencia;
- estado de verificación;
- error/fallo;
- feedback;
- timestamp;
- correlación.

**A:** El Arnés no debe limitar la comunicación a un `SUCCESS/ERROR` si el contrato exige mayor estado y evidencia.

---

## 7. Evidencia y verificación

**A:** El Arnés debe conservar la distinción entre:

```text
AFIRMACIÓN
   ↓
EVIDENCIA
   ↓
RESULTADO
   ↓
VERIFICACIÓN
```

**A:** El Arnés no sustituye la jurisdicción epistemológica de Vár/Yata.

**D:** No se determina aquí una arquitectura adicional de meta-verificación.

---

## 8. Autoridad y detención

**A:** La capacidad técnica no equivale a permiso ni a autorización.

**A:** Ante un vacío material de autoridad, especificación o información necesaria para ejecutar una acción, el comportamiento gobernado es detener, hacer visible el vacío y escalar para validación, en lugar de completarlo mediante inferencia.

**A:** Una actuación no autorizada constituye una infracción de gobernanza independientemente de su impacto posterior.

---

## 9. Dependencias conocidas

### SCI-WAIPL-1.0

**A:** Dependencia contractual para comunicación, transporte, identidad, correlación, trazabilidad y estado/evidencia transportados.

### Graphify

**A:** Forma parte del contexto/cartografía relacional del ecosistema.

**D:** No se determina en este documento la implementación física concreta de una integración directa Graphify ↔ Arnés.

### Positrón

**A:** Rol de procesamiento dentro de la arquitectura conocida.

**D:** No se determina aquí el mecanismo físico de integración Positrón ↔ Arnés.

### Ollama

**A:** Rol de infraestructura/modelo dentro de la arquitectura conocida.

**D:** No se determina aquí el mecanismo físico de integración Ollama ↔ Arnés.

---

## 10. Guías / Feedforward

**C:** El Arnés requerirá una capa de guías operativas que exponga las reglas necesarias antes de la ejecución.

**D:** El catálogo físico definitivo, formato, ubicación y mecanismo de carga de dichas guías todavía no están acreditados.

No se crea en este documento un catálogo ficticio.

---

## 11. Sensores / Feedback

**C:** El Arnés requerirá mecanismos de feedback/observabilidad para detectar y comunicar estados relevantes después de la ejecución.

**D:** El catálogo físico definitivo, implementación, ubicación y cobertura de Sensors todavía no están acreditados.

No se declara ningún sensor como operativo sin evidencia física.

---

## 12. Implementación física

**D:** La existencia de una implementación física completa del Arnés no queda acreditada por este documento.

**D:** No se declara existente una aplicación, workflow, servicio, agente, script, FSM interna, sandbox, `AGENTS.md`, conjunto de Guides o conjunto de Sensors específico del Arnés salvo evidencia independiente.

---

## 13. Condiciones de éxito

**C:** Para considerar una pieza del Arnés materializada, deberá existir un artefacto identificable y evidencia suficiente de su funcionamiento o integración, según corresponda.

Como mínimo, la evidencia deberá permitir distinguir:

```text
DOCUMENTADO
    ≠
EXISTENTE
    ≠
EJECUTABLE
    ≠
OPERATIVO
    ≠
VERIFICADO
```

---

## 14. Condiciones de detención

El Arnés no debe continuar una ejecución cuando aparezca un vacío material relativo a:

- autoridad;
- autorización;
- identidad;
- contexto imprescindible;
- regla aplicable;
- evidencia necesaria;
- condición de seguridad;
- requisito de ejecución;
- resultado que no pueda verificarse cuando la verificación sea exigida.

En esos casos:

```text
DETENER
→ IDENTIFICAR VACÍO
→ HACER VISIBLE
→ ESCALAR / CONSULTAR
→ ESPERAR VALIDACIÓN CUANDO SEA NECESARIA
→ CONTINUAR SOLO CON BASE SUFICIENTE
```

---

## 15. Elementos deliberadamente no definidos

Los siguientes elementos quedan **D — NO DETERMINADOS** hasta disponer de evidencia o decisión válida:

- máquina de estados interna completa;
- estructura física definitiva de directorios del Arnés fuera de este documento;
- implementación definitiva de Context Engineering;
- catálogo definitivo de Guides;
- catálogo definitivo de Sensors;
- integración física Graphify ↔ Arnés;
- integración física Positrón ↔ Arnés;
- integración física Ollama ↔ Arnés;
- despliegue operativo de Vár/Yata dentro de este circuito;
- cualquier nueva jurisdicción o permiso no documentado.

---

## 16. Criterio de cierre de este artefacto

Este artefacto podrá considerarse **cerrado como especificación** cuando el contraste de Aletheia no detecte una cuestión material pendiente dentro de su jurisdicción y, cuando corresponda, se obtenga la validación soberana requerida.

El cierre de esta especificación **no equivale** al cierre del Arnés ni a su declaración de operación.

---

## 17. Siguiente paso operativo

Una vez contrastada esta especificación, el siguiente bloque será la **materialización física mínima** de las piezas que resulten acreditadas, empezando por las que tengan menor riesgo de introducir nuevas decisiones:

1. estructura documental/contractual;
2. contrato de integración SCI ↔ Arnés;
3. Guides acreditables;
4. Sensors acreditables;
5. mecanismo de verificación mínimo;
6. prueba de integración estrictamente necesaria.

No se implementarán piezas clasificadas como D sin resolver previamente el vacío que las afecta.
