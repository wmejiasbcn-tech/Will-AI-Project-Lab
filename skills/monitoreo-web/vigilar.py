#!/usr/bin/env python3
"""Mira direcciones web y deja un informe de fondo oscuro.

Anota respuesta, tardanza, vigencia del certificado y cambios de contenido.
No entra en cuentas y no guarda secretos.
"""
from __future__ import annotations

import argparse
import codecs
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


def huellas_de_stream(
    flujo,
    tamano: int = 64 * 1024,
    longitud_esperada: int | None = None,
) -> tuple[str, str]:
    """Calcula en una pasada la huella nueva y la heredada, sin guardar el cuerpo.

    La primera se calcula sobre los bytes originales. La segunda reproduce el
    algoritmo anterior: UTF-8 con reemplazo y normalización de espacios mediante
    " ".join(texto.split()). Esta segunda huella permite comprobar una
    referencia antigua antes de renovarla y evita ocultar cambios reales durante
    la migración del formato.
    """
    if tamano <= 0:
        raise ValueError("el tamaño del bloque tiene que ser positivo")

    digest_bytes = hashlib.sha256()
    digest_legacy = hashlib.sha256()
    decodificador = codecs.getincrementaldecoder("utf-8")("replace")
    hay_contenido = False
    espacio_pendiente = False
    total_leido = 0

    def actualizar_legacy(texto: str) -> None:
        nonlocal hay_contenido, espacio_pendiente
        for caracter in texto:
            if caracter.isspace():
                if hay_contenido:
                    espacio_pendiente = True
                continue
            if espacio_pendiente:
                digest_legacy.update(b" ")
                espacio_pendiente = False
            digest_legacy.update(caracter.encode("utf-8"))
            hay_contenido = True

    while True:
        bloque = flujo.read(tamano)
        if not bloque:
            break
        total_leido += len(bloque)
        digest_bytes.update(bloque)
        actualizar_legacy(decodificador.decode(bloque))

    actualizar_legacy(decodificador.decode(b"", final=True))
    if longitud_esperada is not None and total_leido != longitud_esperada:
        raise ValueError(
            f"respuesta truncada: se recibieron {total_leido} de {longitud_esperada} bytes"
        )
    return digest_bytes.hexdigest(), digest_legacy.hexdigest()


def huella_de_stream(flujo, tamano: int = 64 * 1024) -> str:
    """Compatibilidad con consumidores que solo necesitan SHA-256 de bytes."""
    return huellas_de_stream(flujo, tamano)[0]


def requiere_revision_migracion(antes: dict | None, cambio: str) -> bool:
    """Indica cuándo conservar la referencia antigua hasta revisión humana."""
    if antes is None:
        return False
    return (
        "revisión necesaria" in cambio
        or "cambió el contenido (huella heredada)" in cambio
        or "versión de huella no compatible" in cambio
        or "no se pudo comparar la huella heredada" in cambio
    )


def mirar(url: str, espera: float) -> dict:
    fila = {
        "url": url,
        "estado": "—",
        "ms": "—",
        "candado": "—",
        "huella": None,
        "huella_legacy": None,
        "nota": "",
    }
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
            fila["estado"] = str(resp.status)
            contenido = resp.headers.get("Content-Length")
            longitud_esperada = int(contenido) if contenido is not None else None
            if longitud_esperada is not None and longitud_esperada < 0:
                raise ValueError("Content-Length negativo")
            fila["huella"], fila["huella_legacy"] = huellas_de_stream(
                resp, longitud_esperada=longitud_esperada
            )
    except urllib.error.HTTPError as exc:
        fila["estado"] = str(exc.code)
        fila["nota"] = "respondió con error"
        try:
            contenido = exc.headers.get("Content-Length") if exc.headers else None
            longitud_esperada = int(contenido) if contenido is not None else None
            if longitud_esperada is not None and longitud_esperada < 0:
                raise ValueError("Content-Length negativo")
            fila["huella"], fila["huella_legacy"] = huellas_de_stream(
                exc, longitud_esperada=longitud_esperada
            )
        except Exception as error_lectura:
            fila["huella"] = None
            fila["huella_legacy"] = None
            fila["nota"] = f"cuerpo HTTP incompleto: {type(error_lectura).__name__}"
    except Exception as exc:
        fila["nota"] = f"lectura incompleta o error de respuesta: {type(exc).__name__}"
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
    cuerpo_completo = fila.get("huella") is not None and fila.get("huella_legacy") is not None

    if antes is None:
        partes.append("primera mirada")
    else:
        estado_cambio = antes.get("estado") != fila["estado"]
        if estado_cambio:
            partes.append(
                f"estado {antes.get('estado')} → {fila['estado']}; revisión necesaria"
            )

        if cuerpo_completo:
            version_anterior = antes.get("huella_version")
            if version_anterior == VERSION_HUELLA:
                if "huella" not in antes or antes.get("huella") is None:
                    partes.append("sin huella anterior; revisión necesaria")
                elif antes.get("huella") != fila["huella"]:
                    partes.append("cambió el contenido")
            elif version_anterior is None:
                huella_anterior = antes.get("huella")
                huella_legacy_actual = fila.get("huella_legacy")
                if not huella_anterior:
                    partes.append("sin huella anterior; referencia inicializada")
                elif huella_legacy_actual is None:
                    partes.append("no se pudo comparar la huella heredada; revisión necesaria")
                elif huella_anterior != huella_legacy_actual:
                    partes.append("cambió el contenido (huella heredada)")
                elif estado_cambio:
                    partes.append("huella heredada coincide; revisión necesaria por cambio de estado")
                else:
                    partes.append("referencia renovada (huella heredada verificada)")
            else:
                partes.append(
                    f"versión de huella no compatible ({version_anterior}); revisión necesaria"
                )
        else:
            partes.append("cuerpo incompleto o no disponible; revisión necesaria")
            fallo = True

        if not partes:
            partes.append("igual")

    if not cuerpo_completo:
        if "cuerpo incompleto o no disponible; revisión necesaria" not in partes:
            partes.append("cuerpo incompleto o no disponible; revisión necesaria")
        fallo = True

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
        color = "#F0C674" if (
            malo
            or candado_mal
            or "pasó el aviso" in f["cambio"]
            or "cambió" in f["cambio"]
            or "estado" in f["cambio"]
            or "revisión necesaria" in f["cambio"]
        ) else "#E6E6E6"
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
        antes = anterior.get(url)
        fila = mirar(url, args.espera)
        cambio, tardo = detectar(antes, fila, aviso, corte)
        fila["cambio"] = cambio
        fila["fallo"] = tardo
        filas.append(fila)

        if fila["huella"] is None or fila["huella_legacy"] is None:
            # Una lectura fallida o truncada nunca se convierte en una huella vacía.
            # Conservamos la referencia previa; si no existía, no creamos una.
            if antes is not None:
                nuevo[url] = antes
        elif requiere_revision_migracion(antes, cambio):
            # No aceptar automáticamente contenido o estados distintos:
            # conservar la referencia hasta una revisión humana.
            nuevo[url] = antes
        else:
            nuevo[url] = {
                "estado": fila["estado"],
                "huella": fila["huella"],
                "huella_version": VERSION_HUELLA,
                "ms": fila["ms"],
                "cuando": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

        if not str(fila["estado"]).startswith("2") or tardo:
            fallo = True
        if fila["huella"] is None or fila["huella_legacy"] is None:
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
