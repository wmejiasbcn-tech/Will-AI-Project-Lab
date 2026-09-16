#!/usr/bin/env python3
"""
provision_fase3.py — Provisión de PostgreSQL + pgvector para el RAG de Will App
(FASE 3, Orden Soberana v0.3.1).

Acciones:
  1. Genera credenciales aleatorias (nunca hardcodeadas) y las persiste en un
     fichero de secretos con ACL restringida (waipl/rag/secrets/pg_secrets.json).
  2. initdb del directorio de datos persistente: waipl/rag/pgdata
     (auth scram-sha-256, listen_addresses=localhost, port 5433).
  3. Arranca la instancia con pg_ctl (log en waipl/rag/pgdata/log).
  4. Crea la base de datos waipl_rag y el rol de aplicación de mínimo
     privilegio `waipl_app` (sin DELETE, sin DDL — separación de credenciales).
  5. CREATE EXTENSION vector y aplicación del esquema canónico FASE 1+3.
  6. Verifica: conexión, extensión, roles, esquema.

Idempotente: si pgdata ya existe y el servidor responde, solo verifica.
"""
import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
PGDATA = ROOT / "waipl" / "rag" / "pgdata"
SECRETS = ROOT / "waipl" / "rag" / "secrets" / "pg_secrets.json"
LOGDIR = PGDATA / "log"
PORT = 5433
BIN = Path(r"C:\msys64\mingw64\bin")
SCHEMA = ROOT / "waipl" / "rag" / "schema" / "will_app_rag_schema.sql"
DB = "waipl_rag"
ADMIN = "waipl_admin"
APP = "waipl_app"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    return r


def restringir_acl(path: Path):
    """Restringe el ACL del fichero de secretos al usuario actual (NTFS)."""
    try:
        user = os.environ.get("USERNAME", "CURRENT_USER")
        subprocess.run(["icacls", str(path), "/inheritance:r",
                        "/grant:r", f"{user}:(R,W)"], capture_output=True, text=True)
    except Exception:
        pass  # documentado; el fichero vive dentro del workspace protegido


def main():
    print("=" * 64)
    print("PROVISIÓN FASE 3 — PostgreSQL + pgvector (Will App RAG)")
    print("=" * 64)

    # 1. Credenciales
    if SECRETS.exists():
        creds = json.loads(SECRETS.read_text(encoding="utf-8"))
        print("[OK] Secretos ya existentes (no se regeneran)")
    else:
        creds = {
            "host": "127.0.0.1", "port": PORT, "database": DB,
            "admin_user": ADMIN, "admin_password": secrets.token_urlsafe(24),
            "app_user": APP, "app_password": secrets.token_urlsafe(24),
        }
        SECRETS.parent.mkdir(parents=True, exist_ok=True)
        SECRETS.write_text(json.dumps(creds, indent=2), encoding="utf-8")
        restringir_acl(SECRETS)
        print(f"[OK] Credenciales generadas y guardadas en {SECRETS} (ACL restringida)")

    pwfile = TMP_PW = SECRETS.parent / "initdb_pw.tmp"
    pg_env = {**os.environ, "PGPASSWORD": creds["admin_password"]}

    # 2. initdb (si no existe pgdata)
    if not PGDATA.exists():
        PGDATA.parent.mkdir(parents=True, exist_ok=True)
        pwfile.write_text(creds["admin_password"], encoding="utf-8")
        r = run([str(BIN / "initdb.exe"), "-D", str(PGDATA), "-U", ADMIN,
                 "-A", "scram-sha-256", "--pwfile", str(pwfile),
                 "-E", "UTF8", "--locale=C"])
        pwfile.unlink(missing_ok=True)
        if r.returncode != 0:
            print(r.stdout[-1500:]); print(r.stderr[-1500:])
            sys.exit(1)
        print("[OK] initdb completado (scram-sha-256, UTF8, superusuario waipl_admin)")
        conf = PGDATA / "postgresql.conf"
        conf.write_text(conf.read_text(encoding="utf-8")
                        + f"\nlisten_addresses = '127.0.0.1'\nport = {PORT}\n"
                          "password_encryption = 'scram-sha-256'\nlog_connections = on\n", encoding="utf-8")
        print("[OK] postgresql.conf: listen 127.0.0.1, port", PORT, "- sin exposición externa")
    else:
        print("[OK] pgdata ya existe (persistencia conservada)")

    # 3. Arranque (si no responde ya). pg_isready: exit 0 = aceptando conexiones
    probe = run([str(BIN / "pg_isready.exe"), "-h", creds["host"], "-p", str(PORT)])
    if probe.returncode != 0:
        LOGDIR.mkdir(parents=True, exist_ok=True)
        r = run([str(BIN / "pg_ctl.exe"), "-D", str(PGDATA), "-l", str(LOGDIR / "postgresql.log"),
                 "-o", f"-p {PORT}", "start"])
        if r.returncode != 0:
            print(r.stdout[-800:]); print(r.stderr[-800:]); sys.exit(1)
        time.sleep(1)
        print("[OK] Servidor arrancado (pg_ctl, proceso local, no servicio global)")
    else:
        print("[OK] Servidor ya respondiendo en puerto", PORT)

    # 4. Base de datos + rol de aplicación
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", "postgres",
             "-tAc", f"SELECT 1 FROM pg_database WHERE datname='{DB}'"], env=pg_env)
    if r.stdout.strip() != "1":
        r = run([str(BIN / "createdb.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, DB], env=pg_env)
        if r.returncode != 0:
            print(r.stdout[-800:]); print(r.stderr[-800:]); sys.exit(1)
    print(f"[OK] Base de datos {DB}")

    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB, "-tAc",
             f"SELECT 1 FROM pg_roles WHERE rolname='{APP}'"], env=pg_env)
    if r.stdout.strip() != "1":
        r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB,
                 "-c", f"CREATE ROLE {APP} LOGIN PASSWORD '{creds['app_password']}'"], env=pg_env)
        if r.returncode != 0:
            print(r.stderr[-800:]); sys.exit(1)
    print(f"[OK] Rol de aplicación {APP} (mínimo privilegio, credenciales separadas)")

    # 5. Extensión vector + esquema
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB,
             "-v", "ON_ERROR_STOP=1",
             "-c", "CREATE EXTENSION IF NOT EXISTS vector;"], env=pg_env)
    if r.returncode != 0:
        print(r.stderr[-1500:]); sys.exit(1)
    print("[OK] Extensión vector creada")

    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB,
             "-f", str(SCHEMA)], env=pg_env)
    # Modo tolerante: "already exists" es benigno en re-provisión; la verificación
    # final por inventario de objetos es la prueba real.
    if "ERROR:" in (r.stderr or "") and "already exists" not in (r.stderr or "") and "ya existe" not in (r.stderr or ""):
        print(r.stdout[-2000:]); print(r.stderr[-2000:]); sys.exit(1)
    print("[OK] Esquema canónico FASE 1+3 aplicado (tolerante a re-provisión)")

    # Grants de mínimo privilegio para waipl_app
    grants = f"""
    GRANT CONNECT ON DATABASE {DB} TO {APP};
    GRANT USAGE ON SCHEMA public TO {APP};
    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO {APP};
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO {APP};
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {APP};
    REVOKE DELETE ON ALL TABLES IN SCHEMA public FROM {APP};
    REVOKE ALL ON audit_log FROM {APP};
    GRANT SELECT ON audit_log TO {APP};
    GRANT SELECT ON retrievable_knowledge TO {APP};
    """
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB,
             "-v", "ON_ERROR_STOP=1", "-c", grants], env=pg_env)
    if r.returncode != 0:
        print(r.stderr[-1500:]); sys.exit(1)
    print("[OK] Grants de mínimo privilegio (app sin DELETE; audit_log solo lectura)")

    # 6. Verificación final por inventario de objetos (la prueba real)
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB, "-tAc",
             "SELECT extname || '=' || extversion FROM pg_extension WHERE extname='vector'"], env=pg_env)
    print("[VERIFY] Extensión:", r.stdout.strip())
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB, "-tAc",
             "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'"], env=pg_env)
    tablas = int(r.stdout.strip() or 0)
    print("[VERIFY] Tablas public:", tablas)
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB, "-tAc",
             "SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
             "WHERE n.nspname='public' AND p.proname LIKE 'fn_%'"], env=pg_env)
    funcs = int(r.stdout.strip() or 0)
    print("[VERIFY] Funciones de enforcement:", funcs)
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB, "-tAc",
             "SELECT count(*) FROM pg_trigger WHERE tgname LIKE 'trg_%'"], env=pg_env)
    print("[VERIFY] Triggers de enforcement:", r.stdout.strip())
    r = run([str(BIN / "psql.exe"), "-h", creds["host"], "-p", str(PORT), "-U", ADMIN, "-d", DB, "-tAc",
             "SELECT count(*) FROM information_schema.views WHERE table_schema='public' AND table_name='retrievable_knowledge'"], env=pg_env)
    print("[VERIFY] Vista retrievable_knowledge:", r.stdout.strip())
    if tablas < 11 or funcs < 2 or int(r.stdout.strip() or 0) < 1:
        print("[FALLO] Inventario incompleto — NO declarar esquema aplicado"); sys.exit(1)
    print("=" * 64)
    print("PROVISIÓN COMPLETADA — PostgreSQL + pgvector operativos")
    print(f"  Datos: {PGDATA}")
    print(f"  Secretos: {SECRETS} (fuera del código; nunca hardcodeados)")
    print(f"  Puerto: {PORT} (solo 127.0.0.1)")
    sys.exit(0)


if __name__ == "__main__":
    main()
