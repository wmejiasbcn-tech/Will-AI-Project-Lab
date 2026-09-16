"""
WAIPL Agente Kairos — Especialista en el ámbito médico-científico y comunitario.

Posee COMPETENCIA sobre el dominio que trata; no se limita a ser un extractor/recolector.
Ámbito de actuación: Will App y ecosistema WAIPL. Sus funciones comprenden: identificación,
recopilación/adquisición, extracción, estructuración, contextualización y mantenimiento de
procedencia y trazabilidad de la información médico-científica y comunitaria.

NO es gate. Sus resultados quedan sometidos a la verificación independiente de Vár y a la
supervisión humana antes de incorporarse al conocimiento canónico del WILL RAG
(RAG de Will App; acompañamiento no directivo / no prescriptivo).

Regla general de especialización: «Los agentes especializados deben poseer competencia sobre
el dominio en el que operan; la especialización no elimina la necesidad de verificación
independiente.»

Áreas clave:
- Salud sexual y gestión del placer.
- Consumo no problemático y reducción de riesgos/daños en sustancias psicotrópicas (Chemsex, Slam).
- Derivación a centros especializados.
"""

import logging
from typing import Any, Dict, List

from waipl.core.rag_pipeline import DOMINIO_MEDICO

logger = logging.getLogger("Kairos-Extractor")


class KairosExtractor:
    def __init__(self, archivist=None, pipeline=None):
        """
        Args:
            archivist: Codd (GDO-01) para registro oficial de documentos.
            pipeline: RAGPipeline (opcional). Si está presente, cada unidad extraída
                se somete al ciclo reconciliado: especialista (Kairos) → verificación
                independiente (Vár) → auditoría de validadores (Yata, cuando corresponda)
                → supervisión humana. Kairos NO es gate; el estado devuelto es el del
                ciclo de admisión, nunca "RAG_READY" directo.
        """
        self.archivist = archivist
        self.pipeline = pipeline
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

        # Ciclo de admisión reconciliado: especialista → Vár → Yata (cuando corresponda)
        # → supervisión humana. Kairos no decide la admisión.
        if self.pipeline is not None and doc_record:
            unit = self.pipeline.submit_knowledge_unit(
                title=title,
                source_url=source_url,
                content_text=content_text,
                category=category,
                evidence_level=evidence_level,
                doc_record=doc_record,
                dominio=DOMINIO_MEDICO,
            )
            return {
                "title": title,
                "category": category,
                "archived_record": doc_record,
                "status": unit["estado"],
                "pipeline_record": unit,
            }

        # Sin pipeline: no se marca como apto (la admisión requiere verificación + supervisión).
        return {
            "title": title,
            "category": category,
            "archived_record": doc_record,
            "status": "PENDIENTE_VERIFICACION",
        }
