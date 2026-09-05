const https = require('https');

const ALLOWED_ORIGINS = new Set([
  'https://will-ai-project-lab.vercel.app',
  'https://www.will-ai-project-lab.vercel.app',
  'https://wmejiasbcn-tech.github.io',
  ...(process.env.ALLOWED_ORIGINS || '').split(',').map((origin) => origin.trim()).filter(Boolean)
]);
const MAX_TEXT_LENGTH = 1000;
const MAX_BODY_LENGTH = 12000;
const RATE_LIMIT_WINDOW_MS = 60 * 1000;
const RATE_LIMIT_MAX_REQUESTS = 10;
const requestCounts = new Map();

function getClientAddress(req) {
  const forwarded = req.headers['x-forwarded-for'];
  return (typeof forwarded === 'string' && forwarded.split(',')[0].trim()) ||
    req.headers['x-real-ip'] ||
    req.socket?.remoteAddress ||
    'unknown';
}

function isRateLimited(address) {
  const now = Date.now();
  const current = requestCounts.get(address);
  if (!current || now - current.startedAt >= RATE_LIMIT_WINDOW_MS) {
    requestCounts.set(address, { startedAt: now, count: 1 });
    return false;
  }
  current.count += 1;
  return current.count > RATE_LIMIT_MAX_REQUESTS;
}

function parseBody(req) {
  if (req.body && typeof req.body === 'object' && !Array.isArray(req.body)) {
    return req.body;
  }
  if (typeof req.body !== 'string') return null;
  try {
    const body = JSON.parse(req.body);
    return body && typeof body === 'object' && !Array.isArray(body) ? body : null;
  } catch {
    return null;
  }
}

module.exports = async function handler(req, res) {
  const origin = req.headers.origin;
  const originAllowed = typeof origin === 'string' && ALLOWED_ORIGINS.has(origin);
  res.setHeader('Vary', 'Origin');

  if (!originAllowed) {
    return res.status(403).json({ error: 'Origin not allowed' });
  }
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const contentLength = Number(req.headers['content-length']);
  if (Number.isFinite(contentLength) && contentLength > MAX_BODY_LENGTH) {
    return res.status(413).json({ error: 'Request too large' });
  }
  if (isRateLimited(getClientAddress(req))) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  const body = parseBody(req);
  const text = body?.text;
  const bodySize = body ? Buffer.byteLength(JSON.stringify(body)) : 0;
  const bodyKeys = body ? Object.keys(body) : [];
  if (
    !body ||
    bodyKeys.some((key) => key !== 'text') ||
    bodySize > MAX_BODY_LENGTH ||
    typeof text !== 'string' ||
    text.trim().length === 0 ||
    text.length > MAX_TEXT_LENGTH
  ) {
    return res.status(400).json({ error: 'Invalid request' });
  }

  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) return res.status(503).json({ error: 'Service unavailable' });

  const postData = JSON.stringify({
    text,
    model_id: 'eleven_multilingual_v2',
    voice_settings: { stability: 0.55, similarity_boost: 0.85, style: 0.18, use_speaker_boost: true }
  });

  return new Promise((resolve) => {
    const request = https.request({
      hostname: 'api.elevenlabs.io',
      path: '/v1/text-to-speech/l32B8XDoylOsZKiSdfhE',
      method: 'POST',
      headers: {
        Accept: 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': apiKey,
        'Content-Length': Buffer.byteLength(postData)
      },
      timeout: 15000
    }, (upstream) => {
      const chunks = [];
      let size = 0;
      upstream.on('data', (chunk) => {
        size += chunk.length;
        if (size <= 5 * 1024 * 1024) chunks.push(chunk);
      });
      upstream.on('end', () => {
        if (upstream.statusCode !== 200 || size > 5 * 1024 * 1024) {
          res.status(502).json({ error: 'Speech service unavailable' });
        } else {
          res.setHeader('Content-Type', 'audio/mpeg');
          res.setHeader('Cache-Control', 'no-store');
          res.send(Buffer.concat(chunks));
        }
        resolve();
      });
    });
    request.on('timeout', () => request.destroy());
    request.on('error', () => {
      if (!res.headersSent) res.status(502).json({ error: 'Speech service unavailable' });
      resolve();
    });
    request.end(postData);
  });
};
