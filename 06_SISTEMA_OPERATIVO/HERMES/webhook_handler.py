"""WAIPL-BUS webhook sink — referencia para AutoClaw / Hermes runtime.

Este archivo NO corre en GitHub. Se copia al runtime local
(waipl/agents/hermes) y se monta en POST /api/bus/webhook.

Hermes ≠ Aether. Aether no usa este handler.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any


class WebhookAuthError(Exception):
    pass


def _compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def verify_signature(raw_body: bytes, header: str | None, secret: str) -> None:
    if not secret:
        raise WebhookAuthError("HERMES_WEBHOOK_SECRET vacío")
    if not header or not header.startswith("sha256="):
        raise WebhookAuthError("falta X-Hub-Signature-256")
    expected = "sha256=" + hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    if not _compare(expected, header.strip()):
        raise WebhookAuthError("firma inválida")


def parse_event(raw_body: bytes) -> dict[str, Any]:
    data = json.loads(raw_body.decode("utf-8"))
    for key in ("issue_number", "de", "para", "sender_login", "sender_association"):
        if not data.get(key):
            raise ValueError(f"payload incompleto: {key}")
    # La identidad del nodo DE no se acepta por sí sola: el workflow debe
    # haber verificado al actor real contra los permisos del repositorio.
    if data["sender_association"] not in {"OWNER", "MEMBER", "COLLABORATOR"}:
        raise WebhookAuthError("remitente sin relación autorizada con el repositorio")
    return data


def ingest(raw_body: bytes, signature_header: str | None, secret: str | None = None) -> dict[str, Any]:
    secret = secret if secret is not None else os.environ.get("HERMES_WEBHOOK_SECRET", "")
    verify_signature(raw_body, signature_header, secret)
    event = parse_event(raw_body)
    # El runtime debe: asentar ledger, aplicar default-deny, NUNCA marcar DELIVERED.
    event["decision"] = "recorded"
    event["received"] = False
    return event
