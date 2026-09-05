const https = require('https');

const MAX_TEXT_LENGTH = 2000;
const MAX_BODY_LENGTH = 16 * 1024;
const RATE_LIMIT = 10;
const RATE_WINDOW_MS = 60 * 1000;
const requests = new Map();

function allowedOrigins() {
  const configured = (process.env.WAIPL_ALLOWED_ORIGINS || process.env.ALLOWED_ORIGINS || '')
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean);
  const defaults = [
    'https://will-ai-project-lab.vercel.app',
    'https://www.will-ai-project-lab.vercel.app',
    'https://wmejiasbcn-tech.github.io',
    'http://localhost:3000',
    'http://localhost:5173'
  ];
  if (process.env.VERCEL_URL) defaults.push(`https://${process.env.VERCEL_URL}`);
  return new Set([...defaults, ...configured]);
}

function clientKey(req, origin) {
  const forwarded = req.headers['x-forwarded-for'];
  const address = forwarded ? forwarded.split(',')[0].trim() : (req.socket && req.socket.remoteAddress) || 'unknown';
  return `${origin}:${address}`;
}

function isRateLimited(key) {
  const now = Date.now();
  if (requests.size > 1000) {
    for (const [storedKey, entry] of requests) {
      if (now - entry.startedAt >= RATE_WINDOW_MS) requests.delete(storedKey);
    }
  }
  const entry = requests.get(key);
  if (!entry || now - entry.startedAt >= RATE_WINDOW_MS) {
    requests.set(key, { startedAt: now, count: 1 });
    return false;
  }
  entry.count += 1;
  return entry.count > RATE_LIMIT;
}

module.exports = async function handler(req, res) {
  const origin = req.headers.origin;
  if (!origin || !allowedOrigins().has(origin)) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (Number(req.headers['content-length']) > MAX_BODY_LENGTH ||
      !String(req.headers['content-type'] || '').toLowerCase().startsWith('application/json')) {
    return res.status(400).json({ error: 'Invalid request' });
  }
  if (isRateLimited(clientKey(req, origin))) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    if (Buffer.byteLength(body, 'utf8') > MAX_BODY_LENGTH) return res.status(413).json({ error: 'Request too large' });
    try { body = JSON.parse(body); } catch (e) { return res.status(400).json({ error: 'Invalid request' }); }
  }
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return res.status(400).json({ error: 'Invalid request' });
  }
  const text = body.text;
  if (typeof text !== 'string' || !text.trim() || text.length > MAX_TEXT_LENGTH) {
    return res.status(400).json({ error: 'Invalid text' });
  }

  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) return res.status(503).json({ error: 'Service unavailable' });

  const voiceId = 'l32B8XDoylOsZKiSdfhE';
  const postData = JSON.stringify({
    text: text,
    model_id: 'eleven_multilingual_v2',
    voice_settings: { stability: 0.55, similarity_boost: 0.85, style: 0.18, use_speaker_boost: true }
  });

  return new Promise((resolve) => {
    const options = {
      hostname: 'api.elevenlabs.io',
      path: '/v1/text-to-speech/' + voiceId,
      method: 'POST',
      headers: {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': apiKey,
        'Content-Length': Buffer.byteLength(postData)
      }
    };
    const r = https.request(options, function(r11) {
      const chunks = [];
      r11.on('data', function(c) { chunks.push(c); });
      r11.on('end', function() {
        const buf = Buffer.concat(chunks);
        if (r11.statusCode !== 200) {
          res.status(502).json({ error: 'Speech service unavailable' });
        } else {
          res.setHeader('Content-Type', 'audio/mpeg');
          res.setHeader('Cache-Control', 'public, max-age=86400');
          res.send(buf);
        }
        resolve();
      });
    });
    r.on('error', function() { res.status(502).json({ error: 'Speech service unavailable' }); resolve(); });
    r.write(postData);
    r.end();
  });
};
