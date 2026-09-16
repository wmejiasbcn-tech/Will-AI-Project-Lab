"""
Will App RAG — Query Analysis (FASE 4, punto 1 de los 14 requisitos).

Analiza la consulta del usuario para extraer información estructurada que
dirija la recuperación gobernada. NO diagnostica ni perfila a la persona;
analiza QUÉ información se solicita, no QUIÉN la solicita.

Campos mínimos (punto 4 de la comanda):
  query, normalized_query, concepts, entities, domain, subdomain,
  territory, jurisdiction, temporal_constraints, information_intent.

Un dominio puede ser múltiple sin fusión artificial.
Solo stdlib.
"""

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class InformationIntent(str, Enum):
    DEFINITION = "DEFINITION"            # qué es X
    PROCEDURE = "PROCEDURE"              # cómo se hace X
    COMPARISON = "COMPARISON"            # X vs Y
    STATUS = "STATUS"                    # estado actual de X
    EVIDENCE = "EVIDENCE"                # qué evidencia hay sobre X
    REGULATION = "REGULATION"            # normativa sobre X
    TEMPORAL = "TEMPORAL"                # cuándo X
    GENERAL = "GENERAL"                  # no clasificable


@dataclass
class TemporalConstraint:
    after: Optional[str] = None    # ISO-8601 o año
    before: Optional[str] = None
    exact: Optional[str] = None
    raw: str = ""


@dataclass
class AnalyzedQuery:
    query: str
    normalized_query: str
    concepts: List[str]
    entities: List[str]
    domain: List[str]                     # puede ser múltiple
    subdomain: List[str]
    territory: List[str]
    jurisdiction: List[str]
    temporal_constraints: List[TemporalConstraint]
    information_intent: InformationIntent
    metadata: Dict[str, Any] = field(default_factory=dict)


# ── Patrones léxicos ──────────────────────────────────────────────────

_DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "MEDICO_CIENTIFICO_COMUNITARIO": [
        "prep", "preep", "profilaxis", "profiláctico", "vihsida", "vih",
        "antirretroviral", "tratamiento", "clínica", "paciente", "diagnóstico",
        "síntoma", "efecto adverso", "dosis", "indicación", "contraindicación",
        "evidencia", "ensayo", "estudio", "cochrane", "oms", "who",
        "salud", "epidemiología", "prevención", "vacuna", "serología",
        "carga viral", "cd4", "supresión viral", "adherencia",
    ],
    "JURIDICO_NORMATIVO": [
        "rgpd", "gdpr", "aesia", "ley", "real decreto", "boe", "normativa",
        "reglamento", "directiva", "cumplimiento", "sanción", "infracción",
        "derecho", "obligación", "protección de datos", "consentimiento",
        "responsable", "encargado", "delegado", "impacto", "evaluación",
        "legitimación", "base legal", "transferencia", "subproceso",
    ],
}

_TERRITORY_KEYWORDS = {
    "ES": ["españa", "español", "estado español", "boe", "real decreto", "nacional"],
    "EU": ["unión europea", "ue", "directiva europea", "reglamento europeo", "europeo"],
    "CAT": ["cataluña", "catalán", "generalitat"],
    "EUS": ["país vasco", "vasco", "euskadi"],
    "GAL": ["galicia", "gallego"],
}

_JURISDICTION_KEYWORDS = {
    "ES_NACIONAL": ["ley orgánica", "ley", "real decreto", "boe"],
    "EU_SUPRANACIONAL": ["directiva", "reglamento europeo", "gdpr", "rgpd"],
    "AUTONOMICO": ["decreto autonómico", "ley autonómica"],
}

_INTENT_PATTERNS: List[Tuple[InformationIntent, str]] = [
    (InformationIntent.DEFINITION, r"(?:qué es|qué significa|definición de|define|concepto de)"),
    (InformationIntent.PROCEDURE, r"(?:cómo se|cómo hacer|procedimiento|protocolo|pasos para|guía de)"),
    (InformationIntent.COMPARISON, r"(?:versus|vs\.?|comparar|diferencia entre|comparación)"),
    (InformationIntent.STATUS, r"(?:estado actual|situación de|estado de|cómo está)"),
    (InformationIntent.REGULATION, r"(?:normativa|regulación|ley sobre|reglamento|cumplimiento de|legal)"),
    (InformationIntent.TEMPORAL, r"(?:cuándo|fecha de|plazo|vigencia|desde cuándo|hasta cuándo)"),
    (InformationIntent.EVIDENCE, r"(?:evidencia|estudio sobre|datos de|prueba de|científico)"),
]

_YEAR_RE = re.compile(r"\b(19[5-9]\d|20[0-5]\d)\b")
_DATE_ISO_RE = re.compile(r"\b(\d{4}[-/]\d{2}[-/]\d{2})\b")


class QueryAnalyzer:
    """Analizador de consultas — qué información, no quién pregunta."""

    def analyze(self, query: str) -> AnalyzedQuery:
        if not query or not query.strip():
            return AnalyzedQuery(
                query=query, normalized_query="", concepts=[], entities=[],
                domain=[], subdomain=[], territory=[], jurisdiction=[],
                temporal_constraints=[], information_intent=InformationIntent.GENERAL,
            )
        nq = self._normalize(query)
        concepts = self._extract_concepts(nq)
        entities = self._extract_entities(nq)
        domains = self._detect_domains(nq)
        subdomains = self._detect_subdomains(nq, domains)
        territories = self._detect_territory(nq)
        jurisdictions = self._detect_jurisdiction(nq)
        temporal = self._detect_temporal(nq)
        intent = self._detect_intent(nq)
        return AnalyzedQuery(
            query=query, normalized_query=nq, concepts=concepts, entities=entities,
            domain=domains, subdomain=subdomains, territory=territories,
            jurisdiction=jurisdictions, temporal_constraints=temporal,
            information_intent=intent,
        )

    # ── normalización ────────────────────────────────────────────────────

    @staticmethod
    def _normalize(text: str) -> str:
        t = unicodedata.normalize("NFKD", text)
        t = t.lower().strip()
        t = re.sub(r"\s+", " ", t)
        return t

    # ── conceptos ────────────────────────────────────────────────────────

    def _extract_concepts(self, nq: str) -> List[str]:
        # Bigramas y unigramas significativos (≥4 chars), sin stopwords
        stopwords = {
            "qué", "como", "cómo", "para", "por", "con", "sin", "una", "uno",
            "unas", "unos", "del", "los", "las", "ella", "ella", "esto",
            "esta", "ese", "esa", "aquel", "aquella", "más", "menos",
            "muy", "mucho", "poco", "todo", "nada", "cada", "otro",
            "sobre", "entre", "desde", "hasta", "también", "además",
            "pero", "aunque", "sino", "ya", "no", "si", "cuando",
            "donde", "quien", "cual", "cuyo", "cuyos", "cuya", "cuyas",
            "hay", "tiene", "puede", "debe", "ser", "estar",
        }
        words = [w for w in re.findall(r"[a-záéíóúñü]+", nq) if len(w) >= 3 and w not in stopwords]
        concepts = list(dict.fromkeys(words))[:10]  # dedup, max 10
        # Bigramas si hay contexto suficiente
        for i in range(len(words) - 1):
            big = f"{words[i]} {words[i+1]}"
            if big not in concepts and len(concepts) < 15:
                concepts.append(big)
        return concepts

    def _extract_entities(self, nq: str) -> List[str]:
        # Entidades nombradas simples: acrónimos y frases clave
        entities: List[str] = []
        for m in re.finditer(r"\b[A-Z]{2,6}\b", nq.upper()):
            entities.append(m.group())
        for m in re.finditer(r"\b(?:prEP|VIH|sida|COVID|AESIA|RGPD|GDPR|BOE|OMS|WHO)\b", nq, re.IGNORECASE):
            entities.append(m.group().upper())
        return list(dict.fromkeys(entities))[:5]

    # ── dominio ──────────────────────────────────────────────────────────

    def _detect_domains(self, nq: str) -> List[str]:
        scores: Dict[str, int] = {}
        for domain, keywords in _DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in nq)
            if score > 0:
                scores[domain] = score
        if not scores:
            return []
        return sorted(scores, key=scores.get, reverse=True)

    def _detect_subdomains(self, nq: str, domains: List[str]) -> List[str]:
        subs: List[str] = []
        if "MEDICO_CIENTIFICO_COMUNITARIO" in domains:
            for kw in ["prep", "profilaxis preexposición"]:
                if kw in nq:
                    subs.append("PrEP")
            for kw in ["antirretroviral", "tratamiento arv"]:
                if kw in nq:
                    subs.append("ARV")
        if "JURIDICO_NORMATIVO" in domains:
            for kw in ["protección de datos", "rgpd", "gdpr"]:
                if kw in nq:
                    subs.append("ProtecciónDatos")
            for kw in ["aesia", "inteligencia artificial"]:
                if kw in nq:
                    subs.append("AESIA")
        return subs

    # ── territorio y jurisdicción ────────────────────────────────────────

    def _detect_territory(self, nq: str) -> List[str]:
        found = []
        for code, keywords in _TERRITORY_KEYWORDS.items():
            if any(kw in nq for kw in keywords):
                found.append(code)
        return found or ["ES"]  # default España para el ecosistema

    def _detect_jurisdiction(self, nq: str) -> List[str]:
        found = []
        for code, keywords in _JURISDICTION_KEYWORDS.items():
            if any(kw in nq for kw in keywords):
                found.append(code)
        return found

    # ── temporal ─────────────────────────────────────────────────────────

    def _detect_temporal(self, nq: str) -> List[TemporalConstraint]:
        constraints: List[TemporalConstraint] = []
        for m in _DATE_ISO_RE.finditer(nq):
            constraints.append(TemporalConstraint(exact=m.group(1), raw=m.group(0)))
        for m in _YEAR_RE.finditer(nq):
            year = m.group(1)
            if not any(c.exact and year in c.exact for c in constraints):
                constraints.append(TemporalConstraint(exact=year, raw=year))
        return constraints

    # ── intent ───────────────────────────────────────────────────────────

    def _detect_intent(self, nq: str) -> InformationIntent:
        for intent, pattern in _INTENT_PATTERNS:
            if re.search(pattern, nq):
                return intent
        return InformationIntent.GENERAL
