const https = require('https');

// Allowlist of origins permitted to call this endpoint.
const ALLOWED_ORIGINS = [
  'https://will-ai-project-lab.vercel.app',
  'https://www.will-ai-project-lab.vercel.app',
  'http://localhost:3000',
  'http://localhost:8080'
];

const MAX_TEXT_LENGTH = 5000;

// --- Rate limiting -----------------------------------------------------
// In-memory sliding-window limiter, keyed by client IP. Module-scope state
// (`requestLog`) persists across invocations within the same warm Vercel
// serverless instance/container, so this actually throttles repeated abuse
// from the same client hitting the same instance — it is not a no-op.
//
// Known limitation: Vercel can route requests to multiple concurrent
// instances/containers, each with its own independent `requestLog`, so the
// effective limit is "N requests per window per instance", not a single
// global limit. For a hard global cap across all instances, replace this
// with a shared store, e.g.:
//
// const { Ratelimit } = require('@upstash/ratelimit');
// const { Redis } = require('@upstash/redis');
// const ratelimit = new Ratelimit({
//   redis: Redis.fromEnv(),
//   limiter: Ratelimit.slidingWindow(10, '1 m'),
// });
// const { success } = await ratelimit.limit(clientIp);
// if (!success) return res.status(429).json({ error: 'Too many requests' });
const RATE_LIMIT_WINDOW_MS = 60 * 1000;
const RATE_LIMIT_MAX_REQUESTS = 10;
const requestLog = new Map(); // clientIp -> array of request timestamps (ms)

function isRateLimited(clientIp) {
  const now = Date.now();
  const timestamps = (requestLog.get(clientIp) || []).filter(
    (t) => now - t < RATE_LIMIT_WINDOW_MS
  );
  if (timestamps.length >= RATE_LIMIT_MAX_REQUESTS) {
    requestLog.set(clientIp, timestamps);
    return true;
  }
  timestamps.push(now);
  requestLog.set(clientIp, timestamps);
  return false;
}

module.exports = async function handler(req, res) {
  const origin = req.headers.origin;
  if (ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  if (origin && !ALLOWED_ORIGINS.includes(origin)) {
    return res.status(403).json({ error: 'Origin not allowed' });
  }

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'Service unavailable' });

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (e) { return res.status(400).json({ error: 'Invalid JSON' }); }
  }
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return res.status(400).json({ error: 'Invalid request body' });
  }

  const text = body.text;
  if (!text || typeof text !== 'string') {
    return res.status(400).json({ error: 'text is required and must be a string' });
  }
  if (text.length > MAX_TEXT_LENGTH) {
    return res.status(400).json({ error: `text exceeds maximum length of ${MAX_TEXT_LENGTH} characters` });
  }

  const forwardedFor = req.headers['x-forwarded-for'];
  const clientIp = (Array.isArray(forwardedFor) ? forwardedFor[0] : forwardedFor || '')
    .split(',')[0]
    .trim() || req.socket?.remoteAddress || 'unknown';
  if (isRateLimited(clientIp)) {
    return res.status(429).json({ error: 'Too many requests, please try again later' });
  }

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
          const payload = { error: 'Failed to synthesize audio' };
          if (process.env.NODE_ENV === 'development') {
            payload.details = buf.toString('utf-8').substring(0, 200);
          }
          res.status(r11.statusCode).json(payload);
        } else {
          res.setHeader('Content-Type', 'audio/mpeg');
          res.setHeader('Cache-Control', 'public, max-age=86400');
          res.send(buf);
        }
        resolve();
      });
    });
    r.on('error', function(e) {
      const payload = { error: 'Internal server error' };
      if (process.env.NODE_ENV === 'development') {
        payload.details = e.message;
      }
      res.status(500).json(payload);
      resolve();
    });
    r.write(postData);
    r.end();
  });
};
