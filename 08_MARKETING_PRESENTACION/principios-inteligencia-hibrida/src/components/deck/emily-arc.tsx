const PATH = {
  volume: "M 36 214 C 92 28, 248 12, 364 132",
  field: "M 10 74 C 28 16, 64 8, 90 36",
  inline: "M 16 92 C 70 8, 210 4, 304 58",
};

const VIEW = {
  volume: "0 0 400 300",
  field: "0 0 100 100",
  inline: "0 0 320 110",
};

type Tone = keyof typeof PATH;

function Particles({ d, tone }: { d: string; tone: Tone }) {
  const n = tone === "field" ? 5 : 8;
  const r = tone === "field" ? 0.55 : tone === "inline" ? 1.4 : 1.8;
  const dur = tone === "field" ? 5.4 : 4.2;
  return (
    <>
      {Array.from({ length: n }, (_, i) => {
        const delay = -((i / n) * dur);
        const reverse = i % 2 === 1;
        return (
          <circle key={i} r={r} className="emily-dot" fill="#c8d8ec">
            <animateMotion
              dur={`${dur}s`}
              begin={`${delay}s`}
              repeatCount="indefinite"
              path={d}
              keyPoints={reverse ? "1;0" : "0;1"}
              keyTimes="0;1"
              calcMode="linear"
            />
          </circle>
        );
      })}
    </>
  );
}

export function EmilyArc({
  tone = "volume",
  labeled = true,
}: {
  tone?: Tone;
  labeled?: boolean;
}) {
  const d = PATH[tone];
  const gid = `emily-stroke-${tone}`;
  const glow = `emily-glow-${tone}`;
  const sw = tone === "field" ? 0.55 : tone === "inline" ? 1.35 : 1.7;
  return (
    <svg
      className="emily-arc pointer-events-none absolute inset-0 h-full w-full"
      viewBox={VIEW[tone]}
      preserveAspectRatio={tone === "field" ? "xMidYMid slice" : "xMidYMid meet"}
      aria-hidden="true"
    >
      <defs>
        <linearGradient id={gid} x1="0" y1="1" x2="1" y2="0">
          <stop offset="0%" stopColor="#f3ecdc" />
          <stop offset="48%" stopColor="#c8d8ec" />
          <stop offset="100%" stopColor="#7ec8e3" />
        </linearGradient>
        <filter id={glow} x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation={tone === "field" ? 0.8 : 2.2} result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <path
        d={d}
        fill="none"
        stroke={`url(#${gid})`}
        strokeWidth={sw * 3.2}
        opacity="0.18"
        filter={`url(#${glow})`}
      />
      <path
        className="emily-pulse"
        d={d}
        fill="none"
        stroke={`url(#${gid})`}
        strokeWidth={sw}
        strokeLinecap="round"
      />
      <Particles d={d} tone={tone} />
      {labeled && tone !== "field" ? (
        <text
          x={tone === "inline" ? 160 : 200}
          y={tone === "inline" ? 22 : 36}
          textAnchor="middle"
          fill="#c8d8ec"
          fontSize={tone === "inline" ? 9 : 11}
          fontFamily="Figtree, sans-serif"
          letterSpacing="2.4"
        >
          EMILY · SINAPSIS
        </text>
      ) : null}
    </svg>
  );
}
