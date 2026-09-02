import { useEffect, useId, useRef, useState, type FormEvent } from "react";
import { createPortal } from "react-dom";
import { Copy, Share2, X } from "lucide-react";
import { SITE } from "@/lib/seo";
import {
  copyFromInput,
  copyText,
  isGatedHost,
  nativeShare,
  parsePublicShareInput,
  rememberPublicUrl,
} from "@/lib/public-url";

export function ShareSheet({
  url,
  onClose,
  onResolved,
}: {
  url: string | null;
  onClose: () => void;
  onResolved: (url: string) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const titleId = useId();
  const [copied, setCopied] = useState(false);
  const [paste, setPaste] = useState("");
  const [hint, setHint] = useState<string | null>(null);

  useEffect(() => {
    if (!url || !inputRef.current) return;
    const ok = copyFromInput(inputRef.current);
    setCopied(ok);
  }, [url]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.stopPropagation();
        onClose();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  function onCopyClick() {
    const ok = copyFromInput(inputRef.current);
    setCopied(ok);
    setHint(ok ? null : "Selecciona el enlace y pulsa Ctrl+C o ⌘C.");
  }

  function onSend() {
    if (!url) return;
    void nativeShare(url, SITE.title).then((ok) => {
      if (ok) return;
      const body = encodeURIComponent(`${SITE.title}\n${url}`);
      const subject = encodeURIComponent(SITE.title);
      window.location.href = `mailto:?subject=${subject}&body=${body}`;
    });
  }

  function onPasteSubmit(e: FormEvent) {
    e.preventDefault();
    const parsed = parsePublicShareInput(paste);
    if (parsed) {
      rememberPublicUrl(parsed);
      copyText(parsed);
      onResolved(parsed);
      setHint(null);
      return;
    }
    const host = paste.trim();
    if (host && isGatedHost(host)) {
      setHint("Eso es el visor de Grok, no el público. El que se abre en cualquier navegador acaba en .grok.me.");
      return;
    }
    setHint("Pega el enlace que acaba en .grok.me (el de Publicar cambios).");
  }

  const sheet = (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-navy-deep/80 px-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      data-share-sheet="1"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md rounded-2xl border border-navy-line bg-navy px-5 py-5 shadow-[0_20px_60px_#040b14]"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-3">
          <h2 id={titleId} className="font-display text-xl text-ivory">
            Enlace público
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex size-11 items-center justify-center rounded-full text-ivory-dim"
            aria-label="Cerrar"
          >
            <X className="size-4" />
          </button>
        </div>

        {url ? (
          <>
            <p className="mt-2 text-sm leading-relaxed text-ivory-dim">
              Este sí se abre en Chrome, Edge, Firefox, Arc, Comet o Neo. Sin cuenta de Grok.
            </p>
            <label className="sr-only" htmlFor="public-url">
              URL pública
            </label>
            <input
              id="public-url"
              ref={inputRef}
              readOnly
              value={url}
              onFocus={(e) => e.currentTarget.select()}
              className="mt-4 w-full rounded-lg border border-navy-line bg-navy-deep px-3 py-3 font-sans text-sm text-ivory"
            />
            <div className="mt-4 flex flex-wrap gap-2">
              <button
                type="button"
                onClick={onCopyClick}
                className="inline-flex min-h-11 items-center gap-2 rounded-full border border-holo/40 bg-navy-mid px-4 text-sm text-ivory"
              >
                <Copy className="size-3.5" />
                {copied ? "Copiado" : "Copiar"}
              </button>
              <button
                type="button"
                onClick={onSend}
                className="inline-flex min-h-11 items-center gap-2 rounded-full border border-navy-line px-4 text-sm text-ivory"
              >
                <Share2 className="size-3.5" />
                Enviar
              </button>
            </div>
            {hint ? <p className="mt-3 text-sm text-gold">{hint}</p> : null}
            {copied ? (
              <p className="mt-3 text-sm text-holo">En el portapapeles. Envíalo; no uses el copiar de la barra de Grok.</p>
            ) : null}
          </>
        ) : (
          <>
            <p className="mt-3 text-sm leading-relaxed text-ivory-dim">
              Este visor es temporal: si lo envías, Cloudflare lo tira o pide cuenta de Grok. El enlace del
              mundo acaba en <span className="text-holo">.grok.me</span>.
            </p>
            <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm leading-relaxed text-ivory-dim">
              <li>
                Pulsa <strong className="font-medium text-ivory">Publicar cambios</strong>.
              </li>
              <li>Copia el enlace que acaba en .grok.me (no el de esta conversación).</li>
              <li>Pégalo aquí. A partir de entonces «Enlace público» lo copiará solo.</li>
            </ol>
            <form className="mt-4" onSubmit={onPasteSubmit}>
              <label className="sr-only" htmlFor="paste-public-url">
                Pegar enlace .grok.me
              </label>
              <input
                id="paste-public-url"
                value={paste}
                onChange={(e) => setPaste(e.target.value)}
                placeholder="https://….grok.me/"
                autoComplete="off"
                spellCheck={false}
                className="w-full rounded-lg border border-navy-line bg-navy-deep px-3 py-3 font-sans text-sm text-ivory placeholder:text-ivory-mute"
              />
              <button
                type="submit"
                className="mt-3 inline-flex min-h-11 items-center rounded-full border border-holo/40 bg-navy-mid px-4 text-sm text-ivory"
              >
                Usar este enlace
              </button>
            </form>
            {hint ? <p className="mt-3 text-sm text-gold">{hint}</p> : null}
          </>
        )}
      </div>
    </div>
  );

  if (typeof document === "undefined") return sheet;
  return createPortal(sheet, document.body);
}
