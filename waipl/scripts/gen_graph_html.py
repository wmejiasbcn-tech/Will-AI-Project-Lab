#!/usr/bin/env python3
"""gen_graph_html.py — Genera graph.html (vis-network) desde graph.json.

Embebe RAW_NODES, RAW_EDGES, hyperedges y stats conforme a N3-GRAPHIFY-WRITE.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # AutoClaw
GRAPH = ROOT / "waipl" / "graphify" / "graph.json"
OUT = ROOT / "waipl" / "graphify" / "graph.html"

AGENT_IDS = {
    "hermes_director_operativo",
    "kairos_will_app",
    "dike_compliance",
    "autoclaw_runtime",
}


def main():
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = g["nodes"]
    links = g["links"]
    hyperedges = g.get("graph", {}).get("hyperedges", [])

    raw_nodes = []
    for n in nodes:
        is_agent = n["id"] in AGENT_IDS
        raw_nodes.append({
            "id": n["id"],
            "label": n.get("label", n["id"]),
            "group": n.get("community", 0),
            "shape": "diamond" if is_agent else "dot",
            "color": {"background": "#a070e0", "border": "#5cff5c"} if is_agent else None,
            "title": (n.get("rationale") or n.get("label") or n["id"])[:160],
        })

    raw_edges = [
        {"from": l["source"], "to": l["target"], "label": l.get("relation", "")}
        for l in links
    ]

    stats = {"nodes": len(nodes), "links": len(links), "hyperedges": len(hyperedges)}

    html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Graphify — Sistema Nervioso Central WAIPL</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Segoe UI',system-ui,sans-serif;background:#08081a;color:#c8d8f0}
  #header{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding:12px 20px;background:#0a0020;border-bottom:2px solid #301870}
  #header strong{color:#a070e0;letter-spacing:1px}
  .stat{font-size:0.82em;color:#8888bb}
  .stat b{color:#c8d8f0}
  #graph{width:100%;height:calc(100vh - 56px);background:#08081a}
  #legend{position:fixed;bottom:12px;left:12px;background:#0a0020;border:1px solid #301870;border-radius:8px;padding:8px 12px;font-size:0.75em;color:#aabbcc}
  #legend .ag{color:#5cff5c}
</style>
</head>
<body>
<div id="header">
  <strong>◈ GRAPHIFY — Sistema Nervioso Central WAIPL ◈</strong>
  <span class="stat">Nodos: <b id="stat-nodes"></b></span>
  <span class="stat">Aristas: <b id="stat-links"></b></span>
  <span class="stat">Hiperaristas: <b id="stat-he"></b></span>
</div>
<div id="graph"></div>
<div id="legend">◆ <span class="ag">agentes operativos</span> (Hermes · Kairos · Dike · AutoClaw) &nbsp;·&nbsp; ● nodos de fundación</div>
<script>
const RAW_NODES = __RAW_NODES__;
const RAW_EDGES = __RAW_EDGES__;
const hyperedges = __HYPEREDGES__;
const stats = __STATS__;

document.getElementById('stat-nodes').textContent = stats.nodes;
document.getElementById('stat-links').textContent = stats.links;
document.getElementById('stat-he').textContent = stats.hyperedges;

const container = document.getElementById('graph');
const data = {
  nodes: new vis.DataSet(RAW_NODES),
  edges: new vis.DataSet(RAW_EDGES)
};
const options = {
  physics: { stabilization: { iterations: 200 }, barnesHut: { gravitationalConstant: -3000, springLength: 120 } },
  nodes: { font: { color: '#c8d8f0', size: 12 }, borderWidth: 1 },
  edges: { font: { size: 8, color: '#5555aa', strokeWidth: 0 }, arrows: { to: { enabled: true, scaleFactor: 0.5 } }, color: { color: '#3a3a6a' } },
  interaction: { hover: true, tooltipDelay: 100 }
};
const network = new vis.Network(container, data, options);
</script>
</body>
</html>
"""

    html = (html
            .replace("__RAW_NODES__", json.dumps(raw_nodes, ensure_ascii=False))
            .replace("__RAW_EDGES__", json.dumps(raw_edges, ensure_ascii=False))
            .replace("__HYPEREDGES__", json.dumps(hyperedges, ensure_ascii=False))
            .replace("__STATS__", json.dumps(stats)))

    OUT.write_text(html, encoding="utf-8")
    print(f"[OK] graph.html escrito: {OUT} ({len(html)} bytes)")
    print(f"[INFO] stats: {stats}")


if __name__ == "__main__":
    main()
