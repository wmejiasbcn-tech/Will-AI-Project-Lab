import { ChevronLeft, ChevronRight } from "lucide-react";
import { useEco } from "@/lib/store";
import { cn } from "@/lib/cn";

export function HistoryNav({ light = false }: { light?: boolean }) {
  const cursor = useEco((s) => s.cursor);
  const stackLen = useEco((s) => s.stack.length);
  const goBack = useEco((s) => s.goBack);
  const goForward = useEco((s) => s.goForward);
  const canBack = cursor > 0;
  const canForward = cursor < stackLen - 1;
  const tone = light ? "text-ivory/80 hover:text-ivory" : "text-ink hover:text-ink";
  const mute = light ? "text-ivory/25" : "text-muted/40";

  return (
    <div className="flex shrink-0 items-center">
      <button
        type="button"
        data-testid="atras"
        aria-label="Pantalla anterior"
        disabled={!canBack}
        onClick={goBack}
        className={cn(
          "flex h-11 w-11 items-center justify-center rounded-md transition-transform duration-150 ease-out active:scale-[0.96]",
          canBack ? tone : mute,
        )}
      >
        <ChevronLeft className="h-5 w-5" />
      </button>
      <button
        type="button"
        data-testid="adelante"
        aria-label="Pantalla siguiente"
        disabled={!canForward}
        onClick={goForward}
        className={cn(
          "flex h-11 w-11 items-center justify-center rounded-md transition-transform duration-150 ease-out active:scale-[0.96]",
          canForward ? tone : mute,
        )}
      >
        <ChevronRight className="h-5 w-5" />
      </button>
    </div>
  );
}
