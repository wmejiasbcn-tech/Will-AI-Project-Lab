# Positrón — Segundo Cerebro Positrónico WAIPL

Repositorio de Positrón, segundo cerebro positrónico del WAIPL y para la transferencia de datos a Vercel.

Centro de mando interactivo del Soberano William L. Mejías Navarro.
**ADN** Super Plantilla Maestra Canónica v3.0 · HACR-IA · Directiva Transversal v1.0 · Prompting 2026

## Nodo canónico

- **ID** `positron`
- **Nodo** #35 de 46
- **Círculo** Estructura
- **Verify** Ejecutar (artefacto comprobable)
- **Creado por** Z.ai
- **Jurisdicción** Cerebro operativo

## Stack técnico

| Componente | Tecnología |
|------------|-----------|
| Framework | Next.js 16 + App Router + TypeScript 5 |
| Base de datos | PostgreSQL (Vercel Postgres / Neon) via Prisma ORM |
| LLM | z-ai-web-dev-sdk |
| Voz | Web Speech API + ElevenLabs |
| UI | Tailwind CSS 4 + shadcn/ui + Lucide |
| Diseño | Cyberpunk dark mode, glassmorphism |

## Migración SQLite a PostgreSQL

```bash
npm install
npx prisma generate
npx prisma migrate deploy
cp .env.example .env.local
npm run dev
```

## Documentación

- `FICHA.md` — Ficha canónica del nodo #35
- `MIGRATION_GUIDE.md` — Guía de migración SQLite a PostgreSQL
- `SCI_INTEGRATION.md` — Requisitos de integración SCI/n8n (48 secciones)

## Estado

- **Código fuente** Pendiente de subida desde sandbox Z.ai
- **Infraestructura** Schema PostgreSQL + dependencias + config Vercel listas
- **SCI** Contrato de integración definido (endpoint `/api/sci/webhook`)
- **Producción** Pendiente de deploy en Vercel
