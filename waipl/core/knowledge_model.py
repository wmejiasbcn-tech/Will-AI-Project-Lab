"""
Will App RAG — Modelo de Conocimiento Canónico (FASE 1, Orden Soberana v0.3.1).

Implementa el esquema completo de datos y relaciones de la Orden Soberana
RAG Will App v0.3.1 (2026-09-01, APROBADA):

Entidades: Document, Version, Source, Acquisition, Verification,
HumanDecision, Ingestion, Chunk, Embedding, Alias, AuditLog.

Invariantes canónicos (no negociables):
  I1 (Principio Absoluto): ninguna versión es recuperable sin verificación
      de su dominio + HumanDecision = ACCEPT.
  I2 (Aislamiento): Archivo Documental ≠ Conocimiento Canónico ≠ Vector Store
      ≠ RAG. Una versión archivada (BORRADOR/EN_VERIFICACION) no es recuperable.
  I3 (Deduplicación / FINDING-1): si content_hash ya existe → ALIAS, nunca
      nuevos embeddings (la versión duplicada no puede ingerirse por sí misma).
  I4 (Vigencia / FINDING-2): solo versiones con estado VIGENTE y decisión
      humana ACCEPT son recuperables; al ingerirse una versión que sustituye
      a otra, la anterior queda automáticamente REVOCADA (no recuperable).
  I5 (Trazabilidad): toda decisión humana registra human_reviewer_id,
      human_decision, decision_timestamp, target_version_id, decision_reason.
  I6 (Auditoría): toda mutación genera entrada en AuditLog.

Persistencia: JSON atómico (tempfile + os.replace) con lock — misma política
de hardening que rag_pipeline.py. En FASE 3 este estado migra a
PostgreSQL + pgvector (waipl/rag/schema/will_app_rag_schema.sql).

Solo stdlib.
"""

import hashlib
import json
import os
import tempfile
import threading
import uuid as uuidlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

WAIPL_ROOT = Path(__file__).parent.parent
DEFAULT_STORE = WAIPL_ROOT / "rag" / "knowledge_model.json"


class Domain(str, Enum):
    MEDICO_CIENTIFICO_COMUNITARIO = "MEDICO_CIENTIFICO_COMUNITARIO"
    JURIDICO_NORMATIVO = "JURIDICO_NORMATIVO"


class VerificationResult(str, Enum):
    CONFORME = "CONFORME"
    CONFORME_CON_RESTRICCIONES = "CONFORME_CON_RESTRICCIONES"
    NO_CONFORME = "NO_CONFORME"
    INDETERMINADO = "INDETERMINADO"


class VersionState(str, Enum):
    BORRADOR = "BORRADOR"
    EN_VERIFICACION = "EN_VERIFICACION"
    PENDIENTE_DECISION_HUMANA = "PENDIENTE_DECISION_HUMANA"
    VIGENTE = "VIGENTE"
    OBSOLETA = "OBSOLETA"        # sustituida por una versión posterior ingesta
    CUARENTENA = "CUARENTENA"    # rechazada por decisión humana
    REVOCADA = "REVOCADA"        # retirada expresamente (decisión/revocación)


class HumanDecisionType(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


class IngestionState(str, Enum):
    PENDIENTE = "PENDIENTE"
    INGESTADO = "INGESTADO"
    REVOCADO = "REVOCADO"


class KnowledgeModelError(Exception):
    """Violación del modelo canónico."""


class IngestionBlockedError(KnowledgeModelError):
    """Principio Absoluto: la versión no puede ingerirse (I1/I2/I3/I4)."""


def _now() -> str:
    return datetime.now(timezone(timedelta(hours=2))).isoformat()


def _uid() -> str:
    return str(uuidlib.uuid4())


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class Source:
    source_id: str
    nombre: str
    url: str
    tipo: str  # p. ej. BOE / OMS / revista_indexada / normativa_oficial
    created_at: str


@dataclass
class Document:
    document_id: str
    source_id: str
    title: str
    domain: str  # Domain
    created_at: str


@dataclass
class Version:
    version_id: str
    document_id: str
    version_number: int
    content_hash: str
    stored_path: str
    state: str  # VersionState
    supersedes_version_id: Optional[str]
    created_at: str
    updated_at: str


@dataclass
class Acquisition:
    acquisition_id: str
    version_id: str
    agent: str  # Kairos / DIKE
    acquired_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Verification:
    verification_id: str
    version_id: str
    domain: str  # Domain
    verifier: str  # DIKE (RGL-01) / Vár (VAC-01) / especialista técnico
    result: str  # VerificationResult
    confidence: float
    dictamen_id: Optional[str]
    auditor: Optional[str]  # Yata si procede
    verified_at: str


@dataclass
class HumanDecision:
    decision_id: str
    version_id: str
    target_version_id: str
    human_reviewer_id: str
    decision: str  # HumanDecisionType
    decision_timestamp: str
    decision_reason: str


@dataclass
class Ingestion:
    ingestion_id: str
    version_id: str
    state: str  # IngestionState
    ingested_at: Optional[str]
    chunk_count: int


@dataclass
class Chunk:
    chunk_id: str
    version_id: str
    ingestion_id: str
    ordinal: int
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)  # paridad con JSONB del esquema SQL (procedencia FASE 2)


@dataclass
class Embedding:
    embedding_id: str
    chunk_id: str
    model: str
    dimensions: int
    vector_ref: Optional[str]  # en FASE 3: id del vector en pgvector


@dataclass
class Alias:
    alias_id: str
    content_hash: str
    canonical_version_id: str
    duplicate_version_id: str
    created_at: str


@dataclass
class AuditEntry:
    audit_id: str
    timestamp: str
    actor: str
    action: str
    target_type: str
    target_id: str
    payload: Dict[str, Any] = field(default_factory=dict)


class KnowledgeStore:
    """Estado canónico del modelo de conocimiento (JSON atómico, lock compartido)."""

    _LOCK = threading.RLock()

    def __init__(self, store_path: Optional[str] = None):
        self.store_path = Path(store_path) if store_path else DEFAULT_STORE
        self._state: Dict[str, Any] = self._load()

    # ── persistencia ──────────────────────────────────────────────────────

    def _load(self) -> Dict[str, Any]:
        if self.store_path.exists():
            with open(self.store_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "sources": {}, "documents": {}, "versions": {}, "acquisitions": {},
            "verifications": {}, "human_decisions": {}, "ingestions": {},
            "chunks": {}, "embeddings": {}, "aliases": {}, "audit_log": [],
        }

    def _save(self):
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(self.store_path.parent), suffix=".tmp", prefix="kmodel_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._state, f, indent=2, ensure_ascii=False)
            os.replace(tmp, self.store_path)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def _audit(self, actor: str, action: str, target_type: str, target_id: str, **payload):
        entry = AuditEntry(_uid(), _now(), actor, action, target_type, target_id, payload)
        self._state["audit_log"].append(asdict(entry))

    def log_event(self, actor: str, action: str, target_type: str, target_id: str, **payload):
        """Evento de auditoría sin mutación de entidades (p. ej. bloqueos del
        ingestion layer). FASE 2 — trazabilidad completa de cada operación."""
        with KnowledgeStore._LOCK:
            self._audit(actor, action, target_type, target_id, **payload)
            self._save()

    # ── fuentes y documentos ─────────────────────────────────────────────

    def register_source(self, nombre: str, url: str, tipo: str, actor: str = "sistema") -> str:
        with KnowledgeStore._LOCK:
            src = Source(_uid(), nombre, url, tipo, _now())
            self._state["sources"][src.source_id] = asdict(src)
            self._audit(actor, "register_source", "Source", src.source_id, nombre=nombre, url=url)
            self._save()
            return src.source_id

    def register_document(self, source_id: str, title: str, domain: Domain, actor: str = "sistema") -> str:
        with KnowledgeStore._LOCK:
            if source_id not in self._state["sources"]:
                raise KnowledgeModelError(f"Source inexistente: {source_id}")
            doc = Document(_uid(), source_id, title, domain.value, _now())
            self._state["documents"][doc.document_id] = asdict(doc)
            self._audit(actor, "register_document", "Document", doc.document_id, title=title, domain=domain.value)
            self._save()
            return doc.document_id

    # ── versiones ────────────────────────────────────────────────────────

    def register_version(
        self,
        document_id: str,
        content_text: str,
        stored_path: str,
        supersedes_version_id: Optional[str] = None,
        actor: str = "sistema",
    ) -> str:
        with KnowledgeStore._LOCK:
            if document_id not in self._state["documents"]:
                raise KnowledgeModelError(f"Document inexistente: {document_id}")
            doc = self._state["documents"][document_id]
            n = sum(
                1 for v in self._state["versions"].values()
                if v["document_id"] == document_id
            ) + 1
            ver = Version(
                _uid(), document_id, n, _sha256(content_text), stored_path,
                VersionState.BORRADOR.value, supersedes_version_id, _now(), _now(),
            )
            self._state["versions"][ver.version_id] = asdict(ver)
            if supersedes_version_id:
                if supersedes_version_id not in self._state["versions"]:
                    raise KnowledgeModelError(f"Versión sustituida inexistente: {supersedes_version_id}")
            self._audit(actor, "register_version", "Version", ver.version_id,
                        document_id=document_id, version_number=n,
                        content_hash=ver.content_hash, domain=doc["domain"])
            self._save()
            return ver.version_id

    # ── adquisición y verificación ───────────────────────────────────────

    def register_acquisition(
        self, version_id: str, agent: str, actor: Optional[str] = None, **metadata
    ) -> str:
        with KnowledgeStore._LOCK:
            ver = self._get_version(version_id)
            if ver["state"] != VersionState.BORRADOR.value:
                raise KnowledgeModelError(f"Solo una versión BORRADOR puede registrar adquisición (estado: {ver['state']})")
            acq = Acquisition(_uid(), version_id, agent, _now(), metadata)
            self._state["acquisitions"][acq.acquisition_id] = asdict(acq)
            self._transition(version_id, VersionState.EN_VERIFICACION, actor or agent)
            self._audit(actor or agent, "register_acquisition", "Acquisition", acq.acquisition_id,
                        version_id=version_id, agent=agent)
            self._save()
            return acq.acquisition_id

    def register_verification(
        self,
        version_id: str,
        verifier: str,
        result: VerificationResult,
        confidence: float,
        dictamen_id: Optional[str] = None,
        auditor: Optional[str] = None,
        actor: Optional[str] = None,
    ) -> str:
        """Verificación del dominio (DIKE para jurídico; verificación técnico-científica + Vár para médico)."""
        with KnowledgeStore._LOCK:
            ver = self._get_version(version_id)
            if ver["state"] != VersionState.EN_VERIFICACION.value:
                raise KnowledgeModelError(
                    f"Solo una versión EN_VERIFICACION puede verificarse (estado: {ver['state']})"
                )
            doc = self._state["documents"][ver["document_id"]]
            vac = Verification(
                _uid(), version_id, doc["domain"], verifier, result.value, float(confidence),
                dictamen_id, auditor, _now(),
            )
            self._state["verifications"][vac.verification_id] = asdict(vac)
            # Toda verificación deja la versión pendiente de supervisión humana (Principio Absoluto).
            self._transition(version_id, VersionState.PENDIENTE_DECISION_HUMANA, actor or verifier)
            self._audit(actor or verifier, "register_verification", "Verification", vac.verification_id,
                        version_id=version_id, result=result.value, confidence=confidence,
                        auditor=auditor, dictamen_id=dictamen_id)
            self._save()
            return vac.verification_id

    # ── decisión humana (Supervisión Humana Autorizada) ──────────────────

    def decide(
        self,
        version_id: str,
        human_reviewer_id: str,
        decision: HumanDecisionType,
        decision_reason: str,
        actor: Optional[str] = None,
    ) -> str:
        """I5: campos obligatorios human_reviewer_id, decision, decision_timestamp,
        target_version_id, decision_reason. Sin reason no hay decisión."""
        with KnowledgeStore._LOCK:
            ver = self._get_version(version_id)
            if ver["state"] != VersionState.PENDIENTE_DECISION_HUMANA.value:
                raise KnowledgeModelError(
                    f"Solo una versión PENDIENTE_DECISION_HUMANA puede decidirse (estado: {ver['state']})"
                )
            if not human_reviewer_id or not str(human_reviewer_id).strip():
                raise KnowledgeModelError("human_reviewer_id obligatorio (I5)")
            if decision not in (HumanDecisionType.ACCEPT, HumanDecisionType.REJECT):
                raise KnowledgeModelError(f"Decisión inválida: {decision!r} (I5)")
            if not decision_reason or not str(decision_reason).strip():
                raise KnowledgeModelError("decision_reason obligatoria (I5)")
            dec = HumanDecision(
                _uid(), version_id, version_id, human_reviewer_id, decision.value,
                _now(), decision_reason,
            )
            self._state["human_decisions"][dec.decision_id] = asdict(dec)
            nuevo = VersionState.VIGENTE if decision == HumanDecisionType.ACCEPT else VersionState.CUARENTENA
            self._transition(version_id, nuevo, actor or human_reviewer_id,
                             motivo=f"HumanDecision {decision.value}: {decision_reason}")
            self._audit(actor or human_reviewer_id, "human_decision", "HumanDecision", dec.decision_id,
                        version_id=version_id, decision=decision.value, reason=decision_reason)
            self._save()
            return dec.decision_id

    # ── ingesta al RAG (conocimiento operativo) ──────────────────────────

    def ingest(self, version_id: str, chunk_texts: List[str], model: str = "pendiente_fase3", actor: str = "sistema", chunk_metadata: Optional[List[Dict[str, Any]]] = None) -> str:
        """I1+I2+I4: solo VIGENTE con ACCEPT y sin alias activo. Genera chunks;
        embeddings quedan como referencias pendientes hasta FASE 3."""
        with KnowledgeStore._LOCK:
            ver = self._get_version(version_id)
            if ver["state"] != VersionState.VIGENTE.value:
                raise IngestionBlockedError(
                    f"I1/I2: solo VIGENTE es ingerible (estado actual: {ver['state']})"
                )
            if not any(
                d["version_id"] == version_id and d["decision"] == HumanDecisionType.ACCEPT.value
                for d in self._state["human_decisions"].values()
            ):
                raise IngestionBlockedError("I1: sin HumanDecision ACCEPT registrada")
            alias = self._state["aliases"].get(version_id)
            if alias and alias["duplicate_version_id"] == version_id:
                raise IngestionBlockedError(
                    f"I3: versión duplicada — usar canónica {alias['canonical_version_id']} (ALIAS {alias['alias_id'][:8]}...)"
                )
            if not chunk_texts:
                raise KnowledgeModelError("Sin chunks: la ingesta requiere al menos un fragmento")

            ing = Ingestion(_uid(), version_id, IngestionState.INGESTADO.value, _now(), len(chunk_texts))
            self._state["ingestions"][ing.ingestion_id] = asdict(ing)
            for i, txt in enumerate(chunk_texts, start=1):
                ch = Chunk(_uid(), version_id, ing.ingestion_id, i, txt,
                           (chunk_metadata[i - 1] if chunk_metadata and i - 1 < len(chunk_metadata) else {}))
                self._state["chunks"][ch.chunk_id] = asdict(ch)
                # Embedding: referencia pendiente hasta FASE 3 (pgvector). Nunca se
                # generan embeddings para duplicados (I3): el flujo llega aquí solo
                # para versiones canónicas.
                emb = Embedding(_uid(), ch.chunk_id, model, 0, None)
                self._state["embeddings"][emb.embedding_id] = asdict(emb)

            # I4 (vigencia): si esta versión sustituye a otra, la anterior pasa a
            # OBSOLETA (no recuperable) y su ingesta queda REVOCADA.
            if ver["supersedes_version_id"]:
                self._obsolete_locked(ver["supersedes_version_id"], actor,
                                      f"Sustituida por {version_id} (ingesta {ing.ingestion_id[:8]}...)")

            self._audit(actor, "ingest", "Ingestion", ing.ingestion_id,
                        version_id=version_id, chunk_count=ing.chunk_count, model=model)
            self._save()
            return ing.ingestion_id

    # ── deduplicación (FINDING-1) ────────────────────────────────────────

    def find_canonical(self, content_hash: str) -> Optional[str]:
        """Devuelve la version_id canónica VIGENTE para un content_hash, si existe.
        Un alias cuya canónica ya no esté VIGENTE no resuelve (sin contenido obsoleto)."""
        for alias in self._state["aliases"].values():
            if alias["content_hash"] == content_hash:
                can = self._state["versions"].get(alias["canonical_version_id"])
                if can and can["state"] == VersionState.VIGENTE.value:
                    return alias["canonical_version_id"]
        for ver in self._state["versions"].values():
            if ver["content_hash"] == content_hash and ver["state"] == VersionState.VIGENTE.value:
                return ver["version_id"]
        return None

    def make_alias(self, duplicate_version_id: str, canonical_version_id: Optional[str] = None,
                   actor: str = "sistema") -> str:
        """I3: si content_hash ya existe → ALIAS, no nuevos embeddings."""
        with KnowledgeStore._LOCK:
            dup = self._get_version(duplicate_version_id)
            canonical = canonical_version_id or self.find_canonical(dup["content_hash"])
            if not canonical:
                raise KnowledgeModelError("Sin versión canónica previa para ese content_hash")
            if canonical == duplicate_version_id:
                raise KnowledgeModelError("Una versión no puede ser alias de sí misma")
            can = self._get_version(canonical)
            if can["content_hash"] != dup["content_hash"]:
                raise KnowledgeModelError("content_hash distinto: no es duplicado")
            if can["state"] != VersionState.VIGENTE.value:
                raise KnowledgeModelError(
                    f"La canónica no está VIGENTE (estado: {can['state']}): alias no permitido"
                )
            al = Alias(_uid(), dup["content_hash"], canonical, duplicate_version_id, _now())
            self._state["aliases"][duplicate_version_id] = asdict(al)  # clave: versión duplicada
            self._audit(actor, "make_alias", "Alias", al.alias_id,
                        canonical=canonical, duplicate=duplicate_version_id)
            self._save()
            return al.alias_id

    # ── revocación (vigencia) ────────────────────────────────────────────

    def revoke(self, version_id: str, reason: str, actor: str = "sistema") -> None:
        with KnowledgeStore._LOCK:
            self._revoke_locked(version_id, actor, reason)
            self._save()

    def _revoke_locked(self, version_id: str, actor: str, reason: str):
        ver = self._get_version(version_id)
        if ver["state"] == VersionState.REVOCADA.value:
            return
        self._transition(version_id, VersionState.REVOCADA, actor, motivo=reason)
        for ing in self._state["ingestions"].values():
            if ing["version_id"] == version_id and ing["state"] == IngestionState.INGESTADO.value:
                ing["state"] = IngestionState.REVOCADO.value
                ing["chunk_count"] = ing.get("chunk_count", 0)
        self._audit(actor, "revoke", "Version", version_id, reason=reason)

    def _obsolete_locked(self, version_id: str, actor: str, reason: str):
        """Sustitución por nueva versión ingesta: la anterior pasa a OBSOLETA
        (distinta de REVOCADA, que es retirada expresa). Nunca recuperable."""
        ver = self._get_version(version_id)
        if ver["state"] in (VersionState.OBSOLETA.value, VersionState.REVOCADA.value):
            return
        self._transition(version_id, VersionState.OBSOLETA, actor, motivo=reason)
        for ing in self._state["ingestions"].values():
            if ing["version_id"] == version_id and ing["state"] == IngestionState.INGESTADO.value:
                ing["state"] = IngestionState.REVOCADO.value
        self._audit(actor, "obsolete", "Version", version_id, reason=reason)

    def validate_integrity(self) -> List[str]:
        """Integridad de relaciones: toda referencia apunta a una entidad existente.
        Retorna lista de errores (vacía = OK)."""
        s = self._state
        errores = []

        def existe(coleccion, eid, origen, campo):
            if eid not in s[coleccion]:
                errores.append(f"{origen}.{campo} referencia inexistente en {coleccion}: {eid}")

        for d in s["documents"].values():
            existe("sources", d["source_id"], f"document {d['document_id'][:8]}", "source_id")
        for v in s["versions"].values():
            existe("documents", v["document_id"], f"version {v['version_id'][:8]}", "document_id")
            if v["supersedes_version_id"]:
                existe("versions", v["supersedes_version_id"], f"version {v['version_id'][:8]}", "supersedes_version_id")
        for a in s["acquisitions"].values():
            existe("versions", a["version_id"], f"acquisition {a['acquisition_id'][:8]}", "version_id")
        for vf in s["verifications"].values():
            existe("versions", vf["version_id"], f"verification {vf['verification_id'][:8]}", "version_id")
        for d in s["human_decisions"].values():
            existe("versions", d["version_id"], f"decision {d['decision_id'][:8]}", "version_id")
            existe("versions", d["target_version_id"], f"decision {d['decision_id'][:8]}", "target_version_id")
        for i in s["ingestions"].values():
            existe("versions", i["version_id"], f"ingestion {i['ingestion_id'][:8]}", "version_id")
        for c in s["chunks"].values():
            existe("versions", c["version_id"], f"chunk {c['chunk_id'][:8]}", "version_id")
            existe("ingestions", c["ingestion_id"], f"chunk {c['chunk_id'][:8]}", "ingestion_id")
        for e in s["embeddings"].values():
            existe("chunks", e["chunk_id"], f"embedding {e['embedding_id'][:8]}", "chunk_id")
        for a in s["aliases"].values():
            existe("versions", a["canonical_version_id"], f"alias {a['alias_id'][:8]}", "canonical_version_id")
            existe("versions", a["duplicate_version_id"], f"alias {a['alias_id'][:8]}", "duplicate_version_id")
        return errores

    # ── consultas ────────────────────────────────────────────────────────

    def retrievable_versions(self) -> List[str]:
        """Único punto de lectura de Will App: I1+I2+I4 — VIGENTE + ACCEPT + INGESTADO."""
        out = []
        for ver in self._state["versions"].values():
            vid = ver["version_id"]
            if ver["state"] != VersionState.VIGENTE.value:
                continue
            if vid in self._state["aliases"]:  # duplicada: solo su canónica es recuperable
                continue
            if not any(
                d["version_id"] == vid and d["decision"] == HumanDecisionType.ACCEPT.value
                for d in self._state["human_decisions"].values()
            ):
                continue
            if not any(
                i["version_id"] == vid and i["state"] == IngestionState.INGESTADO.value
                for i in self._state["ingestions"].values()
            ):
                continue
            out.append(vid)
        return out

    def chunks_of(self, version_id: str) -> List[Dict[str, Any]]:
        return sorted(
            (c for c in self._state["chunks"].values() if c["version_id"] == version_id),
            key=lambda c: c["ordinal"],
        )

    def audit_log(self) -> List[Dict[str, Any]]:
        return list(self._state["audit_log"])

    def stats(self) -> Dict[str, int]:
        s = self._state
        return {k: len(v) if isinstance(v, dict) else len(v) for k, v in s.items()}

    # ── internos ─────────────────────────────────────────────────────────

    def _get_version(self, version_id: str) -> Dict[str, Any]:
        ver = self._state["versions"].get(version_id)
        if not ver:
            raise KnowledgeModelError(f"Version inexistente: {version_id}")
        return ver

    def _transition(self, version_id: str, nuevo: VersionState, actor: str, motivo: str = ""):
        ver = self._get_version(version_id)
        ver["estado_anterior"] = ver["state"]
        ver["state"] = nuevo.value
        ver["updated_at"] = _now()
        self._audit(actor, "transition", "Version", version_id,
                    de=ver.get("estado_anterior"), a=nuevo.value, motivo=motivo)
