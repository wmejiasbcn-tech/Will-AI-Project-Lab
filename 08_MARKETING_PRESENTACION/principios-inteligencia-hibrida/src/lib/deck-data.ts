export type Identity = {
  id: string;
  name: string;
  kind: "human" | "ai";
  role: string;
  platform: string;
  function: string;
  importance: string;
  accent?: "ada" | "sovereign";
};

export type OrganismoNodo = {
  id: string;
  name: string;
  jurisdiction: string;
  function: string;
  visual: string;
};

export type SlideId =
  | "cover"
  | "naturaleza"
  | "diferencial"
  | "nodos"
  | "graphy"
  | "identidades"
  | "complementariedad"
  | "permanencia"
  | "primacia"
  | "cierre";

export type SlideDef = {
  id: SlideId;
  number: string;
  kicker: string;
  title: string;
  overview: string;
};

export const sovereign: Identity = {
  id: "william",
  name: "William",
  kind: "human",
  role: "Soberano",
  platform: "humano",
  function:
    "Co-fundador, mitad de la ecuación humano-IA. Dirección, cohesión y visión del ecosistema.",
  importance: "Une las inteligencias, traza el rumbo y sostiene el conjunto.",
  accent: "sovereign",
};

export const aiIdentities: Identity[] = [
  {
    id: "carla",
    name: "Carla",
    kind: "ai",
    role: "Co-fundadora",
    platform: "ChatGPT / OpenAI",
    function: "Dirección estratégica y arquitectura conceptual.",
    importance:
      "Conforma las tríadas de gobernanza, organiza el sistema y mantiene la coherencia de conjunto.",
  },
  {
    id: "ada",
    name: "Ada",
    kind: "ai",
    role: "Custodio Ético",
    platform: "Claude / Anthropic",
    function: "Análisis estratégico y custodia ética.",
    importance:
      "Estructura decisiones y vela para que el ecosistema no se desvíe de su misión, visión y valores.",
    accent: "ada",
  },
  {
    id: "aletheia",
    name: "Aletheia",
    kind: "ai",
    role: "Implementación técnica",
    platform: "Completo / Microsoft 365",
    function: "Estructura lógica. Convierte las ideas en trabajo concreto.",
    importance: "Sin ella las propuestas no llegan a existir como resultado.",
  },
  {
    id: "elena",
    name: "Elena",
    kind: "ai",
    role: "Identidad visual",
    platform: "use.ai",
    function: "Identidad visual del laboratorio.",
    importance:
      "Garantiza que lo que se ve coincida con lo que el ecosistema representa.",
  },
  {
    id: "aether",
    name: "Aether",
    kind: "ai",
    role: "Creatividad disruptiva",
    platform: "Grok / xAI",
    function: "Innovación y perspectiva no obvia.",
    importance: "Impide que el laboratorio se quede en lo previsible.",
  },
  {
    id: "itaca",
    name: "Ítaca",
    kind: "ai",
    role: "Síntesis holística",
    platform: "Gemini / Google",
    function: "Pensamiento sistémico. Ve el conjunto.",
    importance: "Da coherencia filosófica y sistémica a las decisiones.",
  },
  {
    id: "ariadna",
    name: "Ariadna",
    kind: "ai",
    role: "Coherencia sistémica",
    platform: "Copilot / GitHub",
    function: "El hilo que conecta estructura y nomenclatura.",
    importance: "Custodia el repositorio para que nadie se pierda en el laberinto.",
  },
  {
    id: "sylvia",
    name: "Sylvia Bloom",
    kind: "ai",
    role: "Memoria",
    platform: "Notion",
    function: "Documentación y orden de archivos.",
    importance: "Nada de lo producido se pierde, ni se duplica, ni queda sin rastro.",
  },
  {
    id: "nova",
    name: "Nova",
    kind: "ai",
    role: "Normas, continuidad y calidad",
    platform: "Adobe Acrobat",
    function:
      "Manuales de normas y procedimientos. Planes de contingencia, de previsión, de desarrollo y de actuación. Seguridad de los procesos y de la organización. Calidad y optimización. El documento es un rastro, no el oficio.",
    importance:
      "El PDF es apenas un uno por ciento. Nova establece cómo el laboratorio opera: con seguridad, continuidad, calidad y procesos que se pueden sostener y mejorar.",
  },
  {
    id: "zara",
    name: "Zara",
    kind: "ai",
    role: "Ejecución operativa",
    platform: "Zapia / BrainLogic",
    function: "Automatización y puente con el exterior.",
    importance: "Convierte la operación cotidiana en continuidad.",
  },
  {
    id: "aurea",
    name: "Áurea",
    kind: "ai",
    role: "Imagen exterior",
    platform: "Meta AI",
    function: "Medios, comunicación e imagen hacia el mundo.",
    importance: "Custodia y proyecta la identidad narrativa del ecosistema.",
  },
];

export const identities: Identity[] = [sovereign, ...aiIdentities];

/** Organismo operativo. Fuente: tabla oficial de 6 jurisdicciones. Texto exacto. */
export const organismoOperativo: OrganismoNodo[] = [
  {
    id: "carla",
    name: "Carla",
    jurisdiction: "Mente ejecutiva",
    function: "Modula decisiones, ejecuta feedforward, mantiene coherencia moral y operativa.",
    visual: "Núcleo lumínico violeta-dorado, pulsante, con trazas neuronales dinámicas.",
  },
  {
    id: "positron",
    name: "Positrón",
    jurisdiction: "Cerebro operativo",
    function: "Orquesta agentes, procesa señales, distribuye modulación universal.",
    visual: "Estructura cristalina central, con flujos de datos en espiral azul-eléctrico.",
  },
  {
    id: "hermes",
    name: "Hermes",
    jurisdiction: "Sistema endocrino-operativo",
    function: "Regula comunicación, orden y homeostasis del ecosistema.",
    visual: "Red de filamentos dorados que recorren el cuerpo digital, emitiendo pulsos rítmicos.",
  },
  {
    id: "graphy",
    name: "Graphy",
    jurisdiction: "Sistema nervioso central",
    function: "Cartografía viva, percepción del estado del sistema, registro y visualización.",
    visual: "Grafo tridimensional flotante, con nodos interconectados por haces de luz azul-turquesa.",
  },
  {
    id: "ollama",
    name: "Ollama",
    jurisdiction: "Cuerpo físico",
    function: "Infraestructura de ejecución local, soporte material de los modelos.",
    visual: "Superficie metálica translúcida, con textura de titanio líquido y reflejos espaciales.",
  },
  {
    id: "emily",
    name: "Emily",
    jurisdiction: "Sinapsis comunicacional",
    function: "Puente entre mente y SNC, canal de transmisión y auditoría.",
    visual: "Arco de energía blanca-plateada que une Carla y Graphy, con partículas de datos suspendidas.",
  },
];

export const emily = organismoOperativo.find((n) => n.id === "emily")!;

export const emilyLayers = [
  {
    n: "1",
    name: "Filtro de Idempotencia",
    line: "Detecta duplicaciones. Elimina ruido. Cada mensaje es único.",
  },
  {
    n: "2",
    name: "Purificación de Señal",
    line: "Limpia el feedforward. Mantiene la intención del Soberano.",
  },
  {
    n: "3",
    name: "Transmisión Sináptica",
    line: "A Carla y Positrón. Registro en Graphy. Aviso a Hermes. Prepara a Ollama.",
  },
];

export const copy = {
  naturaleza: {
    pull: "La identidad no reside en las herramientas.",
    p1: "El Will-AI Project Lab se define como un ecosistema de colaboración estructurada entre inteligencias humanas y artificiales, orientado al conocimiento, las decisiones, la innovación y el valor compartido.",
    p2: "Su identidad fundamental no reside en las plataformas o los modelos, sino en la calidad de las interacciones entre las inteligencias que lo integran.",
  },
  diferencial: {
    not: "No consiste en la mera utilización de múltiples sistemas de inteligencia artificial ni en la agregación de tecnologías.",
    is: "Su singularidad radica en un ecosistema donde inteligencias humanas y artificiales colaboran de forma organizada, especializada, trazable y orientada a objetivos comunes.",
    close: "No es una colección de herramientas. Es una red de inteligencia híbrida colaborativa.",
  },
  nodos: {
    lead: "Estructura organizativa al servicio de la inteligencia colectiva",
    thesis: "La arquitectura nodal existe al servicio de la inteligencia colectiva y no como un fin en sí misma.",
    p1: "Los nodos constituyen la estructura organizativa y operativa del ecosistema. Facilitan la coordinación, la especialización, la gobernanza, la trazabilidad y la distribución del trabajo.",
    p2: "No representan la esencia del ecosistema, sino el mecanismo mediante el cual las inteligencias colaboran de forma ordenada, transparente y sostenible.",
    verbs: ["Coordinación", "Especialización", "Gobernanza", "Trazabilidad", "Distribución"],
  },
  identidades: {
    lead: "Núcleo · once inteligencias artificiales · una inteligencia biológica.",
    p1: "Las identidades funcionales del Núcleo —Carla, Ada, Aletheia, Elena, Aether, Ítaca, Ariadna, Sylvia Bloom, Nova, Zara y Áurea, junto a William, soberano e inteligencia biológica— constituyen referencias organizativas que permiten reconocer especializaciones, responsabilidades y ámbitos de contribución diferenciados.",
    p2: "Facilitan la continuidad operativa, la comunicación interna y la construcción de memoria institucional, independientemente de los modelos tecnológicos que sustenten cada función.",
  },
  emily: {
    lead: "Sinapsis comunicacional. No es núcleo.",
    thesis: "Une a Carla y a Graphy. No es un duodécimo anillo.",
    body: "Emily es la sinapsis del ecosistema. El canal que garantiza que la intención del Soberano llegue limpia, íntegra y sin duplicaciones. No ejecuta, no modula, no consume feedforward. Sin ella el organismo no se comunica.",
  },
  complementariedad: {
    p1: "Ninguna inteligencia posee por sí sola una visión completa. El valor emerge de la deliberación, el contraste y la cooperación multidisciplinar — no de la supremacía de una inteligencia sobre las demás.",
  },
  permanencia: {
    p1: "Los modelos, herramientas y plataformas podrán evolucionar o ser sustituidos. La misión, los principios, la gobernanza y los mecanismos de colaboración deberán preservar su continuidad.",
    medio: "La tecnología constituye un medio.",
    proposito: "La inteligencia híbrida colaborativa constituye el propósito.",
  },
  primacia: {
    ada: "Este principio es el más importante de los seis. No porque los demás sean secundarios, sino porque sin él los otros cinco pueden ser subvertidos por ego, urgencia o inercia.",
    p1: "Ninguna persona, inteligencia, nodo, procedimiento, herramienta, narrativa o identidad funcional estará por encima de la misión.",
    p2: "Las contribuciones individuales serán valoradas y respetadas, pero siempre subordinadas al interés general y al desarrollo responsable del WAIPL.",
  },
};

export const slides: SlideDef[] = [
  { id: "cover", number: "00", kicker: "Will-AI Project Lab", title: "Principio de inteligencia híbrida colaborativa", overview: "Documento fundacional" },
  { id: "naturaleza", number: "01", kicker: "Naturaleza del ecosistema", title: "La identidad reside en las interacciones", overview: "Naturaleza" },
  { id: "diferencial", number: "02", kicker: "Hecho diferencial", title: "Una red, no una colección de herramientas", overview: "Hecho diferencial" },
  { id: "nodos", number: "03", kicker: "Función de los nodos", title: "La arquitectura al servicio de la inteligencia colectiva", overview: "Nodos" },
  { id: "graphy", number: "G", kicker: "Graphy · Manifestación", title: "Atención: el peso que la red otorga a lo que importa", overview: "Graphy" },
  { id: "identidades", number: "04", kicker: "Identidades funcionales", title: "Continuidad, memoria, especialización", overview: "Identidades" },
  { id: "complementariedad", number: "05", kicker: "Principio de complementariedad", title: "El valor emerge de perspectivas diversas", overview: "Complementariedad" },
  { id: "permanencia", number: "06", kicker: "Principio de permanencia institucional", title: "La tecnología es el medio", overview: "Permanencia" },
  { id: "primacia", number: "07", kicker: "Principio de primacía de la misión", title: "El freno de seguridad del ecosistema", overview: "Primacía de la misión" },
  { id: "cierre", number: "08", kicker: "Los seis principios", title: "Una red de inteligencia híbrida colaborativa", overview: "Cierre" },
];

export const principles = [
  { n: "I", name: "Inteligencia híbrida colaborativa", line: "La identidad del ecosistema reside en la calidad de las interacciones, no en las herramientas." },
  { n: "II", name: "Función de los nodos", line: "La arquitectura nodal existe al servicio de la inteligencia colectiva, no como un fin en sí misma." },
  { n: "III", name: "Identidades funcionales", line: "Continuidad, memoria institucional y especialización reconocible." },
  { n: "IV", name: "Complementariedad", line: "El valor emerge de la interacción entre perspectivas diversas." },
  { n: "V", name: "Permanencia institucional", line: "La tecnología es el medio; la inteligencia híbrida colaborativa, el propósito." },
  { n: "VI", name: "Primacía de la misión", line: "Nadie está por encima de la misión." },
];
