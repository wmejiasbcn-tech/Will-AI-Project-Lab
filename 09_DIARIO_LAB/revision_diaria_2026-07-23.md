# Revision diaria del Lab - 2026-07-23

## Estado general

Piloto manual de revision diaria iniciado por decision del Soberano.

## Tres prioridades recomendadas

1. Ejecutar la revision diaria manual durante 3 dias.
   - Objetivo: comprobar si reduce carga operativa sin crear ruido.
   - Responsable: Codex / Nauta.

2. Revisar seguridad de archivos sensibles.
   - Objetivo: confirmar que claves, tokens y credenciales no quedan versionados ni expuestos.
   - Nota: los archivos raiz con nombres sensibles estan ignorados por `.gitignore`, pero existe un archivo versionado llamado `04_DOCUMENTACION/test_token.txt` que debe revisarse sin exponer su contenido.

3. Mantener foco en el Sistema Operativo del Lab.
   - Objetivo: cerrar el piloto antes de abrir digest de nodos o auditoria semanal.
   - Criterio: si tras 3 dias aporta claridad, convertirlo en automatizacion recurrente.

## Bloqueos que requieren decision del Soberano

- Tras 3 revisiones: decidir si la revision diaria se automatiza.
- Definir si la futura automatizacion sera todos los dias o solo lunes a viernes.
- Confirmar tratamiento del archivo versionado `04_DOCUMENTACION/test_token.txt`.

## Tareas que Codex puede preparar

- Segunda revision diaria manual.
- Propuesta de automatizacion recurrente despues del piloto.
- Lista segura de archivos potencialmente sensibles, sin leer ni imprimir secretos.

## Asuntos para delegar a nodos

- Sylvia: revisar criterio documental para archivos sensibles.
- Ariadna: revisar higiene Git y confirmar que no se versionan credenciales.
- Zara: proponer flujo gratuito para automatizar la revision diaria si el piloto funciona.
