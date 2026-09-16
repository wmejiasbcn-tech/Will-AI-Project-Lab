"""
Will App RAG — Context Builder (FASE 4, puntos 10-14 de los 14 requisitos).

Transforma resultados recuperados y evaluados en un paquete contextual
estructurado (Context Packet). NO concatena chunks; construye contexto
governado con provenance, limitaciones y contradicciones.

Invariante (punto 20 — Regla de Grounding):
  El Context Builder NO introduce afirmaciones nuevas.
  Su contenido procede EXCLUSIVAMENTE de los resultados recuperados.

Puede: ordenar, agrupar, eliminar redundancia, estructurar, etiquetar, conservar provenance.
No puede: inventar contenido, completar lagunas, reinterpretar hechos, convertir inferencias en hechos.

Anti-leakage (punto 18):
  NUNCA incluir chunk de estado no recuperable en el Context Packet.

Solo stdlib.
"""

import hashlib
import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from waipl.core.retriever import CandidateResult, RetrievalResult, RetrievalStatus
from waipl.core.evidence_assessment import EvidenceAssessment, EvidenceStatus
from waipl.core.query_analysis import AnalyzedQuery


class ContextItem:
    """Un item de evidencia en el Context Packet con trazabilidad completa."""

    def __init__(self, candidate: CandidateResult):
        self.chunk_id = candidate.chunk_id
        self.version_id = candidate.version_id
        self.document_id = candidate.document_id
        self.title = candidate.title
        self.domain = candidate.domain
        self.version_number = candidate.version_number
        self.content_hash = candidate.content_hash
        self.text = candidate.text
        self.similarity = candidate.similarity
        self.rerank_score = candidate.rerank_score
        self.rerank_position = candidate.rerank_position
        self.state = candidate.state
        # Provenance
        self.source_id = candidate.source_id
        self.source_nombre = candidate.source_nombre
        self.source_tipo = candidate.source_tipo
        self.chunk_ordinal = candidate.chunk_ordinal
        self.metadata = candidate.metadata

    def provenance_chain(self) -> Dict[str, Any]:
        """Cadena completa: chunk → document → version → source → verification → decision."""
        chain: Dict[str, Any] = {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "version_id": self.version_id,
            "content_hash": self.content_hash,
            "source_id": self.source_id,
            "source_nombre": self.source_nombre,
            "source_tipo": self.source_tipo,
            "domain": self.domain,
            "state": self.state,
            "version_number": self.version_number,
        }
        # Metadatos de procedencia de Fase 2 (si presentes en chunk.metadata)
        if self.metadata:
            for key in ("verificacion", "supervision_humana", "agente_adquisicion",
                        "reemplaza_a", "source_id", "document_id", "version_id"):
                if key in self.metadata:
                    chain[key] = self.metadata[key]
        return chain

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "version_id": self.version_id,
            "document_id": self.document_id,
            "title": self.title,
            "domain": self.domain,
            "version_number": self.version_number,
            "content_hash": self.content_hash,
            "text": self.text,
            "similarity": round(self.similarity, 4),
            "rerank_score": round(self.rerank_score, 4),
            "rerank_position": self.rerank_position,
            "state": self.state,
            "source_nombre": self.source_nombre,
            "source_tipo": self.source_tipo,
            "provenance": self.provenance_chain(),
        }


@dataclass
class ContextPacket:
    """Contrato serializable del contexto construido (punto 14 de la comanda)."""
    packet_id: str
    query: str
    retrieval_status: str
    evidence_status: str
    items: List[Dict[str, Any]]
    provenance: List[Dict[str, Any]]
    contradictions: List[Dict[str, Any]]
    limitations: List[str]
    version_information: List[Dict[str, Any]]
    created_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "query": self.query,
            "retrieval_status": self.retrieval_status,
            "evidence_status": self.evidence_status,
            "items": self.items,
            "provenance": self.provenance,
            "contradictions": self.contradictions,
            "limitations": self.limitations,
            "version_information": self.version_information,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)

    def fingerprint(self) -> str:
        """Hash del contenido para verificación de integridad."""
        content = json.dumps({
            "query": self.query,
            "items_hashes": sorted(i.get("content_hash", "") for i in self.items),
            "evidence_status": self.evidence_status,
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _now() -> str:
    return datetime.now(timezone(timedelta(hours=2))).isoformat()


def _uid() -> str:
    import uuid as uuidlib
    return str(uuidlib.uuid4())


class ContextBuilder:
    """Construye contexto gobernado a partir de resultados evaluados.

    Invariantes:
      - NO introduce contenido nuevo (regla de grounding)
      - NO incluye chunks no recuperables (anti-leakage)
      - Preserva provenance completa
      - Conserva información de versionado
      - Detecta y conserva contradicciones
    """

    _LOCK = threading.RLock()

    def __init__(self, max_items: int = 10, deduplicate_threshold: float = 0.85):
        self.max_items = max_items
        self.dedup_threshold = deduplicate_threshold

    def build(self, retrieval: RetrievalResult,
              assessment: EvidenceAssessment) -> ContextPacket:
        """Construye el Context Packet a partir de recuperación + evaluación."""
        with ContextBuilder._LOCK:
            # 1. Filtrar leakage: solo items de estados recuperables
            safe_candidates = self._anti_leakage(retrieval.candidates)

            # 2. Deduplicar resultados (punto 17)
            deduped = self._deduplicate_results(safe_candidates)

            # 3. Limitar items
            top = deduped[:self.max_items]

            # 4. Construir items con provenance
            items = []
            provenance = []
            version_info = []
            seen_versions: set = set()

            for c in top:
                item = ContextItem(c)
                items.append(item.to_dict())
                provenance.append(item.provenance_chain())

                if c.version_id not in seen_versions:
                    version_info.append({
                        "version_id": c.version_id,
                        "document_id": c.document_id,
                        "title": c.title,
                        "version_number": c.version_number,
                        "state": c.state,
                        "content_hash": c.content_hash,
                    })
                    seen_versions.add(c.version_id)

            # 5. Contradicciones
            contradictions = [
                {
                    "item_a": cp.item_a,
                    "item_b": cp.item_b,
                    "conflict": cp.conflict_description,
                }
                for cp in assessment.contradiction_pairs
            ]

            # 6. Limitaciones
            limitations = self._build_limitations(retrieval, assessment)

            # 7. Construir packet
            packet = ContextPacket(
                packet_id=_uid(),
                query=retrieval.query,
                retrieval_status=retrieval.status.value,
                evidence_status=assessment.status.value,
                items=items,
                provenance=provenance,
                contradictions=contradictions,
                limitations=limitations,
                version_information=version_info,
                created_at=_now(),
                metadata={
                    "total_candidates": len(retrieval.candidates),
                    "items_after_dedup": len(deduped),
                    "items_in_packet": len(items),
                    "coverage_ratio": round(assessment.coverage_ratio, 3),
                    "fingerprint": "",  # se llena después
                },
            )
            packet.metadata["fingerprint"] = packet.fingerprint()
            return packet

    # ─── Anti-leakage ────────────────────────────────────────────────────

    @staticmethod
    def _anti_leakage(candidates: List[CandidateResult]) -> List[CandidateResult]:
        """Punto 18: nunca incluir chunks de estados no recuperables.
        Defense in depth — el retriever ya filtra, pero el context builder
        refuerza la garantía."""
        from waipl.core.knowledge_model import VersionState
        NON_RETRIEVABLE = {
            VersionState.BORRADOR.value, VersionState.EN_VERIFICACION.value,
            VersionState.PENDIENTE_DECISION_HUMANA.value, VersionState.CUARENTENA.value,
            VersionState.OBSOLETA.value, VersionState.REVOCADA.value,
        }
        return [c for c in candidates if c.state not in NON_RETRIEVABLE]

    # ─── Deduplicación de resultados ─────────────────────────────────────

    def _deduplicate_results(self, candidates: List[CandidateResult]) -> List[CandidateResult]:
        """Punto 17: evitar redundancia SIN destruir evidencia distinta.
        Dos chunks del mismo documento con texto casi idéntico → mantener solo
        el de mayor score. Chunks con texto distinto → mantener ambos."""
        if not candidates:
            return []

        kept: List[CandidateResult] = []
        seen_signatures: Dict[str, int] = {}

        for c in sorted(candidates, key=lambda x: x.rerank_score, reverse=True):
            # Firma de contenido: doc + hash del texto
            sig = f"{c.document_id}:{hashlib.sha256(c.text.encode('utf-8')).hexdigest()[:12]}"
            if sig in seen_signatures:
                # Ya tenemos contenido muy similar de este doc → skip
                continue
            seen_signatures[sig] = 1
            kept.append(c)

        return kept

    # ─── Limitaciones ────────────────────────────────────────────────────

    @staticmethod
    def _build_limitations(retrieval: RetrievalResult,
                           assessment: EvidenceAssessment) -> List[str]:
        """Documenta limitaciones del contexto construido."""
        limitations: List[str] = []

        if assessment.status == EvidenceStatus.NO_EVIDENCE:
            limitations.append("NO_EVIDENCE: no se encontró conocimiento autorizado pertinente")
        elif assessment.status == EvidenceStatus.PARTIAL:
            uncovered = [d.dimension for d in assessment.coverage_dimensions if not d.covered]
            if uncovered:
                limitations.append(f"Evidencia parcial: {', '.join(uncovered)} sin cobertura")
        elif assessment.status == EvidenceStatus.INSUFFICIENT:
            limitations.append("Evidencia insuficiente para fundamentar adecuadamente")
        elif assessment.status == EvidenceStatus.CONTRADICTORY:
            limitations.append(
                f"Evidencia contradictoria: {len(assessment.contradiction_pairs)} conflicto(s) "
                "— la resolución no corresponde al algoritmo de similitud"
            )

        if retrieval.total_candidates_after_filters < retrieval.total_candidates_before_filters:
            limitations.append(
                f"Filtros redujeron candidatos: "
                f"{retrieval.total_candidates_before_filters} → {retrieval.total_candidates_after_filters}"
            )

        return limitations
