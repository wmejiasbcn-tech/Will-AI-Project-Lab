/**
 * Origin cache + Cloudflare purge tags.
 *
 * Purge-by-tag (Cloudflare Cache-Tag / Surrogate-Key):
 *   waipl         everything
 *   waipl-html    documents — revalidate always; stale-if-error keeps last good page
 *   waipl-assets  hashed JS/CSS (self-busting; purge rarely needed)
 *   waipl-fonts   woff2
 *   waipl-audio   Graphy MP3
 *   waipl-media   blason, og, favicon
 *   waipl-meta    robots, sitemap, manifest
 *
 * 4xx/5xx are no-store so a dead-tunnel "Port not found" cannot stick in the CDN.
 */

type Kind = "html" | "assets" | "fonts" | "audio" | "media" | "meta";

function deployTag(): string {
  const raw = String(
    process.env.VERCEL_DEPLOYMENT_ID || process.env.VITE_PUBLIC_HOSTNAME || "dev",
  )
    .toLowerCase()
    .replace(/^https?:\/\//, "")
    .split("/")[0]
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 48);
  return raw ? `waipl-d-${raw}` : "waipl-d-dev";
}

type Policy = {
  /** Browser Cache-Control */
  browser: string;
  /** CDN-Cache-Control + Cloudflare-CDN-Cache-Control + Surrogate-Control */
  cdn: string;
  tags: string[];
  contentType?: string;
  ranges?: boolean;
  htmlExtras?: boolean;
};

function policies(): Record<Kind, Policy> {
  const d = deployTag();
  return {
    html: {
      browser: "public, max-age=0, must-revalidate",
      cdn: "public, max-age=0, must-revalidate, stale-if-error=86400",
      tags: ["waipl", "waipl-html", d],
      htmlExtras: true,
    },
    assets: {
      browser: "public, max-age=31536000, immutable",
      cdn: "public, max-age=31536000, immutable",
      tags: ["waipl", "waipl-assets"],
    },
    fonts: {
      browser: "public, max-age=31536000, immutable",
      cdn: "public, max-age=31536000, immutable",
      tags: ["waipl", "waipl-fonts"],
      contentType: "font/woff2",
    },
    audio: {
      browser: "public, max-age=86400, stale-while-revalidate=604800",
      cdn: "public, max-age=86400, stale-while-revalidate=604800, stale-if-error=604800",
      tags: ["waipl", "waipl-audio"],
      contentType: "audio/mpeg",
      ranges: true,
    },
    media: {
      browser: "public, max-age=604800, stale-while-revalidate=86400",
      cdn: "public, max-age=604800, stale-while-revalidate=86400, stale-if-error=86400",
      tags: ["waipl", "waipl-media"],
    },
    meta: {
      browser: "public, max-age=0, must-revalidate",
      cdn: "public, max-age=3600, must-revalidate",
      tags: ["waipl", "waipl-meta"],
    },
  };
}

function kindOf(path: string, contentType: string): Kind {
  if (contentType.includes("text/html")) return "html";
  if (path.startsWith("/assets/")) return "assets";
  if (path.startsWith("/fonts/") || path.endsWith(".woff2")) return "fonts";
  if (path.startsWith("/graphy/") || path.endsWith(".mp3")) return "audio";
  if (
    path === "/blason.png" ||
    path === "/og.jpg" ||
    path === "/favicon.svg" ||
    path === "/x-banner.jpg"
  ) {
    return "media";
  }
  return "meta";
}

function headerBag(kind: Kind): Record<string, string> {
  const p = policies()[kind];
  const tags = p.tags.join(",");
  const bag: Record<string, string> = {
    "cache-control": p.browser,
    "cdn-cache-control": p.cdn,
    "cloudflare-cdn-cache-control": p.cdn,
    "surrogate-control": p.cdn,
    "cache-tag": tags,
    "surrogate-key": tags.replaceAll(",", " "),
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
  };
  if (p.ranges) bag["accept-ranges"] = "bytes";
  if (p.htmlExtras) {
    bag.expires = "0";
    bag.pragma = "no-cache";
    bag["permissions-policy"] =
      "camera=(), microphone=(), geolocation=(), payment=(), usb=(), clipboard-write=(self)";
  }
  return bag;
}

/** Vercel/Nitro edge routes — same tags the origin middleware writes. */
export const EDGE_ROUTE_RULES = {
  "/": { headers: headerBag("html") },
  "/assets/**": { headers: headerBag("assets") },
  "/fonts/**": { headers: headerBag("fonts") },
  "/graphy/**": { headers: headerBag("audio") },
  "/blason.png": { headers: headerBag("media") },
  "/og.jpg": { headers: headerBag("media") },
  "/favicon.svg": { headers: headerBag("media") },
  "/robots.txt": { headers: headerBag("meta") },
  "/sitemap.xml": { headers: headerBag("meta") },
};

function stripVaryOrigin(headers: Headers) {
  const vary = headers.get("vary");
  if (!vary) return;
  const parts = vary
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.toLowerCase() !== "origin");
  if (parts.length) headers.set("vary", parts.join(", "));
  else headers.delete("vary");
}

function applyBag(headers: Headers, bag: Record<string, string>) {
  for (const [k, v] of Object.entries(bag)) headers.set(k, v);
}

export function applyHttpCache(path: string, result: unknown): unknown {
  if (!(result instanceof Response)) return result;
  const headers = new Headers(result.headers);
  const type = headers.get("content-type") ?? "";

  if (result.status >= 400) {
    applyBag(headers, {
      "cache-control": "no-store, no-cache, must-revalidate",
      "cdn-cache-control": "no-store",
      "cloudflare-cdn-cache-control": "no-store",
      "surrogate-control": "no-store",
      expires: "0",
      pragma: "no-cache",
      "x-content-type-options": "nosniff",
    });
    headers.delete("cache-tag");
    headers.delete("surrogate-key");
    stripVaryOrigin(headers);
    return new Response(result.body, {
      status: result.status,
      statusText: result.statusText,
      headers,
    });
  }

  const kind = kindOf(path, type);
  const policy = policies()[kind];
  applyBag(headers, headerBag(kind));

  if (policy.contentType) {
    const cur = type.toLowerCase();
    if (!cur || cur.includes("octet-stream") || cur === "text/plain") {
      headers.set("content-type", policy.contentType);
    }
  }

  if (path === "/og.jpg") headers.set("content-type", "image/jpeg");
  else if (path === "/blason.png") headers.set("content-type", "image/png");
  else if (path === "/favicon.svg") {
    headers.set("content-type", "image/svg+xml; charset=utf-8");
  }

  stripVaryOrigin(headers);

  return new Response(result.body, {
    status: result.status,
    statusText: result.statusText,
    headers,
  });
}
