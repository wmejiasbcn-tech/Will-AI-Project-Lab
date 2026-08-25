import { useEffect } from "react";
import { BookOpen, X } from "lucide-react";
import { Holo, HoloButton, SectionLabel } from "@/components/holo";
import { GLOSSARY, GLOSSARY_MAP } from "@/lib/glossary";
import { useEco } from "@/lib/store";

export function GlossaryPanel() {
  const glossaryId = useEco((s) => s.glossaryId);
  const openGlossary = useEco((s) => s.openGlossary);
  const closeGlossary = useEco((s) => s.closeGlossary);

  useEffect(() => {
    if (!glossaryId) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") closeGlossary();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [glossaryId, closeGlossary]);

  if (!glossaryId) return null;
  const entry = GLOSSARY_MAP[glossaryId];

  return (
    <>
      <button
        type="button"
        aria-label="Cerrar glosario"
        onClick={closeGlossary}
        className="pointer-events-auto absolute inset-0 z-40 bg-void/25"
      />
      <Holo
        strong
        data-testid="glosario"
        className="pointer-events-auto absolute inset-x-3 top-24 z-50 max-h-[70dvh] overflow-hidden p-4 md:left-auto md:right-4 md:top-24 md:w-[24rem]"
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <SectionLabel>Glosario</SectionLabel>
            <h2 className="mt-1 text-lg font-medium text-ink">{entry?.term ?? "Léxico WAIPL"}</h2>
          </div>
          <button
            type="button"
            aria-label="Cerrar glosario"
            onClick={closeGlossary}
            className="flex h-11 w-11 shrink-0 items-center justify-center rounded-md text-muted hover:text-ink"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {entry ? (
          <>
            <p className="mt-1 text-xs uppercase tracking-[0.18em] text-gold">{entry.kicker}</p>
            <p className="mt-3 text-sm leading-relaxed text-ink/85">{entry.blurb}</p>
          </>
        ) : (
          <p className="mt-3 text-sm text-muted">Elige un término.</p>
        )}

        <ul className="mt-4 flex max-h-[36dvh] flex-col gap-1 overflow-auto">
          {GLOSSARY.map((g) => (
            <li key={g.id}>
              <button
                type="button"
                onClick={() => openGlossary(g.id)}
                className="flex min-h-11 w-full items-center rounded-md px-2 text-left text-sm text-ink hover:bg-fog/70"
                data-active={g.id === glossaryId}
              >
                {g.term}
              </button>
            </li>
          ))}
        </ul>
      </Holo>
    </>
  );
}

export function GlossaryButton({ className }: { className?: string }) {
  const openGlossary = useEco((s) => s.openGlossary);
  return (
    <HoloButton className={className} onClick={() => openGlossary("graphy")}>
      <BookOpen className="h-4 w-4" />
      Glosario
    </HoloButton>
  );
}
