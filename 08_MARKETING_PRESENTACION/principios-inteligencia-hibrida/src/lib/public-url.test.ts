import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  isGatedHost,
  isTunnelHost,
  parsePublicShareInput,
} from "./public-url.ts";

describe("public share URL", () => {
  it("rejects tunnels, grok.com and vercel", () => {
    assert.equal(isTunnelHost("hds-fghyzo1k7txw"), true);
    assert.equal(isTunnelHost("hds-ivjytkrpqm2x-6014-6x2nx.trycloudflare.com"), true);
    assert.equal(isGatedHost("grok.com"), true);
    assert.equal(isGatedHost("www.grok.com"), true);
    assert.equal(isGatedHost("something.vercel.app"), true);
    assert.equal(isGatedHost("wild-race.grok.me"), false);
  });

  it("parses only real *.grok.me app hosts", () => {
    assert.equal(parsePublicShareInput("https://wild-race.grok.me/"), "https://wild-race.grok.me/");
    assert.equal(parsePublicShareInput("wild-race.grok.me"), "https://wild-race.grok.me/");
    assert.equal(parsePublicShareInput("https://plum-plaza-reef-dream.grok.me/foo"), "https://plum-plaza-reef-dream.grok.me/");
    assert.equal(parsePublicShareInput("https://grok.com/chat/abc"), null);
    assert.equal(parsePublicShareInput("https://hds-abc.trycloudflare.com/"), null);
    assert.equal(parsePublicShareInput("https://foo.vercel.app/"), null);
    assert.equal(parsePublicShareInput("localhost"), null);
    assert.equal(parsePublicShareInput("wild-race"), null);
    assert.equal(parsePublicShareInput("https://gate.grok.me/"), null);
    assert.equal(parsePublicShareInput("https://og.grok.me/v1/card.png"), null);
  });
});
