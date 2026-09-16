#!/usr/bin/env python3
"""
test_idempotencia_graphify.py — Evidencia de idempotencia de inject_triad_graph_v2.py
(Orden Soberana, cierre DIKE punto 1).

Secuencia:
  1. Verificación integral del grafo  -> hash H1 + huella estructural F1
  2. Ejecución de inject_triad_graph_v2.py (1ª vez)
  3. Verificación integral            -> H2 + F2
  4. Ejecución de inject_triad_graph_v2.py (2ª vez, mismo script, mismo grafo)
  5. Verificación integral            -> H3 + F3

Criterio de PASS:
  - Las 3 verificaciones con 0 errores
  - H1 == H2 == H3 (byte-idéntico: sin duplicados ni modificaciones espurias)
  - F1 == F2 == F3 (huella estructural invariante)
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
VERIFY = ROOT / "waipl" / "scripts" / "verify_graphify_full.py"
INJECT = ROOT / "waipl" / "scripts" / "inject_triad_graph_v2.py"
GRAPH = ROOT / "waipl" / "graphify" / "graph.json"


def run_verify() -> dict:
    r = subprocess.run(
        [sys.executable, "-X", "utf8", str(VERIFY)],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
    )
    if r.returncode != 0:
        print(f"[FAIL] Verificación del grafo exit code {r.returncode}")
        print(r.stdout[-2000:])
        print(r.stderr[-2000:])
        sys.exit(1)
    return json.loads(r.stdout)


def run_inject(etiqueta: str) -> None:
    r = subprocess.run(
        [sys.executable, "-X", "utf8", str(INJECT), "--graph", str(GRAPH)],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
    )
    inyectadas = "Aristas inyectadas: 0" in r.stdout
    hiper = "Hiperaristas inyectadas: 0" in r.stdout
    print(f"[INJECT {etiqueta}] exit={r.returncode} | aristas nuevas: {'0 (todo SKIP)' if inyectadas else '>0'} | hiperaristas nuevas: {'0 (todo SKIP)' if hiper else '>0'}")
    if r.returncode != 0:
        print(r.stdout[-1500:])
        print(r.stderr[-1500:])
        sys.exit(1)


def main():
    print("=" * 64)
    print("PRUEBA DE IDEMPOTENCIA — inject_triad_graph_v2.py")
    print("=" * 64)

    fallos = 0
    hashes, fps = [], []

    for i in range(1, 4):
        v = run_verify()
        hashes.append(v["file_sha256"])
        fps.append(v["structural_fingerprint_sha256"])
        print(
            f"[VERIFY #{i}] nodos={v['counts']['nodes']} aristas={v['counts']['links']} "
            f"hiperaristas={v['counts']['hyperedges']} | checks={v['total_checks']} "
            f"fallos={v['fallos']} | file_sha256={v['file_sha256'][:16]}... | fp={v['structural_fingerprint_sha256'][:16]}..."
        )
        if v["fallos"]:
            fallos += v["fallos"]
            for e in v["errores"]:
                print(f"  [ERROR] {e}")
        if i < 3:
            run_inject(f"ejecución {i}")

    print("\n[COMPARACIÓN]")
    if hashes[0] == hashes[1] == hashes[2]:
        print(f"  [PASS] hash del archivo invariante: {hashes[0]}")
    else:
        fallos += 1
        print(f"  [FAIL] hash cambió: {hashes[0][:16]} vs {hashes[1][:16]} vs {hashes[2][:16]}")
    if fps[0] == fps[1] == fps[2]:
        print(f"  [PASS] huella estructural invariante: {fps[0]}")
    else:
        fallos += 1
        print(f"  [FAIL] huella cambió: {fps[0][:16]} vs {fps[1][:16]} vs {fps[2][:16]}")

    print("\n" + "=" * 64)
    if fallos:
        print(f"RESULTADO: FAIL — {fallos} fallo(s)")
        sys.exit(1)
    print("RESULTADO: PASS — idempotencia demostrada (2 ejecuciones, sin duplicados, sin cambios topológicos)")
    sys.exit(0)


if __name__ == "__main__":
    main()
