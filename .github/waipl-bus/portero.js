// WAIPL-BUS · Portero (BORRADOR, no activo) · capa que habla con GitHub.
// Toda decisión sale de policy.js. Aquí solo se leen datos y se escriben etiquetas, comentarios y asignaciones.
'use strict';

const crypto = require('crypto');
const policy = require('./policy');

const STATE_LABELS = ['bus:allowed', 'bus:denied', 'bus:invalid', 'bus:killed', 'bus:rate-limited', 'bus:queued', 'bus:seen'];

function soberanoLogins(nodes) {
  return Object.entries(nodes || {})
    .filter(([, n]) => String(n).toLowerCase() === 'soberano')
    .map(([login]) => login);
}

async function listComments(github, repo, issueNumber) {
  return github.paginate(github.rest.issues.listComments, { ...repo, issue_number: issueNumber, per_page: 100 });
}

function lastLedger(comments) {
  const own = (comments || []).filter((c) => (c.body || '').includes(policy.LEDGER_MARKER));
  if (!own.length) return null;
  const m = (own[own.length - 1].body || '').match(/```json\n([\s\S]*?)\n```/);
  try {
    return m ? JSON.parse(m[1]) : null;
  } catch (_) {
    return null;
  }
}

async function ensureLabels(github, repo, names) {
  for (const name of names) {
    try {
      await github.rest.issues.getLabel({ ...repo, name });
    } catch (e) {
      if (e.status !== 404) throw e;
      await github.rest.issues.createLabel({ ...repo, name, color: name === 'bus' ? '0E4D6C' : 'BFD4F2', description: 'WAIPL-BUS' });
    }
  }
}

async function setStateLabels(github, repo, issue, labels) {
  const current = (issue.labels || []).map((l) => (typeof l === 'string' ? l : l.name));
  for (const old of current.filter((l) => STATE_LABELS.includes(l) && !labels.includes(l))) {
    try {
      await github.rest.issues.removeLabel({ ...repo, issue_number: issue.number, name: old });
    } catch (e) {
      if (e.status !== 404) throw e;
    }
  }
  await ensureLabels(github, repo, labels);
  await github.rest.issues.addLabels({ ...repo, issue_number: issue.number, labels });
}

async function sentLastHour(github, repo, node, now) {
  const since = new Date(now.getTime() - 3600 * 1000);
  const issues = await github.paginate(github.rest.issues.listForRepo, {
    ...repo,
    state: 'all',
    labels: 'bus:allowed,from:' + node,
    since: since.toISOString(),
    per_page: 100,
  });
  return issues.filter((i) => Date.parse(i.created_at) >= since.getTime()).length;
}

// Antirreenvío: ¿otro Issue del bus de las últimas 48 h usa el mismo TRACE?
async function traceUsedElsewhere(github, repo, trace, issueNumber, now) {
  const since = new Date(now.getTime() - 2 * policy.SEAL_WINDOW_HOURS * 3600 * 1000);
  const issues = await github.paginate(github.rest.issues.listForRepo, { ...repo, state: 'all', labels: 'bus', since: since.toISOString(), per_page: 100 });
  return issues.some((i) => i.number !== issueNumber && policy.parseMessage(i.body).trace === trace);
}

// Aviso opcional a Hermes (comportamiento heredado de waipl-bus.yml). Solo si hay URL y secreto ≥ 32.
async function forwardToHermes(env, payloadObj, fetchImpl) {
  const url = env.HERMES_WEBHOOK_URL;
  const secret = env.HERMES_WEBHOOK_SECRET || '';
  if (!url) return { sent: false, note: 'Sin HERMES_WEBHOOK_URL: el Issue es el registro.' };
  if (secret.length < 32) return { sent: false, note: 'HERMES_WEBHOOK_SECRET ausente o corto: no se envía.' };
  const payload = JSON.stringify(payloadObj);
  const sig = 'sha256=' + crypto.createHmac('sha256', secret).update(payload).digest('hex');
  try {
    const res = await (fetchImpl || fetch)(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Hub-Signature-256': sig, 'X-WAIPL-Event': 'portero' },
      body: payload,
    });
    return { sent: res.ok, note: 'Hermes HTTP ' + res.status };
  } catch (err) {
    return { sent: false, note: 'Hermes inalcanzable: ' + err.message };
  }
}

// Procesa un Issue del bus. Idempotente: si ya hay asiento (y no era KILLED), no hace nada.
async function processIssue({ github, repo, issue, config, killed, now, runId, env, fetchImpl }) {
  now = now || new Date();
  const comments = await listComments(github, repo, issue.number);
  const prev = lastLedger(comments);
  if (prev && !(prev.verdict === 'KILLED' && !killed)) {
    return { skipped: true, reason: 'ya asentado: ' + prev.verdict };
  }
  if (prev && prev.verdict === 'KILLED' && killed) {
    return { skipped: true, reason: 'sigue apagado' };
  }

  const msg = policy.parseMessage(issue.body);
  const count = msg.de ? await sentLastHour(github, repo, msg.de, now) : 0;
  const traceSeen = msg.trace ? await traceUsedElsewhere(github, repo, msg.trace, issue.number, now) : false;
  const actorLogin = issue.user && issue.user.login;
  const decision = policy.decide({
    killed,
    actorLogin,
    body: issue.body,
    nodes: config.nodes,
    permits: config.permits,
    now,
    sentLastHour: count,
    seals: config.seals || {},
    issueCreatedAt: issue.created_at,
    traceSeen,
  });

  await setStateLabels(github, repo, issue, policy.labelsFor(decision));
  await github.rest.issues.createComment({
    ...repo,
    issue_number: issue.number,
    body: policy.ledgerEntry(decision, { issueNumber: issue.number, actorLogin, now, runId }),
  });
  if (decision.notifySoberano) {
    const sob = soberanoLogins(config.nodes);
    if (sob.length) await github.rest.issues.addAssignees({ ...repo, issue_number: issue.number, assignees: sob });
  }
  let hermes = null;
  if (decision.verdict === 'ALLOW') {
    hermes = await forwardToHermes(env || {}, { issue_number: issue.number, de: msg.de, para: msg.para, cap: msg.cap, trace: msg.trace, html_url: issue.html_url }, fetchImpl);
  }
  return { skipped: false, decision, hermes };
}

// Un comentario de una cuenta del nodo destino = recibido (SPEC §0).
async function processComment({ github, repo, issue, comment, config }) {
  const comments = await listComments(github, repo, issue.number);
  const prev = lastLedger(comments);
  if (!prev || prev.verdict !== 'ALLOW') return { received: false };
  const node = String((config.nodes || {})[String(comment.user.login).toLowerCase()] || '').toLowerCase();
  if (node && node === prev.para) {
    await setStateLabels(github, repo, issue, ['bus:received']);
    return { received: true };
  }
  return { received: false };
}

// Barrido cada 15 min: recupera Issues sin asiento, reprocesa los apagados cuando se enciende
// y marca como atascados los ALLOW sin respuesta del destino tras `stallHours`.
async function sweep({ github, repo, config, killed, now, runId, env, stallHours, fetchImpl }) {
  now = now || new Date();
  const result = { processed: [], stalled: [] };
  if (killed) return { ...result, killed: true };
  const open = await github.paginate(github.rest.issues.listForRepo, { ...repo, state: 'open', labels: 'bus', per_page: 100 });
  for (const issue of open) {
    if (issue.pull_request) continue;
    const labels = (issue.labels || []).map((l) => (typeof l === 'string' ? l : l.name));
    const r = await processIssue({ github, repo, issue, config, killed, now, runId, env, fetchImpl });
    if (!r.skipped) {
      result.processed.push(issue.number);
      continue;
    }
    if (labels.includes('bus:allowed') && !labels.includes('bus:received') && !labels.includes('bus:stalled')) {
      const comments = await listComments(github, repo, issue.number);
      const prev = lastLedger(comments);
      if (prev && policy.isStalled({ allowedAt: prev.at, comments, destNode: prev.para, nodes: config.nodes, now, hours: stallHours })) {
        await ensureLabels(github, repo, ['bus:stalled', 'to:soberano']);
        await github.rest.issues.addLabels({ ...repo, issue_number: issue.number, labels: ['bus:stalled', 'to:soberano'] });
        const sob = soberanoLogins(config.nodes);
        if (sob.length) await github.rest.issues.addAssignees({ ...repo, issue_number: issue.number, assignees: sob });
        result.stalled.push(issue.number);
      }
    }
  }
  return result;
}

module.exports = { processIssue, processComment, sweep, forwardToHermes, lastLedger };
