#!/usr/bin/env python3
"""Comprueba las fichas de skills/ contra la convención ya escrita en skills/README.md.

No añade campos que las fichas viejas no traen. Obligatorio: carpeta, name igual
a la carpeta, description, cuerpo en castellano, fila enlazada en el índice,
y ausencia de tokens. Opcional: type, lifecycle, version.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
README = SKILLS / "README.md"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SPANISH_RE = re.compile(
    r"\b(el|la|los|las|de|que|para|con|una|este|esta|no|se)\b",
    re.IGNORECASE,
)
SECRET_RES = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |)?PRIVATE KEY-----"),
    re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
]


def fail(path: Path, message: str, errors: list[str]) -> None:
    rel = path.relative_to(ROOT)
    errors.append(f"{rel}: {message}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    raw = text[4:end]
    body = text[end + 5 :]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = value
    return fields, body


def main() -> int:
    errors: list[str] = []
    if not SKILLS.is_dir():
        print("No existe skills/.", file=sys.stderr)
        return 1
    readme = README.read_text(encoding="utf-8") if README.is_file() else ""
    if not readme:
        errors.append("skills/README.md: falta el índice de la carpeta.")

    fichas = sorted(SKILLS.glob("*/SKILL.md"))
    if not fichas:
        errors.append("skills/: no hay ninguna ficha SKILL.md.")

    for path in fichas:
        text = path.read_text(encoding="utf-8")
        folder = path.parent.name
        parsed = parse_frontmatter(text)
        if parsed is None:
            fail(path, "el frontmatter debe abrir y cerrar con una línea ---.", errors)
            continue
        fields, body = parsed
        name = fields.get("name", "").strip()
        description = fields.get("description", "").strip()
        if not name:
            fail(path, "falta name.", errors)
        elif not NAME_RE.fullmatch(name):
            fail(path, "name no está en minúsculas con guiones.", errors)
        elif name != folder:
            fail(path, f"name ({name}) no coincide con la carpeta ({folder}).", errors)
        if not description:
            fail(path, "falta description.", errors)
        if not body.strip():
            fail(path, "el cuerpo está vacío.", errors)
        elif not SPANISH_RE.search(body):
            fail(path, "el cuerpo no parece castellano.", errors)
        for secret in SECRET_RES:
            if secret.search(text):
                fail(path, "parece contener un token. Este repositorio es público.", errors)
                break
        link = f"]({folder}/SKILL.md)"
        if link not in readme and f"](./{folder}/SKILL.md)" not in readme:
            fail(path, "el índice de skills/README.md no enlaza esta ficha.", errors)

    if errors:
        print("La carpeta skills/ no cumple la convención:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    print(f"skills/: {len(fichas)} fichas cumplen la convención.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
