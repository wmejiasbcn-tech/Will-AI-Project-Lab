#!/usr/bin/env python3
"""Minimal runtime consumer for the materialized Harness feedforward payload.

Consumes the loader output, validates its integrity, and prepares runtime
context. It does not execute the Guide, grant authority, or communicate via SCI.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PAYLOAD_PATH = Path("harness-feedforward.json")
OUTPUT_PATH = Path("06_SISTEMA_OPERATIVO/ARNES/harness-runtime-context.json")
REQUIRED_KEYS = {"type", "schema_version", "guide_id", "source_path", "sha256", "guide_content", "status", "execution", "authority"}


def consume_feedforward() -> dict[str, object]:
    if not PAYLOAD_PATH.is_file() or PAYLOAD_PATH.is_symlink():
        raise FileNotFoundError(f"Invalid feedforward payload: {PAYLOAD_PATH}")
    payload = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS.difference(payload)
    if missing:
        raise ValueError(f"Missing feedforward keys: {sorted(missing)}")
    guide_content = payload["guide_content"]
    if not isinstance(guide_content, str) or not guide_content.strip():
        raise ValueError("Feedforward guide_content must be non-empty text")
    observed_hash = hashlib.sha256(guide_content.encode("utf-8")).hexdigest()
    if observed_hash != payload["sha256"]:
        raise ValueError("Feedforward SHA-256 does not match guide_content")
    return {
        "schema_version": "1.0",
        "consumer": "harness_feedforward_runtime",
        "guide_id": payload["guide_id"],
        "source_path": payload["source_path"],
        "feedforward_sha256": payload["sha256"],
        "guide_content": guide_content,
        "preparation_status": "CONSUMED_FOR_RUNTIME_CONTEXT",
        "execution": "NOT_EXECUTED_BY_CONSUMER",
        "authority": "NOT_GRANTED",
    }


def main() -> int:
    context = consume_feedforward()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(context, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
