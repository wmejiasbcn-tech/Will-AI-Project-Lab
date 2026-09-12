# Matriz de trazabilidad — G3 + ALNIRA

**Fecha de corte:** 2026-09-11  
**Objetivo:** dejar constancia verificable del estado del estudio, de las fuentes utilizadas y de los límites de evidencia.

## 1. Punto de partida del expediente

La revisión se realizó contra el estado actual del repositorio principal y repositorios hermanos accesibles, no únicamente contra memoria conversacional. La rama de documentación parte de `main` en `565ef17f0acb4a3feef98d5e6d5b8289b5d5074c`.

## 2. Fuentes principales y función probatoria

| Fuente | Uso en este expediente | Estado relevante |
|---|---|---|
| `00_INDEX.md` | índice/censo y estructura documental | 46 nodos canónicos; repositorios hermanos |
| `01_FUNDACION/README.md` | fundación/arquitectura | Graphy y corpus fundacional |
| `01_FUNDACION/MATRIZ_CANONICA_AGENTES_WAIPL_v1.0_DEFINITIVA.md` | jurisdicciones de agentes | VÁR y demás roles |
| documentación Graphy/Graphify | estructura y provenance | Graphy 1.0; Graphify operativo/documentado |
| documentación Arnés | ejecución, carga, feedback, límites | piezas mínimas acreditadas; runtime completo pendiente |
| documentación VÁR | verdad canónica | workflow materializado; DRAFT/no publicado |
| `Agente-Will-App` | producto, interfaz y conocimiento | D1/D2, Knowledge Layer, dominios, provenance, RAG |
| auditoría de interfaz Will App | estado físico de interfaz | auditoría del 2026-09-07 |
| `positron` | Runtime/infraestructura | repositorio activo |
| `WAIPL-OS` | sistema operativo/documental | docs, memory, projects, protocols, templates |
| artefacto/estudio de Aether | antecedente experimental G3 | debe auditarse garantía por garantía |

## 3. Hechos y límites de inferencia

### H1 — 46 nodos

**Hecho:** el censo canónico del ecosistema continúa en 46.  
**No inferir:** el número de elementos gráficos de Graphify como nuevo censo.

### H2 — Graphy

**Hecho:** Graphy 1.0 aparece documentado como cerrado y validado.  
**Consecuencia:** no usar «falta de estructura relacional» como justificación de G3.

### H3 — Graphify

**Hecho:** existe circuito de Graphify con provenance, commit de construcción y representación gráfica.  
**Consecuencia:** la función estructural está fuertemente cubierta.

### H4 — VÁR

**Hecho:** existe materialización n8n `VÁR — VAC-01 — Validación de la Verdad Canónica WAIPL`, workflow `HC1SkjGphGYS3P8M`.  
**Estado:** DRAFT — NO PUBLICADO — AUTORIZACIÓN PENDIENTE.  
**Consecuencia:** VÁR debe contabilizarse como capacidad materializada, pero no como servicio plenamente publicado/operativo.

### H5 — YATA

**Hecho:** YATA tiene jurisdicción definida como auditor de validadores.  
**Límite:** no debe declararse operación plena sin evidencia de implementación/ejecución.

### H6 — Arnés

**Hecho:** hay evidencia de carga/validación de Guide y sensor mínimo de feedback; existe contrato SCI ↔ Arnés.  
**Límite:** el runtime feedforward completo requiere evidencia de ejecución/validación antes de atribuirle todas sus garantías.

### H7 — Will App

**Hecho:** el repositorio actual contiene arquitectura de interfaz, dominios, contexto, Knowledge Layer, provenance, versionado y retrieval gobernado.  
**Límite:** determinados niveles de operación del RAG dependen de infraestructura real pendiente.

### H8 — Fase 4 RAG

**Hecho:** implementación y pruebas en simulación documentadas.  
**Límite:** validación de infraestructura real pendiente.

### H9 — Positrón/Ollama

**Hecho:** existen como infraestructura/capa de ejecución del ecosistema.  
**Límite:** no atribuirles por extensión garantías epistemológicas que no estén demostradas.

### H10 — ALNIRA

**Hecho:** no se encontró implementación de ALNIRA en la búsqueda directa del repositorio principal.  
**Estado:** hipótesis experimental.

## 4. Decisiones registradas

| Decisión | Estado |
|---|---|
| Mantener G3 como hipótesis de estudio | vigente |
| No canonizar G3 | vigente |
| No implementar G3 como consecuencia automática del estudio | vigente |
| Mantener ALNIRA como hipótesis experimental | vigente |
| No canonizar ALNIRA | vigente |
| No construir una plataforma ALNIRA pesada sin PoC | vigente |
| Auditar el artefacto de Aether garantía por garantía antes de PoC G3 | próximo hito |
| Separar G3 y ALNIRA | vigente |

## 5. Preguntas abiertas G3

1. ¿Existe una capa de validez bitemporal equivalente a la del modelo G3?
2. ¿Puede reconstruirse una autorización histórica con garantías equivalentes?
3. ¿Existe atestación formal de actos con principal, derecho, contexto y evidencia?
4. ¿Puede realizarse el triple join Graphy + Utópico + Acta sin unificar los órganos?
5. ¿Existe un receipt compuesto verificable?
6. ¿Existe fail-closed integral ante ausencia/conflicto de una garantía?
7. ¿La respuesta histórica `as_of` puede reconstruirse de forma fiable?
8. ¿El artefacto de Aether aporta garantías no presentes en el WAIPL actual?

## 6. Preguntas abiertas ALNIRA

1. ¿Qué experimento concreto no queda suficientemente resuelto con Positrón + Ollama + agentes + scripts?
2. ¿La separación epistemológica requiere un entorno propio?
3. ¿Qué nivel mínimo de reproducibilidad es necesario?
4. ¿Qué metadatos y trazas deben conservarse?
5. ¿Cómo se impide que un resultado experimental contamine conocimiento canónico?
6. ¿Existe una ventaja suficiente frente a utilizar directamente infraestructura existente?

## 7. Regla de continuidad documental

Este expediente no se considera borrado por un futuro NO-GO. Un resultado NO-GO debe conservarse con:

- fecha;
- hipótesis;
- evidencia revisada;
- pruebas realizadas;
- razones de descarte;
- impacto sobre la arquitectura;
- artefactos/commits/PRs asociados.

Las futuras versiones deben añadir trazabilidad, no borrar la historia del estudio.
