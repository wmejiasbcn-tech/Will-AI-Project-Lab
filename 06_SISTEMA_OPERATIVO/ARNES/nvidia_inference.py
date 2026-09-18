#!/usr/bin/env python3
"""Minimal NVIDIA API inference adapter for the WAIPL Harness.

Provider-only adapter: it does not grant authority, route messages, or bypass
WAIPL-BUS/SCI governance. The API key is read only from NVIDIA_API_KEY and is
never emitted.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "nvidia/nemotron-3-nano-30b-a3b"


def chat(prompt: str, model: str, base_url: str) -> str:
    api_key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is not set")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 256,
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"NVIDIA API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"NVIDIA API connection error: {exc.reason}") from exc

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected NVIDIA API response shape") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Call NVIDIA API from the WAIPL Harness")
    parser.add_argument("prompt", nargs="?", default="Di exactamente: NVIDIA OPERATIVO AHORA")
    parser.add_argument("--model", default=os.environ.get("NVIDIA_MODEL", DEFAULT_MODEL))
    parser.add_argument("--base-url", default=os.environ.get("NVIDIA_BASE_URL", DEFAULT_BASE_URL))
    args = parser.parse_args()

    try:
        print(chat(args.prompt, args.model, args.base_url))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
