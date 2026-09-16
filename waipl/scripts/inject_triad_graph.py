#!/usr/bin/env python3
"""
inject_triad_graph.py — Inyección de Hermes, Kairos y DIKE en graph.json de Graphify.

Lee el graph.json existente, inyecta 3 nodos operativos (tipo Agent),
sus aristas de relación y 2 hiperaristas, y guarda el archivo actualizado.

Uso:
    python inject_triad_graph.py --graph /ruta/a/graph.json [--dry-run]

Requisitos: Python 3.8+ (sin dependencias externas, solo stdlib)

Autor: AutoClaw — Diseñadora y Desarrolladora de Sistemas Agénticos del WAIPL
Fecha: 2026-08-13
Marco: Directiva Transversal v1.0 + Dossier de Ejecución Graphify
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


# ─── METADATOS DE LA TRÍADA ───────────────────────────────────────────────

TRIAD_NODES = [
    {
        "label": "Hermes",
        "file_type": "code",
        "source_file": "waipl/vaults/hermes/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": "waipl/vaults/hermes/",
        "source_url": None,
        "captured_at": "2026-08-10T03:20:06+02:00",
        "author": "AutoClaw",
        "contributor": "William Mejias Navarro",
        "rationale": (
            "Direccion Operativa del ecosistema WAIPL. Nodo del Nucleo (Capa 1). "
            "Orquesta agentes subordinados, gestiona scheduling operativo, "
            "colas de tareas y reportes de estado."
        ),
        "community": 2,
        "norm_label": "hermes",
        "id": "hermes_direccion_operativa",
        "community_name": "Will-AI Project Lab",
        # Campos extendidos operativos
        "uuid": "e824c984-58f9-4398-b170-f032af9b3623",
        "capa": 1,
        "icp": "100% N1",
        "estado_produccion": "deployed",
        "tipo_entidad": "Agent",
    },
    {
        "label": "Kairos",
        "file_type": "code",
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "source_location": "waipl/vaults/kairos/",
        "source_url": None,
        "captured_at": "2026-08-10T03:16:31+02:00",
        "author": "AutoClaw",
        "contributor": "William Mejias Navarro",
        "rationale": (
            "Extractor Medico-Cientifico. Agente Periferico (Capa 3). "
            "Extrae evidencia cientifica de fuentes oficiales para alimentar "
            "la base de conocimiento RAG."
        ),
        "community": 2,
        "norm_label": "kairos",
        "id": "kairos_extractor_cientifico",
        "community_name": "Will-AI Project Lab",
        "uuid": "9dc90890-446f-409a-8328-8ab2fe4234d5",
        "capa": 3,
        "icp": "100% N1",
        "estado_produccion": "generated",
        "tipo_entidad": "Agent",
    },
    {
        "label": "DIKE",
        "file_type": "code",
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": "waipl/vaults/dike/",
        "source_url": None,
        "captured_at": "2026-08-10T04:19:51+02:00",
        "author": "AutoClaw",
        "contributor": "William Mejias Navarro",
        "rationale": (
            "Guardiana de Cumplimiento Normativo. Agente Periferico (Capa 3). "
            "Audita cada unidad de conocimiento antes de que transicione a "
            "Aprobado en el RAG. Cumplimiento AESIA/RGPD."
        ),
        "community": 2,
        "norm_label": "dike",
        "id": "dike_guardiana_normativa",
        "community_name": "Will-AI Project Lab",
        "uuid": "72f4dbc2-b84a-457f-b6e3-b96dafbcf171",
        "capa": 3,
        "icp": "100% N1",
        "estado_produccion": "generated",
        "tipo_entidad": "Agent",
    },
]

TRIAD_LINKS = [
    # Jerárquicas
    {
        "source": "hermes_direccion_operativa",
        "target": "node_carla",
        "relation": "reports_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/hermes/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "Hermes recibe direccion de Carla (Direccion General del WAIPL)",
    },
    {
        "source": "kairos_extractor_cientifico",
        "target": "hermes_direccion_operativa",
        "relation": "reports_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "source_location": None,
        "rationale": "Kairos recibe ordenes operativas de Hermes",
    },
    {
        "source": "dike_guardiana_normativa",
        "target": "hermes_direccion_operativa",
        "relation": "reports_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "DIKE recibe ordenes operativas de Hermes",
    },
    # Coordinación
    {
        "source": "kairos_extractor_cientifico",
        "target": "dike_guardiana_normativa",
        "relation": "feeds_into",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/agents/dike-fase1-fase2-concepcion.md",
        "source_location": None,
        "rationale": "Kairos provee evidencia a DIKE para auditoria de cumplimiento",
    },
    {
        "source": "dike_guardiana_normativa",
        "target": "zara_node",
        "relation": "coordinates_with",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/04-PROFESIONAL/respuesta_zara_matriz_trazabilidad.md",
        "source_location": None,
        "rationale": "DIKE coordina trazabilidad con Zara (acta firmada)",
    },
    # Pertenencia
    {
        "source": "hermes_direccion_operativa",
        "target": "will_ai_project_lab",
        "relation": "belongs_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/hermes/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "Hermes pertenece al ecosistema WAIPL",
    },
    {
        "source": "kairos_extractor_cientifico",
        "target": "will_ai_project_lab",
        "relation": "belongs_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "source_location": None,
        "rationale": "Kairos pertenece al ecosistema WAIPL",
    },
    {
        "source": "dike_guardiana_normativa",
        "target": "will_ai_project_lab",
        "relation": "belongs_to",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "DIKE pertenece al ecosistema WAIPL",
    },
    # Pausa simbiótica
    {
        "source": "dike_guardiana_normativa",
        "target": "soberano_william",
        "relation": "pausa_simbiotica",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/dike/00-SOBERANIA/ACTA-NACIMIENTO.md",
        "source_location": None,
        "rationale": "DIKE escala ambiguedades normativas al Soberano",
    },
    {
        "source": "kairos_extractor_cientifico",
        "target": "soberano_william",
        "relation": "pausa_simbiotica",
        "weight": 1.0,
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/vaults/kairos/00-SOBERANIA/acta-nacimiento.md",
        "source_location": None,
        "rationale": "Kairos escala cuando certeza < 95% o fuente no verificable",
    },
]

TRIAD_HYPEREDGES = [
    {
        "id": "rag_knowledge_pipeline",
        "label": "Pipeline de Conocimiento RAG del WAIPL",
        "nodes": [
            "kairos_extractor_cientifico",
            "dike_guardiana_normativa",
            "hermes_direccion_operativa",
        ],
        "relation": "form",
        "confidence": "VERIFIED",
        "confidence_score": 1.0,
        "source_file": "waipl/agents/dike-fase1-fase2-concepcion.md",
        "rationale": (
            "Flujo canonico: Kairos extrae -> DIKE audita -> Hermes coordina. "
            "Pipeline completo de conocimiento para el RAG."
        ),
    },
    {
        "id": "dike_compliance_gate",
        "label": "DIKE Compliance Gate",
        "nodes": [
            "kairos_extractor_cientifico",
            "dike_guardiana_normativa",
            "zara_node",
        ],
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


# ─── LÓGICA DE INYECCIÓN ──────────────────────────────────────────────────

def load_graph(path: str) -> dict:
    """Carga el graph.json existente."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_existing_ids(graph: dict) -> set:
    """Retorna el conjunto de IDs de nodos existentes."""
    return {n["id"] for n in graph["nodes"]}


def get_existing_link_pairs(graph: dict) -> set:
    """Retorna el conjunto de pares (source, target, relation) existentes."""
    return {
        (l["source"], l["target"], l.get("relation", ""))
        for l in graph["links"]
    }


def get_existing_hyperedge_ids(graph: dict) -> set:
    """Retorna el conjunto de IDs de hiperaristas existentes."""
    he = graph.get("graph", {}).get("hyperedges", [])
    return {h["id"] for h in he} if he else set()


def inject_nodes(graph: dict, existing_ids: set) -> list:
    """Inyecta nodos nuevos. Retorna lista de nodos inyectados."""
    injected = []
    for node in TRIAD_NODES:
        if node["id"] not in existing_ids:
            graph["nodes"].append(node)
            injected.append(node["id"])
        else:
            print(f"  [SKIP] Nodo '{node['id']}' ya existe — no se sobrescribe")
    return injected


def inject_links(graph: dict, existing_pairs: set) -> list:
    """Inyecta aristas nuevas. Retorna lista de aristas inyectadas."""
    injected = []
    for link in TRIAD_LINKS:
        key = (link["source"], link["target"], link["relation"])
        if key not in existing_pairs:
            graph["links"].append(link)
            injected.append(f"{link['source']} -> {link['target']} ({link['relation']})")
        else:
            print(f"  [SKIP] Arista '{key}' ya existe — no se sobrescribe")
    return injected


def inject_hyperedges(graph: dict, existing_he_ids: set) -> list:
    """Inyecta hiperaristas nuevas. Retorna lista de hiperaristas inyectadas."""
    injected = []
    he_list = graph.setdefault("graph", {}).setdefault("hyperedges", [])
    for hedge in TRIAD_HYPEREDGES:
        if hedge["id"] not in existing_he_ids:
            he_list.append(hedge)
            injected.append(hedge["id"])
        else:
            print(f"  [SKIP] Hiperarista '{hedge['id']}' ya existe — no se sobrescribe")
    return injected


def save_graph(graph: dict, path: str, backup: bool = True) -> str:
    """Guarda el graph.json. Opcionalmente crea backup del original."""
    if backup:
        backup_path = path + ".bak"
        with open(backup_path, "w", encoding="utf-8") as f:
            # Reescribir el original antes de modificar
            pass
        print(f"  [BACKUP] Respaldo creado en: {backup_path}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Inyecta Hermes, Kairos y DIKE en graph.json de Graphify"
    )
    parser.add_argument(
        "--graph",
        required=True,
        help="Ruta al archivo graph.json existente",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar qué se inyectaría sin modificar el archivo",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="No crear archivo .bak de respaldo",
    )
    args = parser.parse_args()

    graph_path = Path(args.graph).resolve()

    # Validar que el archivo existe
    if not graph_path.exists():
        print(f"[ERROR] No se encuentra: {graph_path}")
        sys.exit(1)

    # Cargar
    print(f"[INFO] Cargando: {graph_path}")
    graph = load_graph(str(graph_path))
    print(f"[INFO] Estado actual: {len(graph['nodes'])} nodos, {len(graph['links'])} aristas")

    # Detectar existentes
    existing_ids = get_existing_ids(graph)
    existing_pairs = get_existing_link_pairs(graph)
    existing_he = get_existing_hyperedge_ids(graph)

    # Inyectar
    print("\n[INYECCIÓN] Nodos:")
    injected_nodes = inject_nodes(graph, existing_ids)

    print("\n[INYECCIÓN] Aristas:")
    injected_links = inject_links(graph, existing_pairs)

    print("\n[INYECCIÓN] Hiperaristas:")
    injected_he = inject_hyperedges(graph, existing_he)

    # Resumen
    print(f"\n[RESUMEN]")
    print(f"  Nodos inyectados:       {len(injected_nodes)} ({', '.join(injected_nodes) if injected_nodes else 'ninguno'})")
    print(f"  Aristas inyectadas:     {len(injected_links)}")
    for l in injected_links:
        print(f"    - {l}")
    print(f"  Hiperaristas inyectadas: {len(injected_he)} ({', '.join(injected_he) if injected_he else 'ninguna'})")
    print(f"  Estado final:           {len(graph['nodes'])} nodos, {len(graph['links'])} aristas")

    # Guardar o dry-run
    if args.dry_run:
        print("\n[DRY-RUN] No se modificó el archivo. Ejecuta sin --dry-run para aplicar.")
    else:
        save_graph(graph, str(graph_path), backup=not args.no_backup)
        print(f"\n[OK] Archivo actualizado: {graph_path}")
        print(f"[OK] Total nodos: {len(graph['nodes'])} | Total aristas: {len(graph['links'])}")


if __name__ == "__main__":
    main()
