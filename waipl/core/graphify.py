"""Graphify — Sistema Nervioso Central del ecosistema WAIPL.

Carga el graph.json canónico (waipl/graphify/graph.json) y permite que agentes,
nodos y sistemas se lean entre sí: cartografía relacional + relaciones + agentes.

Uso (desde cualquier agente con `waipl/` en sys.path):
    from waipl.core.graphify import Graphify
    g = Graphify()
    g.agent("Hermes")                      # nodo del agente
    g.neighbors("hermes_direccion_operativa")  # con quién se relaciona
    g.relation_to("Kairos", "Hermes")      # relación directa entre dos nodos

Sin dependencias externas (solo stdlib). Una sola fuente de verdad del grafo.
"""
import json
from pathlib import Path

WAIPL_ROOT = Path(__file__).parent.parent          # waipl/
DEFAULT_GRAPH = WAIPL_ROOT / "graphify" / "graph.json"


class Graphify:
    """Acceso de lectura al grafo canónico del ecosistema WAIPL."""

    def __init__(self, path=None):
        self.path = Path(path) if path else DEFAULT_GRAPH
        self.data = self._load()
        self.nodes = self.data.get("nodes", [])
        self.links = self.data.get("links", [])
        self.hyperedges = self.data.get("graph", {}).get("hyperedges", [])
        self._by_id = {n.get("id"): n for n in self.nodes if n.get("id")}

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def node(self, id_or_label):
        """Busca un nodo por id exacto o por label (case-insensitive)."""
        if id_or_label in self._by_id:
            return self._by_id[id_or_label]
        key = (id_or_label or "").lower()
        for n in self.nodes:
            if (n.get("id") or "").lower() == key or (n.get("label") or "").lower() == key:
                return n
        return None

    def neighbors(self, id_or_label):
        """Vecinos de un nodo: relaciones salientes y entrantes con label del otro extremo."""
        nid = (self.node(id_or_label) or {}).get("id")
        if not nid:
            return []
        out = []
        for l in self.links:
            if l.get("source") == nid:
                t = l.get("target")
                out.append({
                    "direction": "out",
                    "other": t,
                    "other_label": (self.node(t) or {}).get("label"),
                    "relation": l.get("relation"),
                })
            elif l.get("target") == nid:
                s = l.get("source")
                out.append({
                    "direction": "in",
                    "other": s,
                    "other_label": (self.node(s) or {}).get("label"),
                    "relation": l.get("relation"),
                })
        return out

    def agents(self):
        """Nodos operativos (tipo_entidad == 'Agent')."""
        return [n for n in self.nodes if n.get("tipo_entidad") == "Agent"]

    def relation_to(self, source, target):
        """Relación directa source -> target, si existe. Devuelve None si no hay arista."""
        sn = (self.node(source) or {}).get("id")
        tn = (self.node(target) or {}).get("id")
        for l in self.links:
            if l.get("source") == sn and l.get("target") == tn:
                return l.get("relation")
        return None

    def summary(self):
        return {
            "nodes": len(self.nodes),
            "links": len(self.links),
            "hyperedges": len(self.hyperedges),
            "agents": [a.get("label") for a in self.agents()],
        }


def load_graph(path=None):
    return Graphify(path)


if __name__ == "__main__":
    g = Graphify()
    print(f"Graphify: {len(g.nodes)} nodos, {len(g.links)} aristas, {len(g.hyperedges)} hiperaristas")
    for a in g.agents():
        print(f"  [Agent] {a.get('label')} ({a.get('id')}) — capa {a.get('capa')}")
