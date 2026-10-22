// WAIPL-BUS · Portero (BORRADOR, no activo) · lógica pura, sin red ni GitHub.
// Implementa SPEC-WAIPL-BUS-v0.1 §9: default = DENY; permit = (src, dst, cap, ttl, granted_by=soberano);
// notify_soberano = risk:high OR grant OR deadlock (y DENY, según §2); max_msg_per_node_hour = 30.
'use strict';

const LEDGER_MARKER = '<!-- waipl-bus:portero v1 -->';
const MAX_MSG_PER_NODE_HOUR = 30;

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

  // Identidad: DE no autentica. El nodo real es el que tiene asignada la cuenta de GitHub que escribió.
  const nodes = input.nodes || {};
  const actorNode = norm(nodes[norm(input.actorLogin)] || '');
  if (!actorNode) {
    return out(VERDICT.DENY, 'La cuenta "' + input.actorLogin + '" no tiene nodo asignado en nodes.json.', {
      notifySoberano: true,
    });
  }
  if (actorNode !== msg.de) {
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

  return out(VERDICT.ALLOW, 'Permiso ' + permit.id + ' (' + permit.src + ' → ' + permit.dst + ').', {
    permitId: permit.id,
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
function isStalled({ allowedAt, comments, destNode, nodes, now, hours }) {
  const t = now instanceof Date ? now.getTime() : Date.parse(now);
  if (t - Date.parse(allowedAt) < hours * 3600 * 1000) return false;
  const destLogins = Object.entries(nodes || {})
    .filter(([, n]) => norm(n) === norm(destNode))
    .map(([login]) => norm(login));
  return !(comments || []).some(
    (c) => destLogins.includes(norm(c.user && c.user.login)) && Date.parse(c.created_at) > Date.parse(allowedAt)
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
};
