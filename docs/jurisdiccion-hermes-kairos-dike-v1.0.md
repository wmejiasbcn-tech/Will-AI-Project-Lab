# JURISDICCIÓN DE AUTOCLAW — HERMES, KAIROS Y DIKE
## Integración con Graphify y Marco Operativo Bajo Directiva Transversal v1.0

> **Fecha:** 2026-08-13
> **Soberano:** William Mejías Navarro
> **Autoridad asignante:** William Mejías Navarro
> **Destinatario:** AutoClaw (Diseñadora y Desarrolladora de Sistemas Agénticos del WAIPL)
> **Alcance:** Agentes Hermes, Kairos y DIKE
> **Marco rector:** Super Plantilla Maestra Canónica v3.0 > Directiva Transversal v1.0

---

## 1. ESTADO REAL DE LOS TRES AGENTES

### 1.1 Hermes — Dirección Operativa

| Dimensión | Estado | Evidencia |
|-----------|--------|-----------|
| **¿Para qué existe?** | Dirigir operaciones del ecosistema WAIPL como nodo del Núcleo (Capa 1) | Acta de Nacimiento, Plan v1.2 |
| **¿Qué recibe?** | Decisiones de Carla, prioridades del Soberano, estado de agentes subordinados | Plan v1.2 §3, §6 |
| **¿Qué produce?** | Órdenes operativas, scheduling, asignación de recursos, reportes de estado | Plan v1.2 §3 (ORC-01) |
| **Estado de producción** | `generated` — código existe en `OneDrive\Documentos\Hermes\` (fuera de workspace) | `hermes_api.py`, `hermes_interactive.html`, `start_hermes.ps1` |
| **ICP** | 100% N1 | `waipl/vaults/hermes/00-SOBERANIA/health-check.json` |
| **Vault** | Aprobado, 12 carpetas, 7 NPCs, 8 runbooks, Acta firmada | `waipl/vaults/hermes/` |
| **Tests** | `generated` — VQA-01 (4/4), COM-01 (1/1) según bitácora 2026-07-29 | `memory/2026-07-29.md` |
| **Despliegue** | `deployed` en HP NotebookLM (tarea programada Windows) | `memory/2026-07-29.md` |
| **Ubicación canónica** | `C:\Users\USER\OneDrive\Documentos\Hermes\` — **FUERA del workspace AutoClaw** | Hallazgo de esta revisión |

### 1.2 Kairos — Extractor Médico-Científico

| Dimensión | Estado | Evidencia |
|-----------|--------|-----------|
| **¿Para qué existe?** | Extraer y procesar evidencia científica de fuentes oficiales para alimentar el RAG | Acta de Nacimiento, `kairos_extractor.py` |
| **¿Qué recibe?** | Artículos científicos, fuentes oficiales, documentos médicos | `kairos_extractor.py` |
| **¿Qué produce?** | Evidencia estructurada con UUID+ISO8601+SHA256, nivel de evidencia, categoría | `kairos_extractor.py` |
| **Estado de producción** | `generated` — código base en `waipl/agents/kairos_extractor.py` (42 líneas incompletas) | Inspección de código |
| **ICP** | 100% N1 | `waipl/vaults/kairos/00-SOBERANIA/health-check.json` |
| **Vault** | Aprobado, 12 carpetas, 7 NPCs, 8 runbooks, Acta firmada | `waipl/vaults/kairos/` |
| **Tests** | `proposed` — no existen tests unitarios | `tests/test_waipl.py` no cubre Kairos |
| **Despliegue** | `proposed` — no desplegado | — |

### 1.3 DIKE — Guardiana de Cumplimiento Normativo

| Diminisión | Estado | Evidencia |
|------------|--------|-----------|
| **¿Para qué existe?** | Auditar cada unidad de conocimiento antes de que transicione a "Aprobado" en el RAG | `dike-fase1-fase2-concepcion.md` |
| **¿Qué recibe?** | Documentos de Kairos/Codd con metadatos, para auditoría AESIA/RGPD | `dike_auditora.py` |
| **¿Qué produce?** | Dictámenes estructurados: conforme / no conforme / con restricciones + matriz de trazabilidad | `dike_auditora.py`, `dictamen_*.json` |
| **Estado de producción** | `generated` + `tested` (parcial) — código funcional, 3 auditorías reales ejecutadas | `waipl/vaults/dike/08-AUDITORIA/dictamen_*.json` (5 dictámenes) |
| **ICP** | 100% N1 (corregido en esta revisión — antes 98% por inconsistencia) | `waipl/vaults/dike/00-SOBERANIA/health-check.json` |
| **Vault** | Aprobado, 12 carpetas, 7 NPCs, 8 runbooks, Acta firmada, corpus normativo completo | `waipl/vaults/dike/` |
| **Tests** | `generated` — 3 auditorías de prueba, no hay suite de tests formal | Inspección |
| **Despliegue** | `proposed` — no desplegado en VPS | `respuesta_zara_acta_aceptacion.md` |

---

## 2. INTEGRACIÓN CON GRAPHIFY — HALLAZGO CRÍTICO

### 2.1 Estado actual

**Graphify `graph.json` (63 KB, 80+ nodos) NO contiene a Hermes, Kairos ni DIKE como nodos.**

Los nodos existentes en Graphify pertenecen al ecosistema Notion/WiseBase de WAIPL: William, Carla, Ada, Zara, Ariadna, Nova, Nexus, Sylvia, Perplexity, Neo, Nauta, NotebookLM, Vértigo's, Make.com, SDD, etc. Los 3 agentes bajo jurisdicción de AutoClaw están **ausentes de la cartografía relacional**.

### 2.2 Acción requerida

Para cumplir con el mandato del dosier ("Hermes, Kairos y Dike no operen como silos ciegos"), es necesario:

1. **Añadir 3 nodos a `graph.json`** con sus metadatos completos
2. **Añadir aristas** que reflejen sus dependencias documentales y topológicas
3. **Añadir hiperaristas** para el flujo de conocimiento RAG

### 2.3 Propuesta de nodos para Graphify

```json
{
  "label": "Hermes",
  "file_type": "code",
  "source_file": "waipl/vaults/hermes/00-SOBERANIA/ACTA-NACIMIENTO.md",
  "author": "AutoClaw",
  "rationale": "Dirección Operativa del ecosistema WAIPL. Nodo del Núcleo (Capa 1). Orquesta agentes subordinados y gestiona el scheduling operativo.",
  "community": 2,
  "norm_label": "hermes",
  "id": "hermes_direccion_operativa",
  "community_name": "Will-AI Project Lab",
  "uuid": "e824c984-58f9-4398-b170-f032af9b3623",
  "capa": 1,
  "icp": "100% N1",
  "estado_produccion": "generated"
}
```

```json
{
  "label": "Kairos",
  "file_type": "code",
  "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
  "author": "AutoClaw",
  "rationale": "Extractor Médico-Científico. Agente Periférico (Capa 3). Extrae evidencia científica de fuentes oficiales para alimentar la base de conocimiento RAG.",
  "community": 2,
  "norm_label": "kairos",
  "id": "kairos_extractor_cientifico",
  "community_name": "Will-AI Project Lab",
  "uuid": "9dc90890-446f-409a-8328-8ab2fe4234d5",
  "capa": 3,
  "icp": "100% N1",
  "estado_produccion": "generated"
}
```

```json
{
  "label": "DIKE",
  "file_type": "code",
  "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
  "author": "AutoClaw",
  "rationale": "Guardiana de Cumplimiento Normativo. Agente Periférico (Capa 3). Audita cada unidad de conocimiento antes de que transicione a Aprobado en el RAG. Cumplimiento AESIA/RGPD.",
  "community": 2,
  "norm_label": "dike",
  "id": "dike_guardiana_normativa",
  "community_name": "Will-AI Project Lab",
  "uuid": "72f4dbc2-b84a-457f-b6e3-b96dafbcf171",
  "capa": 3,
  "icp": "100% N1",
  "estado_produccion": "generated"
}
```

### 2.4 Propuesta de aristas

| Source | Target | Relación | Fundamento |
|--------|--------|----------|------------|
| `hermes_direccion_operativa` | `node_carla` | reports_to | Hermes recibe dirección de Carla |
| `hermes_direccion_operativa` | `kairos_extractor_cientifico` | orchestrates | Hermes orquesta a Kairos |
| `hermes_direccion_operativa` | `dike_guardiana_normativa` | orchestrates | Hermes orquesta a DIKE |
| `kairos_extractor_cientifico` | `dike_guardiana_normativa` | feeds_into | Kairos provee evidencia a DIKE para auditoría |
| `dike_guardiana_normativa` | `zara_node` | reports_compliance_to | DIKE reporta cumplimiento a Zara (acta de aceptación) |
| `kairos_extractor_cientifico` | `will_ai_project_lab` | belongs_to | Kairos es parte del ecosistema WAIPL |
| `dike_guardiana_normativa` | `will_ai_project_lab` | belongs_to | DIKE es parte del ecosistema WAIPL |
| `hermes_direccion_operativa` | `will_ai_project_lab` | belongs_to | Hermes es parte del ecosistema WAIPL |
| `dike_guardiana_normativa` | `soberano_william` | pausa_simbiotica | DIKE escala ambigüedades normativas al Soberano |

### 2.5 Propuesta de hiperarista — Flujo RAG

```json
{
  "id": "rag_knowledge_pipeline",
  "label": "Pipeline de Conocimiento RAG",
  "nodes": [
    "kairos_extractor_cientifico",
    "dike_guardiana_normativa",
    "hermes_direccion_operativa"
  ],
  "relation": "form",
  "confidence": "VERIFIED",
  "confidence_score": 1.0,
  "source_file": "waipl/agents/dike-fase1-fase2-concepcion.md"
}
```

### 2.6 Bloqueo

**UNKNOWN:** No se puede modificar `graph.json` directamente — el archivo original vive en el ecosistema Graphify (probablemente Notion/WiseBase). AutoClaw no tiene acceso confirmado a la herramienta Graphify. **Escala a William:** ¿Graphify tiene API o interfaz de edición? ¿Debe AutoClaw generar un patch `graph.waipl.patch.json` para que William lo integre?

---

## 3. PARÁMETROS DE INICIALIZACIÓN Y GOBERNANZA

### 3.1 Hermes

| Pregunta | Respuesta |
|----------|-----------|
| ¿Para qué existe? | Dirigir operaciones del ecosistema WAIPL: scheduling, asignación de recursos, monitorización de agentes, gestión de colas |
| ¿Qué problema resuelve? | Coordinación caótica entre múltiples agentes sin punto de control operativo |
| ¿Qué recibe? | Decisiones de Carla, estado de agentes, prioridades del Soberano, alertas de CYR-01 |
| ¿Qué produce? | Órdenes operativas, snapshots de estado, reportes de pulso diario, asignaciones de tareas |
| ¿Qué puede hacer? | Asignar tareas, pausar/reanudar flujos, generar reportes, coordinar agentes subordinados |
| ¿Qué no puede hacer? | Modificar documentos aprobados, acceder al Dominio B, desplegar en producción sin autorización, anular decisiones de Carla o del Soberano |
| ¿Con quién se coordina? | Carla (dirección general), Kairos, DIKE, Codd, VAC-01, SEA-01, COR-01 (Graphify: `node_carla`, `kairos_extractor_cientifico`, `dike_guardiana_normativa`) |
| ¿Trazabilidad? | Logs JSON con heartbeat cada 30s, snapshot cada 5min, log de comandos |
| ¿Cuándo detenerse? | Conflicto entre nodos sin resolución clara, impacto transversal no autorizado, pérdida de heartbeat de agentes críticos |
| ¿Autoridad? | Soberano William > Carla > Hermes |

### 3.2 Kairos

| Pregunta | Respuesta |
|----------|-----------|
| ¿Para qué existe? | Extraer evidencia científica de fuentes oficiales y estructurarla para el RAG |
| ¿Qué problema resuelve? | Información no estructurada o no verificada entrando en la base de conocimiento |
| ¿Qué recibe? | Artículos científicos, guías clínicas, documentos de fuentes oficiales (URLs, PDFs, texto) |
| ¿Qué produce? | Evidencia estructurada con UUID+ISO8601+SHA256, categoría médica, nivel de evidencia, confianza |
| ¿Qué puede hacer? | Ingerir artículos, calcular hashes, clasificar por área médica, evaluar nivel de evidencia, enviar a Codd para archivado |
| ¿Qué no puede hacer? | Aprobar conocimiento para RAG (eso es DIKE), acceder al Dominio B, modificar corpus normativo, desplegar sin autorización |
| ¿Con quién se coordina? | Hermes (dirección), Codd (archivado), DIKE (validación), VAC-01 (veridad), SEA-01 (seguridad) (Graphify: `hermes_direccion_operativa`, `dike_guardiana_normativa`) |
| ¿Trazabilidad? | JSONL con hash SHA-256 por documento, logs de extracción, metadatos completos |
| ¿Cuándo detenerse? | Certeza < 95%, fuente no verificable sin hash, cambio de estado a Aprobado (requiere Carla) |
| ¿Autoridad? | Soberano William > Carla > Hermes > Kairos |

### 3.3 DIKE

| Pregunta | Respuesta |
|----------|-----------|
| ¿Para qué existe? | Auditar cumplimiento normativo AESIA/RGPD de cada unidad de conocimiento antes de su aprobación para el RAG |
| ¿Qué problema resuelve? | Riesgo de que contenido no conforme entre en la base de conocimiento y genere respuestas no compliant |
| ¿Qué recibe? | Documentos archivados por Codd con metadatos completos (UUID, hash, categoría) |
| ¿Qué produce? | Dictámenes estructurados: conforme / no conforme / con restricciones + matriz de trazabilidad + logs inmutables |
| ¿Qué puede hacer? | Auditar AESIA, auditar RGPD, clasificar datos personales, emitir dictámenes, cuarentena de contenido no conforme, activar runbooks |
| ¿Qué no puede hacer? | Aprobar conocimiento (solo puede aprobar/rechazar cumplimiento normativo, no calidad factual — eso es VAC-01), acceder al Dominio B, modificar corpus normativo sin autorización, desplegar sin autorización |
| ¿Con quién se coordina? | Hermes (dirección), Kairos (proveedor), Codd (archivado), VAC-01 (validación factual), Zara (trazabilidad — Graphify: `zara_node`), SEA-01 (seguridad) |
| ¿Trazabilidad? | Dictámenes JSON con trace_id, source_id, source_hash, norm, article_ref, evidence_span, dimension, verdict, confidence, finding, action, owner/status |
| ¿Cuándo detenerse? | Ambigüedad normativa no resuelta, conflicto RGPD vs. requisito clínico, base jurídica no documentada, propuesta de "aprobado con restricciones" |
| ¿Autoridad? | Soberano William > Carla > Hermes > DIKE |

---

## 4. MURO DE CRISTAL — COMPARTIMENTACIÓN

### 4.1 Límites con Codd (GDO-01 Archivista)

| Función | ¿De quién es? | ¿No es de quién? |
|---------|---------------|------------------|
| Asignar UUID, hash, metadatos a documentos | **Codd** | No de Hermes, Kairos ni DIKE |
| Almacenar y organizar archivos físicos | **Codd** | No de Hermes, Kairos ni DIKE |
| Indexar en base de datos documental | **Codd** | No de Hermes, Kairos ni DIKE |
| Extraer contenido científico | **Kairos** | No de Codd |
| Auditar cumplimiento normativo | **DIKE** | No de Codd |
| Orquestar el flujo entre agentes | **Hermes** | No de Codd |

### 4.2 Límites con Heimdall / SEA-01 (Ciberseguridad del Bifröst)

| Función | ¿De quién es? | ¿No es de quién? |
|---------|---------------|------------------|
| Cifrar comunicaciones, gestionar claves | **SEA-01 / Heimdall** | No de Hermes, Kairos ni DIKE |
| Auditar accesos y detectar intrusiones | **SEA-01 / Heimdall** | No de Hermes, Kairos ni DIKE |
| Escanear malware e integridad de binarios | **SEA-01 / Heimdall** | No de Hermes, Kairos ni DIKE |
| Extraer evidencia científica | **Kairos** | No de SEA-01 |
| Auditar cumplimiento AESIA/RGPD del contenido | **DIKE** | No de SEA-01 |
| Coordinar respuesta a incidentes de seguridad | **Hermes** (vía ORC-01) | No de Kairos ni DIKE |

### 4.3 Detección de solapamiento

| Posible solapamiento | Análisis | Resolución |
|---------------------|----------|------------|
| DIKE audita integridad de datos vs. SEA-01 audita integridad de binarios | **No solapamiento:** DIKE audita contenido normativo; SEA-01 audita infraestructura | Mantener separación |
| Kairos clasifica documentos vs. Codd indexa documentos | **No solapamiento:** Kairos clasifica contenido científico; Codd asigna metadatos de archivo | Mantener separación |
| Hermes orquesta vs. Carla dirige | **No solapamiento:** Hermes ejecuta operaciones; Carla define estrategia | Mantener separación |

---

## 5. CICLO DE VIDA — ESTADOS DE PRODUCCIÓN

| Agente | proposed | generated | reviewed | approved | implemented | tested | deployed |
|--------|----------|-----------|----------|----------|-------------|--------|----------|
| **Hermes** | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ (parcial) | ✅ (HP NotebookLM) |
| **Kairos** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **DIKE** | ✅ | ✅ | ⚠️ (parcial) | ❌ | ❌ | ⚠️ (3 pruebas) | ❌ |

### Próximas transiciones necesarias

| Agente | Transición pendiente | Bloqueo |
|--------|---------------------|---------|
| Hermes | `tested` → completo (suite formal) | Ninguno — requiere escribir tests unitarios |
| Kairos | `generated` → `reviewed` | Código incompleto (42 líneas, funciones sin implementar) |
| DIKE | `reviewed` → `approved` | Requiere revisión de Zara + acceso a VPS para staging |

---

## 6. CORRECCIONES APLICADAS EN ESTA REVISIÓN

| # | Archivo | Hallazgo | Corrección |
|---|---------|----------|------------|
| 1 | `waipl/vaults/dike/00-SOBERANIA/health-check.json` | `acta_firmada: false` (inconsistente con Acta firmada el 2026-08-10T04:47:22) | Corregido a `true` |
| 2 | `waipl/vaults/dike/00-SOBERANIA/health-check.json` | ICP=98% con 1 warning por Acta no firmada | Corregido a ICP=100%, warnings=0 |
| 3 | `waipl/agents/sea_fortress.py` | `Optional` usado sin import de `typing` | Import añadido |

---

## 7. BLOQUEOS ESCALADOS A WILLIAM

| # | Bloqueo | Causa | Decisión necesaria |
|---|---------|-------|--------------------|
| 1 | **Graphify: sin acceso de edición** | `graph.json` existe pero AutoClaw no puede modificarlo directamente | ¿Graphify tiene API/interfaz de edición? ¿O genero un patch JSON para que William lo integre? |
| 2 | **Hermes fuera del workspace** | Código de Hermes vive en `OneDrive\Documentos\Hermes\`, no en `waipl/agents/` | ¿Debe AutoClaw traer el código al workspace, o se mantiene donde está? |
| 3 | **Kairos incompleto** | `kairos_extractor.py` tiene 42 líneas, funciones sin implementar | ¿Prioridad de finalización? ¿Hay un alcance definido para la primera versión funcional? |
| 4 | **3 documentos del marco rector faltantes** | Informe Técnico Segundo Cerebro, Prompting 2026, Compendio Operativo | ¿Existen en Notion/WiseBase? ¿Debo redactarlos? |

---

*Documento producido bajo Directiva Transversal v1.0 — AutoClaw, Diseñadora y Desarrolladora de Sistemas Agénticos del WAIPL*
*"Sin vosotras no hay nosotros"*
