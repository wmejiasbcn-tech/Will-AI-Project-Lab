#!/usr/bin/env python3
"""Minimal, deterministic Guide loader for the WAIPL Agentic Harness.

Loads only the explicitly allowlisted COMANDO 05 Guide from the repository,
validates its structural markers, and emits a feedforward record for the
preparation stage. It does not execute the Guide and grants no authority.
"""

from __future__ import annotations

import hashlib
import json
import sys
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
        "guide_id": "GUIDE-ARNES-COMANDO-05",
        "source_path": str(GUIDE_PATH).replace("\\", "/"),
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "status": "LOADED_FOR_PREPARATION",
        "execution": "NOT_EXECUTED_BY_LOADER",
        "authority": "NOT_GRANTED",
    }

    OUTPUT_PATH.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
