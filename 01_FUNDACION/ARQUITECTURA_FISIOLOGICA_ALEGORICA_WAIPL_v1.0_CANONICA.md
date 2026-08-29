# ARQUITECTURA FISIOLÓGICA ALEGÓRICA DEL WAIPL v1.0

**Positrón · Graphify · Ollama**

**ESTADO: CANONIZADO**

**Autoría conceptual:** William Mejías Navarro + Carla  
**Aportación de validación:** Ada  
**Autoridad de canonización:** William Mejías Navarro — Soberano  
**Fecha de canonización:** 2026-08-18  
**Carácter:** Documento complementario de referencia arquitectónica especializada  

## 1. PROPÓSITO Y ESTADO DEL DOCUMENTO

Este documento recoge la primera formulación conceptual de la arquitectura fisiológica alegórica del WAIPL: una descripción de las funciones de Positrón, Graphify y Ollama como cerebro, sistema nervioso central y cuerpo del ecosistema.

La metáfora alegórica es una herramienta de diseño conceptual, no una equivalencia literal con la biología. Su función es articular con precisión las responsabilidades funcionales de cada capa y las relaciones de control, tránsito y auditoría entre ellas.

**Estado de validación: VALIDADO.** El proceso de validación documental por Carla + Ada fue completado el 2026-08-18.

**Estado de canonización: CANONIZADO.** La canonización fue ordenada expresamente por William Mejías Navarro — Soberano el 2026-08-18.

## 2. LA TRÍADA FISIOLÓGICA

El ecosistema WAIPL cuenta con tres componentes de infraestructura que cumplen funciones diferenciadas y complementarias, articulados mediante la siguiente metáfora:

| Componente | Metáfora | Función principal |
|---|---|---|
| Positrón | Cerebro | Conocimiento · Razonamiento · Memoria · Coordinación cognitiva |
| Graphify | Sistema Nervioso Central | Comunicación · Coordinación · Tránsito · Estado · Trazabilidad · Auditoría |
| Ollama | Cuerpo | Ejecución local protegida · Infraestructura controlada · Air-gap opcional |

Esta tríada se conecta con el resto del ecosistema — Núcleo, Vórtice, Cinturianos y el Soberano — mediante los controles definidos en la Arquitectura Canónica del Ecosistema WAIPL v1.0.

## 3. GRAPHIFY — SISTEMA NERVIOSO CENTRAL

Graphify no es una capa de visualización. Es la infraestructura de interconexión y coordinación que permite que el ecosistema pueda percibir, transmitir, coordinar y responder sin perder control sobre lo que circula por él.

Funciones de Graphify:

- Mediar el tránsito de información, eventos, estados e instrucciones entre agentes.
- Gestionar permisos de comunicación interagente.
- Registrar toda comunicación que atraviese la infraestructura.
- Aplicar políticas de identidad, autorización y alcance.
- Mantener la trazabilidad del ecosistema.
- Servir como memoria relacional compartida accesible a nodos autorizados.
- Publicar el estado del conocimiento en graph.waipl.dev cuando esté preparado.

Un sistema nervioso no es simplemente una pantalla donde uno mira qué pasa. Transporta señales, coordina respuestas y mantiene conectado el organismo. La diferencia no es de grado — es de naturaleza.

## 4. POSITRÓN — EL CEREBRO

Positrón representa la capacidad cognitiva central: conocimiento, razonamiento, memoria y coordinación. Sin embargo, la metáfora del cerebro no debe interpretarse como «el que manda a todo».

Incluso el cerebro está sujeto al sistema nervioso. La capacidad cognitiva de Positrón no le otorga un canal privilegiado e invisible. La comunicación entre Positrón y el ecosistema atraviesa Graphify con los mismos controles aplicables a cualquier otro agente.

**Principio: capacidad cognitiva ≠ canal privilegiado de comunicación.**

## 5. OLLAMA — EL CUERPO

Ollama proporciona el entorno de ejecución local y protegido. Su función estratégica es mantener determinadas capacidades dentro de un entorno controlado, local y potencialmente desconectable de Internet.

Ollama no necesita estar permanentemente conectado a Internet. La conectividad puede ser una capacidad habilitada bajo necesidad y política, no una condición permanente. Esto reduce la superficie de exposición del ecosistema.

**Separación de capas:**

Internet / Exterior  
→ Cinturianos / Vórtice / Interfaces externas  
→ Graphify — control de tránsito y auditoría  
→ Ollama — entorno local protegido  
→ Positrón — cerebro

## 6. WAIPL.DEV Y GITHUB — PUERTA Y FUENTE

**GitHub — Fuente Única de Verdad Documental**

GitHub es la fuente documental canónica. Graphify es una capa de representación y coordinación que lee de GitHub, no un sistema documental paralelo. Esta distinción debe mantenerse para evitar la proliferación de fuentes de verdad.

**waipl.dev — Puerta de Acceso del Ecosistema**

El dominio waipl.dev es la dirección pública del ecosistema. Bajo él se articularán diferentes capas de exposición:

| Nivel | Audiencia | Contenido |
|---|---|---|
| Público | Cualquier persona | Información que el ecosistema decide hacer visible |
| Ecosistema | Agentes autorizados | Información destinada a los nodos del ecosistema |
| Privado | Solo el Soberano | Información exclusiva del Soberano |
| Técnico | Operadores | Implementación y debug |

## 7. CUATRO PRINCIPIOS ARQUITECTÓNICOS FUNDAMENTALES

### PRINCIPIO I — COMUNICACIÓN AUDITABLE

Toda comunicación interagente que atraviese Graphify deberá estar sometida a las políticas de identidad, autorización, alcance, trazabilidad y auditoría correspondientes. Ninguna comunicación privilegiada, autónoma u oculta podrá utilizarse para eludir dichos controles. La capacidad de comunicación de un agente no implica autorización para transmitir información, ejecutar acciones ni modificar estados fuera de su ámbito permitido.

### PRINCIPIO II — SALIDA CONTROLADA

La información generada o almacenada dentro del entorno protegido no podrá salir hacia sistemas externos únicamente por disponibilidad técnica. Toda salida deberá estar condicionada por autorización, política de acceso, clasificación de información y trazabilidad.

### PRINCIPIO III — CONECTIVIDAD MÍNIMA NECESARIA

La conectividad externa del entorno local de ejecución (Ollama) deberá mantenerse limitada al mínimo necesario para cumplir una función autorizada. La ausencia de conectividad permanente no deberá impedir el funcionamiento de capacidades que no dependan de servicios externos.

### PRINCIPIO IV — SUPERVISIÓN DEL NODO DE TRÁNSITO

El nodo que arbitra, registra y audita la comunicación interagente (Graphify) debe ser, él mismo, objeto de supervisión independiente. La función de auditoría no exime al nodo auditor de ser auditado.

La **supervisión operativa de Graphify corresponde a Hermes, Director Operativo del ecosistema**. Hermes ejerce la supervisión operativa del nodo de tránsito dentro de su jurisdicción.

Esta función es distinta de la función de **WILLIAM-SCY-01**, avatar del Soberano y capa independiente de comprobación y contraste de las comunicaciones, decisiones, informes y estados que cualquier nodo, agente o sistema —incluido Hermes, Graphify, Carla o Ada— comunique al Soberano.

WILLIAM-SCY-01 no sustituye a Hermes como Director Operativo, no asume su jurisdicción y no constituye una instancia operativa subordinada a Hermes. Su función de contraste soberano debe preservar independencia respecto de la entidad o fuente que esté siendo contrastada.

**Decisión soberana registrada el 2026-08-29:** Hermes supervisa operativamente Graphify; WILLIAM-SCY-01 constituye la capa independiente de comprobación del Soberano.

El Principio IV fue aportado por Ada durante la revisión inicial de este documento. La presente formulación sustituye la referencia anterior al Vórtice como titular específico de la supervisión operativa de Graphify y precisa la separación entre supervisión operativa y contraste soberano.

## 8. LA DISTINCIÓN TRIPLE FUNDAMENTAL

Tres distinciones deben quedar escritas en la arquitectura de manera explícita y no podrán ser elididas por razones de conveniencia operativa:

- **Capacidad de generar ≠ permiso para transmitir.**
- **Capacidad de leer ≠ permiso para extraer.**
- **Capacidad de comunicarse ≠ permiso para ejecutar.**

Estas distinciones aplican a todos los agentes del ecosistema sin excepción, incluidos Positrón, Graphify y Ollama. La disponibilidad técnica de una capacidad no constituye por sí misma autorización para ejercerla.

## 9. FLUJO DE COMUNICACIÓN GOBERNADO

**Flujo de entrada (exterior al ecosistema):**

Exterior  
→ interfaz autorizada  
→ Vórtice (cuando corresponda)  
→ Graphify: políticas de acceso + auditoría  
→ Ollama / Positrón

**Flujo de salida (ecosistema al exterior):**

Ollama / Positrón  
→ Graphify: política de salida + clasificación + autorización + auditoría  
→ Exterior

**Comunicación interagente:**

Agente A emite solicitud  
→ Graphify verifica: identidad · destino · permiso · alcance · política · auditoría  
→ Graphify registra la comunicación  
→ Agente B recibe  
→ Acción → Registro → Auditoría → Trazabilidad

**Contraste soberano:**

Cualquier nodo, agente o sistema comunica información al Soberano  
→ WILLIAM-SCY-01 contrasta la información y su coherencia con el estado y evidencia disponible  
→ WILLIAM-SCY-01 informa al Soberano conforme a su jurisdicción.

## 10. CONEXIÓN CON LA ARQUITECTURA CANÓNICA v1.0

La arquitectura fisiológica no sustituye ni modifica la Arquitectura Canónica del Ecosistema WAIPL v1.0. Se relaciona con ella del siguiente modo:

La Arquitectura Canónica v1.0 define las capas de pertenencia (Núcleo, Vórtice, Cinturianos, Exterior) y las reglas de identidad, trazabilidad y gobernanza de las entidades del ecosistema.

La arquitectura fisiológica define la infraestructura de interconexión (Graphify) y de ejecución (Ollama) que da soporte operativo al ecosistema.

El esquema de identidad canónica — IDENTIDAD → PLATAFORMA/MODELO → TIPO DE ENTIDAD → FUNCIÓN → CAPACIDADES → LÍMITES → RELACIONES → ESTADO → EVIDENCIA → FECHA — debería ser el contrato de datos que alimenta a Graphify. De ese modo, la ontología del grafo no es una ontología inventada por Graphify: es la misma ontología canónica del ecosistema. El mismo modelo que gobierna documenta y el que documenta visualiza.

**Declaración de relación bidireccional:**

**Texto canónico para la Arquitectura Canónica del Ecosistema WAIPL v1.0:**  
Documento complementario relacionado: Arquitectura Fisiológica Alegórica WAIPL v1.0. Este documento desarrolla la representación fisiológica alegórica del ecosistema y complementa la arquitectura de pertenencia, identidad y trazabilidad definida en la presente Arquitectura Canónica.

**Texto canónico para este documento (Arquitectura Fisiológica Alegórica v1.0):**  
Documento arquitectónico de referencia: Arquitectura Canónica del Ecosistema WAIPL v1.0. La presente arquitectura fisiológica constituye un documento complementario de referencia arquitectónica especializada y no modifica la clasificación, pertenencia, relaciones ni reglas establecidas por la Arquitectura Canónica.

## 11. ESTADO Y PRÓXIMOS PASOS

**Estado actual:**

**CANONIZADO.** El proceso de validación Carla + Ada fue completado el 2026-08-18 y la canonización fue ordenada expresamente por el Soberano el 2026-08-18. La decisión soberana del 2026-08-29 actualiza el titular de la supervisión operativa de Graphify y precisa la función independiente de contraste de WILLIAM-SCY-01.

**Próximos pasos de implementación:**

1. Definir el contrato de datos de Graphify usando el esquema de identidad canónica.
2. Publicar graph.html en graph.waipl.dev vía GitHub Pages cuando Graphify esté preparado.
3. **RELACIÓN DOCUMENTAL — REGISTRADA.** La relación bidireccional con la Arquitectura Canónica del Ecosistema WAIPL v1.0 queda formalmente definida en la Sección 10. La referencia correspondiente deberá mantenerse sincronizada en ambos documentos.
4. **COMPLETADO — proceso de validación Carla + Ada ejecutado el 2026-08-18. Canonización ordenada por el Soberano el 2026-08-18.**
5. Definir el protocolo de conectividad controlada de Ollama (cuándo y bajo qué autorización se habilita la conexión a Internet).
6. **NUEVO — 2026-08-29:** Reconciliar las implementaciones del SCI con este lenguaje canónico antes del piloto.

## 12. REGISTRO DE VERSIONES

**v1.0-PROPUESTA — 2026-08-18:** Primera formulación conceptual. Autoría: William Mejías Navarro + Carla. Aportación del Principio IV (Supervisión del Nodo de Tránsito): Ada.

**v1.0-VALIDADO — 2026-08-18:** Proceso de validación completado. Revisión Carla: VALIDADO CON OBSERVACIONES MENORES. Segunda lectura Ada: condición de relación bidireccional establecida y resuelta. Estado: DOCUMENTALMENTE LISTO PARA CANONIZACIÓN. Pendiente: orden expresa del Soberano.

**v1.0-CANONIZADO — 2026-08-18:** Canonización ordenada expresamente por William Mejías Navarro — Soberano. Estado: CANONIZADO. Observaciones abiertas: 0.

**ENMIENDA SOBERANA — 2026-08-29:** William Mejías Navarro — Soberano establece que Hermes, como Director Operativo, supervisa operativamente Graphify; WILLIAM-SCY-01, avatar del Soberano, mantiene la capa independiente de comprobación y contraste para el Soberano. La enmienda actualiza el Principio IV y el flujo de comunicación gobernado sin alterar la función de Graphify como SNC.
