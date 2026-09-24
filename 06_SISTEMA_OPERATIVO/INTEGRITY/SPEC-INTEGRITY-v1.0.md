# SPEC-INTEGRITY v1.0 — Verificación de integridad

**Estado:** especificado e implementado · 2026-08-23  
**Rige:** Principio 12, Cero Invención, Trazabilidad Completa  
**Cierra:** el hash `9ade0a9e…` de Z (autoincluido, no verificable) y el recuento 12/13 de hiperaristas.

## Objetivo

Un archivo canónico tiene un SHA-256 **fuera** de sí mismo. Cualquiera puede repetir el cálculo. Un informe que cite un hash no listado aquí es INFERRED, no VERIFIED.

## Alcance

**Dentro:** blob Git (bytes UTF-8, LF) de los paths en `MANIFEST.json`. Chequeo estructural de `graph.json`. Action en push/PR.

**Fuera:** hashear el propio `MANIFEST.json` dentro de sí mismo. Restaurar nodos del grafo (eso es DES-001, otro N3). Runtime de Hermes/Positrón.

## Evidencia

- Algoritmo: SHA-256, hex minúsculas.
- Canon de bytes: el blob de Git, no el render de GitHub.
- El hash **no** se escribe dentro del documento hasheado.

## Éxito

`python3 06_SISTEMA_OPERATIVO/INTEGRITY/verify_integrity.py` sale 0 en CI. Un byte cambiado en un path del manifiesto sale 1.

## Parada

- Hash incrustado en el archivo y presentado como el hash del archivo → STOP.
- Recuento de hiperaristas por arrays duplicados (11 IDs × 2 = 22) presentado como 12 o 13 → STOP.
- `graph.json` que no parsea → STOP.

## Recuento de grafo (regla)

Únicos `id` en `graph.hyperedges` (si vacío, en `hyperedges` raíz). No se suman las dos listas. `nodes: []` en GitHub es un **aviso**, no un restore silencioso.
