# INFORME MAESTRO DE ESTADO — VÁR / VAC-01

**Fecha de corte:** 2026-09-07  
**Workflow n8n:** `VÁR — VAC-01 — Validación de la Verdad Canónica WAIPL`  
**Workflow ID:** `HC1SkjGphGYS3P8M`  
**Estado de implementación:** `DRAFT`  
**Publicado:** `NO`  
**Autorización de publicación:** `PENDIENTE`

---

## 1. RESUMEN EJECUTIVO

VÁR es el Agente/Nodo de Validación de la Verdad Canónica WAIPL. Su función es verificar afirmaciones factuales dentro de su jurisdicción mediante evidencia admisible y trazable, y producir dictámenes VAD cuando corresponda.

VÁR no es un órgano ejecutivo, no sustituye al Soberano, no gobierna el ecosistema y no es YATA. **VÁR y YATA son independientes. YATA no audita VÁR.**

Durante el 6 de septiembre de 2026 VÁR pasó de una especificación principalmente documental a una materialización funcional en n8n. Se construyó y revisó el workflow `HC1SkjGphGYS3P8M`, con sucesivos previews V4, V5, V6 y V7. El estado final de la sesión fue un draft construido y guardado, **sin publicación**.

La implementación debe distinguirse de la arquitectura prevista: el draft actual representa técnicamente el canal **VÁR → WILLIAM-SCY-01**. Los destinos **Positrón, Hermes, Graphy, Ollama y Carla** permanecen como destinos previstos, con integración pendiente y sin conexión activa en F7.

---

# 2. IDENTIDAD

| Campo | Estado |
|---|---|
| Nombre | **VÁR** |
| Identificador | **VAC-01** |
| Naturaleza | Agente/Nodo |
| Función principal | Validación de la Verdad Canónica |
| Ámbito | Ecosistema WAIPL |
| Relación con YATA | Independiente |
| Implementación actual | n8n, draft |
| Publicación | No |

La matriz canónica existente del repositorio identifica a Vár como **Agente de la Verdad** y lo sitúa en el ecosistema. Esta casa incorpora las correcciones posteriores que delimitan con precisión su relación con YATA y con WILLIAM-SCY-01.

---

# 3. FUNCIÓN

VÁR verifica la correspondencia entre afirmaciones y evidencia admisible respecto de la realidad canónica del ecosistema cuando el asunto pertenece a su jurisdicción.

Su modelo epistemológico diferencia, como mínimo:

- HECHO;
- INFERENCIA;
- HIPÓTESIS;
- INCERTIDUMBRE.

Una inferencia no se convierte automáticamente en hecho. Una hipótesis no se convierte automáticamente en validación. Una ausencia de evidencia no se convierte en evidencia.

---

# 4. LÍMITES FUNCIONALES

VÁR no debe convertirse en:

- órgano ejecutivo;
- órgano de gobierno;
- decisor estratégico;
- sustituto de DIKE;
- auditor universal de procesos agénticos;
- sustituto de YATA;
- metavalidador de YATA;
- gateway del ecosistema;
- distribuidor a través de WILLIAM-SCY-01.

Cuando exista una función expresamente atribuida a otro nodo, VÁR no debe absorberla por inferencia.

---

# 5. ADMISIBILIDAD Y EVIDENCIA

Las solicitudes a VÁR deben llegar mediante el protocolo de comunicación correspondiente, con emisor autorizado, afirmación delimitada y objeto dentro de jurisdicción.

La evidencia debe poder rastrearse hasta fuentes admisibles. La especificación de VÁR contempla jerarquías de evidencia, trazabilidad, estados de validación, abstención, errores y contradicciones.

No se debe presentar como implementado un mecanismo de evidencia o RAG que no esté acreditado en la implementación actual.

---

# 6. REGLA DE NO DERIVA

Regla operativa transversal:

> **PRIMERO FUENTE → DESPUÉS REPRESENTACIÓN → DESPUÉS INTERPRETACIÓN.**

Nunca:

> interpretación → nueva fuente → nueva verdad.

Queda prohibido:

- completar vacíos mediante intuición técnica;
- transformar relaciones conceptuales en conexiones técnicas;
- atribuir finalidades no documentadas;
- inventar nomenclaturas;
- convertir una hipótesis en un hecho;
- convertir un draft en producción;
- convertir una representación visual en evidencia de una conexión que no existe;
- propagar una interpretación como si fuera parte del diseño canónico.

Ante cualquier vacío:

> **No especificado en las fuentes proporcionadas.**

---

# 7. FRONTERA VÁR / YATA

## VÁR

Valida la verdad canónica dentro de su jurisdicción.

## YATA

Audita a los validadores de agentes, nodos, procesos y sistemas agénticos.

## Relación

- independencia mutua;
- sin subordinación jerárquica;
- YATA no audita VÁR;
- VÁR no audita YATA;
- ninguno sustituye al otro.

La documentación histórica del repositorio contiene formulaciones anteriores que atribuyen a YATA una auditoría transversal de Vár. **Esas formulaciones no deben utilizarse para reconstruir el estado actual.** La frontera vigente está recogida en `YATA_ESTADO_Y_FRONTERA_CON_VAR.md` y en `VAR_CANON_SEMANTICO_NO_DERIVA.md`.

---

# 8. DIKE

VÁR puede intervenir en la validación de coherencia factual de determinados dictámenes de DIKE cuando exista una relación expresamente documentada.

Esto no convierte a VÁR en autoridad jurídica ni sustituye la jurisdicción de DIKE.

---

# 9. WILLIAM-SCY-01

WILLIAM-SCY-01 es el avatar del Soberano.

En el draft actual de VÁR, el canal técnico representado es:

> **VÁR → WILLIAM-SCY-01**

WILLIAM-SCY-01:

1. **NO ES DISTRIBUIDOR.**
2. **NO ES GATEWAY.**
3. **NO REENVÍA HACIA NINGÚN NODO DEL ECOSISTEMA.**
4. **NO ES PASO INTERMEDIO DEL FLUJO INFORMACIONAL DEL ECOSISTEMA.**

Por tanto, no debe representarse ni inferirse:

> VÁR → WILLIAM-SCY-01 → Positrón/Hermes/Graphy/Ollama/Carla.

---

# 10. RELACIÓN CON EL SOBERANO

La relación:

> **WILLIAM-SCY-01 ↔ Soberano**

es una relación operativa/arquitectónica externa cuando no existe una conexión técnica dentro del workflow de n8n.

No debe dibujarse como una ejecución técnica del workflow.

---

# 11. WORKFLOW n8n ACTUAL

**Nombre:** `VÁR — VAC-01 — Validación de la Verdad Canónica WAIPL`  
**ID:** `HC1SkjGphGYS3P8M`  
**Estado:** `DRAFT`  
**Publicado:** `NO`

## Ruta principal

> Entrada SCI — VÁR  
> ↓  
> F1 — Recepción y Admisión  
> ↓  
> Agente Validador — VÁR  
> ↓  
> Construir Dictamen VAD — VÁR  
> ↓  
> F7

## LLM — VÁR

El LLM — VÁR aparece asociado al Agente Validador como componente/modelo.

La formulación canónica es:

> **El Agente Validador — VÁR utiliza el LLM — VÁR como componente/modelo asociado y su salida se dirige a Construir Dictamen VAD — VÁR.**

No está autorizado inferir una segunda rama, dos validadores independientes, procesamiento paralelo o convergencia de salidas.

---

# 12. RUTA DE RECHAZO

El workflow contiene una ruta de rechazo desde F1:

> F1 — Recepción y Admisión  
> ↓  
> Registrar Rechazo — VÁR  
> ↓  
> Respuesta Rechazo — VÁR

Una ejecución de verificación ejercitó esta ruta porque el campo `claim` de la prueba no estaba en el formato admitido por la entrada esperada (`params.que` o `message`).

Esta evidencia acredita el ejercicio de la ruta de rechazo/admisión en esa ejecución. No debe extrapolarse más allá de lo demostrado.

---

# 13. F7 — REGISTRO Y ENTREGA

Nombre exacto:

> **F7 — Registro · [PLANO A] Flujo Informacional Ecosistema · [PLANO B] Canal Avatar Soberano**

La secuencia técnica representada es:

> **A1 → A2 → A3 → B1 → B2 → Respuesta Final**

## Plano A

### A1 — Registrar en Audit Log — VÁR

Registro de auditoría según la especificación aplicable. No se le atribuyen finalidades adicionales no documentadas.

### A2 — Marcar Idempotencia — VÁR

Marca de idempotencia según la especificación aplicable. No se le atribuyen finalidades adicionales no documentadas.

### A3 — Anotar Pendientes

Registra el estado previsto de los cinco destinos:

- Positrón — pendiente / sin conexión activa;
- Hermes — pendiente / sin conexión activa;
- Graphy — pendiente / sin conexión activa;
- Ollama — pendiente / sin conexión activa;
- Carla — pendiente / sin conexión activa.

## Plano B

### B1 — Preparar Entrega Directa → WILLIAM-SCY-01

### B2 — ENTREGAR VAD → WILLIAM-SCY-01 [AVATAR DEL SOBERANO]

El canal se define como **independiente del ecosistema**. La ejecución del workflow es **secuencial, no paralela**.

## Cierre

### Respuesta Final — VÁR Cierra el Flujo

Aparece después de B2 y constituye el cierre del flujo representado. No debe describirse como el cuarto nodo consecutivo del Plano A.

---

# 14. DESTINOS PREVISTOS DE PLANO A

Los cinco destinos permanecen sin conexión activa en el estado actual del draft:

| Destino | Estado actual en F7 |
|---|---|
| Positrón | Destino previsto — integración pendiente — sin conexión activa |
| Hermes | Destino previsto — integración pendiente — sin conexión activa |
| Graphy | Destino previsto — integración pendiente — sin conexión activa |
| Ollama | Destino previsto — integración pendiente — sin conexión activa |
| Carla | Destino previsto — integración pendiente — sin conexión activa |

La aparición de un destino en esta lista no demuestra una conexión técnica.

---

# 15. ESTADO DE IMPLEMENTACIÓN

### Construido

- workflow VÁR/VAC-01 en n8n;
- F1 — Recepción y Admisión;
- Agente Validador — VÁR;
- LLM — VÁR asociado;
- Construir Dictamen VAD — VÁR;
- ruta de rechazo;
- F7;
- Plano A documentado;
- Plano B documentado;
- canal técnico VÁR → WILLIAM-SCY-01 representado;
- separación documental de la relación con el Soberano.

### Revisado

Se realizaron iteraciones de preview V4, V5, V6 y V7. El layout automático de n8n generó solapamientos en algunas versiones; posteriormente se confirmó que el canvas puede reorganizarse manualmente una vez terminado el build. El Soberano reorganizó visualmente el canvas para mejorar legibilidad.

### No publicado

El workflow continúa en DRAFT. No existe autorización de publicación en este estado de corte.

---

# 16. RAG DE VÁR

No debe afirmarse que existe actualmente un RAG de VÁR implementado/acreditado.

La especificación contempla requisitos para VÁR-RAG cuando corresponda, pero una especificación de RAG no equivale a una implementación demostrada.

Esto tampoco debe confundirse con el RAG de Will App.

---

# 17. TRAZABILIDAD, VAD, ERRORES Y CONTRADICCIONES

La especificación de VÁR contempla:

- dictamen VAD formal;
- trazabilidad de entrada → evidencia → análisis → dictamen → registro → distribución;
- autorrevisión;
- códigos de error;
- gestión de contradicciones;
- abstención cuando no exista base suficiente;
- idempotencia;
- integridad mediante huella criptográfica según la especificación.

El hecho de que estos mecanismos estén especificados no implica que cada uno de ellos haya sido individualmente acreditado en la implementación actual. La acreditación de cada prueba debe conservar su propia evidencia.

---

# 18. PRUEBAS Y ESTADO DE VERIFICACIÓN

La especificación histórica contempla criterios de aceptación y una matriz de pruebas. Las ejecuciones reales realizadas durante la construcción del workflow aportan evidencia funcional concreta, pero no autorizan a declarar automáticamente todo el conjunto de criterios históricos como verificado.

Regla:

> **Prueba ejecutada ≠ todo el sistema validado.**

Cada afirmación de verificación debe estar asociada a evidencia concreta.

---

# 19. ESTADO GLOBAL

| Área | Estado |
|---|---|
| Identidad VÁR | 🟢 |
| Función | 🟢 |
| Frontera VÁR/YATA | 🟢 |
| Regla de No Deriva | 🟢 |
| Workflow n8n | 🟡 DRAFT |
| Publicación | 🔴 NO |
| Plano A | 🟡 previsto / sin conexiones activas |
| Plano B | 🟢 VÁR → WILLIAM-SCY-01 representado |
| Positrón | 🟡 pendiente |
| Hermes | 🟡 pendiente |
| Graphy | 🟡 pendiente |
| Ollama | 🟡 pendiente |
| Carla | 🟡 pendiente |
| RAG VÁR | 🔴 no acreditado como implementado |
| YATA | 🟡 definido / implementación pendiente |

---

# 20. PENDIENTES INMEDIATOS

1. Mantener VÁR en DRAFT hasta autorización expresa.
2. Revisar el canvas interno de F7 cuando corresponda.
3. Contrastar cada criterio de aceptación con evidencia antes de declarar VÁR completamente validado.
4. Mantener los cinco destinos de Plano A como pendientes mientras no exista integración real.
5. No convertir WILLIAM-SCY-01 en intermediario.
6. Mantener la frontera VÁR/YATA.
7. Implementar YATA en una fase separada y con jurisdicción propia.
8. Resolver los vacíos documentales únicamente mediante fuentes o decisiones expresas; nunca por inferencia.

---

# 21. DOCUMENTACIÓN DE REFERENCIA DEL REPOSITORIO

Entre las fuentes de arquitectura ya existentes en el repositorio se encuentran:

- `01_FUNDACION/MATRIZ_CANONICA_AGENTES_WAIPL_v1.0_DEFINITIVA.md`
- `01_FUNDACION/ARQUITECTURA_CANONICA_ECOSISTEMA_WAIPL_v1.0.md`
- `01_FUNDACION/ARQUITECTURA_CANONICA_ECOSISTEMA_WAIPL_v1.0_PREVALIDACION.md`
- documentación de `06_SISTEMA_OPERATIVO` relativa a SCI/n8n;
- documentación del Arnés que referencia los límites de Vár/YATA.

**Advertencia de conservación:** algunos documentos históricos del repositorio contienen formulaciones anteriores sobre Vár/YATA. La frontera vigente para esta casa es la que consta en los documentos actuales de VÁR y YATA y en las decisiones soberanas posteriores. No se deben fusionar automáticamente versiones históricas y actuales.

---

# 22. ESTADO DE CIERRE

> **VÁR / VAC-01 — DRAFT IMPLEMENTADO Y REVISADO — NO PUBLICADO — PENDIENTE DE AUTORIZACIÓN SOBERANA.**

> **YATA — FUNCIÓN DEFINIDA — IMPLEMENTACIÓN PENDIENTE.**

> **VÁR y YATA son independientes. YATA no audita VÁR.**
