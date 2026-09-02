#!/usr/bin/env python3
"""Verificador de integridad WAIPL. Stdlib only.

El hash nunca vive dentro del archivo hasheado.
Uso:
  python3 verify_integrity.py           # CI / comprobación
  python3 verify_integrity.py --write   # regenerar MANIFEST.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]  # Will-AI-Project-Lab root
MANIFEST = HERE / "MANIFEST.json"

CANON_PATHS = [
    "03_PERSONAS_IA/AETHER/IDENTIDAD.md",
    "03_PERSONAS_IA/AETHER-HERMES/IDENTIDAD.md",
    "06_SISTEMA_OPERATIVO/03_NODOS_COMUNICACION.md",
    "06_SISTEMA_OPERATIVO/2026-08-23_WAIPL_GOBERNANZA_ADDENDA_DirectivaTransversal_v1.0_12PrincipioOperativo_CANONIZADO.md",
    "06_SISTEMA_OPERATIVO/HERMES/GLOSARIO.md",
    "06_SISTEMA_OPERATIVO/HERMES/IDENTIDAD.md",
    "06_SISTEMA_OPERATIVO/HERMES/N3-AUTOCLAW-RUNTIME.md",
    "06_SISTEMA_OPERATIVO/HERMES/SPEC-WAIPL-BUS-v0.1.md",
    "06_SISTEMA_OPERATIVO/HERMES/webhook_handler.py",
    "06_SISTEMA_OPERATIVO/INTEGRITY/SPEC-INTEGRITY-v1.0.md",
    "06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py",
    "graph.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_file(rel: str) -> Path:
    return REPO / rel


def build_manifest() -> dict:
    files = {}
    missing = []
    for rel in CANON_PATHS:
        p = repo_file(rel)
        if not p.is_file():
            missing.append(rel)
            continue
        files[rel] = {
            "sha256": sha256_file(p),
            "bytes": p.stat().st_size,
        }
    if missing:
        raise SystemExit("faltan archivos para el manifiesto:\n  " + "\n  ".join(missing))
    return {
        "spec": "SPEC-INTEGRITY-v1.0",
        "algorithm": "SHA-256",
        "canon": "git-blob-bytes",
        "note": "Este manifiesto no se hashea a sí mismo. El Action imprime su sha256 en el log.",
        "files": files,
    }


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        raise SystemExit(f"no existe {MANIFEST}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def check_graph(errors: list[str], warnings: list[str]) -> None:
    path = repo_file("graph.json")
    if not path.is_file():
        errors.append("graph.json ausente")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"graph.json no parsea: {exc}")
        return
    nested = data.get("graph", {}).get("hyperedges") or []
    root = data.get("hyperedges") or []
    source = nested if nested else root
    ids = [h.get("id") for h in source if isinstance(h, dict)]
    unique = list(dict.fromkeys(ids))
    if len(ids) != len(unique):
        errors.append(
            f"graph.json hiperaristas con id duplicado en la lista canónica: {ids}"
        )
    if nested and root:
        nested_ids = [h.get("id") for h in nested]
        root_ids = [h.get("id") for h in root]
        if nested_ids != root_ids:
            warnings.append(
                "graph.json tiene hyperedges en graph.hyperedges y en raíz, con IDs distintos; se usa graph.hyperedges"
            )
        else:
            warnings.append(
                f"graph.json duplica {len(unique)} hiperaristas en dos arrays; el recuento canónico es {len(unique)}, no {len(unique) * 2}"
            )
    nodes = data.get("nodes") or []
    links = data.get("links") or []
    print(
        f"graph.json  nodos={len(nodes)}  links={len(links)}  "
        f"hiperaristas_unicas={len(unique)}  ids={unique}"
    )
    if len(nodes) == 0:
        warnings.append(
            "graph.json en GitHub tiene nodes=[]. DES-001 no está cerrado en el canónico. "
            "No se restaura desde aquí."
        )
    if "vertigos_project_documentation" not in unique:
        warnings.append("falta hiperarista vertigos_project_documentation")


def check_addenda(errors: list[str]) -> None:
    rel = (
        "06_SISTEMA_OPERATIVO/"
        "2026-08-23_WAIPL_GOBERNANZA_ADDENDA_DirectivaTransversal_v1.0_12PrincipioOperativo_CANONIZADO.md"
    )
    p = repo_file(rel)
    if not p.is_file():
        errors.append(f"addenda ausente: {rel}")
        return
    text = p.read_text(encoding="utf-8")
    if "pendiente de generación por Z" in text:
        errors.append("addenda sigue con hash pendiente de Z; el hash vive en MANIFEST.json")
    if "9ade0a9e" in text:
        errors.append("addenda cita el hash no verificable 9ade0a9e")


def check_identity(errors: list[str]) -> None:
    aether = repo_file("03_PERSONAS_IA/AETHER/IDENTIDAD.md")
    hermes = repo_file("06_SISTEMA_OPERATIVO/HERMES/IDENTIDAD.md")
    tomb = repo_file("03_PERSONAS_IA/AETHER-HERMES/IDENTIDAD.md")
    if aether.is_file():
        t = aether.read_text(encoding="utf-8")
        if "Aether-Hermes" in t and "derog" not in t.lower() and "prohibido" not in t.lower():
            errors.append("AETHER/IDENTIDAD.md trata Aether-Hermes como identidad viva")
    else:
        errors.append("falta ficha Aether")
    if not hermes.is_file():
        errors.append("falta ficha Hermes")
    if tomb.is_file():
        t = tomb.read_text(encoding="utf-8")
        if "MOVED" not in t and "derog" not in t.lower() and "lápida" not in t.lower() and "lapida" not in t.lower():
            errors.append("AETHER-HERMES/IDENTIDAD.md no es lápida")
    else:
        errors.append("falta lápida AETHER-HERMES")


def verify() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    manifest = load_manifest()
    files = manifest.get("files") or {}
    if not files:
        errors.append("MANIFEST.json vacío")
    expected = set(CANON_PATHS)
    listed = set(files)
    if expected - listed:
        errors.append("MANIFEST.json no lista: " + ", ".join(sorted(expected - listed)))
    if listed - expected:
        warnings.append("MANIFEST.json lista paths extra: " + ", ".join(sorted(listed - expected)))
    for rel, meta in files.items():
        p = repo_file(rel)
        if not p.is_file():
            errors.append(f"ausente: {rel}")
            continue
        got = sha256_file(p)
        want = meta.get("sha256")
        size = meta.get("bytes")
        if got != want:
            errors.append(f"HASH MISMATCH {rel}\n  manifiesto {want}\n  disco      {got}")
        elif size is not None and p.stat().st_size != size:
            errors.append(f"tamaño mismatch {rel}: manifiesto {size} disco {p.stat().st_size}")
        else:
            print(f"OK  {got}  {rel}")
    print(f"MANIFEST.json sha256={sha256_file(MANIFEST)} bytes={MANIFEST.stat().st_size}")
    check_graph(errors, warnings)
    check_addenda(errors)
    check_identity(errors)
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        print("--- FALLÓ ---")
        for e in errors:
            print(f"ERR   {e}")
        return 1
    print("--- INTEGRIDAD OK ---")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="regenerar MANIFEST.json")
    args = parser.parse_args()
    if args.write:
        data = build_manifest()
        MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"escrito {MANIFEST}")
        for rel, meta in data["files"].items():
            print(f"  {meta['sha256']}  {rel}")
        return 0
    return verify()


if __name__ == "__main__":
    sys.exit(main())
