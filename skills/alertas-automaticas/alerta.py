#!/usr/bin/env python3
"""Arma una alerta sin guardar secretos ni llamar a servicios externos."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

FORMATO = "%Y-%m-%d %H:%M"

def fecha_local(valor: str, zona: ZoneInfo, etiqueta: str) -> datetime:
    naive = datetime.strptime(valor, FORMATO)
    aware = naive.replace(tzinfo=zona)
    vuelta = aware.astimezone(timezone.utc).astimezone(zona).replace(tzinfo=None)
    if vuelta != naive:
        raise SystemExit(f"{etiqueta}: la hora local {valor} no existe por el cambio horario")
    return aware

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
    inicio = fecha_local(args.cuando, zona, "Inicio")
    fin = fecha_local(args.hasta, zona, "Fin") if args.hasta else None
    if fin and fin.astimezone(timezone.utc) <= inicio.astimezone(timezone.utc):
        raise SystemExit("el fin tiene que ser posterior al inicio")

    avisos = []
    for trozo in args.antes.split(","):
        trozo = trozo.strip()
        if not trozo:
            continue
        minutos = int(trozo)
        if minutos < 0:
            raise SystemExit("un aviso no puede ir después de la hora")
        # Restar tiempo transcurrido en UTC evita generar horas locales inexistentes.
        momento = (inicio.astimezone(timezone.utc) - timedelta(minutes=minutos)).astimezone(zona)
        avisos.append((minutos, momento))

    lineas = [
        f"# {args.titulo}",
        "",
        f"- Zona: {args.zona}",
        f"- Empieza: {inicio.strftime(FORMATO)}",
    ]
    if fin:
        lineas.append(f"- Termina: {fin.strftime(FORMATO)}")
    if args.enlace:
        lineas.append(f"- Enlace: {args.enlace}")
    lineas += ["", "## Avisos", ""]
    for minutos, momento in avisos:
        lineas.append(f"- {minutos} min antes: {momento.strftime(FORMATO)}")
    lineas.append(f"- A la hora: {inicio.strftime(FORMATO)}")
    if args.nota:
        lineas += ["", args.nota]
    lineas += ["", "## Texto para el calendario", "", args.titulo, f"Empieza {inicio.strftime(FORMATO)} ({args.zona})."]
    if fin:
        lineas.append(f"Termina {fin.strftime(FORMATO)}.")
    for minutos, momento in avisos:
        lineas.append(f"Aviso a las {momento.strftime('%H:%M')}.")
    if args.enlace:
        lineas.append(args.enlace)
    lineas += ["", "## Texto para Sentinel", "", "DE: aether · PARA: sentinel · TIPO: aviso operativo", "", "Orden del Soberano. No es canon.", "", args.titulo, f"Empieza: {inicio.strftime(FORMATO)} {args.zona}."]
    if fin:
        lineas.append(f"Termina: {fin.strftime(FORMATO)}.")
    for minutos, momento in avisos:
        lineas.append(f"- {momento.strftime('%H:%M')} — aviso de {minutos} minutos.")
    lineas.append(f"- {inicio.strftime('%H:%M')} — empieza.")
    if args.enlace:
        lineas.append(f"Enlace: {args.enlace}")
    print("\n".join(lineas))

if __name__ == "__main__":
    main()
