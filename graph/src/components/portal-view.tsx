import { Seal } from "@/components/seal";
import { HoloButton } from "@/components/holo";
import { HistoryNav } from "@/components/history-nav";
import { SoundToggle } from "@/components/ambient";
import { Term } from "@/components/term";
import { useEco } from "@/lib/store";

const VERBS = [
  { id: "explorar", label: "Explorar", view: "mapa" as const, selectedId: null },
  { id: "conectar", label: "Conectar", view: "mapa" as const, selectedId: "will-ai" },
  { id: "crear", label: "Crear", view: "mapa" as const, selectedId: "laboratorio" },
  { id: "analizar", label: "Analizar", view: "analisis" as const, selectedId: null },
] as const;

export function PortalView() {
  const enter = useEco((s) => s.enter);
  const entered = useEco((s) => s.entered);
  const cursor = useEco((s) => s.cursor);
  const stackLen = useEco((s) => s.stack.length);
  const showHistory = !entered && (cursor > 0 || cursor < stackLen - 1);

  return (
    <div className="absolute inset-0 z-20 flex flex-col overflow-hidden">
      <img
        src="/stills/city-wide.jpg"
        alt=""
        className="pointer-events-none absolute inset-0 h-full w-full object-cover opacity-55"
      />
      <img
        src="/stills/ribbons.jpg"
        alt=""
        className="pointer-events-none absolute inset-0 h-full w-full object-cover opacity-14"
      />
      <div className="pointer-events-none absolute inset-0 portal-tint" />
      <div className="pointer-events-none absolute inset-0 portal-veil" />

      {showHistory ? (
        <div className="pointer-events-auto absolute left-3 top-3 z-30 rounded-xl bg-void/70">
          <HistoryNav light />
        </div>
      ) : null}

      <div className="pointer-events-auto absolute right-3 top-3 z-30 rounded-xl bg-void/70">
        <SoundToggle light />
      </div>

      <div className="relative z-10 flex h-full flex-col items-center px-5 py-10 md:justify-center">
        <Seal />
        <p className="portal-copy mt-5 text-center text-xs font-medium uppercase tracking-[0.32em] text-gold">
          Will-AI · Project Lab
        </p>
        <h1 className="portal-copy mt-2 max-w-xl text-center text-3xl font-medium leading-[1.15] sm:text-5xl">
          Ecosistema Digital{" "}
          <Term id="inmersivo" className="portal-copy text-inherit">
            Inmersivo
          </Term>
        </h1>
        <p className="portal-copy mt-3 max-w-md text-center text-sm leading-relaxed sm:text-base">
          ¿Quieres una experiencia única? Entra al{" "}
          <Term id="grafo" className="portal-copy text-inherit">
            grafo vivo
          </Term>
          .
        </p>

        <div className="mt-auto flex w-full max-w-md flex-col items-center gap-4 md:mt-10">
          <HoloButton
            data-testid="entrar"
            onPointerDown={(e) => {
              e.stopPropagation();
              enter();
            }}
            onClick={() => enter()}
            active
            className="relative z-30 min-h-12 w-full max-w-xs px-8 text-base"
          >
            Entrar
          </HoloButton>
          <div className="relative z-30 flex flex-wrap justify-center gap-2">
            {VERBS.map((v) => (
              <HoloButton
                key={v.id}
                data-testid={v.id}
                className="min-h-11 px-4 text-sm"
                onPointerDown={(e) => {
                  e.stopPropagation();
                  enter({ view: v.view, selectedId: v.selectedId });
                }}
                onClick={() => enter({ view: v.view, selectedId: v.selectedId })}
              >
                {v.label}
              </HoloButton>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
