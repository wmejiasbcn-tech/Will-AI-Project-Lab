import { useEffect, useState } from "react";
import { Ambient } from "@/components/ambient";
import { GlossaryPanel } from "@/components/glossary-panel";
import { GraphStage } from "@/components/graph-stage";
import { PortalView } from "@/components/portal-view";
import { SafeBoundary } from "@/components/safe-boundary";
import { Shell } from "@/components/shell";
import { useEco } from "@/lib/store";
import { cn } from "@/lib/cn";

export function EcoApp() {
  const entered = useEco((s) => s.entered);
  const view = useEco((s) => s.view);
  const cursor = useEco((s) => s.cursor);
  const stackLen = useEco((s) => s.stack.length);
  const [worldOn, setWorldOn] = useState(false);
  const [portalGone, setPortalGone] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setReady(true);
    void useEco.persist.rehydrate();
  }, []);

  useEffect(() => {
    if (entered) {
      setWorldOn(true);
      const t = window.setTimeout(() => setPortalGone(true), 720);
      return () => window.clearTimeout(t);
    }
    setPortalGone(false);
    setWorldOn(false);
  }, [entered]);

  return (
    <div
      className="relative h-dvh w-full overflow-hidden bg-mist"
      data-ready={ready ? "true" : "false"}
      data-entered={entered ? "1" : "0"}
      data-view={view}
      data-cursor={cursor}
      data-stack={stackLen}
    >
      <Ambient />
      {worldOn ? (
        <div className="absolute inset-0 z-0">
          <SafeBoundary
            fallback={
              <img
                src="/stills/city-wide.jpg"
                alt=""
                className="h-full w-full object-cover opacity-80"
              />
            }
          >
            <GraphStage interactive={entered} />
          </SafeBoundary>
        </div>
      ) : null}

      {portalGone ? null : (
        <div
          className={cn(
            "absolute inset-0 z-20 transition-opacity duration-700 ease-out-soft motion-reduce:duration-0",
            entered ? "pointer-events-none opacity-0" : "pointer-events-auto opacity-100",
          )}
        >
          <PortalView />
        </div>
      )}

      {entered ? (
        <SafeBoundary fallback={null}>
          <Shell />
        </SafeBoundary>
      ) : (
        <div className="pointer-events-none absolute inset-0 z-40">
          <GlossaryPanel />
        </div>
      )}
    </div>
  );
}
