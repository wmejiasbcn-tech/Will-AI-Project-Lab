"""
WAIPL Core — Orquestador de admisión del WILL RAG (RAG de Will App).

CADENA CANÓNICA RECONCILIADA (2026-09-16):

    especialista de dominio / adquisición
        · Kairos  → médico-científico y comunitario
        · DIKE    → jurídico-normativo (Will App y ecosistema WAIPL)
    → Vár (VAC-01): verificación independiente
    → Yata: auditoría de validadores y mecanismos de validación (cuando corresponda)
    → supervisión humana (cuando corresponda; obligatoria para conocimiento canónico)
    → conocimiento canónico
    → WILL RAG

Separación de jurisdicciones (no confundir):
    especialización ≠ verificación ≠ auditoría de validadores ≠ Gate ≠ supervisión humana

DISPOSICIONES EXPRESAS:
    - DIKE NO es Gate del RAG y NO decide por sí mismo qué información se convierte en
      conocimiento canónico. Aporta dictamen de su dominio como especialista; su resultado
      queda sometido a la verificación independiente de Vár.
    - Kairos es especialista de dominio, no un mero extractor/recolector.
    - Vár (VAC-01) es verificación transversal; no es especialista de dominio.
    - Yata audita validadores y mecanismos de validación; NO audita directamente a DIKE/Kairos.
    - El cierre/acreditación operacional corresponde al mecanismo canónico de WAIPL (externo a
      este repositorio). Se integra mediante contrato inyectable; NO se implementa aquí un Gate
      paralelo ni se recrea SENTINEL.

Regla general de especialización (transversal):
    «Los agentes especializados deben poseer competencia sobre el dominio en el que operan;
    la especialización no elimina la necesidad de verificación independiente.»

Registro canónico: waipl/rag/knowledge_register.json (fuente única de verdad del estado).

Solo stdlib. Los agentes/contratos se inyectan (inversión de dependencias).
"""

import json
import logging
import os
import tempfile
import threading
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("WAIPL-WillRAG-Pipeline")

WAIPL_ROOT = Path(__file__).parent.parent
DEFAULT_REGISTER = WAIPL_ROOT / "rag" / "knowledge_register.json"

# Dominios (especialistas con competencia de dominio)
DOMINIO_MEDICO = "MEDICO_CIENTIFICO_COMUNITARIO"
DOMINIO_JURIDICO = "JURIDICO_NORMATIVO"

# Nodos del bus (ids coherentes con Graphify)
BUS_RECIPIENTES = {
    "Soberano": "soberano_william",
    "Carla": "node_carla",
}


class KnowledgeStatus(str, Enum):
    BORRADOR = "Borrador"
    EN_REVISION = "En revisión"
    APROBADO = "Aprobado"
    PENDIENTE_CONFIRMACION = "Pendiente confirmación humana"
    APROBADO_CON_RESTRICCIONES = "Aprobado con restricciones"
    RECHAZADO = "Rechazado"
    BLOQUEADO = "Bloqueado"


class ComplianceGateError(Exception):
    """Violación del ciclo de admisión del WILL RAG."""


class RAGPipeline:
    """
    Orquestador del ciclo de admisión del conocimiento del WILL RAG (Dominio A).

    Especialista de dominio produce → Vár verifica (independiente) → Yata (cuando corresponda)
    → supervisión humana → conocimiento canónico.
    """

    _LOCK = threading.RLock()

    def __init__(
        self,
        archivist: Any,
        dike: Any = None,
        guardian: Any = None,
        bus: Any = None,
        register_path: Optional[str] = None,
        yata: Any = None,
        cierre_operacional: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ):
        """
        Args:
            archivist: Codd (GDO-01) con register_document()/get_document().
            dike: Especialista jurídico-normativo (RGL-01) con generate_compliance_report().
                  NO es gate: aporta dictamen de dominio como entrada.
            guardian: Vár (VAC-01) con evaluate_output() — verificación independiente.
            bus: EventBus opcional para publicar pausas de supervisión.
            register_path: ruta del registro canónico de unidades.
            yata: Contrato externo de Yata (auditoría de validadores); NO implementado aquí.
                  Si es None, Yata no interviene (no instanciado).
            cierre_operacional: Contrato externo del mecanismo canónico de cierre/
                  acreditación operacional de WAIPL. Externo a este repositorio; no se
                  implementa aquí. Si es None, no se invoca (dependencia externa documentada).
        """
        self.archivist = archivist
        self.dike = dike
        self.guardian = guardian
        self.bus = bus
        self.yata = yata
        self.cierre_operacional = cierre_operacional
        self.register_path = Path(register_path) if register_path else DEFAULT_REGISTER
        self.register = self._load_register()

    # ─── Registro canónico ────────────────────────────────────────────────

    def _load_register(self) -> Dict[str, Any]:
        if self.register_path.exists():
            with open(self.register_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"unidades": {}}

    def _save_register(self):
        """Escritura atómica (tempfile + os.replace)."""
        self.register_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=str(self.register_path.parent), suffix=".tmp", prefix="register_"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self.register, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self.register_path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone(timedelta(hours=2))).isoformat()

    # ─── Punto de entrada principal ───────────────────────────────────────

    def submit_knowledge_unit(
        self,
        title: str,
        source_url: str,
        content_text: str,
        category: str = "GENERAL",
        evidence_level: str = "OFICIAL",
        doc_record: Optional[Dict[str, Any]] = None,
        dominio: str = DOMINIO_MEDICO,
    ) -> Dict[str, Any]:
        """
        Somete una unidad al ciclo reconciliado:
        Codd → especialista de dominio (dictamen) → Vár (verificación independiente)
        → Yata (si procede) → supervisión humana (pendiente).

        El resultado NUNCA es «Aprobado» automático: requiere ACCEPT humano
        (resolver_supervision_humana / confirm_restricted).
        """
        if not content_text or not content_text.strip():
            raise ValueError("content_text vacío: no se someten unidades sin contenido.")

        with RAGPipeline._LOCK:
            return self._submit_locked(
                title, source_url, content_text, category, evidence_level, doc_record, dominio,
            )

    def _submit_locked(
        self, title, source_url, content_text, category, evidence_level, doc_record, dominio,
    ) -> Dict[str, Any]:

        # 1. Codd: registro oficial (UUID + SHA-256) si no existe.
        if doc_record is None:
            if not self.archivist:
                raise ComplianceGateError("Sin archivista (Codd): no se puede archivar la unidad.")
            doc_record = self.archivist.register_document(
                filename=f"rag_unit_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt",
                content=content_text.encode("utf-8"),
                area="RAG_DOMINIO_A",
                author_node="RAG-Pipeline",
                metadata={
                    "title": title,
                    "source_url": source_url,
                    "category": category,
                    "evidence_level": evidence_level,
                },
            )
        doc_uuid = doc_record["uuid"]

        # 2. Estado inicial: En revisión (nunca RAG_READY sin verificación ni supervisión).
        record = {
            "doc_uuid": doc_uuid,
            "title": title,
            "source_url": source_url,
            "category": category,
            "evidence_level": evidence_level,
            "dominio": dominio,
            "especialista_adquisicion": (
                "DIKE" if dominio == DOMINIO_JURIDICO else "Kairos"
            ),
            "version": 1,
            "sha256": doc_record.get("sha256", ""),
            "stored_path": doc_record.get("stored_path", ""),
            "registered_at": doc_record.get("timestamp", self._now()),
            "estado_anterior": KnowledgeStatus.BORRADOR.value,
            "estado": KnowledgeStatus.EN_REVISION.value,
            "historial": [
                {
                    "timestamp": self._now(),
                    "de": KnowledgeStatus.BORRADOR.value,
                    "a": KnowledgeStatus.EN_REVISION.value,
                    "actor": "RAG-Pipeline",
                    "motivo": "Unidad sometida al ciclo de admisión del WILL RAG",
                }
            ],
            "dictamen_especialista": None,
            "dictamen_id": None,
            "dictamen_timestamp": None,
            "veredicto_final": None,
            "confianza_global": None,
            "pausas_simbioticas": [],
            "vac_validacion": None,
            "auditoria_validadores_yata": None,
            "supervision_humana": None,
            "cierre_operacional": None,
            "fecha_publicacion": None,
            "actualizado_at": self._now(),
        }
        self.register["unidades"][doc_uuid] = record
        self._save_register()
        logger.info(f"[Will RAG] {title} -> En revisión (doc {doc_uuid[:8]}...)")

        # 3. Especialista de dominio: dictamen (entrada, NO decisión de admisión).
        #    DIKE aporta el dictamen de cumplimiento jurídico-normativo (su competencia);
        #    NO decide la admisión. Kairos es el especialista del dominio médico-científico.
        if self.dike is not None:
            dictamen = self.dike.generate_compliance_report(
                doc_id=doc_uuid,
                content=content_text,
                title=title,
                source_url=source_url,
                metadata={
                    "category": category,
                    "evidence_level": evidence_level,
                    "sha256": record["sha256"],
                },
            )
            record["dictamen_especialista"] = {
                "dictamen_id": dictamen.get("dictamen_id"),
                "veredicto_final": dictamen.get("veredicto_final"),
                "confianza_global": dictamen.get("confianza_global"),
                "estado_recomendado": dictamen.get("estado_destino"),
                "timestamp": dictamen.get("timestamp"),
                "jurisdiccion": "especialista de dominio (NO gate)",
            }
            record["dictamen_id"] = dictamen.get("dictamen_id")
            record["dictamen_timestamp"] = dictamen.get("timestamp")
            record["veredicto_final"] = dictamen.get("veredicto_final")
            record["confianza_global"] = dictamen.get("confianza_global")
            record["pausas_simbioticas"] = dictamen.get("pausas_simbioticas_activadas", [])
            for pausa in record["pausas_simbioticas"]:
                self._publish_pausa(record, pausa)

        # 4. Vár (VAC-01): verificación independiente del resultado del especialista.
        #    Si Vár falla, la admisión se aborta (fallo seguro): la unidad queda En revisión.
        bloqueado = False
        if self.guardian is not None:
            vac = self.guardian.evaluate_output(
                prompt=f"Verificación independiente de unidad de dominio {dominio}",
                ai_output=content_text,
                context=title,
            )
            if vac:
                record["vac_validacion"] = {
                    "validador": "Vár (VAC-01)",
                    "score": vac.get("score"),
                    "status": vac.get("status"),
                    "rol": "verificación independiente (no decide canónico)",
                }
                bloqueado = vac.get("status") == "BLOQUEADO"

        if bloqueado:
            self._transition(record, KnowledgeStatus.BLOQUEADO, actor="Vár (VAC-01)",
                             motivo="Vár bloqueó la unidad en verificación independiente")
            return record

        # 5. Yata (cuando corresponda): auditoría de validadores. Externo; solo si inyectado.
        if self.yata is not None:
            try:
                record["auditoria_validadores_yata"] = self.yata(
                    {"validador": "Vár (VAC-01)", "mecanismo": "verificacion_independiente",
                     "doc_uuid": doc_uuid}
                )
            except Exception as e:  # nunca corrompe el ciclo
                logger.warning(f"[Will RAG] Yata no pudo auditar: {e}")

        # 6. Supervisión humana: obligatoria para conocimiento canónico. Pendiente hasta ACCEPT.
        self._transition(record, KnowledgeStatus.PENDIENTE_CONFIRMACION, actor="Vár (VAC-01)",
                         motivo="Verificada; pendiente de supervisión humana (ACCEPT)")
        self._publish_supervision(record)
        return record

    # ─── Re-auditoría ─────────────────────────────

    def audit_registered_document(self, doc_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Re-audita un documento ya registrado: re-ejecuta la verificación independiente de Vár
        y deja la unidad de nuevo en supervisión humana. NO decide la admisión
        (la decisión de conocimiento canónico corresponde a la supervisión humana).
        """
        with RAGPipeline._LOCK:
            record = self.register["unidades"].get(doc_uuid)
            if not record:
                logger.warning(f"[Will RAG] Unidad no encontrada en registro: {doc_uuid}")
                return None
            bloqueado = False
            if self.guardian is not None:
                try:
                    contenido = record.get("title", "")
                    stored = Path(record.get("stored_path", ""))
                    if record.get("stored_path") and stored.exists():
                        contenido = stored.read_text(encoding="utf-8")
                    vac = self.guardian.evaluate_output(
                        prompt=f"Re-verificación independiente de {doc_uuid}",
                        ai_output=contenido,
                        context=record.get("title", ""),
                    )
                    record["vac_validacion"] = {
                        "validador": "Vár (VAC-01)",
                        "score": vac.get("score"),
                        "status": vac.get("status"),
                        "rol": "verificación independiente (no decide canónico)",
                    }
                    bloqueado = vac.get("status") == "BLOQUEADO"
                except Exception as e:  # la verificación nunca corrompe el ciclo
                    logger.warning(f"[Will RAG] Vár no pudo re-verificar: {e}")
            if bloqueado:
                self._transition(record, KnowledgeStatus.BLOQUEADO, actor="Vár (VAC-01)",
                                 motivo="Vár bloqueó la unidad en re-verificación")
                return record
            self._transition(record, KnowledgeStatus.PENDIENTE_CONFIRMACION, actor="Vár (VAC-01)",
                             motivo="Re-verificada; pendiente de supervisión humana (ACCEPT)")
            self._publish_supervision(record)
            return record

    # ─── Supervisión humana ───────────────────────────────────────────────

    def resolver_supervision_humana(
        self,
        doc_uuid: str,
        decision: str,
        reviewer: str,
        motivo: str = "",
    ) -> Dict[str, Any]:
        """
        Resuelve la supervisión humana de una unidad pendiente.
        decision ∈ {"ACCEPT", "ACCEPT_RESTRICTED", "REJECT"}.
        Solo autoridad humana autorizada (Carla / Soberano) decide la incorporación
        al conocimiento canónico.
        """
        with RAGPipeline._LOCK:
            record = self.register["unidades"].get(doc_uuid)
            if not record:
                raise ComplianceGateError(f"Unidad no encontrada: {doc_uuid}")
            if record["estado"] != KnowledgeStatus.PENDIENTE_CONFIRMACION.value:
                raise ComplianceGateError(
                    f"La unidad {doc_uuid[:8]} no está Pendiente confirmación humana "
                    f"(estado actual: {record['estado']})"
                )
            decision = decision.upper()
            if decision == "ACCEPT":
                nuevo = KnowledgeStatus.APROBADO
            elif decision == "ACCEPT_RESTRICTED":
                nuevo = KnowledgeStatus.APROBADO_CON_RESTRICCIONES
            elif decision == "REJECT":
                nuevo = KnowledgeStatus.RECHAZADO
            else:
                raise ValueError("decision debe ser ACCEPT, ACCEPT_RESTRICTED o REJECT")

            record["supervision_humana"] = {
                "human_reviewer_id": reviewer,
                "human_decision": decision,
                "decision_timestamp": self._now(),
                "decision_reason": motivo,
            }
            self._transition(record, nuevo, actor=reviewer,
                             motivo=motivo or f"Supervisión humana: {decision}")
            logger.info(f"[Will RAG] {record['title']} -> {record['estado']} (por {reviewer})")
            return record

    def confirm_restricted(
        self,
        doc_uuid: str,
        approved: bool,
        reviewer: str = "Carla",
        note: str = "",
    ) -> Dict[str, Any]:
        """Compatibilidad: resuelve la supervisión humana de una unidad pendiente."""
        return self.resolver_supervision_humana(
            doc_uuid,
            decision="ACCEPT_RESTRICTED" if approved else "REJECT",
            reviewer=reviewer,
            motivo=note,
        )

    # ─── Transiciones ─────────────────────────────────────────────────────

    def _transition(self, record: Dict[str, Any], nuevo: KnowledgeStatus, actor: str, motivo: str):
        with RAGPipeline._LOCK:
            record["historial"].append(
                {
                    "timestamp": self._now(),
                    "de": record["estado"],
                    "a": nuevo.value,
                    "actor": actor,
                    "motivo": motivo,
                }
            )
            record["estado_anterior"] = record["estado"]
            record["estado"] = nuevo.value
            if nuevo.value in (
                KnowledgeStatus.APROBADO.value,
                KnowledgeStatus.APROBADO_CON_RESTRICCIONES.value,
            ) and not record.get("fecha_publicacion"):
                record["fecha_publicacion"] = self._now()
            record["actualizado_at"] = self._now()
            # Contrato externo de cierre/acreditación operacional (mecanismo canónico WAIPL).
            if nuevo.value in (
                KnowledgeStatus.APROBADO.value,
                KnowledgeStatus.APROBADO_CON_RESTRICCIONES.value,
            ) and self.cierre_operacional is not None:
                try:
                    record["cierre_operacional"] = self.cierre_operacional(dict(record))
                except Exception as e:  # dependencia externa; nunca corrompe el ciclo
                    logger.warning(f"[Will RAG] Cierre operacional externo no disponible: {e}")
            self._save_register()

    # ─── Bus ──────────────────────────────────────────────────────────────

    def _publish_pausa(self, record: Dict[str, Any], pausa: Dict[str, Any]):
        """Publica una pausa simbiotica del especialista de dominio (escalado)."""
        if not self.bus:
            return
        try:
            from waipl.core.bus import Layer, Message, MessagePriority

            destinataria = pausa.get("destinataria", "Carla")
            recipient = BUS_RECIPIENTES.get(destinataria, "node_carla")
            self.bus.publish(
                Message(
                    sender_id="WillRAG-Pipeline",
                    sender_layer=Layer.SERVICES,
                    recipient_id=recipient,
                    content={
                        "tipo": "pausa_simbiotica",
                        "punto": pausa.get("punto"),
                        "motivo": pausa.get("motivo"),
                        "unidad": {
                            "doc_uuid": record["doc_uuid"],
                            "title": record["title"],
                            "estado": record["estado"],
                        },
                    },
                    priority=MessagePriority.HIGH,
                    metadata={"etapa": "dictamen_especialista"},
                )
            )
        except Exception as e:  # el bus nunca bloquea la admisión
            logger.warning(f"[Will RAG] No se pudo publicar pausa del especialista: {e}")

    def _publish_supervision(self, record: Dict[str, Any]):
        if not self.bus:
            return
        try:
            from waipl.core.bus import Layer, Message, MessagePriority

            self.bus.publish(
                Message(
                    sender_id="WillRAG-Pipeline",
                    sender_layer=Layer.SERVICES,
                    recipient_id=BUS_RECIPIENTES["Carla"],
                    content={
                        "tipo": "supervision_humana",
                        "unidad": {
                            "doc_uuid": record["doc_uuid"],
                            "title": record["title"],
                            "estado": record["estado"],
                            "especialista": record.get("especialista_adquisicion", ""),
                        },
                    },
                    priority=MessagePriority.HIGH,
                    metadata={"etapa": "verificacion_independiente → supervision_humana"},
                )
            )
        except Exception as e:  # el bus nunca bloquea la admisión
            logger.warning(f"[Will RAG] No se pudo publicar pausa de supervisión: {e}")

    # ─── Consultas ────────────────────────────────────────────────────────

    def get_unit(self, doc_uuid: str) -> Optional[Dict[str, Any]]:
        return self.register["unidades"].get(doc_uuid)

    def get_register(self) -> Dict[str, Any]:
        return self.register

    def units_by_status(self) -> Dict[str, int]:
        conteo: Dict[str, int] = {}
        for u in self.register["unidades"].values():
            conteo[u["estado"]] = conteo.get(u["estado"], 0) + 1
        return conteo

    def approved_units(self) -> List[Dict[str, Any]]:
        """Unidades de conocimiento canónico que pueden entrar en el WILL RAG."""
        return [
            u
            for u in self.register["unidades"].values()
            if u["estado"]
            in (KnowledgeStatus.APROBADO.value, KnowledgeStatus.APROBADO_CON_RESTRICCIONES.value)
        ]

    def stats(self) -> Dict[str, Any]:
        return {
            "total_unidades": len(self.register["unidades"]),
            "por_estado": self.units_by_status(),
            "en_will_rag": len(self.approved_units()),
            "register_path": str(self.register_path),
        }
