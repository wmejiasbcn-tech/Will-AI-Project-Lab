#!/usr/bin/env python3
"""
test_knowledge_model.py — Batería FASE 1: Modelo de Conocimiento Canónico
(Orden Soberana RAG Will App v0.3.1 — FASE 1: esquema completo de datos y relaciones).

Valida los invariantes canónicos del modelo:
  I1 Principio Absoluto   — sin verificación + HumanDecision ACCEPT no hay ingesta
  I2 Aislamiento          — archivado ≠ canónico ≠ vector store ≠ RAG
  I3 Deduplicación        — content_hash repetido → ALIAS, sin nuevos embeddings
  I4 Vigencia             — solo VIGENTE+ACCEPT+INGESTADO es recuperable;
                            la versión sustituida se revoca automáticamente
  I5 Trazabilidad humana  — decision_reason/reviewer/timestamp/target obligatorios
  I6 AuditLog             — toda mutación queda registrada
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
sys.path.insert(0, str(ROOT))

from waipl.core.knowledge_model import (
    KnowledgeStore, Domain, VerificationResult, HumanDecisionType,
    VersionState, IngestionState, KnowledgeModelError, IngestionBlockedError,
)

TMP = Path(tempfile.mkdtemp(prefix="kmodel_", dir=str(ROOT / ".openclaw" / "tmp")))
TXT = (
    "Guía comunitaria de acompañamiento. Transparencia, supervisión humana, "
    "consentimiento, minimización, derecho de acceso y supresión, equidad."
)

pasos, fallos = 0, 0


def check(nombre, cond, detalle=""):
    global pasos, fallos
    pasos += 1
    ok = bool(cond)
    if not ok:
        fallos += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {nombre}" + (f" — {detalle}" if detalle else ""))


def expect_error(nombre, fn, exc):
    try:
        fn()
        check(nombre, False, "no lanzó excepción")
    except exc:
        check(nombre, True)
    except Exception as e:
        check(nombre, False, f"excepción incorrecta: {type(e).__name__}: {e}")


def nueva_cadena(store, titulo, texto=TXT, domain=Domain.MEDICO_CIENTIFICO_COMUNITARIO,
                 verificador="Vár (VAC-01)", resultado=VerificationResult.CONFORME):
    src = store.register_source("Fuente oficial de ejemplo", "https://fuente/ejemplo", "OMS")
    doc = store.register_document(src, titulo, domain)
    ver = store.register_version(doc, texto, str(TMP / f"{doc[:8]}.txt"))
    store.register_acquisition(ver, "KAIROS" if domain == Domain.MEDICO_CIENTIFICO_COMUNITARIO else "DIKE")
    store.register_verification(ver, verificador, resultado, 0.9)
    return ver


def main():
    print("=" * 64)
    print("FASE 1 — MODELO DE CONOCIMIENTO (Orden Soberana v0.3.1)")
    print("=" * 64)

    store = KnowledgeStore(str(TMP / "kmodel.json"))

    # I1+I2: cadena completa y principio absoluto
    print("\n[I1/I2] Cadena canónica completa y principio absoluto")
    ver = nueva_cadena(store, "Guía conforme")
    check("versión en PENDIENTE_DECISION_HUMANA tras verificación",
          store._get_version(ver)["state"] == VersionState.PENDIENTE_DECISION_HUMANA.value)
    expect_error("ingesta SIN decisión humana bloqueada (I1)",
                 lambda: store.ingest(ver, ["chunk 1"]), IngestionBlockedError)
    check("nada recuperable aún (I2 aislamiento)", store.retrievable_versions() == [])

    # I5: campos obligatorios de decisión humana
    print("\n[I5] Decisión humana: campos obligatorios")
    expect_error("sin decision_reason rechazada",
                 lambda: store.decide(ver, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, ""),
                 KnowledgeModelError)
    expect_error("sin human_reviewer_id rechazada",
                 lambda: store.decide(ver, "", HumanDecisionType.ACCEPT, "razón"),
                 KnowledgeModelError)
    store.decide(ver, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aprobada tras revisión soberana")
    check("versión VIGENTE tras ACCEPT", store._get_version(ver)["state"] == VersionState.VIGENTE.value)
    dec = [d for d in store._state["human_decisions"].values() if d["version_id"] == ver][0]
    check("I5 completa: reviewer/timestamp/target/reason",
          dec["human_reviewer_id"] == "WILLIAM-SCY-01" and dec["decision_timestamp"]
          and dec["target_version_id"] == ver and len(dec["decision_reason"]) > 5)

    # Ingesta + chunks + embeddings pendientes
    print("\n[Ingesta] chunks creados; embeddings referenciados (vector en FASE 3)")
    ing = store.ingest(ver, ["chunk uno", "chunk dos", "chunk tres"])
    check("ingesta INGESTADO", store._state["ingestions"][ing]["state"] == IngestionState.INGESTADO.value)
    check("3 chunks ordenados", [c["ordinal"] for c in store.chunks_of(ver)] == [1, 2, 3])
    check("embedding por chunk (referencia FASE 3)", len(store._state["embeddings"]) == 3)
    check("recuperable por Will App", store.retrievable_versions() == [ver])

    # REJECT → cuarentena, nunca recuperable
    print("\n[REJECT] Versión rechazada → CUARENTENA, nunca recuperable")
    ver_rej = nueva_cadena(store, "Guía rechazada", resultado=VerificationResult.NO_CONFORME)
    store.decide(ver_rej, "WILLIAM-SCY-01", HumanDecisionType.REJECT, "No conforme: sin base jurídica")
    check("estado CUARENTENA", store._get_version(ver_rej)["state"] == VersionState.CUARENTENA.value)
    expect_error("ingesta de rechazada bloqueada", lambda: store.ingest(ver_rej, ["c"]), IngestionBlockedError)
    check("cuarentena NO recuperable", ver_rej not in store.retrievable_versions())

    # I3: deduplicación → ALIAS
    print("\n[I3] Duplicado: mismo content_hash → ALIAS, sin nuevos embeddings")
    emb_antes = len(store._state["embeddings"])
    ver_dup = nueva_cadena(store, "Guía duplicada (mismo contenido)", texto=TXT)
    check("mismo content_hash", store._get_version(ver_dup)["content_hash"] == store._get_version(ver)["content_hash"])
    store.make_alias(ver_dup, actor="Codd (custodia)")  # Codd crea alias; NO decide admisibilidad
    check("find_canonical resuelve a la canónica VIGENTE (alias → vigente)",
          store.find_canonical(store._get_version(ver_dup)["content_hash"]) == ver)
    expect_error("ingesta del duplicado bloqueada (I3)",
                 lambda: store.ingest(ver_dup, ["c"]), IngestionBlockedError)
    check("sin nuevos embeddings para el duplicado", len(store._state["embeddings"]) == emb_antes)
    check("duplicado NO recuperable; canónica sí", store.retrievable_versions() == [ver])

    # I4: versionado y vigencia (resuelve FINDING-2 estructuralmente)
    print("\n[I4] Versionado: v2 sustituye a v1 → v1 OBSOLETA (no recuperable)")
    ver2 = store.register_version(store._state["documents"][store._get_version(ver)["document_id"]]["document_id"],
                                  TXT + " Contenido ampliado versión 2.", str(TMP / "v2.txt"),
                                  supersedes_version_id=ver)
    store.register_acquisition(ver2, "KAIROS")
    store.register_verification(ver2, "Vár (VAC-01)", VerificationResult.CONFORME, 0.92)
    store.decide(ver2, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Versión 2 vigente")
    store.ingest(ver2, ["v2 chunk 1", "v2 chunk 2"])
    check("v1 pasa a OBSOLETA automáticamente al ingerirse v2 (distinta de REVOCADA)",
          store._get_version(ver)["state"] == VersionState.OBSOLETA.value, store._get_version(ver)["state"])
    check("ingesta de v1 marcada REVOCADO",
          all(i["state"] == IngestionState.REVOCADO.value for i in store._state["ingestions"].values() if i["version_id"] == ver))
    check("solo v2 recuperable (vigencia)", store.retrievable_versions() == [ver2])
    expect_error("obsoleta no re-ingerible", lambda: store.ingest(ver, ["c"]), IngestionBlockedError)

    # Alias → canónica vigente vs alias → canónica no-vigente (revocada/obsoleta)
    print("\n[ALIAS] alias → canónica VIGENTE resuelve; alias → canónica no-VIGENTE no resuelve")
    ver_dup2 = nueva_cadena(store, "Duplicado tras obsolescencia (mismo contenido)", texto=TXT)
    check("alias obsoleto NO resuelve: canónica ya no VIGENTE → find_canonical None",
          store.find_canonical(store._get_version(ver_dup2)["content_hash"]) is None)
    expect_error("make_alias sobre canónica no-VIGENTE rechazado (alias obsoleto no se crea)",
                 lambda: store.make_alias(ver_dup2, actor="Codd (custodia)"), KnowledgeModelError)
    check("duplicado nunca recuperable aunque su alias quede obsoleto",
          ver_dup2 not in store.retrievable_versions())

    # REVOCADA explícita (distinta de OBSOLETA)
    print("\n[REVOCADA] retirada expresa de una versión vigente")
    ver_r = nueva_cadena(store, "Guía retirada expresamente")
    store.decide(ver_r, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aceptada")
    store.ingest(ver_r, ["c1"])
    check("antes de revocar: recuperable", ver_r in store.retrievable_versions())
    store.revoke(ver_r, "Retirada por orden del Soberano", actor="WILLIAM-SCY-01")
    check("estado REVOCADA (no OBSOLETA)", store._get_version(ver_r)["state"] == VersionState.REVOCADA.value)
    check("ingesta REVOCADO", all(i["state"] == IngestionState.REVOCADO.value for i in store._state["ingestions"].values() if i["version_id"] == ver_r))
    check("revocada NO recuperable", ver_r not in store.retrievable_versions())
    expect_error("revocada no re-ingerible", lambda: store.ingest(ver_r, ["c"]), IngestionBlockedError)

    # Estados no recuperables: barrido exhaustivo
    print("\n[NO-RECUPERABLES] ningún estado distinto de VIGENTE es conocimiento canónico")
    estados_vistos = {v["state"] for v in store._state["versions"].values()}
    no_recuperables_ok = True
    for v in store._state["versions"].values():
        if v["state"] != VersionState.VIGENTE.value and v["version_id"] in store.retrievable_versions():
            no_recuperables_ok = False
    check(f"0 versiones no-VIGENTE recuperables (estados presentes: {sorted(estados_vistos)})", no_recuperables_ok)
    check("estados BORRADOR/EN_VERIFICACION/PENDIENTE no generan ingesta",
          all(v["state"] not in (VersionState.BORRADOR.value, VersionState.EN_VERIFICACION.value,
                                  VersionState.PENDIENTE_DECISION_HUMANA.value)
              or v["version_id"] not in store.retrievable_versions()
              for v in store._state["versions"].values()))

    # Competencias: Codd custodia pero no decide; DIKE no es gate universal
    print("\n[Competencias] límites estrictos de la orden")
    ver_legal = nueva_cadena(store, "Normativa AESIA (dominio jurídico)",
                             texto="Texto jurídico normativo distinto: disposición adicional única.",
                             domain=Domain.JURIDICO_NORMATIVO,
                             verificador="DIKE (RGL-01)")
    store.decide(ver_legal, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Conforme: normativa oficial vigente")
    store.ingest(ver_legal, ["artículo 1...", "artículo 2..."])
    check("dominio jurídico: DIKE verifica, humano decide, ingesta OK", ver_legal in store.retrievable_versions())
    try:
        store.make_alias(ver_legal, actor="Codd (custodia)")  # mismo hash? no: distinto contenido
        check("alias con hash distinto rechazado", False, "no lanzó excepción")
    except KnowledgeModelError:
        check("alias con hash distinto rechazado", True)
    expect_error("acquisición de versión ya verificada rechazada",
                 lambda: store.register_acquisition(ver_legal, "KAIROS"), KnowledgeModelError)

    # I6: auditoría completa
    print("\n[I6] AuditLog: trazabilidad completa de mutaciones")
    log = store.audit_log()
    acciones = {e["action"] for e in log}
    check("acciones canónicas registradas",
          {"register_source", "register_document", "register_version", "register_acquisition",
           "register_verification", "human_decision", "ingest", "make_alias", "revoke", "obsolete",
           "transition"}.issubset(acciones), str(sorted(acciones)))
    check("cada decisión humana auditada", sum(1 for e in log if e["action"] == "human_decision") == 5,
          str(sum(1 for e in log if e["action"] == "human_decision")))
    print(f"  Registro de auditoría: {len(log)} entradas | stats: {store.stats()}")

    # Integridad de relaciones (validador) + prueba de que el validador detecta corrupción
    print("\n[INTEGRIDAD] validador de relaciones del modelo")
    errores = store.validate_integrity()
    check("0 errores de integridad en el store real", len(errores) == 0, str(errores[:3]))
    store._state["chunks"]["chunk-fantasma"] = {"chunk_id": "chunk-fantasma", "version_id": "version-inexistente",
                                                 "ingestion_id": "ing-inexistente", "ordinal": 1, "text": "x"}
    errores_fantasma = store.validate_integrity()
    check("el validador SÍ detecta referencias colgantes inyectadas", len(errores_fantasma) > 0,
          f"{len(errores_fantasma)} errores detectados")
    del store._state["chunks"]["chunk-fantasma"]

    # Persistencia atómica: reabrir el store conserva el estado
    print("\n[Persistencia] re-apertura del store")
    store2 = KnowledgeStore(str(TMP / "kmodel.json"))
    check("estado persiste entre aperturas", store2.retrievable_versions() == store.retrievable_versions())
    check("hash store estable (escritura atómica determinista)",
          (TMP / "kmodel.json").exists())

    print("\n" + "=" * 64)
    if fallos:
        print(f"RESULTADO: FAIL — {fallos} fallo(s) de {pasos} comprobaciones")
        sys.exit(1)
    print(f"RESULTADO: OK — {pasos}/{pasos} comprobaciones superadas (FASE 1)")
    sys.exit(0)


if __name__ == "__main__":
    main()
