"""
WAIPL Agente Codd — GDO-01 "Archivista y Gestor del Explorador de Archivos"
Encargado de organizar de forma óptima y eficiente el sistema de archivos del Nodo Central:
- Asignación de UUID v4 único por documento.
- Cálculo de hash SHA-256 para trazabilidad e integridad.
- Organización de carpetas estructuradas.
- Indexación de metadatos e integración con la base de datos RAG.
"""

import hashlib
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger("Codd-GDO-01")


class CoddArchivist:
    def __init__(self, base_storage_dir: str = r"C:\Users\USER\Desktop\AutoClaw\docs"):
        self.base_storage_dir = base_storage_dir
        self._ensure_storage_structure()
        self.catalog_file = os.path.join(self.base_storage_dir, "document_catalog.json")
        self._catalog = self._load_catalog()

    def _ensure_storage_structure(self):
        """Crea la estructura de carpetas base del sistema documental."""
        years_dir = os.path.join(self.base_storage_dir, datetime.now().strftime("%Y"), datetime.now().strftime("%m"))
        os.makedirs(years_dir, exist_ok=True)

    def _load_catalog(self) -> Dict[str, Any]:
        """Carga el catálogo documental existente."""
        if os.path.exists(self.catalog_file):
            try:
                with open(self.catalog_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error cargando catálogo: {e}")
        return {}

    def _save_catalog(self):
        """Guarda el catálogo documental en disco."""
        with open(self.catalog_file, "w", encoding="utf-8") as f:
            json.dump(self._catalog, f, indent=2, ensure_ascii=False)

    def calculate_sha256(self, file_bytes: bytes) -> str:
        """Calcula la firma digital SHA-256 del contenido."""
        return hashlib.sha256(file_bytes).hexdigest()

    def register_document(
        self,
        filename: str,
        content: bytes,
        area: str = "GENERAL",
        author_node: str = "NÚCLEO",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Registra e indexa un nuevo documento en el sistema del Nodo Central."""
        doc_uuid = str(uuid.uuid4())
        file_hash = self.calculate_sha256(content)
        timestamp = datetime.utcnow().isoformat()

        # Determinar ruta de almacenamiento
        now = datetime.now()
        relative_folder = os.path.join(area.upper(), now.strftime("%Y"), now.strftime("%m"))
        target_folder = os.path.join(self.base_storage_dir, relative_folder)
        os.makedirs(target_folder, exist_ok=True)

        _, ext = os.path.splitext(filename)
        safe_filename = f"{doc_uuid}{ext if ext else '.bin'}"
        target_path = os.path.join(target_folder, safe_filename)

        # Escribir archivo en disco
        with open(target_path, "wb") as f:
            f.write(content)

        doc_record = {
            "uuid": doc_uuid,
            "original_filename": filename,
            "stored_path": target_path,
            "sha256": file_hash,
            "size_bytes": len(content),
            "area": area,
            "author_node": author_node,
            "timestamp": timestamp,
            "metadata": metadata or {},
        }

        self._catalog[doc_uuid] = doc_record
        self._save_catalog()

        logger.info(f"[Codd-GDO-01] Documento archivado con éxito: UUID={doc_uuid} | SHA256={file_hash[:8]}...")
        return doc_record

    def get_document(self, doc_uuid: str) -> Optional[Dict[str, Any]]:
        """Obtiene la Ficha Documental de un archivo indexado."""
        return self._catalog.get(doc_uuid)
