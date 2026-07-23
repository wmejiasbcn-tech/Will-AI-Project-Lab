"""
WAIPL Agente Kairos — Extractor Médico-Científico
Extrae y procesa evidencia científica de fuentes oficiales para alimentar
la base de conocimiento (RAG) de la Will App (acompañamiento no directivo / no prescriptivo).

Áreas clave:
- Salud sexual y gestión del placer.
- Consumo no problemático y reducción de riesgos/daños en sustancias psicotrópicas (Chemsex, Slam).
- Derivación a centros especializados.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger("Kairos-Extractor")


class KairosExtractor:
    def __init__(self, archivist=None):
        self.archivist = archivist
        self.extracted_count = 0

    def ingest_scientific_article(
        self,
        title: str,
        source_url: str,
        content_text: str,
        category: str = "REDUCCION_DANOS",
        evidence_level: str = "OFICIAL_MEDICO",
    ) -> Dict[str, Any]:
        """Procesa e ingesta un artículo/evidencia médico-científica extraída."""
        self.extracted_count += 1

        payload = {
            "title": title,
            "source_url": source_url,
            "category": category,
            "evidence_level": evidence_level,
            "summary": content_text[:300] + "..." if len(content_text) > 300 else content_text,
        }

        # Si el archivista Codd está disponible, registra el documento de forma oficial
        doc_record = None
        if self.archivist:
            doc_bytes = content_text.encode("utf-8")
            doc_record = self.archivist.register_document(
                filename=f"kairos_{category.lower()}_{self.extracted_count}.txt",
                content=doc_bytes,
                area="KAIROS_RAG",
                author_node="Kairos",
                metadata=payload,
            )

        logger.info(f"[Kairos] Artículo procesado: '{title}' | Categoría: {category}")
        return {
            "title": title,
            "category": category,
            "archived_record": doc_record,
            "status": "RAG_READY",
        }
