import { crawlerSections } from "@/lib/seo";
import { identities, principles } from "@/lib/deck-data";

export function SeoCorpus() {
  return (
    <div className="sr-only">
      <p>
        Will-AI Project Lab. Principio de inteligencia híbrida colaborativa. Once inteligencias
        artificiales y una inteligencia biológica. Graphy es la red.
      </p>
      {crawlerSections().map((s) => (
        <section key={s.h}>
          <h2>{s.h}</h2>
          <p>{s.t}</p>
        </section>
      ))}
      <h2>Núcleo</h2>
      <ul>
        {identities.map((n) => (
          <li key={n.id}>
            {n.name}, {n.role}, {n.platform}. {n.function} {n.importance}
          </li>
        ))}
      </ul>
      <h2>Seis principios</h2>
      <ol>
        {principles.map((p) => (
          <li key={p.n}>
            {p.n}. {p.name}. {p.line}
          </li>
        ))}
      </ol>
    </div>
  );
}
