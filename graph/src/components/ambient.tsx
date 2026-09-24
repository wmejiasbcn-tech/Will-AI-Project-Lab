import { useEffect, useRef } from "react";
import { Volume2, VolumeX } from "lucide-react";
import { useEco } from "@/lib/store";
import { cn } from "@/lib/cn";

const BED = "/audio/ola.mp3";
const MASTER = 0.28;

type Tide = {
  ctx: AudioContext;
  master: GainNode;
  voice: GainNode;
  filter: BiquadFilterNode;
  source: AudioBufferSourceNode | null;
  nodes: AudioScheduledSourceNode[];
};

function connectLfo(
  ctx: AudioContext,
  hz: number,
  depth: number,
  offset: number,
  target: AudioParam,
  nodes: AudioScheduledSourceNode[],
) {
  const osc = ctx.createOscillator();
  osc.type = "sine";
  osc.frequency.value = hz;
  const gain = ctx.createGain();
  gain.gain.value = depth;
  const bias = ctx.createConstantSource();
  bias.offset.value = offset;
  osc.connect(gain);
  gain.connect(target);
  bias.connect(target);
  osc.start();
  bias.start();
  nodes.push(osc, bias);
}

function makeTide(ctx: AudioContext): Tide {
  const nodes: AudioScheduledSourceNode[] = [];
  const master = ctx.createGain();
  master.gain.value = 0;

  const voice = ctx.createGain();
  voice.gain.value = 0;

  const filter = ctx.createBiquadFilter();
  filter.type = "lowpass";
  filter.frequency.value = 0;
  filter.Q.value = 0.5;

  const pan = ctx.createStereoPanner();
  pan.pan.value = 0;

  filter.connect(pan);
  pan.connect(voice);
  voice.connect(master);
  master.connect(ctx.destination);

  // Wave: rise, hold, fall, hold at the bottom, return.
  connectLfo(ctx, 1 / 22.5, 0.26, 0.74, voice.gain, nodes);
  connectLfo(ctx, 1 / 45, 500, 720, filter.frequency, nodes);
  connectLfo(ctx, 1 / 36, 0.16, 0, pan.pan, nodes);

  return { ctx, master, voice, filter, source: null, nodes };
}

function attachBed(tide: Tide, buffer: AudioBuffer) {
  tide.source?.stop();
  tide.source?.disconnect();
  const src = tide.ctx.createBufferSource();
  src.buffer = buffer;
  src.loop = true;
  src.connect(tide.filter);
  src.start(0);
  tide.source = src;
}

export function Ambient() {
  const sound = useEco((s) => s.sound);
  const tideRef = useRef<Tide | null>(null);
  const bufferRef = useRef<AudioBuffer | null>(null);
  const wantRef = useRef(sound);

  useEffect(() => {
    wantRef.current = sound;
  }, [sound]);

  useEffect(() => {
    let cancelled = false;
    let tide: Tide | null = null;

    const fadeMaster = (value: number) => {
      if (!tide) return;
      const now = tide.ctx.currentTime;
      tide.master.gain.cancelScheduledValues(now);
      tide.master.gain.setTargetAtTime(value, now, 0.6);
    };

    const startIfWanted = async () => {
      if (!tide || cancelled) return;
      if (!bufferRef.current) {
        const res = await fetch(BED);
        const raw = await res.arrayBuffer();
        if (cancelled) return;
        bufferRef.current = await tide.ctx.decodeAudioData(raw.slice(0));
      }
      if (!tide.source && bufferRef.current) attachBed(tide, bufferRef.current);
      fadeMaster(wantRef.current ? MASTER : 0);
    };

    const unlock = () => {
      if (!tide) {
        tide = makeTide(new AudioContext({ latencyHint: "playback" }));
        tideRef.current = tide;
      }
      if (tide.ctx.state === "suspended") void tide.ctx.resume();
      void startIfWanted();
    };

    const onVis = () => {
      if (document.visibilityState === "visible" && wantRef.current) {
        void startIfWanted();
      }
    };

    window.addEventListener("pointerdown", unlock, true);
    window.addEventListener("keydown", unlock, true);
    document.addEventListener("visibilitychange", onVis);

    return () => {
      cancelled = true;
      window.removeEventListener("pointerdown", unlock, true);
      window.removeEventListener("keydown", unlock, true);
      document.removeEventListener("visibilitychange", onVis);
      if (tide) {
        try {
          tide.source?.stop();
        } catch {
          /* already stopped */
        }
        for (const n of tide.nodes) {
          try {
            n.stop();
          } catch {
            /* already stopped */
          }
        }
        void tide.ctx.close();
      }
      tideRef.current = null;
    };
  }, []);

  useEffect(() => {
    const tide = tideRef.current;
    if (!tide) return;
    const now = tide.ctx.currentTime;
    tide.master.gain.cancelScheduledValues(now);
    tide.master.gain.setTargetAtTime(sound ? MASTER : 0, now, 0.5);
    if (sound && tide.ctx.state === "suspended") void tide.ctx.resume();
  }, [sound]);

  return null;
}

export function SoundToggle({ light = false }: { light?: boolean }) {
  const sound = useEco((s) => s.sound);
  const toggleSound = useEco((s) => s.toggleSound);
  return (
    <button
      type="button"
      aria-label={sound ? "Silenciar ambiente" : "Activar ambiente"}
      onClick={toggleSound}
      className={cn(
        "flex h-11 w-11 items-center justify-center rounded-md",
        light ? "text-ivory/80 hover:text-ivory" : "text-ink hover:text-ink",
      )}
    >
      {sound ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
    </button>
  );
}
