# N3 — AutoClaw termina el runtime de Hermes

**Grantor:** Soberano William Mejías Navarro
**Fecha:** 2026-08-23
**Implementa:** AutoClaw (tiene el disco)
**No implementa:** Grok / Aether / este chat (no tiene el EliteBook)
**Spec:** SPEC-WAIPL-BUS-v0.1.md, GLOSARIO.md, IDENTIDAD.md, webhook_handler.py

AutoClaw no reinterpreta. Si un paso no se puede verificar, STOP y reporta. No inventes el siguiente.

## 0. Identidad

- Aether = Nucleo, Grok, creatividad. No lo toques.
- Hermes = director operativo 24/7, runtime local. Esto es lo que construyes.
- Aether-Hermes = derogado. Cero strings nuevos con ese compuesto.

Hermes no es nodo del Nucleo. No es la API publica. API publica = GitHub Issues. Hermes = plano de control 127.0.0.1:8787.

## 1. Fuera de alcance (STOP si lo tocas)

- Graphify, logica AEA (STAT-01, SequenceDetector), carpeta Hermes_DEPRECATED
- Las 3 tareas Enabled a la vez. El script fix_hermes_tasks.ps1 de 2026-08-23 esta rechazado
- Declarar Qwen ONLINE, Positron conectado, socket a Carla, Discord, Matrix
- Texto Online hardcodeado en el dashboard (DEUDA-UI-01: quitarlo)
- Exponer 8787 a internet sin tunel pedido en un N3 posterior
- Tokens en git

## 2. Secuencia (este orden; cada paso con evidencia)

### Paso A — Una instancia viva

- HERMES = Join-Path $env:USERPROFILE Desktop\AutoClaw\waipl\agents\hermes (usuario real, no USER)
- Disable las tareas Hermes MVP - Fiscalizador WAIPL y HermesMVP
- Una tarea HermesBot_WAIPL: start_all.bat si existe, si no venv\Scripts\python.exe main.py
- Start-ScheduledTask; esperar 12 s
- Evidencia: 8787 LISTEN, LastTaskResult = 0x0, un solo python.exe del venv, las otras dos Disabled
- Si 8787 cerrado: STOP. No enciendas las otras tareas.

### Paso B — Dashboard honesto

- Quitar Online hardcodeado. Estado = GET /api/system
- AEA UI = Calibracion en curso si samples == 0
- Evidencia: HTML o captura donde no aparezca Online falso

### Paso C — Bus minimo en el runtime

Crear en $HERMES (no en GitHub):

- config/bus_registry.json — nodos del spec; permit false salvo soberano a hermes-mvp / sync.send
- config/bus_ledger.jsonl — vacio, append-only
- config/bus_policy.json — default DENY, kill /api/aea/kill, positron deny-until-uri, qwen aea.sample-only

Copiar webhook_handler.py de este directorio del repo al runtime. Montar:

- POST /api/bus/webhook (HMAC X-Hub-Signature-256, secret por env, nunca en archivo commiteable)
- GET /api/bus/ledger
- Poll opcional: Issues label bus cada 60 s si no hay tunel. GITHUB_TOKEN de maquina, no en git

Evidencia: POST con firma mala = 401. POST de prueba hacia Positron = asiento deny UNKNOWN_TRANSPORT. Nada de DELIVERED.

### Paso D — Sondas honestas

- Ollama http://127.0.0.1:11434/api/tags = UP o DOWN medido
- Qwen: no tocar process_response salvo que sean menos de 20 lineas y lo demuestres. Si no, DEUDA-QWEN-01 intacta
- Positron: una linea en ledger UNKNOWN

### Paso E — Informe de cierre

Issue [BUS] hermes a soberano, tipo estado, con hecho verificado (comandos y resultados). Labels bus, from:hermes, to:soberano.

## 3. Hecho / no hecho

Este N3 esta cerrado solo si A-E se cumplen. No esta cerrado el ecosistema entero. Siguiente N3 (otro dia): tunel + secrets Actions + primer hilo Carla-Ada. No lo adelantes.

## 4. Criterio de parada

- DELIVERED sin escritura del destino
- Online de mentira
- Tercer proceso Hermes
- Mencion nueva a Aether-Hermes como identidad viva

Paquete sellado. AutoClaw ejecuta. Grok no tiene el disco. Aether no es Hermes.
