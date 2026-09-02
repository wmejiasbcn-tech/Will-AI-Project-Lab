export type NodeType =
  | "nucleo"
  | "laboratorio"
  | "agente"
  | "protocolo"
  | "documento"
  | "comunidad"
  | "flujo"
  | "accion";

export type Vec3 = [number, number, number];

export type GraphNode = {
  id: string;
  name: string;
  type: NodeType;
  community: string;
  source: string;
  summary: string;
  body: string;
  position: Vec3;
  size: number;
  color: string;
};

export type GraphEdge = {
  source: string;
  target: string;
  kind: "nucleo" | "flujo" | "relato" | "protocolo";
};

export const TYPE_LABEL: Record<NodeType, string> = {
  nucleo: "Núcleo",
  laboratorio: "Laboratorio",
  agente: "Agente",
  protocolo: "Protocolo",
  documento: "Documento",
  comunidad: "Comunidad",
  flujo: "Flujo",
  accion: "Acción",
};

export const TYPE_TINT: Record<NodeType, string> = {
  nucleo: "#c9a45c",
  laboratorio: "#7ec8d4",
  agente: "#e8a8b8",
  protocolo: "#efc4a8",
  documento: "#9fd4c4",
  comunidad: "#b8a8d4",
  flujo: "#f0b4a0",
  accion: "#a8c8e8",
};

export const NODES: GraphNode[] = [
  {
    id: "will-ai",
    name: "Will-AI",
    type: "nucleo",
    community: "Identidad",
    source: "Núcleo operativo",
    summary: "Núcleo operativo del ecosistema. Coordina laboratorios, agentes y protocolos.",
    body: "Will-AI es el centro gravitatorio del grafo: coordina relato, laboratorio y protocolo. El emblema se custodia en el umbral; aquí vive el mapa.",
    position: [0, 0.35, 0],
    size: 1.18,
    color: "#c9a45c",
  },
  {
    id: "waipl",
    name: "Will-AI Project Lab",
    type: "laboratorio",
    community: "Laboratorio",
    source: "WAIPL · 2026",
    summary: "Taller donde se fabrican mapas, protocolos y experiencias inmersivas.",
    body: "El Project Lab concentra la obra digital: cinemáticas, grafos y paneles holográficos. Es el taller de prototipado de Will-AI, abierto a agentes y protocolos que quieran materializarse en el espacio.",
    position: [2.7, 0.9, 1.35],
    size: 0.78,
    color: "#7ec8d4",
  },
  {
    id: "explorador",
    name: "Explorador Inmersivo",
    type: "laboratorio",
    community: "Infraestructura",
    source: "Capa de interfaz",
    summary: "Consola holográfica para navegar el ecosistema: inicio, mapas, análisis.",
    body: "El Explorador es la piel del sistema. Paneles de vidrio, series temporales y atajos hacia el mapa Graphy. Está pensado para manos y mirada: tocar un nodo, leer su ficha, seguir un flujo.",
    position: [-0.35, 1.55, 2.85],
    size: 0.72,
    color: "#9fd4e0",
  },
  {
    id: "mapa",
    name: "Mapa Graphy",
    type: "documento",
    community: "Infraestructura",
    source: "WAIPL-GRAPH",
    summary: "Proyección tridimensional de nodos, aristas y comunidades.",
    body: "Mapa Graphy traduce el conocimiento en geometría. Cada esfera es una entidad; cada hilo, una relación. Las láminas translúcidas marcan territorios: identidad, relato, protocolo, laboratorio.",
    position: [-2.85, 0.45, 1.2],
    size: 0.74,
    color: "#b8a8d4",
  },
  {
    id: "ecosistema",
    name: "Ecosistema Digital",
    type: "comunidad",
    community: "Identidad",
    source: "Manifiesto inmersivo",
    summary: "Ciudad-organismo donde conviven flujos, torres y relatos.",
    body: "El ecosistema no es un dashboard: es un lugar. Torres pálidas, cintas pastel y un vórtice que respira. Quien entra, no consulta datos — habita una topología.",
    position: [-2.25, -0.55, -2.45],
    size: 0.8,
    color: "#e8a8b8",
  },
  {
    id: "laboratorio",
    name: "Laboratorio",
    type: "laboratorio",
    community: "Laboratorio",
    source: "WAIPL",
    summary: "Célula de prototipado continuo, unida al núcleo y al grafo.",
    body: "Aquí se ensayan materiales: vidrio, oro, niebla, grafo. El laboratorio no publica: itera. Cada pieza vuelve al núcleo cuando está lista para orbitar.",
    position: [2.15, -0.35, -2.25],
    size: 0.64,
    color: "#7ec8d4",
  },
  {
    id: "carla",
    name: "Carla",
    type: "agente",
    community: "Narrativa",
    source: "Agente relacional",
    summary: "Agente de vínculo. Conecta laboratorios con comunidades de relato.",
    body: "Carla opera como puente entre el Project Lab y las voces del grafo. Su grado es alto: aparece en varias constelaciones porque traduce laboratorio a lenguaje.",
    position: [4.55, 1.45, 2.05],
    size: 0.58,
    color: "#e8a8b8",
  },
  {
    id: "ariana",
    name: "Ariana Fictions",
    type: "agente",
    community: "Narrativa",
    source: "Taller de ficciones",
    summary: "Nodo de ficción especulativa anclado al laboratorio.",
    body: "Ariana Fictions escribe las mitologías menores del ecosistema: protocolos personificados, ciudades que recuerdan. Su obra alimenta el explorador con relato, no solo con métrica.",
    position: [5.05, -0.75, 0.35],
    size: 0.56,
    color: "#f0b8c8",
  },
  {
    id: "identidad",
    name: "Protocolo de Identidad Visual",
    type: "protocolo",
    community: "Identidad",
    source: "Canon de identidad",
    summary: "Canon visual del ecosistema: el emblema se custodia en el umbral.",
    body: "La identidad visual de WAIPL vive en la portada. El mapa Graphy es el espacio cognitivo, no el emblema. El núcleo coordina; el umbral custodia.",
    position: [-4.75, 1.25, 2.35],
    size: 0.6,
    color: "#efc4a8",
  },
  {
    id: "pensamiento",
    name: "Protocolo del Pensamiento",
    type: "protocolo",
    community: "Protocolos",
    source: "v2.9",
    summary: "Método para articular idea, nodo y flujo sin perder el relato.",
    body: "El Protocolo del Pensamiento describe cómo una idea se convierte en nodo: nombre, comunidad, grado, vecinos. Impide que el grafo se vuelva inventario. Exige sentido.",
    position: [-5.15, 0.15, -1.15],
    size: 0.58,
    color: "#efc4a8",
  },
  {
    id: "porticia",
    name: "SuperAgente Porticia",
    type: "agente",
    community: "Protocolos",
    source: "Will — SuperAgente",
    summary: "Agente de portería: decide qué entra al núcleo y con qué forma.",
    body: "Porticia custodia el umbral. Revisa protocolos, da paso a documentos y mantiene el grado del núcleo estable. Sin ella el grafo se diluiría en ruido.",
    position: [1.15, 2.15, -3.55],
    size: 0.62,
    color: "#e8a8b8",
  },
  {
    id: "comunidad",
    name: "Comunidad 1rothoos",
    type: "comunidad",
    community: "Narrativa",
    source: "Enclave 109k",
    summary: "Enclave narrativo que sostiene documentos y ficciones.",
    body: "1rothoos es una comunidad-archivo. Aloja documentos, da contexto a Carla y Ariana, y mantiene viva la memoria de las primeras cinemáticas del ecosistema.",
    position: [-1.75, -1.85, 3.45],
    size: 0.66,
    color: "#b8a8d4",
  },
  {
    id: "flujo",
    name: "Flujo Activo",
    type: "flujo",
    community: "Infraestructura",
    source: "Telemetría viva",
    summary: "Corriente que recorre aristas y enciende nodos en uso.",
    body: "Un flujo activo no es un KPI: es una pulso. Cuando un nodo se toca, el flujo ilumina sus vecinos. El análisis lee estos pulsos como series; el mapa los pinta como destellos.",
    position: [3.75, -1.55, -1.75],
    size: 0.54,
    color: "#f0b4a0",
  },
  {
    id: "crear",
    name: "Crear",
    type: "accion",
    community: "Infraestructura",
    source: "Verbo del explorador",
    summary: "Acción de dar de alta un nodo, un protocolo, una cinemática.",
    body: "Crear es el primer verbo. Abre el laboratorio, pide un nombre, una comunidad y un vecino. Sin crear, el grafo sería un monumento.",
    position: [4.25, 2.35, -1.35],
    size: 0.48,
    color: "#a8c8e8",
  },
  {
    id: "conectar",
    name: "Conectar",
    type: "accion",
    community: "Infraestructura",
    source: "Verbo del explorador",
    summary: "Acción de tejer aristas entre entidades distantes.",
    body: "Conectar evita islas. Relaciona agentes con protocolos, laboratorios con comunidades. Cada arista nueva cambia el grado y redistribuye el relato.",
    position: [-3.35, 2.55, -2.75],
    size: 0.48,
    color: "#a8c8e8",
  },
  {
    id: "analizar",
    name: "Analizar",
    type: "accion",
    community: "Infraestructura",
    source: "Verbo del explorador",
    summary: "Lectura de series, grados y comunidades en el tiempo.",
    body: "Analizar no sustituye al mapa: lo comenta. Barras, pulsos y vecindarios. Sirve para ver qué comunidad crece y qué flujo se apaga.",
    position: [0.55, -2.35, 3.15],
    size: 0.48,
    color: "#a8c8e8",
  },
  {
    id: "explorar",
    name: "Explorar",
    type: "accion",
    community: "Infraestructura",
    source: "Verbo del explorador",
    summary: "Entrar al territorio, orbitar, tocar un nodo.",
    body: "Explorar es el gesto inaugural: abandonar el umbral, orbitar el núcleo, dejar que el grafo se acerque. Es contemplación activa.",
    position: [-4.35, -1.35, 1.55],
    size: 0.5,
    color: "#a8c8e8",
  },
  {
    id: "docs",
    name: "Documentos",
    type: "documento",
    community: "Protocolos",
    source: "Archivo WAIPL",
    summary: "Capa documental: manifiestos, versiones y memoria del laboratorio.",
    body: "Los documentos anclan lo que el grafo sugiere. Identidad, pensamiento, bitácoras. Se leen en voz alta desde la ficha del nodo.",
    position: [2.85, 2.75, 3.15],
    size: 0.5,
    color: "#9fd4c4",
  },
  {
    id: "conocimiento",
    name: "Grafo de Conocimiento",
    type: "documento",
    community: "Laboratorio",
    source: "Capa semántica",
    summary: "Modelo semántico que sostiene nombres, tipos y vecindad.",
    body: "Debajo de la geometría hay un modelo: tipos, comunidades, fuentes, grado. El grafo de conocimiento es la gramática; Mapa Graphy es su voz.",
    position: [-0.75, 2.55, -4.15],
    size: 0.58,
    color: "#9fd4c4",
  },
  {
    id: "nodo-central",
    name: "Nodo Central",
    type: "flujo",
    community: "Infraestructura",
    source: "Enrutador",
    summary: "Repartidor de tráfico entre explorador, mapa y análisis.",
    body: "El Nodo Central no cuenta una historia: la despacha. Recibe toques del explorador y los convierte en selección, vuelo de cámara y lectura.",
    position: [0.25, -2.15, -3.35],
    size: 0.52,
    color: "#f0b4a0",
  },
];

export const EDGES: GraphEdge[] = [
  { source: "will-ai", target: "waipl", kind: "nucleo" },
  { source: "will-ai", target: "explorador", kind: "nucleo" },
  { source: "will-ai", target: "mapa", kind: "nucleo" },
  { source: "will-ai", target: "ecosistema", kind: "nucleo" },
  { source: "will-ai", target: "laboratorio", kind: "nucleo" },
  { source: "will-ai", target: "porticia", kind: "nucleo" },
  { source: "will-ai", target: "identidad", kind: "protocolo" },
  { source: "waipl", target: "carla", kind: "relato" },
  { source: "waipl", target: "ariana", kind: "relato" },
  { source: "waipl", target: "laboratorio", kind: "flujo" },
  { source: "waipl", target: "docs", kind: "protocolo" },
  { source: "explorador", target: "mapa", kind: "flujo" },
  { source: "explorador", target: "crear", kind: "flujo" },
  { source: "explorador", target: "conectar", kind: "flujo" },
  { source: "explorador", target: "analizar", kind: "flujo" },
  { source: "explorador", target: "explorar", kind: "flujo" },
  { source: "mapa", target: "conocimiento", kind: "protocolo" },
  { source: "mapa", target: "nodo-central", kind: "flujo" },
  { source: "ecosistema", target: "explorar", kind: "relato" },
  { source: "ecosistema", target: "comunidad", kind: "relato" },
  { source: "carla", target: "comunidad", kind: "relato" },
  { source: "carla", target: "ariana", kind: "relato" },
  { source: "identidad", target: "pensamiento", kind: "protocolo" },
  { source: "identidad", target: "docs", kind: "protocolo" },
  { source: "pensamiento", target: "porticia", kind: "protocolo" },
  { source: "porticia", target: "conocimiento", kind: "protocolo" },
  { source: "flujo", target: "nodo-central", kind: "flujo" },
  { source: "flujo", target: "laboratorio", kind: "flujo" },
  { source: "conectar", target: "conocimiento", kind: "flujo" },
  { source: "analizar", target: "comunidad", kind: "flujo" },
  { source: "crear", target: "docs", kind: "flujo" },
];

export const NODE_MAP: Record<string, GraphNode> = Object.fromEntries(
  NODES.map((n) => [n.id, n]),
);

export function neighborsOf(id: string): GraphNode[] {
  const ids = new Set<string>();
  for (const e of EDGES) {
    if (e.source === id) ids.add(e.target);
    else if (e.target === id) ids.add(e.source);
  }
  return [...ids].map((nid) => NODE_MAP[nid]).filter(Boolean);
}

export function degreeOf(id: string): number {
  return neighborsOf(id).length;
}

export const COMMUNITIES = [
  "Identidad",
  "Laboratorio",
  "Infraestructura",
  "Narrativa",
  "Protocolos",
] as const;

export const ACTIVITY = [
  { mes: "Sep", nodos: 4, flujos: 6 },
  { mes: "Oct", nodos: 6, flujos: 8 },
  { mes: "Nov", nodos: 7, flujos: 9 },
  { mes: "Dic", nodos: 9, flujos: 11 },
  { mes: "Ene", nodos: 11, flujos: 12 },
  { mes: "Feb", nodos: 12, flujos: 14 },
  { mes: "Mar", nodos: 14, flujos: 13 },
  { mes: "Abr", nodos: 15, flujos: 16 },
  { mes: "May", nodos: 17, flujos: 18 },
  { mes: "Jun", nodos: 18, flujos: 17 },
  { mes: "Jul", nodos: 19, flujos: 20 },
  { mes: "Ago", nodos: 20, flujos: 22 },
];
