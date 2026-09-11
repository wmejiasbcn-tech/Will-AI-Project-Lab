# G3 — Estudio de viabilidad v2

**Fecha de corte:** 2026-09-11  
**Clasificación:** I+D+I+e+A / hipótesis experimental  
**Dictamen provisional:** 🟡 INDETERMINADO  
**Canonización:** NO  
**Implementación autorizada por este documento:** NO

## 1. Pregunta de investigación

¿Necesita WAIPL una capa formal que relacione, bajo garantías comunes y fail-closed, **estructura + validez temporal + acto/atestación + identidad/autorización + evidencia**, permitiendo reconstrucción histórica y evitando afirmaciones cuando una de las garantías necesarias no puede demostrarse?

La hipótesis G3 no se justifica por «tener otro grafo», «tener otra capa de verdad» ni por duplicar capacidades ya existentes.

## 2. Genealogía y composición conceptual

El artefacto experimental de Aether es el antecedente concreto del estudio. El modelo conceptual trabajado en I+D+I+e+A distingue tres órganos:

- **Graphy:** qué existe y cómo está estructurado/relacionado.
- **Utópico:** qué fue/está siendo válido y cuándo.
- **Acta:** qué ocurrió/está ocurriendo, quién actuó y con qué derecho/autoridad.

G3 no debe confundirse con Graphy, Graphify, SCI, VÁR, YATA, Arnés, Positrón ni ALNIRA. VÁR y YATA pueden consumir/relacionarse con G3 sin convertirse en G3.

## 3. Reglas conceptuales registradas

1. Graphy no escribe hechos ni permisos.
2. Utópico es el órgano conceptual que cierra validez temporal.
3. Acta es el órgano conceptual que atestigua actos; no sobrescribe validez.
4. SpiceDB, cuando se use en el modelo, representa autorización actual; la validez histórica requiere una capa temporal independiente.
5. `INFERRED` no se convierte automáticamente en hecho.
6. Un span/registro de actividad no se convierte automáticamente en hecho de validez.
7. No se deben unificar físicamente los tres almacenes sólo para simplificar consultas.
8. Las consultas G3 deben fallar cerradas si falta una garantía necesaria o existen conflictos.
9. Los agentes no deben acceder directamente a órganos internos sin la capa de consulta/gobernanza correspondiente.
10. G3 no es un RAG.
11. G3 es portable como protocolo conceptual, pero la soberanía WAIPL no se transfiere con él.

## 4. Modelo conceptual de consulta

La hipótesis trabajada incluye un contexto equivalente a:

- `principal`
- `on_behalf_of`
- capability/biscuit atenuado
- `as_of`
- órganos consultados
- claves de correlación como `source_uri`, `entity_id`, `symbol_id`, `workflow_id`/`trace_id`

El resultado esperado sería un recibo compuesto que permita enlazar evidencia de Utópico, ruta/estructura de Graphy y trazabilidad de Acta. Si no puede demostrarse la cadena necesaria, la respuesta no debe presentarse como afirmación garantizada.

## 5. Estado real de WAIPL que afecta a la hipótesis

### Graphy / Graphify

Graphy 1.0 aparece en la documentación actual como cerrado y validado. Graphify dispone de un circuito de representación/ingesta con provenance, `built_at_commit`, 86 nodos gráficos, 59 aristas y 12 hiperaristas, además de agentes operativos inyectados. Esto cubre con mucha fuerza la dimensión de estructura y representación relacional.

Importante: los 86 elementos de Graphify no alteran el censo canónico del ecosistema, que continúa siendo **46 nodos**.

### VÁR

VÁR ya existe como capacidad materializada en n8n: `VÁR — VAC-01 — Validación de la Verdad Canónica WAIPL`, workflow `HC1SkjGphGYS3P8M`. El estado documentado es `DRAFT — NO PUBLICADO — AUTORIZACIÓN PENDIENTE`.

Por tanto, VÁR debe contabilizarse como capacidad existente/materializada, pero no debe presentarse como servicio publicado/operativo plenamente desplegado mientras su estado siga siendo DRAFT.

VÁR reduce de forma significativa el supuesto espacio de necesidad de G3 en validación de afirmaciones, pero no demuestra por sí solo temporalidad histórica formal, autorización histórica, atestación de actos o triple join fail-closed.

### YATA

YATA mantiene la jurisdicción de auditoría de validadores. No audita VÁR. Su implementación operacional completa no queda demostrada por la mera definición arquitectónica.

### Arnés

El repositorio acredita componentes mínimos: carga/validación de Guide y un sensor mínimo de feedback. También existe contrato SCI ↔ Arnés. El runtime feedforward completo continúa siendo un punto que requiere validación física si se quiere usar como garantía operacional.

### Positrón / Ollama

Positrón constituye la capa Runtime/centro operativo previsto del Arnés y Ollama la infraestructura local de ejecución. Esto aporta una base real para ejecución y continuidad, pero no sustituye las garantías epistemológicas/históricas específicas que investiga G3.

### SCI / Emily / Hermes

SCI existe como sistema de comunicación interna; Emily actúa como sinapsis/puente y Hermes como dirección operativa/comunicaciones. Son capacidades reales de comunicación, coordinación y gobierno operativo, pero no deben reinterpretarse automáticamente como un ledger histórico de actos G3.

### Will App / Knowledge Layer

Will App dispone actualmente de arquitectura de conocimiento, dominios diferenciados, provenance, versionado, retrieval gobernado, Evidence Assessment, Context Builder/Packet y circuitos diferenciados de Kairos/Dike. Esto cubre una parte importante de conocimiento, evidencia y trazabilidad.

La Fase 4 del RAG está implementada y probada en simulación, con validación de infraestructura real pendiente. Esto debe conservarse como distinción de estado.

## 6. Matriz de eliminación provisional

| Garantía investigada | Cobertura actual | Estado del contraste |
|---|---|---|
| Estructura relacional | Graphy/Graphify | 🟢 fuerte; G3 no puede justificarse por esto |
| Representación/provenance | Graphify + circuitos documentales | 🟢/🟡 según dominio |
| Validación de afirmaciones | VÁR | 🟡 materializado; publicación/operación plena pendiente |
| Auditoría de validadores | YATA | 🟡 definido; operación completa no demostrada |
| Validez temporal formal | capacidades distribuidas/versionado | 🟡 posible gap |
| Autorización histórica | capacidades distribuidas | 🟡 posible gap |
| Atestación formal de actos | logs/workflows/actas distribuidos | 🟡 posible gap |
| Triple join estructura-valididad-acto | no acreditado como mecanismo único | 🔴 gap potencial |
| Receipts compuestos | distribuidos/parciales | 🔴 no acreditado como garantía G3 |
| Fail-closed integral | varias capas parciales | 🟡 no acreditado como propiedad G3 |
| Consulta histórica `as_of` integral | no acreditada | 🔴 gap potencial |

## 7. Falsación

La hipótesis G3 debe poder morir.

Será **NO-GO** si se demuestra que WAIPL ya proporciona las garantías anteriores con alcance equivalente, persistencia equivalente, autoridad equivalente, evidencia equivalente y comportamiento ante fallo equivalente, aunque estén distribuidas entre varios órganos.

Será **GO para PoC** sólo si aparece una garantía no cubierta que sea relevante, recurrente y suficientemente diferencial como para justificar una prueba experimental.

## 8. Dictamen a 2026-09-11

**INDETERMINADO.**

No por falta de información, sino porque el contexto actual demuestra cobertura fuerte de estructura, conocimiento, provenance, validación y comunicación, mientras permanece sin resolver si existe una garantía sistémica adicional en la combinación formal de temporalidad + autorización histórica + acto/atestación + triple correlación + fail-closed.

## 9. Próximo hito autorizado metodológicamente

Antes de construir G3: **auditar el artefacto real de Aether garantía por garantía y comparar cada garantía contra WAIPL actual**.

No se debe crear un nodo G3, desplegar infraestructura G3 ni alterar órganos canónicos como consecuencia de este informe.
