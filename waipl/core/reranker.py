"""
Will App RAG — Reranking (FASE 4, punto 5 de los 14 requisitos).

Capa separada que reordena candidatos ya autorizados para recuperación.
NO puede saltarse los filtros de gobernanza: trabaja SOLO sobre
candidatos que ya pasaron el Governed Retriever.

Factores de ranking:
  - similitud vectorial
  - correspondencia conceptual con la consulta
  - dominio/subdominio
  - calidad/autoridad de fuente
  - pertinencia temática
  - penalización por redundancia

Solo stdlib.
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List

from waipl.core.retriever import CandidateResult
from waipl.core.query_analysis import AnalyzedQuery, InformationIntent


@dataclass
class RerankConfig:
    """Configuración del reranker — todos los pesos son ajustables."""
    weight_similarity: float = 0.40
    weight_domain_match: float = 0.20
    weight_source_quality: float = 0.15
    weight_concept_overlap: float = 0.15
    weight_recency: float = 0.10
    # Calidad de fuente por tipo
    source_quality: Dict[str, float] = None  # se inicializa en __post_init__

    def __post_init__(self):
        if self.source_quality is None:
            self.source_quality = {
                "normativa_oficial": 1.0,
                "revista_indexada": 0.95,
                "BOE": 1.0,
                "OMS": 0.95,
                "who": 0.95,
                "guia_clinica": 0.90,
                "informe_tecnico": 0.80,
                "organismo_publico": 0.85,
                "default": 0.60,
            }


class Reranker:
    """Reordena candidatos autorizados. Nunca reintroduce no-recuperables."""

    def __init__(self, config: RerankConfig = None):
        self.config = config or RerankConfig()

    def rerank(self, analyzed: AnalyzedQuery, candidates: List[CandidateResult]) -> List[CandidateResult]:
        """Reordena candidatos. Los no-recuperables ya fueron excluidos por
        el Governed Retriever; este método NO los reintroduce."""
        if not candidates:
            return []

        scored = []
        for c in candidates:
            score = self._compute_score(analyzed, c)
            c.rerank_score = score
            scored.append(c)

        # Ordenar por score descendente
        scored.sort(key=lambda c: c.rerank_score, reverse=True)

        # Penalizar redundancia: si dos chunks son del mismo documento
        # y texto muy similar, el segundo baja
        scored = self._penalize_redundancy(scored)

        # Asignar posición
        for i, c in enumerate(scored, start=1):
            c.rerank_position = i

        return scored

    def _compute_score(self, analyzed: AnalyzedQuery, candidate: CandidateResult) -> float:
        cfg = self.config

        # 1. Similitud
        sim_score = candidate.similarity

        # 2. Correspondencia de dominio
        domain_score = 0.5  # neutro
        if analyzed.domain and candidate.domain in analyzed.domain:
            domain_score = 1.0
        elif analyzed.domain:
            domain_score = 0.3  # dominio distinto

        # 3. Calidad de fuente
        source_type = candidate.source_tipo or "default"
        quality_score = cfg.source_quality.get(source_type, cfg.source_quality["default"])

        # 4. Solapamiento conceptual
        concept_score = self._concept_overlap(analyzed.concepts, candidate.text)

        # 5. Recencia (normalizada: más reciente = mejor)
        recency_score = 0.5  # neutro si no hay info temporal

        # Puntuación compuesta
        total = (
            cfg.weight_similarity * sim_score +
            cfg.weight_domain_match * domain_score +
            cfg.weight_source_quality * quality_score +
            cfg.weight_concept_overlap * concept_score +
            cfg.weight_recency * recency_score
        )
        return total

    @staticmethod
    def _concept_overlap(concepts: List[str], text: str) -> float:
        if not concepts or not text:
            return 0.0
        text_lower = text.lower()
        hits = sum(1 for c in concepts if c.lower() in text_lower)
        return min(hits / max(len(concepts), 1), 1.0)

    @staticmethod
    def _penalize_redundancy(candidates: List[CandidateResult], penalty: float = 0.15) -> List[CandidateResult]:
        """Si chunks del mismo documento tienen texto muy similar, penaliza el segundo."""
        seen_signatures: Dict[str, int] = {}
        for c in candidates:
            # Firma: doc + primeros 80 chars del texto
            sig = f"{c.document_id}:{c.text[:80]}"
            if sig in seen_signatures:
                c.rerank_score -= penalty * seen_signatures[sig]
                seen_signatures[sig] += 1
            else:
                seen_signatures[sig] = 1
        # Re-ordenar tras penalización
        candidates.sort(key=lambda c: c.rerank_score, reverse=True)
        return candidates
