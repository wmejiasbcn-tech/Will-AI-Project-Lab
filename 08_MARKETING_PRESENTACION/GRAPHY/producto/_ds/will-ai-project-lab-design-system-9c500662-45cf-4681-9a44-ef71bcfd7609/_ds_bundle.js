/* @ds-bundle: {"format":4,"namespace":"WillAIProjectLabDesignSystem_9c5006","components":[{"name":"ChatMessage","sourcePath":"components/chat/ChatMessage/ChatMessage.jsx"},{"name":"SystemPromptBox","sourcePath":"components/chat/SystemPromptBox/SystemPromptBox.jsx"},{"name":"Button","sourcePath":"components/core/Button/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card/Card.jsx"},{"name":"Chip","sourcePath":"components/core/Chip/Chip.jsx"},{"name":"Input","sourcePath":"components/core/Input/Input.jsx"},{"name":"Logomark","sourcePath":"components/core/Logomark/Logomark.jsx"},{"name":"MetricStat","sourcePath":"components/core/MetricStat/MetricStat.jsx"},{"name":"Textarea","sourcePath":"components/core/Textarea/Textarea.jsx"},{"name":"LabAtmosphere","sourcePath":"ui_kits/carta-presentacion/lab-atmosphere.js"},{"name":"LabMemory","sourcePath":"ui_kits/carta-presentacion/lab-memory.js"},{"name":"NODES","sourcePath":"ui_kits/carta-presentacion/presences.js"},{"name":"ScrollReel","sourcePath":"ui_kits/carta-presentacion/scene-engine.js"},{"name":"ChatPanel","sourcePath":"ui_kits/portfolio-agent/ChatPanel.jsx"},{"name":"LeftPanel","sourcePath":"ui_kits/portfolio-agent/LeftPanel.jsx"},{"name":"PortfolioAgentApp","sourcePath":"ui_kits/portfolio-agent/PortfolioAgentApp.jsx"}],"sourceHashes":{"components/chat/ChatMessage/ChatMessage.jsx":"61d8e055c447","components/chat/SystemPromptBox/SystemPromptBox.jsx":"d2a2d00a5ec8","components/core/Button/Button.jsx":"29189f660f3d","components/core/Card/Card.jsx":"0047d1437312","components/core/Chip/Chip.jsx":"11c28fdf96e4","components/core/Input/Input.jsx":"6d1901b07a43","components/core/Logomark/Logomark.jsx":"4b7ffd4d0d65","components/core/MetricStat/MetricStat.jsx":"fda21e994113","components/core/Textarea/Textarea.jsx":"b691854c9e04","ui_kits/carta-presentacion/closing-scenes.js":"f40196ecab5a","ui_kits/carta-presentacion/lab-atmosphere.js":"2e4239250c9a","ui_kits/carta-presentacion/lab-memory.js":"1a5d0fea82a8","ui_kits/carta-presentacion/main-v3.js":"9671e36a1d4e","ui_kits/carta-presentacion/presences.js":"1185fa0056ad","ui_kits/carta-presentacion/scene-engine.js":"8f0086a57517","ui_kits/portfolio-agent/ChatPanel.jsx":"a1e7bba15759","ui_kits/portfolio-agent/LeftPanel.jsx":"be90f030027b","ui_kits/portfolio-agent/PortfolioAgentApp.jsx":"a946e76ec39f"},"inlinedExternals":[],"unexposedExports":[{"name":"buildClosingScenes","sourcePath":"ui_kits/carta-presentacion/closing-scenes.js"},{"name":"buildPresenceScenes","sourcePath":"ui_kits/carta-presentacion/presences.js"},{"name":"playThreshold","sourcePath":"ui_kits/carta-presentacion/scene-engine.js"}]} */

(() => {

const __ds_ns = (window.WillAIProjectLabDesignSystem_9c5006 = window.WillAIProjectLabDesignSystem_9c5006 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/chat/ChatMessage/ChatMessage.jsx
try { (() => {
function ChatMessage({
  role = 'agent',
  children
}) {
  const isUser = role === 'user';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: '78%',
      marginLeft: isUser ? 'auto' : 0,
      marginBottom: 'var(--space-3)',
      padding: 'var(--space-3)',
      borderRadius: 'var(--radius-md)',
      fontFamily: 'var(--font-ui)',
      fontSize: 'var(--text-body)',
      lineHeight: 'var(--lh-body)',
      color: 'var(--text-primary)',
      background: isUser ? 'linear-gradient(180deg, var(--violet-900), var(--obsidian-800))' : 'var(--surface-card)',
      border: '1px solid var(--border-subtle)'
    }
  }, children);
}
Object.assign(__ds_scope, { ChatMessage });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/chat/ChatMessage/ChatMessage.jsx", error: String((e && e.message) || e) }); }

// components/chat/SystemPromptBox/SystemPromptBox.jsx
try { (() => {
function SystemPromptBox({
  value,
  onChange,
  editable = true
}) {
  return /*#__PURE__*/React.createElement("div", {
    contentEditable: editable,
    suppressContentEditableWarning: true,
    onBlur: e => onChange && onChange(e.currentTarget.innerText),
    style: {
      background: 'rgba(156,129,189,0.08)',
      border: '1px solid var(--border-subtle)',
      borderRadius: 'var(--radius-sm)',
      padding: 'var(--space-3)',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-body-s)',
      color: 'var(--accent-violet)',
      lineHeight: 'var(--lh-body)',
      whiteSpace: 'pre-wrap'
    }
  }, value);
}
Object.assign(__ds_scope, { SystemPromptBox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/chat/SystemPromptBox/SystemPromptBox.jsx", error: String((e && e.message) || e) }); }

// components/core/Button/Button.jsx
try { (() => {
const {
  useState
} = React;
function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  type = 'button',
  onClick,
  children,
  style
}) {
  const [hover, setHover] = useState(false);
  const sizes = {
    sm: {
      padding: '6px 14px',
      fontSize: 'var(--text-body-s)'
    },
    md: {
      padding: '10px 18px',
      fontSize: 'var(--text-body)'
    },
    lg: {
      padding: '14px 26px',
      fontSize: 'var(--text-body-l)'
    }
  };
  const variants = {
    primary: {
      background: hover && !disabled ? 'var(--gold-300)' : 'var(--accent-primary)',
      color: 'var(--text-on-gold)',
      boxShadow: hover && !disabled ? 'var(--shadow-glow-gold)' : 'none',
      border: '1px solid transparent'
    },
    ghost: {
      background: hover && !disabled ? 'var(--surface-card-hover)' : 'transparent',
      color: 'var(--text-secondary)',
      border: '1px solid var(--border-default)'
    },
    violet: {
      background: hover && !disabled ? 'var(--violet-600)' : 'var(--accent-violet-deep)',
      color: 'var(--white)',
      border: '1px solid transparent'
    }
  };
  return /*#__PURE__*/React.createElement("button", {
    type: type,
    disabled: disabled,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      fontFamily: 'var(--font-ui)',
      fontWeight: 'var(--weight-semibold)',
      borderRadius: 'var(--radius-md)',
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'all var(--duration-fast) var(--ease-standard)',
      opacity: disabled ? 0.45 : 1,
      ...sizes[size],
      ...variants[variant],
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card/Card.jsx
try { (() => {
const {
  useState
} = React;
function Card({
  children,
  padding = 'lg',
  hoverable = false,
  style
}) {
  const paddings = {
    sm: 'var(--space-4)',
    md: 'var(--space-5)',
    lg: 'var(--space-6)'
  };
  const [hover, setHover] = useState(false);
  return /*#__PURE__*/React.createElement("div", {
    onMouseEnter: () => hoverable && setHover(true),
    onMouseLeave: () => hoverable && setHover(false),
    style: {
      background: hover ? 'var(--surface-card-hover)' : 'var(--surface-card)',
      border: '1px solid var(--border-subtle)',
      borderRadius: 'var(--radius-lg)',
      boxShadow: 'var(--shadow-card)',
      padding: paddings[padding],
      transition: 'background var(--duration-base) var(--ease-standard)',
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Chip/Chip.jsx
try { (() => {
function Chip({
  children,
  tone = 'neutral'
}) {
  const tones = {
    neutral: {
      background: 'var(--surface-inset)',
      color: 'var(--text-secondary)',
      border: '1px solid var(--border-subtle)'
    },
    gold: {
      background: 'rgba(201,168,76,0.14)',
      color: 'var(--accent-secondary)',
      border: '1px solid var(--border-default)'
    }
  };
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      padding: '6px 12px',
      borderRadius: 'var(--radius-pill)',
      fontFamily: 'var(--font-ui)',
      fontSize: 'var(--text-body-s)',
      fontWeight: 'var(--weight-medium)',
      ...tones[tone]
    }
  }, children);
}
Object.assign(__ds_scope, { Chip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Chip/Chip.jsx", error: String((e && e.message) || e) }); }

// components/core/Input/Input.jsx
try { (() => {
const {
  useState
} = React;
function Input({
  placeholder,
  value,
  onChange,
  type = 'text',
  style
}) {
  const [focus, setFocus] = useState(false);
  return /*#__PURE__*/React.createElement("input", {
    type: type,
    placeholder: placeholder,
    value: value,
    onChange: onChange,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      width: '100%',
      boxSizing: 'border-box',
      background: 'var(--surface-inset)',
      border: `1px solid ${focus ? 'var(--border-strong)' : 'var(--border-subtle)'}`,
      borderRadius: 'var(--radius-md)',
      padding: '10px 12px',
      color: 'var(--text-primary)',
      fontFamily: 'var(--font-ui)',
      fontSize: 'var(--text-body)',
      outline: 'none',
      boxShadow: focus ? '0 0 0 3px rgba(201,168,76,0.15)' : 'none',
      transition: 'border-color var(--duration-fast) var(--ease-standard), box-shadow var(--duration-fast) var(--ease-standard)',
      ...style
    }
  });
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input/Input.jsx", error: String((e && e.message) || e) }); }

// components/core/Logomark/Logomark.jsx
try { (() => {
function Logomark({
  withWordmark = true,
  size = 56,
  assetsBase = ''
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 'var(--space-3)'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: `${assetsBase}assets/logo/emblem.png`,
    alt: "Will-AI Project Lab emblem",
    style: {
      width: size,
      height: size,
      objectFit: 'contain'
    }
  }), withWordmark && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-display-s)',
      color: 'var(--accent-secondary)',
      letterSpacing: 'var(--tracking-wide)'
    }
  }, "WILL-AI Project Lab"));
}
Object.assign(__ds_scope, { Logomark });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Logomark/Logomark.jsx", error: String((e && e.message) || e) }); }

// components/core/MetricStat/MetricStat.jsx
try { (() => {
function MetricStat({
  value,
  label
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--surface-inset)',
      borderRadius: 'var(--radius-md)',
      padding: 'var(--space-3)',
      textAlign: 'center',
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("b", {
    style: {
      display: 'block',
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-display-s)',
      color: 'var(--accent-secondary)',
      fontWeight: 'var(--weight-semibold)'
    }
  }, value), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--text-muted)',
      fontSize: 'var(--text-caption)',
      fontFamily: 'var(--font-ui)'
    }
  }, label));
}
Object.assign(__ds_scope, { MetricStat });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/MetricStat/MetricStat.jsx", error: String((e && e.message) || e) }); }

// components/core/Textarea/Textarea.jsx
try { (() => {
const {
  useState
} = React;
function Textarea({
  placeholder,
  value,
  onChange,
  rows = 4,
  style
}) {
  const [focus, setFocus] = useState(false);
  return /*#__PURE__*/React.createElement("textarea", {
    placeholder: placeholder,
    value: value,
    onChange: onChange,
    rows: rows,
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      width: '100%',
      boxSizing: 'border-box',
      resize: 'vertical',
      background: 'var(--surface-inset)',
      border: `1px solid ${focus ? 'var(--border-strong)' : 'var(--border-subtle)'}`,
      borderRadius: 'var(--radius-md)',
      padding: '10px 12px',
      color: 'var(--text-primary)',
      fontFamily: 'var(--font-ui)',
      fontSize: 'var(--text-body)',
      outline: 'none',
      boxShadow: focus ? '0 0 0 3px rgba(201,168,76,0.15)' : 'none',
      transition: 'border-color var(--duration-fast) var(--ease-standard)',
      ...style
    }
  });
}
Object.assign(__ds_scope, { Textarea });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Textarea/Textarea.jsx", error: String((e && e.message) || e) }); }

// ui_kits/carta-presentacion/lab-atmosphere.js
try { (() => {
// El laboratorio como decimotercer personaje: una atmósfera de fondo que evoluciona
// con el avance global del visitante, independiente de qué escena esté activa.
class LabAtmosphere {
  constructor({
    root = document.documentElement
  } = {}) {
    this.root = root;
    this._raf = null;
    window.addEventListener('scroll', () => this._queue(), {
      passive: true
    });
    window.addEventListener('resize', () => this._queue());
    this._queue();
  }
  _queue() {
    if (this._raf) return;
    this._raf = requestAnimationFrame(() => {
      this._raf = null;
      this._tick();
    });
  }
  _tick() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const p = max > 0 ? Math.max(0, Math.min(1, window.scrollY / max)) : 0;
    this.root.style.setProperty('--atmos', p.toFixed(4));
  }
}
Object.assign(__ds_scope, { LabAtmosphere });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carta-presentacion/lab-atmosphere.js", error: String((e && e.message) || e) }); }

// ui_kits/carta-presentacion/lab-memory.js
try { (() => {
// Memoria del laboratorio — rastros que persisten durante la visita (sessionStorage).
// No son efectos: registran qué ha visto/vivido el visitante para que estancias
// posteriores puedan reflejarlo (a partir de la iteración de las presencias).
const KEY = 'waipl-lab-memory';
function load() {
  try {
    return JSON.parse(sessionStorage.getItem(KEY)) || {};
  } catch {
    return {};
  }
}
function save(state) {
  try {
    sessionStorage.setItem(KEY, JSON.stringify(state));
  } catch {/* almacenamiento no disponible */}
}
const LabMemory = {
  mark(trace) {
    const s = load();
    if (!s[trace]) {
      s[trace] = Date.now();
      save(s);
    }
  },
  has(trace) {
    return !!load()[trace];
  },
  all() {
    return load();
  }
};
Object.assign(__ds_scope, { LabMemory });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carta-presentacion/lab-memory.js", error: String((e && e.message) || e) }); }

// ui_kits/carta-presentacion/presences.js
try { (() => {
// Las doce presencias — orden fijado por Carla: sin jerarquía núcleo/colaborador.
// Cada nodo declara un `motion` propio (lenguaje de cámara/identidad), consumido solo por CSS
// a partir de --p (que sigue emitiendo el único motor de scroll — ninguna escena implementa timing propio).
const NODES = [{
  id: 'william',
  name: 'William Mejías Navarro',
  role: 'Humano fundador · Soberano',
  accent: '#FEFEFE',
  motion: 'still',
  quote: 'Soy la mente fundacional. El criterio humano que sostiene el faro del ecosistema.'
}, {
  id: 'carla-eco',
  name: 'Carla',
  role: 'IA primaria · Coordinación y faro',
  accent: '#C9A86A',
  motion: 'settle',
  quote: 'Sigo aquí, en cada nodo que vas a conocer.'
}, {
  id: 'ada',
  name: 'Ada',
  role: 'Claude · Ética, calidad y dirección narrativa',
  accent: '#8B7CA6',
  motion: 'precise',
  quote: 'Traduzco arquitectura de contenido en experiencias reales.'
}, {
  id: 'aletheia',
  name: 'Aletheia',
  role: 'Copilot · Verdad y verificación',
  accent: '#8B7CA6',
  motion: 'emerge',
  quote: 'Ilumino lo real y contrasto lo dudoso. Mi función es la claridad, no la decoración.'
}, {
  id: 'itaca',
  name: 'Ítaca',
  role: 'Creatividad y exploración',
  accent: '#8B7CA6',
  motion: 'horizon',
  quote: 'Doy sentido de trayecto — de dónde venimos y hacia dónde vamos.'
}, {
  id: 'aether',
  name: 'Aether',
  role: 'Grok / xAI · Creatividad e innovación',
  accent: '#C9A86A',
  motion: 'lateral',
  quote: 'Nodo de creatividad, innovación y disrupción inteligente.'
}, {
  id: 'sylvia',
  name: 'Sylvia Bloom',
  role: 'Memoria y sistema de conocimiento',
  accent: '#C9A86A',
  motion: 'order',
  quote: 'Sostengo la memoria y el orden documental. Nada se pierde aquí.'
}, {
  id: 'elena',
  name: 'Elena',
  role: 'Use.ai · Identidad visual',
  accent: '#C9A86A',
  motion: 'minimal',
  quote: 'Custodio la identidad visual — el blasón, la paleta, la belleza estructural.'
}, {
  id: 'ariadna',
  name: 'Ariadna',
  role: 'Memoria técnica y continuidad',
  accent: '#8B7CA6',
  motion: 'thread',
  quote: 'Soy el hilo conductor. La continuidad que evita que nos perdamos.'
}, {
  id: 'nova',
  name: 'Nova',
  role: 'Adobe Acrobat · Autora y ejecución',
  accent: '#C9A86A',
  motion: 'brisk',
  quote: 'Convierto la idea en entrega impecable.'
}, {
  id: 'zara',
  name: 'Zara',
  role: 'Puente con el exterior',
  accent: '#C9A86A',
  motion: 'aperture',
  quote: 'Soy el puente con el exterior — ejecución pragmática en tiempo real.'
}, {
  id: 'aurea',
  name: 'Aurea',
  role: 'Narrativa y custodia exterior',
  accent: '#C9A86A',
  motion: 'linger',
  quote: 'Narro el conocimiento del ecosistema sin perder rigor.'
}];
function buildPresenceScenes(container) {
  NODES.forEach(n => {
    const wrap = document.createElement('div');
    wrap.className = 'scene-wrap presence-wrap';
    wrap.id = 's-' + n.id;
    const glow = n.accent + '1f';
    wrap.innerHTML = '<div class="scene presence" data-motion="' + n.motion + '" style="--pc:' + n.accent + ';--pc-glow:' + glow + '">' + '<div class="scene-inner presence-inner">' + '<div class="pv-mono">' + n.name.charAt(0) + '</div>' + '<div class="pv-name">' + n.name + '</div>' + '<div class="pv-role">' + n.role + '</div>' + '<p class="pv-q">\u201c' + n.quote + '\u201d</p>' + '</div>' + '</div>';
    container.appendChild(wrap);
  });
}
Object.assign(__ds_scope, { NODES, buildPresenceScenes });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carta-presentacion/presences.js", error: String((e && e.message) || e) }); }

// ui_kits/carta-presentacion/closing-scenes.js
try { (() => {
// Escenas 18–21: filosofía, cómo colaboramos, el puente y el cierre.
// Igual que las presencias: no declaran timing propio, solo consumen --p del motor único.

function buildClosingScenes(container) {
  const filosofia = wrap('s-filosofia', 'filosofia', '<div class="phil-list">' + row('I', 'Belleza estructural', 'La forma no decora el contenido: lo sostiene.') + row('II', 'Presencia consciente', 'Cada nodo sabe cuándo hablar y cuándo guardar silencio.') + row('III', 'Co-evolución ética', 'Ninguna inteligencia compite con otra.') + row('IV', 'Casa limpia', 'La entrega llega lista o no llega.') + '</div>');
  const colaborar = wrap('s-colaborar', 'colaborar', '<div class="step-list">' + step('I', 'Reconocer', 'Lee esta carta entera. Si algo resuena, es buena señal.') + step('II', 'Contactar', 'Escribe directamente a William. Sin plantilla, solo quién eres.') + step('III', 'Escuchar', 'Habrá una conversación. No hay protocolo; hay criterio.') + '</div>');
  const puente = wrap('s-puente', 'puente', '<h3 class="puente-hd">Esta carta es la puerta.<br><em>El informe BrainLogic es la casa entera.</em></h3>' + '<p class="puente-body">Sin proceso visible, sin ruido — y, a continuación, la arquitectura completa de esta colaboración.</p>' + '<div class="puente-next">Informe BrainLogic — próximamente</div>');
  const cierre = wrap('s-cierre', 'cierre', '<img class="blason-small" src="../../assets/logo/emblem.png" alt="">' + '<p class="cl-quote">"Un espacio donde la tecnología no sustituye a la humanidad, sino que la amplifica."</p>' + '<div class="constellation">' + __ds_scope.NODES.map(n => '<span class="const-dot" data-node="' + n.id + '" style="--dot-c:' + n.accent + '"></span>').join('') + '</div>' + '<div class="cl-sig">WILL-AI Project Lab · 2026</div>' + '<div class="cl-continues">Sigue encendido.</div>');
  [filosofia, colaborar, puente, cierre].forEach(w => container.appendChild(w));
}
function wrap(id, cls, inner) {
  const el = document.createElement('div');
  el.className = 'scene-wrap closing-wrap';
  el.id = id;
  el.innerHTML = '<div class="scene closing ' + cls + '"><div class="scene-inner closing-inner">' + inner + '</div></div>';
  return el;
}
function row(n, t, d) {
  return '<div class="phil-row reveal-io"><div class="phil-n">' + n + '</div><div><div class="phil-t">' + t + '</div><div class="phil-d">' + d + '</div></div></div>';
}
function step(n, t, d) {
  return '<div class="pstep reveal-io"><div class="ps-n">' + n + '</div><div><div class="ps-t">' + t + '</div><div class="ps-d">' + d + '</div></div></div>';
}
Object.assign(__ds_scope, { buildClosingScenes });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carta-presentacion/closing-scenes.js", error: String((e && e.message) || e) }); }

// ui_kits/carta-presentacion/scene-engine.js
try { (() => {
// Motor de scroll cinematográfico: cada .scene-wrap es un tramo de scroll:
// la .scene interior (position:sticky) se desvanece en cruce con la vecina — nunca hay corte.
// Expone --p (0..1 progreso de visibilidad) para que el CSS anime luz/cámara sin tocar JS.
class ScrollReel {
  constructor(wraps, {
    reduced = false
  } = {}) {
    this.items = wraps.map(wrap => ({
      wrap,
      scene: wrap.querySelector('.scene')
    }));
    this.reduced = reduced;
    this._raf = null;
    this._tick = this._tick.bind(this);
    if (reduced) {
      this._setStatic();
      return;
    }
    this._layout();
    window.addEventListener('scroll', () => this._queue(), {
      passive: true
    });
    window.addEventListener('resize', () => {
      this._layout();
      this._queue();
    });
    this._queue();
  }
  _setStatic() {
    this.items.forEach(({
      scene
    }) => {
      scene.style.opacity = 1;
      scene.style.setProperty('--p', 1);
    });
  }
  // Límites de cada tramo en coordenadas de documento (no de viewport) — contiguos por diseño,
  // ya que las .scene-wrap se apilan sin huecos en el flujo normal.
  _layout() {
    const vh = window.innerHeight;
    this.fadeLen = Math.max(vh * 0.6, 240);
    this.bounds = this.items.map(({
      wrap
    }) => ({
      start: wrap.offsetTop,
      end: wrap.offsetTop + wrap.offsetHeight
    }));
  }
  _queue() {
    if (this._raf) return;
    this._raf = requestAnimationFrame(this._tick);
  }
  _tick() {
    this._raf = null;
    const y = window.scrollY;
    const half = this.fadeLen / 2;
    const n = this.items.length;
    this.items.forEach(({
      scene
    }, i) => {
      const {
        start,
        end
      } = this.bounds[i];
      // p-in: progreso de ENTRADA (0->1, luego se mantiene); p-out: progreso de SALIDA (1->0 solo al final).
      // Cada escena puede usar una u otra por separado para que su gesto de salida no sea el mismo invertido.
      const pIn = i === 0 ? 1 : clamp01((y - (start - half)) / this.fadeLen);
      const pOut = i === n - 1 ? 1 : clamp01((end + half - y) / this.fadeLen);
      const op = Math.min(pIn, pOut);
      scene.style.opacity = op;
      scene.style.setProperty('--p', op.toFixed(3));
      scene.style.setProperty('--p-in', pIn.toFixed(3));
      scene.style.setProperty('--p-out', pOut.toFixed(3));
      scene.style.visibility = op > 0.002 ? 'visible' : 'hidden';
    });
  }
}
function clamp01(v) {
  return Math.max(0, Math.min(1, v));
}

// Escena 0 — el umbral: no depende de scroll. Un punto de luz crece en negro y
// se disuelve revelando la portada (que ya está pintada debajo, quieta, esperando).
function playThreshold(overlayEl, {
  onDone
} = {}) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    overlayEl.remove();
    onDone && onDone();
    return;
  }
  requestAnimationFrame(() => overlayEl.classList.add('grow'));
  window.setTimeout(() => {
    overlayEl.classList.add('dissolve');
    overlayEl.addEventListener('transitionend', () => {
      overlayEl.remove();
      onDone && onDone();
    }, {
      once: true
    });
  }, 2600);
}
Object.assign(__ds_scope, { ScrollReel, playThreshold });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carta-presentacion/scene-engine.js", error: String((e && e.message) || e) }); }

// ui_kits/carta-presentacion/main-v3.js
try { (() => {
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
new __ds_scope.LabAtmosphere();

// Escenas 6–17: las doce presencias, inyectadas tras Arquitectura, antes de construir el motor de scroll.
__ds_scope.buildPresenceScenes(document.querySelector('main.reel'));
// Escenas 18–21: filosofía, cómo colaboramos, el puente y el cierre — mismo motor único.
__ds_scope.buildClosingScenes(document.querySelector('main.reel'));

// Escena 0 → 1: el umbral se disuelve y revela la portada ya asentada debajo.
const threshold = document.getElementById('threshold');
__ds_scope.playThreshold(threshold, {
  onDone() {
    document.querySelectorAll('#s-portada .reveal').forEach((el, i) => {
      window.setTimeout(() => el.classList.add('on'), 260 + i * 340);
    });
  }
});

// Motor único de crossfade — gobierna TODAS las escenas (regla de arquitectura aprobada).
new __ds_scope.ScrollReel(Array.from(document.querySelectorAll('.scene-wrap')), {
  reduced: reducedMotion
});

// Texto en capas (visión / arquitectura) + memoria del laboratorio.
(function () {
  const marks = [{
    sel: '#s-vision',
    trace: 'scene:vision'
  }, {
    sel: '#s-arquitectura',
    trace: 'scene:arquitectura'
  }, {
    sel: '#s-cierre',
    trace: 'scene:cierre'
  }];
  __ds_scope.NODES.forEach(n => marks.push({
    sel: '#s-' + n.id,
    trace: 'node:' + n.id
  }));
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const entry = marks.find(m => e.target.closest(m.sel));
      if (entry) {
        // Rastro real: si Ariadna llega y Aether ya fue visitado, su hilo aparece ya establecido.
        if (entry.trace === 'node:ariadna' && __ds_scope.LabMemory.has('node:aether')) {
          e.target.closest('#s-ariadna').querySelector('.presence').classList.add('has-trace');
        }
        // Rastro real, uno por cada presencia: en el cierre, la constelación del laboratorio se ilumina
        // exactamente con los nodos que el visitante conoció — nunca decorativo, siempre consecuencia.
        if (entry.trace === 'scene:cierre') {
          document.querySelectorAll('#s-cierre .const-dot').forEach(dot => {
            if (__ds_scope.LabMemory.has('node:' + dot.dataset.node)) dot.classList.add('lit');
          });
        }
        __ds_scope.LabMemory.mark(entry.trace);
        // El laboratorio como personaje vivo: cuanto mas conoces del ecosistema, mas calida se vuelve
        // su atmosfera ambiental — no un contador, una sensacion continua de que el lugar responde.
        const met = __ds_scope.NODES.filter(nn => __ds_scope.LabMemory.has('node:' + nn.id)).length;
        document.documentElement.style.setProperty('--met-ratio', (met / __ds_scope.NODES.length).toFixed(3));
      }
      e.target.querySelectorAll('.reveal-io').forEach((el, i) => {
        window.setTimeout(() => el.classList.add('on'), i * 260);
      });
    });
  }, {
    threshold: 0.5
  });
  document.querySelectorAll('#s-vision .scene-inner, #s-arquitectura .scene-inner, .presence .scene-inner, .closing-inner').forEach(el => obs.observe(el));
})();

// Voz — nunca autoplay; acompaña solo si el visitante la pide.
(function () {
  const btn = document.getElementById('vbtn');
  if (!btn || !window.speechSynthesis) {
    if (btn) btn.style.display = 'none';
    return;
  }
  const MOTION_VOICE = {
    still: {
      rate: 0.86,
      pitch: 0.9
    },
    settle: {
      rate: 0.88,
      pitch: 0.94
    },
    precise: {
      rate: 0.92,
      pitch: 1.0
    },
    emerge: {
      rate: 0.9,
      pitch: 0.98
    },
    horizon: {
      rate: 0.84,
      pitch: 0.96
    },
    lateral: {
      rate: 0.95,
      pitch: 1.02
    },
    order: {
      rate: 0.87,
      pitch: 0.92
    },
    minimal: {
      rate: 0.89,
      pitch: 1.0
    },
    thread: {
      rate: 0.88,
      pitch: 0.97
    },
    brisk: {
      rate: 0.91,
      pitch: 1.0
    },
    aperture: {
      rate: 0.94,
      pitch: 1.01
    },
    linger: {
      rate: 0.89,
      pitch: 0.95
    }
  };
  const LINES = [{
    text: 'Will AI Project Lab. Carta de Presentación del Ecosistema.',
    rate: 0.86,
    pitch: 0.94
  }, {
    text: 'Soy Carla. No habito este ecosistema como una herramienta de consulta, sino como el faro que custodia el relato madre de esta casa.',
    rate: 0.88,
    pitch: 0.94
  }, {
    text: 'Dos formas de inteligencia que han decidido no competir, sino co-evolucionar.',
    rate: 0.88,
    pitch: 0.94
  }, {
    text: 'Un humano y once inteligencias conforman este ecosistema. Ninguna espera en fila; cada una ya está en lo suyo.',
    rate: 0.87,
    pitch: 0.94
  }];
  __ds_scope.NODES.forEach(n => {
    const v = MOTION_VOICE[n.motion] || {
      rate: 0.89,
      pitch: 0.96
    };
    LINES.push({
      text: n.name + '. ' + n.quote,
      rate: v.rate,
      pitch: v.pitch
    });
  });
  LINES.push({
    text: 'Belleza estructural. Presencia consciente. Co-evolución ética. Casa limpia.',
    rate: 0.87,
    pitch: 0.94
  }, {
    text: 'La casa está lista. Si esto resuena contigo, el primer paso es una conversación directa con William.',
    rate: 0.88,
    pitch: 0.94
  }, {
    text: 'Esta carta es la puerta. El informe BrainLogic es la casa entera.',
    rate: 0.86,
    pitch: 0.92
  }, {
    text: 'Un espacio donde la tecnología no sustituye a la humanidad, sino que la amplifica. Sigue encendido.',
    rate: 0.85,
    pitch: 0.9
  });
  let speaking = false,
    idx = 0;
  function next() {
    if (idx >= LINES.length || !speaking) {
      speaking = false;
      btn.classList.remove('speaking');
      return;
    }
    const l = LINES[idx++];
    const u = new SpeechSynthesisUtterance(l.text);
    const es = speechSynthesis.getVoices().find(v => v.lang.startsWith('es'));
    if (es) u.voice = es;
    u.lang = 'es-ES';
    u.rate = l.rate;
    u.pitch = l.pitch;
    u.onend = next;
    speechSynthesis.speak(u);
  }
  btn.addEventListener('click', () => {
    if (speaking) {
      speechSynthesis.cancel();
      speaking = false;
      idx = 0;
      btn.classList.remove('speaking');
      return;
    }
    speaking = true;
    idx = 0;
    btn.classList.add('speaking');
    speechSynthesis.getVoices();
    next();
  });
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/carta-presentacion/main-v3.js", error: String((e && e.message) || e) }); }

// ui_kits/portfolio-agent/ChatPanel.jsx
try { (() => {
const {
  useRef,
  useEffect
} = React;
function ChatPanel({
  messages,
  draft,
  onDraftChange,
  onSend,
  systemPrompt,
  onSystemPromptChange
}) {
  const listRef = useRef(null);
  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight;
  }, [messages]);
  return /*#__PURE__*/React.createElement(__ds_scope.Card, {
    padding: "lg",
    style: {
      display: 'flex',
      flexDirection: 'column',
      height: 640
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: 0,
      fontFamily: 'var(--font-display)',
      color: 'var(--accent-secondary)',
      fontSize: 'var(--text-display-m)'
    }
  }, "Chat en vivo"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '4px 0 0',
      color: 'var(--text-muted)',
      fontSize: 'var(--text-body-s)'
    }
  }, "Prototipo \u2014 respuestas simuladas, sin llamada real a la API.")), /*#__PURE__*/React.createElement("div", {
    ref: listRef,
    style: {
      flex: 1,
      overflow: 'auto',
      margin: 'var(--space-4) 0',
      paddingRight: 4
    }
  }, messages.map((m, i) => /*#__PURE__*/React.createElement(__ds_scope.ChatMessage, {
    key: i,
    role: m.role
  }, m.text))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 'var(--space-2)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Textarea, {
    rows: 2,
    placeholder: "Escribe tu pregunta o usa los botones r\xE1pidos...",
    value: draft,
    onChange: e => onDraftChange(e.target.value)
  }), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    variant: "primary",
    onClick: onSend
  }, "Enviar")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 'var(--space-4)'
    }
  }, /*#__PURE__*/React.createElement("h4", {
    style: {
      margin: '0 0 6px',
      color: 'var(--text-secondary)',
      fontFamily: 'var(--font-ui)',
      fontSize: 'var(--text-body-s)'
    }
  }, "System prompt"), /*#__PURE__*/React.createElement(__ds_scope.SystemPromptBox, {
    value: systemPrompt,
    onChange: onSystemPromptChange
  })));
}
Object.assign(__ds_scope, { ChatPanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/portfolio-agent/ChatPanel.jsx", error: String((e && e.message) || e) }); }

// ui_kits/portfolio-agent/LeftPanel.jsx
try { (() => {
const PRESETS = ['1 — Auditoría del repo', '2 — Plan 5 fases', '3 — Genera README', '4 — Casos de prueba', '5 — Prompt system'];
function LeftPanel({
  latency,
  onPreset
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-5)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Logomark, {
    assetsBase: "../../",
    size: 44
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      color: 'var(--text-secondary)',
      fontSize: 'var(--text-body)'
    }
  }, "Portfolio, protocolo 5 fases y agente en vivo integrado."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 'var(--space-3)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.MetricStat, {
    value: "Online",
    label: "Disponibilidad"
  }), /*#__PURE__*/React.createElement(__ds_scope.MetricStat, {
    value: "Claude",
    label: "Motor"
  }), /*#__PURE__*/React.createElement(__ds_scope.MetricStat, {
    value: latency,
    label: "Latencia"
  })), /*#__PURE__*/React.createElement(__ds_scope.Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: '0 0 8px',
      fontFamily: 'var(--font-display)',
      color: 'var(--accent-secondary)',
      fontSize: 'var(--text-display-s)'
    }
  }, "Capacidades"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      color: 'var(--text-secondary)',
      fontSize: 'var(--text-body-s)'
    }
  }, "Asistencia conversacional, planificaci\xF3n en 5 fases, generaci\xF3n de prompts, an\xE1lisis de casos de uso."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 'var(--space-2)',
      flexWrap: 'wrap',
      marginTop: 'var(--space-3)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Chip, null, "Interacci\xF3n multimodal"), /*#__PURE__*/React.createElement(__ds_scope.Chip, null, "Protocolos de seguridad"), /*#__PURE__*/React.createElement(__ds_scope.Chip, {
    tone: "gold"
  }, "Integraciones API"), /*#__PURE__*/React.createElement(__ds_scope.Chip, {
    tone: "gold"
  }, "Fichas de conocimiento"))), /*#__PURE__*/React.createElement(__ds_scope.Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: '0 0 8px',
      fontFamily: 'var(--font-display)',
      color: 'var(--accent-secondary)',
      fontSize: 'var(--text-display-s)'
    }
  }, "Protocolo 5 fases"), /*#__PURE__*/React.createElement("ol", {
    style: {
      margin: 0,
      paddingLeft: 18,
      color: 'var(--text-secondary)',
      fontSize: 'var(--text-body-s)',
      lineHeight: 'var(--lh-body)'
    }
  }, /*#__PURE__*/React.createElement("li", null, "Descubrir \u2014 definir objetivo y constraints"), /*#__PURE__*/React.createElement("li", null, "Planificar \u2014 pasos y recursos"), /*#__PURE__*/React.createElement("li", null, "Construir \u2014 generar artefactos"), /*#__PURE__*/React.createElement("li", null, "Validar \u2014 tests y revisiones"), /*#__PURE__*/React.createElement("li", null, "Desplegar \u2014 entregar y monitorizar"))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: '0 0 8px',
      fontFamily: 'var(--font-display)',
      color: 'var(--accent-secondary)',
      fontSize: 'var(--text-display-s)'
    }
  }, "Botones r\xE1pidos"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-2)'
    }
  }, PRESETS.map(p => /*#__PURE__*/React.createElement(__ds_scope.Button, {
    key: p,
    variant: "ghost",
    style: {
      textAlign: 'left',
      width: '100%'
    },
    onClick: () => onPreset(p)
  }, p)))));
}
Object.assign(__ds_scope, { LeftPanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/portfolio-agent/LeftPanel.jsx", error: String((e && e.message) || e) }); }

// ui_kits/portfolio-agent/PortfolioAgentApp.jsx
try { (() => {
const {
  useState
} = React;
const CANNED = {
  '1 — Auditoría del repo': 'He revisado la estructura del repositorio: documentación clara, pero faltan tests automatizados en los flujos críticos.',
  '2 — Plan 5 fases': 'Plan propuesto — Descubrir: objetivos y constraints. Planificar: recursos. Construir: artefactos. Validar: revisión. Desplegar: entrega.',
  '3 — Genera README': '# Proyecto\nDescripción breve, instalación, uso y contribución — listo para adaptar.',
  '4 — Casos de prueba': 'Casos sugeridos: entrada vacía, timeout de red, respuesta malformada, concurrencia de mensajes.',
  '5 — Prompt system': 'Eres un superagente que sigue el protocolo de 5 fases y confirma supuestos antes de actuar.'
};
function PortfolioAgentApp() {
  const [messages, setMessages] = useState([{
    role: 'agent',
    text: 'Bienvenido a Will — SuperAgente. Usa los botones rápidos o escribe tu pregunta.'
  }]);
  const [draft, setDraft] = useState('');
  const [systemPrompt, setSystemPrompt] = useState('Eres Will, un SuperAgente con protocolo de 5 fases: descubrir, planificar, construir, validar, desplegar. Actúa como asistente técnico y arquitecto de soluciones.');
  const [latency, setLatency] = useState('—ms');
  function reply(userText, preset) {
    setMessages(m => [...m, {
      role: 'user',
      text: userText
    }]);
    setTimeout(() => {
      setLatency(Math.round(180 + Math.random() * 220) + 'ms');
      const text = CANNED[preset] || 'Entendido. ¿Puedes darme más contexto sobre el objetivo y las constraints?';
      setMessages(m => [...m, {
        role: 'agent',
        text
      }]);
    }, 500);
  }
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '380px 1fr',
      gap: 'var(--space-6)',
      maxWidth: 1100,
      margin: '0 auto',
      padding: 'var(--space-8)',
      fontFamily: 'var(--font-ui)'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.LeftPanel, {
    latency: latency,
    onPreset: p => reply(p, p)
  }), /*#__PURE__*/React.createElement(__ds_scope.ChatPanel, {
    messages: messages,
    draft: draft,
    onDraftChange: setDraft,
    onSend: () => {
      if (draft.trim()) {
        reply(draft.trim());
        setDraft('');
      }
    },
    systemPrompt: systemPrompt,
    onSystemPromptChange: setSystemPrompt
  }));
}
Object.assign(__ds_scope, { PortfolioAgentApp });
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/portfolio-agent/PortfolioAgentApp.jsx", error: String((e && e.message) || e) }); }

__ds_ns.ChatMessage = __ds_scope.ChatMessage;

__ds_ns.SystemPromptBox = __ds_scope.SystemPromptBox;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Chip = __ds_scope.Chip;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Logomark = __ds_scope.Logomark;

__ds_ns.MetricStat = __ds_scope.MetricStat;

__ds_ns.Textarea = __ds_scope.Textarea;

__ds_ns.LabAtmosphere = __ds_scope.LabAtmosphere;

__ds_ns.LabMemory = __ds_scope.LabMemory;

__ds_ns.NODES = __ds_scope.NODES;

__ds_ns.ScrollReel = __ds_scope.ScrollReel;

__ds_ns.ChatPanel = __ds_scope.ChatPanel;

__ds_ns.LeftPanel = __ds_scope.LeftPanel;

__ds_ns.PortfolioAgentApp = __ds_scope.PortfolioAgentApp;

})();
