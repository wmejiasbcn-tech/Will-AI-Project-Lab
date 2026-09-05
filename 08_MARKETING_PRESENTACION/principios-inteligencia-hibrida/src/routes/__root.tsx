import { HeadContent, Outlet, Scripts, createRootRoute } from "@tanstack/react-router";
import { Analytics } from "@vercel/analytics/react";
import { AuthProvider } from "@/lib/auth/provider";
import { PreviewHostBridge } from "@/components/preview-host-bridge";
import { SITE, jsonLd } from "@/lib/seo";
import appCss from "../styles.css?url";

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" },
      { title: SITE.title },
      { name: "description", content: SITE.description },
      { name: "theme-color", content: "#06101c" },
      { name: "robots", content: "index,follow" },
      { name: "language", content: "es-ES" },
      { name: "author", content: "William Mejías Navarro · Will-AI Project Lab" },
      { name: "referrer", content: "strict-origin-when-cross-origin" },
    ],
    links: [
      { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
      { rel: "stylesheet", href: appCss },
      { rel: "manifest", href: "/__grok/manifest.webmanifest" },
      { rel: "apple-touch-icon", href: "/__grok/icon-180.png" },
      { rel: "preload", href: "/fonts/cormorant-garamond-500.woff2?v=1", as: "font", type: "font/woff2" },
      { rel: "preload", href: "/fonts/figtree-400.woff2?v=1", as: "font", type: "font/woff2" },
    ],
  }),
  component: RootDocument,
});

function RootDocument() {
  return (
    <html lang="es-ES" suppressHydrationWarning>
      <head>
        <HeadContent />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd()) }}
        />
      </head>
      <body className="bg-navy text-ivory antialiased">
        <PreviewHostBridge />
        <AuthProvider>
          <Outlet />
        </AuthProvider>
        <Scripts />
        <Analytics />
      </body>
    </html>
  );
}
