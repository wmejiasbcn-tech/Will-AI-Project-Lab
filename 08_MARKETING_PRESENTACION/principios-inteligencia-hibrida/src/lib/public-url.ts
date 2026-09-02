const STORE_KEY = "waipl:public-url";

function cleanHost(raw: string): string {
  return String(raw ?? "")
    .replace(/^https?:\/\//i, "")
    .split("/")[0]
    .split(":")[0]
    .trim()
    .toLowerCase();
}

function isPublicGrokMe(host: string): boolean {
  if (!host.endsWith(".grok.me")) return false;
  if (host === "grok.me" || host === "www.grok.me") return false;
  if (host === "gate.grok.me" || host === "auth.grok.me" || host === "og.grok.me") {
    return false;
  }
  if (host.endsWith(".auth.grok.me")) return false;
  return /^[a-z0-9-]+(?:\.[a-z0-9-]+)*\.grok\.me$/.test(host);
}

export function isTunnelHost(hostRaw: string): boolean {
  const host = cleanHost(hostRaw);
  if (!host) return false;
  if (host.startsWith("hds-")) return true;
  if (/(^|\.)hds-[a-z0-9-]+/.test(host)) return true;
  if (host.endsWith(".trycloudflare.com")) return true;
  if (host.endsWith(".grok-sandbox.com") || host === "grok-sandbox.com") return true;
  if (host.includes(".preview.")) return true;
  return false;
}

export function isGatedHost(hostRaw: string): boolean {
  const host = cleanHost(hostRaw);
  return (
    host === "grok.com" ||
    host.endsWith(".grok.com") ||
    host.endsWith(".vercel.app") ||
    host === "vercel.app" ||
    isTunnelHost(host)
  );
}

function urlFromHost(host: string): string | null {
  if (!host || isTunnelHost(host) || isGatedHost(host)) return null;
  if (isPublicGrokMe(host)) return `https://${host}/`;
  return null;
}

function hostFromMaybeUrl(raw: string): string {
  const s = String(raw ?? "").trim();
  if (!s) return "";
  try {
    if (s.includes("://")) return cleanHost(new URL(s).hostname);
  } catch {
    /* fall through */
  }
  return cleanHost(s);
}

/** Accept only a real `*.grok.me` public app host. Never invent a slug. */
export function parsePublicShareInput(raw: string): string | null {
  const s = String(raw ?? "").trim();
  if (!s) return null;
  const host = hostFromMaybeUrl(s);
  return urlFromHost(host);
}

function fromStore(): string | null {
  try {
    if (typeof localStorage === "undefined") return null;
    return parsePublicShareInput(localStorage.getItem(STORE_KEY) ?? "");
  } catch {
    return null;
  }
}

export function rememberPublicUrl(raw: string): string | null {
  const parsed = parsePublicShareInput(raw);
  if (!parsed) return null;
  try {
    localStorage.setItem(STORE_KEY, parsed);
  } catch {
    /* private mode */
  }
  return parsed;
}

function urlFromMeta(): string | null {
  if (typeof document === "undefined") return null;
  const attrs = [
    ['meta[property="og:url"]', "content"],
    ['meta[property="og:image"]', "content"],
    ['meta[name="twitter:image"]', "content"],
    ['link[rel="canonical"]', "href"],
  ] as const;
  for (const [sel, attr] of attrs) {
    const el = document.querySelector(sel);
    const raw = el?.getAttribute(attr) ?? "";
    if (!raw) continue;
    try {
      const u = new URL(raw, document.baseURI);
      const fromHost = urlFromHost(u.hostname);
      if (fromHost) return fromHost;
      const viaQuery = u.searchParams.get("host");
      if (viaQuery) {
        const q = urlFromHost(hostFromMaybeUrl(viaQuery));
        if (q) return q;
      }
    } catch {
      const direct = urlFromHost(hostFromMaybeUrl(raw));
      if (direct) return direct;
    }
  }
  return null;
}

function envPublicUrl(): string | null {
  const env =
    typeof import.meta !== "undefined"
      ? (import.meta as ImportMeta & { env?: { VITE_PUBLIC_HOSTNAME?: string } }).env
          ?.VITE_PUBLIC_HOSTNAME
      : "";
  return urlFromHost(hostFromMaybeUrl(String(env ?? "")));
}

/**
 * URL anyone can open without a Grok account.
 * Never the conversation, never *.vercel.app, never the hds- tunnel.
 */
export function publicShareUrl(): string | null {
  const fromEnv = envPublicUrl();
  if (fromEnv) return fromEnv;

  if (typeof window === "undefined") return null;

  const fromMeta = urlFromMeta();
  if (fromMeta) return fromMeta;

  const fromLoc = urlFromHost(cleanHost(window.location.hostname));
  if (fromLoc) return fromLoc;

  return fromStore();
}

/** Sync copy — iframe-safe. Do not await clipboard before execCommand (loses the gesture). */
export function copyText(text: string): boolean {
  if (typeof document === "undefined" || !text) return false;
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.setAttribute("readonly", "");
  ta.setAttribute("aria-hidden", "true");
  ta.style.cssText =
    "position:fixed;top:0;left:0;width:1px;height:1px;padding:0;border:0;opacity:0;";
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  ta.setSelectionRange(0, text.length);
  let ok = false;
  try {
    ok = document.execCommand("copy");
  } catch {
    ok = false;
  }
  document.body.removeChild(ta);
  if (ok) return true;
  try {
    if (navigator.clipboard && window.isSecureContext) {
      void navigator.clipboard.writeText(text);
      return true;
    }
  } catch {
    /* ignore */
  }
  return false;
}

export function copyFromInput(el: HTMLInputElement | null): boolean {
  if (!el || !el.value) return false;
  el.focus();
  el.select();
  el.setSelectionRange(0, el.value.length);
  try {
    if (document.execCommand("copy")) return true;
  } catch {
    /* fall through */
  }
  return copyText(el.value);
}

export async function nativeShare(url: string, title: string): Promise<boolean> {
  if (typeof navigator === "undefined" || typeof navigator.share !== "function") {
    return false;
  }
  try {
    await navigator.share({ title, url, text: title });
    return true;
  } catch {
    return false;
  }
}
