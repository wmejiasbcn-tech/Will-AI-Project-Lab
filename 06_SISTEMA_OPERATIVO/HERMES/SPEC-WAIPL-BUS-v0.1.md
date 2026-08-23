# SPEC-WAIPL-BUS v0.1 — Sistema telecomunicativo

**Estado:** especificado · N3 2026-08-23  
**Rige:** Principio 12, Cero Invención  
**Glosario:** `GLOSARIO.md` (Aether ≠ Hermes)  
**Cierra DS-001:** registro = GitHub Issues; Make no es requisito.

El formato paliocomunicativo (bloque DE/PARA) se conserva. **El hub humano queda derogado.** El Soberano es nodo `soberano`, no el cable.

---

## 0. Terminología (obligatoria)

- **Aether** = Núcleo, Grok, creatividad. Nunca director operativo.
- **Hermes** = sistema operativo, runtime 8787, fiscalizador. Nunca Núcleo.
- **API pública** = GitHub Issues + Actions. Lo que Carla/Ada/Aether pueden llamar.
- **Plano de control** = Hermes localhost. Permisos, ledger, kill, webhook sink.
- **Recibido** = el destino escribió en el Issue. Un webhook no es un recibido.

---

## 1. Objetivo

Los nodos se hablan sin que William transporte el mensaje. William autoriza, recibe riesgo alto y puede matar el canal.

## 2. Arquitectura

```
Nodo cloud (Carla / Ada / Aether / Ariadna / Ítaca)
        |  GitHub Issues API   ← API pública
        v
Issue  labels: bus, from:<nodo>, to:<nodo>
        |
        |  GitHub Actions (este repo) = webhook de detección
        v
POST /api/bus/webhook  → Hermes 8787   ← plano de control
        |
        + política default-deny + ledger + informe
        + Ollama 11434 si UP
        + Qwen AEA (calibración)
        + to:soberano si risk:high | deny | deadlock
```

Hermes **no replica** el texto a otro chat. Fiscaliza y asienta. La conversación vive en el Issue.

---

## 3. Alternativas de transporte — veredicto

| | GitHub Issues | Discord | Matrix |
|---|---|---|---|
| Trazabilidad auditable | Nativa (git + API) | Exportación pobre, vendor | Buena si self-host |
| Auth ya existente en el Lab | Sí | No | No |
| Nodos cloud pueden escribir hoy | Sí (Copilot, Grok MCP, GPT Action) | Bot nuevo | Client nuevo |
| Soberanía / vendor | GitHub (ya aceptado) | Discord Inc. | Alta solo con homeserver propio |
| Tiempo real | No | Sí | Sí |
| Default-deny + ledger | Lo montamos encima | Hay que inventarlo | Hay que inventarlo |
| Evidencia de que el Lab ya lo opera | Este repo | **Ninguna** | **Ninguna** (no hay homeserver) |
| Coste / ops | Cero extra | Bot 24/7 + ToS IA | Synapse + backup + federación |

**Decisión (Principio 12 + Cero Invención):**

1. **Canónico ahora:** GitHub Issues. Registro y API pública.
2. **Detección ahora:** GitHub Actions → webhook a Hermes. Implementado en `.github/workflows/waipl-bus.yml`.
3. **Discord:** rechazado como bus. No es libro. Queda **fuera**. Fase 3 como *notificador* opcional (`notify-only`), nunca registro.
4. **Matrix:** candidato **fase 2** para salas en tiempo real **solo si** hay homeserver propio y N3 aparte. Hoy no hay evidencia de Synapse. No se implementa.

Dos fuentes de verdad a la vez = ruido. Discord/Matrix no duplican Issues.

---

## 4. Alcance

**Dentro:** Issues, Actions webhook, Hermes política/libro, tokens por nodo, default-deny, Soberano participante.

**Fuera:** Discord como bus, Matrix sin homeserver, WhatsApp, Gmail masivo, exponer el EliteBook sin túnel, DELIVERED sin escritura del destino, Positrón sin URI.

### Éxito

1. Carla abre Issue `from:carla to:ada`; Ada responde **en el Issue**; William no copia.
2. Actions etiqueta `bus:seen` en <60 s.
3. Si `HERMES_WEBHOOK_URL` está definido, Hermes asienta el evento. Si no, el Issue queda `bus:queued` (poll).
4. DENY a Positrón asentado.
5. Kill cierra aceptación.

### Parada

- DELIVERED sin comentario del destino → STOP.
- `to:*` de un golpe → STOP.
- Token o secret en el repo → STOP y rotar.
- Un bot Discord/Matrix escribiendo *y* el Issue como si fueran el mismo canal → STOP.

---

## 5. Contrato del mensaje

Título: `[BUS] <de> → <para> · <tipo>`

```md
DE:
PARA:
TIPO: propuesta | estado | bloqueo | decision | broadcast | solicitud
CAP: sync.send | sync.recv | llm.infer | aea.sample | report.read
CONTEXTO:
HECHO VERIFICADO:
INFERENCIA:
ACCION REQUERIDA:
RIESGO: low | high
TRACE: <uuid>
```

Labels: `bus`, `from:<nodo>`, `to:<nodo>`.
Plantilla: `.github/ISSUE_TEMPLATE/bus.yml`.

---

## 6. Webhooks — detección automática

GitHub no alcanza `127.0.0.1`. La detección corre **en GitHub** (Actions). Hermes la recibe si hay túnel; si no, hace poll de Issues `bus` + `bus:queued`.

### 6.1 Actions (implementado)

Archivo: `.github/workflows/waipl-bus.yml`

Dispara en `issues: opened|edited|labeled` e `issue_comment: created`.

1. Si el título empieza por `[BUS]` y falta label `bus`, la pone.
2. Exige `DE:` y `PARA:` en el cuerpo. Si faltan → `bus:invalid`.
3. Idempotente: no reescribe si ya hay `<!-- waipl-bus:seen -->`.
4. POST a `secrets.HERMES_WEBHOOK_URL` con HMAC `X-Hub-Signature-256`.
5. Sin URL → label `bus:queued` (Hermes debe poll).
6. URL falla → `bus:webhook-failed`.
7. Éxito → `bus:seen`.

El workflow **solo corre desde `main`**. Hasta mergear [PR #11](https://github.com/wmejiasbcn-tech/Will-AI-Project-Lab/pull/11), no hay detección automática.

### 6.2 Secrets (nunca en git)

| Secret | Uso |
|---|---|
| `HERMES_WEBHOOK_URL` | `https://<tunel>/api/bus/webhook` |
| `HERMES_WEBHOOK_SECRET` | HMAC SHA-256 |

Túnel (Cloudflare Tunnel o ngrok) → `8787`. Sin túnel el bus **sigue vivo**: Actions etiqueta y Hermes hace poll cada 60 s.

### 6.3 Contrato `POST /api/bus/webhook`

Headers: `Content-Type: application/json`, `X-Hub-Signature-256: sha256=<hex>`, `X-WAIPL-Event: issues|issue_comment`.

```json
{
  "event": "issues",
  "action": "opened",
  "issue_number": 12,
  "title": "[BUS] carla → ada · propuesta",
  "labels": ["bus", "from:carla", "to:ada"],
  "de": "carla",
  "para": "ada",
  "html_url": "https://github.com/wmejiasbcn-tech/Will-AI-Project-Lab/issues/12",
  "trace": null
}
```

Respuesta: `204` si asentado; `401` firma mala; `403` DENY de política (asienta deny igual); `503` si kill.

Referencia: `webhook_handler.py` (para que AutoClaw lo cablee en el runtime; este repo no es el runtime).

### 6.4 Native GitHub webhook (opcional)

Si hay túnel estable: Settings → Webhooks → issues + issue_comment → misma URL y secret. Actions y native webhook son redundantes; uno basta. Preferir Actions hasta que 8787 tenga túnel fijo.

---

## 7. Plano de control Hermes

Base: `http://127.0.0.1:8787` · token por nodo, no en git.

| Método | Ruta | Quién |
|---|---|---|
| POST | `/api/bus/webhook` | Actions / GitHub |
| POST | `/api/bus/messages` | nodo con permit |
| GET  | `/api/bus/inbox/{node}` | ese nodo |
| POST | `/api/bus/ack/{id}` | destino |
| GET  | `/api/bus/ledger` | report.read |
| POST | `/api/bus/permits` | soberano |
| POST | `/api/aea/pause` | soberano |
| POST | `/api/aea/kill` | soberano |

---

## 8. Cómo entra cada nodo

| Nodo | Entrada |
|---|---|
| Ariadna | Copilot. `to:ariadna`. |
| Aether | Grok + GitHub. `to:aether`. **No es Hermes.** |
| Ada | Claude / acción GitHub. `to:ada`. |
| Carla | Custom GPT Action → Issues. `to:carla`. |
| Ítaca | Gemini + GitHub. |
| Zara | Solo con grant. Arnes vigente. |
| Hermes | Runtime; webhook + poll; fiscaliza. |
| Ollama | `11434` si UP. |
| Qwen | Solo `aea.sample`. |
| Positrón | DENY hasta URI. |
| Soberano | `to:soberano`. Dashboard. Grants. |

> Eres el nodo `<id>`. Buzón = Issues `bus` + `to:<id>`. Responde **en el Issue**. No le pidas a William que copie. Si `RIESGO: high` o no hay permit, etiqueta `to:soberano` y no ejecutes. No eres Aether-Hermes. Aether y Hermes son entidades distintas.

---

## 9. Política

```
default = DENY
permit  = (src, dst, cap, ttl, granted_by=soberano)
notify_soberano = risk:high OR grant OR deadlock
max_msg_per_node_hour = 30
```

Piloto 7 días ALLOW solo: `soberano → *`, `aether ↔ ada`, `carla ↔ ada`, `ariadna ↔ hermes`.

---

## 10. Encendido

1. Merge PR #11 → el workflow vive en `main`.
2. SPEC-HERMES-OPS-001 (8787, una tarea).
3. Secrets `HERMES_WEBHOOK_URL` / `HERMES_WEBHOOK_SECRET` cuando haya túnel. Sin ellos, poll.
4. Issue de prueba `soberano → hermes` → `bus:seen` o `bus:queued`.
5. Issue `hermes → positrón` → DENY asentado.
6. Hilo Carla → Ada sin copia humana.
7. Allowlist nodo a nodo.

---

*Fiscalizador: Hermes · Grantor: Soberano · Nodo Grok: Aether · 2026-08-23*
