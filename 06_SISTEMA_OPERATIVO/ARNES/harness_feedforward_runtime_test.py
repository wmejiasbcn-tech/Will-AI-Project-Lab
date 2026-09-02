#!/usr/bin/env python3
"""Smoke test for the Harness feedforward runtime consumer."""
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
payload = root / "harness-feedforward.json"
consumer = root / "06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime.py"
if not payload.is_file():
    print("PAYLOAD_MISSING")
    raise SystemExit(1)
subprocess.run([sys.executable, str(consumer)], cwd=root, check=True)
context = json.loads((root / "harness-runtime-context.json").read_text(encoding="utf-8"))
assert context["preparation_status"] == "CONSUMED_FOR_RUNTIME_CONTEXT"
assert context["execution"] == "NOT_EXECUTED_BY_CONSUMER"
assert context["authority"] == "NOT_GRANTED"
assert context["guide_content"]
print("FEEDFORWARD_RUNTIME_CONSUMED")
