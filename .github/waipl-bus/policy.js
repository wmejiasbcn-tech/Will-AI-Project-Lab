// WAIPL-BUS · Portero (BORRADOR, no activo) · lógica pura, sin red ni GitHub.
// Implementa SPEC-WAIPL-BUS-v0.1 §9: default = DENY; permit = (src, dst, cap, ttl, granted_by=soberano);
// notify_soberano = risk:high OR grant OR deadlock (y DENY, según §2); max_msg_per_node_hour = 30.
'use strict';

const crypto = require('crypto');

const LEDGER_MARKER = '<!-- waipl-bus:portero v1 -->';
const MAX_MSG_PER_NODE_HOUR = 30;
const SEAL_WINDOW_HOURS = 24; // un sello solo vale si FECHA está a ±24 h de la creación del Issue

const VERDICT = Object.freeze({
  ALLOW: 'ALLOW',
  DENY: 'DENY',
  INVALID: 'INVALID',
  KILLED: 'KILLED',
  RATE_LIMITED: 'RATE_LIMITED',
});

// Lee un campo del cuerpo: formato "CAMPO: valor" o formulario de Issue ("### CAMPO\n\nvalor").
function field(body, name) {
  const text = body || '';
  const esc = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const line = text.match(new RegExp('^' + esc + ':[ \\t]*(\\S[^\\n]*)$', 'mi'));
  if (line) return line[1].trim();
  const form = text.match(new RegExp('###[ \\t]*' + esc + '[ \\t]*\\n+([^#\\n][^\\n]*)', 'i'));
  if (form && form[1].trim() !== '_No response_') return form[1].trim();
  return '';
}

function norm(s) {
  return String(s || '').trim().toLowerCase();
}

function parseMessage(body) {
  return {
    de: norm(field(body, 'DE')),
    para: norm(field(body, 'PARA')),
    tipo: norm(field(body, 'TIPO')),
    cap: norm(field(body, 'CAP')),
    riesgo: norm(field(body, 'RIESGO')),
    trace: field(body, 'TRACE') || null,
    fecha: field(body, 'FECHA') || null,
    sello: field(body, 'SELLO') || null,
  };
}

// Un permiso vale si coincide origen, destino y capacidad, lo concedió el soberano y no ha caducado.
// "*" en dst significa cualquier destino (piloto: soberano → *). Los permisos son direccionales:
// "carla ↔ ada" se escribe como dos permisos.
function findPermit(permits, msg, now) {
  const t = now instanceof Date ? now.getTime() : Date.parse(now);
  for (const p of permits || []) {
    if (norm(p.granted_by) !== 'soberano') continue;
    if (norm(p.src) !== msg.de) continue;
    if (norm(p.dst) !== '*' && norm(p.dst) !== msg.para) continue;
    const caps = Array.isArray(p.cap) ? p.cap.map(norm) : [norm(p.cap)];
    if (!caps.includes('*') && !caps.includes(msg.cap)) continue;
    // ttl obligatorio (SPEC §9): sin fecha válida de caducidad, el permiso no vale.
    const exp = Date.parse(p.expires_at);
    if (!p.expires_at || Number.isNaN(exp) || exp <= t) continue;
    return p;
  }
  return null;
}

// ---------- Sello por nodo (HMAC-SHA256) ----------
// Texto sellado = cuerpo completo del Issue sin la línea SELLO, con saltos \n y sin espacios finales.
// Así el sello cubre DE, PARA, TRACE, FECHA y todo el contenido: si alguien cambia una letra, deja de valer.
function sealPayload(body) {
  return String(body || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .filter((l) => !/^\s*SELLO:/i.test(l))
    .map((l) => l.replace(/\s+$/, ''))
    .join('\n')
    .trim();
}

function computeSeal(body, secret) {
  return 'v1:' + crypto.createHmac('sha256', secret).update('WAIPL-SELLO-v1\n' + sealPayload(body)).digest('hex');
}

// Devuelve null si el sello es válido, o el motivo del rechazo.
function checkSeal({ msg, body, secret, issueCreatedAt, traceSeen }) {
  if (!secret) return 'El nodo "' + msg.de + '" no tiene sello configurado (secreto BUS_SEAL_' + msg.de.toUpperCase() + ').';
  if (!msg.sello) return 'Falta SELLO del nodo "' + msg.de + '".';
  if (!msg.trace || !msg.fecha) return 'Un mensaje sellado necesita TRACE y FECHA.';
  const f = Date.parse(msg.fecha);
  const c = Date.parse(issueCreatedAt);
  if (Number.isNaN(f) || Number.isNaN(c) || Math.abs(c - f) > SEAL_WINDOW_HOURS * 3600 * 1000) {
    return 'FECHA fuera de la ventana de ' + SEAL_WINDOW_HOURS + ' h: posible reenvío de un mensaje viejo.';
  }
  if (traceSeen) return 'TRACE "' + msg.trace + '" ya se usó en otro mensaje: posible reenvío.';
  const expected = Buffer.from(computeSeal(body, secret));
  const given = Buffer.from(String(msg.sello).trim());
  if (expected.length !== given.length || !crypto.timingSafeEqual(expected, given)) {
    return 'SELLO no válido para el nodo "' + msg.de + '" (mensaje alterado o sello falso).';
  }
  return null;
}

// Decide qué hacer con un mensaje. Orden: apagado → formato → identidad → permiso → límite.
// input: { killed, actorLogin, body, nodes: {login: nodo}, permits: [...], now, sentLastHour }
function decide(input) {
  const out = (verdict, reason, extra = {}) => ({
    verdict,
    reason,
    msg,
    notifySoberano: false,
    ...extra,
  });
  const msg = parseMessage(input.body);

  if (input.killed) {
    return out(VERDICT.KILLED, 'Bus apagado por el soberano (BUS_KILL=true). No se procesa nada.');
  }
  if (!msg.de || !msg.para) {
    return out(VERDICT.INVALID, 'Faltan DE y/o PARA.');
  }
  if (!msg.cap) {
    return out(VERDICT.INVALID, 'Falta CAP (capacidad solicitada).');
  }
  if (msg.riesgo && !['low', 'high'].includes(msg.riesgo)) {
    return out(VERDICT.INVALID, 'RIESGO debe ser low o high.');
  }

  // Identidad: DE no autentica. Dos comprobaciones que se suman (mezcla acordada el 2026-10-22):
  //  1) la cuenta de GitHub que escribe (nodes.json);
  //  2) el sello secreto del nodo (seals: nodo → secreto), obligatorio para todo nodo que tenga sello.
  // Caso A: la cuenta es del propio nodo (DE = nodo de la cuenta) → si el nodo tiene sello, se verifica.
  // Caso B: la cuenta es del soberano y DE es otro nodo (el soberano transporta) → el sello del nodo es obligatorio.
  const nodes = input.nodes || {};
  const seals = input.seals || {};
  const actorNode = norm(nodes[norm(input.actorLogin)] || '');
  const sealArgs = { msg, body: input.body, secret: seals[msg.de], issueCreatedAt: input.issueCreatedAt, traceSeen: input.traceSeen };
  let identity;
  if (!actorNode) {
    return out(VERDICT.DENY, 'La cuenta "' + input.actorLogin + '" no tiene nodo asignado en nodes.json.', { notifySoberano: true });
  } else if (actorNode === msg.de) {
    if (seals[msg.de] || msg.sello) {
      const bad = checkSeal(sealArgs);
      if (bad) return out(VERDICT.DENY, bad, { notifySoberano: true });
      identity = 'cuenta+sello';
    } else {
      identity = 'cuenta';
    }
  } else if (actorNode === 'soberano') {
    const bad = checkSeal(sealArgs);
    if (bad) {
      return out(VERDICT.DENY, 'Identidad no verificada: escrito con la cuenta del soberano como "' + msg.de + '". ' + bad, { notifySoberano: true });
    }
    identity = 'sello (transportado por soberano)';
  } else {
    return out(
      VERDICT.DENY,
      'Identidad no verificada: DE="' + msg.de + '" pero la cuenta "' + input.actorLogin + '" pertenece al nodo "' + actorNode + '".',
      { notifySoberano: true }
    );
  }

  const permit = findPermit(input.permits, msg, input.now || new Date());
  if (!permit) {
    return out(VERDICT.DENY, 'Sin permiso vigente ' + msg.de + ' → ' + msg.para + ' (' + msg.cap + '). DENY por defecto.', {
      notifySoberano: true,
    });
  }

  if ((input.sentLastHour || 0) >= MAX_MSG_PER_NODE_HOUR) {
    return out(VERDICT.RATE_LIMITED, 'El nodo ' + msg.de + ' superó ' + MAX_MSG_PER_NODE_HOUR + ' mensajes en la última hora.', {
      notifySoberano: true,
    });
  }

  return out(VERDICT.ALLOW, 'Permiso ' + permit.id + ' (' + permit.src + ' → ' + permit.dst + '). Identidad: ' + identity + '.', {
    permitId: permit.id,
    identity,
    notifySoberano: msg.riesgo === 'high',
  });
}

// Etiquetas que reflejan el veredicto. Una sola etiqueta de estado bus:* por Issue.
function labelsFor(decision) {
  const state = {
    ALLOW: 'bus:allowed',
    DENY: 'bus:denied',
    INVALID: 'bus:invalid',
    KILLED: 'bus:killed',
    RATE_LIMITED: 'bus:rate-limited',
  }[decision.verdict];
  const labels = ['bus', state];
  if (decision.msg.de) labels.push('from:' + decision.msg.de);
  if (decision.msg.para) labels.push('to:' + decision.msg.para);
  if (decision.notifySoberano) labels.push('to:soberano');
  if (decision.msg.riesgo === 'high') labels.push('risk:high');
  return labels;
}

// Asiento del libro: un comentario por Issue con un JSON legible por máquina.
function ledgerEntry(decision, ctx) {
  const entry = {
    v: 1,
    issue: ctx.issueNumber,
    at: (ctx.now instanceof Date ? ctx.now : new Date(ctx.now || Date.now())).toISOString(),
    actor: ctx.actorLogin,
    de: decision.msg.de,
    para: decision.msg.para,
    cap: decision.msg.cap,
    riesgo: decision.msg.riesgo || null,
    trace: decision.msg.trace,
    verdict: decision.verdict,
    reason: decision.reason,
    permit: decision.permitId || null,
    identity: decision.identity || null,
    sealed: Boolean(decision.msg.sello),
    notify_soberano: decision.notifySoberano,
    run: ctx.runId || null,
  };
  return (
    LEDGER_MARKER +
    '\n**WAIPL-BUS · portero** · ' + entry.verdict + ' · ' + (entry.de || '?') + ' → ' + (entry.para || '?') +
    '\n' + entry.reason +
    (entry.verdict === 'ALLOW' ? '\nEsto no es un *recibido*. Recibido = comentario del nodo destino en este Issue.' : '') +
    '\n\n```json\n' + JSON.stringify(entry) + '\n```'
  );
}

function hasLedger(comments) {
  return (comments || []).some((c) => (c.body || '').includes(LEDGER_MARKER));
}

// Un mensaje ALLOW está atascado si pasan más de `hours` horas sin comentario de una cuenta del nodo destino.
// Nodo que firma un comentario, solo para «recibido»:
//  1) la cuenta propia del nodo (nodes.json), o
//  2) si comenta la cuenta del soberano A TRAVÉS de una app registrada en apps.json, el nodo de esa app.
// La app solo cuenta junto con la cuenta del soberano; una app usada desde otra cuenta no cuenta.
function commentNode(comment, nodes, apps) {
  if (!comment) return '';
  const accountNode = norm((nodes || {})[norm(comment.user && comment.user.login)] || '');
  const app = comment.performed_via_github_app;
  const slug = norm(app && (app.slug || app.name));
  if (accountNode === 'soberano' && slug && (apps || {})[slug]) return norm(apps[slug]);
  return accountNode;
}

function isStalled({ allowedAt, comments, destNode, nodes, apps, now, hours }) {
  const t = now instanceof Date ? now.getTime() : Date.parse(now);
  if (t - Date.parse(allowedAt) < hours * 3600 * 1000) return false;
  return !(comments || []).some(
    (c) => commentNode(c, nodes, apps) === norm(destNode) && Date.parse(c.created_at) > Date.parse(allowedAt)
  );
}

module.exports = {
  LEDGER_MARKER,
  MAX_MSG_PER_NODE_HOUR,
  VERDICT,
  field,
  parseMessage,
  findPermit,
  decide,
  labelsFor,
  ledgerEntry,
  hasLedger,
  isStalled,
  commentNode,
  sealPayload,
  computeSeal,
  checkSeal,
  SEAL_WINDOW_HOURS,
};
