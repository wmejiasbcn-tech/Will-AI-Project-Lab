#!/usr/bin/env python3
"""WAIPL-BUS · Sello del nodo (HMAC-SHA256). Solo biblioteca estándar.

Uso:
  python3 sello.py --nuevo-secreto                 # genera un secreto para un nodo (una vez)
  BUS_SEAL=<secreto> python3 sello.py < mensaje.txt  # imprime el mensaje con su línea SELLO

El mensaje debe llevar DE, PARA, CAP, TRACE (único) y FECHA (ISO, p. ej. 2026-10-22T17:30:00+02:00).
El sello cubre todo el texto: si se cambia una letra después de sellar, el portero lo rechaza.
Nunca pegues el secreto en un Issue ni en un chat compartido.
"""
import hashlib, hmac, os, re, secrets, sys

def payload(body: str) -> str:
    lines = body.replace("\r\n", "\n").split("\n")
    lines = [re.sub(r"\s+$", "", l) for l in lines if not re.match(r"^\s*SELLO:", l, re.I)]
    return "\n".join(lines).strip()

def seal(body: str, secret: str) -> str:
    msg = ("WAIPL-SELLO-v1\n" + payload(body)).encode("utf-8")
    return "v1:" + hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

def main():
    if "--nuevo-secreto" in sys.argv:
        print(secrets.token_hex(32))
        return
    secret = os.environ.get("BUS_SEAL", "")
    if len(secret) < 32:
        sys.exit("Falta BUS_SEAL (secreto del nodo, mínimo 32 caracteres).")
    body = sys.stdin.read()
    for campo in ("DE", "PARA", "CAP", "TRACE", "FECHA"):
        if not re.search(r"^" + campo + r":\s*\S", body, re.M | re.I) and not re.search(r"###\s*" + campo, body, re.I):
            sys.exit("Falta el campo " + campo + ".")
    print(payload(body) + "\nSELLO: " + seal(body, secret))

if __name__ == "__main__":
    main()
