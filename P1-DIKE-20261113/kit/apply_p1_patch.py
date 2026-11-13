#!/usr/bin/env python3
"""Apply the byte-integrity correction to the local active DIKE source file."""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import tempfile
from pathlib import Path

OLD_HASH = '        doc_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()'
NEW_HASH = (
    '        content_bytes = content_text.encode("utf-8")\n'
    '        doc_hash = hashlib.sha256(content_bytes).hexdigest()'
)
OLD_WRITE = (
    '        with open(corpus_file, "w", encoding="utf-8") as f:\n'
    '            f.write(content_text)'
)
NEW_WRITE = (
    '        with open(corpus_file, "wb") as f:\n'
    '            f.write(content_bytes)\n'
    '            f.flush()\n'
    '            os.fsync(f.fileno())\n'
    '\n'
    '        # Verify the physical bytes before registering the index entry.\n'
    '        with open(corpus_file, "rb") as f:\n'
    '            stored_bytes = f.read()\n'
    '        stored_hash = hashlib.sha256(stored_bytes).hexdigest()\n'
    '        if stored_hash != doc_hash:\n'
    '            try:\n'
    '                os.remove(corpus_file)\n'
    '            finally:\n'
    '                raise IOError("DIKE integrity error: persisted SHA-256 mismatch")'
)
OLD_SIZE = '            "size_bytes": len(content_text.encode("utf-8")),'
NEW_SIZE = '            "size_bytes": len(content_bytes),'


def _replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise ValueError(
            f"Patch refused: block {label!r} found {count} times; exactly one required"
        )
    return source.replace(old, new, 1)


def build_patched_bytes(raw: bytes) -> bytes:
    """Patch UTF-8 source while preserving a uniform LF or CRLF convention."""
    text = raw.decode("utf-8")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    normalized = text.replace("\r\n", "\n")

    already_patched = (
        normalized.count(NEW_HASH) == 1
        and normalized.count(NEW_WRITE) == 1
        and normalized.count(NEW_SIZE) == 1
        and OLD_HASH not in normalized
        and OLD_WRITE not in normalized
        and OLD_SIZE not in normalized
    )
    if already_patched:
        return raw

    normalized = _replace_once(normalized, OLD_HASH, NEW_HASH, "hash")
    normalized = _replace_once(normalized, OLD_WRITE, NEW_WRITE, "file write")
    normalized = _replace_once(normalized, OLD_SIZE, NEW_SIZE, "size_bytes")
    return normalized.replace("\n", newline).encode("utf-8")


def apply_patch(path: Path, dry_run: bool = False) -> dict[str, str | bool]:
    path = path.expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")

    original = path.read_bytes()
    patched = build_patched_bytes(original)
    backup_path = path.with_name(path.name + ".before-p1-crlf-lf.bak")
    result: dict[str, str | bool] = {
        "path": str(path),
        "original_sha256": hashlib.sha256(original).hexdigest(),
        "patched_sha256": hashlib.sha256(patched).hexdigest(),
        "backup_path": str(backup_path),
        "dry_run": dry_run,
        "changed": patched != original,
    }
    if dry_run or patched == original:
        return result

    if backup_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing backup: {backup_path}")
    shutil.copy2(path, backup_path)

    fd, temp_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".p1.tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(patched)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise

    persisted = path.read_bytes()
    if hashlib.sha256(persisted).hexdigest() != result["patched_sha256"]:
        shutil.copy2(backup_path, path)
        raise IOError("Post-replacement verification failed; previous file restored")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_file", help="Exact local path to the active dike_auditora.py")
    parser.add_argument("--dry-run", action="store_true", help="Validate fit without changing files")
    args = parser.parse_args()

    result = apply_patch(Path(args.source_file), dry_run=args.dry_run)
    for key, value in result.items():
        print(f"{key}={value}")
    state = "DRY_RUN_OK" if args.dry_run else (
        "PATCH_APPLIED_VERIFIED" if result["changed"] else "ALREADY_PATCHED"
    )
    print(f"RESULT={state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
