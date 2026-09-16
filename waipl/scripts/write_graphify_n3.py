#!/usr/bin/env python3
"""
write_graphify_n3.py — Escritura Graphify conforme a N3-GRAPHIFY-WRITE.

Base: graph.json local de 82 nodos (nunca `main` con nodes=[]).
Inyecta 4 nodos canónicos + 4 aristas `implements` -> will_ai_project_lab
+ 1 hiperarista `graphify_cns_operativo` (confidence DECLARED).
Resultado esperado: 86 nodos.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # AutoClaw (workspace raíz)
BASE = ROOT / ".openclaw-attachments" / "20260823-160750-4aa87ec3-678-graph.json"
OUT = ROOT / "waipl" / "graphify" / "graph.json"

NODES = [
    {
        "label": "Hermes",
        "file_type": "code",
        "source_file": "waipl/vaults/hermes/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "rationale": "Director Operativo del ecosistema WAIPL (DO). No es Aether.",
        "community": 2,
        "norm_label": "hermes",
        "id": "hermes_director_operativo",
        "community_name": "Will-AI Project Lab",
    },
    {
        "label": "Kairos",
        "file_type": "code",
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "rationale": "RAG de la Will App (matriz). Extractor de evidencia cientifica.",
        "community": 2,
        "norm_label": "kairos",
        "id": "kairos_will_app",
        "community_name": "Will-AI Project Lab",
    },
    {
        "label": "Dike",
        "file_type": "code",
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "rationale": "Compliance normativo del ecosistema (no Daik/Dyke). AESIA/RGPD.",
        "community": 2,
        "norm_label": "dike",
        "id": "dike_compliance",
        "community_name": "Will-AI Project Lab",
    },
    {
        "label": "AutoClaw",
        "file_type": "code",
        "source_file": "IDENTITY.md",
        "rationale": "Constructor del runtime Hermes. Disenadora y Desarrolladora de Sistemas Agenticos del WAIPL.",
        "community": 2,
        "norm_label": "autoclaw",
        "id": "autoclaw_runtime",
        "community_name": "Will-AI Project Lab",
    },
]

LINKS = [
    {
        "relation": "implements",
        "confidence": "DECLARED",
        "confidence_score": 1.0,
        "source_file": "N3-GRAPHIFY-WRITE.md",
        "source_location": None,
        "weight": 1.0,
        "source": nid,
        "target": "will_ai_project_lab",
    }
    for nid in ["hermes_director_operativo", "kairos_will_app", "dike_compliance", "autoclaw_runtime"]
]

HYPEREDGE = {
    "id": "graphify_cns_operativo",
    "label": "Graphify CNS Operativo",
    "nodes": ["hermes_director_operativo", "kairos_will_app", "dike_compliance", "autoclaw_runtime"],
    "relation": "form",
    "confidence": "DECLARED",
    "confidence_score": 1.0,
    "source_file": "N3-GRAPHIFY-WRITE.md",
}


def main():
    if not BASE.exists():
        print(f"[ERROR] Base no encontrada: {BASE}")
        sys.exit(1)

    graph = json.loads(BASE.read_text(encoding="utf-8"))
    n = len(graph.get("nodes", []))
    print(f"[INFO] Base: {n} nodos, {len(graph.get('links', []))} aristas")
    if n < 80:
        print(f"[ERROR] Base con nodes<80 ({n}). Abortar: no usar main con nodes=[].")
        sys.exit(2)

    existing_ids = {nd["id"] for nd in graph["nodes"]}
    added_nodes = []
    for nd in NODES:
        if nd["id"] not in existing_ids:
            graph["nodes"].append(nd)
            existing_ids.add(nd["id"])
            added_nodes.append(nd["id"])
        else:
            print(f"  [SKIP nodo] {nd['id']} ya existe")

    existing_pairs = {(l["source"], l["target"], l.get("relation")) for l in graph["links"]}
    added_links = []
    for lk in LINKS:
        key = (lk["source"], lk["target"], lk["relation"])
        if key not in existing_pairs:
            graph["links"].append(lk)
            added_links.append(key)
        else:
            print(f"  [SKIP arista] {key}")

    # Hiperaristas: mantener consistencia entre graph.hyperedges y top-level hyperedges
    he_list = graph.setdefault("graph", {}).setdefault("hyperedges", [])
    he_ids = {h.get("id") for h in he_list}
    if HYPEREDGE["id"] not in he_ids:
        he_list.append(HYPEREDGE)
        print(f"  [OK hiperarista] {HYPEREDGE['id']}")
    # Sincronizar top-level hyperedges con graph.hyperedges (una sola fuente)
    graph["hyperedges"] = he_list

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    final_n = len(graph["nodes"])
    print(f"[RESUMEN] nodos añadidos: {len(added_nodes)} ({', '.join(added_nodes)})")
    print(f"[RESUMEN] aristas añadidas: {len(added_links)}")
    print(f"[RESUMEN] total final: {final_n} nodos, {len(graph['links'])} aristas, {len(he_list)} hiperaristas")
    print(f"[OK] escrito: {OUT}")


if __name__ == "__main__":
    main()
