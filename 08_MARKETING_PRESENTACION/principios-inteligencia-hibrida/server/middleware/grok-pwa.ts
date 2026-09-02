/**
 * Deployed-app (Nitro) half of the platform PWA chrome. Auto-registered as
 * global h3 middleware because vite.config.ts sets `serverDir: "./server"` —
 * without that option Nitro v3 never scans this directory.
 *
 * - `?install=1&platform=ios` on a document path → the Home Screen tutorial,
 *   bundled into the server build via `?raw` (the public/ directory is CDN
 *   static output on Vercel and not readable from the function).
 * - `/__grok/manifest.webmanifest` → per-app-named manifest (kept out of
 *   public/ so this dynamic response is the only one).
 * - `/sitemap.xml` → public grok.me loc when the published host is known.
 * - Other HTML documents → stream-inject PWA + OG head tags at `</head>`.
 *   OG identity is baked via `virtual:grok-og-identity` at `vite build`
 *   (this function cannot read `src/lib/og/site.json` or `public/og.jpg`).
 *   This must be a middleware transforming `next()`: h3 discards the `response`
 *   runtime hook's return value, and `render:html` does not exist in Nitro v3.
 *
 * Every response is wrapped with applyHttpCache so HTML revalidates, 4xx is
 * no-store (a dead-tunnel "Port not found" cannot stick in Cloudflare), and
 * hashed assets stay immutable.
 */
import installPageTemplate from "../../scripts/install-page.html?raw";
import { grokOgIdentity } from "virtual:grok-og-identity";
import {
  acceptsHtml,
  createHeadInjector,
  isDocumentPath,
  isInstallQuery,
  publicAppHost,
  renderInstallPageHtml,
  renderWebManifest,
} from "../../scripts/grok-pwa-shared.mjs";
import { applyHttpCache } from "../http-cache";

interface GrokPwaEvent {
  url: URL;
  req: { method: string; headers: Headers };
}

function requestHost(event: GrokPwaEvent): string {
  return (
    event.req.headers.get("x-forwarded-host") ?? event.req.headers.get("host") ?? event.url.host
  );
}

function injectHeadStreaming(response: Response, host: string): Response {
  const injector = createHeadInjector({
    host,
    site: grokOgIdentity.site,
  });
  const transformed = response.body!.pipeThrough(
    new TransformStream<Uint8Array, Uint8Array>({
      transform(chunk, controller) {
        for (const out of injector.push(chunk)) controller.enqueue(out);
      },
      flush(controller) {
        for (const out of injector.flush()) controller.enqueue(out);
      },
    }),
  );
  const headers = new Headers(response.headers);
  headers.delete("content-length");
  return new Response(transformed, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

function sitemapXml(hostHeader: string): string | null {
  const host =
    publicAppHost(process.env.VITE_PUBLIC_HOSTNAME ?? "") || publicAppHost(hostHeader);
  if (!host || !host.endsWith(".grok.me") || host.split(".").length < 3) return null;
  if (host === "www.grok.me" || host === "gate.grok.me" || host === "auth.grok.me" || host === "og.grok.me") {
    return null;
  }
  const loc = `https://${host}/`;
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>${loc}</loc><changefreq>weekly</changefreq></url>\n</urlset>\n`;
}

export default async function grokPwaMiddleware(
  event: GrokPwaEvent,
  next: () => unknown | Promise<unknown>,
): Promise<unknown> {
  const method = (event.req.method ?? "GET").toUpperCase();
  const path = event.url.pathname;
  const urlWithQuery = path + event.url.search;

  if (method === "GET" || method === "HEAD") {
    if (path === "/__grok/manifest.webmanifest" || path === "/__grok/manifest.json") {
      const body = renderWebManifest(requestHost(event));
      return applyHttpCache(
        path,
        new Response(method === "HEAD" ? null : body, {
          headers: {
            "content-type": "application/manifest+json; charset=utf-8",
          },
        }),
      );
    }

    if (path === "/sitemap.xml") {
      const xml = sitemapXml(requestHost(event));
      if (xml) {
        return applyHttpCache(
          path,
          new Response(method === "HEAD" ? null : xml, {
            headers: { "content-type": "application/xml; charset=utf-8" },
          }),
        );
      }
    }

    if (
      method === "GET" &&
      isInstallQuery(urlWithQuery) &&
      isDocumentPath(path) &&
      acceptsHtml(event.req.headers.get("accept"))
    ) {
      const html = renderInstallPageHtml(installPageTemplate, {
        host: requestHost(event),
        url: urlWithQuery,
      });
      return applyHttpCache(
        path,
        new Response(html, {
          headers: { "content-type": "text/html; charset=utf-8" },
        }),
      );
    }
  }

  const result = await next();
  if (
    method === "GET" &&
    result instanceof Response &&
    result.body &&
    String(result.headers.get("content-type") ?? "").includes("text/html") &&
    !result.headers.get("content-encoding")
  ) {
    return applyHttpCache(path, injectHeadStreaming(result, requestHost(event)));
  }
  return applyHttpCache(path, result);
}
