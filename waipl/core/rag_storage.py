"""
Will App RAG — Capa de almacenamiento físico PostgreSQL + pgvector (FASE 3).

Espeja el estado del modelo canónico (knowledge_model.py, FASE 1) en
PostgreSQL 18 + pgvector 0.8.6 conforme a la Orden Soberana v0.3.1:

  - Separación estricta: Archivo documental ≠ canónico ≠ Vector Store ≠ Retriever ≠ Will App.
  - Regla de seguridad fundamental: los estados BORRADOR / EN_VERIFICACION /
    PENDIENTE_DECISION_HUMANA / CUARENTENA / OBSOLETA / REVOCADA jamás aparecen
    como conocimiento operativo (vista retrievable_knowledge + triggers).
  - Deduplicación: content_hash → canónica → ALIAS; duplicados sin embeddings.
  - Embeddings: SOLO infraestructura pgvector con vectores SINTÉTICOS de prueba
    (model='SYNTHETIC_TEST_FASE3'), claramente identificados; el modelo de
    embeddings productivo NO se selecciona en esta fase.
  - AuditLog persistido (inmutable para la app: solo SELECT).
  - Backup/restore con pg_dump/pg_restore + verificación de integridad.
  - Credenciales por secrets externos (waipl/rag/secrets/) — nada hardcodeado.

Solo stdlib + psycopg3. Los binarios de PostgreSQL provienen de MSYS2
(mingw-w64), instalados bajo C:\\msys64\\mingw64\\bin.
"""

import json
import os
import subprocess
import threading
import uuid as uuidlib
from pathlib import Path
from typing import Any, Dict, List, Optional

import psycopg
from psycopg.types.json import Jsonb

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
SECRETS = ROOT / "waipl" / "rag" / "secrets" / "pg_secrets.json"
PG_BIN = Path(r"C:\msys64\mingw64\bin")
BACKUP_DIR = ROOT / "waipl" / "rag" / "backups"
SYNTHETIC_DIM = 8


def _creds(path: Optional[str] = None) -> Dict[str, Any]:
    p = Path(path) if path else SECRETS
    return json.loads(p.read_text(encoding="utf-8"))


class RagStorage:
    """Espejo físico en PostgreSQL + pgvector del modelo canónico."""

    _LOCK = threading.RLock()

    def __init__(self, secrets_path: Optional[str] = None, role: str = "admin"):
        c = _creds(secrets_path)
        user = c["admin_user"] if role == "admin" else c["app_user"]
        pwd = c["admin_password"] if role == "admin" else c["app_password"]
        self.role = role
        self.creds = c
        self.conninfo = (f"host={c['host']} port={c['port']} dbname={c['database']} "
                         f"user={user} password={pwd}")
        self.conn = psycopg.connect(self.conninfo)

    # ─── Utilidades ───────────────────────────────────────────────────────

    def execute(self, sql: str, params: tuple = (), fetch: bool = False):
        with self.conn.cursor() as cur:
            try:
                cur.execute(sql, params)
                rows = cur.fetchall() if fetch else None
            except Exception:
                self.conn.rollback()  # libera el estado 'aborted' tras un rechazo de trigger
                raise
        self.conn.commit()
        return rows

    def close(self):
        self.conn.close()

    # ─── Sincronización desde el modelo canónico (idempotente) ────────────

    def sync_from_model(self, store, actor: str = "IngestionLayer") -> Dict[str, int]:
        """Espeja el KnowledgeStore (FASE 1) en las tablas físicas.
        Idempotente: upserts ON CONFLICT. Contadores = filas procesadas."""
        with RagStorage._LOCK:
            s = store._state
            counts = {"sources": 0, "documents": 0, "versions": 0, "acquisitions": 0,
                      "verifications": 0, "human_decisions": 0, "ingestions": 0,
                      "chunks": 0, "aliases": 0, "audit_log": 0}
            with self.conn.cursor() as cur:
                for x in s["sources"].values():
                    cur.execute(
                        "INSERT INTO sources (source_id,nombre,url,tipo,created_at) VALUES (%s,%s,%s,%s,%s) "
                        "ON CONFLICT (source_id) DO UPDATE SET nombre=EXCLUDED.nombre,url=EXCLUDED.url,tipo=EXCLUDED.tipo",
                        (x["source_id"], x["nombre"], x["url"], x["tipo"], x["created_at"]))
                    counts["sources"] += 1
                for x in s["documents"].values():
                    cur.execute(
                        "INSERT INTO documents (document_id,source_id,title,domain,created_at) VALUES (%s,%s,%s,%s,%s) "
                        "ON CONFLICT (document_id) DO UPDATE SET title=EXCLUDED.title,domain=EXCLUDED.domain",
                        (x["document_id"], x["source_id"], x["title"], x["domain"], x["created_at"]))
                    counts["documents"] += 1
                for x in s["versions"].values():
                    cur.execute(
                        "INSERT INTO versions (version_id,document_id,version_number,content_hash,stored_path,"
                        "state,supersedes_version_id,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON CONFLICT (version_id) DO UPDATE SET state=EXCLUDED.state,updated_at=EXCLUDED.updated_at,"
                        "supersedes_version_id=EXCLUDED.supersedes_version_id",
                        (x["version_id"], x["document_id"], x["version_number"], x["content_hash"],
                         x["stored_path"], x["state"], x.get("supersedes_version_id"),
                         x["created_at"], x["updated_at"]))
                    counts["versions"] += 1
                for x in s["acquisitions"].values():
                    cur.execute(
                        "INSERT INTO acquisitions (acquisition_id,version_id,agent,acquired_at,metadata) "
                        "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (acquisition_id) DO NOTHING",
                        (x["acquisition_id"], x["version_id"], x["agent"], x["acquired_at"],
                         Jsonb(x.get("metadata", {}))))
                    counts["acquisitions"] += 1
                for x in s["verifications"].values():
                    cur.execute(
                        "INSERT INTO verifications (verification_id,version_id,domain,verifier,result,confidence,"
                        "dictamen_id,auditor,verified_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON CONFLICT (verification_id) DO NOTHING",
                        (x["verification_id"], x["version_id"], x["domain"], x["verifier"], x["result"],
                         x["confidence"], x.get("dictamen_id"), x.get("auditor"), x["verified_at"]))
                    counts["verifications"] += 1
                for x in s["human_decisions"].values():
                    cur.execute(
                        "INSERT INTO human_decisions (decision_id,version_id,target_version_id,human_reviewer_id,"
                        "decision,decision_timestamp,decision_reason) VALUES (%s,%s,%s,%s,%s,%s,%s) "
                        "ON CONFLICT (decision_id) DO NOTHING",
                        (x["decision_id"], x["version_id"], x["target_version_id"], x["human_reviewer_id"],
                         x["decision"], x["decision_timestamp"], x["decision_reason"]))
                    counts["human_decisions"] += 1
                for x in s["ingestions"].values():
                    cur.execute(
                        "INSERT INTO ingestions (ingestion_id,version_id,state,ingested_at,chunk_count) "
                        "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (ingestion_id) DO UPDATE SET state=EXCLUDED.state",
                        (x["ingestion_id"], x["version_id"], x["state"], x.get("ingested_at"),
                         x.get("chunk_count", 0)))
                    counts["ingestions"] += 1
                for x in s["chunks"].values():
                    cur.execute(
                        "INSERT INTO chunks (chunk_id,version_id,ingestion_id,ordinal,text,metadata) "
                        "VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (chunk_id) DO NOTHING",
                        (x["chunk_id"], x["version_id"], x["ingestion_id"], x["ordinal"], x["text"],
                         Jsonb(x.get("metadata", {}))))
                    counts["chunks"] += 1
                for x in s["aliases"].values():
                    cur.execute(
                        "INSERT INTO aliases (alias_id,content_hash,canonical_version_id,duplicate_version_id,created_at) "
                        "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (alias_id) DO NOTHING",
                        (x["alias_id"], x["content_hash"], x["canonical_version_id"],
                         x["duplicate_version_id"], x["created_at"]))
                    counts["aliases"] += 1
                for x in s["audit_log"]:
                    cur.execute(
                        "INSERT INTO audit_log (audit_id,timestamp,actor,action,target_type,target_id,payload) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (audit_id) DO NOTHING",
                        (x["audit_id"], x["timestamp"], x["actor"], x["action"], x["target_type"],
                         x["target_id"], Jsonb(x.get("payload", {}))))
                    counts["audit_log"] += 1
            self.conn.commit()
            return counts

    def sync_embeddings_synthetic(self, store, actor: str = "IngestionLayer") -> int:
        """Infraestructura pgvector con vectores SINTÉTICOS DE PRUEBA
        (identificados como SYNTHETIC_TEST_FASE3). Solo chunks de versiones
        recuperables (VIGENTE+ACCEPT+INGESTADO, sin alias). Idempotente."""
        with RagStorage._LOCK:
            recuperables = set(store.retrievable_versions())
            n = 0
            with self.conn.cursor() as cur:
                for c in store._state["chunks"].values():
                    if c["version_id"] not in recuperables:
                        continue  # I3+I1: ningún embedding para no-recuperables
                    vec = "[" + ",".join(
                        str((int(c["chunk_id"][i % 32], 16) % 10) / 10) for i in range(SYNTHETIC_DIM)
                    ) + "]"
                    cur.execute(
                        "INSERT INTO embeddings (embedding_id,chunk_id,model,dimensions,vector) "
                        "VALUES (%s,%s,'SYNTHETIC_TEST_FASE3',%s,%s::vector) "
                        "ON CONFLICT (chunk_id) DO NOTHING",
                        (str(uuidlib.uuid4()), c["chunk_id"], SYNTHETIC_DIM, vec))
                    n += cur.rowcount
            self.conn.commit()
            return n

    # ─── Consultas de conocimiento operativo ─────────────────────────────

    def retrievable(self) -> List[Dict[str, Any]]:
        rows = self.execute(
            "SELECT version_id::text, document_id::text, domain, title, version_number, content_hash "
            "FROM retrievable_knowledge ORDER BY title", fetch=True)
        return [dict(zip(["version_id", "document_id", "domain", "title",
                          "version_number", "content_hash"], r)) for r in rows]

    def search_similar(self, query_vector: str, k: int = 5) -> List[Dict[str, Any]]:
        """Búsqueda vectorial RESTRICTA a conocimiento operativo recuperable.
        query_vector: literal pgvector, p. ej. '[0.1,0.2,...]'."""
        rows = self.execute(
            "SELECT c.chunk_id, c.version_id, c.text, e.vector <=> %s::vector AS distance "
            "FROM embeddings e JOIN chunks c ON c.chunk_id = e.chunk_id "
            "JOIN retrievable_knowledge rk ON rk.version_id = c.version_id "
            "WHERE e.model = 'SYNTHETIC_TEST_FASE3' "
            "ORDER BY e.vector <=> %s::vector LIMIT %s",
            (query_vector, query_vector, k), fetch=True)
        return [dict(zip(["chunk_id", "version_id", "text", "distance"], r)) for r in rows]

    def validate_relational(self) -> List[str]:
        """Integridad relacional en el almacén físico: 0 huérfanos esperado."""
        checks = [
            ("documents", "source_id", "sources", "source_id"),
            ("versions", "document_id", "documents", "document_id"),
            ("acquisitions", "version_id", "versions", "version_id"),
            ("verifications", "version_id", "versions", "version_id"),
            ("human_decisions", "version_id", "versions", "version_id"),
            ("ingestions", "version_id", "versions", "version_id"),
            ("chunks", "version_id", "versions", "version_id"),
            ("chunks", "ingestion_id", "ingestions", "ingestion_id"),
            ("embeddings", "chunk_id", "chunks", "chunk_id"),
        ]
        errores = []
        for tabla, col, ref_tabla, ref_col in checks:
            rows = self.execute(
                f"SELECT count(*) FROM {tabla} t LEFT JOIN {ref_tabla} r ON t.{col} = r.{ref_col} "
                f"WHERE t.{col} IS NOT NULL AND r.{ref_col} IS NULL", fetch=True)
            if rows[0][0] > 0:
                errores.append(f"{tabla}.{col}: {rows[0][0]} huérfanos hacia {ref_tabla}")
        return errores

    # ─── Backup / restauración (punto 8 de la orden) ─────────────────────

    def _pg_env(self) -> Dict[str, str]:
        env = dict(os.environ)
        env["PGPASSWORD"] = self.creds["admin_password"]
        return env

    def backup(self, destino: Optional[str] = None) -> Path:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        destino = Path(destino) if destino else BACKUP_DIR / "waipl_rag_backup.dump"
        r = subprocess.run(
            [str(PG_BIN / "pg_dump.exe"), "-h", self.creds["host"], "-p", str(self.creds["port"]),
             "-U", self.creds["admin_user"], "-Fc", "-f", str(destino), self.creds["database"]],
            env=self._pg_env(), capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"pg_dump falló: {r.stderr[-500:]}")
        return destino

    def restore_to(self, backup: Path, target_db: str) -> None:
        r = subprocess.run(
            [str(PG_BIN / "psql.exe"), "-h", self.creds["host"], "-p", str(self.creds["port"]),
             "-U", self.creds["admin_user"], "-d", "postgres", "-tAc",
             f"SELECT 1 FROM pg_database WHERE datname='{target_db}'"],
            env=self._pg_env(), capture_output=True, text=True)
        if r.stdout.strip() != "1":
            subprocess.run([str(PG_BIN / "createdb.exe"), "-h", self.creds["host"],
                            "-p", str(self.creds["port"]), "-U", self.creds["admin_user"], target_db],
                           env=self._pg_env(), capture_output=True, text=True)
        r = subprocess.run(
            [str(PG_BIN / "pg_restore.exe"), "-h", self.creds["host"], "-p", str(self.creds["port"]),
             "-U", self.creds["admin_user"], "-d", target_db, "--no-owner", str(backup)],
            env=self._pg_env(), capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"pg_restore falló: {r.stderr[-500:]}")

    def counts_snapshot(self, db_override: Optional[str] = None) -> Dict[str, int]:
        c = dict(self.creds)
        if db_override:
            c["database"] = db_override
        conn = psycopg.connect(f"host={c['host']} port={c['port']} dbname={c['database']} "
                               f"user={c['admin_user']} password={c['admin_password']}")
        out = {}
        with conn.cursor() as cur:
            for t in ["sources", "documents", "versions", "acquisitions", "verifications",
                      "human_decisions", "ingestions", "chunks", "embeddings", "aliases", "audit_log"]:
                cur.execute(f"SELECT count(*) FROM {t}")
                out[t] = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM retrievable_knowledge")
            out["retrievable_knowledge"] = cur.fetchone()[0]
        conn.close()
        return out
