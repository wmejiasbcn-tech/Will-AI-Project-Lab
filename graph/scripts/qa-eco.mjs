import { chromium } from "playwright";

const url = process.argv[2] || "http://127.0.0.1:8080/";
const out = process.argv[3] || "/workspace/screenshots";

const browser = await chromium.launch({ args: ["--no-sandbox"] });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
page.setDefaultTimeout(10000);
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});

const shot = (name) =>
  page.screenshot({ path: `${out}/${name}.png`, fullPage: false, timeout: 4000 }).catch((e) => {
    console.error("shot fail", name, e.message);
  });
const step = (s) => console.error("STEP", s);
const clickNav = (id) =>
  page.evaluate((nav) => {
    const el = [...document.querySelectorAll(`[data-nav="${nav}"]`)].find((n) => n.offsetParent);
    if (!el) throw new Error("nav " + nav);
    el.click();
  }, id);
const eco = () =>
  page.evaluate(() => {
    const el = document.querySelector("[data-ready]");
    return {
      entered: el?.getAttribute("data-entered"),
      view: el?.getAttribute("data-view"),
      cursor: el?.getAttribute("data-cursor"),
      stack: el?.getAttribute("data-stack"),
    };
  });

try {
  step("goto");
  await page.goto(url, { waitUntil: "load" });
  await page.waitForSelector("[data-ready='true']");
  await shot("qa-portal");

  step("entrar");
  await page.getByTestId("entrar").click();
  await page.waitForSelector("[data-entered='1']");
  // skip 3D screenshots — headless waits forever on webfonts + WebGL

  step("mapas");
  await clickNav("mapa");
  await page.waitForTimeout(300);

  step("chip documento");
  const chip = page.getByTestId("chip-documento");
  await chip.hover();
  await page.waitForTimeout(200);
  if (!/Memoria escrita/i.test(await page.locator("body").innerText())) {
    throw new Error("Hover Documento no muestra pista");
  }
  await chip.click();
  await page.waitForSelector("[data-testid=galleta]");

  step("chip comunidad");
  await page.getByTestId("chip-comunidad").click();
  await page.waitForTimeout(300);
  await page.getByTestId("galleta").waitFor({ state: "visible" });

  step("config");
  console.error("before config", await eco());
  await clickNav("config");
  await page.waitForTimeout(300);
  console.error("after config", await eco());
  const cfg = await page.locator("body").innerText();
  if (/Custodia del blasón|#0A0A0B|Elena o su delegada/i.test(cfg)) {
    throw new Error("Leyenda técnica de custodia sigue visible");
  }

  step("volver portada");
  await page.evaluate(() => {
    const btn = [...document.querySelectorAll("button")].find((b) =>
      (b.textContent || "").includes("Volver a la portada"),
    );
    if (!btn) throw new Error("no volver");
    btn.click();
  });
  await page.waitForSelector("[data-entered='0']");
  await shot("qa-portal-back");

  step("glosario");
  await page.getByRole("button", { name: "Inmersivo" }).click();
  await page.getByTestId("glosario").waitFor({ state: "visible", timeout: 5000 });
  await shot("qa-glosario");
  await page.evaluate(() => {
    document.querySelector("[aria-label='Cerrar glosario']")?.click();
  });
  await page.waitForTimeout(200);

  step("explorar after back");
  await page.getByTestId("explorar").click();
  await page.waitForSelector("[data-entered='1']");

  step("atras then conectar");
  console.error("before atras", await eco());
  await page.evaluate(() => document.querySelector("[data-testid=atras]")?.click());
  await page.waitForSelector("[data-entered='0']", { timeout: 5000 });
  console.error("after atras", await eco());
  await page.evaluate(() => document.querySelector("[data-testid=conectar]")?.click());
  console.error("clicked conectar");
  await page.waitForSelector("[data-entered='1']", { timeout: 5000 });
  console.error("after conectar", await eco());
  const hasGalleta = await page.evaluate(() => !!document.querySelector("[data-testid=galleta]"));
  console.error("galleta", hasGalleta);
  if (!hasGalleta) throw new Error("Conectar no abre ficha");

  const audio = await page.evaluate(() => {
    const el = document.querySelector("audio");
    return el ? { src: el.getAttribute("src"), loop: el.loop } : null;
  });
  if (!audio || !/umbral/.test(audio.src || "")) throw new Error("Audio ambiental ausente");

  step("mobile");
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
  mobile.on("pageerror", (e) => errors.push("mobile: " + e.message));
  await mobile.goto(url, { waitUntil: "load" });
  await mobile.waitForSelector("[data-ready='true']");
  await mobile.screenshot({ path: `${out}/qa-portal-mobile.png`, timeout: 3000 }).catch(() => {});
  await mobile.getByTestId("entrar").click();
  await mobile.waitForSelector("[data-entered='1']");
  await mobile.evaluate(() => {
    const el = [...document.querySelectorAll("[data-nav='mapa']")].find((n) => n.offsetParent);
    el?.click();
  });
  await mobile.waitForTimeout(300);
  await mobile.getByTestId("chip-documento").click();
  await mobile.waitForTimeout(400);
  const mobileGalleta = await mobile.evaluate(() => !!document.querySelector("[data-testid=galleta]"));
  if (!mobileGalleta) throw new Error("Mobile: Documento no abre galleta");
  await mobile.close();

  await browser.close();
  const unique = [...new Set(errors)].filter((e) => !/favicon|Download the React DevTools/i.test(e));
  console.log(JSON.stringify({ ok: unique.length === 0, errors: unique, audio }, null, 2));
  if (unique.length) process.exit(1);
} catch (err) {
  await shot("qa-fail").catch(() => {});
  console.error("FAIL", err);
  await browser.close().catch(() => {});
  process.exit(1);
}
