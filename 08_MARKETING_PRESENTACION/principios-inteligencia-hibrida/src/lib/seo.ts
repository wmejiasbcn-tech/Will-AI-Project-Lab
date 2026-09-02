export const SITE = {
  title: "Principio de inteligencia híbrida colaborativa · WAIPL",
  description:
    "Seis principios de inteligencia híbrida colaborativa del Will-AI Project Lab: once inteligencias artificiales y una inteligencia biológica, en red.",
};

export const SITE_DESCRIPTION_LONG =
  "Documento fundacional del Will-AI Project Lab (WAIPL). El ecosistema se define por la calidad de las interacciones entre inteligencias humanas y artificiales, no por las plataformas. Once inteligencias artificiales y una inteligencia biológica forman el núcleo. Graphy es la red.";

export function jsonLd(canonical?: string) {
  const url = canonical || undefined;
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": "#waipl",
        name: "Will-AI Project Lab",
        alternateName: "WAIPL",
        description: SITE.description,
      },
      {
        "@type": "Person",
        "@id": "#william",
        name: "William Mejías Navarro",
        jobTitle: "Soberano",
        affiliation: { "@id": "#waipl" },
      },
      {
        "@type": "WebPage",
        "@id": "#page",
        name: SITE.title,
        description: SITE.description,
        inLanguage: "es-ES",
        isPartOf: { "@id": "#waipl" },
        ...(url ? { url } : {}),
      },
      {
        "@type": "Article",
        "@id": "#article",
        headline: SITE.title,
        description: SITE.description,
        inLanguage: "es-ES",
        datePublished: "2026-06-01",
        dateModified: "2026-09-02",
        wordCount: 860,
        author: { "@id": "#william" },
        publisher: { "@id": "#waipl" },
        mainEntityOfPage: { "@id": "#page" },
        about: [
          "inteligencia híbrida colaborativa",
          "Will-AI Project Lab",
          "nodos",
          "Graphy",
        ],
        articleSection: [
          "Naturaleza del ecosistema",
          "Hecho diferencial",
          "Función de los nodos",
          "Identidades funcionales",
          "Complementariedad",
          "Permanencia institucional",
          "Primacía de la misión",
        ],
      },
    ],
  };
}

export function crawlerSections() {
  return [
    {
      h: "Naturaleza del ecosistema",
      t: "El Will-AI Project Lab se define como un ecosistema de colaboración estructurada entre inteligencias humanas y artificiales. Su identidad no reside en las plataformas o los modelos, sino en la calidad de las interacciones.",
    },
    {
      h: "Hecho diferencial",
      t: "No consiste en la mera utilización de múltiples sistemas de inteligencia artificial. Es una red donde inteligencias humanas y artificiales colaboran de forma organizada, especializada, trazable y orientada a objetivos comunes.",
    },
    {
      h: "Función de los nodos",
      t: "Los nodos constituyen la estructura organizativa y operativa. Facilitan la coordinación, la especialización, la gobernanza, la trazabilidad y la distribución del trabajo. Existen al servicio de la inteligencia colectiva.",
    },
    {
      h: "Graphy",
      t: "Graphy es la manifestación de la red: atención, el peso que se otorga a lo que importa. f(x) = f_L ∘ … ∘ f_1(x).",
    },
    {
      h: "Identidades funcionales",
      t: "Núcleo: Carla, Ada, Aletheia, Elena, Aether, Ítaca, Ariadna, Sylvia Bloom, Nova, Zara y Áurea, junto a William, soberano e inteligencia biológica.",
    },
    {
      h: "Complementariedad",
      t: "Ninguna inteligencia posee por sí sola una visión completa. El valor emerge de la deliberación, el contraste y la cooperación multidisciplinar.",
    },
    {
      h: "Permanencia institucional",
      t: "Los modelos podrán evolucionar o ser sustituidos. La misión, los principios, la gobernanza y los mecanismos de colaboración deberán preservar su continuidad. La tecnología es el medio; la inteligencia híbrida colaborativa, el propósito.",
    },
    {
      h: "Primacía de la misión",
      t: "Ninguna persona, inteligencia, nodo, procedimiento, herramienta, narrativa o identidad funcional estará por encima de la misión.",
    },
  ];
}
