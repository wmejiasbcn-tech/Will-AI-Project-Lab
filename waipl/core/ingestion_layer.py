"""
Will App RAG — Ingestion Layer (FASE 2, Orden Soberana v0.3.1).

Capa que transforma conocimiento canónico autorizado en unidades preparadas
para su posterior indexación RAG. Opera EXCLUSIVAMENTE sobre el estado del
modelo de conocimiento (knowledge_model.py, FASE 1).

REGLA CRÍTICA: la existencia de un documento en Codd / Ariadna / Sylvia /
el archivo documental o cualquier otra ubicación NUNCA equivale a autorización
para el RAG. Solo el estado canónico (VIGENTE + HumanDecision ACCEPT + cadena
de procedencia completa) autoriza la ingesta.

Rechazo absoluto de los estados: BORRADOR, EN_VERIFICACION,
PENDIENTE_DECISION_HUMANA, CUARENTENA (rechazada), OBSOLETA y REVOCADA.

Operaciones idempotentes: re-ingerir una versión ya ingestado devuelve la
ingesta existente sin duplicar chunks ni embeddings. Deduplicación por
content_hash → ALIAS (nunca embeddings nuevos). Escritura segura (atomic +
lock heredados del modelo). Trazabilidad completa vía AuditLog (incluidos
bloqueos y rechazos de la propia capa).

Prohibido en FASE 2: PostgreSQL/pgvector, embeddings productivos, retriever,
conexión con Will App, producción. Los embeddings se registran como
referencias pendientes (vector_ref=None) para FASE 3.

Solo stdlib.
"""

import re
import threading
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from waipl.core.knowledge_model import (
    KnowledgeStore,
    VersionState,
    IngestionState,
    HumanDecisionType,
    KnowledgeModelError,
)


class IngestionBlockedError(KnowledgeModelError):
    """La capa de ingesta bloquea la operación (estado/procedencia/regla crítica)."""
    def __init__(self, motivo: str, veredicto: Optional["AdmissibilityVerdict"] = None):
        super().__init__(motivo)
        self.veredicto = veredicto


class ArchiveNotAuthorizedError(KnowledgeModelError):
    """Regla crítica: el Archivo Documental no autoriza ingesta."""


# Estados con rechazo ABSOLUTO (Orden Soberana v0.3.1 — FASE 2)
ESTADOS_PROHIBIDOS = {
    VersionState.REVOCADA.value: "REVOCADA (retirada expresamente)",
    VersionState.CUARENTENA.value: "CUARENTENA (rechazada por decisión humana)",
    VersionState.PENDIENTE_DECISION_HUMANA.value: "PENDIENTE_DECISION_HUMANA (falta supervisión humana)",
    VersionState.EN_VERIFICACION.value: "EN_VERIFICACION (verificación incompleta)",
    VersionState.BORRADOR.value: "BORRADOR (nunca verificado)",
    VersionState.OBSOLETA.value: "OBSOLETA (sustituida por versión posterior)",
}


@dataclass
class AdmissibilityVerdict:
    admisible: bool
    accion: str            # INGESTAR | ALIAS | YA_INGESTADO | BLOQUEO
    estado: str
    motivo: str
    canonical_version_id: Optional[str] = None


class IngestionLayer:
    """Puerta de entrada al RAG: solo conocimiento canónico autorizado y vigente."""

    _LOCK = threading.RLock()  # serializa ingestas intra-proceso (idempotencia bajo concurrencia)

    def __init__(self, store: KnowledgeStore, chunk_max_chars: int = 1200, actor: str = "IngestionLayer"):
        self.store = store
        self.chunk_max_chars = chunk_max_chars
        self.actor = actor

    # ──────────────────────────────────────────────────────────────────────
    # Admisibilidad
    # ──────────────────────────────────────────────────────────────────────

    def check_admissibility(
        self,
        version_id: str,
        content_text: Optional[str] = None,
        verify_content: bool = False,
    ) -> AdmissibilityVerdict:
        """Verifica el estado canónico y la autorización ANTES de ingerir (I1-I5).
        La existencia en el archivo jamás es criterio: solo el modelo canónico."""
        s = self.store._state
        ver = s["versions"].get(version_id)
        if not ver:
            return AdmissibilityVerdict(False, "BLOQUEO", "INEXISTENTE",
                                        "La versión no existe en el modelo canónico: no hay autorización")
        estado = ver["state"]
        if estado != VersionState.VIGENTE.value:
            motivo = ESTADOS_PROHIBIDOS.get(estado, f"estado {estado} no autorizado")
            return AdmissibilityVerdict(False, "BLOQUEO", estado,
                                        f"Rechazo absoluto: {motivo}")
        if not any(
            d["version_id"] == version_id and d["decision"] == HumanDecisionType.ACCEPT.value
            for d in s["human_decisions"].values()
        ):
            return AdmissibilityVerdict(False, "BLOQUEO", estado,
                                        "Sin HumanDecision = ACCEPT: el principio absoluto prohíbe la ingesta")
        if not any(a["version_id"] == version_id for a in s["acquisitions"].values()):
            return AdmissibilityVerdict(False, "BLOQUEO", estado,
                                        "Procedencia de adquisición ausente (sin Acquisition)")
        if not any(v["version_id"] == version_id for v in s["verifications"].values()):
            return AdmissibilityVerdict(False, "BLOQUEO", estado,
                                        "Verificación de dominio ausente (sin Verification)")
        if verify_content and content_text is not None:
            import hashlib
            h = hashlib.sha256(content_text.encode("utf-8")).hexdigest()
            if h != ver["content_hash"]:
                return AdmissibilityVerdict(False, "BLOQUEO", estado,
                                            "Procedencia alterada: el content_hash no coincide con el contenido actual (I)")
        if not ver.get("stored_path"):
            return AdmissibilityVerdict(False, "BLOQUEO", estado,
                                        "Procedencia primaria ausente: versión sin stored_path")

        # Deduplicación (I3): otro VIGENTE ya ingerido con el mismo hash → ALIAS
        canonical = self.store.find_canonical(ver["content_hash"])
        if canonical and canonical != version_id:
            ya_ingestada = any(
                i["version_id"] == canonical and i["state"] == IngestionState.INGESTADO.value
                for i in s["ingestions"].values()
            )
            if ya_ingestada:
                return AdmissibilityVerdict(False, "ALIAS", estado,
                                            f"Duplicado de {canonical[:8]}...: ALIAS sin nuevos embeddings (I3)",
                                            canonical_version_id=canonical)

        # Idempotencia (J): ingesta activa previa → devolver la existente
        for i in s["ingestions"].values():
            if i["version_id"] == version_id and i["state"] == IngestionState.INGESTADO.value:
                return AdmissibilityVerdict(True, "YA_INGESTADO", estado,
                                            f"Ya ingestado (idempotente): {i['ingestion_id'][:8]}...")
        return AdmissibilityVerdict(True, "INGESTAR", estado, "Autorizada: VIGENTE + ACCEPT + procedencia completa")

    # ──────────────────────────────────────────────────────────────────────
    # Ingesta canónica (idempotente)
    # ──────────────────────────────────────────────────────────────────────

    def ingest_canonical(
        self,
        version_id: str,
        structure: Optional[Dict[str, Any]] = None,
        content_text: Optional[str] = None,
        verify_content: bool = False,
        actor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Punto único de ingesta del conocimiento canónico. Idempotente."""
        with IngestionLayer._LOCK:
            verdict = self.check_admissibility(version_id, content_text=content_text, verify_content=verify_content)
            if verdict.accion == "YA_INGESTADO":
                ing = next(i for i in self.store._state["ingestions"].values()
                           if i["version_id"] == version_id and i["state"] == IngestionState.INGESTADO.value)
                self.store.log_event(self.actor, "ingest_idempotent", "Ingestion", ing["ingestion_id"],
                                     version_id=version_id)
                return {"accion": "YA_INGESTADO", "ingestion_id": ing["ingestion_id"],
                        "chunks": ing["chunk_count"], "idempotente": True, "veredicto": verdict}
            if verdict.accion == "ALIAS":
                alias_id = self.store.make_alias(version_id, verdict.canonical_version_id,
                                                 actor=actor or self.actor)
                return {"accion": "ALIAS", "alias_id": alias_id,
                        "canonical_version_id": verdict.canonical_version_id,
                        "embeddings_nuevos": 0, "veredicto": verdict}
            if not verdict.admisible:
                self.store.log_event(self.actor, "ingest_blocked", "Version", version_id,
                                     estado=verdict.estado, motivo=verdict.motivo)
                raise IngestionBlockedError(verdict.motivo, verdict)

            # Procedencia primaria → metadatos de procedencia en cada chunk (FASE 2)
            procedencia = self._procedencia(version_id)
            estructura = structure or ({"texto": content_text} if content_text else None)
            if estructura is None:
                estructura = self._leer_archivo(version_id)
            chunks = self.prepare_chunks(estructura)
            if not chunks:
                self.store.log_event(self.actor, "ingest_blocked", "Version", version_id,
                                     estado=verdict.estado, motivo="Sin chunks tras la preparación")
                raise IngestionBlockedError("La preparación no produjo chunks: nada que ingerir")

            ing_id = self.store.ingest(
                version_id,
                chunk_texts=[c["texto"] for c in chunks],
                chunk_metadata=[{**c["metadata"], **procedencia} for c in chunks],
                actor=actor or self.actor,
            )
            self.store.log_event(self.actor, "ingest_canonical", "Ingestion", ing_id,
                                 version_id=version_id, chunks=len(chunks))
            return {"accion": "INGESTADO", "ingestion_id": ing_id, "chunks": len(chunks),
                    "idempotente": False, "veredicto": verdict}

    def _procedencia(self, version_id: str) -> Dict[str, Any]:
        """Procedencia primaria + Vár + Yata (si procede) + supervisión humana."""
        s = self.store._state
        ver = s["versions"][version_id]
        doc = s["documents"][ver["document_id"]]
        proc: Dict[str, Any] = {
            "source_id": doc["source_id"],
            "document_id": ver["document_id"],
            "version_id": version_id,
            "version_number": ver["version_number"],
            "content_hash": ver["content_hash"],
            "domain": doc["domain"],
            "reemplaza_a": ver.get("supersedes_version_id"),
        }
        for a in s["acquisitions"].values():
            if a["version_id"] == version_id:
                proc["agente_adquisicion"] = a["agent"]
        for vf in s["verifications"].values():
            if vf["version_id"] == version_id:
                proc["verificacion"] = {"verifier": vf["verifier"], "result": vf["result"],
                                        "confidence": vf["confidence"], "dictamen_id": vf["dictamen_id"],
                                        "auditor": vf["auditor"]}  # auditor = Yata si procede
        for d in s["human_decisions"].values():
            if d["version_id"] == version_id:
                proc["supervision_humana"] = {"human_reviewer_id": d["human_reviewer_id"],
                                              "decision": d["decision"],
                                              "decision_timestamp": d["decision_timestamp"],
                                              "decision_reason": d["decision_reason"]}
        return proc

    def _leer_archivo(self, version_id: str) -> Dict[str, Any]:
        from pathlib import Path
        ver = self.store._state["versions"][version_id]
        p = Path(ver["stored_path"])
        if not p.is_file():
            raise IngestionBlockedError(f"Contenido canónico no accesible: {ver['stored_path']}")
        return {"texto": p.read_text(encoding="utf-8")}

    # ──────────────────────────────────────────────────────────────────────
    # Regla crítica: archivo documental ≠ autorización
    # ──────────────────────────────────────────────────────────────────────

    def ingest_from_archive(self, **kwargs) -> None:
        """PROHIBIDO. La existencia en el Archivo Documental (Codd/Ariadna/Sylvia)
        o en cualquier ubicación NUNCA autoriza la ingesta. Este método existe
        para demostrar en pruebas que el intento se bloquea y se audita."""
        self.store.log_event(self.actor, "archive_ingestion_refused", "Policy", "ingest_from_archive",
                             motivo="La existencia documental no equivale a autorización para RAG")
        raise ArchiveNotAuthorizedError(
            "REGLA CRÍTICA: el Archivo Documental no autoriza la ingesta. "
            "Solo el estado canónico (VIGENTE + HumanDecision ACCEPT) del modelo de conocimiento autoriza."
        )

    # ──────────────────────────────────────────────────────────────────────
    # Chunking con preservación de estructura multimodal (K)
    # ──────────────────────────────────────────────────────────────────────

    def prepare_chunks(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convierte estructura canónica en chunks SIN destruir relaciones
        semánticas: tablas/figuras atómicas, notas enlazadas, referencias
        preservadas, párrafos divididos solo por fronteras de frase."""
        if not isinstance(structure, dict):
            raise KnowledgeModelError("Estructura inválida: se espera un dict canónico")
        secciones = structure.get("secciones")
        if not secciones:
            texto = structure.get("texto", "")
            if not texto or not str(texto).strip():
                return []
            secciones = [{"tipo": "parrafo", "texto": str(texto)}]

        chunks: List[Dict[str, Any]] = []
        ultimo_ancla = None
        for sec in secciones:
            tipo = (sec.get("tipo") or "parrafo").lower()
            if tipo == "parrafo":
                for parte in self._dividir_parrafo(sec.get("texto", "")):
                    chunks.append({"texto": parte, "metadata": {"tipo": "parrafo", "vinculos": []}})
                    ultimo_ancla = len(chunks)
            elif tipo == "tabla":
                texto_tabla = self._render_tabla(sec)
                chunks.append({"texto": texto_tabla,
                               "metadata": {"tipo": "tabla", "atomica": True,
                                            "titulo": sec.get("titulo", ""), "vinculos": []}})
                ultimo_ancla = len(chunks)
                if sec.get("nota"):
                    chunks.append({"texto": f"[Nota de tabla] {sec['nota']}",
                                   "metadata": {"tipo": "nota", "vinculos": [len(chunks)]}})
            elif tipo == "nota":
                vinc = [ultimo_ancla] if ultimo_ancla else []
                chunks.append({"texto": f"[Nota] {sec.get('texto', '')}",
                               "metadata": {"tipo": "nota", "vinculos": vinc}})
            elif tipo in ("referencia", "figura"):
                texto = sec.get("texto") or sec.get("descripcion") or ""
                if sec.get("referencia"):
                    texto = f"{texto} ({sec['referencia']})" if texto else str(sec["referencia"])
                chunks.append({"texto": f"[{tipo.capitalize()}] {texto}",
                               "metadata": {"tipo": tipo, "atomica": True,
                                            "referencia": sec.get("referencia"), "vinculos": []}})
            else:
                raise KnowledgeModelError(f"Tipo de sección canónica desconocido: {tipo!r}")
        for i, c in enumerate(chunks, start=1):
            c["metadata"]["ordinal_global"] = i
        return chunks

    def _dividir_parrafo(self, texto: str) -> List[str]:
        texto = (texto or "").strip()
        if not texto:
            return []
        if len(texto) <= self.chunk_max_chars:
            return [texto]
        frases = re.split(r"(?<=[.!?])\s+", texto)
        partes, actual = [], ""
        for f in frases:
            if actual and len(actual) + len(f) + 1 > self.chunk_max_chars:
                partes.append(actual.strip())
                actual = f
            else:
                actual = f"{actual} {f}".strip()
        if actual:
            partes.append(actual.strip())
        return partes

    @staticmethod
    def _render_tabla(sec: Dict[str, Any]) -> str:
        """Tabla atómica: nunca se divide; se renderiza preservando filas/cols."""
        titulo = sec.get("titulo", "")
        filas = sec.get("contenido", [])
        lineas = [f"[Tabla] {titulo}".strip()] if titulo else ["[Tabla]"]
        if filas:
            ancho = [max(len(str(fila[c])) if c < len(fila) else 0 for fila in filas)
                     for c in range(max(len(f) for f in filas))]
            for idx, fila in enumerate(filas):
                celdas = [str(fila[c]).ljust(ancho[c]) if c < len(fila) else " " * ancho[c]
                          for c in range(len(ancho))]
                lineas.append("| " + " | ".join(celdas) + " |")
                if idx == 0:
                    lineas.append("|" + "|".join("-" * (w + 2) for w in ancho) + "|")
        return "\n".join(lineas)
