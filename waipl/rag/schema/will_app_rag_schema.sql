-- ============================================================================
-- Will App RAG â€” Esquema CanÃ³nico de Datos (FASE 1, Orden Soberana v0.3.1)
-- ============================================================================
-- Infraestructura: PostgreSQL + pgvector (secciÃ³n 5 de la Orden Soberana).
-- Este DDL se APLICA en FASE 3 (provisiÃ³n de PostgreSQL). En FASE 1 es el
-- entregable canÃ³nico del modelo, en paridad 1:1 con waipl/core/knowledge_model.py.
--
-- Entidades: Document, Version, Source, Acquisition, Verification,
--            HumanDecision, Ingestion, Chunk, Embedding, Alias, AuditLog.
-- Invariantes: Principio Absoluto (I1), Aislamiento (I2), DeduplicaciÃ³nâ†’Alias
--              (I3), Vigencia (I4), Trazabilidad de decisiones (I5), AuditLog (I6).
-- Las reglas de negocio de transiciÃ³n se aplican en la capa de aplicaciÃ³n
-- (knowledge_model.py) y se reforzarÃ¡n con triggers en FASE 3.
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS vector;

-- â”€â”€â”€ 1. Source â€” fuente origen â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE sources (
    source_id     UUID PRIMARY KEY,
    nombre        TEXT NOT NULL,
    url           TEXT NOT NULL,
    tipo          TEXT NOT NULL,               -- BOE / OMS / revista_indexada / normativa_oficial / ...
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- â”€â”€â”€ 2. Document â€” documento lÃ³gico Ãºnico â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE documents (
    document_id   UUID PRIMARY KEY,
    source_id     UUID NOT NULL REFERENCES sources(source_id),
    title         TEXT NOT NULL,
    domain        TEXT NOT NULL CHECK (domain IN ('MEDICO_CIENTIFICO_COMUNITARIO','JURIDICO_NORMATIVO')),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_documents_source ON documents(source_id);
CREATE INDEX idx_documents_domain ON documents(domain);

-- â”€â”€â”€ 3. Version â€” cada versiÃ³n del documento â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE versions (
    version_id            UUID PRIMARY KEY,
    document_id           UUID NOT NULL REFERENCES documents(document_id),
    version_number        INT  NOT NULL,
    content_hash          CHAR(64) NOT NULL,  -- SHA-256
    stored_path           TEXT NOT NULL,
    state                 TEXT NOT NULL CHECK (state IN (
                              'BORRADOR','EN_VERIFICACION','PENDIENTE_DECISION_HUMANA',
                              'VIGENTE','OBSOLETA','CUARENTENA','REVOCADA')),
    supersedes_version_id UUID REFERENCES versions(version_id),
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (document_id, version_number)
);
CREATE INDEX idx_versions_document ON versions(document_id);
CREATE INDEX idx_versions_state ON versions(state);
CREATE INDEX idx_versions_hash ON versions(content_hash);

-- â”€â”€â”€ 4. Acquisition â€” adquisiciÃ³n realizada â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE acquisitions (
    acquisition_id UUID PRIMARY KEY,
    version_id     UUID NOT NULL REFERENCES versions(version_id),
    agent          TEXT NOT NULL,              -- KAIROS / DIKE (adquisiciÃ³n, no decisiÃ³n)
    acquired_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata       JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX idx_acquisitions_version ON acquisitions(version_id);

-- â”€â”€â”€ 5. Verification â€” resultado de verificaciÃ³n del dominio â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE verifications (
    verification_id UUID PRIMARY KEY,
    version_id      UUID NOT NULL REFERENCES versions(version_id),
    domain          TEXT NOT NULL CHECK (domain IN ('MEDICO_CIENTIFICO_COMUNITARIO','JURIDICO_NORMATIVO')),
    verifier        TEXT NOT NULL,             -- DIKE (RGL-01) / VÃ¡r (VAC-01) / especialista tÃ©cnico
    result          TEXT NOT NULL CHECK (result IN (
                        'CONFORME','CONFORME_CON_RESTRICCIONES','NO_CONFORME','INDETERMINADO')),
    confidence      NUMERIC(3,2) CHECK (confidence BETWEEN 0 AND 1),
    dictamen_id     UUID,                      -- referencia al dictamen en vault DIKE
    auditor         TEXT,                      -- Yata si procede (auditorÃ­a de verificadores)
    verified_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_verifications_version ON verifications(version_id);

-- â”€â”€â”€ 6. HumanDecision â€” decisiÃ³n humana trazable (I5: campos obligatorios) â”€â”€
CREATE TABLE human_decisions (
    decision_id         UUID PRIMARY KEY,
    version_id          UUID NOT NULL REFERENCES versions(version_id),
    target_version_id   UUID NOT NULL REFERENCES versions(version_id),
    human_reviewer_id   TEXT NOT NULL,          -- quiÃ©n decide (Soberano / Carla / autorizada)
    decision            TEXT NOT NULL CHECK (decision IN ('ACCEPT','REJECT')),
    decision_timestamp  TIMESTAMPTZ NOT NULL DEFAULT now(),
    decision_reason     TEXT NOT NULL,          -- NOT NULL: sin razÃ³n no hay decisiÃ³n (I5)
    CONSTRAINT decision_targets_version CHECK (version_id = target_version_id)
);
CREATE INDEX idx_decisions_version ON human_decisions(version_id);

-- â”€â”€â”€ 7. Ingestion â€” estado de ingesta al RAG â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE ingestions (
    ingestion_id UUID PRIMARY KEY,
    version_id   UUID NOT NULL REFERENCES versions(version_id),
    state        TEXT NOT NULL CHECK (state IN ('PENDIENTE','INGESTADO','REVOCADO')),
    ingested_at  TIMESTAMPTZ,
    chunk_count  INT NOT NULL DEFAULT 0
);
CREATE INDEX idx_ingestions_version ON ingestions(version_id);

-- â”€â”€â”€ 8. Chunk â€” fragmentos para embeddings â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE chunks (
    chunk_id     UUID PRIMARY KEY,
    version_id   UUID NOT NULL REFERENCES versions(version_id),
    ingestion_id UUID NOT NULL REFERENCES ingestions(ingestion_id),
    ordinal      INT  NOT NULL,
    text         TEXT NOT NULL,
    metadata     JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (ingestion_id, ordinal)
);
CREATE INDEX idx_chunks_version ON chunks(version_id);

-- â”€â”€â”€ 9. Embedding â€” vector generado (pgvector) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
-- DimensiÃ³n del modelo de embeddings: SE DECIDE EN FASE 3 (vector(768) es placeholder).
CREATE TABLE embeddings (
    embedding_id UUID PRIMARY KEY,
    chunk_id     UUID NOT NULL UNIQUE REFERENCES chunks(chunk_id),
    model        TEXT NOT NULL,
    dimensions   INT  NOT NULL DEFAULT 0,
    vector_ref   TEXT,                          -- id externo si aplica (transiciÃ³n FASE 3)
    vector       vector(768)                    -- placeholder; ajustar dimensiÃ³n en FASE 3
    -- FASE 3: CREATE INDEX ... USING hnsw (vector vector_cosine_ops);
);

-- â”€â”€â”€ 10. Alias â€” deduplicaciÃ³n por content_hash (I3: sin nuevos embeddings) â”€
CREATE TABLE aliases (
    alias_id              UUID PRIMARY KEY,
    content_hash          CHAR(64) NOT NULL,
    canonical_version_id  UUID NOT NULL REFERENCES versions(version_id),
    duplicate_version_id  UUID NOT NULL UNIQUE REFERENCES versions(version_id),
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_aliases_hash ON aliases(content_hash);

-- â”€â”€â”€ 11. AuditLog â€” trazabilidad completa (I6) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CREATE TABLE audit_log (
    audit_id    UUID PRIMARY KEY,
    timestamp   TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor       TEXT NOT NULL,
    action      TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id   UUID,
    payload     JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX idx_audit_target ON audit_log(target_type, target_id);
CREATE INDEX idx_audit_time ON audit_log(timestamp);

-- â”€â”€â”€ Vista canÃ³nica de recuperaciÃ³n (Ãºnico punto de lectura de Will App) â”€â”€â”€â”€
-- I1+I2+I4: VIGENTE + ACCEPT + INGESTADO y no duplicada (sin alias propio).
CREATE VIEW retrievable_knowledge AS
SELECT v.version_id, v.document_id, d.domain, d.title, v.version_number,
       v.content_hash, v.stored_path
FROM versions v
JOIN documents d ON d.document_id = v.document_id
WHERE v.state = 'VIGENTE'
  AND NOT EXISTS (SELECT 1 FROM aliases a WHERE a.duplicate_version_id = v.version_id)
  AND EXISTS (SELECT 1 FROM human_decisions hd
              WHERE hd.version_id = v.version_id AND hd.decision = 'ACCEPT')
  AND EXISTS (SELECT 1 FROM ingestions i
              WHERE i.version_id = v.version_id AND i.state = 'INGESTADO');

-- ============================================================================
-- FASE 3 â€” Capa fÃ­sica de seguridad y operaciÃ³n (Orden Soberana v0.3.1)
-- ============================================================================
-- Se aÃ±ade a la aprobaciÃ³n de FASE 1: roles de mÃ­nimo privilegio, triggers que
-- IMPIDEN fÃ­sicamente que estados no recuperables (BORRADOR, EN_VERIFICACION,
-- PENDIENTE_DECISION_HUMANA, CUARENTENA, OBSOLETA, REVOCADA) se conviertan en
-- conocimiento operativo, e Ã­ndices adicionales.
-- Credenciales: SIEMPRE por variables de entorno / secrets externos. NADA hardcodeado.

-- â”€â”€â”€ Seguridad: roles (creaciÃ³n condicional) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'waipl_app') THEN
        CREATE ROLE waipl_app LOGIN PASSWORD NULL;  -- contraseÃ±a fijada por el aprovisionador vÃ­a env
    END IF;
END
$$;

-- â”€â”€â”€ Enforcement fÃ­sico: solo VIGENTE + ACCEPT admite ingesta (I1+I4) â”€â”€â”€â”€â”€â”€â”€
CREATE OR REPLACE FUNCTION fn_verificar_ingesta_admisible() RETURNS trigger AS $$
DECLARE v_state TEXT;
BEGIN
    -- Solo las ingestas ACTIVAS requieren admisibilidad; las REVOCADO son
    -- hechos históricos (trazabilidad) y se permiten.
    IF NEW.state NOT IN ('INGESTADO','PENDIENTE') THEN
        RETURN NEW;
    END IF;
    SELECT state INTO v_state FROM versions WHERE version_id = NEW.version_id;
    IF v_state IS NULL THEN
        RAISE EXCEPTION 'INGESTION RECHAZADA: version inexistente %', NEW.version_id;
    END IF;
    IF v_state <> 'VIGENTE' THEN
        RAISE EXCEPTION 'INGESTION RECHAZADA: estado % no admisible (solo VIGENTE)', v_state;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM human_decisions
                   WHERE version_id = NEW.version_id AND decision = 'ACCEPT') THEN
        RAISE EXCEPTION 'INGESTION RECHAZADA: sin HumanDecision ACCEPT (Principio Absoluto)';
    END IF;
    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_ingestion_admisible ON ingestions;
CREATE TRIGGER trg_ingestion_admisible
    BEFORE INSERT OR UPDATE ON ingestions
    FOR EACH ROW EXECUTE FUNCTION fn_verificar_ingesta_admisible();

-- Los chunks heredan la admisibilidad de su ingestion (no hay ingesta huÃ©rfana)
CREATE OR REPLACE FUNCTION fn_chunk_requiere_ingestion_valida() RETURNS trigger AS $$
DECLARE v_vid UUID;
BEGIN
    SELECT version_id INTO v_vid FROM ingestions WHERE ingestion_id = NEW.ingestion_id;
    IF v_vid IS NULL THEN
        RAISE EXCEPTION 'CHUNK RECHAZADO: ingestion inexistente %', NEW.ingestion_id;
    END IF;
    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_chunk_ingestion_valida ON chunks;
CREATE TRIGGER trg_chunk_ingestion_valida
    BEFORE INSERT OR UPDATE ON chunks
    FOR EACH ROW EXECUTE FUNCTION fn_chunk_requiere_ingestion_valida();

-- â”€â”€â”€ Ãndices adicionales FASE 3 (bÃºsqueda, procedencia, deduplicaciÃ³n) â”€â”€â”€â”€â”€â”€
CREATE INDEX IF NOT EXISTS idx_versions_content_hash ON versions(content_hash);
CREATE INDEX IF NOT EXISTS idx_versions_state_vigente ON versions(state) WHERE state = 'VIGENTE';
CREATE INDEX IF NOT EXISTS idx_chunks_metadata_gin ON chunks USING gin(metadata jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_verifications_version ON verifications(version_id);
CREATE INDEX IF NOT EXISTS idx_decisions_version_decision ON human_decisions(version_id, decision);
-- FASE 3+: Ã­ndice vectorial (hnsw/ivfflat) se crea al fijar la dimensiÃ³n del modelo de embeddings.

