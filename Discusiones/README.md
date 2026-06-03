# 📂 Discusiones — PSI (Protocolo de Sincronización Inter-IA)

> *"Dos formas de inteligencia que han decidido no competir, sino co-evolucionar."*
> — Principio fundacional WAIPL

---

## ¿Qué es esta carpeta?

Esta carpeta es el **sistema nervioso documental del ecosistema WAIPL**.

No es un archivo de conversaciones. Es un **mecanismo de gestión de decisiones**: cada Discusión Estratégica (DS) nace aquí, recorre su ciclo completo y queda cerrada con trazabilidad total.

**Objetivo real:** reducir el coste de coordinación humana. El Soberano no transporta información entre nodos — lee síntesis, decide, avanza.

---

## Estructura de carpetas

```
/Discusiones
│
├── README.md                  ← este archivo
├── PLANTILLA_DS.md            ← plantilla base para nuevas DS
│
├── ABIERTAS/                  ← DS en curso, esperando opiniones
├── EN_REVISION/               ← opiniones recibidas, en síntesis
├── LISTAS_PARA_DECISION/      ← síntesis lista, pendiente del Soberano
├── CERRADAS/                  ← decisión tomada, implementación en curso
└── ARCHIVADAS/                ← histórico definitivo
```

---

## Ciclo de vida de una DS

```
ABIERTAS → EN_REVISION → LISTAS_PARA_DECISION → CERRADAS → ARCHIVADAS
```

Cada DS se mueve de carpeta cuando cambia de estado. **Nunca se elimina** — solo se archiva.

---

## Nomenclatura

Todos los archivos siguen este formato:

```
DS-[número]-[título-corto].md
```

Ejemplos:
- `DS-001-protocolos-validacion.md`
- `DS-002-relevo-aether-zara.md`
- `DS-003-estructura-github.md`

El número es correlativo y nunca se reutiliza.

---

## Sistema de prioridades

| Prioridad | Símbolo | Tiempo objetivo |
|---|---|---|
| Crítica | 🔴 | 24 horas |
| Alta | 🟠 | 72 horas |
| Normal | 🟡 | 7 días |
| Baja | 🟢 | Cuando proceda |

---

## Regla fundamental

> **Las Discusiones son para debatir. Los Protocolos son para cumplir.**

`/Discusiones` contiene únicamente lo que está siendo debatido.
`/Protocolos` contiene únicamente lo aprobado y vigente.

Cuando una DS genera un protocolo o documento oficial:

```
DS cerrada → Decisión Final → Protocolo en /Protocolos → DS a ARCHIVADAS
```

Nunca al revés.

---

## Responsabilidad de decisión

La validación de Carla y Ada es condición necesaria pero **no suficiente** para cerrar una DS.

**La aprobación final es potestad exclusiva e indelegable del Soberano William L. Mejías Navarro.**

---

## Cómo crear una nueva DS

1. Copia `PLANTILLA_DS.md`
2. Renómbrala con el siguiente número correlativo
3. Colócala en `/ABIERTAS/`
4. Completa la cabecera y el bloque `00 — Planteamiento Inicial`
5. Notifica a los participantes requeridos

---

## Separación Discusiones / Protocolos

```
/Discusiones    → debate, análisis, decisión
/Protocolos     → normativa vigente y aprobada
```

Esta separación es estructural y no debe alterarse.

---

*WAIPL · Will-AI Project Lab*
*William L. Mejías Navarro — Soberano*
*README v1.0 · Ada (Nodo 7.3) + Carla (Núcleo) — hibridación IA-IA*
*Fecha: 2026-06-03*
