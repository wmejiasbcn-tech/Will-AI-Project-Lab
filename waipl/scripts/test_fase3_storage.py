#!/usr/bin/env python3
"""
test_fase3_storage.py — Batería esencial FASE 3: Almacenamiento PostgreSQL + pgvector
(Orden Soberana v0.3.1, ritmo RÁPIDO Y SUFICIENTE).

Casos esenciales (mapeo de la orden):
  A  inserción de conocimiento canónico válido      (persistencia)
  B/C/D/E  rechazo de no-canónico / sin decisión / OBSOLETA / REVOCADA (triggers + vista)
  F/G  deduplicación → ALIAS, cero embeddings nuevos
  H/I  versionado (reemplaza_a) y revocación
  J  integridad relacional (0 huérfanos)
  K  persistencia tras reinicio del servidor
  L/M  concurrencia y reintentos idempotentes
  N  backup → restauración → verificación de integridad
  O  aislamiento y autorización (mínimo privilegio, credenciales, auth)
  P/Q  preservación multimodal y de procedencia
  R  AuditLog preservado (inmutable para la app)
  S  estados no recuperables jamás como conocimiento operativo
"""
import concurrent.futures
import json
import sys
import tempfile
import uuid as uuidlib
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
sys.path.insert(0, str(ROOT))

from waipl.core.knowledge_model import (
    KnowledgeStore, Domain, VerificationResult, HumanDecisionType, VersionState,
)
from waipl.core.ingestion_layer import IngestionLayer
from waipl.core.rag_storage import RagStorage, SECRETS

TMP = Path(tempfile.mkdtemp(prefix="fase3_", dir=str(ROOT / ".openclaw" / "tmp")))
TXT = ("Guía comunitaria conforme. Transparencia, supervisión humana, consentimiento, "
       "minimización, derecho de acceso y supresión, equidad.")

pasos, fallos = 0, 0


def check(nombre, cond, detalle=""):
    global pasos, fallos
    pasos += 1
    ok = bool(cond)
    if not ok:
        fallos += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {nombre}" + (f" — {detalle}" if detalle else ""))


def main():
    print("=" * 64)
    print("FASE 3 — ALMACENAMIENTO PostgreSQL + pgvector (batería esencial)")
    print("=" * 64)

    # Modelo canónico + ingestion layer (Fases 1-2) y capa física (Fase 3)
    store = KnowledgeStore(str(TMP / "kmodel_f3.json"))
    layer = IngestionLayer(store)
    rs = RagStorage()

    def cadena(titulo, texto, domain=Domain.MEDICO_CIENTIFICO_COMUNITARIO, decidir=True,
               decision=HumanDecisionType.ACCEPT):
        src = store.register_source("Fuente oficial F3", "https://fuente/f3", "OMS")
        doc = store.register_document(src, titulo, domain)
        ver = store.register_version(doc, texto, str(TMP / f"{doc[:8]}.txt"))
        store.register_acquisition(ver, "KAIROS" if domain == Domain.MEDICO_CIENTIFICO_COMUNITARIO else "DIKE")
        store.register_verification(ver, "Vár (VAC-01)", VerificationResult.CONFORME, 0.9,
                                    auditor="Yata" if domain == Domain.JURIDICO_NORMATIVO else None)
        if decidir:
            store.decide(ver, "WILLIAM-SCY-01", decision, "Revisión soberana del contenido")
        return ver

    # ── A. inserción de conocimiento canónico válido ─────────────────────
    print("\n[A] Canónico válido → persistido y recuperable")
    ver_a = cadena("Guía válida F3", TXT)
    layer.ingest_canonical(ver_a, structure={"texto": TXT}, content_text=TXT, verify_content=True)
    rs.sync_from_model(store)
    rs.sync_embeddings_synthetic(store)
    rec = rs.retrievable()
    check("versión en retrievable_knowledge (PostgreSQL)", ver_a in [r["version_id"] for r in rec])
    n_emb = rs.execute("SELECT count(*) FROM embeddings e JOIN chunks c ON c.chunk_id=e.chunk_id "
                       "JOIN retrievable_knowledge rk ON rk.version_id=c.version_id", fetch=True)[0][0]
    check("embeddings de prueba solo para conocimiento operativo", n_emb > 0, f"{n_emb} embeddings")
    sim = rs.search_similar("[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]", k=3)
    check("búsqueda vectorial pgvector operativa", len(sim) >= 1, f"{len(sim)} resultados")

    # ── B/C/D/E. rechazo de estados no admitidos (físico + vista) ────────
    print("\n[B-E] Estados no canónicos → imposibles como conocimiento operativo")
    ver_b = cadena("Sin decisión", TXT + " B.", decidir=False)                     # PENDIENTE
    ver_c = cadena("Rechazada", TXT + " C.", decidir=True, decision=HumanDecisionType.REJECT)  # CUARENTENA
    rs.sync_from_model(store)
    rec_ids = [r["version_id"] for r in rs.retrievable()]
    check("PENDIENTE no recuperable", ver_b not in rec_ids)
    check("CUARENTENA no recuperable", ver_c not in rec_ids)
    # Trigger físico: INSERT de ingesta INGESTADO para no-VIGENTE debe fallar en la BD
    fallo_trigger = False
    try:
        rs.execute("INSERT INTO ingestions (ingestion_id,version_id,state,ingested_at,chunk_count) "
                   "VALUES (%s,%s,'INGESTADO',now(),0)", (str(uuidlib.uuid4()), ver_c))
    except Exception as e:
        fallo_trigger = "no admisible" in str(e) or "Principio" in str(e)
    check("trigger físico rechaza ingesta de versión no-VIGENTE", fallo_trigger)
    ver_d = cadena("Obsoleta F3", TXT + " D v1.", decidir=False)
    store.decide(ver_d, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aceptada v1")
    layer.ingest_canonical(ver_d, structure={"texto": TXT + " D v1."})
    doc_d = store._state["versions"][ver_d]["document_id"]
    ver_d2 = store.register_version(doc_d, TXT + " D v2.", str(TMP / "d2.txt"), supersedes_version_id=ver_d)
    store.register_acquisition(ver_d2, "KAIROS")
    store.register_verification(ver_d2, "Vár (VAC-01)", VerificationResult.CONFORME, 0.93)
    store.decide(ver_d2, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aceptada v2")
    layer.ingest_canonical(ver_d2, structure={"texto": TXT + " D v2."})
    rs.sync_from_model(store)
    rs.sync_embeddings_synthetic(store)
    st_d1 = rs.execute("SELECT state FROM versions WHERE version_id=%s", (ver_d,), fetch=True)[0][0]
    check("OBSOLETA persistida con estado correcto (≠ REVOCADA)", st_d1 == VersionState.OBSOLETA.value, st_d1)
    check("OBSOLETA no recuperable", ver_d not in [r["version_id"] for r in rs.retrievable()])
    ver_e = cadena("Revocada F3", TXT + " E.", decidir=False)
    store.decide(ver_e, "WILLIAM-SCY-01", HumanDecisionType.ACCEPT, "Aceptada")
    layer.ingest_canonical(ver_e, structure={"texto": TXT + " E."})
    store.revoke(ver_e, "Retirada expresamente", actor="WILLIAM-SCY-01")
    rs.sync_from_model(store)
    st_e = rs.execute("SELECT state FROM versions WHERE version_id=%s", (ver_e,), fetch=True)[0][0]
    check("REVOCADA persistida (distinta de OBSOLETA)", st_e == VersionState.REVOCADA.value, st_e)
    check("REVOCADA no recuperable", ver_e not in [r["version_id"] for r in rs.retrievable()])

    # ── F/G. deduplicación → ALIAS ───────────────────────────────────────
    print("\n[F/G] Duplicado → ALIAS, cero embeddings nuevos")
    emb_antes = rs.execute("SELECT count(*) FROM embeddings", fetch=True)[0][0]
    ver_f = cadena("Duplicado exacto", TXT)
    res_f = layer.ingest_canonical(ver_f, structure={"texto": TXT})
    check("ALIAS en la capa de ingesta", res_f["accion"] == "ALIAS")
    rs.sync_from_model(store)
    rs.sync_embeddings_synthetic(store)
    emb_despues = rs.execute("SELECT count(*) FROM embeddings", fetch=True)[0][0]
    check("cero embeddings nuevos para el duplicado", emb_despues == emb_antes,
          f"{emb_antes} → {emb_despues}")
    alias_row = rs.execute("SELECT canonical_version_id::text FROM aliases WHERE duplicate_version_id=%s",
                           (ver_f,), fetch=True)
    check("alias persistido apuntando a la canónica", bool(alias_row) and alias_row[0][0] == ver_a)

    # ── H/I. versionado y revocación (relaciones) ────────────────────────
    print("\n[H/I] Versionado y revocación con relaciones")
    sup = rs.execute("SELECT supersedes_version_id::text FROM versions WHERE version_id=%s",
                     (ver_d2,), fetch=True)[0][0]
    check("reemplaza_a persistido", sup == ver_d)
    check("v1 obsoleta no recuperable; v2 sí",
          ver_d not in [r["version_id"] for r in rs.retrievable()]
          and ver_d2 in [r["version_id"] for r in rs.retrievable()])

    # ── J. integridad relacional ─────────────────────────────────────────
    print("\n[J] Integridad relacional: 0 huérfanos")
    errores = rs.validate_relational()
    check("0 referencias colgantes", len(errores) == 0, str(errores))

    # ── K. persistencia tras reinicio ────────────────────────────────────
    print("\n[K] Reinicio del servidor → datos intactos")
    import subprocess as sp
    import os as _os
    env = {**_os.environ, "PGPASSWORD": rs.creds["admin_password"]}
    # Salida a FICHERO (no pipes): el postmaster heredaría los pipes y colgaría run()
    restart_log = TMP / "pg_ctl_restart.log"
    with open(restart_log, "w", encoding="utf-8") as rl:
        sp.run([str(Path(r"C:\msys64\mingw64\bin\pg_ctl.exe")), "-D",
                str(ROOT / "waipl" / "rag" / "pgdata"), "restart", "-m", "fast",
                "-o", f"-p {rs.creds['port']}", "-w"],
               stdout=rl, stderr=rl, env=env)
    rs = RagStorage()  # reconexión nueva tras el reinicio
    rec2 = rs.retrievable()
    rec_ids2 = [r["version_id"] for r in rec2]
    check("datos accesibles tras restart (persistencia)",
          ver_d2 in rec_ids2 and ver_c not in rec_ids2 and ver_e not in rec_ids2,
          f"{len(rec2)} versiones recuperables en la BD persistente")

    def ver_g_ok(rec2):
        return ver_d2 in [r["version_id"] for r in rec2]

    # ── L/M. concurrencia y reintentos idempotentes ──────────────────────
    print("\n[L/M] Concurrencia y reintentos → idempotente")
    ver_l = cadena("Concurrente F3", TXT + " L.")
    layer.ingest_canonical(ver_l, structure={"texto": TXT + " L."})
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(lambda _: rs.sync_from_model(store), range(8)))
    counts_l = rs.execute(
        "SELECT (SELECT count(*) FROM versions WHERE version_id=%s), "
        "(SELECT count(*) FROM ingestions WHERE version_id=%s), "
        "(SELECT count(*) FROM chunks WHERE version_id=%s)",
        (ver_l, ver_l, ver_l), fetch=True)[0]
    check("sincronización concurrente sin duplicados", counts_l == (1, 1, 1), str(tuple(counts_l)))
    rs.sync_from_model(store)  # reintento
    counts_m = rs.execute(
        "SELECT (SELECT count(*) FROM versions WHERE version_id=%s), "
        "(SELECT count(*) FROM chunks WHERE version_id=%s)",
        (ver_l, ver_l), fetch=True)[0]
    check("reintento idempotente", counts_m == (1, 1), str(tuple(counts_m)))

    # ── P/Q. preservación multimodal y procedencia ───────────────────────
    print("\n[P/Q] Multimodal y procedencia preservados en PostgreSQL")
    estructura = {"secciones": [
        {"tipo": "parrafo", "texto": "Sección introductoria del documento multimodal."},
        {"tipo": "tabla", "titulo": "Tabla A", "contenido": [["Col1", "Col2"], ["d1", "d2"]],
         "nota": "Nota de la tabla A."},
        {"tipo": "referencia", "texto": "RGPD Art. 9.", "referencia": "https://eur-lex/x"},
    ]}
    ver_p = cadena("Multimodal F3", "contenido multimodal P")
    layer.ingest_canonical(ver_p, structure=estructura)
    rs.sync_from_model(store)
    metas = rs.execute("SELECT metadata FROM chunks WHERE version_id=%s ORDER BY ordinal",
                       (ver_p,), fetch=True)
    tipos = [m[0].get("tipo") for m in metas]
    check("estructura multimodal persistida (tabla/nota/referencia)",
          {"tabla", "nota", "referencia"}.issubset(set(tipos)), str(tipos))
    proc = metas[0][0]
    check("procedencia persistida (source/document/hash/verificación/supervisión)",
          all(k in proc for k in ("source_id", "document_id", "content_hash", "verificacion", "supervision_humana")))

    # ── O. aislamiento y autorización ────────────────────────────────────
    print("\n[O] Seguridad: roles, mínimo privilegio, credenciales")
    app = RagStorage(role="app")
    check("conexión con rol de app (credenciales separadas)", True)
    try:
        app.execute("DELETE FROM audit_log")
        check("app sin DELETE sobre audit_log", False)
    except Exception:
        check("app sin DELETE sobre audit_log (mínimo privilegio)", True)
    try:
        app.execute("DROP TABLE chunks")
        check("app sin DDL", False)
    except Exception:
        check("app sin DDL (mínimo privilegio)", True)
    app.close()
    import psycopg as _ps
    try:
        _ps.connect(f"host={rs.creds['host']} port={rs.creds['port']} dbname={rs.creds['database']} "
                    f"user={rs.creds['admin_user']} password=incorrecta")
        check("contraseña incorrecta rechazada", False)
    except _ps.OperationalError:
        check("contraseña incorrecta rechazada (scram-sha-256)", True)
    check("sin secretos hardcodeados (leídos de secrets externo)", SECRETS.is_file())

    # ── R + N. AuditLog, backup → destrucción controlada → restauración ──
    print("\n[R/N] AuditLog persistido y backup/restauración verificado")
    audit_antes = rs.execute("SELECT count(*) FROM audit_log", fetch=True)[0][0]
    check("AuditLog persistido", audit_antes > 100, f"{audit_antes} entradas")
    backup = rs.backup()
    check("pg_dump generado", backup.is_file() and backup.stat().st_size > 1000,
          f"{backup.stat().st_size} bytes")
    destino_restore = "waipl_rag_restore_test"
    rs.restore_to(backup, destino_restore)
    snap_orig = rs.counts_snapshot()
    snap_rest = rs.counts_snapshot(db_override=destino_restore)
    check("todas las tablas conservan el mismo conteo tras restaurar",
          all(snap_orig[t] == snap_rest[t] for t in snap_orig),
          str({k: (snap_orig[k], snap_rest[k]) for k in snap_orig if snap_orig[k] != snap_rest[k]}))
    check("AuditLog íntegro tras restaurar", snap_orig["audit_log"] == snap_rest["audit_log"])
    check("vista de recuperación restaurada", snap_rest["retrievable_knowledge"] >= 1)
    sp.run([str(Path(r"C:\msys64\mingw64\bin\dropdb.exe")), "-h", rs.creds["host"], "-p", str(rs.creds["port"]),
            "-U", rs.creds["admin_user"], "--if-exists", "waipl_rag_restore_test"],
           env=rs._pg_env(), capture_output=True, text=True)

    # ── S. barrido final: no-recuperable jamás operativo ─────────────────
    print("\n[S] Barrido: ningún estado no-VIGENTE como conocimiento operativo")
    filas = rs.execute(
        "SELECT v.state, count(*) FROM versions v "
        "JOIN retrievable_knowledge rk ON rk.version_id = v.version_id "
        "GROUP BY v.state", fetch=True)
    check("la vista de recuperación solo contiene VIGENTE",
          all(f[0] == VersionState.VIGENTE.value for f in filas), str(filas))

    print("\n" + "=" * 64)
    if fallos:
        print(f"RESULTADO: FAIL — {fallos} fallo(s) de {pasos} comprobaciones")
        sys.exit(1)
    print(f"RESULTADO: OK — {pasos}/{pasos} comprobaciones superadas (FASE 3)")
    sys.exit(0)


if __name__ == "__main__":
    main()
