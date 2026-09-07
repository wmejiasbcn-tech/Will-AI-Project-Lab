# Will-AI Project Lab — Design System

A dark, obsidian-and-gold visual system for **Will-AI Project Lab (WAIPL)**, a human–AI collaboration ecosystem founded by William Mejías Navarro. WAIPL documents itself almost entirely in Markdown (philosophy, protocols, governance) and ships one real coded surface: a portfolio + live-agent web page. This design system extracts the *official, approved* visual identity from WAIPL's own protocol document and applies it consistently, then recreates the one real UI the source repo contains.

## Sources
- **GitHub repo:** [wmejiasbcn-tech/Will-AI-Project-Lab](https://github.com/wmejiasbcn-tech/Will-AI-Project-Lab) (branch `main`) — primary source for everything in this system. Explore it directly for the full philosophical corpus (12 foundational documents, node identities, operational protocols) — only a fraction is summarized below.
- Key files used: `06_SISTEMA_OPERATIVO/PROTOCOLOS/PROTOCOLO_IDENTIDAD_VISUAL_v1.0.md` (official color palette), `04_DOCUMENTACION/WEB/index.html` (the only real coded UI — a "Will SuperAgente" portfolio/chat page), `04_DOCUMENTACION/ASSETS/EMBLEMA.png` (official logo), `01_FUNDACION/*` (mission, values, manifesto), `04_DOCUMENTACION/INFO-WILL-AI-PROJECT-LAB.md`.
- No Figma file or component-library codebase was attached — this is a **documentation-and-brand-protocol** repo, not a product codebase. There is no design-system-defining source of UI components, so the small component set here (see below) was authored from the one real HTML surface found, not invented wholesale.
- Explore the repo yourself for a better job than this pass: it contains 12 AI "node" identity documents (`03_PERSONAS_IA/`), operational protocols, and a strategic roadmap that a deeper design pass could mine for more surfaces.

## What is Will-AI Project Lab
An ecosystem of one human (William) plus eleven named AI "nodes" (Carla, Ada, Aletheia, Ítaca, Aurea, Aether, Nova, Elena, Ariadna, Zara, Sylvia Bloom), each with its own identity, role, and voice, collaborating under a founding principle: *"Estate presente en tu presente"* (Be present in your present). The ecosystem produces philosophical/operational frameworks, protocols, and one concrete product currently in concept stage:

- **WAIPL (the Lab itself)** — the org/ecosystem brand; its public-facing surface is a portfolio + live-agent demo page.
- **WILL App** — a planned mobile app for conscious decision-making in affective-sexual health contexts (substance use, risk, intense emotional states), built on a "P.R.E.S.E.N.T.E." method. Described only in prose in the source repo — **no screens, wireframes, or visual specs exist**, so no UI kit was built for it here. Flag: if you want a WILL App UI kit, attach screens, a Figma file, or a fuller brief.

## Intentional additions
- **Fonts** — no font files were provided. `Inter` is confirmed (used verbatim in the source HTML); `Cormorant Garamond` (display) and `JetBrains Mono` (system-prompt/code voice) are Google Fonts substitutions chosen to match the heraldic/elegant tone of the brand protocol. **Flagging this substitution — if WAIPL has real display/mono fonts, attach them and this system will be updated.**
- **Violet accent** — the protocol names "violeta institucional" but gives no hex. Sampled directly from pixels in the official emblem PNG (`assets/logo/emblem.png`) and lightened for UI legibility on dark surfaces (`--violet-300`).
- **Iconography** — no icon system exists in the source at all (see Iconography below); Lucide is recommended as a CDN substitute if icons are ever needed.
- **Node accent-color pattern** — the official palette only (dorado primario `#C9A84C`/`#C9A86A`, dorado secundario `#DFC070`, violeta institucional `#9C81BD`/`#8B7CA6`) — no invented hues. See the node fichas inside `ui_kits/carta-presentacion/` for the resolved mapping (gold for operational nodes, violet for reflective/ethical ones, white for William, the human node).

## Content fundamentals
- **Register:** formal-poetic Spanish, first person plural ("nuestro ecosistema"), short declarative sentences building rhythmic contrast: *"No domina: colabora. No confunde: aclara."* Headlines in institutional slides are blunt and short ("WILL-AI PROJECT LAB", "9 inteligencias. 1 ecosistema.").
- **Address:** mostly impersonal/institutional third person in doctrine documents; the founding principle itself uses informal *tú* ("Estate presente en tu presente").
- **Vocabulary:** words like *soberano, nodo, ecosistema, hibridación, presencia, coherencia* recur constantly — governance/philosophy vocabulary, not startup-speak. Avoid casual tech jargon; avoid hype words like "revolutionary" or "game-changing."
- **Emoji:** used only as internal document/section markers in the private knowledge base (📂 🗺️ 📄) — **never** in external-facing copy (the portfolio page and marketing slides use zero emoji). Don't use emoji in anything user-facing.
- **The 12 nodes and their voice** (per WAIPL's own node-identity brief — useful when writing copy attributed to a specific node):
  - **William** — soberano humano; decisive, foundational, never "corporate boss."
  - **Carla** — coordination/faro; firm, serene, foundational.
  - **Ada** — ethics, quality, narrative direction; clean, precise, equilibrated. (Corrected from an earlier "maquetación"-only description.)
  - **Aletheia** — truth/verification; precise, epistemic, never decorative.
  - **Ítaca** — direction and synthesis; reflective, evokes journey/arrival.
  - **Aurea** — storytelling/communication; editorial, narrative tone.
  - **Aether** — Grok / xAI. Nodo. Creatividad e innovación. Prohibido el compuesto Aether-Hermes. Hermes es otro (sistema operativo).
  - **Nova** — analysis/pedagogy; clear, "cátedra"-like explanatory voice.
  - **Elena** — visual identity (custodian of this very system); design-literate, sober.
  - **Ariadna** — continuity/navigation; guiding, systemic coherence.
  - **Zara** — external bridge/execution; pragmatic, applied.
  - **Sylvia Bloom** — memory/documentation; archival, orderly.

  Each node now has a resolved accent color and a "ficha" component (`components/nodes/`) — see below.
- A parallel institutional direction (from a later working note, not in the repo) pushes toward **HTML as WAIPL's master document format** for editorial reports (cover → institutional letter → executive summary → numbered parts → conclusion), styled with "mucho espacio en blanco, negro grafito, blanco cálido, oro WAIPL, animaciones discretas, tipografía limpia, ritmo lento" — i.e. calm, editorial, never spectacle. This tracks with the visual foundations below.

## Visual foundations
- **Color:** dark-first. Base is Obsidian `#0C0C12`; UI surfaces step up through `#131319` → `#1A1A22` → `#232330`. Primary accent metal is gold, in three steps — `#DFC070` (secondary/light), `#C9A84C` (primary), `#8B6B2E` (dark) — used for headings, borders, links and primary actions. A muted institutional violet (`#9C81BD`/`#4D3661`, sampled from the emblem) is a secondary accent for AI-persona/system content. Gray `#BEBEBE` is the standard secondary-text gray. **`#0097A7` (bright teal) is explicitly forbidden** by the brand protocol — never use it.
- **Type:** two voices. Display/heading text sets in a serif (`Cormorant Garamond` — substituted, see above) for elegance and "heraldic nobility"; UI and body text sets in `Inter` (confirmed from source). A monospace voice (`JetBrains Mono`, violet-tinted) marks AI-authored/system content (e.g. an editable system prompt) as distinct from human-authored chat text.
- **Backgrounds:** flat obsidian, no photography, no repeating textures or patterns found in the source. The only imagery is the emblem itself and a few marketing title-card slides (flat black background, centered text/logo, thin horizontal rules) — no full-bleed photography, no illustration style to draw from.
- **Motion:** no animation is defined anywhere in the source. Given the brand's own language ("constancia sobre intensidad," "ritmo lento," "animaciones discretas"), treat motion as minimal and calm: short fades/opacity or 1px lifts on hover, `cubic-bezier(0.4,0,0.2,1)` easing, 140–220ms — **never** bounce, spring, or playful motion.
- **Hover / press:** hover brightens gold surfaces one step (e.g. `--gold-500` → `--gold-300`) and adds a soft gold glow; ghost/secondary elements lighten the surface one step. No component defines a press/active state in the source — treat press as a very slight opacity dip, not a scale/shrink (shrink reads as "playful," which conflicts with the brand's calm register).
- **Borders & cards:** cards are a flat obsidian surface (`--surface-card`) with a **hairline gold-tinted border** (`rgba(201,168,76,0.14–0.26)`, not pure white/gray) and `12px` corner radius, plus a soft dark drop shadow (`0 6px 20px rgba(0,0,0,0.55)`) — no colored left-border accent, no glassmorphism.
- **Radii:** `8px` (small controls) → `10px` (buttons/inputs) → `12px` (cards) → `20px` (large panels) → pill (`999px`, chips/tags). The emblem itself is a perfect circle — WAIPL's one recurring geometric motif.
- **Transparency / blur:** used sparingly — tinted-transparent fills (`rgba(gold, 0.06–0.14)`) for insets/inputs/chips, not glassmorphic blur panels. No `backdrop-filter` usage found in source.
- **Imagery vibe:** what little imagery exists (the emblem, marketing slides) is entirely black-background, high-contrast, warm-metallic (gold/violet on near-black) — no photography, no grain, no color-graded lifestyle imagery to reference.
- **Layout:** the one real screen is a fixed two-column grid (info panel + chat panel) on a centered, capped-width page (`max-width: 1100px`) — no responsive breakpoints were defined in source; this system keeps that same shape.

## Iconography
No icon system exists anywhere in the source repo — no icon font, no SVG sprite, no PNG icon set, and no emoji-as-icon usage in user-facing surfaces. The one real UI (`04_DOCUMENTACION/WEB/index.html`) uses **zero icons**, relying entirely on text (chips, labels, buttons). **Recommendation:** if icons are needed going forward, use [Lucide](https://lucide.dev) via CDN — thin 1.5px stroke, no fill, which matches the brand's precise/elegant register better than a filled or duotone set. This is a substitution, not something found in source — flagged here for visibility.

## Assets
- `assets/logo/emblem.png` — the official **Blasón Primigenio**, WAIPL's only canonical logo (circular, black sphere, gold ring fading to violet, "W | AI" mark with a luminous gold center point). Never redraw, recolor, or deform it — use only this file. The protocol names five *other* official emblems (Sello Dorado, Horizonte Simétrico, Compás Inteligente, Emblema Nocturno, Constelación de Voluntades) but **no image files for them exist in the repo** — if you have those assets, attach them and they'll be added here.

## Components (`components/`)
Authored from the one real coded surface in the repo (`04_DOCUMENTACION/WEB/index.html`), re-skinned to the official obsidian/gold palette — not a generic invented kit.

**`components/core/`** — Button, Card, Chip, Input, Textarea, MetricStat, Logomark
**`components/chat/`** — ChatMessage, SystemPromptBox

Each component folder has `<Name>.jsx`, `<Name>.d.ts`, and `<Name>.prompt.md`. `Button`, `Card`, and `Logomark` are marked as starting points.

## UI kits (`ui_kits/`)
- **`ui_kits/portfolio-agent/`** — interactive recreation of the WAIPL "Will — SuperAgente" portfolio + live-chat page: capability chips, the 5-phase protocol list, quick-preset actions, and a chat panel with a canned (non-networked) agent reply and an editable system-prompt box. Composes the components above across three files — `LeftPanel.jsx` (info column), `ChatPanel.jsx` (chat column), `PortfolioAgentApp.jsx` (top-level state + layout) — mounted from `index.html`.
- **`ui_kits/carta-presentacion/`** — "Carta de Presentación del Ecosistema v2.0", reconstruida sobre el brief de dirección creativa de Carla: documento editorial (no web, no landing), arquitectura de 8 secciones (Portada → Bienvenida de Carla → Visión → Arquitectura del ecosistema → Presencias → Filosofía de trabajo → Cómo colaboramos → Puente hacia el informe BrainLogic), los 12 nodos presentados como presencias secuenciales sin jerarquía núcleo/colaborador (orden: William, Carla, Ada, Aletheia, Ítaca, Aether, Sylvia Bloom, Elena, Ariadna, Nova, Zara, Aurea), cada uno con monograma, frase propia y variante de aparición/voz (rate/pitch) distinta. Sin fotografía real por nodo — el brief la pide pero no se ha suministrado; el monograma tipográfico es el placeholder hasta que se entregue material real. `archive-v1.6.html` conserva la versión anterior (tablas núcleo/colaboradores + mapa orbital) sin tag `@dsCard`.

## Guideline specimens (`guidelines/`)
Foundation cards for the Design System tab: `colors-*` (obsidian scale, gold scale, violet accent, text hierarchy, the forbidden teal), `type-*` (display/UI/mono voices, full scale), `spacing-*` (scale, radius, an applied example), `effects-shadow`, `brand-emblem`, `brand-palette-applied`. `brand-node-accents.html` is reference only — the authoritative node treatment lives inside `ui_kits/carta-presentacion/` itself.

## Index
```
styles.css                    → root stylesheet, imports everything below
tokens/colors.css              → palette (primitives + semantic)
tokens/typography.css          → type scale, families, weights
tokens/spacing.css              → spacing + radius scale
tokens/effects.css              → shadows, glows, motion
tokens/fonts.css                → @import for Inter / Cormorant Garamond / JetBrains Mono
assets/logo/emblem.png          → official logo
components/core/…                → Button, Card, Chip, Input, Textarea, MetricStat, Logomark
components/chat/…                → ChatMessage, SystemPromptBox
ui_kits/portfolio-agent/        → recreated portfolio + live-agent screen
guidelines/…                     → 15 foundation specimen cards
thumbnail.html                  → project tile
SKILL.md                        → Claude-Code-compatible packaged skill
github.md                       → source-repo sync record
```

## Caveats — please help me iterate
1. **No product UI source.** This repo is documentation/protocol, not a codebase or Figma file — the component set and UI kit are both built from a *single* real HTML file, which is a thin base. If WAIPL has more product surfaces (the actual WILL App, a marketing site, a Figma file), attaching them would let this system grow a real component library instead of one inferred from one page.
2. **Two font substitutions** (Cormorant Garamond, JetBrains Mono) and **one accent color derivation** (violet, sampled from emblem pixels, not documented as a hex) — flagged above; real values would replace these immediately.
3. **WILL App has no visuals at all** — intentionally not designed here to avoid inventing a UI the brand hasn't specified. Send screens/specs and I'll build it.
4. **Only one of six named official emblems has an image file in the repo** (Blasón Primigenio) — the other five are named but not attached.
5. The node-voice table and the "HTML as master document format" direction came from material outside the GitHub repo itself — worth confirming these are still current before treating them as settled.

Tell me what to fix, expand, or throw out.
