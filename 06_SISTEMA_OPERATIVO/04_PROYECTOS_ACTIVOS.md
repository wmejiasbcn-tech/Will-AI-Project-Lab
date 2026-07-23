# Proyectos Activos

Este archivo permite ver que esta vivo, que esta bloqueado y cual es el siguiente paso.

## Vista ejecutiva

| Proyecto | Estado | Responsable sugerido | Proximo paso | Bloqueo |
| --- | --- | --- | --- | --- |
| Sistema Operativo del Lab | Piloto manual iniciado | Nauta / Codex | Ejecutar 3 revisiones diarias y evaluar automatizacion | Evaluar valor tras 3 dias |
| Sistema de Comunicacion Interna Make + SDD | En estudio | Nauta / Carla / Ada | Validar DS-001 y definir piloto | Definir SDD y registro inicial |
| WILL-App | Activo por confirmar | Aletheia/Ariadna | Revisar documento base | Pendiente de priorizacion |
| Vertigos | Activo por confirmar | Aether/Aurea/Nova | Revisar estado de entregables | Pendiente de priorizacion |
| Sider/Wisebase documental | Activo por confirmar | Sylvia/Itaca | Verificar indice maestro | Pendiente de priorizacion |

## Plantilla de proyecto

```md
## Nombre del proyecto

Estado:
Responsable principal:
Nodos de apoyo:
Objetivo:
Por que importa:
Ultimo avance:
Proximo paso:
Bloqueo actual:
Decision requerida del Soberano:
Archivos relacionados:
```

## Sistema Operativo del Lab

Estado: piloto manual iniciado por decision del Soberano.

Responsable principal: Nauta / Codex.

Nodos de apoyo: Carla, Sylvia, Aletheia, Zara.

Objetivo: crear una capa operativa que reduzca el cuello de botella del Soberano.

Por que importa: permite pasar de comunicacion centralizada a comunicacion coordinada.

Ultimo avance: iniciada la revision diaria manual del Lab el 2026-07-23.

Proximo paso: ejecutar 3 revisiones diarias y decidir si se convierte en automatizacion recurrente.

Bloqueo actual: ninguno critico. Queda evaluar si el piloto aporta valor suficiente.

Decision requerida del Soberano: tras 3 dias, confirmar si se automatiza la revision diaria.

Archivos relacionados:

- `00_MESA_CONTROL_LAB.md`
- `01_INBOX.md`
- `02_PRIORIDADES.md`
- `03_NODOS_COMUNICACION.md`
- `05_AUTOMATIZACIONES.md`

## Sistema de Comunicacion Interna Make + SDD

Estado: en estudio.

Responsable principal: Nauta / Codex.

Nodos de apoyo: Carla, Ada, Sylvia, Ariadna, Zara.

Objetivo: estudiar y pilotar un mecanismo interno de comunicacion para que los nodos puedan emitir propuestas, bloqueos y estados sin que todo pase manualmente por el Soberano.

Por que importa: reduce el cuello de botella comunicacional y convierte el PSI en flujo operativo real.

Ultimo avance: creada `Discusiones/ABIERTAS/DS-001-sistema-comunicacion-interna-make-sdd.md`.

Proximo paso: validar con el Soberano el significado oficial de SDD y elegir el registro inicial del piloto.

Bloqueo actual: falta definicion final de SDD y decision entre GitHub Issues, GitHub Discussions o carpeta `Discusiones/`.

Decision requerida del Soberano: confirmar si empezamos con el piloto minimo `Webhook Make -> GitHub Issue -> revision`.

Archivos relacionados:

- `Discusiones/ABIERTAS/DS-001-sistema-comunicacion-interna-make-sdd.md`
- `06_SISTEMA_OPERATIVO/PSI/PSI_v1.1_OFICIAL.md`
- `Discusiones/README.md`
- `06_SISTEMA_OPERATIVO/BROADCAST.md`
- `03_PERSONAS_IA/ZARA/PROTOCOLO_RECALIBRACION_OPERATIVA_ZARA.md`
