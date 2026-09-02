import { attentionFocus } from "@/lib/graphy-voice";
import type { SlideId } from "@/lib/deck-data";

const TOKENS = ["misión", "nodo", "red", "atención", "soberano", "valor"];
const LAYERS = ["Q", "K", "V"];

export function AttentionNet({ slideId }: { slideId: SlideId }) {
  const focus = attentionFocus[slideId] % TOKENS.length;
  return (
    <div className="relative mx-auto w-full max-w-lg">
      <svg viewBox="0 0 320 200" className="h-auto w-full" aria-hidden="true">
        {TOKENS.map((t, i) => {
          const x = 28 + i * 48;
          const hot = i === focus;
          return (
            <g key={t}>
              {LAYERS.map((L, li) => {
                const y = 28 + li * 44;
                return (
                  <line
                    key={L}
                    x1={x}
                    y1={y}
                    x2={28 + focus * 48}
                    y2={160}
                    stroke={hot ? "#7ec8e3" : "#1a3354"}
                    strokeWidth={hot ? 1.4 : 0.5}
                    opacity={hot ? 0.85 : 0.28}
                    className={hot ? "attn-pulse" : undefined}
                  />
                );
              })}
              <circle cx={x} cy={160} r={hot ? 6 : 3.5} fill={hot ? "#d4b483" : "#4a8aa3"} />
              <text
                x={x}
                y={182}
                textAnchor="middle"
                fill={hot ? "#f3ecdc" : "#8fa3b8"}
                fontSize="8"
                fontFamily="Figtree, sans-serif"
              >
                {t}
              </text>
            </g>
          );
        })}
        {LAYERS.map((L, li) => (
          <g key={L}>
            {TOKENS.map((_, i) => (
              <circle
                key={i}
                cx={28 + i * 48}
                cy={28 + li * 44}
                r="3"
                fill="#7ec8e3"
                opacity="0.7"
              />
            ))}
            <text
              x="4"
              y={32 + li * 44}
              fill="#d4b483"
              fontSize="9"
              fontFamily="Figtree, sans-serif"
            >
              {L}
            </text>
          </g>
        ))}
        <text
          x="160"
          y="14"
          textAnchor="middle"
          fill="#c9bfa8"
          fontSize="8"
          fontFamily="Figtree, sans-serif"
          letterSpacing="1.4"
        >
          softmax · haz de luz
        </text>
      </svg>
      <p className="mt-2 text-center font-display text-lg italic text-ivory-dim">
        f(x) = f<sub>L</sub> ∘ ⋯ ∘ f<sub>1</sub>(x)
      </p>
    </div>
  );
}
