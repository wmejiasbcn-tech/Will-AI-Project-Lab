import { useEffect, useState, type ComponentType } from "react";
import { SafeBoundary } from "@/components/safe-boundary";

type GraphCanvasProps = { interactive: boolean; onFail?: () => void };

function StageFallback() {
  return (
    <div className="relative h-full w-full overflow-hidden bg-mist">
      <img
        src="/stills/city-wide.jpg"
        alt=""
        className="h-full w-full object-cover opacity-80"
      />
    </div>
  );
}

export function GraphStage({ interactive }: { interactive: boolean }) {
  const [Canvas, setCanvas] = useState<ComponentType<GraphCanvasProps> | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let alive = true;
    import("./graph-canvas")
      .then((m) => {
        if (alive) setCanvas(() => m.GraphCanvas);
      })
      .catch(() => {
        if (alive) setFailed(true);
      });
    return () => {
      alive = false;
    };
  }, []);

  if (failed) return <StageFallback />;
  if (!Canvas) return <StageFallback />;
  return (
    <SafeBoundary fallback={<StageFallback />}>
      <Canvas interactive={interactive} onFail={() => setFailed(true)} />
    </SafeBoundary>
  );
}
