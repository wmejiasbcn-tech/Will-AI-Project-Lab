import { useMemo } from "react";
import type { SlideId } from "@/lib/deck-data";
import { EmilyArc } from "./emily-arc";

function mulberry32(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function rnd(n: number) {
  return Math.round(n * 1000) / 1000;
}

function hash(s: string) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

type Pt = { x: number; y: number };

function layout(variant: SlideId, rand: () => number): Pt[] {
  const pts: Pt[] = [];
  const push = (x: number, y: number) => pts.push({ x: rnd(x), y: rnd(y) });

  if (variant === "cover") {
    for (let i = 0; i < 36; i++) {
      const a = (i / 36) * Math.PI * 2;
      push(50 + Math.cos(a) * 38, 50 + Math.sin(a) * 24);
    }
    for (let i = 0; i < 18; i++) {
      const a = (i / 18) * Math.PI * 2 + 0.2;
      push(50 + Math.cos(a) * 22, 50 + Math.sin(a) * 14);
    }
  } else if (variant === "naturaleza") {
    for (let r = 0; r < 5; r++) {
      const n = 6 + r * 4;
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2 + r * 0.2;
        push(50 + Math.cos(a) * (10 + r * 7.5), 50 + Math.sin(a) * (16 + r * 8));
      }
    }
  } else if (variant === "diferencial") {
    for (let i = 0; i < 28; i++) {
      const t = i / 27;
      push(18 + t * 64, 22 + Math.sin(t * Math.PI) * 18);
      push(18 + t * 64, 78 - Math.sin(t * Math.PI) * 18);
    }
    for (let i = 0; i < 9; i++) push(50, 18 + i * 8);
  } else if (variant === "nodos") {
    for (let k = 0; k < 12; k++) {
      const a = (k / 12) * Math.PI * 2 - Math.PI / 2;
      const cx = 50 + Math.cos(a) * 28;
      const cy = 50 + Math.sin(a) * 28;
      push(cx, cy);
      for (let j = 0; j < 4; j++) {
        const b = (j / 4) * Math.PI * 2;
        push(cx + Math.cos(b) * 7, cy + Math.sin(b) * 7);
      }
    }
    push(50, 50);
  } else if (variant === "graphy") {
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 8; c++) {
        push(16 + c * 9.5, 22 + r * 18);
      }
    }
    for (let i = 0; i < 7; i++) push(12 + i * 12, 50);
  } else if (variant === "identidades") {
    for (let i = 0; i < 11; i++) {
      const a = (i / 11) * Math.PI * 2 - Math.PI / 2;
      push(50 + Math.cos(a) * 34, 50 + Math.sin(a) * 34);
      push(50 + Math.cos(a) * 22, 50 + Math.sin(a) * 22);
    }
    push(50, 50);
  } else if (variant === "complementariedad") {
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * Math.PI * 2;
      push(34 + Math.cos(a) * 16, 50 + Math.sin(a) * 16);
      push(66 + Math.cos(a) * 16, 50 + Math.sin(a) * 16);
    }
  } else if (variant === "permanencia") {
    for (let i = 0; i < 40; i++) {
      const t = i / 39;
      const a = t * Math.PI * 4.2;
      push(50 + Math.cos(a) * (8 + t * 32), 50 + Math.sin(a) * (8 + t * 20));
    }
  } else if (variant === "primacia") {
    push(50, 18);
    for (let i = 0; i < 6; i++) {
      const a = Math.PI / 2 + ((i - 2.5) * Math.PI) / 8;
      push(50 + Math.cos(a) * 32, 28 + Math.sin(a) * 42);
    }
    for (let i = 0; i < 18; i++) {
      const t = i / 17;
      push(22 + t * 56, 78);
    }
  } else {
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2 - Math.PI / 2;
      push(50 + Math.cos(a) * 30, 48 + Math.sin(a) * 26);
      for (let j = 0; j < 5; j++) {
        const b = (j / 5) * Math.PI * 2;
        push(
          50 + Math.cos(a) * 30 + Math.cos(b) * 8,
          48 + Math.sin(a) * 26 + Math.sin(b) * 8,
        );
      }
    }
  }

  for (let i = 0; i < 10; i++) {
    push(8 + rand() * 84, 8 + rand() * 84);
  }
  return pts;
}

function edges(pts: Pt[], maxDist: number, cap: number) {
  const out: Array<[Pt, Pt]> = [];
  for (let i = 0; i < pts.length; i++) {
    for (let j = i + 1; j < pts.length; j++) {
      const dx = pts[i].x - pts[j].x;
      const dy = pts[i].y - pts[j].y;
      if (dx * dx + dy * dy < maxDist * maxDist) {
        out.push([pts[i], pts[j]]);
        if (out.length >= cap) return out;
      }
    }
  }
  return out;
}

export function NetworkField({ variant }: { variant: SlideId }) {
  const mesh = useMemo(() => {
    const randA = mulberry32(hash(variant + "-a"));
    const randB = mulberry32(hash(variant + "-b"));
    const far = layout(variant, randA);
    const near = layout(variant, randB).map((p) => ({
      x: rnd(p.x + (randB() - 0.5) * 6),
      y: rnd(p.y + (randB() - 0.5) * 6),
    }));
    const stars = Array.from({ length: 48 }, (_, i) => {
      const r = mulberry32(hash(variant + "-s" + i));
      return {
        x: rnd(r() * 100),
        y: rnd(r() * 100),
        r: rnd(0.12 + r() * 0.28),
        delay: rnd(r() * 3.4),
        dur: rnd(2.4 + r() * 2.2),
      };
    });
    return {
      far,
      near,
      farE: edges(far, 16, 90),
      nearE: edges(near, 14, 70),
      stars,
    };
  }, [variant]);

  const emilyHot = variant === "cover" || variant === "nodos" || variant === "graphy" || variant === "identidades";

  return (
    <div className="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true">
      <svg
        className="parallax-far net-layer net-far h-full w-full"
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid slice"
        style={{ contain: "layout paint" }}
      >
        {mesh.farE.map((e, i) => (
          <line
            key={`fe${i}`}
            x1={e[0].x}
            y1={e[0].y}
            x2={e[1].x}
            y2={e[1].y}
            stroke="#7ec8e3"
            strokeWidth="0.11"
            opacity="0.32"
          />
        ))}
        {mesh.far.map((p, i) => (
          <circle key={`fn${i}`} cx={p.x} cy={p.y} r="0.28" fill="#7ec8e3" opacity="0.28" />
        ))}
      </svg>
      <svg
        className="parallax-near net-layer net-near h-full w-full"
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid slice"
        style={{ contain: "layout paint" }}
      >
        {mesh.nearE.map((e, i) => (
          <line
            key={`ne${i}`}
            x1={e[0].x}
            y1={e[0].y}
            x2={e[1].x}
            y2={e[1].y}
            stroke="#7ec8e3"
            strokeWidth="0.16"
            opacity="0.48"
          />
        ))}
        {mesh.near.map((p, i) => (
          <circle key={`nn${i}`} cx={p.x} cy={p.y} r="0.38" fill="#d4b483" opacity="0.35" />
        ))}
        {mesh.stars.map((s, i) => (
          <circle
            key={`st${i}`}
            className="star-twinkle"
            cx={s.x}
            cy={s.y}
            r={s.r}
            fill="#f3ecdc"
            style={{ animationDelay: `${s.delay}s`, animationDuration: `${s.dur}s` }}
          />
        ))}
      </svg>
      <div className={emilyHot ? "absolute inset-0 opacity-80" : "absolute inset-0 opacity-35"}>
        <EmilyArc tone="field" labeled={false} />
      </div>
      <div className="film" />
    </div>
  );
}
