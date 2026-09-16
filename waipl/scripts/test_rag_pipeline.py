#!/usr/bin/env python3
"""
test_rag_pipeline.py — Smoke test del ciclo de admisión del WILL RAG (RAG de Will App).

Cadena verificada (reconciliación 2026-09-16):
    especialista de dominio (Kairos: médico-científico y comunitario;
                             DIKE: jurídico-normativo)
    → Vár (VAC-01): verificación independiente
    → supervisión humana (obligatoria para conocimiento canónico)
    → conocimiento canónico → WILL RAG

Se comprueba expresamente:
    - DIKE NO es gate: su dictamen es entrada de especialista, no decisión.
    - Ninguna unidad entra en el WILL RAG sin supervisión humana (ACCEPT).
    - Kairos es especialista de dominio; no marca «apto» por sí mismo.

El registro/almacenamiento usan rutas temporales para no contaminar el registro canónico.
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
sys.path.insert(0, str(ROOT))

from waipl.agents.gdo_archivist import CoddArchivist
from waipl.agents.dike_auditora import DikeAuditora
from waipl.agents.vac_guardian import VACGuardian
from waipl.agents.kairos_extractor import KairosExtractor
from waipl.core.rag_pipeline import (
    RAGPipeline, KnowledgeStatus, DOMINIO_MEDICO, DOMINIO_JURIDICO,
)
from waipl.core.bus import EventBus

TMP = Path(tempfile.mkdtemp(prefix="rag_smoke_", dir=str(ROOT / ".openclaw" / "tmp")))

CONTENIDO_LIMPIO = (
    "Guía de acompañamiento no directivo para la comunidad. "
    "El servicio se rige por la transparencia y la trazabilidad de sus fuentes. "
    "Toda decisión relevante cuenta con supervisión humana y control humano. "
    "El tratamiento se apoya en la equidad, la inclusión y la diversidad. "
    "La base jurídica del tratamiento es el consentimiento informado de las personas usuarias. "
    "Aplicamos minimización: los datos son limitados a lo necesario. "
    "Se garantiza el derecho de acceso y el derecho de supresión."
)

CONTENIDO_SENSIBLE = (
    "Protocolo de gestión de dosis y receta médica para personas con diagnóstico de hepatitis. "
    "Describe el tratamiento médico prescrito y el seguimiento de la medicación."
)

CONTENIDO_PARCIAL = (
    "Marco de transparencia de la aplicación y supervisión humana de las respuestas generadas."
)

paso = 0
fallos = 0


def check(nombre, condicion, detalle=""):
    global paso, fallos
    paso += 1
    marca = "PASS" if condicion else "FAIL"
    if not condicion:
        fallos += 1
    print(f"  [{marca}] {nombre}" + (f" — {detalle}" if detalle else ""))


def main():
    print("=" * 64)
    print("SMOKE TEST — Ciclo de admisión WILL RAG")
    print("(especialista → Vár → supervisión humana → conocimiento canónico)")
    print("=" * 64)

    bus = EventBus()
    codd = CoddArchivist(base_storage_dir=str(TMP / "codd_storage"))
    dike = DikeAuditora(
        vault_path=str(ROOT / "waipl" / "vaults" / "dike"),
        guardian=VACGuardian(),
    )
    pipeline = RAGPipeline(
        archivist=codd,
        dike=dike,
        guardian=VACGuardian(),
        bus=bus,
        register_path=str(TMP / "knowledge_register_smoke.json"),
    )

    # ── Caso 1: unidad médico-científica limpia → Vár → supervisión humana ──
    print("\n[CASO 1] Unidad médico-científica limpia → Vár → supervisión humana → Aprobado")
    r1 = pipeline.submit_knowledge_unit(
        title="Guía de acompañamiento no directivo",
        source_url="https://example.org/guia",
        content_text=CONTENIDO_LIMPIO,
        category="ACOMPAÑAMIENTO",
        evidence_level="OFICIAL",
        dominio=DOMINIO_MEDICO,
    )
    check("NO auto-Aprobado (nadie decide por sí mismo)",
          r1["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r1["estado"])
    check("especialista de adquisición médico es Kairos",
          r1["especialista_adquisicion"] == "Kairos", r1["especialista_adquisicion"])
    check("Vár verificó independientemente", bool(r1["vac_validacion"]), str(r1["vac_validacion"]))
    r1b = pipeline.resolver_supervision_humana(r1["doc_uuid"], "ACCEPT", "william_mnj", "conforme")
    check("ACCEPT humano → Aprobado", r1b["estado"] == KnowledgeStatus.APROBADO.value, r1b["estado"])
    check("supervisión humana registrada",
          bool(r1b["supervision_humana"]) and r1b["supervision_humana"]["human_decision"] == "ACCEPT")
    check("entra en el WILL RAG", r1["doc_uuid"] in {u["doc_uuid"] for u in pipeline.approved_units()})

    # ── Caso 2: contenido jurídico-normativo no conforme (DIKE especialista) ──
    print("\n[CASO 2] Jurídico-normativo: DIKE dictamina 'No conforme' (entrada, no decisión)")
    r2 = pipeline.submit_knowledge_unit(
        title="Protocolo clínico (prueba de no conformidad normativa)",
        source_url="https://example.org/clinico",
        content_text=CONTENIDO_SENSIBLE,
        category="SALUD",
        evidence_level="OFICIAL_MEDICO",
        dominio=DOMINIO_JURIDICO,
    )
    check("DIKE dictamina pero NO decide: estado Pendiente confirmación",
          r2["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r2["estado"])
    check("dictamen del especialista es entrada, no gate",
          r2["dictamen_especialista"] is not None
          and r2["dictamen_especialista"]["jurisdiccion"].endswith("(NO gate)"))
    check("veredicto del especialista registrado",
          r2["veredicto_final"] == "No conforme", str(r2["veredicto_final"]))
    check("pausa simbiótica punto 3 propagada al registro",
          any(p.get("punto") == 3 for p in r2["pausas_simbioticas"]))
    r2b = pipeline.resolver_supervision_humana(r2["doc_uuid"], "REJECT", "carla", "no conforme")
    check("REJECT humano → Rechazado", r2b["estado"] == KnowledgeStatus.RECHAZADO.value, r2b["estado"])
    check("NO está en el WILL RAG",
          r2["doc_uuid"] not in {u["doc_uuid"] for u in pipeline.approved_units()})

    # ── Caso 3: parcial → supervisión humana con restricciones ─────────────
    print("\n[CASO 3] Jurídico-normativo parcial → supervisión humana → Aprobado con restricciones")
    r3 = pipeline.submit_knowledge_unit(
        title="Marco de transparencia (prueba de restricciones)",
        source_url="https://example.org/marco",
        content_text=CONTENIDO_PARCIAL,
        category="GOBERNANZA",
        evidence_level="OFICIAL",
        dominio=DOMINIO_JURIDICO,
    )
    check("estado intermedio Pendiente confirmación humana",
          r3["estado"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, r3["estado"])
    r3b = pipeline.confirm_restricted(r3["doc_uuid"], approved=True, reviewer="Carla")
    check("estado final Aprobado con restricciones",
          r3b["estado"] == KnowledgeStatus.APROBADO_CON_RESTRICCIONES.value, r3b["estado"])
    try:
        pipeline.confirm_restricted(r3["doc_uuid"], approved=True, reviewer="Carla")
        check("segunda confirmación rechazada", False, "no lanzó error")
    except Exception as e:
        check("segunda confirmación rechazada", "Pendiente" in str(e) or "no está" in str(e), type(e).__name__)

    # ── Caso 4: Kairos cableado al pipeline (no marca apto) ────────────────
    print("\n[CASO 4] Kairos → pipeline (estado del ciclo, no RAG_READY)")
    kairos = KairosExtractor(archivist=codd, pipeline=pipeline)
    k1 = kairos.ingest_scientific_article(
        title="Evidencia sobre acompañamiento (vía Kairos)",
        source_url="https://example.org/evidencia",
        content_text=CONTENIDO_LIMPIO + " Documento adicional con consentimiento y minimización.",
        category="REDUCCION_DANOS",
        evidence_level="OFICIAL_MEDICO",
    )
    check("status NO es RAG_READY", k1["status"] != "RAG_READY", k1["status"])
    check("status refleja el ciclo (pendiente de supervisión)",
          k1["status"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, k1["status"])
    check("pipeline_record presente", bool(k1.get("pipeline_record")))

    # ── Caso 5: Kairos sin pipeline (no marca apto) ────────────────────────
    print("\n[CASO 5] Kairos sin pipeline → no marca apto")
    kairos_off = KairosExtractor(archivist=codd)
    k2 = kairos_off.ingest_scientific_article(
        title="Documento sin pipeline",
        source_url="https://example.org/sin-pipeline",
        content_text=CONTENIDO_LIMPIO,
    )
    check("status PENDIENTE_VERIFICACION (no RAG_READY)", k2["status"] == "PENDIENTE_VERIFICACION", k2["status"])

    # ── Invariantes ────────────────────────────────────────────────────────
    print("\n[INVARIANTES]")
    st = pipeline.stats()
    print(f"  Registro: {st['total_unidades']} unidades | por estado: {st['por_estado']} | en WILL RAG: {st['en_will_rag']}")
    aprobadas = pipeline.approved_units()
    check("toda unidad canónica pasó por supervisión humana",
          all(u.get("supervision_humana") for u in aprobadas))
    rechazadas = [
        u for u in pipeline.get_register()["unidades"].values()
        if u["estado"] in (KnowledgeStatus.RECHAZADO.value, KnowledgeStatus.BLOQUEADO.value)
    ]
    check("ninguna unidad Rechazada/Bloqueada está en el WILL RAG",
          all(u["doc_uuid"] not in {a["doc_uuid"] for a in aprobadas} for u in rechazadas))
    hist = bus.get_history(100)
    n_sup = sum(1 for m in hist if m["content"].get("tipo") == "supervision_humana")
    print(f"  Historial del bus: {len(hist)} mensajes ({n_sup} de supervisión)")
    check("hay mensajes de supervisión en el bus", n_sup >= 3)

    print("\n" + "=" * 64)
    if fallos:
        print(f"RESULTADO: {fallos} fallo(s) de {paso} comprobaciones")
        sys.exit(1)
    print(f"RESULTADO: OK — {paso}/{paso} comprobaciones superadas")
    sys.exit(0)


if __name__ == "__main__":
    main()
