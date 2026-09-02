#!/usr/bin/env python3
"""Minimal Harness feedback sensor.

Observes already-produced verification outputs and emits a feedback record.
It does not perform verification, grant authority, or make governance decisions.
"""

import json
import os
from pathlib import Path


def read_exit_code(path: Path) -> str:
    if not path.exists():
        return "NOT_AVAILABLE"
    return path.read_text(encoding="utf-8").strip() or "EMPTY"


exit_code = read_exit_code(Path("harness-verification-exit-code.txt"))
outcome = os.environ.get("VERIFICATION_OUTCOME", "NOT_AVAILABLE")
run_id = os.environ.get("RUN_ID_VALUE", "NOT_AVAILABLE")
commit = os.environ.get("GITHUB_SHA_VALUE", "NOT_AVAILABLE")

if exit_code == "0" and outcome == "success":
    feedback_state = "VERIFICATION_OBSERVED_SUCCESS"
elif exit_code in {"NOT_AVAILABLE", "EMPTY"} or outcome == "NOT_AVAILABLE":
    feedback_state = "VERIFICATION_FEEDBACK_NOT_AVAILABLE"
else:
    feedback_state = "VERIFICATION_OBSERVED_FAILURE"

record = {
    "feedback_type": "HARNESS_FEEDBACK",
    "sensor": "06_SISTEMA_OPERATIVO/ARNES/harness_feedback_sensor.py",
    "observed_verification": "06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py",
    "run_id": run_id,
    "commit": commit,
    "verification_outcome": outcome,
    "verification_exit_code": exit_code,
    "feedback_state": feedback_state,
}

Path("harness-feedback.json").write_text(
    json.dumps(record, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(json.dumps(record, ensure_ascii=False))
