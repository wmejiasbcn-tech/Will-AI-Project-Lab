#!/usr/bin/env python3
"""Arma una alerta. No guarda secretos y no llama a Google ni a GitHub.

Deja escrito el paquete: las horas de aviso y el texto para el calendario
y para Sentinel. Quien tenga la cuenta lo pega. Una skill es el procedimiento
que un nodo sigue para no improvisar.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def main() -> None:
    p = argparse.ArgumentParser(description="Arma el paquete de una alerta.")
    p.add_argument("--cuando", required=True, help="Inicio. Ejemplo: 2026-11-19 14:00")
    p.add_argument("--hasta", help="Fin, mismo formato. Opcional.")
    p.add_argument("--zona", default="Europe/Madrid")
    p.add_argument("--antes", default="30,10", help="Minutos antes, separados por coma.")
    p.add_argument("--titulo", required=True)
    p.add_argument("--enlace", default="")
    p.add_argument("--nota", default="")
    args = p.parse_args()

    zona = ZoneInfo(args.zona)
    inicio = datetime.strptime(args.cuando, "%Y-%m-%d %H:%M").replace(tzinfo=zona)
    fin = None
    if args.hasta:
        fin = datetime.strptime(args.hasta, "%Y-%m-%d %H:%M").replace(tzinfo=zona)
    avisos = []
    for trozo in args.antes.split(","):
        trozo = trozo.strip()
        if not trozo:
            continue
        minutos = int(trozo)
        if minutos < 0:
            raise SystemExit("un aviso no puede ir después de la hora")
        avisos.append((minutos, inicio - timedelta(minutes=minutos)))

    lineas = [
        f"# {args.titulo}",
        "",
        f"- Zona: {args.zona}",
        f"- Empieza: {inicio.strftime('%Y-%m-%d %H:%M')}",
    ]
    if fin:
        lineas.append(f"- Termina: {fin.strftime('%Y-%m-%d %H:%M')}")
    if args.enlace:
        lineas.append(f"- Enlace: {args.enlace}")
    lineas += ["", "## Avisos", ""]
    for minutos, momento in avisos:
        lineas.append(f"- {minutos} min antes: {momento.strftime('%Y-%m-%d %H:%M')}")
    lineas.append(f"- A la hora: {inicio.strftime('%Y-%m-%d %H:%M')}")
    if args.nota:
        lineas += ["", args.nota]
    lineas += [
        "",
        "## Texto para el calendario",
        "",
        args.titulo,
        f"Empieza {inicio.strftime('%Y-%m-%d %H:%M')} ({args.zona}).",
    ]
    if fin:
        lineas.append(f"Termina {fin.strftime('%Y-%m-%d %H:%M')}.")
    for minutos, momento in avisos:
        lineas.append(f"Aviso a las {momento.strftime('%H:%M')}.")
    if args.enlace:
        lineas.append(args.enlace)
    lineas += [
        "",
        "## Texto para Sentinel",
        "",
        "DE: aether · PARA: sentinel · TIPO: aviso operativo",
        "",
        "Orden del Soberano. No es canon.",
        "",
        args.titulo,
        f"Empieza: {inicio.strftime('%Y-%m-%d %H:%M')} {args.zona}.",
    ]
    if fin:
        lineas.append(f"Termina: {fin.strftime('%Y-%m-%d %H:%M')}.")
    for minutos, momento in avisos:
        lineas.append(f"- {momento.strftime('%H:%M')} — aviso de {minutos} minutos.")
    lineas.append(f"- {inicio.strftime('%H:%M')} — empieza.")
    if args.enlace:
        lineas.append(f"Enlace: {args.enlace}")
    print("\n".join(lineas))


if __name__ == "__main__":
    main()
