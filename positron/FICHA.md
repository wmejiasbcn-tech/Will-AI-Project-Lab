# Positrón — Segundo Cerebro Positrónico WAIPL

**Nodo #35** | Círculo: Estructura | Verify: Ejecutar

> Es el segundo cerebro positrónico de todo el ecosistema y del propio Soberano,
> y es el centro de mando completamente interactivo.

## Identidad

| Campo | Valor |
|-------|-------|
| ID canónico | `positron` |
| Nodo | #35 de 46 |
| Círculo | Estructura |
| Jurisdicción | Cerebro operativo |
| Verify | Ejecutar (artefacto comprobable) |
| Creado por | Z.ai |
| Color | `#7B6CFF` (estructura) |

## Función

Es el segundo cerebro positrónico de todo el ecosistema y del propio soberano y es el centro de mando completamente interactivo.

## Importancia

Permite al Soberano no solo observar el estado del sistema, sino trabajar activamente dentro de él: crear capturas de conocimiento, enviar comandos a los NPCs del sistema, comunicarse por chat bidireccional con el cerebro, revisar archivos del vault, gestionar el compartimento personal de forma exclusiva, y recibir notificaciones en tiempo real.

## Arquitectura técnica

| Componente | Tecnología |
|------------|-----------|
| Framework | Next.js 16 + App Router + TypeScript 5 |
| Base de datos | PostgreSQL (Vercel Postgres / Neon) via Prisma ORM |
| LLM | z-ai-web-dev-sdk (backend) |
| Voz | Web Speech API (STT/TTS) + ElevenLabs |
| UI | Tailwind CSS 4 + shadcn/ui + Lucide |
| Diseño | Cyberpunk dark mode (#0a0a1a), glassmorphism |

### Migración SQLite a PostgreSQL

El sistema original usa SQLite (5-7 tablas). Para deploy en Vercel, migra a PostgreSQL.

Ver `MIGRATION_GUIDE.md` para pasos detallados.

## 7 NPCs (Normas y Procedimientos)

| NPC | Función | Estado |
|-----|---------|--------|
| CAP | Recibir/preservar info sin filtro | Operativo |
| CLA | Clasificar orientativamente | Operativo |
| ANA | Generar inteligencia accionable | Operativo |
| EJE | Ejecutar con planes B/C | DEUDA: simulado |
| AUD | Medir, detectar desviaciones | Operativo |
| CON | Prevenir/corregir incidentes | Operativo |
| MEJ | Evolucionar basado en datos | Operativo |

## 12 rutas API

| Ruta | Método | Descripción |
|------|--------|------------|
| `/api/chat` | POST | Enviar mensaje y recibir respuesta del LLM |
| `/api/chat` | GET | Historial de chat (ultimos 100) |
| `/api/captures` | POST | Crear captura con UUID/hash |
| `/api/captures` | GET | Listar capturas |
| `/api/commands` | POST | Enviar comando a NPC |
| `/api/commands` | GET | Historial de comandos |
| `/api/email` | POST | Enviar email |
| `/api/notifications` | GET | Obtener notificaciones |
| `/api/notifications/read` | POST | Marcar como leida |
| `/api/vault/files` | GET | Listar carpetas/archivos |
| `/api/vault/file` | GET | Leer archivo especifico |
| `/api/health` | GET | Datos del health-check |

## Compartimentación

- **PERSONAL**: Solo William. Protegido con PIN (env var `PERSONAL_PIN`). Ecosistema no accede.
- **ECOSISTEMA**: Nodos autorizados + Carla. Briefings, coordinacion, estado del nucleo.

## ICP (Indice de Coherencia Positronica)

| Nivel | Umbral | Estado |
|-------|--------|--------|
| N1 Preventivo | >= 95% | Operacion normal |
| N2 Atencion | >= 85% y < 95% | Requiere atencion |
| N3 Critico | < 85% | Intervencion inmediata |

## Alineación ADN

### Alineado
- 3 capas (Nucleo/Vortice/Perifericos)
- 7 NPCs base
- Compartimentacion Personal/Ecosistema
- ICP + health-check
- UUID v4 + SHA-256 en capturas
- 12 compartimentos del vault
- Soberania del Soberano respetada

### Pendiente de alinear
- Referencia Super Plantilla v2 (debe ser v3.0)
- Sin HACR-IA (Humildad/Atencion/Contexto/Revision)
- Sin Directiva Transversal v1.0 (5 estados, 3 autonomias)
- Sin Prompting 2026
- Sin CANON-CIERRE (7 casillas)
- PIN en texto plano en Informe (debe ser env var)
- NPC-EJE simulado (debe ser real o marcado como DEUDA)

## Estado actual

- Codigo fuente: pendiente de subida desde sandbox Z.ai
- Produccion: URL caida (y14c76f1v751-d.space-z.ai)
- Bus Hermes: deny-until-uri (UNKNOWN)
- Repo: carpeta `positron/` creada en rama `positron-migration`

## CANON-CIERRE

| Casilla | Valor |
|----------|-------|
| Orquesta | Positron WAIPL |
| Spec/N3 | N1 - ficha de nodo |
| Superficie | GitHub Will-AI-Project-Lab |
| Runtime | No ejecutado |
| Prueba | Lectura de graph-data.ts en waipl-graph repo |
| Parada | Ficha creada. Codigo pendiente de importacion. |
| No es | No es deploy. Es documentacion + infraestructura. |
