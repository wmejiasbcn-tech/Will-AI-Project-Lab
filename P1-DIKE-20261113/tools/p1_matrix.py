#!/usr/bin/env python3
"""P1 cross-platform functional matrix for the patched DIKE source."""
import argparse
import hashlib
import importlib.util
import json
import os
import platform
import sys
import tempfile


CASES = [
    ("lf_final_newline", "Línea 1: ñ á ü 中文\nLínea 2: fin.\n"),
    ("crlf_final_newline", "Línea 1: ñ á ü 中文\r\nLínea 2: fin.\r\n"),
    ("mixed_final_newline", "Línea 1\nLínea 2\r\nLínea 3\n"),
    ("utf8_non_ascii_final_newline", "Año 2026 · niño · 中文 · Ω\n"),
    ("lf_no_final_newline", "Línea 1\nLínea 2"),
    ("crlf_no_final_newline", "Línea 1\r\nLínea 2"),
]


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_dike(source_path):
    spec = importlib.util.spec_from_file_location("dike_auditora_p1", source_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.DikeAuditora


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    source_hash = sha256_file(args.source)
    source_match = source_hash == args.expected_sha

    DikeAuditora = load_dike(args.source)
    tmp = tempfile.mkdtemp(prefix="p1_matrix_")
    vault = os.path.join(tmp, "vault")
    os.makedirs(vault, exist_ok=True)
    dike = DikeAuditora(vault_path=vault)

    results = []
    for name, text in CASES:
        expected = text.encode("utf-8")
        entry = dike.ingest_corpus_document(
            title=f"P1 matrix {name}",
            source_url="https://example.invalid/p1",
            content_text=text,
            normative_type="AI_ACT",
        )
        stored = entry["stored_path"]
        raw = open(stored, "rb").read()
        index = json.load(open(os.path.join(vault, "04-PROFESIONAL", "corpus_index.json"), encoding="utf-8"))
        indexed = next(x for x in index["documentos"] if x["uuid"] == entry["uuid"])
        results.append({
            "case": name,
            "input_bytes": len(expected),
            "stored_bytes": len(raw),
            "index_size_bytes": indexed["size_bytes"],
            "bytes_equal": raw == expected,
            "sha256_disk": hashlib.sha256(raw).hexdigest(),
            "sha256_index": indexed["sha256"],
            "sha256_equal": hashlib.sha256(raw).hexdigest() == indexed["sha256"],
            "length_equal": len(raw) == indexed["size_bytes"],
            "has_final_newline": raw.endswith(b"\n"),
            "has_crlf": b"\r\n" in raw,
        })

    ok = source_match and all(
        r["bytes_equal"] and r["sha256_equal"] and r["length_equal"]
        for r in results
    )
    report = {
        "label": args.label,
        "platform": platform.platform(),
        "python": sys.version,
        "source": os.path.abspath(args.source),
        "source_sha256": source_hash,
        "expected_sha256": args.expected_sha,
        "source_match": source_match,
        "cases": results,
        "result": "PASS" if ok else "FAIL",
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
