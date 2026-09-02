-- Positrón WAIPL — Migración inicial PostgreSQL
-- Crea las 7 tablas (5 originales + 2 evolucionadas)

CREATE TABLE IF NOT EXISTS "messages" (
  "id" TEXT NOT NULL,
  "role" TEXT NOT NULL,
  "content" TEXT NOT NULL,
  "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "audio" BOOLEAN NOT NULL DEFAULT false,
  CONSTRAINT "messages_pkey" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "captures" (
  "id" TEXT NOT NULL,
  "uuid" TEXT NOT NULL,
  "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "hash" TEXT NOT NULL,
  "origen" TEXT NOT NULL,
  "tipo" TEXT NOT NULL,
  "prioridad" TEXT NOT NULL,
  "tags" TEXT,
  "contenido" TEXT NOT NULL,
  "estadoCLA" TEXT NOT NULL DEFAULT 'sin_clasificar',
  "estadoANA" TEXT NOT NULL DEFAULT 'pendiente',
  CONSTRAINT "captures_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "captures_uuid_key" UNIQUE ("uuid")
);

CREATE TABLE IF NOT EXISTS "commands" (
  "id" TEXT NOT NULL,
  "target" TEXT NOT NULL,
  "content" TEXT NOT NULL,
  "status" TEXT NOT NULL DEFAULT 'enviado',
  "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "commands_pkey" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "notifications" (
  "id" TEXT NOT NULL,
  "type" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "content" TEXT NOT NULL,
  "read" BOOLEAN NOT NULL DEFAULT false,
  "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "notifications_pkey" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "emails" (
  "id" TEXT NOT NULL,
  "to" TEXT NOT NULL,
  "subject" TEXT NOT NULL,
  "body" TEXT NOT NULL,
  "status" TEXT NOT NULL DEFAULT 'pendiente',
  "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "emails_pkey" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "radar_signals" (
  "id" TEXT NOT NULL,
  "signalType" TEXT NOT NULL,
  "target" TEXT NOT NULL,
  "intensity" DOUBLE PRECISION NOT NULL DEFAULT 0.0,
  "metadata" JSONB,
  "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTA
MP,
  CONSTRAINT "radar_signals_pkey" PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "quarantine_entries" (
  "id" TEXT NOT NULL,
  "entityId" TEXT NOT NULL,
  "reason" TEXT NOT NULL,
  "severity" TEXT NOT NULL,
  "status" TEXT NOT NULL DEFAULT 'active',
  "metadata" JSONB,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "releasedAt" TIMESTAMP(3),
  CONSTRAINT "quarantine_entries_pkey" PRIMARY KEY ("id")
);
