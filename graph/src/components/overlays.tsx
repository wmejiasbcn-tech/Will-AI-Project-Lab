import type { ReactNode } from "react";
import { useEffect, useRef, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Eye, EyeOff, RotateCcw, Sparkles, Volume2, VolumeX } from "lucide-react";
import { Holo, HoloButton, SectionLabel } from "@/components/holo";
import { GlossaryButton } from "@/components/glossary-panel";
import { NodePanel } from "@/components/node-panel";
import { SafeBoundary } from "@/components/safe-boundary";
import { Term } from "@/components/term";
import {
  ACTIVITY,
  COMMUNITIES,
  degreeOf,
  EDGES,
  NODES,
  TYPE_LABEL,
  TYPE_TINT,
  type NodeType,
} from "@/lib/graph-data";
import { TYPE_HINT } from "@/lib/glossary";
import { APEX_URL } from "@/lib/hosts";
import { useEco } from "@/lib/store";
import { cn } from "@/lib/cn";

const TYPES: NodeType[] = [
  "nucleo",
  "laboratorio",
  "agente",
  "protocolo",
  "documento",
  "comunidad",
  "flujo",
  "accion",
];

const GALLERY = [
  { src: "/stills/swirl.jpg", title: "Portada", caption: "El umbral, antes de entrar", action: "portal" as const, term: "portada" },
  { src: "/stills/ribbons.jpg", title: "Flujos", caption: "Cintas que recorren el territorio", action: "mapa" as const, term: "flujo" },
  { src: "/stills/graphy.jpg", title: "Mapa Graphy", caption: "El grafo tocable", action: "mapa" as const, term: "graphy" },
  { src: "/stills/explorer.jpg", title: "Análisis", caption: "El pulso del ecosistema", action: "analisis" as const, term: "explorador" },
];

const tooltipStyle = {
  background: "color-mix(in oklab, white 72%, transparent)",
  border: "1px solid color-mix(in oklab, white 58%, transparent)",
  borderRadius: 12,
  fontSize: 12,
  color: "#2c3040",
};

function ChartBox({ className, children }: { className: string; children: ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const sync = () => {
      const r = el.getBoundingClientRect();
      setReady(r.width > 16 && r.height > 16);
    };
    sync();
    const ro = new ResizeObserver(sync);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return (
    <div ref={ref} className={className}>
      {ready ? (
        <SafeBoundary fallback={null}>
          <ResponsiveContainer width="100%" height="100%" minWidth={16} minHeight={16} debounce={50}>
            {children as never}
          </ResponsiveContainer>
        </SafeBoundary>
      ) : null}
    </div>
  );
}

function PanelFrame({ children }: { children: ReactNode }) {
  return (
    <div className="pointer-events-auto absolute inset-x-3 top-20 bottom-32 z-30 md:inset-x-auto md:left-4 md:top-24 md:bottom-6 md:w-full md:max-w-md">
      <div className="hud-scroll h-full pr-1">{children}</div>
    </div>
  );
}

export function InicioOverlay() {
  const setView = useEco((s) => s.setView);
  const replayPortal = useEco((s) => s.replayPortal);
  const openGlossary = useEco((s) => s.openGlossary);
  const last = ACTIVITY[ACTIVITY.length - 1];

  return (
    <PanelFrame>
      <div className="stagger-in flex flex-col gap-3 pb-2">
        <Holo strong className="p-5">
          <SectionLabel>Explorador Inmersivo</SectionLabel>
          <h2 className="mt-1 text-2xl font-light tracking-tight text-ink">El grafo está despierto</h2>
          <p className="mt-2 text-sm leading-relaxed text-muted">
            Esto es un{" "}
            <Term id="grafo" className="text-muted">
              grafo vivo
            </Term>
            : cada esfera es un{" "}
            <Term id="nodo" className="text-muted">
              nodo
            </Term>
            , cada hilo una relación. La{" "}
            <Term id="portada" className="text-muted">
              portada
            </Term>{" "}
            es el umbral. El{" "}
            <Term id="graphy" className="text-muted">
              Mapa Graphy
            </Term>{" "}
            se toca y se orbita. Las palabras subrayadas abren el glosario.
          </p>
          <div className="mt-4 grid grid-cols-3 gap-2">
            <Stat k="Nodos" v={String(NODES.length)} />
            <Stat k="Vínculos" v={String(EDGES.length)} />
            <Stat k="Flujos" v={String(last.flujos)} />
          </div>
        </Holo>

        <Holo className="p-4">
          <SectionLabel>Flujos activos</SectionLabel>
          <ChartBox className="mt-2 h-36">
            <AreaChart data={ACTIVITY} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="rgba(44,48,64,0.08)" vertical={false} />
              <XAxis dataKey="mes" tick={{ fill: "#6a6e80", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis width={28} tick={{ fill: "#6a6e80", fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Area type="monotone" dataKey="flujos" stroke="#7ec8d4" fill="#7ec8d4" fillOpacity={0.28} />
              <Area type="monotone" dataKey="nodos" stroke="#c9a45c" fill="#c9a45c" fillOpacity={0.18} />
            </AreaChart>
          </ChartBox>
        </Holo>

        <div className="grid grid-cols-2 gap-2">
          {GALLERY.map((g) => (
            <button
              key={g.src}
              type="button"
              onClick={() => {
                if (g.action === "portal") replayPortal();
                else setView(g.action);
              }}
              className="holo overflow-hidden rounded-xl text-left"
            >
              <img src={g.src} alt={g.title} className="h-24 w-full object-cover" />
              <span className="block px-3 py-2">
                <span className="block text-sm font-medium text-ink">{g.title}</span>
                <span className="block text-xs text-muted">{g.caption}</span>
                <span
                  className="mt-1 inline-block text-[11px] text-gold underline decoration-dotted"
                  onClick={(e) => {
                    e.stopPropagation();
                    openGlossary(g.term);
                  }}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.stopPropagation();
                      openGlossary(g.term);
                    }
                  }}
                  role="link"
                  tabIndex={0}
                >
                  ¿Qué es esto?
                </span>
              </span>
            </button>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-2">
          <HoloButton className="min-h-12" onClick={() => setView("mapa")}>
            <Sparkles className="h-4 w-4" />
            Abrir mapa
          </HoloButton>
          <GlossaryButton className="min-h-12" />
        </div>
      </div>
    </PanelFrame>
  );
}

function Stat({ k, v }: { k: string; v: string }) {
  return (
    <div className="holo-quiet rounded-md px-3 py-2">
      <p className="text-xs uppercase tracking-wider text-muted">{k}</p>
      <p className="text-xl font-medium text-ink">{v}</p>
    </div>
  );
}

export function MapaChrome() {
  const query = useEco((s) => s.query);
  const setQuery = useEco((s) => s.setQuery);
  const typeFilter = useEco((s) => s.typeFilter);
  const setTypeFilter = useEco((s) => s.setTypeFilter);
  const select = useEco((s) => s.select);
  const selectedId = useEco((s) => s.selectedId);
  const [chipHint, setChipHint] = useState<string | null>(null);

  const q = query.trim().toLowerCase();
  const hits = NODES.filter((n) => {
    const byQuery =
      !q ||
      n.name.toLowerCase().includes(q) ||
      n.community.toLowerCase().includes(q) ||
      TYPE_LABEL[n.type].toLowerCase().includes(q);
    const byType = typeFilter === "all" || n.type === typeFilter;
    return byQuery && byType;
  }).slice(0, 8);

  const openType = (t: NodeType | "all") => {
    setTypeFilter(t);
    if (t === "all") {
      select(null);
      return;
    }
    const first = NODES.find((n) => n.type === t);
    if (first) select(first.id);
  };

  return (
    <>
      <div className="pointer-events-auto absolute inset-x-3 top-20 z-30 md:inset-x-auto md:left-4 md:top-24 md:w-[22rem]">
        <Holo strong className="p-3">
          <label className="sr-only" htmlFor="grafo-buscar">
            Buscar nodo
          </label>
          <input
            id="grafo-buscar"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar nodo o comunidad…"
            className="h-11 w-full rounded-md bg-fog/70 px-3 text-sm text-ink outline-none placeholder:text-muted"
          />
          <div className="mt-2 flex flex-wrap gap-1.5">
            <FilterChip
              label="Todos"
              active={typeFilter === "all"}
              hint="Ver todos los nodos"
              onEnter={() => setChipHint("Ver todos los nodos")}
              onLeave={() => setChipHint(null)}
              onClick={() => openType("all")}
            />
            {TYPES.map((t) => (
              <FilterChip
                key={t}
                label={TYPE_LABEL[t]}
                tint={TYPE_TINT[t]}
                active={typeFilter === t}
                hint={TYPE_HINT[t]}
                testId={`chip-${t}`}
                onEnter={() => setChipHint(TYPE_HINT[t] ?? TYPE_LABEL[t])}
                onLeave={() => setChipHint(null)}
                onClick={() => openType(t)}
              />
            ))}
          </div>
          <p className="mt-2 px-1 text-xs leading-relaxed text-muted">
            {chipHint ?? "Pasa el puntero por un tipo. Tócalo para abrir su ficha."}
          </p>
          {typeFilter !== "all" || q ? (
            <ul className="mt-2 flex flex-col">
              {hits.length === 0 ? (
                <li className="px-1 py-2 text-sm text-muted">Ningún nodo coincide.</li>
              ) : (
                hits.map((n) => (
                  <li key={n.id}>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        select(n.id);
                      }}
                      className={cn(
                        "flex min-h-11 w-full items-center gap-2 rounded-md px-2 text-left text-sm",
                        selectedId === n.id ? "bg-fog" : "hover:bg-fog/70",
                      )}
                    >
                      <span className="h-2 w-2 rounded-full" style={{ background: n.color }} />
                      {n.name}
                    </button>
                  </li>
                ))
              )}
            </ul>
          ) : null}
        </Holo>
        <p className="mt-2 hidden px-2 text-xs text-muted md:block">
          Arrastra para orbitar · el nombre aparece al pasar el puntero
        </p>
      </div>
      <NodePanel />
    </>
  );
}

function FilterChip({
  label,
  active,
  onClick,
  tint,
  hint,
  testId,
  onEnter,
  onLeave,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
  tint?: string;
  hint?: string;
  testId?: string;
  onEnter?: () => void;
  onLeave?: () => void;
}) {
  return (
    <button
      type="button"
      data-testid={testId}
      title={hint}
      aria-label={hint ? `${label}. ${hint}` : label}
      onPointerEnter={onEnter}
      onPointerLeave={onLeave}
      onClick={(e) => {
        e.stopPropagation();
        onClick();
      }}
      className={cn(
        "inline-flex min-h-11 items-center gap-1.5 rounded-full px-3 text-xs font-medium",
        active ? "holo-strong text-ink" : "holo-quiet text-muted",
      )}
    >
      {tint ? <span className="h-1.5 w-1.5 rounded-full" style={{ background: tint }} /> : null}
      {label}
    </button>
  );
}

export function AnalisisOverlay() {
  const select = useEco((s) => s.select);
  const ranked = [...NODES]
    .map((n) => ({ ...n, degree: degreeOf(n.id) }))
    .sort((a, b) => b.degree - a.degree)
    .slice(0, 8);

  const byType = TYPES.map((t) => ({
    tipo: TYPE_LABEL[t],
    n: NODES.filter((x) => x.type === t).length,
    fill: TYPE_TINT[t],
  }));

  const byCommunity = COMMUNITIES.map((c) => ({
    name: c,
    n: NODES.filter((x) => x.community === c).length,
  }));

  return (
    <PanelFrame>
      <div className="stagger-in flex flex-col gap-3 pb-2">
        <Holo strong className="p-5">
          <SectionLabel>Análisis</SectionLabel>
          <h2 className="mt-1 text-2xl font-light tracking-tight text-ink">Nodos y flujos</h2>
          <p className="mt-2 text-sm leading-relaxed text-muted">
            Lectura temporal del ecosistema. El mapa muestra la geometría; aquí, el pulso.
          </p>
        </Holo>

        <Holo className="p-4">
          <SectionLabel>Serie anual</SectionLabel>
          <ChartBox className="mt-2 h-40">
            <BarChart data={ACTIVITY} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="rgba(44,48,64,0.08)" vertical={false} />
              <XAxis dataKey="mes" tick={{ fill: "#6a6e80", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis width={28} tick={{ fill: "#6a6e80", fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="nodos" fill="#c9a45c" radius={[6, 6, 0, 0]} />
              <Bar dataKey="flujos" fill="#7ec8d4" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ChartBox>
        </Holo>

        <Holo className="p-4">
          <SectionLabel>Por tipo</SectionLabel>
          <ul className="mt-3 flex flex-col gap-2">
            {byType.map((t) => (
              <li key={t.tipo} className="flex items-center gap-3 text-sm">
                <span className="w-28 shrink-0 text-muted">{t.tipo}</span>
                <span className="h-2 flex-1 overflow-hidden rounded-full bg-fog">
                  <span
                    className="block h-full rounded-full"
                    style={{ width: `${(t.n / NODES.length) * 100}%`, background: t.fill }}
                  />
                </span>
                <span className="w-6 text-right text-ink">{t.n}</span>
              </li>
            ))}
          </ul>
        </Holo>

        <Holo className="p-4">
          <SectionLabel>Comunidades</SectionLabel>
          <ul className="mt-3 grid grid-cols-2 gap-2">
            {byCommunity.map((c) => (
              <li key={c.name} className="holo-quiet rounded-md px-3 py-2">
                <p className="text-xs text-muted">{c.name}</p>
                <p className="text-lg font-medium text-ink">{c.n}</p>
              </li>
            ))}
          </ul>
        </Holo>

        <Holo className="p-4">
          <SectionLabel>Mayor grado</SectionLabel>
          <ol className="mt-2 flex flex-col">
            {ranked.map((n) => (
              <li key={n.id}>
                <button
                  type="button"
                  onClick={() => select(n.id)}
                  className="flex min-h-11 w-full items-center justify-between gap-2 rounded-md px-1 text-left text-sm hover:bg-fog/60"
                >
                  <span className="flex items-center gap-2 truncate">
                    <span className="h-2 w-2 rounded-full" style={{ background: n.color }} />
                    {n.name}
                  </span>
                  <span className="text-muted">{n.degree}</span>
                </button>
              </li>
            ))}
          </ol>
        </Holo>
      </div>
    </PanelFrame>
  );
}

export function ConfigOverlay() {
  const autoRotate = useEco((s) => s.autoRotate);
  const showLabels = useEco((s) => s.showLabels);
  const reduceMotion = useEco((s) => s.reduceMotion);
  const quality = useEco((s) => s.quality);
  const toggleAutoRotate = useEco((s) => s.toggleAutoRotate);
  const toggleLabels = useEco((s) => s.toggleLabels);
  const toggleMotion = useEco((s) => s.toggleMotion);
  const setQuality = useEco((s) => s.setQuality);
  const replayPortal = useEco((s) => s.replayPortal);
  const setQuery = useEco((s) => s.setQuery);
  const setTypeFilter = useEco((s) => s.setTypeFilter);
  const select = useEco((s) => s.select);
  const sound = useEco((s) => s.sound);
  const toggleSound = useEco((s) => s.toggleSound);

  return (
    <PanelFrame>
      <div className="stagger-in flex flex-col gap-3 pb-2">
        <Holo strong className="p-5">
          <SectionLabel>Configuración</SectionLabel>
          <h2 className="mt-1 text-2xl font-light tracking-tight text-ink">Preferencias de órbita</h2>
          <p className="mt-2 text-sm leading-relaxed text-muted">
            Ajusta el render, el movimiento y las etiquetas. Los cambios se guardan en este dispositivo.
          </p>
        </Holo>

        <Holo className="divide-y divide-ink/10 p-2">
          <ToggleRow
            label="Rotación automática"
            hint="El grafo orbita cuando no hay nodo seleccionado"
            on={autoRotate}
            onClick={toggleAutoRotate}
          />
          <ToggleRow
            label="Etiquetas"
            hint="Nombres sobre el núcleo y los nodos mayores"
            on={showLabels}
            icon={showLabels ? Eye : EyeOff}
            onClick={toggleLabels}
          />
          <ToggleRow
            label="Reducir movimiento"
            hint="Detiene pulsos, auto-órbita y el bucle continuo"
            on={reduceMotion}
            onClick={toggleMotion}
          />
          <ToggleRow
            label="Ambiente"
            hint="Capa sonora etérea de las cinemáticas originales"
            on={sound}
            icon={sound ? Volume2 : VolumeX}
            onClick={toggleSound}
          />
        </Holo>

        <Holo className="p-4">
          <SectionLabel>Calidad de render</SectionLabel>
          <div className="mt-3 grid grid-cols-2 gap-2">
            <HoloButton active={quality === "alta"} onClick={() => setQuality("alta")} className="min-h-11">
              Alta
            </HoloButton>
            <HoloButton active={quality === "media"} onClick={() => setQuality("media")} className="min-h-11">
              Media
            </HoloButton>
          </div>
        </Holo>

        <div className="grid grid-cols-1 gap-2">
          <GlossaryButton className="min-h-12" />
          <HoloButton
            className="min-h-12"
            onClick={() => {
              setQuery("");
              setTypeFilter("all");
              select(null);
            }}
          >
            Restablecer filtros
          </HoloButton>
          <HoloButton className="min-h-12" onClick={replayPortal}>
            <RotateCcw className="h-4 w-4" />
            Volver a la portada
          </HoloButton>
        </div>

        <Holo quiet className="p-4">
          <p className="text-sm leading-relaxed text-muted">
            WAIPL Graph es una obra inmersiva de Will-AI Project Lab. El umbral público es{" "}
            <a href={APEX_URL} className="text-gold underline-offset-2 hover:underline">
              waipl.dev
            </a>
            ; este explorador es el territorio Graphy.
            Las palabras subrayadas abren el glosario.
          </p>
        </Holo>
      </div>
    </PanelFrame>
  );
}

function ToggleRow({
  label,
  hint,
  on,
  onClick,
  icon: Icon,
}: {
  label: string;
  hint: string;
  on: boolean;
  onClick: () => void;
  icon?: typeof Eye;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex min-h-14 w-full items-center justify-between gap-3 px-3 py-2 text-left"
    >
      <span>
        <span className="flex items-center gap-2 text-sm font-medium text-ink">
          {Icon ? <Icon className="h-4 w-4" /> : null}
          {label}
        </span>
        <span className="mt-0.5 block text-xs text-muted">{hint}</span>
      </span>
      <span
        className={cn(
          "relative h-7 w-12 shrink-0 rounded-full transition-colors",
          on ? "bg-gold/80" : "bg-ink/15",
        )}
      >
        <span
          className={cn(
            "absolute top-0.5 h-6 w-6 rounded-full bg-fog shadow-sm transition-transform",
            on ? "translate-x-5" : "translate-x-0.5",
          )}
        />
      </span>
    </button>
  );
}
