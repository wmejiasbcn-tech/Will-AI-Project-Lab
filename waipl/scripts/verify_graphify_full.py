#!/usr/bin/env python3
"""
verify_graphify_full.py — Validación integral de integridad del grafo canónico
Graphify + huella estructural para prueba de idempotencia.

Comprueba (Orden Soberana, cierre DIKE punto 1):
  - 86 nodos, 69 aristas, 14 hiperaristas (estado esperado post-v2)
  - integridad referencial de TODOS los endpoints (aristas e hiperaristas)
  - unicidad de ids de nodo, triples de arista e ids de hiperarista
  - campos canónicos de los 4 agentes (tipo_entidad, capa, uuid, icp)
  - resolución correcta vía Graphify.agents() y relaciones de la tríada
  - huella estructural SHA-256 (fingerprint) reproducible

Salida: JSON por stdout + exit code 0 si todo OK.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Desktop\AutoClaw")
GRAPH = ROOT / "waipl" / "graphify" / "graph.json"
sys.path.insert(0, str(ROOT))

EXPECTED = {"nodes": 86, "links": 69, "hyperedges": 14}
AGENT_IDS = {"hermes_director_operativo", "kairos_will_app", "dike_compliance", "autoclaw_runtime"}
CANON_FIELDS = ["tipo_entidad", "capa", "icp", "estado_produccion"]
TRIAD_RELATIONS = [
    ("hermes_director_operativo", "node_carla", "reports_to"),
    ("kairos_will_app", "hermes_director_operativo", "reports_to"),
    ("dike_compliance", "hermes_director_operativo", "reports_to"),
    ("kairos_will_app", "dike_compliance", "feeds_into"),
    ("dike_compliance", "zara_node", "coordinates_with"),
    ("hermes_director_operativo", "will_ai_project_lab", "belongs_to"),
    ("kairos_will_app", "will_ai_project_lab", "belongs_to"),
    ("dike_compliance", "will_ai_project_lab", "belongs_to"),
    ("dike_compliance", "soberano_william", "pausa_simbiotica"),
    ("kairos_will_app", "soberano_william", "pausa_simbiotica"),
]
TRIAD_HYPEREDGES = {"rag_knowledge_pipeline", "dike_compliance_gate", "graphify_cns_operativo"}


def main():
    raw = GRAPH.read_bytes()
    file_hash = hashlib.sha256(raw).hexdigest()
    graph = json.loads(raw.decode("utf-8"))

    errores, checks = [], []

    def check(nombre, cond, detalle=""):
        checks.append({"check": nombre, "ok": bool(cond), "detalle": detalle})
        if not cond:
            errores.append(f"{nombre}: {detalle}")

    n_nodes = len(graph.get("nodes", []))
    n_links = len(graph.get("links", []))
    he = graph.get("graph", {}).get("hyperedges", [])
    he_top = graph.get("hyperedges", [])
    n_he = len(he)
    check("total nodos", n_nodes == EXPECTED["nodes"], f"{n_nodes} (esperados {EXPECTED['nodes']})")
    check("total aristas", n_links == EXPECTED["links"], f"{n_links} (esperadas {EXPECTED['links']})")
    check("total hiperaristas", n_he == EXPECTED["hyperedges"], f"{n_he} (esperadas {EXPECTED['hyperedges']})")
    check("hiperaristas sincronizadas top-level/graph", he_top == he, f"top={len(he_top)} graph={len(he)}")

    # Integridad referencial completa
    ids = [n.get("id") for n in graph["nodes"]]
    id_set = set(ids)
    check("ids de nodo únicos", len(ids) == len(id_set), f"{len(ids)} nodos, {len(id_set)} ids")
    for l in graph["links"]:
        if l.get("source") not in id_set:
            errores.append(f"arista source inexistente: {l.get('source')}")
        if l.get("target") not in id_set:
            errores.append(f"arista target inexistente: {l.get('target')}")
    check("endpoints de aristas existen", not errores, f"{len(graph['links'])} aristas verificadas")

    triples = [(l["source"], l["target"], l.get("relation", "")) for l in graph["links"]]
    check("triples de arista únicos (sin duplicados)", len(triples) == len(set(triples)),
          f"{len(triples)} aristas, {len(set(triples))} triples únicos")

    he_ids = [h.get("id") for h in he]
    check("ids de hiperarista únicos", len(he_ids) == len(set(he_ids)), str(len(he_ids)))
    for h in he:
        for nid in h.get("nodes", []):
            if nid not in id_set:
                errores.append(f"hiperarista {h.get('id')}: miembro inexistente {nid}")
    check("miembros de hiperaristas existen", all("miembro inexistente" not in e for e in errores), str(len(he)))

    # Campos canónicos de agentes
    by_id = {n["id"]: n for n in graph["nodes"]}
    for aid in AGENT_IDS:
        n = by_id.get(aid)
        check(f"nodo agente {aid} existe", n is not None)
        if n:
            faltan = [f for f in CANON_FIELDS if f not in n]
            check(f"campos canónicos {aid}", not faltan, f"faltan: {faltan}" if faltan else "completos")

    # Relaciones de la tríada (topología operativa v2)
    tset = set(triples)
    for t in TRIAD_RELATIONS:
        check(f"arista {t[0]} -> {t[1]} ({t[2]})", t in tset, "presente" if t in tset else "AUSENTE")

    hset = set(he_ids)
    for hid in TRIAD_HYPEREDGES:
        check(f"hiperarista {hid}", hid in hset, "presente" if hid in hset else "AUSENTE")

    # Resolución vía API canónica
    from waipl.core.graphify import Graphify
    g = Graphify()
    agents = sorted(a["id"] for a in g.agents())
    check("Graphify.agents() resuelve los 4 agentes", agents == sorted(AGENT_IDS), str(agents))
    check("relation_to kairos->dike", g.relation_to("kairos_will_app", "dike_compliance") == "feeds_into")
    check("relation_to dike->hermes", g.relation_to("dike_compliance", "hermes_director_operativo") == "reports_to")
    check("neighbors dike >= 6", len(g.neighbors("dike_compliance")) >= 6, f"{len(g.neighbors('dike_compliance'))} vecinos")

    # Huella estructural (independiente del orden de serialización)
    fingerprint_src = json.dumps(
        {
            "nodes": sorted(ids),
            "triples": sorted(triples),
            "hyperedges": sorted(he_ids),
            "he_members": {h["id"]: sorted(h.get("nodes", [])) for h in he},
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    fingerprint = hashlib.sha256(fingerprint_src.encode("utf-8")).hexdigest()

    result = {
        "graph_path": str(GRAPH),
        "file_sha256": file_hash,
        "structural_fingerprint_sha256": fingerprint,
        "counts": {"nodes": n_nodes, "links": n_links, "hyperedges": n_he},
        "total_checks": len(checks),
        "fallos": len(errores),
        "errores": errores,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if not errores else 1)


if __name__ == "__main__":
    main()
