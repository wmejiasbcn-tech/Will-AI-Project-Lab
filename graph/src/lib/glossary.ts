export type GlossaryEntry = {
  id: string;
  term: string;
  kicker: string;
  blurb: string;
};

export const GLOSSARY: GlossaryEntry[] = [
  {
    id: "portada",
    term: "Portada",
    kicker: "El umbral",
    blurb:
      "La primera imagen: el blasón flotando sobre la ciudad. No es un menú. Es la puerta. Desde aquí se entra al grafo vivo.",
  },
  {
    id: "graphy",
    term: "Mapa Graphy",
    kicker: "El territorio",
    blurb:
      "La proyección 3D del ecosistema. Cada esfera es una entidad; cada hilo, una relación. Se orbita con el dedo, se toca para leer.",
  },
  {
    id: "inmersivo",
    term: "Inmersivo",
    kicker: "Habitar, no consultar",
    blurb:
      "No es un dashboard con pestañas. Es un espacio: ciudad, cintas, nodos. Entras, orbitas, tocas. La información vive en el lugar.",
  },
  {
    id: "grafo",
    term: "Grafo vivo",
    kicker: "Red que respira",
    blurb:
      "Un mapa de nodos y vínculos que no está quieto. Los flujos pulsan, las cintas giran, un toque enciende vecinos.",
  },
  {
    id: "nodo",
    term: "Nodo",
    kicker: "Una entidad",
    blurb:
      "Una esfera en el mapa: un agente, un protocolo, un laboratorio, un documento. Al pasar el puntero sale su nombre; al tocar, su ficha.",
  },
  {
    id: "nucleo",
    term: "Núcleo",
    kicker: "Will-AI",
    blurb:
      "El centro gravitatorio. Alrededor orbitan laboratorios, agentes y protocolos. Tocar el núcleo es tocar el corazón del ecosistema.",
  },
  {
    id: "laboratorio",
    term: "Laboratorio",
    kicker: "Donde se fabrica",
    blurb:
      "Célula de prototipado. Aquí nacen mapas, protocolos y experiencias. No publica: itera, y devuelve al núcleo lo que ya puede orbitar.",
  },
  {
    id: "agente",
    term: "Agente",
    kicker: "Una voz del grafo",
    blurb:
      "Entidad que actúa: Carla, Ariana, Porticia. Conectan laboratorio con relato, umbral con núcleo.",
  },
  {
    id: "protocolo",
    term: "Protocolo",
    kicker: "Una regla viva",
    blurb:
      "Método que da forma a una idea antes de ser nodo. Identidad, pensamiento, custodia. Impide que el grafo se vuelva inventario.",
  },
  {
    id: "documento",
    term: "Documento",
    kicker: "Memoria escrita",
    blurb:
      "Manifiestos, versiones, archivos. Anclan lo que el mapa sugiere. Se leen en la ficha del nodo.",
  },
  {
    id: "comunidad",
    term: "Comunidad",
    kicker: "Un enclave",
    blurb:
      "Grupo de nodos que comparte relato: Identidad, Laboratorio, Narrativa. Filtrar por comunidad enseña un barrio del grafo.",
  },
  {
    id: "flujo",
    term: "Flujo",
    kicker: "La corriente",
    blurb:
      "Pulso que recorre las aristas. Cuando un nodo se toca, el flujo ilumina a sus vecinos. El análisis lo lee como serie; el mapa, como destello.",
  },
  {
    id: "accion",
    term: "Acción",
    kicker: "Un verbo",
    blurb:
      "Explorar, conectar, crear, analizar. Son gestos, no menús: cada uno abre un lugar distinto del territorio.",
  },
  {
    id: "explorador",
    term: "Explorador",
    kicker: "La consola",
    blurb:
      "Piel holográfica del sistema: inicio, mapas, análisis, ajustes. Pensado para manos y mirada.",
  },
  {
    id: "umbral",
    term: "Umbral",
    kicker: "Antes de entrar",
    blurb:
      "La portada. El blasón se custodia aquí. Los verbos —entrar, explorar, conectar— son invitaciones, no botones de un sitio web.",
  },
];

export const GLOSSARY_MAP: Record<string, GlossaryEntry> = Object.fromEntries(
  GLOSSARY.map((g) => [g.id, g]),
);

export const TYPE_HINT: Record<string, string> = {
  nucleo: "El centro. Toca para ver Will-AI.",
  laboratorio: "Donde se fabrica. Abre el taller.",
  agente: "Una voz del grafo. Carla, Ariana, Porticia.",
  protocolo: "Una regla viva.",
  documento: "Memoria escrita del ecosistema.",
  comunidad: "Un enclave de relato.",
  flujo: "La corriente entre nodos.",
  accion: "Un verbo: explorar, conectar, crear, analizar.",
};
