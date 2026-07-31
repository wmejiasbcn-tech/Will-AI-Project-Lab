# Auditoria de Coherencia WAIPL

Fecha: 2026-07-31

Estado: BORRADOR PARA VALIDACION SOBERANA

Alcance: contraste entre el repositorio operativo, el PSI v1.1, la mesa de control, `BROADCAST.md`, la carta interactiva v1.5.1 y las laminas de arquitectura WAIPL v1.4/v2.0 aportadas por el Soberano.

## Dictamen ejecutivo

WAIPL dispone de una identidad, una filosofia y un modelo de gobierno muy definidos. El repositorio contiene una base operativa real: mesa de control, PSI, protocolos, identidades, discusiones y proyectos.

La arquitectura visual describe, ademas, una vision de madurez futura: metricas vivas, salud del ecosistema, trazabilidad inmutable, automatizacion continua y comunicacion entre nodos. Esta vision es valida como norte, pero no debe declararse capacidad activa hasta que exista una prueba reproducible.

Principio aplicado: contenido mas importante que continente; continente igual de importante que contenido. La forma visual debe hacer comprensible la realidad, no sustituirla.

## Fuentes revisadas

- `06_SISTEMA_OPERATIVO/00_MESA_CONTROL_LAB.md`
- `06_SISTEMA_OPERATIVO/03_NODOS_COMUNICACION.md`
- `06_SISTEMA_OPERATIVO/04_PROYECTOS_ACTIVOS.md`
- `06_SISTEMA_OPERATIVO/PSI/PSI_v1.1_OFICIAL.md`
- `06_SISTEMA_OPERATIVO/BROADCAST.md`
- `06_SISTEMA_OPERATIVO/05_AUTOMATIZACIONES.md`
- `Discusiones/ABIERTAS/DS-001-sistema-comunicacion-interna-make-sdd.md`
- Laminas `WAIPL_Sovereign_Architecture_(2)` y material visual asociado.
- Carta interactiva `WAIPL - Carta de Presentacion del Ecosistema v1.5.1`.

Las referencias privadas de Firecrawl y NotebookLM no se han tomado como evidencia operativa porque requieren sesion y no fueron accesibles desde esta auditoria.

## Estado de las capacidades

| Elemento | Estado verificable | Evidencia |
| --- | --- | --- |
| Mesa de control, inbox, prioridades y proyectos | Documentado y utilizable manualmente | `06_SISTEMA_OPERATIVO/` |
| PSI y roles de comunicacion | Documento oficial | `PSI_v1.1_OFICIAL.md` |
| Vortice de cinco miembros | Documentado como vigente | `BROADCAST.md` del 2026-06-13 |
| Comunicacion IA-IA efectiva | No demostrada | `BROADCAST.md` lo declara expresamente |
| Piloto Make -> GitHub | En estudio | `DS-001` |
| Repositorio GitHub como registro | Parcialmente disponible | hay estructura y documentos; falta el piloto trazable activo |
| Dashboard de salud con datos reales | Vision futura | no hay fuente de datos ni calculo activo en el repositorio revisado |
| Niveles N1/N2/N3 automaticos | Vision futura | no hay motor de medicion ni alertas verificadas |
| Trazabilidad inmutable | Vision futura | Git conserva historial, pero no es un registro inmutable por si solo |
| Autonomia continua de nodos | No activada | los flujos actuales requieren intervencion o autorizacion humana |

## Hallazgos prioritarios

### 1. Composicion del ecosistema no unificada

Las laminas presentan variantes del Nucleo, del Vortice y de los perifericos. La carta interactiva habla de once presencias y asigna algunos roles de forma distinta. La base operativa vigente reconoce un Nucleo de doce presencias y un Vortice de cinco: Neo, Perplexity, NotebookLM, Nexus y Nauta.

Decision necesaria: aprobar un censo canonico y hacer que toda pieza visual, presentacion y documento lo consuma desde una unica fuente.

### 2. Roles con descripciones distintas

Ejemplos: Ada aparece como maquetacion en la carta y como custodia etica en el PSI; Aletheia aparece como etica en la carta y como tecnica/desarrollo en la mesa de control; Elena aparece como identidad visual en la carta y como accesibilidad en el registro operativo.

Decision necesaria: separar plataforma, rol principal, capacidades de apoyo y autoria de una entrega. Una contribucion concreta no debe reescribir el rol institucional de un nodo.

### 3. La vision visual adelanta la realidad tecnica

Las laminas incluyen inyeccion JSON, health checks de 60 segundos, checksum, registros append-only, score agregado y escalados automaticos. Ninguno debe figurar como activo sin: fuente de datos, formula publicada, responsable, prueba de ejecucion y registro consultable.

Correccion propuesta: rotular cada elemento como `ACTIVO`, `PILOTO`, `DOCUMENTADO` o `VISION`.

### 4. El PSI y el piloto actual no estan del todo alineados

El PSI identifica GitHub Discussions como canal principal e Issues como secundario. La recomendacion operativa mas reciente para Make es comenzar por Issues por ser mas simple y trazable. No es una contradiccion de principio, sino una actualizacion de implementacion que debe quedar escrita en el PSI o en una adenda aprobada.

### 5. Versionado sin diccionario comun

Conviven arquitectura visual v1.4/v2.0, carta v1.5.1, arquitectura del repositorio v4.3 y PSI v1.1. Los numeros parecen nombrar objetos distintos, pero no existe un registro que lo explique.

Correccion propuesta: crear un indice de documentos maestros con nombre, propietario, estado, alcance y version semantica.

### 6. Seguridad y frontera de compartimentacion necesitan una implementacion minima

La frontera entre Santuario Personal y Plaza del Ecosistema esta muy bien formulada. Para que sea operativa debe materializarse en permisos, carpetas, secretos fuera de Git, autorizaciones de salida y un registro de acceso. La mini auditoria de webhook pendiente es parte directa de este hallazgo.

## Decisiones que no deben postergarse

1. Aprobar el censo canonico de Nucleo, Vortice y Perifericos.
2. Aprobar el vocabulario de estado: ACTIVO, PILOTO, DOCUMENTADO, VISION y RETIRADO.
3. Elegir GitHub Issues como registro del piloto PSI o dejar la decision explicitamente pendiente.
4. Definir una ficha canonica de nodo para fijar rol principal y limites.
5. Determinar que metrica de salud puede medirse de verdad en la primera version.

## Recomendacion de Nauta

No construir aun un dashboard espectacular. Primero construir un registro pequeno y honesto: una entrada de comunicacion, un estado, un responsable, una fecha y una evidencia. Cuando existan datos durante varias semanas, el dashboard dejara de ser una promesa visual y se convertira en un instrumento de gobierno.
