import { aiIdentities, sovereign } from "@/lib/deck-data";

const RING = aiIdentities.map((n, i) => {
  const a = (i / aiIdentities.length) * Math.PI * 2 - Math.PI / 2;
  return { ...n, a };
});

export function HoloVolume({ compact = false }: { compact?: boolean }) {
  const size = compact ? "h-[220px] sm:h-[260px]" : "h-[260px] sm:h-[340px] md:h-[380px]";
  const radius = compact ? "92px" : "118px";
  return (
    <div className={`holo-stage relative mx-auto w-full max-w-xl ${size}`}>
      <div className="pointer-events-none absolute inset-x-[12%] bottom-[8%] h-[18%] rounded-[100%] bg-holo/10" />
      <div className="holo-rig absolute inset-0">
        <div
          className="absolute left-1/2 top-[58%] h-[42%] w-[72%] -translate-x-1/2 -translate-y-1/2 rounded-[100%] border border-holo/25"
          style={{ transform: "translate(-50%, -50%) rotateX(72deg)" }}
        />
        {RING.map((n) => {
          const isAda = n.accent === "ada";
          return (
            <div
              key={n.id}
              className="absolute left-1/2 top-1/2"
              style={{
                transform: `translate(-50%, -50%) rotateY(${(n.a * 180) / Math.PI}deg) translateZ(${radius})`,
              }}
            >
              <div className="flex flex-col items-center">
                <span
                  className="block size-2.5 rounded-full sm:size-3"
                  style={{
                    background: isAda ? "#c4785a" : "#7ec8e3",
                    boxShadow: isAda
                      ? "0 0 10px rgba(196,120,90,0.85)"
                      : "0 0 10px rgba(126,200,227,0.85)",
                  }}
                />
                <span className="mt-1 hidden max-w-[4.5rem] truncate text-center font-sans text-[9px] tracking-wide text-ivory-dim sm:block">
                  {n.name}
                </span>
              </div>
            </div>
          );
        })}
      </div>
      <div className="absolute left-1/2 top-[48%] z-10 -translate-x-1/2 -translate-y-1/2">
        <div className="flex flex-col items-center">
          <span
            className="block size-4 rounded-full sm:size-5"
            style={{
              background: "#f3ecdc",
              boxShadow: "0 0 16px rgba(243,236,220,0.95)",
            }}
          />
          <span className="mt-2 font-display text-sm tracking-wide text-ivory sm:text-base">
            {sovereign.name}
          </span>
          <span className="text-[10px] uppercase tracking-[0.22em] text-gold">{sovereign.role}</span>
        </div>
      </div>
      <div className="holo-scan absolute inset-[8%] rounded-[50%] border border-holo/20" />
    </div>
  );
}
