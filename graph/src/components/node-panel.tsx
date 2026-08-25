import { useEffect, useState } from "react";
import { Volume2, VolumeX, X } from "lucide-react";
import { Holo, HoloButton, SectionLabel } from "@/components/holo";
import { degreeOf, neighborsOf, NODE_MAP, TYPE_LABEL, TYPE_TINT } from "@/lib/graph-data";
import { useEco } from "@/lib/store";

export function NodePanel() {
  const selectedId = useEco((s) => s.selectedId);
  const select = useEco((s) => s.select);
  const node = selectedId ? NODE_MAP[selectedId] : null;
  const [openMore, setOpenMore] = useState(false);
  const [speaking, setSpeaking] = useState(false);

  useEffect(() => {
    setOpenMore(false);
    window.speechSynthesis?.cancel();
    setSpeaking(false);
  }, [selectedId]);

  useEffect(() => {
    return () => window.speechSynthesis?.cancel();
  }, []);

  if (!node) return null;

  const degree = degreeOf(node.id);
  const neighbors = neighborsOf(node.id);
  const tint = TYPE_TINT[node.type];

  const speak = () => {
    const synth = window.speechSynthesis;
    if (!synth) return;
    if (speaking) {
      synth.cancel();
      setSpeaking(false);
      return;
    }
    const text = [
      node.name,
      TYPE_LABEL[node.type],
      `Comunidad ${node.community}`,
      node.summary,
      openMore ? node.body : "",
    ]
      .filter(Boolean)
      .join(". ");
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "es-ES";
    utterance.rate = 0.94;
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    setSpeaking(true);
    synth.speak(utterance);
  };

  return (
    <Holo
      strong
      data-testid="galleta"
      className="pointer-events-auto absolute inset-x-3 bottom-32 z-40 max-h-[46dvh] w-auto overflow-hidden p-4 md:inset-x-auto md:bottom-8 md:right-24 md:w-[22rem]"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <SectionLabel>Información del nodo</SectionLabel>
          <h2 className="mt-1 text-lg font-medium leading-tight text-ink">{node.name}</h2>
        </div>
        <button
          type="button"
          aria-label="Cerrar ficha"
          onClick={() => select(null)}
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-md text-muted hover:text-ink"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      <dl className="mt-3 grid grid-cols-[7.5rem_1fr] gap-x-3 gap-y-1.5 text-sm">
        <dt className="text-muted">Tipo</dt>
        <dd className="flex items-center gap-2 font-medium text-ink">
          <span className="inline-block h-2 w-2 rounded-full" style={{ background: tint }} />
          {TYPE_LABEL[node.type]}
        </dd>
        <dt className="text-muted">Comunidad</dt>
        <dd className="text-ink">{node.community}</dd>
        <dt className="text-muted">Fuente</dt>
        <dd className="text-ink">{node.source}</dd>
        <dt className="text-muted">Grado</dt>
        <dd className="text-ink">{degree}</dd>
      </dl>

      <p className="mt-3 text-sm leading-relaxed text-ink/80">{node.summary}</p>
      {openMore ? <p className="mt-2 text-sm leading-relaxed text-muted">{node.body}</p> : null}

      <div className="mt-3">
        <SectionLabel>Vecinos</SectionLabel>
        <ul className="mt-2 flex flex-col gap-1">
          {neighbors.map((n) => (
            <li key={n.id}>
              <button
                type="button"
                onClick={() => select(n.id)}
                className="flex min-h-11 w-full items-center gap-2 rounded-md px-2 text-left text-sm text-ink hover:bg-fog/60"
              >
                <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: n.color }} />
                <span className="truncate">{n.name}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        <HoloButton onClick={speak} className="min-h-11 flex-1 text-sm">
          {speaking ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
          {speaking ? "Silenciar" : "Leer en voz alta"}
        </HoloButton>
        <HoloButton onClick={() => setOpenMore((v) => !v)} className="min-h-11 text-sm">
          {openMore ? "Ocultar" : "Leer más"}
        </HoloButton>
      </div>
    </Holo>
  );
}
