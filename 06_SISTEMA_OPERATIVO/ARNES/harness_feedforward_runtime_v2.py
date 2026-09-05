#!/usr/bin/env python3
"""Runtime consumer for the materialized Harness feedforward payload."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

PAYLOAD_PATH = Path("harness-feedforward.json")
OUTPUT_PATH = Path("harness-runtime-context.json")
REQUIRED_KEYS = {"type","schema_version","guide_id","source_path","sha256","guide_content","status","execution","authority"}

def consume_feedforward() -> dict[str, object]:
    if not PAYLOAD_PATH.is_file() or PAYLOAD_PATH.is_symlink():
        raise FileNotFoundError(f"Invalid feedforward payload: {PAYLOAD_PATH}")
    payload = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    missing = REQUIRED_KEYS.difference(payload)
    if missing:
        raise ValueError(f"Missing feedforward keys: {sorted(missing)}")
    content = payload["guide_content"]
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Feedforward guide_content must be non-empty text")
    if hashlib.sha256(content.encode("utf-8")).hexdigest() != payload["sha256"]:
        raise ValueError("Feedforward SHA-256 does not match guide_content")
    return {"schema_version":"1.0","consumer":"harness_feedforward_runtime","guide_id":payload["guide_id"],"source_path":payload["source_path"],"feedforward_sha256":payload["sha256"],"guide_content":content,"preparation_status":"CONSUMED_FOR_RUNTIME_CONTEXT","execution":"NOT_EXECUTED_BY_CONSUMER","authority":"NOT_GRANTED"}

def main() -> int:
    OUTPUT_PATH.write_text(json.dumps(consume_feedforward(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
