"""
WAIPL Agente DIKE — RGL-01 "Guardiana de Cumplimiento Normativo"
Auditora AESIA/RGPD del ecosistema WAIPL.

Verifica que toda evidencia científica y textual que entra en la base de
conocimiento (RAG) cumple con:
  - AESIA (Agencia Española de Supervisión de la Inteligencia Artificial)
  - RGPD (Reglamento General de Protección de Datos)

Sin la validación de DIKE, ninguna unidad de conocimiento puede pasar
de "En revisión" a "Aprobado" en el RAG del Dominio A.

Skills específicos:
  - audit_aesia_compliance(doc_id)
  - audit_rgpd_compliance(doc_id)
  - check_data_category(content)
  - generate_compliance_report(doc_id)

Dependencias:
  - Codd (GDO-01): registro y recuperación de documentos
  - VAC-01 Guardiana: validación de coherencia factual del dictamen
"""

import hashlib
import json
import logging
import os
import re
import uuid as uuidlib
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("DIKE-RGL-01")

# ============================================
# ENUMS Y CONSTANTES
# ============================================

class ComplianceVerdict(Enum):
    CONFORME = "Conforme"
    NO_CONFORME = "No conforme"
    CONFORME_CON_RESTRICCIONES = "Conforme con restricciones"


class DataCategory(Enum):
    """Categorías de datos personales según RGPD Art. 9."""
    SALUD = "datos_salud"                    # Art. 9.1.a —Datos relativos a la salud
    BIOMETRICOS = "datos_biometricos"        # Art. 9.1.b
    GENETICOS = "datos_geneticos"            # Art. 9.1.c
    SEXuales = "datos_sexo_vida_sexual"      # Art. 9.1.d
    ORIENTACION = "datos_orientacion_sexual" # Art. 9.1.d (subconjunto)
    ETNICOS = "datos_origen_etnico"          # Art. 9.1.e
    SIN_DATOS_PERSONALES = "sin_datos_personales"
    OTROS = "otros_datos_personales"


# Patrones de detección de datos personales sensibles (Art. 9 RGPD)
PATRONES_DATOS_SENSIBLES = {
    DataCategory.SALUD: [
        r'\b(diagn[oó]stic[oa])\b', r'\b(enfermedad)\b', r'\b(tratamiento m[eé]dico)\b',
        r'\b(VIH|ITS|ETS)\b', r'\b(hepatitis)\b', r'\b(sobredosis)\b',
        r'\b(prescripci[oó]n m[eé]dica)\b', r'\b(dosis)\b', r'\b(receta m[eé]dica)\b',
    ],
    DataCategory.BIOMETRICOS: [
        r'\b(huella dactilar)\b', r'\b(reconocimiento facial)\b',
        r'\b(iris)\b', r'\b(voz biom[eé]trica)\b',
    ],
    DataCategory.GENETICOS: [
        r'\b(ADN|DNA)\b', r'\b(genoma)\b', r'\b(prueba gen[eé]tica)\b',
        r'\b(marcador gen[eé]tico)\b',
    ],
    DataCategory.SEXuales: [
        r'\b(orientaci[oó]n sexual)\b', r'\b(vida sexual)\b',
        r'\b(pr[aá]cticas sexuales)\b', r'\b(chemsex)\b', r'\b(slam)\b',
    ],
    DataCategory.ETNICOS: [
        r'\b(origen [eé]tnico)\b', r'\b(raza)\b', r'\b(etnia)\b',
    ],
}

# Palabras clave para principios AESIA
AESIA_PRINCIPIOS = {
    "transparencia": [
        r'\b(transparencia)\b', r'\b(explicable)\b', r'\b(trazable)\b',
        r'\b(auditable)\b', r'\b(identificaci[oó]n del sistema)\b',
    ],
    "no_discriminacion": [
        r'\b(no discriminaci[oó]n)\b', r'\b(sesgo)\b', r'\b(equidad)\b',
        r'\b(inclusi[oó]n)\b', r'\b(diversidad)\b',
    ],
    "responsabilidad_humana": [
        r'\b(supervisi[oó]n humana)\b', r'\b(intervenci[oó]n humana)\b',
        r'\b(human-in-the-loop)\b', r'\b(soberan[íi]a humana)\b',
        r'\b(control humano)\b',
    ],
}

# ============================================
# CLASE PRINCIPAL: DIKE AUDITORA
# ============================================

class DikeAuditora:
    """
    Guardiana de Cumplimiento Normativo del ecosistema WAIPL.
    Audita documentos contra AESIA y RGPD antes de su aprobación en el RAG.
    """

    def __init__(
        self,
        vault_path: str,
        archivist: Any = None,
        guardian: Any = None,
    ):
        """
        Args:
            vault_path: Ruta al Vault v3.0 de DIKE
            archivist: Instancia de Codd (GDO-01) para recuperación de documentos
            guardian: Instancia de VAC-01 Guardiana para validación del dictamen
        """
        self.vault_path = vault_path
        self.archivist = archivist
        self.guardian = guardian
        self.corpus_dir = os.path.join(vault_path, "04-PROFESIONAL")
        self.templates_dir = os.path.join(vault_path, "07-TEMPLATES")
        self.audit_log_dir = os.path.join(vault_path, "08-AUDITORIA")
        self.total_auditorias = 0
        self.dictamenes_emitidos: List[Dict[str, Any]] = []
        self._load_corpus_index()

        logger.info("[DIKE] Guardiana de Cumplimiento Normativo inicializada")

    # ============================================
    # GESTIÓN DEL CORPUS NORMATIVO
    # ============================================

    def _load_corpus_index(self):
        """Carga el índice del corpus normativo disponible."""
        index_path = os.path.join(self.corpus_dir, "corpus_index.json")
        if os.path.isfile(index_path):
            try:
                with open(index_path, "r", encoding="utf-8") as f:
                    self.corpus_index = json.load(f)
            except Exception as e:
                logger.warning(f"[DIKE] Error cargando índice de corpus: {e}")
                self.corpus_index = {"documentos": []}
        else:
            self.corpus_index = {"documentos": []}

    def ingest_corpus_document(
        self,
        title: str,
        source_url: str,
        content_text: str,
        normative_type: str = "AESIA",
    ) -> Dict[str, Any]:
        """
        Ingesta un documento normativo en el corpus de DIKE.

        Args:
            title: Título del documento normativo
            source_url: URL de origen oficial
            content_text: Texto completo del documento
            normative_type: "AESIA" o "RGPD"
        """
        doc_uuid = str(uuidlib.uuid4())
        doc_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()
        timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat()

        # Almacenar documento
        corpus_file = os.path.join(self.corpus_dir, f"{normative_type.lower()}_{doc_uuid}.txt")
        os.makedirs(self.corpus_dir, exist_ok=True)
        with open(corpus_file, "w", encoding="utf-8") as f:
            f.write(content_text)

        # Registrar en índice
        entry = {
            "uuid": doc_uuid,
            "title": title,
            "source_url": source_url,
            "normative_type": normative_type,
            "sha256": doc_hash,
            "stored_path": corpus_file,
            "timestamp": timestamp,
            "size_bytes": len(content_text.encode("utf-8")),
        }
        self.corpus_index["documentos"].append(entry)

        # Guardar índice actualizado
        index_path = os.path.join(self.corpus_dir, "corpus_index.json")
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(self.corpus_index, f, indent=2, ensure_ascii=False)

        logger.info(f"[DIKE] Corpus ingestado: {title} ({normative_type}) | Hash: {doc_hash[:8]}...")
        return entry

    # ============================================
    # SKILL: check_data_category(content)
    # ============================================

    def check_data_category(self, content: str) -> Dict[str, Any]:
        """
        Clasifica los datos personales presentes en el contenido
        según las categorías del Art. 9 RGPD.

        Returns:
            Dict con categorías detectadas, nivel de sensibilidad y coincidencias.
        """
        content_lower = content.lower()
        categorias_detectadas: Dict[str, List[str]] = {}
        nivel_sensibilidad = "bajo"

        for categoria, patrones in PATRONES_DATOS_SENSIBLES.items():
            coincidencias = []
            for patron in patrones:
                matches = re.findall(patron, content_lower, re.IGNORECASE)
                if matches:
                    coincidencias.extend(matches)
            if coincidencias:
                categorias_detectadas[categoria.value] = coincidencias

        # Determinar nivel de sensibilidad
        if any(cat in categorias_detectadas for cat in [
            DataCategory.SALUD.value, DataCategory.GENETICOS.value,
            DataCategory.BIOMETRICOS.value, DataCategory.SEXuales.value,
        ]):
            nivel_sensibilidad = "alto"
        elif categorias_detectadas:
            nivel_sensibilidad = "medio"

        if not categorias_detectadas:
            categorias_detectadas[DataCategory.SIN_DATOS_PERSONALES.value] = []

        resultado = {
            "categorias": list(categorias_detectadas.keys()),
            "coincidencias": categorias_detectadas,
            "nivel_sensibilidad": nivel_sensibilidad,
            "total_patrones_detectados": sum(len(v) for v in categorias_detectadas.values()),
        }

        logger.info(f"[DIKE] Categorización de datos: {resultado['categorias']} | Sensibilidad: {nivel_sensibilidad}")
        return resultado

    # ============================================
    # SKILL: audit_aesia_compliance(doc_id)
    # ============================================

    def audit_aesia_compliance(self, content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Verifica el cumplimiento de los principios AESIA:
        - Transparencia
        - No discriminación
        - Responsabilidad humana

        Returns:
            Dict con veredicto por dimensión, nivel de confianza y observaciones.
        """
        content_lower = content.lower()
        dimensiones: Dict[str, Dict[str, Any]] = {}
        total_conforme = 0

        for principio, patrones in AESIA_PRINCIPIOS.items():
            coincidencias = []
            for patron in patrones:
                matches = re.findall(patron, content_lower, re.IGNORECASE)
                if matches:
                    coincidencias.extend(matches)

            if coincidencias:
                veredicto = "conforme"
                confianza = min(0.95, 0.70 + 0.10 * len(coincidencias))
                total_conforme += 1
            else:
                # Si no hay mención explícita pero el contenido no parece violar el principio
                veredicto = "indeterminado"
                confianza = 0.60

            dimensiones[principio] = {
                "veredicto": veredicto,
                "confianza": round(confianza, 2),
                "coincidencias": coincidencias,
                "observacion": (
                    f"Principio mencionado con {len(coincidencias)} referencias."
                    if coincidencias
                    else "Sin referencia explícita detectada. Revisión manual recomendada."
                ),
            }

        # Veredicto global AESIA
        if total_conforme == len(AESIA_PRINCIPIOS):
            veredicto_global = ComplianceVerdict.CONFORME.value
        elif total_conforme > 0:
            veredicto_global = ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value
        else:
            veredicto_global = ComplianceVerdict.NO_CONFORME.value

        resultado = {
            "normativa": "AESIA",
            "dimensiones": dimensiones,
            "veredicto_global": veredicto_global,
            "principios_conformes": total_conforme,
            "principios_totales": len(AESIA_PRINCIPIOS),
            "confianza_global": round(
                sum(d["confianza"] for d in dimensiones.values()) / len(dimensiones), 2
            ),
        }

        logger.info(f"[DIKE] Audit AESIA: {veredicto_global} | Confianza: {resultado['confianza_global']}")
        return resultado

    # ============================================
    # SKILL: audit_rgpd_compliance(doc_id)
    # ============================================

    def audit_rgpd_compliance(
        self,
        content: str,
        metadata: Optional[Dict] = None,
        data_category_result: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Verifica el cumplimiento del RGPD:
        - Base jurídica (Art. 6)
        - Datos sensibles (Art. 9)
        - Minimización de datos (Art. 5.1.c)
        - Derechos de las interesadas (Arts. 12-22)

        Returns:
            Dict con veredicto por dimensión, nivel de confianza y observaciones.
        """
        content_lower = content.lower()

        # Usar categorización de datos si se proporciona, si no, calcularla
        if data_category_result is None:
            data_category_result = self.check_data_category(content)

        dimensiones: Dict[str, Dict[str, Any]] = {}

        # 1. Base jurídica (Art. 6)
        base_juridica_patrones = [
            r'\b(consentimiento)\b', r'\b(inter[eé]s leg[ií]timo)\b',
            r'\b(cumplimiento de obligaci[oó]n legal)\b',
            r'\b(misi[oó]n de inter[eé]s p[uú]blico)\b',
            r'\b(base jur[ií]dica)\b',
        ]
        base_juridica_matches = []
        for p in base_juridica_patrones:
            base_juridica_matches.extend(re.findall(p, content_lower, re.IGNORECASE))

        if base_juridica_matches:
            veredicto_bj = "conforme"
            confianza_bj = 0.90
            obs_bj = f"Base jurídica mencionada: {base_juridica_matches[:3]}"
        elif data_category_result["nivel_sensibilidad"] == "alto":
            veredicto_bj = "no_conforme"
            confianza_bj = 0.85
            obs_bj = "Datos sensibles detectados sin base jurídica explícita. Consentimiento explícito requerido (Art. 9.2.a)."
        else:
            veredicto_bj = "indeterminado"
            confianza_bj = 0.60
            obs_bj = "Sin base jurídica explícita. Revisión manual recomendada."

        dimensiones["base_juridica"] = {
            "veredicto": veredicto_bj,
            "confianza": confianza_bj,
            "articulo": "Art. 6 RGPD",
            "coincidencias": base_juridica_matches,
            "observacion": obs_bj,
        }

        # 2. Datos sensibles (Art. 9)
        if data_category_result["nivel_sensibilidad"] == "alto":
            veredicto_ds = "conforme_con_restricciones"
            confianza_ds = 0.85
            obs_ds = (
                f"Datos sensibles detectados: {data_category_result['categorias']}. "
                "Requiere garantías específicas y consentimiento explícito (Art. 9.2)."
            )
        elif data_category_result["nivel_sensibilidad"] == "medio":
            veredicto_ds = "indeterminado"
            confianza_ds = 0.70
            obs_ds = "Posibles datos personales sin categoría especial. Revisión manual."
        else:
            veredicto_ds = "conforme"
            confianza_ds = 0.95
            obs_ds = "No se detectan datos personales sensibles."

        dimensiones["datos_sensibles"] = {
            "veredicto": veredicto_ds,
            "confianza": confianza_ds,
            "articulo": "Art. 9 RGPD",
            "categorias_detectadas": data_category_result["categorias"],
            "observacion": obs_ds,
        }

        # 3. Minimización (Art. 5.1.c)
        minimizacion_patrones = [
            r'\b(minimizaci[oó]n)\b', r'\b(datos necesarios)\b',
            r'\b(limitado a lo necesario)\b', r'\b(no excesivo)\b',
        ]
        min_matches = []
        for p in minimizacion_patrones:
            min_matches.extend(re.findall(p, content_lower, re.IGNORECASE))

        veredicto_min = "conforme" if min_matches else "indeterminado"
        dimensiones["minimizacion"] = {
            "veredicto": veredicto_min,
            "confianza": 0.85 if min_matches else 0.60,
            "articulo": "Art. 5.1.c RGPD",
            "coincidencias": min_matches,
            "observacion": (
                "Principio de minimización referenciado."
                if min_matches
                else "Sin mención explícita. Verificar que solo se procesan datos necesarios."
            ),
        }

        # 4. Derechos de las interesadas (Arts. 12-22)
        derechos_patrones = [
            r'\b(derecho de acceso)\b', r'\b(derecho de rectificaci[oó]n)\b',
            r'\b(derecho de supresi[oó]n)\b', r'\b(derecho al olvido)\b',
            r'\b(derecho de oposici[oó]n)\b', r'\b(derecho de portabilidad)\b',
            r'\b(derechos de las personas interesadas)\b', r'\b(ARCO)\b',
        ]
        derechos_matches = []
        for p in derechos_patrones:
            derechos_matches.extend(re.findall(p, content_lower, re.IGNORECASE))

        veredicto_dr = "conforme" if derechos_matches else "indeterminado"
        dimensiones["derechos_interesadas"] = {
            "veredicto": veredicto_dr,
            "confianza": 0.85 if derechos_matches else 0.55,
            "articulo": "Arts. 12-22 RGPD",
            "coincidencias": derechos_matches,
            "observacion": (
                f"Derechos mencionados: {len(derechos_matches)} referencias."
                if derechos_matches
                else "Sin mención de derechos de interesadas. Revisión manual recomendada."
            ),
        }

        # Veredicto global RGPD
        conformes = sum(1 for d in dimensiones.values() if d["veredicto"] == "conforme")
        no_conformes = sum(1 for d in dimensiones.values() if d["veredicto"] == "no_conforme")
        restringidas = sum(1 for d in dimensiones.values() if d["veredicto"] == "conforme_con_restricciones")

        if no_conformes > 0:
            veredicto_global = ComplianceVerdict.NO_CONFORME.value
        elif restringidas > 0:
            veredicto_global = ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value
        elif conformes == len(dimensiones):
            veredicto_global = ComplianceVerdict.CONFORME.value
        else:
            veredicto_global = ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value

        resultado = {
            "normativa": "RGPD",
            "dimensiones": dimensiones,
            "veredicto_global": veredicto_global,
            "dimensiones_conformes": conformes,
            "dimensiones_no_conformes": no_conformes,
            "dimensiones_restringidas": restringidas,
            "dimensiones_totales": len(dimensiones),
            "confianza_global": round(
                sum(d["confianza"] for d in dimensiones.values()) / len(dimensiones), 2
            ),
            "data_category": data_category_result,
        }

        logger.info(f"[DIKE] Audit RGPD: {veredicto_global} | Confianza: {resultado['confianza_global']}")
        return resultado

    # ============================================
    # SKILL: generate_compliance_report(doc_id)
    # ============================================

    def generate_compliance_report(
        self,
        doc_id: str,
        content: str,
        title: str = "",
        source_url: str = "",
        metadata: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Genera un dictamen estructurado de cumplimiento normativo completo.

        Combina audit_aesia_compliance + audit_rgpd_compliance + check_data_category
        en un único dictamen canónico.

        Returns:
            Dict con el dictamen completo listo para almacenar.
        """
        self.total_auditorias += 1
        timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat()
        dictamen_uuid = str(uuidlib.uuid4())

        # 1. Categorización de datos
        data_cat = self.check_data_category(content)

        # 2. Audit AESIA
        aesia_result = self.audit_aesia_compliance(content, metadata)

        # 3. Audit RGPD
        rgpd_result = self.audit_rgpd_compliance(content, metadata, data_cat)

        # 4. Veredicto combinado
        if aesia_result["veredicto_global"] == ComplianceVerdict.NO_CONFORME.value or \
           rgpd_result["veredicto_global"] == ComplianceVerdict.NO_CONFORME.value:
            veredicto_final = ComplianceVerdict.NO_CONFORME.value
            estado_destino = "Rechazado"
        elif aesia_result["veredicto_global"] == ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value or \
             rgpd_result["veredicto_global"] == ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value:
            veredicto_final = ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value
            estado_destino = "Aprobado con restricciones"
        else:
            veredicto_final = ComplianceVerdict.CONFORME.value
            estado_destino = "Aprobado"

        # 5. Construcción del dictamen
        dictamen = {
            "dictamen_id": dictamen_uuid,
            "doc_id": doc_id,
            "timestamp": timestamp,
            "auditora": "DIKE (RGL-01)",
            "titulo_documento": title,
            "url_origen": source_url,
            "hash_contenido": hashlib.sha256(content.encode("utf-8")).hexdigest(),

            "veredicto_final": veredicto_final,
            "estado_destino": estado_destino,
            "confianza_global": round(
                (aesia_result["confianza_global"] + rgpd_result["confianza_global"]) / 2, 2
            ),

            "audit_aesia": aesia_result,
            "audit_rgpd": rgpd_result,
            "data_category": data_cat,

            "pausas_simbioticas_activadas": [],
            "observaciones_generales": "",
        }

        # 6. Detectar si se necesitan pausas simbióticas
        if aesia_result["confianza_global"] < 0.70:
            dictamen["pausas_simbioticas_activadas"].append({
                "punto": 1,
                "motivo": "Confianza AESIA < 70% — ambigüedad normativa no resuelta",
                "destinataria": "Soberano",
            })
        if rgpd_result["dimensiones"].get("base_juridica", {}).get("veredicto") == "no_conforme":
            dictamen["pausas_simbioticas_activadas"].append({
                "punto": 3,
                "motivo": "Base jurídica faltante para datos sensibles",
                "destinataria": "Soberano",
            })
        if veredicto_final == ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value:
            dictamen["pausas_simbioticas_activadas"].append({
                "punto": 4,
                "motivo": "Aprobado con restricciones requiere confirmación",
                "destinataria": "Carla",
            })

        # 7. Observaciones generales
        observaciones = []
        if data_cat["nivel_sensibilidad"] == "alto":
            observaciones.append(
                "Documento contiene datos sensibles (Art. 9 RGPD). "
                "Requiere garantías específicas y posible anonimización."
            )
        if aesia_result["principios_conformes"] < aesia_result["principios_totales"]:
            observaciones.append(
                f"Solo {aesia_result['principios_conformes']}/{aesia_result['principios_totales']} "
                "principios AESIA confirmados explícitamente."
            )
        if rgpd_result["dimensiones_no_conformes"] > 0:
            observaciones.append(
                f"{rgpd_result['dimensiones_no_conformes']} dimensión(es) RGPD no conforme(s). "
                "Revisión manual obligatoria."
            )
        dictamen["observaciones_generales"] = " | ".join(observaciones) if observaciones else "Sin observaciones adicionales."

        # 8. Validación con VAC-01 Guardiana (si está disponible)
        if self.guardian:
            vac_result = self.guardian.evaluate_output(
                prompt=f"Auditoría normativa de: {title}",
                ai_output=json.dumps(dictamen, ensure_ascii=False),
                context=content[:500],
            )
            dictamen["vac_validacion"] = {
                "score": vac_result.get("score", 0),
                "status": vac_result.get("status", ""),
            }
            if vac_result.get("status") == "BLOQUEADO":
                dictamen["veredicto_final"] = ComplianceVerdict.NO_CONFORME.value
                dictamen["estado_destino"] = "Bloqueado"
                dictamen["observaciones_generales"] += " | VAC-01 bloqueó el dictamen por posible alucinación."

        # 9. Almacenar dictamen
        dictamen_file = os.path.join(
            self.audit_log_dir,
            f"dictamen_{dictamen_uuid[:8]}.json"
        )
        with open(dictamen_file, "w", encoding="utf-8") as f:
            json.dump(dictamen, f, indent=2, ensure_ascii=False)

        self.dictamenes_emitidos.append(dictamen)
        logger.info(
            f"[DIKE] Dictamen emitido: {veredicto_final} | "
            f"Estado destino: {estado_destino} | "
            f"Confianza: {dictamen['confianza_global']}"
        )
        return dictamen

    # ============================================
    # MÉTODO AUXILIAR: audit_document(doc_id)
    # ============================================

    def audit_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Recupera un documento del archivista Codd y ejecuta la auditoría completa.

        Args:
            doc_id: UUID del documento registrado por Codd (GDO-01)

        Returns:
            Dictamen completo o None si el documento no se encuentra.
        """
        if not self.archivist:
            logger.error("[DIKE] No hay archivista (Codd) conectado.")
            return None

        doc_record = self.archivist.get_document(doc_id)
        if not doc_record:
            logger.warning(f"[DIKE] Documento no encontrado: {doc_id}")
            return None

        # Leer contenido del archivo
        stored_path = doc_record.get("stored_path", "")
        if not os.path.isfile(stored_path):
            logger.error(f"[DIKE] Archivo no accesible: {stored_path}")
            return None

        with open(stored_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Ejecutar auditoría completa
        return self.generate_compliance_report(
            doc_id=doc_id,
            content=content,
            title=doc_record.get("metadata", {}).get("title", ""),
            source_url=doc_record.get("metadata", {}).get("source_url", ""),
            metadata=doc_record.get("metadata", {}),
        )

    # ============================================
    # MÉTODO: get_stats()
    # ============================================

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de auditoría de DIKE."""
        conformes = sum(1 for d in self.dictamenes_emitidos if d["veredicto_final"] == ComplianceVerdict.CONFORME.value)
        no_conformes = sum(1 for d in self.dictamenes_emitidos if d["veredicto_final"] == ComplianceVerdict.NO_CONFORME.value)
        restringidos = sum(1 for d in self.dictamenes_emitidos if d["veredicto_final"] == ComplianceVerdict.CONFORME_CON_RESTRICCIONES.value)
        tasa_conformidad = (conformes / max(1, self.total_auditorias)) * 100

        return {
            "total_auditorias": self.total_auditorias,
            "conformes": conformes,
            "no_conformes": no_conformes,
            "restringidos": restringidos,
            "tasa_conformidad": round(tasa_conformidad, 1),
            "corpus_documentos": len(self.corpus_index.get("documentos", [])),
        }

    # ============================================
    # MATRIZ DE TRAZABILIDAD (Propuesta Zara v1.0)
    # ============================================

    def generate_trace_matrix(self, dictamen: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera entradas de la matriz de trazabilidad a partir de un dictamen.
        Cada dimensión auditada produce una entrada con fuente, artículo,
        evidencia, veredicto, confianza, acción y estado.
        """
        traces: List[Dict[str, Any]] = []
        timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat()

        source_id = dictamen.get("doc_id", "")
        source_hash = dictamen.get("hash_contenido", "")
        source_title = dictamen.get("titulo_documento", "")
        source_url = dictamen.get("url_origen", "")

        # Procesar dimensiones AESIA
        for dim_name, dim_info in dictamen.get("audit_aesia", {}).get("dimensiones", {}).items():
            trace = {
                "trace_id": str(uuidlib.uuid4()),
                "source_id": source_id,
                "source_hash": source_hash,
                "source_title": source_title,
                "source_url": source_url,
                "norm": "AESIA",
                "article_ref": self._map_aesia_article(dim_name),
                "evidence_span": {
                    "fragment": ", ".join(dim_info.get("coincidencias", [])[:3]) if dim_info.get("coincidencias") else "",
                    "page": "",
                    "location": "regex_pattern_match",
                },
                "dimension": dim_name,
                "verdict": dim_info.get("veredicto", "indeterminado"),
                "confidence": {
                    "value": dim_info.get("confianza", 0.0),
                    "explanation": dim_info.get("observacion", ""),
                },
                "finding": dim_info.get("observacion", ""),
                "action": self._suggest_action(dim_name, dim_info.get("veredicto", "")),
                "owner": "DIKE (RGL-01)",
                "status": "abierto" if dim_info.get("veredicto") != "conforme" else "aceptado",
                "created_at": timestamp,
                "updated_at": timestamp,
                "revision_log": [],
            }
            traces.append(trace)

        # Procesar dimensiones RGPD
        for dim_name, dim_info in dictamen.get("audit_rgpd", {}).get("dimensiones", {}).items():
            trace = {
                "trace_id": str(uuidlib.uuid4()),
                "source_id": source_id,
                "source_hash": source_hash,
                "source_title": source_title,
                "source_url": source_url,
                "norm": "RGPD",
                "article_ref": dim_info.get("articulo", ""),
                "evidence_span": {
                    "fragment": ", ".join(dim_info.get("coincidencias", [])[:3]) if dim_info.get("coincidencias") else "",
                    "page": "",
                    "location": "regex_pattern_match",
                },
                "dimension": dim_name,
                "verdict": dim_info.get("veredicto", "indeterminado"),
                "confidence": {
                    "value": dim_info.get("confianza", 0.0),
                    "explanation": dim_info.get("observacion", ""),
                },
                "finding": dim_info.get("observacion", ""),
                "action": self._suggest_action(dim_name, dim_info.get("veredicto", "")),
                "owner": "DIKE (RGL-01)",
                "status": "abierto" if dim_info.get("veredicto") not in ("conforme",) else "aceptado",
                "created_at": timestamp,
                "updated_at": timestamp,
                "revision_log": [],
            }
            traces.append(trace)

        # Guardar matriz en archivo
        trace_file = os.path.join(
            self.audit_log_dir,
            f"trazabilidad_{dictamen.get('dictamen_id', str(uuidlib.uuid4()))[:8]}.json"
        )
        with open(trace_file, "w", encoding="utf-8") as f:
            json.dump(traces, f, indent=2, ensure_ascii=False)

        logger.info(f"[DIKE] Matriz de trazabilidad generada: {len(traces)} entradas")
        return traces

    def _map_aesia_article(self, dimension: str) -> str:
        """Mapea dimensiones AESIA a artículos del Estatuto RD 729/2023."""
        mapping = {
            "transparencia": "RD 729/2023 Art. 7 — Transparencia",
            "no_discriminacion": "RD 729/2023 Art. 5 — Objeto y fines (no discriminacion)",
            "responsabilidad_humana": "RD 729/2023 Art. 9 — Principios de actuacion",
        }
        return mapping.get(dimension, "No determinado")

    def _suggest_action(self, dimension: str, verdict: str) -> str:
        """Sugiere una acción correctora según la dimensión y el veredicto."""
        if verdict == "conforme":
            return "Sin acción requerida. Mantener monitoreo."
        if verdict == "no_conforme":
            return f"Revision manual obligatoria para {dimension}. Documentar base juridica o evidencia faltante."
        if verdict == "conforme_con_restricciones":
            return f"Documentar restricciones aplicables a {dimension}. Verificar condiciones de uso."
        return f"Revisar {dimension}: evidencia insuficiente. Completar documentacion o marcar como indeterminado."

    # ============================================
    # REGISTRO DE EJECUCION (Propuesta Zara — health-check)
    # ============================================

    def generate_run_record(self, script_version: str = "1.0") -> Dict[str, Any]:
        """
        Genera un registro de ejecución según el modelo propuesto por Zara.
        No se ha desplegado en VPS. Es un registro local de auditoría.
        """
        timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat()
        return {
            "run_id": str(uuidlib.uuid4()),
            "started_at": timestamp,
            "finished_at": timestamp,
            "script_version": script_version,
            "config_hash": hashlib.sha256(
                json.dumps(self.get_stats(), sort_keys=True).encode()
            ).hexdigest()[:16],
            "target": self.vault_path,
            "status": "OK",
            "findings": self.get_stats(),
            "alert_id": None,
            "operator": "AutoClaw",
            "reviewer": None,
            "retention_until": "2027-08-10",
            "deployed_to_vps": False,
            "note": "Ejecucion local en Nodo Central. No desplegado en VPS.",
        }
