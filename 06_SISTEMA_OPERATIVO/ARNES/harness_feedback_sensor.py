#!/usr/bin/env python3
"""Minimal Harness feedback sensor.

Observes already-produced verification outputs and emits a feedback record.
It does not perform verification, grant authority, or make governance decisions.
"""

import json
import os
from pathlib import Path

FEEDBACK_PATH = Path("harness-feedback.json")


def read_exit_code(path: Path) -> str:
    if not path.exists():
        return "NOT_AVAILABLE"
    return path.read_text(encoding="utf-8").strip() or "EMPTY"


def safe_write_json(path: Path, data: dict) -> None:
    """Write JSON to path safely, rejecting symlinks and writing atomically.

    - Rejects symlinks at the target path (prevents redirection attacks).
    - Refuses to write outside the current working directory.
    - Writes to a temporary file first, then atomically replaces the target.
    """
    # Reject if the target path is a symlink
    if path.is_symlink():
        raise RuntimeError(
            f"Refusing to write: {path} is a symlink - possible redirection attack."
        )

    # If the path exists and is not a regular file, reject
    if path.exists() and not path.is_file():
        raise RuntimeError(
            f"Refusing to write: {path} exists but is not a regular file."
        )

    # Resolve and verify the path is within the current working directory
    resolved = path.resolve()
    cwd = Path.cwd().resolve()
    if not str(resolved).startswith(str(cwd)):
        raise RuntimeError(
            f"Refusing to write: {path} resolves outside the working directory."
        )

    # Write to a temporary file first, then atomically replace
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(path)


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

safe_write_json(FEEDBACK_PATH, record)
print(json.dumps(record, ensure_ascii=False))