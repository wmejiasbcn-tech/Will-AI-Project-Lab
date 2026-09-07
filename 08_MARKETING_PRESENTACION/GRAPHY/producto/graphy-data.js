// GRAPHY 0.3 — DATOS
// Capa de datos separada de la presentación y de la interacción. La topología vive aquí:
// la interfaz no la conoce, solo la recorre. Se puede sustituir este fichero sin tocar la vista.
//
// Procedencia de cada relación:
//   'master'      → declarada en el master de la Carta (ui_kits/carta-presentacion/presences.js)
//   'mvp'         → observada en el MVP 001-030 validado
//   'experimental'→ propuesta de esta fase, sin respaldo todavía
// No se declara ninguna relación entre Presence concretas: el master no las fija y el MVP
// las produce en tiempo de ejecución, distintas en cada corrida. Su ausencia es deliberada.

export const LEVELS = {
  ecosystem: { label: 'Ecosistema', order: 0 },
  domain: { label: 'Dominio', order: 1 },
  presence: { label: 'Presencia', order: 2 },
  relationship: { label: 'Relación', order: 3 }
};

// El master de la Carta es la fuente de las presencias. Se lee en cada consulta, nunca en una
// instantanea al cargar el modulo: el bundle del sistema de diseno se carga de forma asincrona y
// nada garantiza que ya este disponible. Si todavia no lo esta, el nodo queda identificado pero
// sin voz, y se resuelve solo en cuanto el master aparece.
function master() {
  const ns = typeof window !== 'undefined' ? window.WillAIProjectLabDesignSystem_9c5006 : null;
  return ns && Array.isArray(ns.NODES) ? ns.NODES : [];
}

// Correspondencia entre el id de topologia y el id del master.
const MASTER_ID = { carla: 'carla-eco', ada: 'ada', aletheia: 'aletheia', itaca: 'itaca',
  'aether-hermes': 'aether-hermes', sylvia: 'sylvia', elena: 'elena', ariadna: 'ariadna',
  nova: 'nova', zara: 'zara', aurea: 'aurea' };

const PRESENCE_IDS = Object.keys(MASTER_ID);

const VIOLET = ['ada', 'aletheia', 'itaca', 'ariadna'];

function fromMaster(id) {
  const m = master().find((n) => n.id === MASTER_ID[id]);
  return {
    name: m ? m.name : id,
    kind: m ? m.role : 'Presencia del ecosistema',
    note: m ? m.quote : 'Voz no disponible: el master no esta cargado.',
    accent: VIOLET.indexOf(id) >= 0 ? 'violet' : 'gold'
  };
}

const STRUCTURAL = [
  { id: 'waipl', level: 'ecosystem', name: 'WAIPL', kind: 'Ecosistema de inteligencias',
    note: 'Un humano y once inteligencias que han decidido no competir, sino co-evolucionar.', accent: 'gold' },

  { id: 'william', level: 'domain', name: 'William Mejías Navarro', kind: 'Fundador soberano',
    note: 'Criterio humano final. No se delega ni se simula.', accent: 'white' },
  { id: 'lab', level: 'domain', name: 'Will-AI Project Lab', kind: 'Laboratorio vivo',
    note: 'Donde las once presencias trabajan. Muestra el comportamiento.', accent: 'gold' },
  { id: 'graphy', level: 'domain', name: 'Graphy', kind: 'Representación relacional',
    note: 'Muestra la estructura. Fase experimental.', accent: 'violet' },

];

const PRESENCES = PRESENCE_IDS;

// La lista completa se compone en cada lectura, de modo que las presencias siempre reflejan el
// master vigente. Las presencias no se escriben aqui: solo se declara su lugar en la topologia.
export function nodes() {
  return STRUCTURAL.concat(PRESENCE_IDS.map((id) => Object.assign({ id: id, level: 'presence' }, fromMaster(id))));
}

// Compatibilidad de lectura: NODES sigue disponible y se recalcula en cada acceso.
export const NODES = new Proxy([], {
  get(_t, prop) {
    const list = nodes();
    const v = list[prop];
    return typeof v === 'function' ? v.bind(list) : v;
  },
  has(_t, prop) { return prop in nodes(); },
  ownKeys() { return Reflect.ownKeys(nodes()); },
  getOwnPropertyDescriptor(_t, prop) {
    return Object.getOwnPropertyDescriptor(nodes(), prop);
  }
});

export const EDGES = [
  { from: 'waipl', to: 'william', rel: 'criterio', source: 'master' },
  { from: 'waipl', to: 'lab', rel: 'pertenencia', source: 'master' },
  { from: 'waipl', to: 'graphy', rel: 'pertenencia', source: 'experimental' },
  ...PRESENCES.map((id) => ({ from: 'lab', to: id, rel: 'habita', source: 'master' })),
  ...PRESENCES.map((id) => ({ from: 'graphy', to: id, rel: 'representa', source: 'experimental' }))
];

export const RELATIONS = {
  criterio: { label: 'Criterio', note: 'El ecosistema se sostiene en un criterio humano.' },
  pertenencia: { label: 'Pertenencia', note: 'Forma parte del ecosistema.' },
  habita: { label: 'Habita', note: 'La presencia trabaja dentro del laboratorio.' },
  representa: { label: 'Representa', note: 'Graphy hace visible su lugar en la estructura.' }
};

// La colaboración entre presencias existe en el laboratorio, pero no como topología fija.
export const ABSENT = [
  { what: 'Relaciones entre Presence concretas',
    why: 'El master no las fija y el laboratorio las produce en cada corrida. Se observan allí, no aquí.' },
  { what: 'Jerarquía entre presencias',
    why: 'El orden del master es de presentación, no de rango. No hay núcleo ni colaboradores.' }
];

// Tipos de relación con su tratamiento visual. El trazo distingue el tipo; el color, la
// procedencia. Nada se anima de forma continua.
export const RELATION_TYPES = {
  criterio: { label: 'Criterio', stroke: 'solid', width: 0.3 },
  pertenencia: { label: 'Pertenencia', stroke: 'solid', width: 0.22 },
  habita: { label: 'Habita', stroke: 'solid', width: 0.2 },
  representa: { label: 'Representa', stroke: 'dashed', width: 0.2 },
};

export const PROVENANCE = {
  master: { label: 'Master de la Carta', status: 'declarada', color: '#C9A86A' },
  mvp: { label: 'Observada en el laboratorio', status: 'observada', color: '#C9A86A' },
  experimental: { label: 'Propuesta de esta fase', status: 'experimental', color: '#9C81BD' },
  // Categoria conservada y diferenciada: hoy no se emite ninguna relacion deducida, porque
  // deducir por co-presencia esta prohibido. Se mantiene para no perder la distincion.
  derived: { label: 'Deducida', status: 'deducida', color: '#6E6E78' }
};

// Estados relacionales. El estado no vive en los datos: lo fija la interaccion y se aplica
// sobre este modelo. Graphy representa; no decide ni ejecuta.
export const REL_STATES = {
  INACTIVE: { label: 'Inactiva', opacity: 0.5, visibility: 'visible' },
  ACTIVE: { label: 'Activa', opacity: 0.9, visibility: 'visible' },
  FOCUSED: { label: 'En foco', opacity: 1, visibility: 'visible' },
  DIMMED: { label: 'Atenuada', opacity: 0.22, visibility: 'attenuated' }
};

// Reloj determinista propio: avanza solo cuando Graphy registra una interaccion. Sin reloj real,
// sin scheduler, sin bucles. Una misma secuencia de interacciones da los mismos sellos.
let SIM_TICK = 0;
export function tickSimulated() { return ++SIM_TICK; }
export function nowSimulated() { return SIM_TICK; }
export function resetSimulated() { SIM_TICK = 0; }

export function relationId(r) { return r.source + '→' + r.target + ':' + r.type; }

// Registro normalizado de relaciones: source, target, type, provenance, status.
// Solo se emiten relaciones declaradas. No se deduce ninguna arista entre presencias por el
// hecho de compartir laboratorio: la travesia entre presencias pasa por la arista declarada
// al laboratorio, que ya existe.
export function relationships() {
  const out = EDGES.map((e) => {
    const t = RELATION_TYPES[e.rel] || {};
    return {
      id: e.from + '→' + e.to + ':' + e.rel,
      source: e.from, target: e.to, type: e.rel, provenance: e.source,
      status: (PROVENANCE[e.source] || {}).status || 'sin clasificar', basis: null,
      // El peso relativo procede del propio modelo de tipos declarado arriba, no de una
      // medicion del ecosistema: no se inventa ningun dato sobre el laboratorio.
      weight: t.width != null ? t.width : 0.2,
      state: 'INACTIVE',
      visibility: 'visible',
      updatedAtSimulated: nowSimulated()
    };
  });
  return out;
}

// Relaciones de un nodo, con su tipo y su procedencia. No altera nada del master.
export function relationshipsOf(id) {
  const out = [];
  for (const r of relationships()) {
    if (r.source === id) out.push({ id: r.target, type: r.type, provenance: r.provenance, status: r.status, basis: r.basis, dir: 'out' });
    else if (r.target === id) out.push({ id: r.source, type: r.type, provenance: r.provenance, status: r.status, basis: r.basis, dir: 'in' });
  }
  return out;
}

export function neighborsOf(id) {
  const out = [];
  for (const e of EDGES) {
    if (e.from === id) out.push({ id: e.to, rel: e.rel, source: e.source, dir: 'out' });
    else if (e.to === id) out.push({ id: e.from, rel: e.rel, source: e.source, dir: 'in' });
  }
  return out;
}

export function nodeById(id) {
  for (const n of nodes()) if (n.id === id) return n;
  return null;
}
