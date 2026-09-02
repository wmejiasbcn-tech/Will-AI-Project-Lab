# Migracion SQLite a PostgreSQL

## Cambios
1. Prisma: sqlite a postgresql, String @db.Text
2. PIN hardcoded a env var PERSONAL_PIN
3. /api/vault/* (filesystem) a GitHub API o Vercel Blob
4. react-markdown v10 a dynamic import (ssr:false)
5. Ref Super Plantilla v2 a v3.0

## Pasos
1. Crear repo (manual)
2. Push archivos de migracion
3. Importar codigo de Z.ai
4. Crear Vercel Postgres
5. Configurar env vars
6. Deploy
7. Smoke test API routes
