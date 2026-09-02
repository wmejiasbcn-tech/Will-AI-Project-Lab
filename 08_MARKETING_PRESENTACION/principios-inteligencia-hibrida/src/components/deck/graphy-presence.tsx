import { useEffect, useRef } from "react";
import { graphyAudio, graphyLines } from "@/lib/graphy-voice";
import { slides, type SlideId } from "@/lib/deck-data";

function speakFallback(text: string, onEnd?: () => void) {
  if (typeof window === "undefined" || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "es-ES";
  u.rate = 0.92;
  u.pitch = 0.82;
  const voices = window.speechSynthesis.getVoices();
  const es = voices.find((v) => v.lang === "es-ES") || voices.find((v) => v.lang.startsWith("es"));
  if (es) u.voice = es;
  if (onEnd) u.onend = onEnd;
  window.speechSynthesis.speak(u);
}

function srcOf(el: HTMLAudioElement) {
  return el.getAttribute("src") || el.currentSrc || "";
}

export function GraphyPresence({
  slideId,
  playing,
  onAdvance,
  onFinished,
  onToggle,
  hideDock,
}: {
  slideId: SlideId;
  playing: boolean;
  onAdvance: () => void;
  onFinished: () => void;
  onToggle: () => void;
  hideDock?: boolean;
}) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const armed = useRef(playing);
  const slideRef = useRef(slideId);
  const playingSrc = useRef("");
  const line = graphyLines[slideId];
  slideRef.current = slideId;
  armed.current = playing;

  const playClip = (id: SlideId) => {
    const el = audioRef.current;
    const src = graphyAudio[id];
    const text = graphyLines[id];
    playingSrc.current = src;
    if (!el) {
      speakFallback(text, () => finishClip(id));
      return;
    }
    try {
      el.pause();
    } catch {
      /* ignore */
    }
    if (srcOf(el) !== src) el.src = src;
    el.currentTime = 0;
    const go = el.play();
    if (go && typeof go.then === "function") {
      go.catch((err: { name?: string }) => {
        if (err?.name === "AbortError") return;
        if (!armed.current) return;
        speakFallback(text, () => finishClip(id));
      });
    }
  };

  const finishClip = (endedId: SlideId) => {
    if (!armed.current) return;
    if (endedId !== slideRef.current) return;
    const ids = slides.map((s) => s.id);
    const i = ids.indexOf(endedId);
    const next = ids[i + 1];
    if (!next) {
      playingSrc.current = "";
      onFinished();
      return;
    }
    playClip(next);
    onAdvance();
  };

  useEffect(() => {
    if (!playing) {
      playingSrc.current = "";
      audioRef.current?.pause();
      if (typeof window !== "undefined" && window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      return;
    }
    const src = graphyAudio[slideId];
    if (playingSrc.current === src) return;
    playClip(slideId);
  }, [slideId, playing]);

  return (
    <>
      <audio
        ref={audioRef}
        preload="auto"
        onEnded={() => {
          const el = audioRef.current;
          // Changing src can fire `ended` at t=0. Ignore those.
          if (!el || !Number.isFinite(el.currentTime) || el.currentTime < 0.4) return;
          finishClip(slideRef.current);
        }}
        onError={() => {
          if (armed.current) speakFallback(graphyLines[slideRef.current], () => finishClip(slideRef.current));
        }}
      />
      {!hideDock ? (
        <button
          type="button"
          onClick={onToggle}
          className="pointer-events-auto flex min-w-0 flex-row-reverse items-center gap-2 pr-1"
          aria-label={playing ? "Silenciar a Graphy" : "La voz de Graphy"}
        >
          <svg viewBox="0 0 48 48" className="size-8 shrink-0 graphy-breathe sm:size-9" aria-hidden="true">
            <circle cx="24" cy="24" r="18" fill="none" stroke="#7ec8e3" strokeWidth="0.6" opacity="0.4" />
            <circle cx="24" cy="24" r="10" fill="none" stroke="#7ec8e3" strokeWidth="0.7" />
            <path
              d="M10 24 C16 10, 32 10, 38 24 C32 38, 16 38, 10 24"
              fill="none"
              stroke="#d4b483"
              strokeWidth="0.5"
              opacity="0.8"
            />
            <circle cx="24" cy="24" r={playing ? 3 : 2.2} fill="#f3ecdc" />
          </svg>
          <p className="hidden max-w-[11rem] truncate text-left font-sans text-[11px] leading-snug text-ivory-dim lg:block">
            {playing ? line : "La voz de Graphy"}
          </p>
        </button>
      ) : null}
    </>
  );
}
