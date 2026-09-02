#!/usr/bin/env python3
"""Minimal integration test for the Harness feedforward runtime consumer."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CONSUMER = ROOT / "06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime.py"
OUTPUT = ROOT / "06_SISTEMA_OPERATIVO/ARNES/harness-runtime-context.json"
PAYLOAD = ROOT / "harness-feedforward.json"
def main() -> int:
    subprocess.run([sys.executable, str(CONSUMER)], cwd=ROOT, check=True)
    if not OUTPUT.is_file() or OUTPUT.is_symlink():
        raise AssertionError("runtime context was not materialized as a regular file")
    context = json.loads(OUTPUT.read_text(encoding="utf-8"))
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    assert context["guide_id"] == payload["guide_id"]
    assert context["feedforward_sha256"] == payload["sha256"]
    assert context["guide_content"] == payload["guide_content"]
    assert context["preparation_status"] == "CONSUMED_FOR_RUNTIME_CONTEXT"
    assert context["execution"] == "NOT_EXECUTED_BY_CONSUMER"
    assert context["authority"] == "NOT_GRANTED"
    print("HARNESS_FEEDFORWARD_RUNTIME_TEST: PASS")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
