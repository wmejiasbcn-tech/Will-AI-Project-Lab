#!/usr/bin/env python3
"""Long seamless aquatic tide bed for the WAIPL umbral."""

from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np

SR = 44100
DUR = 180.0
FADE = 6.0
N = int(SR * DUR)
EXTRA = int(SR * FADE)


def iir_lp(x: np.ndarray, cutoff: float) -> np.ndarray:
    a = 1.0 - math.exp(-2.0 * math.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc)
        y[i] = acc
    return y


def iir_hp(x: np.ndarray, cutoff: float) -> np.ndarray:
    return x - iir_lp(x, cutoff)


def osc(freq: np.ndarray | float, n: int) -> np.ndarray:
    if np.isscalar(freq):
        phase = 2.0 * math.pi * float(freq) * np.arange(n) / SR
    else:
        phase = np.cumsum(2.0 * math.pi * np.asarray(freq) / SR)
    return np.sin(phase)


def tanh_tide(t: np.ndarray, period: float, hold: float) -> np.ndarray:
    return np.tanh(hold * np.sin(2.0 * math.pi * t / period))


def load_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    if sw != 2:
        raise RuntimeError("int16 only")
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch == 2:
        data = data.reshape(-1, 2).mean(axis=1)
    if sr != SR:
        x_old = np.linspace(0.0, 1.0, data.size, endpoint=False)
        x_new = np.linspace(0.0, 1.0, int(data.size * SR / sr), endpoint=False)
        data = np.interp(x_new, x_old, data).astype(np.float32)
    return data


def loop_blend(src: np.ndarray, n: int, overlap: int) -> np.ndarray:
    if src.size == 0:
        return np.zeros(n, dtype=np.float32)
    out = np.zeros(n, dtype=np.float32)
    pos = 0
    hop = max(1, src.size - overlap)
    win = np.hanning(src.size).astype(np.float32)
    while pos < n:
        sl = src * win
        end = min(pos + src.size, n)
        out[pos:end] += sl[: end - pos]
        pos += hop
    peak = float(np.max(np.abs(out))) or 1.0
    return out / peak


def main() -> None:
    n = N + EXTRA
    t = np.arange(n, dtype=np.float64) / SR

    # Crest holds, trough holds, then returns — never a sharp triangle.
    # Periods divide 180s so the loop seam disappears.
    tide = (
        0.76 * tanh_tide(t, 22.5, 2.9)
        + 0.17 * tanh_tide(t, 45.0, 2.1)
        + 0.07 * tanh_tide(t, 90.0, 1.6)
    )
    tide = tide / (np.max(np.abs(tide)) + 1e-9)
    lift = 0.5 * (tide + 1.0)  # 0..1
    env = 0.08 + 0.92 * np.power(lift, 1.25)  # deep trough, long crest

    rng = np.random.default_rng(1971)

    rng = np.random.default_rng(1971)
    white = rng.standard_normal(n).astype(np.float64)
    brown = np.cumsum(white)
    brown *= 0.997 ** np.arange(n)
    brown -= np.mean(brown)
    brown /= np.std(brown) * 3.2 + 1e-9
    pink = iir_lp(white, 900.0)
    pink /= np.std(pink) * 3.0 + 1e-9

    water_deep = iir_lp(brown, 220.0)
    water_body = iir_lp(brown, 520.0)
    foam = iir_hp(iir_lp(pink, 2800.0), 700.0)

    water = water_deep * (1.15 - lift) + water_body * (0.55 + 0.7 * lift)
    foam_env = np.clip((lift - 0.42) / 0.58, 0.0, 1.0) ** 1.4
    foam *= foam_env

    # Sub swell: pitch opens as the wave rises, drops as it goes to the bottom.
    sub = 0.62 * osc(28.0 + 10.0 * lift, n)
    sub += 0.34 * osc(41.5 + 7.0 * lift, n)
    sub += 0.16 * osc(55.0 + 4.0 * lift, n)
    sub += 0.08 * osc(82.4, n)
    sub = iir_lp(sub, 140.0)

    # Distant pad — more present in the trough (underwater cathedral).
    pad = (
        0.045 * osc(110.0, n)
        + 0.038 * osc(110.18, n)
        + 0.030 * osc(164.81, n)
        + 0.022 * osc(220.0, n)
        + 0.014 * osc(329.63, n)
    )
    pad *= 0.35 + 0.65 * (1.0 - lift)

    # Whisper of the original five clips (deepest two), stretched into the tide.
    orig = np.zeros(n, dtype=np.float64)
    for name, gain in (("clip5", 0.22), ("clip2", 0.12)):
        p = Path(f"/tmp/waipl-audio/{name}.wav")
        if p.exists():
            orig += gain * loop_blend(load_wav(p).astype(np.float64), n, int(SR * 2.5))
    orig = iir_lp(orig, 480.0) * (0.45 + 0.55 * lift)

    mono = (
        0.38 * sub
        + 0.42 * water
        + 0.18 * foam
        + 0.22 * pad
        + 0.16 * orig
    ) * env

    # Stereo: slow lateral drift + a few ms of Haas delay.
    delay = int(0.014 * SR)
    left = mono.copy()
    right = np.concatenate([np.zeros(delay), mono[:-delay]])
    pan = 0.12 * tanh_tide(t, 36.0, 1.8)
    l_g = 0.72 - pan
    r_g = 0.72 + pan
    stereo = np.stack([left * l_g, right * r_g], axis=1)

    # Seamless loop: blend the extra tail into the head.
    fade = EXTRA
    w = np.sin(np.linspace(0.0, math.pi / 2.0, fade)) ** 2
    head = stereo[:fade]
    tail = stereo[N : N + fade]
    stereo[N : N + fade] = tail * (1.0 - w)[:, None] + head * w[:, None]
    out = stereo[:N].copy()
    out[:fade] = stereo[N : N + fade]

    peak = float(np.max(np.abs(out))) or 1.0
    out = (out / peak) * 0.72
    pcm = np.clip(out * 32767.0, -32767, 32767).astype(np.int16)

    wav_path = Path("/tmp/waipl-audio/ola.wav")
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"wrote {wav_path} peak={peak:.3f} dur={N/SR:.1f}s")


if __name__ == "__main__":
    main()
