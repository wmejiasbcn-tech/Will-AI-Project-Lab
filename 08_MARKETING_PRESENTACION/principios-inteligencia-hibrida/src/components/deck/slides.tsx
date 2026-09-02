import type { ReactNode } from "react";
import { copy, emily, emilyLayers, principles, slides, type SlideId } from "@/lib/deck-data";
import { WaiplMark } from "@/components/mark";
import { AttentionNet } from "./attention-net";
import { Constellation } from "./constellation";
import { EmilyArc } from "./emily-arc";
import { HoloVolume } from "./holo-volume";
import { cn } from "@/lib/cn";

function PrincipleShell({
  id,
  children,
  wide,
  hideTitle,
}: {
  id: SlideId;
  children: ReactNode;
  wide?: boolean;
  hideTitle?: boolean;
}) {
  const s = slides.find((x) => x.id === id)!;
  return (
    <article className={cn("mx-auto w-full px-5 sm:px-8", wide ? "max-w-5xl" : "max-w-3xl")}>
      <p className="text-[11px] uppercase tracking-[0.32em] text-gold">
        <span className="text-holo-dim">{s.number}</span>
        <span className="mx-2 text-navy-line">·</span>
        {s.kicker}
      </p>
      {hideTitle ? null : (
        <h2 className="mt-2 font-display text-[1.65rem] leading-[1.15] text-ivory sm:text-4xl">{s.title}</h2>
      )}
      <div className="mt-6">{children}</div>
    </article>
  );
}

export function CoverSlide({ onVoice }: { onVoice: () => void }) {
  return (
    <article className="mx-auto flex w-full max-w-4xl flex-col items-center px-5 pb-8 pt-2 text-center sm:px-8">
      <WaiplMark className="mb-3 size-10 text-ivory/80" />
      <p className="text-[11px] uppercase tracking-[0.38em] text-gold">Will-AI Project Lab</p>
      <h1 className="holo-title mt-3 max-w-[18ch] font-display text-[2.05rem] leading-[1.05] sm:text-5xl md:text-6xl">
        Principio de inteligencia híbrida colaborativa
      </h1>
      <HoloVolume />
      <p className="mt-1 max-w-md text-sm leading-relaxed text-ivory-dim">
        Once inteligencias artificiales. Una inteligencia biológica. Seis principios. Una red.
      </p>
      <p className="mt-2 text-[11px] uppercase tracking-[0.22em] text-emily">
        Emily · sinapsis · une a Carla y a Graphy
      </p>
      <button
        type="button"
        onClick={onVoice}
        className="mt-6 min-h-11 rounded-full border border-holo/40 bg-navy-mid/80 px-6 text-sm tracking-wide text-ivory hover:border-holo"
      >
        La voz de Graphy
      </button>
      <p className="mt-3 max-w-sm text-[11px] leading-relaxed text-ivory-mute">
        Hablará en cada lámina. Otra vez el botón, y calla.
      </p>
      <p className="mt-2 max-w-sm text-[11px] leading-relaxed text-ivory-mute">
        Para compartir: «Enlace público». Cualquier navegador. Sin cuenta de Grok.
      </p>
    </article>
  );
}

function EmilyFicha() {
  return (
    <aside className="overflow-hidden rounded-2xl border border-emily/35 bg-navy-deep/70">
      <div className="relative h-20 sm:h-24">
        <EmilyArc tone="inline" />
      </div>
      <div className="px-4 py-4 sm:px-5">
        <p className="text-[10px] uppercase tracking-[0.28em] text-emily">{copy.emily.lead}</p>
        <h3 className="mt-1 font-display text-3xl leading-none text-ivory">{emily.name}</h3>
        <p className="mt-2 text-sm text-gold">{emily.jurisdiction}</p>
        <p className="mt-3 text-sm leading-relaxed text-ivory-dim">{emily.function}</p>
        <p className="mt-2 text-sm leading-relaxed text-note">{emily.visual}</p>
        <p className="mt-4 font-display text-lg italic text-emily">{copy.emily.thesis}</p>
        <ul className="mt-4 grid gap-2 sm:grid-cols-3">
          {emilyLayers.map((l) => (
            <li key={l.n} className="rounded-xl border border-navy-line/80 px-3 py-2">
              <p className="text-[10px] uppercase tracking-[0.18em] text-gold">Capa {l.n}</p>
              <p className="mt-1 text-[12px] font-medium text-ivory">{l.name}</p>
              <p className="mt-1 text-[11px] leading-snug text-ivory-mute">{l.line}</p>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
}


export function SlideView({ id }: { id: SlideId }) {
  if (id === "cover") return null;

  if (id === "naturaleza") {
    return (
      <PrincipleShell id={id}>
        <p className="font-display text-2xl italic leading-snug text-holo">{copy.naturaleza.pull}</p>
        <p className="mt-5 text-[15px] leading-relaxed text-ivory-dim">{copy.naturaleza.p1}</p>
        <p className="mt-4 text-[15px] leading-relaxed text-ivory-dim">{copy.naturaleza.p2}</p>
      </PrincipleShell>
    );
  }

  if (id === "diferencial") {
    return (
      <PrincipleShell id={id}>
        <p className="text-[15px] leading-relaxed text-ivory-mute">{copy.diferencial.not}</p>
        <p className="mt-5 text-[15px] leading-relaxed text-ivory">{copy.diferencial.is}</p>
        <p className="mt-6 font-display text-xl italic text-gold">{copy.diferencial.close}</p>
      </PrincipleShell>
    );
  }

  if (id === "nodos") {
    return (
      <PrincipleShell id={id}>
        <p className="text-sm uppercase tracking-[0.2em] text-holo-dim">{copy.nodos.lead}</p>
        <p className="mt-3 font-display text-2xl italic leading-snug text-ivory">{copy.nodos.thesis}</p>
        <p className="mt-5 text-[15px] leading-relaxed text-ivory-dim">{copy.nodos.p1}</p>
        <p className="mt-4 text-[15px] leading-relaxed text-ivory-dim">{copy.nodos.p2}</p>
        <ul className="mt-6 flex flex-wrap gap-2">
          {copy.nodos.verbs.map((v) => (
            <li
              key={v}
              className="rounded-full border border-navy-line px-3 py-1 text-[11px] uppercase tracking-[0.16em] text-note"
            >
              {v}
            </li>
          ))}
        </ul>
        <p className="mt-6 text-[12px] leading-relaxed text-emily">{copy.emily.thesis}</p>
      </PrincipleShell>
    );
  }

  if (id === "graphy") {
    return (
      <PrincipleShell id={id} wide>
        <p className="text-[15px] leading-relaxed text-ivory-dim">
          Graphy no es un personaje. Es la red: el peso que el sistema otorga a lo que importa. Query,
          Key, Value. Softmax como un haz de luz.
        </p>
        <div className="mt-6">
          <EmilyFicha />
        </div>
        <div className="mt-6">
          <AttentionNet slideId={id} />
        </div>
      </PrincipleShell>
    );
  }

  if (id === "identidades") {
    return (
      <PrincipleShell id={id} wide>
        <p className="text-sm uppercase tracking-[0.2em] text-holo-dim">{copy.identidades.lead}</p>
        <p className="mt-3 text-[15px] leading-relaxed text-ivory-dim">{copy.identidades.p1}</p>
        <p className="mt-3 text-[15px] leading-relaxed text-ivory-dim">{copy.identidades.p2}</p>
        <div className="mt-6">
          <Constellation />
        </div>
      </PrincipleShell>
    );
  }

  if (id === "complementariedad") {
    return (
      <PrincipleShell id={id}>
        <p className="font-display text-2xl italic leading-snug text-ivory">{copy.complementariedad.p1}</p>
        <HoloVolume compact />
      </PrincipleShell>
    );
  }

  if (id === "permanencia") {
    return (
      <PrincipleShell id={id} hideTitle>
        <p className="text-[15px] leading-relaxed text-ivory-dim">{copy.permanencia.p1}</p>
        <p className="mt-8 text-sm uppercase tracking-[0.22em] text-ivory-mute">{copy.permanencia.medio}</p>
        <h2 className="mt-2 font-display text-3xl leading-tight text-gold sm:text-4xl">
          {copy.permanencia.proposito}
        </h2>
      </PrincipleShell>
    );
  }

  if (id === "primacia") {
    return (
      <PrincipleShell id={id}>
        <p className="font-display text-xl italic leading-snug text-ada">{copy.primacia.ada}</p>
        <p className="mt-5 text-[15px] leading-relaxed text-ivory">{copy.primacia.p1}</p>
        <p className="mt-4 text-[15px] leading-relaxed text-ivory-dim">{copy.primacia.p2}</p>
      </PrincipleShell>
    );
  }

  return (
    <PrincipleShell id={id} wide>
      <ol className="grid gap-3 sm:grid-cols-2">
        {principles.map((p) => (
          <li key={p.n} className="rounded-2xl border border-navy-line/80 bg-navy-deep/50 px-4 py-4">
            <p className="font-display text-2xl text-gold">{p.n}</p>
            <p className="mt-1 font-sans text-sm font-medium text-ivory">{p.name}</p>
            <p className="mt-2 text-sm leading-relaxed text-ivory-dim">{p.line}</p>
          </li>
        ))}
      </ol>
    </PrincipleShell>
  );
}
