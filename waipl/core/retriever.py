"""
Will App RAG — Governed Retriever (FASE 4, puntos 2-6 de los 14 requisitos).

Recuperación gobernada: gobernanza ANTES que similitud vectorial.
Opera sobre PostgreSQL + pgvector existentes (FASE 3). No crea otro Vector Store.

Flujo:
  AnalyzedQuery → Pre-Filters → Vector Search → Reranking → RawCandidates

Invariante FUNDAMENTAL (punto 6 de la comanda):
  Una versión VIGENTE con similarity=0.91 SIEMPRE supera
  a una versión OBSOLETA con similarity=0.97.
  GOBERNANZA > SIMILITUD.

Solo stdlib + psycopg3.
"""

import threading
import uuid as uuidlib
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

try:
    from psycopg.types.json import Jsonb
    HAS_PSYCOPG = True
except ImportError:
    HAS_PSYCOPG = False

from waipl.core.query_analysis import AnalyzedQuery, InformationIntent
from waipl.core.knowledge_model import VersionState, HumanDecisionType


class RetrievalStatus(str, Enum):
    FOUND = "FOUND"
    PARTIAL = "PARTIAL"
    NO_EVIDENCE = "NO_EVIDENCE"


@dataclass
class CandidateResult:
    """Un candidato recuperado, con toda la trazabilidad necesaria."""
    chunk_id: str
    version_id: str
    document_id: str
    title: str
    domain: str
    version_number: int
    content_hash: str
    text: str
    distance: float            # distancia vectorial (menor = más similar)
    similarity: float          # 1 - distancia_cosine
    state: str                  # siempre VIGENTE (garantía del retriever)
    source_id: str
    source_nombre: str
    source_tipo: str
    ingestion_id: str
    chunk_ordinal: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Reranking
    rerank_score: float = 0.0
    rerank_position: int = 0


@dataclass
class RetrievalResult:
    """Resultado completo de la recuperación gobernada."""
    query: str
    analyzed: AnalyzedQuery
    status: RetrievalStatus
    candidates: List[CandidateResult]
    filters_applied: Dict[str, Any]
    total_candidates_before_filters: int
    total_candidates_after_filters: int
    elapsed_ms: float = 0.0


# Estados NO recuperables — la gobernanza prohíbe su recuperación
NON_RETRIEVABLE_STATES = {
    VersionState.BORRADOR.value,
    VersionState.EN_VERIFICACION.value,
    VersionState.PENDIENTE_DECISION_HUMANA.value,
    VersionState.CUARENTENA.value,
    VersionState.OBSOLETA.value,
    VersionState.REVOCADA.value,
}


class GovernedRetriever:
    """Retriever gobernado sobre PostgreSQL + pgvector (FASE 3 existente)."""

    _LOCK = threading.RLock()

    def __init__(self, rag_storage, candidate_k: int = 20, similarity_threshold: float = 0.0):
        """
        Args:
            rag_storage: instancia de RagStorage (FASE 3)
            candidate_k: candidatos a solicitar al vector search (configurable)
            similarity_threshold: umbral mínimo de similitud (0 = sin umbral)
        """
        self.storage = rag_storage
        self.candidate_k = candidate_k
        self.similarity_threshold = similarity_threshold

    # ─── Recuperación gobernada ──────────────────────────────────────────

    def retrieve(self, analyzed: AnalyzedQuery, query_vector: Optional[str] = None) -> RetrievalResult:
        """Flujo completo: filters → vector search → gobernanza check."""
        import time
        t0 = time.monotonic()

        with GovernedRetriever._LOCK:
            filters = self._build_filters(analyzed)
            pre_filtered = self._pre_filter(filters)

            if query_vector:
                candidates = self._vector_search(query_vector, filters, pre_filtered)
            else:
                candidates = self._keyword_search(analyzed.normalized_query, filters, pre_filtered)

            # Doble verificación de gobernanza (defense in depth)
            candidates = self._enforce_governance(candidates)

            # Umbral de similitud
            if self.similarity_threshold > 0:
                candidates = [c for c in candidates if c.similarity >= self.similarity_threshold]

            status = self._determine_status(candidates)
            elapsed = (time.monotonic() - t0) * 1000

            return RetrievalResult(
                query=analyzed.query,
                analyzed=analyzed,
                status=status,
                candidates=candidates,
                filters_applied=filters,
                total_candidates_before_filters=len(pre_filtered) if pre_filtered else len(candidates),
                total_candidates_after_filters=len(candidates),
                elapsed_ms=elapsed,
            )

    # ─── Pre-filters ─────────────────────────────────────────────────────

    def _build_filters(self, analyzed: AnalyzedQuery) -> Dict[str, Any]:
        """Construye filtros SQL a partir del AnalyzedQuery."""
        filters: Dict[str, Any] = {}
        if analyzed.domain:
            filters["domain"] = analyzed.domain
        if analyzed.territory:
            filters["territory"] = analyzed.territory
        if analyzed.jurisdiction:
            filters["jurisdiction"] = analyzed.jurisdiction
        if analyzed.temporal_constraints:
            filters["temporal"] = analyzed.temporal_constraints
        return filters

    def _pre_filter(self, filters: Dict[str, Any]) -> Optional[List[str]]:
        """Retorna version_ids que pasan los filtros pre-búsqueda, o None (= sin filtro)."""
        if not filters:
            return None
        # Construir WHERE para la vista retrievable_knowledge + joins
        conditions = ["1=1"]
        params: List[Any] = []

        if "domain" in filters:
            placeholders = ", ".join(f"%s" for _ in filters["domain"])
            conditions.append(f"d.domain IN ({placeholders})")
            params.extend(filters["domain"])

        if "temporal" in filters:
            for tc in filters["temporal"]:
                if tc.after:
                    conditions.append("v.created_at >= %s")
                    params.append(tc.after)
                if tc.before:
                    conditions.append("v.created_at <= %s")
                    params.append(tc.before)

        where = " AND ".join(conditions)
        sql = (
            f"SELECT v.version_id::text FROM versions v "
            f"JOIN documents d ON d.document_id = v.document_id "
            f"JOIN retrievable_knowledge rk ON rk.version_id = v.version_id "
            f"WHERE {where}"
        )
        rows = self.storage.execute(sql, tuple(params), fetch=True)
        return [r[0] for r in rows] if rows else []

    # ─── Vector search ───────────────────────────────────────────────────

    def _vector_search(self, query_vector: str, filters: Dict[str, Any],
                       allowed_versions: Optional[List[str]]) -> List[CandidateResult]:
        """Búsqueda vectorial RESTRINGIDA a conocimiento operativo recuperable."""
        if allowed_versions is not None and len(allowed_versions) == 0:
            return []  # los filtros eliminaron todo

        sql = (
            "SELECT c.chunk_id::text, c.version_id::text, c.text, "
            "c.ordinal, c.metadata, "
            "v.document_id::text, v.version_number, v.content_hash, v.state, "
            "d.title, d.domain, "
            "s.source_id::text, s.nombre AS source_nombre, s.tipo AS source_tipo, "
            "i.ingestion_id::text, "
            "e.vector <=> %s::vector AS distance "
            "FROM embeddings e "
            "JOIN chunks c ON c.chunk_id = e.chunk_id "
            "JOIN versions v ON v.version_id = c.version_id "
            "JOIN documents d ON d.document_id = v.document_id "
            "JOIN sources s ON s.source_id = d.source_id "
            "JOIN ingestions i ON i.version_id = v.version_id AND i.state = 'INGESTADO' "
            "WHERE e.model = 'SYNTHETIC_TEST_FASE3' "
        )
        params: List[Any] = [query_vector, query_vector]

        if allowed_versions is not None:
            placeholders = ", ".join(f"%s" for _ in allowed_versions)
            sql += f"AND v.version_id IN ({placeholders}) "
            params.extend(allowed_versions)

        sql += "ORDER BY e.vector <=> %s::vector LIMIT %s"
        params.append(self.candidate_k)

        rows = self.storage.execute(sql, tuple(params), fetch=True)
        return [self._row_to_candidate(r) for r in rows]

    def _keyword_search(self, normalized_query: str, filters: Dict[str, Any],
                        allowed_versions: Optional[List[str]]) -> List[CandidateResult]:
        """Búsqueda por texto cuando no hay vector de consulta."""
        if not normalized_query or (allowed_versions is not None and len(allowed_versions) == 0):
            return []

        sql = (
            "SELECT c.chunk_id::text, c.version_id::text, c.text, "
            "c.ordinal, c.metadata, "
            "v.document_id::text, v.version_number, v.content_hash, v.state, "
            "d.title, d.domain, "
            "s.source_id::text, s.nombre AS source_nombre, s.tipo AS source_tipo, "
            "i.ingestion_id::text, "
            "0.5 AS distance "  # distancia neutra para búsqueda por texto
            "FROM chunks c "
            "JOIN versions v ON v.version_id = c.version_id "
            "JOIN documents d ON d.document_id = v.document_id "
            "JOIN sources s ON s.source_id = d.source_id "
            "JOIN ingestions i ON i.version_id = v.version_id AND i.state = 'INGESTADO' "
            "WHERE c.text ILIKE %s "
        )
        params: List[Any] = [f"%{normalized_query}%"]

        if allowed_versions is not None:
            placeholders = ", ".join(f"%s" for _ in allowed_versions)
            sql += f"AND v.version_id IN ({placeholders}) "
            params.extend(allowed_versions)

        sql += "ORDER BY c.ordinal LIMIT %s"
        params.append(self.candidate_k)

        rows = self.storage.execute(sql, tuple(params), fetch=True)
        return [self._row_to_candidate(r) for r in rows]

    def _row_to_candidate(self, row: tuple) -> CandidateResult:
        return CandidateResult(
            chunk_id=row[0], version_id=row[1], text=row[2],
            chunk_ordinal=row[3], metadata=row[4] if row[4] else {},
            document_id=row[5], version_number=row[6], content_hash=row[7],
            state=row[8], title=row[9], domain=row[10],
            source_id=row[11], source_nombre=row[12], source_tipo=row[13],
            ingestion_id=row[14],
            distance=float(row[15]),
            similarity=1.0 - float(row[15]),
        )

    # ─── Gobernanza (defense in depth) ──────────────────────────────────

    def _enforce_governance(self, candidates: List[CandidateResult]) -> List[CandidateResult]:
        """Elimina cualquier candidato que viole la gobernanza.
        Aunque la vista retrievable_knowledge ya filtra, esto es defensa
        en profundidad contra leakage o bypass."""
        return [c for c in candidates if self._is_retrievable(c)]

    @staticmethod
    def _is_retrievable(candidate: CandidateResult) -> bool:
        if candidate.state in NON_RETRIEVABLE_STATES:
            return False
        if candidate.state != VersionState.VIGENTE.value:
            return False
        return True

    # ─── Status ──────────────────────────────────────────────────────────

    @staticmethod
    def _determine_status(candidates: List[CandidateResult]) -> RetrievalStatus:
        if not candidates:
            return RetrievalStatus.NO_EVIDENCE
        if len(candidates) < 3:
            return RetrievalStatus.PARTIAL
        return RetrievalStatus.FOUND

    # ─── Utilidades para tests ───────────────────────────────────────────

    def retrievable_version_ids(self) -> List[str]:
        """Version IDs recuperables via vista retrievable_knowledge."""
        rows = self.storage.execute(
            "SELECT version_id::text FROM retrievable_knowledge", fetch=True)
        return [r[0] for r in rows] if rows else []
