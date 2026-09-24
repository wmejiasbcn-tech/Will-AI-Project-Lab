import { useEffect } from "react";
import { BarChart3, ChevronRight, House, Map, Settings } from "lucide-react";
import { SoundToggle } from "@/components/ambient";
import { GlossaryPanel } from "@/components/glossary-panel";
import { AnalisisOverlay, ConfigOverlay, InicioOverlay, MapaChrome } from "@/components/overlays";
import { HistoryNav } from "@/components/history-nav";
import { type EcoView, useEco } from "@/lib/store";
import { cn } from "@/lib/cn";

const NAV: { id: EcoView; label: string; short: string; icon: typeof House }[] = [
  { id: "inicio", label: "Inicio", short: "Inicio", icon: House },
  { id: "mapa", label: "Mapas", short: "Mapas", icon: Map },
  { id: "analisis", label: "Análisis", short: "Análisis", icon: BarChart3 },
  { id: "config", label: "Configuración", short: "Ajustes", icon: Settings },
];

const TITLES: Record<EcoView, { kicker: string; title: string }> = {
  inicio: { kicker: "Will-AI", title: "Explorador Inmersivo" },
  mapa: { kicker: "Mapa Graphy", title: "WAIPL — GRAPH" },
  analisis: { kicker: "Telemetría", title: "Análisis de flujos" },
  config: { kicker: "Sistema", title: "Configuración" },
};

export function Shell() {
  const view = useEco((s) => s.view);
  const setView = useEco((s) => s.setView);
  const select = useEco((s) => s.select);
  const goBack = useEco((s) => s.goBack);
  const goForward = useEco((s) => s.goForward);
  const selectedId = useEco((s) => s.selectedId);
  const glossaryId = useEco((s) => s.glossaryId);
  const closeGlossary = useEco((s) => s.closeGlossary);
  const openGlossary = useEco((s) => s.openGlossary);
  const title = TITLES[view];

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        if (glossaryId) {
          closeGlossary();
          return;
        }
        if (selectedId) select(null);
        else goBack();
        return;
      }
      if (e.altKey && e.key === "ArrowLeft") {
        e.preventDefault();
        goBack();
      }
      if (e.altKey && e.key === "ArrowRight") {
        e.preventDefault();
        goForward();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [select, selectedId, goBack, goForward, glossaryId, closeGlossary]);

  return (
    <div className="pointer-events-none absolute inset-0 z-30">
      <header className="pointer-events-auto absolute inset-x-3 top-3 z-40 flex items-center gap-3 md:inset-x-4 md:right-72">
        <div className="holo-strong flex min-h-14 flex-1 items-center gap-1 rounded-xl py-1 pr-1 pl-1">
          <HistoryNav />
          <button
            type="button"
            onClick={() =>
              openGlossary(
                view === "mapa" ? "graphy" : view === "inicio" ? "explorador" : view === "analisis" ? "flujo" : "umbral",
              )
            }
            className="min-w-0 flex-1 text-left"
          >
            <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-muted">{title.kicker}</p>
            <h1 className="truncate text-lg font-light leading-tight text-ink sm:text-xl">{title.title}</h1>
          </button>
          <SoundToggle />
        </div>
      </header>

      <div className="pointer-events-auto absolute right-4 top-3 z-40 hidden flex-col items-end gap-3 md:flex">
        <nav className="holo w-56 rounded-xl p-2" aria-label="Explorador">
          {NAV.map((item) => {
            const Icon = item.icon;
            const active = view === item.id;
            return (
              <button
                key={item.id}
                type="button"
                data-active={active}
                data-nav={item.id}
                onClick={() => setView(item.id)}
                className="nav-item w-full text-sm"
              >
                <span className="flex items-center gap-2">
                  <Icon className="h-4 w-4" />
                  {item.label}
                </span>
                <ChevronRight className={cn("h-4 w-4 text-muted", active && "text-gold")} />
              </button>
            );
          })}
        </nav>
      </div>

      {view === "inicio" ? <InicioOverlay /> : null}
      {view === "mapa" ? <MapaChrome /> : null}
      {view === "analisis" ? <AnalisisOverlay /> : null}
      {view === "config" ? <ConfigOverlay /> : null}
      <GlossaryPanel />

      <nav
        className="pointer-events-auto absolute inset-x-3 bottom-10 z-40 flex h-16 items-stretch rounded-xl holo-strong md:hidden"
        aria-label="Explorador"
      >
        {NAV.map((item) => {
          const Icon = item.icon;
          const active = view === item.id;
          return (
            <button
              key={item.id}
              type="button"
              data-nav={item.id}
              onPointerDown={(e) => {
                e.stopPropagation();
                setView(item.id);
              }}
              onClick={() => setView(item.id)}
              className={cn(
                "flex flex-1 flex-col items-center justify-center gap-0.5 text-[11px]",
                active ? "text-ink" : "text-muted",
              )}
            >
              <Icon className={cn("h-5 w-5", active && "text-gold")} />
              {item.short}
            </button>
          );
        })}
      </nav>
    </div>
  );
}
