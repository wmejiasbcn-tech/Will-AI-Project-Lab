#!/usr/bin/env python3
"""Mira unas direcciones web y deja un informe de fondo oscuro.

Comprueba tres cosas: si la página responde, cuánto tarda y cuántos días
le quedan al candado (el certificado que cifra la visita). No entra en
cuentas y no guarda secretos.
"""
from __future__ import annotations

import argparse
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def leer_objetivos(ruta: Path, extras: list[str]) -> list[str]:
    vistos: list[str] = []
    if ruta.exists():
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#"):
                vistos.append(linea)
    vistos.extend(extras)
    unicos: list[str] = []
    for url in vistos:
        if url not in unicos:
            unicos.append(url)
    return unicos


def mirar(url: str, espera: float) -> dict:
    fila = {"url": url, "estado": "—", "ms": "—", "candado": "—", "nota": ""}
    inicio = time.perf_counter()
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "waipl-vigilar/1"})
        with urllib.request.urlopen(req, timeout=espera) as resp:
            resp.read(1024)
            fila["estado"] = str(resp.status)
    except urllib.error.HTTPError as exc:
        fila["estado"] = str(exc.code)
        fila["nota"] = "respondió con error"
    except Exception as exc:
        fila["nota"] = type(exc).__name__
    fila["ms"] = str(int((time.perf_counter() - inicio) * 1000))

    host = url.split("://", 1)[-1].split("/", 1)[0].split(":", 1)[0]
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(__import__("socket").create_connection((host, 443), espera), server_hostname=host) as sock:
            cert = sock.getpeercert()
        caduca = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        dias = (caduca - datetime.now(timezone.utc)).days
        fila["candado"] = str(dias)
    except Exception as exc:
        if fila["candado"] == "—":
            fila["candado"] = "sin dato"
            if not fila["nota"]:
                fila["nota"] = type(exc).__name__
    return fila


def html(filas: list[dict], minimo: int) -> str:
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    cuerpo = []
    for f in filas:
        malo = not str(f["estado"]).startswith("2")
        try:
            candado_mal = int(f["candado"]) < minimo
        except ValueError:
            candado_mal = True
        color = "#E6E6E6" if not (malo or candado_mal) else "#F0C674"
        cuerpo.append(
            "<tr>"
            f"<td>{f['url']}</td><td>{f['estado']}</td><td>{f['ms']}</td>"
            f"<td style=\"color:{color}\">{f['candado']}</td><td>{f['nota']}</td>"
            "</tr>"
        )
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Vigilancia web {ahora}</title>
<style>
@page{{size:210mm 297mm;margin:0}}
html,body{{margin:0;background:#121212;color:#E6E6E6}}
body{{padding:16mm 14mm;font:11pt/1.45 Georgia,serif}}
h1{{color:#fff;font-weight:normal;font-size:18pt}}
table{{border-collapse:collapse;width:100%;font-size:10pt}}
th,td{{border:1px solid #3A3A3A;padding:4px 6px;text-align:left}}
th{{background:#232323;color:#fff}}
tr:nth-child(even) td{{background:#181818}}
</style>
</head>
<body>
<h1>Vigilancia web</h1>
<p>{ahora}. Un candado con menos de {minimo} días se marca. Estado 2xx es respuesta normal.</p>
<table>
<tr><th>Dirección</th><th>Estado</th><th>Milisegundos</th><th>Días de candado</th><th>Nota</th></tr>
{''.join(cuerpo)}
</table>
</body>
</html>
"""


def main() -> None:
    p = argparse.ArgumentParser(description="Vigila direcciones web.")
    p.add_argument("--lista", default=str(Path(__file__).with_name("objetivos.txt")))
    p.add_argument("--url", action="append", default=[])
    p.add_argument("--espera", type=float, default=12)
    p.add_argument("--dias", type=int, default=14, help="Por debajo de estos días el candado se marca.")
    p.add_argument("--salida", default="")
    args = p.parse_args()

    urls = leer_objetivos(Path(args.lista), args.url)
    if not urls:
        raise SystemExit("no hay direcciones")
    filas = [mirar(url, args.espera) for url in urls]
    informe = html(filas, args.dias)
    if args.salida:
        Path(args.salida).write_text(informe, encoding="utf-8")
        print(args.salida)
    else:
        print(informe)
    fallo = False
    for f in filas:
        if not str(f["estado"]).startswith("2"):
            fallo = True
        try:
            if int(f["candado"]) < args.dias:
                fallo = True
        except ValueError:
            fallo = True
    raise SystemExit(1 if fallo else 0)


if __name__ == "__main__":
    main()
