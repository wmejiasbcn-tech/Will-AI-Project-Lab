import { useCallback, useEffect, useRef, useState } from "react";
import { Copy, List, Maximize, Minimize } from "lucide-react";
import { slides, type SlideId } from "@/lib/deck-data";
import { copyText, publicShareUrl } from "@/lib/public-url";
import { cn } from "@/lib/cn";
import { GraphyPresence } from "./graphy-presence";
import { NetworkField } from "./network-field";
import { SeoCorpus } from "./seo-corpus";
import { ShareSheet } from "./share-sheet";
import { CoverSlide, SlideView } from "./slides";

export function Deck() {
  const [index, setIndex] = useState(0);
  const [overview, setOverview] = useState(false);
  const [voiceOn, setVoiceOn] = useState(false);
  const [fs, setFs] = useState(false);
  const [shareUrl, setShareUrl] = useState<string | null>(null);
  const [shareOpen, setShareOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const indexRef = useRef(0);
  indexRef.current = index;
  const px = useRef(0);
  const py = useRef(0);
  const tx = useRef(0);
  const ty = useRef(0);
  const slide = slides[index];

  useEffect(() => {
    setShareUrl(publicShareUrl());
  }, []);

  const go = useCallback((i: number) => {
    setIndex((cur) => {
      const next = ((i % slides.length) + slides.length) % slides.length;
      return next === cur ? cur : next;
    });
    setOverview(false);
  }, []);

  useEffect(() => {
    const onVis = () => {
      document.documentElement.classList.toggle("deck-paused", document.hidden);
    };
    document.addEventListener("visibilitychange", onVis);
    return () => document.removeEventListener("visibilitychange", onVis);
  }, []);

  useEffect(() => {
    let raf = 0;
    const loop = () => {
      px.current += (tx.current - px.current) * 0.08;
      py.current += (ty.current - py.current) * 0.08;
      const el = rootRef.current;
      if (el) {
        el.style.setProperty("--px", px.current.toFixed(4));
        el.style.setProperty("--py", py.current.toFixed(4));
        el.style.setProperty("--hx", px.current.toFixed(4));
        el.style.setProperty("--hy", py.current.toFixed(4));
      }
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, []);

  useEffect(() => {
    const onMove = (e: PointerEvent) => {
      const w = window.innerWidth || 1;
      const h = window.innerHeight || 1;
      tx.current = (e.clientX / w) * 2 - 1;
      ty.current = (e.clientY / h) * 2 - 1;
    };
    window.addEventListener("pointermove", onMove, { passive: true });
    return () => window.removeEventListener("pointermove", onMove);
  }, []);

  const toggleFs = useCallback(() => {
    const el = rootRef.current;
    if (!el) return;
    const doc = document as Document & { webkitExitFullscreen?: () => void };
    const node = el as HTMLElement & { webkitRequestFullscreen?: () => void };
    if (document.fullscreenElement) {
      void document.exitFullscreen?.();
      doc.webkitExitFullscreen?.();
      setFs(false);
    } else {
      void (node.requestFullscreen?.() ?? node.webkitRequestFullscreen?.());
      setFs(true);
    }
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement | null)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      if (e.key === "ArrowRight" || e.key === "PageDown") {
        e.preventDefault();
        go(index + 1);
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        go(index - 1);
      } else if (e.key === " " && tag !== "BUTTON") {
        e.preventDefault();
        go(index + 1);
      } else if (e.key === "Escape") {
        setOverview(false);
        setShareOpen(false);
      } else if (e.key === "o" || e.key === "i") {
        setOverview((v) => !v);
      } else if (e.key === "f") {
        toggleFs();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [go, index, toggleFs]);

  function onCopy() {
    const url = publicShareUrl();
    setShareUrl(url);
    setShareOpen(true);
    if (url) copyText(url);
  }

  return (
    <div ref={rootRef} className="deck-root">
      <NetworkField variant={slide.id} />
      <SeoCorpus />
      <header className="pointer-events-none absolute inset-x-0 top-0 z-30 flex items-center gap-2 px-3 py-3 sm:px-5">
        <img
          src="/blason.png"
          alt="Blasón del WAIPL"
          width={28}
          height={28}
          className="size-7 object-contain"
        />
        <span className="font-sans text-[11px] font-medium tracking-[0.22em] text-ivory-dim">WAIPL</span>
        <div className="pointer-events-auto ml-auto flex min-w-0 items-center gap-1">
          <GraphyPresence
            slideId={slide.id}
            playing={voiceOn}
            onAdvance={() => {
              const i = indexRef.current;
              if (i < slides.length - 1) go(i + 1);
            }}
            onFinished={() => setVoiceOn(false)}
            onToggle={() => setVoiceOn((v) => !v)}
            hideDock={slide.id === "cover"}
          />
          <button
            type="button"
            onClick={onCopy}
            className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-navy-line/80 bg-navy-deep/70 px-3 text-[11px] tracking-wide text-ivory"
            aria-label="Copiar enlace público"
            aria-haspopup="dialog"
            aria-expanded={shareOpen}
          >
            <Copy className="size-3.5" />
            <span>Enlace</span>
          </button>
          <button
            type="button"
            onClick={() => setOverview(true)}
            className="inline-flex size-11 items-center justify-center rounded-full text-ivory-dim"
            aria-label="Índice"
          >
            <List className="size-4" />
          </button>
          <button
            type="button"
            onClick={toggleFs}
            className="inline-flex size-11 items-center justify-center rounded-full text-ivory-dim"
            aria-label={fs ? "Salir de pantalla completa" : "Pantalla completa"}
          >
            {fs ? <Minimize className="size-4" /> : <Maximize className="size-4" />}
          </button>
          <span className="w-8 text-right font-sans text-[11px] tabular-nums text-ivory-mute sm:w-10">
            {slide.number}
          </span>
        </div>
      </header>

      {shareOpen ? (
        <ShareSheet
          url={shareUrl}
          onClose={() => setShareOpen(false)}
          onResolved={(next) => {
            setShareUrl(next);
            copyText(next);
          }}
        />
      ) : null}

      <main className="relative z-10 flex h-full min-h-0 flex-col justify-center overflow-y-auto pt-16 pb-16">
        {slide.id === "cover" ? (
          <CoverSlide onVoice={() => setVoiceOn((v) => !v)} />
        ) : (
          <SlideView id={slide.id as SlideId} />
        )}
      </main>

      <nav
        className="absolute inset-x-0 bottom-3 z-30 flex items-center justify-center gap-1.5 px-4"
        aria-label="Láminas"
      >
        {slides.map((s, i) => (
          <button
            key={s.id}
            type="button"
            aria-label={s.overview}
            onClick={() => go(i)}
            className={cn(
              "h-2.5 min-h-0 rounded-full transition-[width,background-color] duration-150",
              i === index ? "w-6 bg-ivory" : "w-2.5 bg-navy-line hover:bg-holo-dim",
            )}
          />
        ))}
      </nav>

      {overview ? (
        <div className="absolute inset-0 z-40 flex items-center justify-center bg-navy-deep/80 px-4">
          <ul className="grid max-h-[80dvh] w-full max-w-3xl grid-cols-2 gap-2 overflow-y-auto sm:grid-cols-3">
            {slides.map((s, i) => (
              <li key={s.id}>
                <button
                  type="button"
                  onClick={() => go(i)}
                  className="flex min-h-20 w-full flex-col items-start rounded-xl border border-navy-line bg-navy/90 px-3 py-3 text-left"
                >
                  <span className="text-[10px] uppercase tracking-[0.2em] text-gold">{s.number}</span>
                  <span className="mt-1 font-sans text-sm text-ivory">{s.overview}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      <noscript>
        <article className="relative z-50 max-w-2xl p-8 text-ivory">
          <h1>Principio de inteligencia híbrida colaborativa</h1>
          <p>
            Will-AI Project Lab. Once inteligencias artificiales y una inteligencia biológica. Seis
            principios. Graphy es la red.
          </p>
        </article>
      </noscript>
    </div>
  );
}
