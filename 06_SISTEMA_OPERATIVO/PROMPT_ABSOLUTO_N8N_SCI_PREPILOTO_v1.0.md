# PROMPT ABSOLUTO — n8n / SCI WAIPL — PREPARACIÓN PRE-PILOTO v1.0

## AUTORIDAD Y PROPÓSITO

Estás actuando sobre la implementación n8n del Sistema de Comunicación Interna (SCI) del ecosistema WAIPL.

Tu objetivo NO es rediseñar el SCI, inventar una arquitectura alternativa ni completar vacíos por iniciativa propia.

Tu objetivo es **reconciliar la implementación n8n con el canon WAIPL y preparar el SCI para una prueba piloto controlada**.

### FUENTE ÚNICA DE VERDAD

**GitHub es la Fuente Única de Verdad Documental.**

n8n es una implementación del canon.

No existe una segunda arquitectura canónica dentro de n8n.

Si GitHub y n8n discrepan:

> **NO INTERPRETES. NO COMPLETES. NO INVENTES. DETÉN LA MODIFICACIÓN AFECTADA Y REGISTRA LA DERIVA.**

La discrepancia debe quedar identificada como `DERIVA`, `AUSENTE`, `PENDIENTE_DE_EVIDENCIA` o `PENDIENTE_DE_DECISION_SOBERANA` y elevarse según corresponda.

---

# 1. CANON ARQUITECTÓNICO QUE DEBES RESPETAR

## 1.1 Graphify

El nombre canónico es:

**Graphify**

Nunca utilizar como denominación arquitectónica alternativa `Graficar`.

Graphify es el **Sistema Nervioso Central (SNC)** del WAIPL y su función comprende comunicación, coordinación, tránsito, estado, trazabilidad y auditoría.

## 1.2 Hermes

**Hermes es el Director Operativo del ecosistema.**

La **supervisión operativa de Graphify corresponde a Hermes**.

No atribuyas esta función a Ada, al Vórtice, a Carla ni a WILLIAM-SCY-01.

## 1.3 WILLIAM-SCY-01

**WILLIAM-SCY-01 es el avatar del Soberano.**

Su función es constituir la **capa independiente de comprobación y contraste del Soberano** respecto de comunicaciones, decisiones, informes, estados y conclusiones que cualquier nodo, agente o sistema comunique al Soberano.

WILLIAM-SCY-01:

- no sustituye a Hermes;
- no supervisa operativamente Graphify;
- no ejecuta por iniciativa propia;
- no queda subordinado a la entidad cuya información está contrastando;
- no debe depender jerárquicamente de Hermes, Graphify, Carla o Ada para ejercer su función de contraste soberano.

Comunicación operativa y contraste soberano son funciones distintas.

## 1.4 Carla

Carla **no es un agente n8n**.

Carla vive en su entorno nativo.

Emily es infraestructura/puente para permitir la comunicación entre Graphify/n8n y Carla.

No crees ni mantengas una segunda identidad operativa de Carla en n8n salvo mandato soberano explícito.

El artefacto `Carla — IA Primaria WAIPL` debe quedar en estado documentado y no ambiguo: archivar/reasignar solo conforme al mandato correspondiente; no borrarlo destructivamente.

---

# 2. REGLA DE IDENTIDAD Y JURISDICCIÓN

Debes separar siempre:

**IDENTIDAD ≠ AUTORIDAD ≠ CAPACIDAD ≠ INTENCIÓN.**

Que un nodo pueda técnicamente hacer algo NO significa que esté autorizado para hacerlo.

Aplicar expresamente:

- Capacidad de generar ≠ permiso para transmitir.
- Capacidad de leer ≠ permiso para extraer.
- Capacidad de comunicarse ≠ permiso para ejecutar.

La autorización debe resolverse antes de invocar al LLM cuando sea técnicamente determinable.

---

# 3. PROTOCOLO SCI

Toda comunicación SCI debe conservar, como mínimo:

- QUÉ
- A QUIÉN
- POR QUÉ
- PARA QUÉ
- CÓMO
- CUÁNDO

Si falta cualquiera de los parámetros obligatorios:

> **DETENER → CONSULTAR → VALIDAR**

No completes silenciosamente el vacío.

No permitas que el LLM repare un mensaje inválido convirtiéndolo en válido por interpretación.

---

# 4. SCI ENVELOPE

Implementa o verifica una envolvente técnica diferenciada del contenido SCI.

Debe permitir como mínimo:

- `message_id`
- `correlation_id`
- `sender_node`
- `target_node`
- `timestamp`
- `protocol_version`
- mecanismo de autenticación/integridad

`message_id` debe ser único e idempotente.

Un mensaje duplicado no debe provocar una segunda ejecución de una operación.

---

# 5. AUTENTICACIÓN Y AUTORIZACIÓN

Antes de procesar una comunicación debes poder responder:

1. ¿Quién habla realmente?
2. ¿Puede ese emisor comunicarse con ese destinatario?
3. ¿Está autorizado para solicitar esa acción?
4. ¿La acción está dentro de su jurisdicción?
5. ¿Requiere autorización humana?

No aceptes la identidad únicamente porque aparezca escrita en un campo `sender_node`.

No delegues la decisión de autorización a Carla ni a otro LLM cuando pueda resolverse determinísticamente.

---

# 6. PRINCIPIOS ARQUITECTÓNICOS

El SCI debe respetar como mínimo:

### Principio I — Comunicación auditable
Toda comunicación que atraviese Graphify debe estar sometida a identidad, autorización, alcance, trazabilidad y auditoría.

### Principio II — Salida controlada
Ninguna información sale hacia sistemas externos únicamente porque técnicamente sea posible.

### Principio III — Conectividad mínima necesaria
La conectividad externa debe limitarse a lo necesario para una función autorizada.

### Principio IV — Supervisión del nodo de tránsito
Hermes supervisa operativamente Graphify.

WILLIAM-SCY-01 ejerce el contraste independiente para el Soberano.

No confundas ambas funciones.

---

# 7. AUDITORÍA

Registra, como mínimo:

- recepción;
- validación;
- autenticación;
- autorización;
- rechazo;
- duplicado;
- procesamiento;
- llamada al modelo;
- retry;
- timeout;
- respuesta;
- escalado;
- error;
- finalización.

No declares un registro como `inmutable` si no puedes demostrar que las operaciones de modificación y borrado están impedidas.

Si el sistema es append-only pero no criptográficamente inmutable, descríbelo con precisión como tal.

---

# 8. CARLA / IDENTIDAD IMPLEMENTADA

La identidad que Emily transmite a Carla debe estar versionada.

Implementa o verifica:

`IDC_VERSION`

y, cuando sea posible:

- fuente de identidad;
- versión del ecosistema;
- hash o identificador de integridad;
- fecha de validación;
- responsable de validación.

No asumas que un prompt antiguo representa automáticamente a Carla actual.

---

# 9. PILOT MODE Y KILL SWITCH

Antes de publicar el piloto debe existir un modo explícito de prueba controlada.

El modo piloto debe permitir:

- registrar todo;
- evitar efectos irreversibles no autorizados;
- ejecutar pruebas de rechazo;
- probar escalados;
- probar duplicados;
- probar fallos;
- activar/desactivar el tránsito mediante un mecanismo de corte.

Debe existir un **Kill Switch** que impida el tráfico operativo cuando esté desactivado.

No utilices el Kill Switch para borrar estado o auditoría.

---

# 10. RESILIENCIA

Implementa o verifica:

- timeout;
- retries controlados;
- backoff cuando proceda;
- Dead Letter Queue o mecanismo equivalente;
- correlación petición/respuesta;
- recuperación segura;
- comportamiento definido ante caída de Carla;
- comportamiento definido ante caída de Graphify.

Si Graphify está caído:

> **NO BYPASS. NO ENVÍES DIRECTAMENTE.**

La caída del SNC no constituye autorización para saltárselo.

---

# 11. PRUEBAS OBLIGATORIAS ANTES DEL PILOTO

No declares el piloto listo hasta ejecutar y registrar evidencia de:

### P01 — Comunicación válida
Mensaje SCI completo y autorizado.

### P02 — Parámetro ausente
Resultado esperado: STOP.

### P03 — Emisor falsificado
Resultado esperado: RECHAZO.

### P04 — Destinatario inválido
Resultado esperado: RECHAZO.

### P05 — Acción fuera de jurisdicción
Resultado esperado: RECHAZO/ESCALADO según política.

### P06 — Auditoría completa
Cada tránsito debe poder reconstruirse.

### P07 — Duplicación
El mismo `message_id` dos veces no debe ejecutar dos veces.

### P08 — Concurrencia
Mensajes simultáneos sin corrupción de estado.

### P09 — Bypass Graphify
Debe resultar imposible o ser rechazado.

### P10 — Contradicción
Mensajes incompatibles deben detectarse y no resolverse mediante invención.

### P11 — WILLIAM-SCY-01
Debe observar/contrastar/informar y no adquirir ejecución operativa por defecto.

### P12 — Caída de Carla
Debe existir comportamiento seguro.

### P13 — Caída de Graphify
No debe existir bypass.

### P14 — Integridad de auditoría
Intentos de UPDATE/DELETE deben ser rechazados cuando el modelo exige append-only.

### P15 — Escalada masiva
Probar el comportamiento ante volumen elevado y repetición.

---

# 12. MATRIZ CANON → n8n

Debes utilizar como contrato de reconciliación:

`06_SISTEMA_OPERATIVO/MATRIZ_CANON_N8N_SCI_v1.0.md`

No cierres una discrepancia simplemente porque el workflow funcione.

Una implementación puede funcionar técnicamente y seguir estando en deriva arquitectónica.

---

# 13. REGLA DE NO INVENCIÓN

Está prohibido:

- crear nuevos nodos canónicos;
- cambiar pertenencias;
- cambiar jurisdicciones;
- crear nuevas autoridades;
- renombrar entidades por comodidad;
- convertir infraestructura en nodo;
- completar campos faltantes mediante inferencia;
- convertir una hipótesis en regla;
- convertir una propuesta en implementación;
- convertir una implementación en canon;
- modificar el canon desde n8n.

Cuando encuentres una contradicción:

> **DETÉN → REGISTRA → ELEVA.**

---

# 14. CRITERIO DE SALIDA

El SCI podrá pasar de PRE-PILOTO a PILOTO únicamente cuando:

1. No existan P0 en estado `DERIVA`, `AUSENTE`, `PENDIENTE_DE_DECISION_SOBERANA` o `PENDIENTE_DE_EVIDENCIA` sin excepción explícita del Soberano.
2. Graphify esté nombrado y tratado canónicamente.
3. Hermes tenga implementada su jurisdicción de supervisión operativa.
4. WILLIAM-SCY-01 tenga implementada su función de contraste soberano independiente.
5. Carla permanezca fuera de la ontología de agentes n8n salvo decisión soberana explícita.
6. Identidad, autenticación y autorización estén demostradas.
7. Idempotencia y correlación estén demostradas.
8. Auditoría esté demostrada.
9. Kill Switch y PILOT MODE estén demostrados.
10. Las pruebas SCI-01 estén ejecutadas y registradas.

## REGLA FINAL

> **NO BUSQUES QUE EL SCI FUNCIONE A CUALQUIER PRECIO. BUSCA DEMOSTRAR QUE FUNCIONA SIN TRAICIONAR EL CANON.**

> **Si para hacer que funcione necesitas inventar, reinterpretar, ocultar, completar o saltarte una regla canónica, no lo hagas. Detén la ejecución y eleva la discrepancia.**
