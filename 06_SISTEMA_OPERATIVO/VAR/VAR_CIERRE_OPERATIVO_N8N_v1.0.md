# VÁR — CIERRE OPERATIVO n8n v1.0

**Fecha:** 2026-09-08  
**Workflow:** `VÁR — VAC-01 — Validación de la Verdad Canónica WAIPL`  
**Workflow ID:** `HC1SkjGphGYS3P8M`  
**Estado de partida:** DRAFT / NO PUBLICADO

## 0. OBJETIVO

Cerrar VÁR/VAC-01 para que pueda pasar de DRAFT a operativo únicamente después de una verificación final y autorización expresa del Soberano.

Este documento es un **criterio de cierre operativo**. No autoriza por sí mismo la publicación.

---

## 1. PERÍMETRO

Este documento trata exclusivamente de **VÁR**.

No diseña ni modifica el RAG de Will App.

La única consideración intersistema es evitar duplicación o confusión de funciones:

- VÁR valida verdad canónica dentro de su jurisdicción.
- El RAG de Will App mantiene sus propias funciones.
- Ninguna función del RAG se incorpora a VÁR por defecto.
- Ninguna función propia de VÁR se replica en el RAG por defecto.

---

## 2. IDENTIDAD QUE DEBE QUEDAR FIJADA

- **VÁR / VAC-01** = Agente/Nodo de Validación de la Verdad Canónica WAIPL.
- **Implementación actual:** n8n.
- **Workflow:** `HC1SkjGphGYS3P8M`.
- **Estado:** DRAFT hasta cierre.
- **YATA:** independiente y actualmente en desarrollo; no audita VÁR.
- **WILLIAM-SCY-01:** avatar del Soberano; no distribuidor, no gateway, no reenviador y no paso intermedio del flujo informacional del ecosistema.

No debe aparecer en documentación nueva que VÁR fue hecho/implementado por AutoClaw. La materialización actual de VÁR es en n8n.

---

## 3. CRITERIOS DE CIERRE n8n

### C-01 — Entrada y admisión

**Debe quedar acreditado:**

1. La entrada de VÁR recibe el contrato previsto.
2. F1 — Recepción y Admisión distingue una entrada admisible de una no admisible.
3. La ruta de rechazo funciona cuando la entrada no cumple el contrato.
4. No se amplía jurisdicción ni se ejecutan acciones fuera de la función de VÁR.

**Resultado requerido:** VERDE.

---

### C-02 — Agente Validador + LLM

**Debe quedar acreditado:**

1. El Agente Validador — VÁR es el componente funcional de validación.
2. LLM — VÁR es el modelo/componente asociado.
3. La salida del Agente Validador llega a Construir Dictamen VAD — VÁR.
4. No existen dos validadores independientes por inferencia visual.
5. No existe procesamiento paralelo no especificado.

**Resultado requerido:** VERDE.

---

### C-03 — Dictamen VAD

**Debe quedar acreditado:**

1. El flujo produce el objeto VAD previsto cuando corresponde.
2. Los campos obligatorios definidos en la especificación están presentes.
3. El resultado conserva estado y trazabilidad según lo especificado.
4. Los casos que no pueden resolverse no se convierten artificialmente en validación positiva.

**Resultado requerido:** VERDE o ABSTENCIÓN explícita cuando proceda.

---

### C-04 — No deriva epistemológica

VÁR debe conservar estas reglas:

- HECHO no se obtiene de una inferencia sin base.
- HIPÓTESIS no se convierte en hecho.
- INCERTIDUMBRE permanece expresada como tal.
- Ausencia de evidencia no se convierte en evidencia.
- Un vacío no se rellena por intuición.
- Ante información no sustentable: **«No especificado en las fuentes proporcionadas.»**

**Resultado requerido:** VERDE.

---

### C-05 — Contradicciones y abstención

**Debe quedar acreditado:**

1. Una contradicción no se resuelve por invención.
2. Cuando corresponda, el estado `CONTRADICCIÓN_SIN_RESOLVER` se conserva.
3. Cuando no existe base suficiente, VÁR puede abstenerse.
4. La abstención no se convierte en una respuesta afirmativa por defecto.

**Resultado requerido:** VERDE.

---

### C-06 — Registro e idempotencia

F7 debe conservar, según la especificación aplicable:

1. Registrar en Audit Log — VÁR.
2. Marcar Idempotencia — VÁR.
3. Anotar Pendientes.

Debe verificarse que estas operaciones no introducen conexiones o finalidades no documentadas.

**Resultado requerido:** VERDE.

---

### C-07 — F7 y separación de planos

La secuencia técnica debe permanecer:

`A1 → A2 → A3 → B1 → B2 → Respuesta Final`

Con:

**Plano A:**
- Positrón — pendiente.
- Hermes — pendiente.
- Graphy — pendiente.
- Ollama — pendiente.
- Carla — pendiente.

**Plano B:**
- VÁR → WILLIAM-SCY-01.

La ejecución es **secuencial, no paralela**.

No deben aparecer conexiones técnicas activas hacia los cinco destinos pendientes si no existen realmente.

**Resultado requerido:** VERDE.

---

### C-08 — WILLIAM-SCY-01

Debe verificarse que la salida directa:

`VÁR → WILLIAM-SCY-01`

no genere ninguna retransmisión posterior dentro del workflow.

Debe conservarse expresamente:

- no distribuidor;
- no gateway;
- no reenvío a otros nodos;
- no paso intermedio del flujo informacional del ecosistema.

**Resultado requerido:** VERDE.

---

### C-09 — Cierre del flujo

`Respuesta Final — VÁR Cierra el Flujo` debe quedar después de la entrega a WILLIAM-SCY-01 y actuar como cierre del workflow representado.

No debe reinterpretarse como un destino del Plano A ni como una nueva rama.

**Resultado requerido:** VERDE.

---

### C-10 — Frontera VÁR/YATA

Debe quedar preservado:

> **VÁR valida la verdad canónica. YATA audita a los validadores. YATA no audita VÁR. VÁR no audita YATA. Ninguno está subordinado al otro.**

YATA permanece en desarrollo hasta evidencia posterior de implementación.

**Resultado requerido:** VERDE.

---

### C-11 — Integridad documental

No deben quedar en documentación operativa vigente afirmaciones que contradigan el estado actual, especialmente:

- VÁR = 29 elementos.
- VÁR creado por AutoClaw.
- YATA hecho por AutoClaw.
- YATA auditando VÁR.
- WILLIAM-SCY-01 como gateway/distribuidor.
- conexiones activas a Positrón/Hermes/Graphy/Ollama/Carla que no estén implementadas.

**Dato canónico del universo:** **46 elementos**, incluyendo agentes, superagentes y sistemas agénticos.

**Resultado requerido:** VERDE.

---

## 4. MATRIZ MÍNIMA DE PRUEBA DE CIERRE

| ID | Prueba | Evidencia requerida | Resultado |
|---|---|---|---|
| T-01 | Entrada válida | Ejecución + salida | Pendiente de ejecución final |
| T-02 | Entrada inválida | Ejecución de rechazo | Evidencia parcial existente; repetir en cierre |
| T-03 | Validación | Ejecución VAD | Pendiente de ejecución final |
| T-04 | Incertidumbre/insuficiencia | Ejecución | Pendiente |
| T-05 | Contradicción | Ejecución | Pendiente |
| T-06 | Audit Log | Registro verificable | Pendiente |
| T-07 | Idempotencia | Segunda entrega / mismo message_id | Pendiente |
| T-08 | F7 secuencial | Ejecución completa | Pendiente |
| T-09 | No retransmisión WILLIAM-SCY-01 | Inspección de conexiones + ejecución | Pendiente |
| T-10 | Cierre final | Ejecución completa | Pendiente |

**Regla:** una prueba ejecutada acredita únicamente lo que demuestra esa prueba.

---

## 5. CONDICIÓN DE PUBLICACIÓN

VÁR solo puede pasar de DRAFT a publicado cuando se cumplan simultáneamente:

1. C-01 a C-11 revisados.
2. T-01 a T-10 ejecutados o formalmente justificados por evidencia equivalente.
3. No exista contradicción documental abierta que afecte a la identidad o función de VÁR.
4. Las conexiones previstas pero no implementadas sigan claramente marcadas como pendientes.
5. La inspección visual/semántica final del workflow no introduzca relaciones inexistentes.
6. Exista **autorización expresa del Soberano para publicar**.

Hasta entonces:

> **VÁR = DRAFT / NO PUBLICADO.**

---

## 6. CRITERIO DE CIERRE

El objetivo no es que el workflow tenga más nodos ni más complejidad.

El objetivo es:

> **VÁR hace exactamente lo que debe hacer, no hace lo que no debe hacer, deja evidencia de lo que hace y no permite inferir como existente lo que no existe.**

Cuando C-01…C-11 y T-01…T-10 estén acreditados y exista autorización soberana, VÁR estará en condición de publicación.
