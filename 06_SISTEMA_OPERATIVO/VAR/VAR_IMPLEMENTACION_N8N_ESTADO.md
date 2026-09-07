# VÁR / VAC-01 — ESTADO DE IMPLEMENTACIÓN n8n

**Fecha de corte:** 2026-09-07  
**Workflow:** `VÁR — VAC-01 — Validación de la Verdad Canónica WAIPL`  
**ID:** `HC1SkjGphGYS3P8M`

## Estado

**DRAFT · CONSTRUIDO · GUARDADO · NO PUBLICADO**

No existe autorización soberana de publicación en el estado documentado aquí.

## Cadena principal

```text
Entrada SCI — VÁR
        ↓
F1 — Recepción y Admisión
        ↓
Agente Validador — VÁR
        ↓
Construir Dictamen VAD — VÁR
        ↓
F7
```

## LLM — VÁR

El LLM — VÁR aparece asociado al Agente Validador como componente/modelo.

Formulación vigente:

> El Agente Validador — VÁR utiliza el LLM — VÁR como componente/modelo asociado y su salida se dirige a Construir Dictamen VAD — VÁR.

No se debe inferir una segunda rama, dos validadores independientes ni ejecución paralela.

## Ruta de rechazo

```text
F1 — Recepción y Admisión
        ↓
Registrar Rechazo — VÁR
        ↓
Respuesta Rechazo — VÁR
```

La ruta fue ejercitada durante una verificación en la que el campo `claim` no llegó en el formato de entrada esperado. Esta evidencia acredita el ejercicio de la ruta de rechazo en esa prueba concreta; no debe extrapolarse a otros criterios sin evidencia.

## F7

Nombre exacto:

`F7 — Registro · [PLANO A] Flujo Informacional Ecosistema · [PLANO B] Canal Avatar Soberano`

Secuencia técnica representada:

```text
A1 → A2 → A3 → B1 → B2 → Respuesta Final
```

### Plano A

- A1 — `Registrar en Audit Log — VÁR`
- A2 — `Marcar Idempotencia — VÁR`
- A3 — `Anotar Pendientes`

Destinos previstos, todos sin conexión activa:

- Positrón
- Hermes
- Graphy
- Ollama
- Carla

### Plano B

- B1 — `Preparar Entrega Directa → WILLIAM-SCY-01`
- B2 — `ENTREGAR VAD → WILLIAM-SCY-01 [AVATAR DEL SOBERANO]`

Restricciones de WILLIAM-SCY-01:

- no distribuidor;
- no gateway;
- no reenvío al ecosistema;
- no paso intermedio del flujo informacional del ecosistema.

La ejecución del workflow es **secuencial, no paralela**.

### Cierre

`Respuesta Final — VÁR Cierra el Flujo` aparece después de B2.

## Relación con Soberano

`WILLIAM-SCY-01 ↔ Soberano` se trata como relación operativa/arquitectónica externa cuando no existe conexión técnica dentro del workflow.

## Iteraciones de preview

Durante la construcción se revisaron sucesivamente previews V4, V5, V6 y V7.

El problema de solapamiento del layout automático dejó de considerarse un bloqueo estructural cuando se confirmó que, una vez finalizado el build, el canvas puede reorganizarse manualmente. El Soberano reorganizó el canvas para mejorar legibilidad y evitar solapamientos.

## Estado de integración

| Destino | Estado en F7 |
|---|---|
| Positrón | pendiente / sin conexión activa |
| Hermes | pendiente / sin conexión activa |
| Graphy | pendiente / sin conexión activa |
| Ollama | pendiente / sin conexión activa |
| Carla | pendiente / sin conexión activa |
| WILLIAM-SCY-01 | conexión técnica representada |

## No confundir

- Draft ≠ publicado.
- Arquitectura prevista ≠ conexión activa.
- Relación visual ≠ conexión técnica.
- LLM asociado ≠ rama independiente.
- VÁR → WILLIAM-SCY-01 ≠ WILLIAM-SCY-01 → ecosistema.
