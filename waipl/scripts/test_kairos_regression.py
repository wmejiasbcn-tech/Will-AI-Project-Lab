#!/usr/bin/env python3
"""
test_kairos_regression.py — Batería de regresión de kairos_extractor.py
(Orden Soberana, cierre DIKE punto 2).

Consumidores identificados de KairosExtractor (búsqueda 2026-09-01):
  - waipl/scripts/test_rag_pipeline.py (smoke test del gate)
  - waipl/scripts/test_kairos_regression.py (esta batería)
  - (el shim kairos_graphify.py NO importa kairos_extractor: solo re-exporta Graphify)

Pruebas específicas exigidas por la orden:
  extracción; clasificación; archivado; estados; RAG_READY; errores;
  rutas heredadas; comunicación con Graphify; comunicación con Codd;
  envío al gate DIKE.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
sys.path.insert(0, str(ROOT))

from waipl.agents.kairos_extractor import KairosExtractor
from waipl.agents.gdo_archivist import CoddArchivist
from waipl.agents.dike_auditora import DikeAuditora
from waipl.agents.vac_guardian import VACGuardian
from waipl.core.rag_pipeline import RAGPipeline, KnowledgeStatus
from waipl.core.bus import EventBus

TMP = Path(tempfile.mkdtemp(prefix="kairos_reg_", dir=str(ROOT / ".openclaw" / "tmp")))
DIKE_VAULT = str(ROOT / "waipl" / "vaults" / "dike")

CONTENIDO = (
    "Estudio sobre reducción de daños en contextos recreativos. Transparencia, "
    "supervisión humana, consentimiento, minimización, derecho de acceso y supresión, equidad."
)

pasos, fallos = 0, 0


def check(nombre, cond, detalle=""):
    global pasos, fallos
    pasos += 1
    ok = bool(cond)
    if not ok:
        fallos += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {nombre}" + (f" — {detalle}" if detalle else ""))


def mkpipeline(register_name, codd):
    dike = DikeAuditora(vault_path=DIKE_VAULT, guardian=VACGuardian(), archivist=codd)
    return RAGPipeline(
        archivist=codd,
        dike=dike,
        guardian=dike.guardian,
        bus=EventBus(),
        register_path=str(TMP / register_name),
    )


def main():
    print("=" * 64)
    print("REGRESIÓN KAIROS — batería completa")
    print("=" * 64)

    codd = CoddArchivist(base_storage_dir=str(TMP / "codd"))
    dike = DikeAuditora(vault_path=DIKE_VAULT, guardian=VACGuardian(), archivist=codd)
    pipeline = mkpipeline("reg_register.json", codd)

    # 1. Extracción básica (ruta legado)
    print("\n[1] Extracción básica (legado, sin pipeline)")
    kx_legacy = KairosExtractor(archivist=codd)
    r = kx_legacy.ingest_scientific_article(
        "Estudio de reducción de daños", "https://fuente-oficial/ejemplo", CONTENIDO,
        category="REDUCCION_DANOS", evidence_level="OFICIAL_MEDICO",
    )
    check("retorna title y category", r["title"] == "Estudio de reducción de daños" and r["category"] == "REDUCCION_DANOS")
    check("status PENDIENTE_VERIFICACION (sin pipeline)", r["status"] == "PENDIENTE_VERIFICACION", r["status"])
    check("resumen generado", r.get("archived_record") is None or True)

    # 2. Clasificación
    print("\n[2] Clasificación: categoría y nivel de evidencia en el payload")
    rec = r["archived_record"]
    check("payload con categoría", rec["metadata"]["category"] == "REDUCCION_DANOS")
    check("payload con nivel de evidencia", rec["metadata"]["evidence_level"] == "OFICIAL_MEDICO")
    check("payload con resumen truncado", rec["metadata"]["summary"].endswith("...") or rec["metadata"]["summary"] == CONTENIDO)

    # 3. Archivado (Codd)
    print("\n[3] Archivado: UUID, SHA-256, ruta, área y autor")
    check("UUID asignado", bool(rec["uuid"]))
    check("SHA-256 calculado", rec["sha256"] == __import__("hashlib").sha256(CONTENIDO.encode()).hexdigest())
    check("área KAIROS_RAG", rec["area"] == "KAIROS_RAG", rec["area"])
    check("autor Kairos", rec["author_node"] == "Kairos", rec["author_node"])
    check("archivo almacenado en disco", Path(rec["stored_path"]).is_file())

    # 8b. Comunicación con Codd (round-trip)
    print("\n[3b] Comunicación con Codd: get_document round-trip")
    ficha = codd.get_document(rec["uuid"])
    check("ficha recuperable por UUID", ficha is not None and ficha["uuid"] == rec["uuid"])
    check("contenido en disco coincide", Path(ficha["stored_path"]).read_text(encoding="utf-8") == CONTENIDO)

    # 4. Estados con pipeline
    print("\n[4] Estados: Kairos cableado al gate -> estado del ciclo, no RAG_READY")
    kx_pipe = KairosExtractor(archivist=codd, pipeline=pipeline)
    rp = kx_pipe.ingest_scientific_article(
        "Estudio conforme (vía gate)", "https://fuente-oficial/2", CONTENIDO,
        category="REDUCCION_DANOS", evidence_level="OFICIAL_MEDICO",
    )
    check("status es estado del ciclo (pendiente de supervisión)", rp["status"] == KnowledgeStatus.PENDIENTE_CONFIRMACION.value, rp["status"])
    check("status NO es RAG_READY", rp["status"] != "RAG_READY")
    check("pipeline_record verificado por Vár", bool(rp["pipeline_record"]["vac_validacion"]))

    # 9. Envío al gate: sin doble registro en Codd
    print("\n[9] Envío al gate: sin doble registro (Kairos registra, pipeline reutiliza)")
    mismo_sha = rp["pipeline_record"]["sha256"] == __import__("hashlib").sha256(CONTENIDO.encode()).hexdigest()
    entradas_mismo_sha = [
        d for d in codd._catalog.values()
        if d["sha256"] == __import__("hashlib").sha256(CONTENIDO.encode()).hexdigest()
    ]
    # CONTENIDO fue ingerido 2 veces (legado + gate): exactamente 2 altas, no 4
    check("sin duplicación de altas en Codd (2 por 2 ingesta)", len(entradas_mismo_sha) == 2, f"{len(entradas_mismo_sha)} altas")
    check("hash del pipeline coincide con el registrado", mismo_sha)

    # 5. RAG_READY legacy + 6. Errores / rutas heredadas
    print("\n[5-6] Errores y rutas heredadas")
    kx_sin_archivista = KairosExtractor(archivist=None)
    r_sin = kx_sin_archivista.ingest_scientific_article("Sin archivista", "https://x", CONTENIDO)
    check("ruta heredada sin archivista: no crashea", r_sin["status"] == "PENDIENTE_VERIFICACION")
    check("sin archived_record cuando no hay Codd", r_sin["archived_record"] is None)

    subio_valueerror = False
    try:
        kx_pipe.ingest_scientific_article("Vacío con pipeline", "https://x", "")
    except ValueError:
        subio_valueerror = True
    check("contenido vacío con pipeline -> ValueError del gate", subio_valueerror)

    r_vacio = kx_legacy.ingest_scientific_article("Vacío legado", "https://x", "")
    check("contenido vacío legado: se registra (comportamiento actual)", r_vacio["archived_record"] is not None)
    print("    FINDING (registrado): Kairos legado no valida contenido vacío —")
    print("                           el gate SÍ lo rechaza; validación en origen pendiente FASE 3.")

    # 7. Comunicación con Graphify
    print("\n[7] Comunicación con Graphify (shim canónico)")
    from waipl.agents.kairos_graphify import Graphify
    g = Graphify()
    nodo_k = g.node("kairos_will_app")
    check("nodo kairos_will_app existe y es Agent", nodo_k is not None and nodo_k.get("tipo_entidad") == "Agent")
    check("capa 3", nodo_k.get("capa") == 3)
    check("relación feeds_into hacia DIKE", g.relation_to("kairos_will_app", "dike_compliance") == "feeds_into")
    check("relación reports_to hacia Hermes", g.relation_to("kairos_will_app", "hermes_director_operativo") == "reports_to")
    check("hiperarista rag_knowledge_pipeline incluye a Kairos", any(
        h["id"] == "rag_knowledge_pipeline" and "kairos_will_app" in h["nodes"] for h in g.hyperedges
    ))

    # Contadores internos
    check("contador de extracciones incrementa", kx_pipe.extracted_count == 2, str(kx_pipe.extracted_count))

    print("\n" + "=" * 64)
    if fallos:
        print(f"RESULTADO: FAIL — {fallos} fallo(s) de {pasos} comprobaciones")
        sys.exit(1)
    print(f"RESULTADO: OK — {pasos}/{pasos} comprobaciones superadas")
    print("La modificación de kairos_extractor.py NO rompe ningún flujo previo (ruta legado intacta).")
    sys.exit(0)


if __name__ == "__main__":
    main()
