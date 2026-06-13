# Automatizaciones del Lab

Este archivo define que puede hacer Codex en automatico.

Regla: primero se prueba manualmente. Luego se automatiza.

## Principio de coste

Prioridad absoluta a soluciones gratuitas, locales y simples.

Antes de pagar una herramienta, debe demostrarse que:

- El cuello de botella es real.
- La tarea se repite.
- El ahorro de tiempo justifica el coste.
- No hay alternativa local razonable.

## Candidatas iniciales

### 1. Revision diaria del Lab

Objetivo: revisar inbox, prioridades y proyectos activos para proponer 3 acciones ejecutivas.

Frecuencia sugerida: diaria.

Momento sugerido: manana.

Salida esperada:

- 3 prioridades del dia.
- Bloqueos que requieren decision del Soberano.
- Tareas que pueden delegarse a nodos.

Estado: pendiente de activar.

### 2. Digest de comunicacion para nodos

Objetivo: convertir capturas del inbox en paquetes listos para nodos.

Frecuencia sugerida: diaria o bajo demanda.

Salida esperada:

- Mensajes preparados por nodo.
- Preguntas faltantes.
- Recomendacion de envio.

Estado: pendiente de probar manualmente.

### 3. Auditoria semanal de proyectos

Objetivo: revisar proyectos activos, detectar bloqueos y proponer siguiente paso por proyecto.

Frecuencia sugerida: semanal.

Momento sugerido: lunes.

Salida esperada:

- Estado por proyecto.
- Riesgos.
- Decisiones pendientes.
- Proximos pasos.

Estado: pendiente de activar.

## Automatizacion recomendada para empezar

Empezar con la Revision diaria del Lab.

Por que: es pequena, barata, util y entrena el sistema sin depender de conectores externos.

## Preguntas necesarias para activarla

1. A que hora quieres recibir la revision diaria.
2. Si debe ejecutarse todos los dias o solo de lunes a viernes.
3. Si debe continuar en este mismo hilo o aparecer como tarea independiente en Codex.

## Prompt base para la revision diaria

```text
Revisa los archivos del Sistema Operativo del Lab dentro de 06_SISTEMA_OPERATIVO. Lee el inbox, prioridades, nodos, proyectos activos y automatizaciones. Devuelve una revision ejecutiva breve con: 1) tres prioridades recomendadas, 2) bloqueos que requieren decision del Soberano, 3) tareas que Codex puede preparar, 4) asuntos que deberian delegarse a nodos. No modifiques archivos salvo que el Soberano lo pida.
```
