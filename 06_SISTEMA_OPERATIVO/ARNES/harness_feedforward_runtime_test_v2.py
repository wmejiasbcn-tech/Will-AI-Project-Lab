#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
root = Path(__file__).resolve().parents[3]
subprocess.run([sys.executable, str(root / "06_SISTEMA_OPERATIVO/ARNES/harness_feedforward_runtime_v2.py")], cwd=root, check=True)
context = json.loads((root / "harness-runtime-context.json").read_text(encoding="utf-8"))
assert context["preparation_status"] == "CONSUMED_FOR_RUNTIME_CONTEXT"
assert context["execution"] == "NOT_EXECUTED_BY_CONSUMER"
assert context["authority"] == "NOT_GRANTED"
assert context["guide_content"]
print("FEEDFORWARD_RUNTIME_CONSUMED")
