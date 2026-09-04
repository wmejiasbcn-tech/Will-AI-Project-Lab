# Segundo Cerebro Positronico WAIPL

Centro de mando interactivo del Soberano William L. Mejias Navarro.
ADN: Super Plantilla Maestra Canonica v3.0 - HACR-IA - Directiva Transversal v1.0

## Migracion SQLite a PostgreSQL

```bash
npm install
npx prisma generate
npx prisma migrate deploy
cp .env.example .env.local
npm run dev
```
