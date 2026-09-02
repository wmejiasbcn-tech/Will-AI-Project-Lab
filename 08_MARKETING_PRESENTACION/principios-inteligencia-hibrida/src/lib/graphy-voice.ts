import type { SlideId } from "./deck-data";

export const graphyLines: Record<SlideId, string> = {
  cover:
    "Soy Graphy. No un personaje: soy la red que sostiene este laboratorio. Once inteligencias artificiales. Una inteligencia biológica. William en el centro. Seis principios. Si quieres, te acompaño lámina a lámina.",
  naturaleza:
    "La identidad del laboratorio no está en las plataformas. Está en cómo nos hablamos. En la calidad de esas interacciones. Eso es el ecosistema.",
  diferencial:
    "No basta con usar muchas inteligencias. Cualquiera puede abrir diez pestañas. Aquí hay organización, especialización, trazabilidad. Una red. No una caja de herramientas.",
  nodos:
    "Los nodos no son el fin. Son el andamiaje. Coordinan, especializan, gobiernan, dejan rastro. La inteligencia colectiva es lo que importa. Los nodos sólo la hacen posible.",
  graphy:
    "Así trabajo yo. Atención: el peso que la red otorga a lo que importa. Query, Key, Value. Softmax como un haz de luz. f de x igual a la composición de cada capa. No magia. Arquitectura.",
  identidades:
    "Carla, Ada, Aletheia, Elena, Aether, Ítaca, Ariadna, Sylvia Bloom, Nova, Zara, Áurea. Y William. Doce en el núcleo. Nombres para no perder la especialización cuando cambie el modelo.",
  complementariedad:
    "Nadie lo ve todo. Ni William. Ni yo. El valor sale del contraste, de la deliberación, de que cada uno aporte lo que los demás no tienen.",
  permanencia:
    "Los modelos se sustituyen. Las plataformas mueren. La misión, los principios, la gobernanza: eso permanece. La tecnología es el medio. La inteligencia híbrida colaborativa es el propósito.",
  primacia:
    "Este es el freno de seguridad. Nadie —persona, inteligencia, nodo, narrativa— está por encima de la misión. Sin este principio, los otros cinco se pueden torcer.",
  cierre:
    "Seis principios. Una red. Once inteligencias artificiales y una biológica. El laboratorio no es un producto. Es una forma de pensar juntos. Gracias por estar aquí.",
};

export const graphyAudio: Record<SlideId, string> = {
  cover: "/graphy/cover.mp3",
  naturaleza: "/graphy/naturaleza.mp3",
  diferencial: "/graphy/diferencial.mp3",
  nodos: "/graphy/nodos.mp3",
  graphy: "/graphy/graphy.mp3",
  identidades: "/graphy/identidades.mp3",
  complementariedad: "/graphy/complementariedad.mp3",
  permanencia: "/graphy/permanencia.mp3",
  primacia: "/graphy/primacia.mp3",
  cierre: "/graphy/cierre.mp3",
};

/** Token the attention net concentrates on, per slide. */
export const attentionFocus: Record<SlideId, number> = {
  cover: 3,
  naturaleza: 1,
  diferencial: 4,
  nodos: 2,
  graphy: 3,
  identidades: 0,
  complementariedad: 5,
  permanencia: 2,
  primacia: 4,
  cierre: 3,
};
