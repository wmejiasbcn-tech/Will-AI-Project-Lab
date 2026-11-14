#!/usr/bin/env python3
"""Mira direcciones web y deja un informe de fondo oscuro.

Anota respuesta, tardanza, vigencia del certificado y cambios de contenido.
No entra en cuentas y no guarda secretos.
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VERSION_HUELLA = "sha256-bytes-v1"

def leer_lineas(ruta: Path) -> list[str]:
    if not ruta.exists():
        return []
    return [
        linea.strip()
        for linea in ruta.read_text(encoding="utf-8").splitlines()
        if linea.strip() and not linea.strip().startswith("#")
    ]

def leer_objetivos(ruta: Path, extras: list[str]) -> list[str]:
    unicos: list[str] = []
    for url in leer_lineas(ruta) + extras:
        if url not in unicos:
            unicos.append(url)
    return unicos

def leer_umbrales(ruta: Path, aviso: int | None, corte: int | None) -> tuple[int, int]:
    valores = {"aviso": 800, "corte": 2000}
    for linea in leer_lineas(ruta):
        if "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        clave = clave.strip()
        if clave in valores:
            valores[clave] = int(valor.strip())
    if aviso is not None:
        valores["aviso"] = aviso
    if corte is not None:
        valores["corte"] = corte
    if valores["aviso"] < 0 or valores["corte"] < valores["aviso"]:
        raise SystemExit("el corte tiene que ser mayor o igual que el aviso, y ninguno negativo")
    return valores["aviso"], valores["corte"]

def huella_de_stream(flujo, tamano: int = 64 * 1024) -> str:
    """Calcula la huella incrementalmente sobre los bytes originales de la respuesta.

    No decodifica el contenido ni lo copia en memoria: conserva cualquier charset
    y permite detectar cambios en respuestas de cualquier tamaño.
    """
    digest = hashlib.sha256()
    while True:
        bloque = flujo.read(tamano)
        if not bloque:
            break
        digest.update(bloque)
    return digest.hexdigest()

def mirar(url: str, espera: float) -> dict:
    fila = {"url": url, "estado": "—", "ms": "—", "candado": "—", "huella": hashlib.sha256(b"").hexdigest(), "nota": ""}
    try:
        partes = urllib.parse.urlsplit(url)
        if partes.scheme not in ("https", "http") or not partes.hostname or partes.username or partes.password:
            raise ValueError("dirección no admitida")
        host = partes.hostname
        puerto = partes.port or (443 if partes.scheme == "https" else 80)
    except (ValueError, TypeError):
        fila["nota"] = "dirección no admitida"
        return fila

    inicio = time.perf_counter()
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "waipl-vigilar/1"})
        with urllib.request.urlopen(req, timeout=espera) as resp:
            fila["huella"] = huella_de_stream(resp)
            fila["estado"] = str(resp.status)
    except urllib.error.HTTPError as exc:
        fila["estado"] = str(exc.code)
        fila["nota"] = "respondió con error"
        try:
            fila["huella"] = huella_de_stream(exc)
        except Exception:
            fila["huella"] = hashlib.sha256(b"").hexdigest()
    except Exception as exc:
        fila["nota"] = type(exc).__name__
    fila["ms"] = str(int((time.perf_counter() - inicio) * 1000))

    if partes.scheme == "http":
        fila["candado"] = "no aplica"
    else:
        try:
            ctx = ssl.create_default_context()
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            with ctx.wrap_socket(__import__("socket").create_connection((host, puerto), espera), server_hostname=host) as sock:
                cert = sock.getpeercert()
            caduca = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            fila["candado"] = str((caduca - datetime.now(timezone.utc)).days)
        except Exception as exc:
            fila["candado"] = "sin dato"
            if not fila["nota"]:
                fila["nota"] = type(exc).__name__
    return fila

def detectar(antes: dict | None, fila: dict, aviso: int, corte: int) -> tuple[str, bool]:
    partes: list[str] = []
    fallo = False
    if antes is None:
        partes.append("primera mirada")
    else:
        if antes.get("estado") != fila["estado"]:
            partes.append(f"estado {antes.get('estado')} → {fila['estado']}")
        if antes.get("huella_version") != VERSION_HUELLA:
            # Las huellas previas usaban otra normalización. Renovar la referencia
            # evita presentar el cambio de algoritmo como un cambio real de la página.
            partes.append("referencia renovada (cambio de algoritmo de huella)")
        elif "huella" not in antes:
            partes.append("sin huella anterior")
        elif antes.get("huella") != fila["huella"]:
            partes.append("cambió el contenido")
        if not partes:
            partes.append("igual")
    try:
        ms = int(fila["ms"])
    except (ValueError, TypeError):
        ms = None
    if ms is not None and ms >= corte:
        partes.append(f"pasó el corte de {corte} ms")
        fallo = True
    elif ms is not None and ms >= aviso:
        partes.append(f"pasó el aviso de {aviso} ms")
    return "; ".join(partes), fallo

def html(filas: list[dict], minimo: int, aviso: int, corte: int) -> str:
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    cuerpo = []
    for f in filas:
        malo = not str(f["estado"]).startswith("2") or f["fallo"]
        try:
            candado_mal = int(f["candado"]) < minimo
        except (ValueError, TypeError):
            candado_mal = f["candado"] != "no aplica"
        color = "#F0C674" if (malo or candado_mal or "pasó el aviso" in f["cambio"] or "cambió" in f["cambio"] or "estado" in f["cambio"]) else "#E6E6E6"
        cuerpo.append(
            "<tr>"
            f"<td>{html_lib.escape(f['url'], quote=True)}</td>"
            f"<td>{html_lib.escape(str(f['estado']), quote=True)}</td>"
            f"<td>{html_lib.escape(str(f['ms']), quote=True)}</td>"
            f"<td style=\"color:{color}\">{html_lib.escape(str(f['candado']), quote=True)}</td>"
            f"<td style=\"color:{color}\">{html_lib.escape(str(f['cambio']), quote=True)}</td>"
            f"<td>{html_lib.escape(str(f['nota']), quote=True)}</td>"
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
<p>{ahora}. Aviso de tardanza: {aviso} ms. Corte: {corte} ms. Candado marcado por debajo de {minimo} días. Estado 2xx es respuesta normal.</p>
<table>
<tr><th>Dirección</th><th>Estado</th><th>Milisegundos</th><th>Días de candado</th><th>Cambio</th><th>Nota</th></tr>
{''.join(cuerpo)}
</table>
</body>
</html>
"""

def main() -> None:
    aqui = Path(__file__).parent
    p = argparse.ArgumentParser(description="Vigila direcciones web.")
    p.add_argument("--lista", default=str(aqui / "objetivos.txt"))
    p.add_argument("--umbrales", default=str(aqui / "umbrales.txt"))
    p.add_argument("--estado", default=str(aqui / "estado.json"))
    p.add_argument("--url", action="append", default=[])
    p.add_argument("--espera", type=float, default=12)
    p.add_argument("--dias", type=int, default=14, help="Por debajo de estos días el candado se marca.")
    p.add_argument("--aviso", type=int, default=None, help="Milisegundos a partir de los que se marca la tardanza.")
    p.add_argument("--corte", type=int, default=None, help="Milisegundos a partir de los que la vigilancia falla.")
    p.add_argument("--salida", default="")
    args = p.parse_args()

    aviso, corte = leer_umbrales(Path(args.umbrales), args.aviso, args.corte)
    urls = leer_objetivos(Path(args.lista), args.url)
    if not urls:
        raise SystemExit("no hay direcciones")

    ruta_estado = Path(args.estado)
    anterior = json.loads(ruta_estado.read_text(encoding="utf-8")) if ruta_estado.exists() else {}
    filas = []
    nuevo = {}
    fallo = False
    for url in urls:
        fila = mirar(url, args.espera)
        cambio, tardo = detectar(anterior.get(url), fila, aviso, corte)
        fila["cambio"] = cambio
        fila["fallo"] = tardo
        filas.append(fila)
        nuevo[url] = {"estado": fila["estado"], "huella": fila["huella"], "huella_version": VERSION_HUELLA, "ms": fila["ms"], "cuando": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        if not str(fila["estado"]).startswith("2") or tardo:
            fallo = True
        try:
            if int(fila["candado"]) < args.dias:
                fallo = True
        except (ValueError, TypeError):
            if fila["candado"] != "no aplica":
                fallo = True

    ruta_estado.write_text(json.dumps(nuevo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    informe = html(filas, args.dias, aviso, corte)
    if args.salida:
        Path(args.salida).write_text(informe, encoding="utf-8")
        print(args.salida)
    else:
        print(informe)
    for f in filas:
        print(f"{f['url']}  {f['estado']}  {f['ms']} ms  {f['cambio']}")
    raise SystemExit(1 if fallo else 0)

if __name__ == "__main__":
    main()
