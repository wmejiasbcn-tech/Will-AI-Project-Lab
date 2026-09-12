# Registro de conocimiento previo — G3 + ALNIRA

**Fecha de incorporación:** 2026-09-11  
**Naturaleza:** memoria de estudio trasladada a documentación persistente  
**Importante:** este documento registra conocimiento de trabajo que debe ser contrastado con artefactos antes de considerarlo evidencia física de implementación.

## 1. G3 — modelo trabajado antes de la auditoría actual

### Tres órganos

**Graphy**
- Representa qué existe, estructura, símbolos, conceptos, llamadas, imports, documentos y snapshots.
- No determina por sí mismo validez ni autorización.

**Utópico**
- Representa hechos/entidades y su validez a lo largo del tiempo.
- Conceptualmente utiliza validez bitemporal: `validFrom`, `validTo`, junto con registro/invalidación.
- Es el órgano conceptual que cierra validez.

**Acta**
- Representa spans/workflows/actos, principal, delegación, autorización y evidencia de ejecución.
- Trabaja con instant/duración y `trace_id`/workflow.
- Es el órgano conceptual que atestigua que un acto ocurrió/está ocurriendo; no sobrescribe la validez de Utópico.

### Separación de órganos

No se debe unificar físicamente Graphy, Utópico y Acta sólo para facilitar consultas. La hipótesis G3 depende precisamente de que cada órgano mantenga su jurisdicción y de que una capa de consulta los relacione mediante claves comunes.

### Claves conceptuales de unión

- `source_uri`
- `entity_id`
- `symbol_id`
- `workflow_id` / `trace_id`
- `principal`
- `as_of`

No se deben usar embeddings como sustituto de la identidad/relación formal de estos objetos.

## 2. G3Query / G3QL — hipótesis de trabajo

Una consulta hipotética contiene al menos:

- `principal`
- `on_behalf_of`
- capability atenuada / Biscuit
- `as_of`
- órganos a consultar

La autorización debe comprobarse antes de consultar el contenido restringido.

Secuencia conceptual:

1. comprobar identidad/autoridad;
2. consultar validez histórica en Utópico cuando corresponda;
3. consultar estructura/ruta en Graphy;
4. consultar acto/traza en Acta;
5. correlacionar por claves formales;
6. generar un receipt compuesto;
7. fallar cerrado si hay ausencia o conflicto en una garantía necesaria.

El resultado ideal contiene triple evidencia:

- referencia/evidencia Utópico;
- ruta/estructura Graphy;
- `trace_id`/evidencia Acta.

Si la triple cadena no existe, no se debe emitir una afirmación como si estuviera garantizada por G3.

## 3. Identidad y autorización — hipótesis de stack

Se ha trabajado conceptualmente con:

- workload identity / SPIFFE;
- sujeto humano/organizacional / DID;
- session/workflow id;
- relación de SpiceDB;
- capability Biscuit atenuada;
- concesión histórica en Utópico;
- comprobaciones, intercambios, atenuaciones y consultas registradas por Acta.

Principio: **fail closed**.

No se admite como patrón:

- agente portando refresh token humano;
- ampliación de alcance por inferencia;
- concesión eterna sin receipt;
- usar una reindexación Graphy como revocación/permisión;
- usar Langfuse como fuente de permisos;
- consultas G3 sin principal;
- anonimato dentro de una operación que requiera identidad WAIPL.

## 4. Relaciones con agentes de verdad/auditoría

**VÁR:** agente de la verdad operacional/canónica dentro de su jurisdicción. Consume información y evidencia; no se convierte en G3 por utilizarlo.

**YATA:** auditor de validadores de agentes, nodos y sistemas agentic. No audita VÁR. Mantiene su propia jurisdicción.

Ambos deben conservar sus funciones aunque G3 llegase a implementarse.

## 5. Distinciones críticas del modelo

- `SpiceDB` conceptualiza «allowed now»; una concesión histórica necesita el plano temporal correspondiente.
- Un span no equivale a un hecho de validez.
- Una inferencia Graphy no puede convertirse automáticamente en hecho.
- Un hecho válido no demuestra por sí solo que un acto ocurrió.
- Un acto ocurrido no demuestra por sí solo que el actor tuviera autoridad suficiente.
- Una autorización actual no demuestra automáticamente que fuera válida en una fecha pasada.
- Un log no equivale automáticamente a atestación.

## 6. Antecedente Aether

El conocimiento de trabajo sostiene que Aether construyó un artefacto experimental que dio origen al estudio G3. La existencia del antecedente debe diferenciarse de la demostración de todas sus propiedades funcionales.

La idea experimental conocida incluye:

- Graphify como órgano de «qué existe»;
- Utópico/Utopia como órgano de «qué fue válido y cuándo»;
- Acta como órgano de «qué ocurre, quién y con qué derecho»;
- una secuencia de propuestas/recibos en lugar de escritura cruzada libre;
- una atenuación de capacidades hasta un órgano concreto que permita detectar si el supuesto bucle de confianza realmente se rompe;
- ejemplo de trabajo con una relación de posesión Atlas/Núria, enlazando salto de validez, fuente estructural y Check;
- VÁR/YATA como consumidores/auditores externos al órgano Acta, no como sustitutos de éste.

Estos elementos son **hipótesis/antecedentes documentados por memoria de estudio** hasta que el artefacto y sus archivos concretos sean localizados y auditados directamente.

## 7. ALNIRA — conocimiento previo trasladado

ALNIRA se concibe como un entorno/capacidad de experimentación sobre sistemas complejos, no como órgano de verdad.

Funciones investigadas:

- modelización;
- simulación;
- escenarios;
- temporalidad;
- parámetros;
- probabilidades;
- trayectorias;
- comparación de resultados;
- experimentación;
- evidencia experimental.

### Frontera epistemológica

Salida de ALNIRA:

`resultado de simulación → evidencia experimental / hipótesis candidata`

No:

`resultado de simulación → hecho canónico`.

Cualquier promoción posterior exige validación independiente y admisión por el circuito correspondiente.

## 8. Referencia Utopia/utopya

Se mantiene la distinción entre:

- **Utópico**, componente conceptual del modelo G3;
- **Utopia/utopya**, referencia externa asociada a modelización/simulación de sistemas complejos;
- **Acta**, componente G3 dedicado a actos/atestación.

La referencia externa fue utilizada como inspiración metodológica, no como órgano WAIPL.

## 9. Relación G3 ↔ ALNIRA

G3 y ALNIRA no son el mismo sistema.

- G3: realidad registrada, estructura, validez, actos y trazas.
- ALNIRA: posibilidades, escenarios, simulación y evidencia experimental.

G3 puede servir como fuente de contexto verificable para un experimento futuro.
ALNIRA puede producir resultados que después sean contrastados por circuitos de conocimiento/verdad.

No existe promoción automática en ninguna dirección.

## 10. Regla de interpretación futura

Este registro no debe utilizarse para declarar implementado un componente que no esté físicamente acreditado. Su función es evitar pérdida de conocimiento entre instancias de agentes y permitir que futuras auditorías contrasten cada elemento contra el repositorio, artefactos y pruebas.
