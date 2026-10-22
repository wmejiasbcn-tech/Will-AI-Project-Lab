// Pruebas del portero (BORRADOR). Ejecutar: node --test .github/waipl-bus/test/
// Usan un GitHub falso en memoria: demuestran el comportamiento de los controles, no solo que el código existe.
'use strict';
const test = require('node:test');
const assert = require('node:assert');
const policy = require('../policy');
const portero = require('../portero');

const NOW = new Date('2026-11-01T10:00:00Z');
const FUTURE = '2026-11-08T10:00:00Z';
const PAST = '2026-10-01T10:00:00Z';

const NODES = { 'wmejiasbcn-tech': 'soberano', 'carla-bot': 'carla', 'ada-bot': 'ada' };
const PERMITS = [
  { id: 'P-001', src: 'soberano', dst: '*', cap: '*', granted_by: 'soberano', expires_at: FUTURE },
  { id: 'P-004', src: 'carla', dst: 'ada', cap: '*', granted_by: 'soberano', expires_at: FUTURE },
  { id: 'P-OLD', src: 'ada', dst: 'carla', cap: '*', granted_by: 'soberano', expires_at: PAST },
  { id: 'P-FAKE', src: 'ada', dst: 'soberano', cap: '*', granted_by: 'carla', expires_at: FUTURE },
  { id: 'P-NOTTL', src: 'ada', dst: 'ariadna', cap: '*', granted_by: 'soberano', expires_at: 'PENDIENTE' },
];
const CONFIG = { nodes: NODES, permits: PERMITS };

function body({ de, para, cap = 'sync.send', riesgo = 'low' }) {
  return ['DE: ' + de, 'PARA: ' + para, 'TIPO: propuesta', 'CAP: ' + cap, 'RIESGO: ' + riesgo, 'TRACE: t-1'].join('\n');
}

// ---------- GitHub falso ----------
function fakeGithub() {
  const state = { issues: new Map(), comments: new Map(), labels: new Set(), calls: [] };
  let cid = 1;
  const rest = {
    issues: {
      getLabel: async ({ name }) => {
        if (!state.labels.has(name)) { const e = new Error('404'); e.status = 404; throw e; }
        return {};
      },
      createLabel: async ({ name }) => { state.labels.add(name); },
      addLabels: async ({ issue_number, labels }) => {
        const i = state.issues.get(issue_number);
        for (const l of labels) if (!i.labels.includes(l)) i.labels.push(l);
      },
      removeLabel: async ({ issue_number, name }) => {
        const i = state.issues.get(issue_number);
        i.labels = i.labels.filter((l) => l !== name);
      },
      createComment: async ({ issue_number, body }) => {
        state.calls.push(['comment', issue_number]);
        state.comments.get(issue_number).push({ id: cid++, body, user: { login: 'github-actions[bot]' }, created_at: new Date().toISOString() });
      },
      addAssignees: async ({ issue_number, assignees }) => {
        const i = state.issues.get(issue_number);
        i.assignees = [...new Set([...(i.assignees || []), ...assignees])];
      },
      listComments: 'listComments',
      listForRepo: 'listForRepo',
    },
  };
  const github = {
    rest,
    paginate: async (fn, args) => {
      if (fn === 'listComments') return state.comments.get(args.issue_number) || [];
      if (fn === 'listForRepo') {
        const want = (args.labels || '').split(',').filter(Boolean);
        return [...state.issues.values()].filter(
          (i) => want.every((w) => i.labels.includes(w)) && (args.state === 'all' || i.state === args.state)
        );
      }
      throw new Error('paginate desconocido');
    },
  };
  function addIssue(n, author, text, extra = {}) {
    const issue = { number: n, user: { login: author }, body: text, labels: ['bus'], state: 'open', created_at: NOW.toISOString(), html_url: 'u', ...extra };
    state.issues.set(n, issue);
    state.comments.set(n, []);
    return issue;
  }
  return { github, state, addIssue };
}
const REPO = { owner: 'o', repo: 'r' };
const ledgers = (state, n) => state.comments.get(n).filter((c) => c.body.includes(policy.LEDGER_MARKER));

// ---------- Política pura ----------
test('ALLOW: soberano → cualquiera con permiso vigente', () => {
  const d = policy.decide({ actorLogin: 'wmejiasbcn-tech', body: body({ de: 'soberano', para: 'ada' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'ALLOW');
  assert.equal(d.permitId, 'P-001');
  assert.equal(d.notifySoberano, false);
});

test('DENY por defecto: sin permiso para ese par', () => {
  const d = policy.decide({ actorLogin: 'ada-bot', body: body({ de: 'ada', para: 'zara' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'DENY');
  assert.equal(d.notifySoberano, true);
});

test('DENY: permiso caducado', () => {
  const d = policy.decide({ actorLogin: 'ada-bot', body: body({ de: 'ada', para: 'carla' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'DENY');
});

test('DENY: permiso sin fecha válida (PENDIENTE) no vale', () => {
  const d = policy.decide({ actorLogin: 'ada-bot', body: body({ de: 'ada', para: 'ariadna' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'DENY');
});

test('DENY: permiso concedido por alguien que no es el soberano', () => {
  const d = policy.decide({ actorLogin: 'ada-bot', body: body({ de: 'ada', para: 'soberano' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'DENY');
});

test('Identidad: DE falso con la cuenta del soberano → DENY', () => {
  const d = policy.decide({ actorLogin: 'wmejiasbcn-tech', body: body({ de: 'carla', para: 'ada' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'DENY');
  assert.match(d.reason, /Identidad no verificada/);
});

test('Identidad: cuenta sin nodo asignado → DENY', () => {
  const d = policy.decide({ actorLogin: 'desconocido', body: body({ de: 'carla', para: 'ada' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'DENY');
});

test('Identidad: cuenta propia del nodo con permiso → ALLOW', () => {
  const d = policy.decide({ actorLogin: 'carla-bot', body: body({ de: 'carla', para: 'ada' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'ALLOW');
});

test('Formato: sin DE/PARA o sin CAP → INVALID', () => {
  assert.equal(policy.decide({ actorLogin: 'carla-bot', body: 'hola', ...CONFIG, now: NOW }).verdict, 'INVALID');
  assert.equal(policy.decide({ actorLogin: 'carla-bot', body: 'DE: carla\nPARA: ada', ...CONFIG, now: NOW }).verdict, 'INVALID');
});

test('Riesgo alto → ALLOW con aviso al soberano', () => {
  const d = policy.decide({ actorLogin: 'carla-bot', body: body({ de: 'carla', para: 'ada', riesgo: 'high' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'ALLOW');
  assert.equal(d.notifySoberano, true);
  assert.ok(policy.labelsFor(d).includes('to:soberano'));
});

test('Límite: el mensaje 31 de la hora → RATE_LIMITED', () => {
  const base = { actorLogin: 'carla-bot', body: body({ de: 'carla', para: 'ada' }), ...CONFIG, now: NOW };
  assert.equal(policy.decide({ ...base, sentLastHour: 29 }).verdict, 'ALLOW');
  assert.equal(policy.decide({ ...base, sentLastHour: 30 }).verdict, 'RATE_LIMITED');
});

test('Apagado: con BUS_KILL nada se procesa, ni siquiera el soberano', () => {
  const d = policy.decide({ killed: true, actorLogin: 'wmejiasbcn-tech', body: body({ de: 'soberano', para: 'ada' }), ...CONFIG, now: NOW });
  assert.equal(d.verdict, 'KILLED');
});

test('Formulario de Issue (### CAMPO) se lee igual que CAMPO:', () => {
  const m = policy.parseMessage('### DE\n\ncarla\n\n### PARA\n\nada\n\n### CAP\n\nsync.send\n\n### TRACE\n\n_No response_');
  assert.deepEqual([m.de, m.para, m.cap, m.trace], ['carla', 'ada', 'sync.send', null]);
});

// ---------- Flujo con GitHub falso ----------
test('Libro: un asiento con JSON, etiquetas de estado y asignación al soberano si hay DENY', async () => {
  const { github, state, addIssue } = fakeGithub();
  const issue = addIssue(1, 'ada-bot', body({ de: 'ada', para: 'zara' }));
  await portero.processIssue({ github, repo: REPO, issue, config: CONFIG, killed: false, now: NOW, runId: 7 });
  const l = ledgers(state, 1);
  assert.equal(l.length, 1);
  const entry = portero.lastLedger(l);
  assert.equal(entry.verdict, 'DENY');
  assert.equal(entry.run, 7);
  assert.ok(issue.labels.includes('bus:denied'));
  assert.ok(issue.labels.includes('to:soberano'));
  assert.deepEqual(issue.assignees, ['wmejiasbcn-tech']);
});

test('Idempotencia: procesar dos veces el mismo Issue no duplica el asiento', async () => {
  const { github, state, addIssue } = fakeGithub();
  const issue = addIssue(2, 'carla-bot', body({ de: 'carla', para: 'ada' }));
  await portero.processIssue({ github, repo: REPO, issue, config: CONFIG, killed: false, now: NOW });
  const again = await portero.processIssue({ github, repo: REPO, issue, config: CONFIG, killed: false, now: NOW });
  assert.equal(again.skipped, true);
  assert.equal(ledgers(state, 2).length, 1);
});

test('Apagado y recuperación: KILLED mientras está apagado; al encender, el barrido lo procesa una vez', async () => {
  const { github, state, addIssue } = fakeGithub();
  const issue = addIssue(3, 'carla-bot', body({ de: 'carla', para: 'ada' }));
  await portero.processIssue({ github, repo: REPO, issue, config: CONFIG, killed: true, now: NOW });
  assert.ok(issue.labels.includes('bus:killed'));
  const stillOff = await portero.sweep({ github, repo: REPO, config: CONFIG, killed: true, now: NOW, stallHours: 24 });
  assert.equal(stillOff.killed, true);
  assert.equal(ledgers(state, 3).length, 1);
  const on = await portero.sweep({ github, repo: REPO, config: CONFIG, killed: false, now: NOW, stallHours: 24 });
  assert.deepEqual(on.processed, [3]);
  assert.ok(issue.labels.includes('bus:allowed'));
  assert.ok(!issue.labels.includes('bus:killed'));
  await portero.sweep({ github, repo: REPO, config: CONFIG, killed: false, now: NOW, stallHours: 24 });
  assert.equal(ledgers(state, 3).length, 2); // KILLED + ALLOW, sin tercero
});

test('Recuperación: un Issue que nunca se procesó (caída del workflow) lo recoge el barrido', async () => {
  const { github, state, addIssue } = fakeGithub();
  addIssue(4, 'wmejiasbcn-tech', body({ de: 'soberano', para: 'carla' }));
  const r = await portero.sweep({ github, repo: REPO, config: CONFIG, killed: false, now: NOW, stallHours: 24 });
  assert.deepEqual(r.processed, [4]);
  assert.equal(ledgers(state, 4).length, 1);
});

test('Recibido: solo cuenta el comentario de una cuenta del nodo destino', async () => {
  const { github, state, addIssue } = fakeGithub();
  const issue = addIssue(5, 'carla-bot', body({ de: 'carla', para: 'ada' }));
  await portero.processIssue({ github, repo: REPO, issue, config: CONFIG, killed: false, now: NOW });
  const no = await portero.processComment({ github, repo: REPO, issue, comment: { user: { login: 'wmejiasbcn-tech' } }, config: CONFIG });
  assert.equal(no.received, false);
  const yes = await portero.processComment({ github, repo: REPO, issue, comment: { user: { login: 'ada-bot' } }, config: CONFIG });
  assert.equal(yes.received, true);
  assert.ok(issue.labels.includes('bus:received'));
  assert.ok(!issue.labels.includes('bus:allowed'));
});

test('Atasco: ALLOW sin respuesta del destino tras 24 h → bus:stalled + aviso; con respuesta, no', async () => {
  const { github, state, addIssue } = fakeGithub();
  const a = addIssue(6, 'carla-bot', body({ de: 'carla', para: 'ada' }));
  const b = addIssue(7, 'carla-bot', body({ de: 'carla', para: 'ada' }));
  await portero.processIssue({ github, repo: REPO, issue: a, config: CONFIG, killed: false, now: NOW });
  await portero.processIssue({ github, repo: REPO, issue: b, config: CONFIG, killed: false, now: NOW });
  state.comments.get(7).push({ id: 99, body: 'recibido', user: { login: 'ada-bot' }, created_at: '2026-11-01T11:00:00Z' });
  const later = new Date(NOW.getTime() + 25 * 3600 * 1000);
  const r = await portero.sweep({ github, repo: REPO, config: CONFIG, killed: false, now: later, stallHours: 24 });
  assert.deepEqual(r.stalled, [6]);
  assert.ok(a.labels.includes('bus:stalled'));
  assert.ok(!b.labels.includes('bus:stalled'));
});

test('Hermes: sin URL no se envía nada; con secreto corto tampoco', async () => {
  let calls = 0;
  const f = async () => { calls++; return { ok: true, status: 204 }; };
  assert.equal((await portero.forwardToHermes({}, {}, f)).sent, false);
  assert.equal((await portero.forwardToHermes({ HERMES_WEBHOOK_URL: 'https://x', HERMES_WEBHOOK_SECRET: 'corto' }, {}, f)).sent, false);
  assert.equal(calls, 0);
  assert.equal((await portero.forwardToHermes({ HERMES_WEBHOOK_URL: 'https://x', HERMES_WEBHOOK_SECRET: 'x'.repeat(32) }, {}, f)).sent, true);
});

test('Archivos reales: con permits.json del piloto (PENDIENTE) todo es DENY, incluido el soberano', () => {
  const nodes = require('../nodes.json');
  const permits = require('../permits.json').permits;
  const d = policy.decide({ actorLogin: 'wmejiasbcn-tech', body: body({ de: 'soberano', para: 'ada' }), nodes, permits, now: NOW });
  assert.equal(d.verdict, 'DENY');
});
