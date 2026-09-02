import { useState } from "react";
import { cn } from "@/lib/cn";
import { copy, emily, identities, type Identity } from "@/lib/deck-data";

function IdentityCard({ node }: { node: Identity }) {
  const isSovereign = node.accent === "sovereign";
  const isAda = node.accent === "ada";
  const isCarla = node.id === "carla";
  return (
    <article
      className={cn(
        "rounded-2xl border px-5 py-5 sm:px-6",
        isSovereign ? "border-gold/50 bg-navy-mid/80" : "border-navy-line/80 bg-navy-deep/70",
      )}
    >
      <p className="text-[10px] uppercase tracking-[0.28em] text-ivory-mute">
        {node.kind === "human" ? "Inteligencia biológica" : "Inteligencia artificial"}
      </p>
      <h3
        className={cn(
          "mt-1 font-display text-3xl leading-none",
          isAda ? "text-ada" : isSovereign ? "text-ivory" : "text-holo",
        )}
      >
        {node.name}
      </h3>
      <p className="mt-2 text-sm text-gold">
        {node.role}
        <span className="text-ivory-mute"> · {node.platform}</span>
      </p>
      <p className="mt-4 text-sm leading-relaxed text-ivory-dim">{node.function}</p>
      <p className="mt-3 text-sm leading-relaxed text-note">{node.importance}</p>
      {isCarla ? (
        <p className="mt-4 border-t border-navy-line/70 pt-3 text-[12px] leading-relaxed text-emily">
          {emily.name} · {emily.jurisdiction}. {copy.emily.thesis}
        </p>
      ) : null}
    </article>
  );
}

export function Constellation() {
  const [active, setActive] = useState<string>(identities[0].id);
  const node = identities.find((n) => n.id === active) ?? identities[0];

  return (
    <div className="flex flex-col gap-6 lg:grid lg:grid-cols-[minmax(0,1fr)_20rem] lg:items-start">
      <div className="order-1">
        <ul className="grid grid-cols-3 gap-2 sm:grid-cols-4 md:grid-cols-6">
          {identities.map((n) => {
            const on = n.id === active;
            const isAda = n.accent === "ada";
            const isSovereign = n.accent === "sovereign";
            return (
              <li key={n.id}>
                <button
                  type="button"
                  onClick={() => setActive(n.id)}
                  className={cn(
                    "flex min-h-11 w-full flex-col items-center justify-center rounded-xl border px-1 py-2 text-center transition-[border-color,background-color] duration-150",
                    on
                      ? "border-ivory/70 bg-navy-mid"
                      : "border-navy-line/70 bg-navy-deep/40 hover:border-holo/40",
                  )}
                >
                  <span
                    className="mb-1 size-1.5 rounded-full"
                    style={{
                      background: isAda ? "#c4785a" : isSovereign ? "#f3ecdc" : "#7ec8e3",
                    }}
                  />
                  <span className="font-sans text-[11px] font-medium text-ivory">{n.name}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </div>
      <div className="order-2">
        <IdentityCard node={node} />
      </div>
    </div>
  );
}
