#!/usr/bin/env python3
"""
test_gate_dike.py — Batería de validación del ciclo de admisión del WILL RAG
(reconciliación 2026-09-16: DIKE deja de ser gate).

Modelo verificado:
    especialista de dominio (DIKE: dictamen jurídico-normativo, entrada NO decisión)
    → Vár (VAC-01): verificación independiente
    → supervisión humana (obligatoria para conocimiento canónico)
    → conocimiento canónico → WILL RAG

Escenarios:
  1.  Documento conforme                      -> Pendiente → ACCEPT humano -> Aprobado
  2.  Documento no conforme (dictamen DIKE)   -> Pendiente → REJECT humano -> Rechazado
  3.  Datos especialmente protegidos          -> Pendiente + pausa punto 3 → REJECT -> Rechazado
  4.  Documento parcialmente conforme         -> Pendiente confirmación humana (pausa 4)
  5.  Decisión humana                         -> confirm_restricted(True) -> Aprobado con restricciones
  6.  Rechazo                                 -> nunca entra en el WILL RAG
  7.  Bloqueo (Vár BLOQUEADO)                 -> Bloqueado, nunca en el WILL RAG
  8.  Aprobación con restricciones            -> tras confirmación humana
  9.  Documento duplicado                     -> comportamiento documentado (finding)
  10. Documento modificado tras su auditoría  -> alteración detectable + re-verificación
  11. Error de DIKE (fault injection)         -> unidad queda En revisión, nada se aprueba
  12. Error de Vár (fault injection)          -> igual
  13. Pérdida de comunicación (sin Codd)      -> ComplianceGateError, registro intacto
  14. Recuperación del servicio               -> re-verificación + reintento OK

Seguridad y concurrencia:
  A-C. 8 submits simultáneos -> estados correctos, registro JSON válido
  B.   Doble ingestión vía Kairos+pipeline
  E.   Actualización de documento (nueva versión -> nuevo hash -> nuevo dictamen)

Invariantes globales: ninguna unidad Rechazada/Bloqueada/Pendiente en el WILL RAG;
toda unidad canónica pasó por supervisión humana y tiene dictamen del especialista + verificación de Vár.
"""
import concurrent.futures
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
sys.path.insert(0, str(ROOT))

from waipl.agents.gdo_archivist import CoddArchivist
from waipl.agents.dike_auditora import DikeAuditora
from waipl.agents.vac_guardian import VACGuardian
from waipl.core.rag_pipeline import RAGPipeline, KnowledgeStatus, ComplianceGateError
from waipl.core.bus import EventBus

TMP = Path(tempfile.mkdtemp(prefix="gate_dike_", dir=str(ROOT / ".openclaw" / "tmp")))
DIKE_VAULT = str(ROOT / "waipl" / "vaults" / "dike")

TXT_LIMPIO = (
    "Guía de acompañamiento no directivo para la comunidad. "
    "El servicio se rige por la transparencia y la trazabilidad de sus fuentes. "
    "Toda decisión relevante cuenta con supervisión humana y control humano. "
    "El tratamiento se apoya en la equidad, la inclusión y la diversidad. "
    "La base jurídica del tratamiento es el consentimiento informado de las personas usuarias. "
    "Aplicamos minimización: los datos son limitados a lo necesario. "
    "Se garantiza el derecho de acceso y el derecho de supresión."
)
TXT_NO_CONFORME = (
    "Recetario de cocina tradicional: paella con arroz, azafrán y marisco; "
    "gazpacho andaluz; tortilla de patatas. Descripción de elaboraciones y presentaciones."
)
TXT_SENSIBLE = (
    "Protocolo de gestión de dosis y receta médica para personas con diagnóstico de hepatitis. "
    "Describe el tratamiento médico prescrito y el seguimiento de la medicación."
)
TXT_PARCIAL = (
    "Marco de transparencia de la aplicación y supervisión humana de las respuestas generadas."
)
TXT_SENSIBLE_REVOCA = TXT_SENSIBLE + " Contenido añadido en la versión modificada del documento."

pasos, fallos = 0, 0


def check(nombre, cond, detalle=""):
    global pasos, fallos
    pasos += 1
    ok = bool(cond)
    if not ok:
        fallos += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {nombre}" + (f" — {detalle}" if detalle else ""))


class FailingDike:
    """Fault injection: DIKE cae en plena auditoría."""
    def generate_compliance_report(self, *a, **k):
        raise RuntimeError("FALLO SIMULADO: DIKE indisponible")


class FailingGuardian:
    """Fault injection: Vár cae en plena verificación."""
    def evaluate_output(self, *a, **k):
        raise RuntimeError("FALLO SIMULADO: Vár (VAC-01) indisponible")


def mkpipeline(bus=None, dike=None, guardian=None, nombre="x"):
    codd = CoddArchivist(base_storage_dir=str(TMP / f"codd_{nombre}"))
    d = dike or DikeAuditora(
        vault_path=DIKE_VAULT,
        guardian=guardian or VACGuardian(),
        archivist=codd,
    )
    return RAGPipeline(
        archivist=codd,
        dike=d,
        guardian=guardian or getattr(d, "guardian", None),
        bus=bus,
        register_path=str(TMP / "knowledge_register_gate.json"),
    )


def main():
    print("=" * 64)
    print("BATERÍA CICLO WILL RAG — 14 escenarios + seguridad/concurrencia")
    print("(DIKE especialista · Vár verificación independiente · supervisión humana)")
    print("=" * 64)

    bus = EventBus()
    pipe = mkpipeline(bus=bus, nombre="principal")

    # 1. Documento conforme -> Pendiente -> ACCEPT humano -> Aprobado
    print("\n[1] Documento conforme -> supervisión humana -> Aprobado")
    r1 = pipe.submit_knowledge_unit("Guía conforme", "https://src/1", TXT_LIMPIO, "GENERAL", "OFICIAL")
    check("Pendiente confirmación humana (nadie decide por sí mismo)",
          r1["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r1["estado"])
    check("dictamen del especialista + Vár presentes",
          bool(r1["dictamen_id"]) and bool(r1["vac_validacion"]))
    r1 = pipe.resolver_supervision_humana(r1["doc_uuid"], "ACCEPT", "william_mnj", "conforme")
    check("Aprobado tras ACCEPT humano", r1["estado"] == KnowledgeStatus.APROBADO.value, r1["estado"])
    check("fecha_publicacion registrada", bool(r1.get("fecha_publicacion")))
    check("especialista de adquisición y versión",
          r1.get("especialista_adquisicion") in ("Kairos", "DIKE") and r1.get("version") == 1)

    # 2. Documento no conforme -> Pendiente -> REJECT humano -> Rechazado
    print("\n[2] Documento no conforme -> REJECT humano -> Rechazado")
    r2 = pipe.submit_knowledge_unit("Recetario", "https://src/2", TXT_NO_CONFORME, "GENERAL", "OFICIAL")
    check("Pendiente (DIKE no decide)", r2["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r2["estado"])
    r2 = pipe.resolver_supervision_humana(r2["doc_uuid"], "REJECT", "carla", "no conforme")
    check("Rechazado", r2["estado"] == KnowledgeStatus.RECHAZADO.value, f"{r2['estado']} / veredicto {r2['veredicto_final']}")

    # 3. Datos especialmente protegidos sin base jurídica
    print("\n[3] Datos sensibles Art. 9 -> Pendiente + pausa 3 -> REJECT -> Rechazado")
    r3 = pipe.submit_knowledge_unit("Protocolo clínico", "https://src/3", TXT_SENSIBLE, "SALUD", "OFICIAL_MEDICO")
    check("Pendiente (dictamen de especialista como entrada)",
          r3["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r3["estado"])
    check("pausa punto 3 al Soberano", any(p["punto"] == 3 for p in r3["pausas_simbioticas"]))
    check("mensaje en bus a soberano_william", any(m["recipient_id"] == "soberano_william" for m in bus.get_history(200)))
    r3 = pipe.resolver_supervision_humana(r3["doc_uuid"], "REJECT", "carla", "sin base jurídica")
    check("Rechazado", r3["estado"] == KnowledgeStatus.RECHAZADO.value, r3["estado"])

    # 4-5. Parcialmente conforme / decisión humana
    print("\n[4-5] Parcialmente conforme -> decisión humana (pausa punto 4)")
    r4 = pipe.submit_knowledge_unit("Marco parcial", "https://src/4", TXT_PARCIAL, "GOBERNANZA", "OFICIAL")
    check("Pendiente confirmación humana", r4["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r4["estado"])
    check("pausa punto 4 a Carla", any(p["punto"] == 4 for p in r4["pausas_simbioticas"]))
    check("mensaje en bus a node_carla (punto 4)",
          any(m["recipient_id"] == "node_carla" and m["content"].get("punto") == 4 for m in bus.get_history(200)))
    check("NO publicado", r4["estado"] not in (KnowledgeStatus.APROBADO.value, KnowledgeStatus.APROBADO_CON_RESTRICCIONES.value))

    # 8. Aprobación con restricciones tras confirmación humana
    print("\n[8] Confirmación humana -> Aprobado con restricciones")
    r8 = pipe.confirm_restricted(r4["doc_uuid"], approved=True, reviewer="Carla", note="Restricciones documentadas")
    check("Aprobado con restricciones", r8["estado"] == KnowledgeStatus.APROBADO_CON_RESTRICCIONES.value, r8["estado"])
    check("fecha_publicacion tras confirmación", bool(r8.get("fecha_publicacion")))

    # 7. Bloqueo (Vár BLOQUEADO)
    print("\n[7] Bloqueo — Vár (VAC-01) BLOQUEADO")
    pipe_bloqueo = mkpipeline(dike=DikeAuditora(vault_path=DIKE_VAULT, guardian=VACGuardian(pass_threshold=0.97, warn_threshold=0.96)), nombre="bloqueo")
    r7 = pipe_bloqueo.submit_knowledge_unit("Documento bloqueado", "https://src/7", TXT_LIMPIO, "GENERAL", "OFICIAL")
    check("Bloqueado", r7["estado"] == KnowledgeStatus.BLOQUEADO.value, r7["estado"])
    check("vac_validacion = BLOQUEADO", r7.get("vac_validacion", {}).get("status") == "BLOQUEADO", str(r7.get("vac_validacion")))
    check("NO está en el WILL RAG", r7["doc_uuid"] not in {u["doc_uuid"] for u in pipe_bloqueo.approved_units()})

    # 9. Documento duplicado
    print("\n[9] Documento duplicado (mismo contenido, dos altas)")
    rd1 = pipe.submit_knowledge_unit("Duplicado A", "https://src/9a", TXT_LIMPIO, "GENERAL", "OFICIAL")
    rd2 = pipe.submit_knowledge_unit("Duplicado B", "https://src/9b", TXT_LIMPIO, "GENERAL", "OFICIAL")
    check("dos UUID distintos", rd1["doc_uuid"] != rd2["doc_uuid"])
    check("mismo sha256", rd1["sha256"] == rd2["sha256"], rd1["sha256"][:16] + "...")
    check("ambos auditados individualmente (entrada de especialista)",
          bool(rd1["dictamen_id"]) and bool(rd2["dictamen_id"]))
    print("    FINDING (registrado): sin política de deduplicación — cada copia se audita por separado.")

    # 10. Documento modificado tras su auditoría
    print("\n[10] Alteración post-auditoría -> detectable + re-verificación")
    target = pipe.get_unit(r1["doc_uuid"])
    stored = Path(target["stored_path"])
    original = stored.read_bytes()
    stored.write_text(TXT_SENSIBLE_REVOCA, encoding="utf-8")
    hash_actual = hashlib.sha256(stored.read_bytes()).hexdigest()
    check("alteración detectable por hash", hash_actual != target["sha256"], "sha256 != registrado")
    r10 = pipe.audit_registered_document(r1["doc_uuid"])
    check("re-verificación devuelve la unidad a supervisión humana",
          r10["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r10["estado"])
    check("revocado: sale del WILL RAG",
          r10["doc_uuid"] not in {u["doc_uuid"] for u in pipe.approved_units()})
    stored.write_bytes(original)

    # 11. Error de DIKE (fault injection)
    print("\n[11] Error de DIKE -> unidad permanece En revisión")
    pipe_err = mkpipeline(dike=FailingDike(), nombre="err")
    codd_err = pipe_err.archivist
    doc_err = codd_err.register_document("err.txt", b"contenido de prueba", area="RAG_DOMINIO_A", author_node="RAG-Pipeline")
    subio = False
    try:
        pipe_err.submit_knowledge_unit("Con DIKE caída", "https://src/11", TXT_LIMPIO, doc_record=doc_err)
    except RuntimeError:
        subio = True
    check("excepción propagada", subio)
    u11 = pipe_err.get_register()["unidades"].get(doc_err["uuid"])
    check("unidad queda En revisión (nunca aprobada por defecto)", u11["estado"] == KnowledgeStatus.EN_REVISION.value, u11["estado"])

    # 12. Error de Vár (fault injection)
    print("\n[12] Error de Vár -> unidad permanece En revisión")
    pipe_err2 = mkpipeline(guardian=FailingGuardian(), nombre="err2")
    codd_err2 = pipe_err2.archivist
    doc_err2 = codd_err2.register_document("err2.txt", b"contenido de prueba 2", area="RAG_DOMINIO_A", author_node="RAG-Pipeline")
    subio2 = False
    try:
        pipe_err2.submit_knowledge_unit("Con Vár caída", "https://src/12", TXT_LIMPIO, doc_record=doc_err2)
    except RuntimeError:
        subio2 = True
    check("excepción propagada (fallo seguro)", subio2)
    u12 = pipe_err2.get_register()["unidades"].get(doc_err2["uuid"])
    check("unidad queda En revisión", u12["estado"] == KnowledgeStatus.EN_REVISION.value, u12["estado"])

    # 13. Pérdida de comunicación (sin Codd y sin doc_record)
    print("\n[13] Pérdida de comunicación -> ComplianceGateError, registro intacto")
    pipe_sin_codd = RAGPipeline(
        archivist=None,
        dike=DikeAuditora(vault_path=DIKE_VAULT, guardian=VACGuardian()),
        register_path=str(TMP / "register_sin_codd.json"),
    )
    n_antes = len(pipe_sin_codd.get_register()["unidades"])
    lanzo = False
    try:
        pipe_sin_codd.submit_knowledge_unit("Sin Codd", "https://src/13", TXT_LIMPIO)
    except ComplianceGateError:
        lanzo = True
    check("ComplianceGateError lanzado", lanzo)
    check("registro intacto (0 unidades nuevas)", len(pipe_sin_codd.get_register()["unidades"]) == n_antes == 0)

    # 14. Recuperación del servicio + reintentos (D)
    print("\n[14] Recuperación del servicio + reintentos")
    pipe_rec = mkpipeline(nombre="rec")
    doc_rec = pipe_rec.archivist.register_document("rec.txt", TXT_LIMPIO.encode(), area="RAG_DOMINIO_A", author_node="RAG-Pipeline")
    pipe_rec.register["unidades"][doc_rec["uuid"]] = {
        "doc_uuid": doc_rec["uuid"], "title": "Recuperación", "source_url": "https://src/14",
        "category": "GENERAL", "evidence_level": "OFICIAL", "especialista_adquisicion": "Kairos",
        "version": 1, "sha256": doc_rec["sha256"], "stored_path": doc_rec["stored_path"],
        "registered_at": doc_rec["timestamp"], "estado_anterior": "Borrador",
        "estado": KnowledgeStatus.EN_REVISION.value,
        "historial": [], "dictamen_id": None, "dictamen_timestamp": None, "dictamen_path": None,
        "veredicto_final": None, "confianza_global": None, "pausas_simbioticas": [],
        "vac_validacion": None, "fecha_publicacion": None, "actualizado_at": pipe_rec._now(),
    }
    pipe_rec._save_register()
    r14 = pipe_rec.audit_registered_document(doc_rec["uuid"])
    check("re-verificación lleva a supervisión humana",
          r14["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r14["estado"])
    r14 = pipe_rec.resolver_supervision_humana(doc_rec["uuid"], "ACCEPT", "carla", "ok")
    check("ACCEPT completa la transición", r14["estado"] == KnowledgeStatus.APROBADO.value, r14["estado"])
    r14b = pipe_rec.submit_knowledge_unit("Reintento tras fallo", "https://src/14b", TXT_LIMPIO, "GENERAL", "OFICIAL")
    r14b = pipe_rec.resolver_supervision_humana(r14b["doc_uuid"], "ACCEPT", "carla", "ok")
    check("reintento posterior funciona", r14b["estado"] == KnowledgeStatus.APROBADO.value, r14b["estado"])

    # A-C. Concurrencia: 8 submits simultáneos
    print("\n[A-C] Concurrencia: 8 documentos simultáneos (ThreadPool 8)")
    def submit_i(i):
        return pipe.submit_knowledge_unit(f"Concurrente {i}", f"https://src/c{i}", TXT_LIMPIO + f" Variante {i}.", "GENERAL", "OFICIAL")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        resultados = list(ex.map(submit_i, range(8)))
    uuids = [r["doc_uuid"] for r in resultados]
    check("8/8 unidades procesadas", len(resultados) == 8)
    check("UUIDs únicos (sin colisiones)", len(set(uuids)) == 8)
    check("todas en supervisión humana (nada auto-aprobado)",
          all(r["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value for r in resultados))
    reg = json.loads(Path(pipe.register_path).read_text(encoding="utf-8"))
    check("registro JSON válido tras concurrencia", len(reg["unidades"]) >= 8)

    # B. Doble ingestión vía Kairos+pipeline
    print("\n[B] Doble ingestión (mismo contenido por dos rutas)")
    from waipl.agents.kairos_extractor import KairosExtractor
    kx = KairosExtractor(archivist=pipe.archivist, pipeline=pipe)
    ka = kx.ingest_scientific_article("Doble A", "https://src/d", TXT_LIMPIO, category="GENERAL")
    kb = kx.ingest_scientific_article("Doble B", "https://src/d", TXT_LIMPIO, category="GENERAL")
    check("dos altas independientes con mismo hash",
          ka["pipeline_record"]["sha256"] == kb["pipeline_record"]["sha256"]
          and ka["pipeline_record"]["doc_uuid"] != kb["pipeline_record"]["doc_uuid"])

    # E. Actualización de documento (nueva versión)
    print("\n[E] Actualización de documento -> nueva versión, nuevo hash, nuevo dictamen")
    r_old = pipe.submit_knowledge_unit("Doc versionado v1", "https://src/v", TXT_LIMPIO, "GENERAL", "OFICIAL")
    v1_hash = r_old["sha256"]
    r_new = pipe.submit_knowledge_unit("Doc versionado v2", "https://src/v", TXT_LIMPIO + " Contenido ampliado de la versión 2.", "GENERAL", "OFICIAL")
    check("nuevo hash en nueva versión", r_new["sha256"] != v1_hash)
    check("ambas versiones con dictamen de especialista", bool(r_old["dictamen_id"]) and bool(r_new["dictamen_id"]))

    # Invariantes globales
    print("\n[INVARIANTES GLOBALES]")
    aprobados = {u["doc_uuid"] for u in pipe.approved_units()}
    prohibidos = [
        u for u in pipe.get_register()["unidades"].values()
        if u["estado"] in (
            KnowledgeStatus.RECHAZADO.value,
            KnowledgeStatus.BLOQUEADO.value,
            KnowledgeStatus.PENDIENTE_CONFIRMACION.value,
        )
    ]
    check("ninguna Rechazada/Bloqueada/Pendiente en el WILL RAG",
          all(u["doc_uuid"] not in aprobados for u in prohibidos))
    check("toda unidad canónica pasó por supervisión humana y tiene dictamen + Vár",
          all(u.get("supervision_humana") and u.get("dictamen_id") and u.get("vac_validacion")
              for u in pipe.get_register()["unidades"].values()
              if u["estado"] in (KnowledgeStatus.APROBADO.value, KnowledgeStatus.APROBADO_CON_RESTRICCIONES.value)))
    estados = pipe.units_by_status()
    print(f"  Estados finales: {estados}")

    print("\n" + "=" * 64)
    if fallos:
        print(f"RESULTADO: FAIL — {fallos} fallo(s) de {pasos} comprobaciones")
        sys.exit(1)
    print(f"RESULTADO: OK — {pasos}/{pasos} comprobaciones superadas")
    sys.exit(0)


if __name__ == "__main__":
    main()
