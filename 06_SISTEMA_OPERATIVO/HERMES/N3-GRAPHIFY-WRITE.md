# N3-GRAPHIFY-WRITE

**Grantor:** Soberano 2026-08-23  
**Orden:** inyectar Graphify en Hermes, Kairos, Dike y AutoClaw.  
**Voz:** Alvaro **confirmada** (no reabrir).

No hay API Graphify. El instrumento **es** el par:

1. `graph.json` (datos)
2. `graph.html` (vis-network — lo que el Lab llama Graphify)

`graph.json` de GitHub `main` tiene `nodes=[]` (hueco). **No es la base.** Base = el grafo de **82 nodos** que ya tienes en el EliteBook (el mismo que está embebido en `graph.html`).

## Cómo (no pares; hazlo así)

1. Base: `graph.json` local de 82 nodos. Comprueba `len(nodes)>=80`. Si es 0, aborta y usa el JSON del adjunto/graph.html, no `main`.
2. Añade 4 nodos (mismo schema que Carla: `id,label,file_type,source_file,rationale,community,norm_label,community_name`):
   - `hermes_director_operativo` — DO, no Aether
   - `kairos_will_app` — RAG Will App (matriz)
   - `dike_compliance` — Dike (no Daik/Dyke)
   - `autoclaw_runtime` — constructor del runtime Hermes
3. 4 aristas `implements` → `will_ai_project_lab`
4. Hiperarista `graphify_cns_operativo` con esos 4 ids. `confidence: DECLARED`
5. Escribe **los dos**: `graph.json` (top-level `nodes` y `links` llenos) **y** `graph.html` (`RAW_NODES`, `RAW_EDGES`, `hyperedges`, stats).
6. Entrega: esos dos archivos. Si no hay `GITHUB_TOKEN`, no inventes push; deja rutas. El PR lo abre quien tenga grant. No copies markdown al Soberano.

## Prohibido

- Base = `main` con `nodes=[]`
- Solo JSON en Desktop, sin `graph.html`
- Identidad `Aether-Hermes`
- `graphify/write` a un servicio inventado

## Éxito

Búsqueda en Graphify: Hermes, Kairos, Dike, AutoClaw. 86 nodos. Pie CANON-CIERRE de `CANON-CIERRE.md`.
