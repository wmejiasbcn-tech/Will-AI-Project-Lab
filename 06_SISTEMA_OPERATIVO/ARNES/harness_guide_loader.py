#!/usr/bin/env python3
"""Minimal deterministic Guide loader for the WAIPL Agentic Harness."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

GUIDE_PATH = Path("04_DOCUMENTACION/ARNES_AGENTEICO/GUIDE-ARNES-COMANDO-05.md")
OUTPUT_PATH = Path("harness-feedforward.json")
REQUIRED_MARKERS = (
    "# GUIDE-ARNES-COMANDO-05",
    "**Capa:** Arnés Agéntico WAIPL · Guides / Feedforward",
    "## 1. Finalidad",
    "## 2. Regla de decisión",
    "## 3. Prohibiciones operativas",
    "## 5. Fronteras de jurisdicción",
)


def fail(message: str) -> int:
    print(f"HARNESS_GUIDE_LOAD_FAILURE: {message}", file=sys.stderr)
    return 1


def atomic_write_json(path: Path, payload: dict) -> None:
    """Write beside destination, fsync, then atomically replace it."""
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_path, 0o644)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"output path is not a regular file: {path}")


def main() -> int:
    if not GUIDE_PATH.is_file():
        return fail(f"Guide not found: {GUIDE_PATH}")
    if GUIDE_PATH.is_symlink():
        return fail(f"Guide path must not be a symlink: {GUIDE_PATH}")

    content = GUIDE_PATH.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED_MARKERS if marker not in content]
    if missing:
        return fail("missing structural markers: " + ", ".join(missing))

    record = {
        "type": "HARNESS_FEEDFORWARD",
        "schema_version": "1.0",
        "guide_id": "GUIDE-ARNES-COMANDO-05",
        "source_path": str(GUIDE_PATH).replace("\\", "/"),
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "guide_content": content,
        "status": "LOADED_FOR_PREPARATION",
        "execution": "NOT_EXECUTED_BY_LOADER",
        "authority": "NOT_GRANTED",
    }

    try:
        atomic_write_json(OUTPUT_PATH, record)
    except (OSError, RuntimeError) as exc:
        return fail(str(exc))

    print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
