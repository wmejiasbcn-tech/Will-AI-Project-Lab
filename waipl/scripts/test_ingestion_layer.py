#!/usr/bin/env python3
"""
test_ingestion_layer.py — Batería FASE 2: Ingestion Layer de Will App
(Orden Soberana v0.3.1 — FASE 2 AUTHORIZED).

Casos obligatorios:
  A. documento válido → ingestión correcta
  B. documento sin decisión humana → bloqueo
  C. documento rechazado → bloqueo
  D. documento obsoleto → bloqueo
  E. documento revocado → bloqueo
  F. documento duplicado → ALIAS, cero embeddings nuevos
  G. nueva versión → correcta relación con versión anterior (reemplaza_a)
  H. versión anterior → no recuperable como vigente
  I. pérdida o alteración de procedencia → bloqueo
  J. concurrencia/reintentos → resultado idempotente
  K. contenido multimodal → preservación de estructura
  L. trazabilidad → reconstrucción completa del ciclo
  M. intento directo desde Archivo Documental → bloqueo
"""
import concurrent.futures
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
sys.path.insert(0, str(ROOT))

from waipl.core.knowledge_model import (
    KnowledgeStore, Domain, VerificationResult, HumanDecisionType,
    VersionState, IngestionState,
)
from waipl.core.ingestion_layer import (
    IngestionLayer, IngestionBlockedError, ArchiveNotAuthorizedError,
)
from waipl.agents.gdo_archivist import CoddArchivist

TMP = Path(tempfile.mkdtemp(prefix="ingestion_l2_", dir=str(ROOT / ".openclaw" / "tmp")))
TXT = (
    "Guía comunitaria de acompañamiento no directivo. Transparencia y trazabilidad de fuentes. "
    "Supervisión humana de toda salida. Consentimiento informado como base jurídica. "
    "Minimización: datos limitado a lo necesario. Derecho de acceso y de supresión garantizados."
)
TXT_V2 = TXT + " Anexo de la versión 2 con contenido ampliado y vigente."

pasos, fallos = 0, 0


def check(nombre, cond, detalle=""):
    global pasos, fallos
    pasos += 1
    ok = bool(cond)
    if not ok:
        fallos += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {nombre}" + (f" — {detalle}" if detalle else ""))


def expect_bloqueo(nombre, fn, contiene=None):
    try:
        fn()
        check(nombre, False, "no bloqueó")
    except IngestionBlockedError as e:
        ok = (contiene is None) or (contiene.lower() in str(e).lower())
        check(nombre, ok, str(e)[:90])
    except Exception as e:
        check(nombre, False, f"excepción incorrecta: {type(e).__name__}: {e}")


def expect_excepcion(nombre, fn, exc_type, contiene=None):
    try:
        fn()
        check(nombre, False, "no lanzó excepción")
    except exc_type as e:
        ok = (contiene is None) or (contiene.lower() in str(e).lower())
        check(nombre, ok, str(e)[:90])
    except Exception as e:
        check(nombre, False, f"excepción incorrecta: {type(e).__name__}: {e}")


def main():
    print("=" * 64)
    print("FASE 2 — INGESTION LAYER (Orden Soberana v0.3.1) — casos A-M")
    print("=" * 64)

    store = KnowledgeStore(str(TMP / "kmodel_f2.json"))
    layer = IngestionLayer(store)

    def cadena(titulo, texto, domain=Domain.MEDICO_CIENTIFICO_COMUNITARIO,
               decidir=True, decision=HumanDecisionType.ACCEPT, supersedes=None,
               con_procedencia=True):
        src = store.register_source("Fuente oficial", "https://fuente/oficial", "OMS")
        doc = store.register_document(src, titulo, domain)
        ver = store.register_version(doc, texto, str(TMP / f"{doc[:8]}.txt"),
                                     supersedes_version_id=supersedes)
        if con_procedencia:
            store.register_acquisition(ver, "KAIROS" if domain == Domain.MEDICO_CIENTIFICO_COMUNITARIO else "DIKE")
            store.register_verification(ver, "Vár (VAC-01)", VerificationResult.CONFORME, 0.9,
                                        auditor="Yata" if decidir and domain == Domain.JURIDICO_NORMATIVO else None)
        else:
            # sin procedencia: solo alta de versión (para el caso I)
            pass
        if decidir:
            store.decide(ver, "WILLIAM-SCY-01", decision, "Revisión soberana del contenido")
        return ver

    # ── A. documento válido → ingestión correcta ─────────────────────────
    print("\n[A] Documento válido → ingestión correcta")
    ver_a = cadena("Guía válida", TXT)
    res_a = layer.ingest_canonical(ver_a, structure={"texto": TXT}, content_text=TXT, verify_content=True)
    check("ingesta INGESTADO", res_a["accion"] == "INGESTADO", str(res_a["accion"]))
    check("chunks creados", res_a["chunks"] >= 1, f"{res_a['chunks']} chunks")
    ing = store._state["ingestions"][res_a["ingestion_id"]]
    check("estado INGESTADO en el modelo", ing["state"] == IngestionState.INGESTADO.value)
    ch0 = store.chunks_of(ver_a)[0]
    proc = ch0["metadata"]
    check("procedencia primaria en chunk (source/document/version/hash/domain)",
          all(k in proc for k in ("source_id", "document_id", "version_id", "content_hash", "domain")))
    check("metadatos de Vár preservados", proc.get("verificacion", {}).get("verifier") == "Vár (VAC-01)")
    check("supervisión humana preservada", proc.get("supervision_humana", {}).get("human_reviewer_id") == "WILLIAM-SCY-01")
    check("sin embeddings productivos (FASE 3 pendiente)",
          all(e["vector_ref"] is None and e["dimensions"] == 0 for e in store._state["embeddings"].values()))
    check("recuperable por Will App", ver_a in store.retrievable_versions())

    # ── B. sin decisión humana → bloqueo ─────────────────────────────────
    print("\n[B] Sin decisión humana → bloqueo")
    ver_b = cadena("Pendiente de decisión", TXT + " variante B.", decidir=False)
    check("estado PENDIENTE_DECISION_HUMANA", store._get_version(ver_b)["state"] == VersionState.PENDIENTE_DECISION_HUMANA.value)
    expect_bloqueo("ingesta bloqueada", lambda: layer.ingest_canonical(ver_b, structure={"texto": "x"}), "supervisión humana")

    # ── C. documento rechazado → bloqueo ─────────────────────────────────
    print("\n[C] Documento rechazado → bloqueo")
    ver_c = cadena("Guía rechazada", TXT + " variante C.", decidir=True, decision=HumanDecisionType.REJECT)
    check("estado CUARENTENA", store._get_version(ver_c)["state"] == VersionState.CUARENTENA.value)
    expect_bloqueo("ingesta bloqueada", lambda: layer.ingest_canonical(ver_c, structure={"texto": "x"}), "CUARENTENA")

    # ── D. documento obsoleto → bloqueo ──────────────────────────────────
    print("\n[D] Documento obsoleto → bloqueo")
    ver_d1 = cadena("Guía obsoleta v1", TXT + " variante D v1.", decidir=False)
    store.decide(ver_d1, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aceptada v1")
    layer.ingest_canonical(ver_d1, structure={"texto": TXT + " variante D v1."})
    ver_d2 = store.register_version(store._state["documents"][store._get_version(ver_d1)["document_id"]]["document_id"],
                                    TXT + " variante D v2.", str(TMP / "d2.txt"), supersedes_version_id=ver_d1)
    store.register_acquisition(ver_d2, "KAIROS")
    store.register_verification(ver_d2, "Vár (VAC-01)", VerificationResult.CONFORME, 0.93)
    store.decide(ver_d2, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aceptada v2")
    layer.ingest_canonical(ver_d2, structure={"texto": TXT + " variante D v2."})
    check("v1 en OBSOLETA", store._get_version(ver_d1)["state"] == VersionState.OBSOLETA.value)
    expect_bloqueo("ingesta de obsoleta bloqueada", lambda: layer.ingest_canonical(ver_d1, structure={"texto": "x"}), "OBSOLETA")

    # ── E. documento revocado → bloqueo ──────────────────────────────────
    print("\n[E] Documento revocado → bloqueo")
    ver_e = cadena("Guía revocada", TXT + " variante E.", decidir=False)
    store.decide(ver_e, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aceptada")
    layer.ingest_canonical(ver_e, structure={"texto": TXT + " variante E."})
    store.revoke(ver_e, "Retirada por orden soberana", actor="WILLIAM-SCY-01")
    check("estado REVOCADA", store._get_version(ver_e)["state"] == VersionState.REVOCADA.value)
    expect_bloqueo("ingesta de revocada bloqueada", lambda: layer.ingest_canonical(ver_e, structure={"texto": "x"}), "REVOCADA")

    # ── F. duplicado → ALIAS, cero embeddings nuevos ─────────────────────
    print("\n[F] Duplicado → ALIAS, cero embeddings nuevos")
    emb_antes = len(store._state["embeddings"])
    ver_f = cadena("Duplicado exacto de la guía válida", TXT)
    check("mismo content_hash que A", store._get_version(ver_f)["content_hash"] == store._get_version(ver_a)["content_hash"])
    res_f = layer.ingest_canonical(ver_f, structure={"texto": TXT})
    check("acción ALIAS", res_f["accion"] == "ALIAS", str(res_f["accion"]))
    check("alias apunta a la canónica A", res_f["canonical_version_id"] == ver_a)
    check("cero embeddings nuevos", len(store._state["embeddings"]) == emb_antes,
          f"{emb_antes} → {len(store._state['embeddings'])}")
    check("duplicado NO recuperable; canónica sí",
          ver_f not in store.retrievable_versions() and ver_a in store.retrievable_versions())
    check("operación auditada", any(e["action"] == "make_alias" for e in store.audit_log()))

    # ── G. nueva versión → relación reemplaza_a ──────────────────────────
    print("\n[G] Nueva versión → relación con la anterior")
    doc_g = store._state["documents"][store._get_version(ver_a)["document_id"]]["document_id"]
    ver_g2 = store.register_version(doc_g, TXT_V2, str(TMP / "g2.txt"), supersedes_version_id=ver_a)
    store.register_acquisition(ver_g2, "KAIROS")
    store.register_verification(ver_g2, "Vár (VAC-01)", VerificationResult.CONFORME, 0.94)
    store.decide(ver_g2, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Versión 2 vigente")
    res_g = layer.ingest_canonical(ver_g2, structure={"texto": TXT_V2})
    check("v2 INGESTADO", res_g["accion"] == "INGESTADO")
    proc_g = store.chunks_of(ver_g2)[0]["metadata"]
    check("reemplaza_a registrado en la procedencia del chunk", proc_g.get("reemplaza_a") == ver_a)
    check("relación supersedes en el modelo", store._get_version(ver_g2)["supersedes_version_id"] == ver_a)

    # ── H. versión anterior → no recuperable como vigente ────────────────
    print("\n[H] Versión anterior → no recuperable como vigente")
    check("v1 en OBSOLETA", store._get_version(ver_a)["state"] == VersionState.OBSOLETA.value)
    check("v1 NO recuperable", ver_a not in store.retrievable_versions())
    check("v2 recuperable", ver_g2 in store.retrievable_versions())
    check("ingesta de v1 REVOCADO", all(
        i["state"] == IngestionState.REVOCADO.value
        for i in store._state["ingestions"].values() if i["version_id"] == ver_a))

    # ── I. pérdida o alteración de procedencia → bloqueo ─────────────────
    print("\n[I] Procedencia ausente o alterada → bloqueo")
    ver_i = cadena("Sin procedencia de adquisición", TXT + " variante I.", con_procedencia=False, decidir=False)
    check("sin procedencia la versión jamás alcanza estado decidible",
          store._get_version(ver_i)["state"] == VersionState.BORRADOR.value)
    v = check_adm = layer.check_admissibility(ver_i)
    check("sin Acquisition/Verification → BLOQUEO", (not v.admisible) and v.accion == "BLOQUEO", v.motivo[:80])
    expect_bloqueo("ingesta bloqueada por procedencia incompleta",
                   lambda: layer.ingest_canonical(ver_i, structure={"texto": "x"}))
    ver_i2 = cadena("Contenido alterado", TXT + " variante I2.")
    texto_alterado = TXT + " variante I2 ALTERADA después de la auditoría."
    res_i2 = layer.check_admissibility(ver_i2, content_text=texto_alterado, verify_content=True)
    check("hash alterado detectado → BLOQUEO", (not res_i2.admisible) and "alterada" in res_i2.motivo.lower(), res_i2.motivo[:80])
    expect_bloqueo("ingesta bloqueada por alteración",
                   lambda: layer.ingest_canonical(ver_i2, structure={"texto": texto_alterado}, content_text=texto_alterado, verify_content=True))

    # ── J. concurrencia/reintentos → idempotencia ────────────────────────
    print("\n[J] Concurrencia y reintentos → resultado idempotente")
    ver_j = cadena("Guía para concurrencia", TXT + " variante J.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        resultados = list(ex.map(
            lambda _: layer.ingest_canonical(ver_j, structure={"texto": TXT + " variante J."}),
            range(8)))
    ids = {r["ingestion_id"] for r in resultados}
    check("8/8 llamadas devuelven la MISMA ingesta", len(ids) == 1, str(ids))
    check("marca idempotente en reintentos", sum(1 for r in resultados if r.get("idempotente")) == 7)
    check("una sola ingesta INGESTADO en el modelo", sum(
        1 for i in store._state["ingestions"].values()
        if i["version_id"] == ver_j and i["state"] == IngestionState.INGESTADO.value) == 1)
    chunks_j_antes = len(store.chunks_of(ver_j))
    r_retry = layer.ingest_canonical(ver_j, structure={"texto": TXT + " variante J."})
    check("reintento tras éxito no duplica chunks", len(store.chunks_of(ver_j)) == chunks_j_antes)

    # ── K. contenido multimodal → preservación de estructura ─────────────
    print("\n[K] Multimodal → preservación de tablas, notas, referencias")
    estructura = {
        "secciones": [
            {"tipo": "parrafo", "texto": "Introducción con transparencia y supervisión humana. " * 40},
            {"tipo": "tabla", "titulo": "Tabla 1. Categorías de datos",
             "contenido": [["Categoría", "Artículo"], ["Salud", "Art. 9.1.a"], ["Biométricos", "Art. 9.1.b"]],
             "nota": "Los datos de salud requieren consentimiento explícito."},
            {"tipo": "nota", "texto": "Nota general del documento."},
            {"tipo": "referencia", "texto": "Reglamento (UE) 2016/679 (RGPD), Arts. 5, 6, 9.",
             "referencia": "https://eur-lex.europa.eu/eli/reg/2016/679/oj"},
            {"tipo": "figura", "descripcion": "Diagrama del pipeline de conocimiento",
             "referencia": "fig-1"},
        ]
    }
    ver_k = cadena("Documento multimodal", "contenido multimodal K")
    res_k = layer.ingest_canonical(ver_k, structure=estructura)
    check("ingesta multimodal correcta", res_k["accion"] == "INGESTADO")
    chunks_k = store.chunks_of(ver_k)
    tipos = [c["metadata"]["tipo"] for c in chunks_k]
    check("tipos preservados (parrafo/tabla/nota/referencia/figura)",
          {"tabla", "nota", "referencia", "figura"}.issubset(set(tipos)), str(tipos))
    tabla = next(c for c in chunks_k if c["metadata"]["tipo"] == "tabla")
    check("tabla ATÓMICA (una sola chunk con todas sus filas)",
          all(fila in tabla["text"] for fila in ("Salud", "Biométricos", "Art. 9.1.a")) and "Tabla 1" in tabla["text"])
    check("tabla marcada atomica=True", tabla["metadata"].get("atomica") is True)
    nota_tabla = next(c for c in chunks_k if c["metadata"]["tipo"] == "nota" and "Nota de tabla" in c["text"])
    check("nota de tabla enlazada a su tabla (relación semántica)",
          tabla["metadata"]["ordinal_global"] in nota_tabla["metadata"]["vinculos"])
    check("referencia preservada con URL",
          any("eur-lex" in c["text"] for c in chunks_k if c["metadata"]["tipo"] == "referencia"))
    check("sin pérdida de texto: todas las celdas presentes en los chunks",
          all(palabra in " ".join(c["text"] for c in chunks_k) for palabra in ("Introducción", "consentimiento explícito", "Diagrama")))
    ordinales = [c["metadata"]["ordinal_global"] for c in chunks_k]
    check("ordinales globales secuenciales", ordinales == list(range(1, len(ordinales) + 1)))

    # ── L. trazabilidad → reconstrucción completa del ciclo ──────────────
    print("\n[L] Trazabilidad: reconstrucción completa del ciclo")
    ver_legal_l = cadena("Normativa legal con auditoría Yata", "Texto jurídico L para auditoría.",
                         domain=Domain.JURIDICO_NORMATIVO)
    log = store.audit_log()
    doc_id_a = store._state["versions"][ver_a]["document_id"]
    src_id_a = store._state["documents"][doc_id_a]["source_id"]
    targets_a = {ver_a, doc_id_a, src_id_a}
    ciclo = [e for e in log if e["target_id"] in targets_a
             or e["payload"].get("version_id") == ver_a
             or (e["action"] == "ingest_canonical" and e["payload"].get("version_id") == ver_a)]
    acciones_ciclo = [e["action"] for e in ciclo]
    esperadas = ["register_source", "register_document", "register_version",
                 "register_acquisition", "register_verification", "human_decision", "ingest"]
    check("todas las etapas del ciclo presentes", all(a in acciones_ciclo for a in esperadas), str(acciones_ciclo))
    ts = [e["timestamp"] for e in ciclo]
    check("orden cronológico del ciclo", ts == sorted(ts))
    check("bloqueos también auditados", any(e["action"] == "ingest_blocked" for e in log))
    proc_l = store.chunks_of(ver_a)[0]["metadata"]
    check("reconstrucción desde el chunk hasta la fuente primaria",
          proc_l["source_id"] in store._state["sources"]
          and proc_l["document_id"] in store._state["documents"]
          and proc_l["version_id"] in store._state["versions"])
    check("ciclo verificable vía dictamen DIKE/Vár + auditor Yata cuando procede",
          any(vf.get("auditor") == "Yata" for vf in store._state["verifications"].values()),
          str([vf.get("auditor") for vf in store._state["verifications"].values() if vf.get("auditor")]))

    # ── M. intento directo desde Archivo Documental → bloqueo ────────────
    print("\n[M] Intento directo desde Archivo Documental → bloqueo")
    codd = CoddArchivist(base_storage_dir=str(TMP / "codd"))
    doc_archivo = codd.register_document("documento_solo_archivado.txt", TXT.encode(),
                                         area="ARCHIVO_DOCUMENTAL", author_node="Codd")
    expect_bloqueo("versión inexistente en el modelo canónico → BLOQUEO",
                   lambda: layer.ingest_canonical(doc_archivo["uuid"], structure={"texto": TXT}),
                   "no existe en el modelo canónico")
    expect_excepcion("ingest_from_archive SIEMPRE rechazado (regla crítica)",
                     lambda: layer.ingest_from_archive(documento=doc_archivo["uuid"]),
                     ArchiveNotAuthorizedError, "Archivo Documental no autoriza")
    check("intento auditado como archive_ingestion_refused",
          any(e["action"] == "archive_ingestion_refused" for e in store.audit_log()))
    check("el documento archivado NO es conocimiento canónico",
          doc_archivo["uuid"] not in store._state["versions"])

    # ── Cierre: escritura segura y estado global ─────────────────────────
    print("\n[CIERRE] Escritura segura y estado global")
    estado = json.loads((TMP / "kmodel_f2.json").read_text(encoding="utf-8"))
    check("store JSON válido tras todas las operaciones", len(estado["versions"]) >= 8)
    errores = store.validate_integrity()
    check("integridad de relaciones: 0 errores", len(errores) == 0, str(errores[:3]))
    print(f"  Stats: { {k: (len(v) if isinstance(v, (dict, list)) else v) for k, v in store.stats().items()} }")

    print("\n" + "=" * 64)
    if fallos:
        print(f"RESULTADO: FAIL — {fallos} fallo(s) de {pasos} comprobaciones")
        sys.exit(1)
    print(f"RESULTADO: OK — {pasos}/{pasos} comprobaciones superadas (FASE 2)")
    sys.exit(0)


if __name__ == "__main__":
    main()
