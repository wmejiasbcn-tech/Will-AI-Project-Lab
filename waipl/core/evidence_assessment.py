"""
Will App RAG — Evidence Assessment (FASE 4, puntos 6-9 de los 14 requisitos).

Evalúa la suficiencia de la evidencia recuperada para la consulta.
NO diagnostica, prescribe ni decide. Evalúa si la evidencia es suficiente
para FUNDAMENTAR, no para CONCLUIR.

Estados (punto 9 de la comanda):
  SUFFICIENT    — la evidencia permite fundamentar razonablemente
  PARTIAL       — existe pero no cubre completamente
  INSUFFICIENT  — material relacionado pero no alcanza
  NO_EVIDENCE   — no existe conocimiento pertinente autorizado
  CONTRADICTORY — evidencia relevante incompatible que no debe ocultarse

Principio de ausencia (punto 10):
  NO_EVIDENCE es un resultado VÁLIDO.
  NO_EVIDENCIA ≠ PERMISO PARA FABRICAR.

Principio de parcialidad (punto 11):
  A → cubierto, B → cubierto, C → no cubierto
  sin falsar completitud.

Principio de contradicción (punto 12):
  Fuente A → X, Fuente B → ¬X
  → CONTRADICTORY, conservar ambas con provenance,
  NO resolver por max(similarity), NO fabricar síntesis.

Solo stdlib.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from waipl.core.retriever import CandidateResult
from waipl.core.query_analysis import AnalyzedQuery


class EvidenceStatus(str, Enum):
    SUFFICIENT = "SUFFICIENT"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"
    NO_EVIDENCE = "NO_EVIDENCE"
    CONTRADICTORY = "CONTRADICTORY"


@dataclass
class ContradictionPair:
    """Dos piezas de evidencia contradictoria con sus provenances."""
    item_a: Dict[str, Any]
    item_b: Dict[str, Any]
    conflict_description: str


@dataclass
class CoverageDimension:
    """Cobertura por dimensión de la consulta."""
    dimension: str
    covered: bool
    evidence_ids: List[str] = field(default_factory=list)
    reason: str = ""


@dataclass
class EvidenceAssessment:
    """Resultado completo de la evaluación de evidencia."""
    status: EvidenceStatus
    coverage_dimensions: List[CoverageDimension]
    sufficient_threshold: float
    coverage_ratio: float         # dimensiones cubiertas / total
    contradiction_pairs: List[ContradictionPair]
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class EvidenceAssessor:
    """Evalúa suficiencia, parcialidad, ausencia y contradicción."""

    def __init__(self, sufficient_threshold: float = 0.7,
                 contradiction_similarity_threshold: float = 0.6):
        """
        Args:
            sufficient_threshold: ratio de cobertura para considerar SUFFICIENT
            contradiction_similarity_threshold: similitud mínima para considerar
                dos chunks como candidatos a contradicción
        """
        self.sufficient_threshold = sufficient_threshold
        self.contradiction_sim_threshold = contradiction_similarity_threshold

    def assess(self, analyzed: AnalyzedQuery, candidates: List[CandidateResult]) -> EvidenceAssessment:
        """Evalúa la evidencia recuperada contra la consulta."""
        # 1. Sin candidatos → NO_EVIDENCE
        if not candidates:
            return EvidenceAssessment(
                status=EvidenceStatus.NO_EVIDENCE,
                coverage_dimensions=[], sufficient_threshold=self.sufficient_threshold,
                coverage_ratio=0.0, contradiction_pairs=[],
                reason="No se recuperó conocimiento autorizado pertinente",
            )

        # 2. Evaluar cobertura por dimensiones de la consulta
        dimensions = self._evaluate_coverage(analyzed, candidates)
        total = len(dimensions) if dimensions else 1
        covered = sum(1 for d in dimensions if d.covered)
        ratio = covered / total

        # 3. Detectar contradicciones
        contradictions = self._detect_contradictions(candidates)

        # 4. Determinar estado
        if contradictions:
            status = EvidenceStatus.CONTRADICTORY
            reason = f"Evidencia contradictoria detectada ({len(contradictions)} pares)"
        elif ratio >= self.sufficient_threshold:
            status = EvidenceStatus.SUFFICIENT
            reason = f"Cobertura {ratio:.0%} ≥ umbral {self.sufficient_threshold:.0%}"
        elif ratio > 0:
            status = EvidenceStatus.PARTIAL if covered > 0 else EvidenceStatus.INSUFFICIENT
            uncovered = [d.dimension for d in dimensions if not d.covered]
            reason = f"Cobertura {ratio:.0%} < umbral; no cubierto: {', '.join(uncovered)}"
        else:
            status = EvidenceStatus.INSUFFICIENT
            reason = "Material relacionado pero insuficiente para fundamentar"

        return EvidenceAssessment(
            status=status, coverage_dimensions=dimensions,
            sufficient_threshold=self.sufficient_threshold,
            coverage_ratio=ratio, contradiction_pairs=contradictions,
            reason=reason,
        )

    # ── Cobertura por dimensiones ────────────────────────────────────────

    def _evaluate_coverage(self, analyzed: AnalyzedQuery,
                           candidates: List[CandidateResult]) -> List[CoverageDimension]:
        """Evalúa qué aspectos de la consulta están cubiertos."""
        dimensions: List[CoverageDimension] = []

        # Dimensión: dominio(s) solicitados
        if analyzed.domain:
            for dom in analyzed.domain:
                covered_ids = [c.chunk_id for c in candidates if c.domain == dom]
                dimensions.append(CoverageDimension(
                    dimension=f"domain:{dom}",
                    covered=len(covered_ids) > 0,
                    evidence_ids=covered_ids,
                    reason=f"{'Cubierto' if covered_ids else 'Sin evidencia'} en dominio {dom}",
                ))

        # Dimensión: conceptos clave
        if analyzed.concepts:
            for concept in analyzed.concepts[:5]:  # top 5
                covered_ids = [
                    c.chunk_id for c in candidates
                    if concept.lower() in c.text.lower()
                ]
                dimensions.append(CoverageDimension(
                    dimension=f"concept:{concept}",
                    covered=len(covered_ids) > 0,
                    evidence_ids=covered_ids,
                ))

        # Si no hay dimensiones explícitas, cobertura simple por existencia
        if not dimensions:
            dimensions.append(CoverageDimension(
                dimension="general",
                covered=len(candidates) > 0,
                evidence_ids=[c.chunk_id for c in candidates[:3]],
            ))

        return dimensions

    # ── Detección de contradicciones ─────────────────────────────────────

    def _detect_contradictions(self, candidates: List[CandidateResult]) -> List[ContradictionPair]:
        """Detecta pares de evidencia que se contradicen.
        Heurística: mismo documento/dominio pero texto con negaciones mutuas."""
        pairs: List[ContradictionPair] = []

        # Patrones de negación en español
        negation_patterns = [
            (r"\bno\s+(?:es|está|se|debe|puede|recomienda|indica)\b",
             r"\b(?:es|está|se|debe|puede|recomienda|indica)\b"),
            (r"\bcontraindicad[oa]\b", r"\b(?:indicad[oa]|se indica)\b"),
            (r"\bprohibid[oa]\b", r"\bpermitid[oa]\b"),
            (r"\bno\s+recomienda\b", r"\brecomienda\b"),
            (r"\bestá contraindicad[oa]\b", r"\bse indica\b"),
        ]

        for i, a in enumerate(candidates):
            for b in candidates[i + 1:]:
                if a.version_id == b.version_id:
                    continue  # mismo documento, no contradictorio
                for neg_pat, aff_pat in negation_patterns:
                    a_has_neg = bool(re.search(neg_pat, a.text, re.IGNORECASE))
                    a_has_aff = bool(re.search(aff_pat, a.text, re.IGNORECASE))
                    b_has_neg = bool(re.search(neg_pat, b.text, re.IGNORECASE))
                    b_has_aff = bool(re.search(aff_pat, b.text, re.IGNORECASE))

                    # A niega lo que B afirma o viceversa
                    if (a_has_neg and b_has_aff) or (a_has_aff and b_has_neg):
                        # Solo si ambos tienen similitud suficiente
                        if a.similarity >= self.contradiction_sim_threshold and \
                           b.similarity >= self.contradiction_sim_threshold:
                            pairs.append(ContradictionPair(
                                item_a=self._candidate_to_provenance_dict(a),
                                item_b=self._candidate_to_provenance_dict(b),
                                conflict_description="Negación mutua detectada",
                            ))
                            break
                if len(pairs) >= 5:
                    break  # límite razonable
            if len(pairs) >= 5:
                break

        return pairs

    @staticmethod
    def _candidate_to_provenance_dict(c: CandidateResult) -> Dict[str, Any]:
        return {
            "chunk_id": c.chunk_id,
            "version_id": c.version_id,
            "document_id": c.document_id,
            "title": c.title,
            "text_preview": c.text[:200],
            "source_nombre": c.source_nombre,
            "source_tipo": c.source_tipo,
            "domain": c.domain,
            "similarity": c.similarity,
        }
