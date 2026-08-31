# Graphify — Sistema Nervioso Central WAIPL (ruta canónica)

> **Ruta canónica fijada por el N3-GRAPHIFY-WRITE (2026-08-23):** `waipl/graphify/graph.json` + `waipl/graphify/graph.html`
> **Ejecutó:** AutoClaw — Construcción del runtime Hermes
> **Incorporado al canónico:** 2026-08-30 (PR desde `fix/graphify-cns-canonical`)

## Estado del grafo

- **Nodos:** 86 · **Aristas:** 59 · **Hiperaristas:** 12
- **4 agentes operativos inyectados** (ids canónicos, NUNCA los previos):
  - `hermes_director_operativo` — Director Operativo (DO). No es Aether.
  - `kairos_will_app` — RAG Will App (matriz). Extractor de evidencia científica.
  - `dike_compliance` — Compliance normativo AESIA/RGPD (no Daik/Dyke).
  - `autoclaw_runtime` — Constructor del runtime Hermes.
- **Hiperarista nueva:** `graphify_cns_operativo` (los 4 agentes, confidence DECLARED, source `N3-GRAPHIFY-WRITE.md`).
- **Provenance:** `built_at_commit` incluido en el propio `graph.json`.

## Archivos

| Archivo | Rol |
|---------|-----|
| `graph.json` | Fuente única de verdad (nodos, aristas, hiperaristas, provenance). |
| `graph.html` | Visualización vis-network (CDN) que consume los datos embebidos. |
| `graph.json.orig` | Backup local previo a la inyección (82 nodos). No se sube al canónico. |

## Notas de integridad

1. **Búsqueda por `id`, no por `label`:** el grafo de fundación tiene labels repetidos (3 × "Carla", 4 × "Zara"). El label devuelve el primer match y puede no apuntar al nodo exacto de una arista. El `id` es inequívoco.
2. **Los archivos `graph.json` / `graph.html` en la RAÍZ del repo son legado** (estado previo al N3). Esta ruta (`waipl/graphify/`) es la canónica. Su retirada o redirección queda a decisión del Soberano.
3. El documento local `INCORPORACION.md` (2026-08-23 16:18) describe la inyección inicial (85/65/13 con ids previos) y quedó **superado** por N3-GRAPHIFY-WRITE (86/59/12 con ids canónicos). No se replica aquí para no introducir metadatos contradictorios.

## Módulo canónico y puntos de incorporación

- Módulo: `waipl/core/graphify.py` (clase `Graphify`, stdlib) — en el workspace del runtime.
- Shims: `waipl/agents/hermes/infrastructure/graphify.py` (Hermes) · `waipl/agents/kairos_graphify.py` (Kairos) · `waipl/agents/dike_graphify.py` (DIKE).
- Scripts de generación: `waipl/scripts/write_graphify_n3.py` · `waipl/scripts/gen_graph_html.py` (locales al EliteBook/Nodo Central).
