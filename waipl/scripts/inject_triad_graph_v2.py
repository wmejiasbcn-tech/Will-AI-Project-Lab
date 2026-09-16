#!/usr/bin/env python3
"""
inject_triad_graph_v2.py — Reinyección canónica de la topología operativa de la tríada.

Contexto: el 2026-08-23 la tríada (Hermes, Kairos, DIKE) fue inyectada con 10 aristas
+ 2 hiperaristas, pero la reconstrucción posterior conforme a N3-GRAPHIFY-WRITE partió
de un snapshot PRE-inyección, dejando el grafo solo con las 4 aristas `implements`
canónicas. Este script restaura la topología operativa verificada usando los
IDS CANÓNICOS N3 (hermes_director_operativo, kairos_will_app, dike_compliance).

- Idempotente: salta nodos/aristas/hiperaristas ya existentes (clave: triple source-target-relation).
- Valida integridad referencial ANTES de escribir (aborta si falta un endpoint).
- Crea backup real del grafo antes de modificar.
- Mantiene sincronizadas `graph.hyperedges` y `hyperedges` top-level (convención N3).

Uso:
    python inject_triad_graph_v2.py --graph /ruta/a/graph.json [--dry-run]

Requisitos: Python 3.8+ (solo stdlib)

Autor: AutoClaw — Diseñadora y Desarrolladora de Sistemas Agénticos del WAIPL
Fecha: 2026-09-01
Marco: Directiva Transversal v1.0 + incorporacion.md (relaciones verificadas 2026-08-23)
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# ─── IDS CANÓNICOS N3 ─────────────────────────────────────────────────────

ID_HERMES = "hermes_director_operativo"
ID_KAIROS = "kairos_will_app"
ID_DIKE = "dike_compliance"
ID_WAIPL = "will_ai_project_lab"
ID_CARLA = "node_carla"
ID_ZARA = "zara_node"
ID_SOBERANO = "soberano_william"

TRIAD_LINKS = [
    # Jerárquicas
    {
        "source": ID_HERMES,
        "target": ID_CARLA,
        "relation": "reports_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/hermes/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "Hermes recibe direccion de Carla (Direccion General del WAIPL)",
    },
    {
        "source": ID_KAIROS,
        "target": ID_HERMES,
        "relation": "reports_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "source_location": None,
        "rationale": "Kairos recibe ordenes operativas de Hermes (Director Operativo)",
    },
    {
        "source": ID_DIKE,
        "target": ID_HERMES,
        "relation": "reports_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "DIKE recibe ordenes operativas de Hermes (Director Operativo)",
    },
    # Coordinación
    {
        "source": ID_KAIROS,
        "target": ID_DIKE,
        "relation": "feeds_into",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/agents/dike-fase1-fase2-concepcion.md",
        "source_location": None,
        "rationale": "Kairos provee evidencia cientifica a DIKE para auditoria de cumplimiento",
    },
    {
        "source": ID_DIKE,
        "target": ID_ZARA,
        "relation": "coordinates_with",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/04-PROFESIONAL/respuesta_zara_matriz_trazabilidad.md",
        "source_location": None,
        "rationale": "DIKE coordina trazabilidad con Zara (acta formal de aceptacion firmada)",
    },
    # Pertenencia (complementa las aristas `implements` canónicas del N3)
    {
        "source": ID_HERMES,
        "target": ID_WAIPL,
        "relation": "belongs_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/hermes/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "Hermes pertenece al ecosistema WAIPL",
    },
    {
        "source": ID_KAIROS,
        "target": ID_WAIPL,
        "relation": "belongs_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "source_location": None,
        "rationale": "Kairos pertenece al ecosistema WAIPL",
    },
    {
        "source": ID_DIKE,
        "target": ID_WAIPL,
        "relation": "belongs_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "DIKE pertenece al ecosistema WAIPL",
    },
    # Pausa simbiótica (Human-in-the-Loop)
    {
        "source": ID_DIKE,
        "target": ID_SOBERANO,
        "relation": "pausa_simbiotica",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "DIKE escala ambiguedades normativas al Soberano (puntos 1 y 3)",
    },
    {
        "source": ID_KAIROS,
        "target": ID_SOBERANO,
        "relation": "pausa_simbiotica",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "source_location": None,
        "rationale": "Kairos escala al Soberano cuando certeza < 95% o fuente no verificable",
    },
]

TRIAD_HYPEREDGES = [
    {
        "id": "rag_knowledge_pipeline",
        "label": "Pipeline de Conocimiento RAG del WAIPL",
        "nodes": [ID_KAIROS, ID_DIKE, ID_HERMES],
        "relation": "form",
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/core/rag_pipeline.py",
        "rationale": (
            "Flujo canonico: Kairos extrae -> Codd archiva -> DIKE audita -> "
            "VAC-01 valida -> RAG (Will App). Implementado en waipl/core/rag_pipeline.py."
        ),
    },
    {
        "id": "dike_compliance_gate",
        "label": "DIKE Compliance Gate",
        "nodes": [ID_KAIROS, ID_DIKE, ID_ZARA],
        "relation": "participate_in",
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/04-PROFESIONAL/respuesta_zara_matriz_trazabilidad.md",
        "rationale": (
            "Gate critico: sin DIKE, nada pasa de 'En revision' a 'Aprobado' "
            "en el RAG. Zara supervisa la matriz de trazabilidad."
        ),
    },
]


# ─── ENRIQUECIMIENTO DE NODOS (campos operativos perdidos en el rebuild N3) ──

NODE_ENRICHMENT = {
    ID_HERMES: {
        "tipo_entidad": "Agent",
        "capa": 1,
        "icp": "100% N1",
        "estado_produccion": "deployed",
        "uuid": "e824c984-58f9-4398-b170-f032af9b3623",
    },
    ID_KAIROS: {
        "tipo_entidad": "Agent",
        "capa": 3,
        "icp": "100% N1",
        "estado_produccion": "generated",
        "uuid": "9dc90890-446f-409a-8328-8ab2fe4234d5",
    },
    ID_DIKE: {
        "tipo_entidad": "Agent",
        "capa": 3,
        "icp": "100% N1",
        "estado_produccion": "generated",
        "uuid": "72f4dbc2-b84a-457f-b6e3-b96dafbcf171",
    },
    "autoclaw_runtime": {
        "tipo_entidad": "Agent",
        "capa": 2,
        "icp": "100% N1",
        "estado_produccion": "deployed",
    },
}


def enrich_nodes(graph: dict) -> list:
    """Anade campos operativos a los nodos canonicos si faltan. No sobrescribe valores existentes."""
    enriched = []
    for n in graph["nodes"]:
        extra = NODE_ENRICHMENT.get(n.get("id"))
        if not extra:
            continue
        changed = False
        for k, v in extra.items():
            if k not in n:
                n[k] = v
                changed = True
        if changed:
            enriched.append(n["id"])
    return enriched


# ─── LÓGICA DE INYECCIÓN ──────────────────────────────────────────────────

def load_graph(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_referential_integrity(graph: dict) -> list:
    """Retorna lista de errores: endpoints de aristas/hiperaristas inexistentes."""
    ids = {n["id"] for n in graph["nodes"]}
    errors = []
    for l in graph["links"]:
        if l.get("source") not in ids:
            errors.append(f"Arista con source inexistente: {l.get('source')}")
        if l.get("target") not in ids:
            errors.append(f"Arista con target inexistente: {l.get('target')}")
    for h in graph.get("graph", {}).get("hyperedges", []):
        for nid in h.get("nodes", []):
            if nid not in ids:
                errors.append(f"Hiperarista '{h.get('id')}' con miembro inexistente: {nid}")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Reinyecta la topologia operativa canonica de la triada en graph.json"
    )
    parser.add_argument("--graph", required=True, help="Ruta al graph.json canonico")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar cambios sin escribir")
    parser.add_argument("--no-backup", action="store_true", help="No crear backup pre-inyeccion")
    args = parser.parse_args()

    graph_path = Path(args.graph).resolve()
    if not graph_path.exists():
        print(f"[ERROR] No se encuentra: {graph_path}")
        sys.exit(1)

    print(f"[INFO] Cargando: {graph_path}")
    graph = load_graph(graph_path)
    n0, l0 = len(graph["nodes"]), len(graph["links"])
    print(f"[INFO] Estado actual: {n0} nodos, {l0} aristas")

    existing_ids = {n["id"] for n in graph["nodes"]}

    # Validar que TODOS los endpoints de la topologia a inyectar existen
    required = {ID_HERMES, ID_KAIROS, ID_DIKE, ID_WAIPL, ID_CARLA, ID_ZARA, ID_SOBERANO}
    missing = required - existing_ids
    if missing:
        print(f"[ERROR] Nodos requeridos ausentes en el grafo: {sorted(missing)}. Abortando.")
        sys.exit(2)

    # Nodos: enriquecer campos operativos si faltan (no se anaden: ya existen via N3)
    enriched = enrich_nodes(graph)
    if enriched:
        print(f"  [ENRICH] Campos operativos restaurados en: {', '.join(enriched)}")
    for nid in (ID_HERMES, ID_KAIROS, ID_DIKE):
        if nid not in existing_ids:
            print(f"[WARN] Nodo canonico ausente (no se anade en v2): {nid}")

    # Aristas idempotentes
    existing_pairs = {(l["source"], l["target"], l.get("relation", "")) for l in graph["links"]}
    injected_links = []
    for link in TRIAD_LINKS:
        key = (link["source"], link["target"], link["relation"])
        if key not in existing_pairs:
            graph["links"].append(link)
            existing_pairs.add(key)
            injected_links.append(f"{link['source']} -> {link['target']} ({link['relation']})")
        else:
            print(f"  [SKIP] Arista ya existe: {key}")

    # Hiperaristas idempotentes (sincronizadas en graph.hyperedges y top-level)
    he_list = graph.setdefault("graph", {}).setdefault("hyperedges", [])
    he_ids = {h.get("id") for h in he_list}
    injected_he = []
    for hedge in TRIAD_HYPEREDGES:
        if hedge["id"] not in he_ids:
            he_list.append(hedge)
            he_ids.add(hedge["id"])
            injected_he.append(hedge["id"])
        else:
            print(f"  [SKIP] Hiperarista ya existe: {hedge['id']}")
    graph["hyperedges"] = he_list  # sincronizar top-level (convencion N3)

    # Integridad referencial del grafo resultante
    errors = validate_referential_integrity(graph)
    if errors:
        print("[ERROR] Integridad referencial fallida — NO se escribe el grafo:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(3)

    # Resumen
    n1, l1 = len(graph["nodes"]), len(graph["links"])
    agent_count = sum(1 for n in graph["nodes"] if n.get("tipo_entidad") == "Agent")
    print("\n[RESUMEN]")
    print(f"  Nodos: {n0} -> {n1} (sin cambios: ya inyectados via N3)")
    print(f"  Nodos enriquecidos: {len(enriched)} ({', '.join(enriched) if enriched else 'ninguno'})")
    print(f"  Nodos tipo_entidad=Agent: {agent_count}")
    print(f"  Aristas inyectadas: {len(injected_links)}")
    for l in injected_links:
        print(f"    - {l}")
    print(f"  Hiperaristas inyectadas: {len(injected_he)} ({', '.join(injected_he) if injected_he else 'ninguna'})")
    print(f"  Estado final: {n1} nodos, {l1} aristas, {len(he_list)} hiperaristas")
    print(f"  Integridad referencial: OK ({len(errors)} errores)")

    if args.dry_run:
        print("\n[DRY-RUN] No se modifico el archivo. Ejecuta sin --dry-run para aplicar.")
        return

    if not args.no_backup:
        backup_path = graph_path.with_name(graph_path.name + ".pre-triada-v2")
        shutil.copy2(graph_path, backup_path)
        print(f"\n[BACKUP] {backup_path}")

    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"[OK] Escrito: {graph_path}")


if __name__ == "__main__":
    main()
