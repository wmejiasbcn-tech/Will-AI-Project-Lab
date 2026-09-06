const https = require('https');

const ALLOWED_ORIGINS = [
  'https://will-ai-project-lab.vercel.app',
  'https://www.will-ai-project-lab.vercel.app',
  'https://graph.waipl.dev',
  'https://waipl.dev',
  'http://localhost:3000',
  'http://localhost:8080'
];

const MAX_TEXT_LENGTH = 5000;
const RATE_LIMIT_WINDOW_MS = 60 * 1000;
const RATE_LIMIT_MAX_REQUESTS = 10;
const requestLog = new Map();

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

function elevenRequest(apiKey, method, path, body, accept) {
  return new Promise((resolve, reject) => {
    const postData = body ? JSON.stringify(body) : '';
    const headers = {
      Accept: accept || 'application/json',
      'xi-api-key': apiKey
    };
    if (postData) {
      headers['Content-Type'] = 'application/json';
      headers['Content-Length'] = Buffer.byteLength(postData);
    }
    const r = https.request({
      hostname: 'api.elevenlabs.io',
      path,
      method,
      headers
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, buf: Buffer.concat(chunks) }));
    });
    r.on('error', reject);
    if (postData) r.write(postData);
    r.end();
  });
}

function safeReason(buf) {
  try {
    const parsed = JSON.parse(buf.toString('utf-8').substring(0, 400));
    let detail = '';
    if (typeof parsed.detail === 'string') detail = parsed.detail;
    else if (parsed.detail && typeof parsed.detail === 'object') {
      detail = parsed.detail.message || parsed.detail.status || '';
    } else {
      detail = parsed.message || parsed.error || '';
    }
    if (detail && !/xi-api-key|api.key|sk_/i.test(String(detail))) {
      return String(detail).substring(0, 160);
    }
  } catch (e) { /* ignore */ }
  return '';
}

async function resolveVoiceId(apiKey, raw) {
  const token = String(raw || 'Zara').trim().replace(/^["']|["']$/g, '');
  if (/^[a-zA-Z0-9]{16,32}$/.test(token)) return token;
  const listed = await elevenRequest(apiKey, 'GET', '/v1/voices');
  if (listed.status !== 200) return null;
  let data;
  try { data = JSON.parse(listed.buf.toString('utf-8')); } catch (e) { return null; }
  const voices = data.voices || [];
  const want = token.toLowerCase();
  const named = voices.find((v) => String(v.name || '').toLowerCase() === want)
    || voices.find((v) => /^(zara|sara)$/i.test(v.name || ''))
    || voices.find((v) => /zara|sara/i.test(v.name || ''));
  return named ? named.voice_id : null;
}

async function synthesize(apiKey, voiceId, text) {
  const models = ['eleven_multilingual_v2', 'eleven_turbo_v2_5', 'eleven_flash_v2_5'];
  const bodyBase = {
    text,
    voice_settings: { stability: 0.5, similarity_boost: 0.8 }
  };
  let last = { status: 500, buf: Buffer.from('{}') };
  for (const model_id of models) {
    last = await elevenRequest(
      apiKey,
      'POST',
      '/v1/text-to-speech/' + encodeURIComponent(voiceId),
      { ...bodyBase, model_id },
      'audio/mpeg'
    );
    if (last.status === 200) return last;
  }
  return last;
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

  let voiceId;
  try {
    voiceId = await resolveVoiceId(apiKey, process.env.ELEVENLABS_VOICE_ID);
  } catch (e) {
    return res.status(502).json({ error: 'Voice lookup failed' });
  }
  if (!voiceId) {
    return res.status(500).json({ error: 'Zara voice not found' });
  }

  let result;
  try {
    result = await synthesize(apiKey, voiceId, text);
  } catch (e) {
    return res.status(500).json({ error: 'Internal server error' });
  }

  if (result.status !== 200) {
    const payload = { error: 'Failed to synthesize audio', status: result.status };
    const reason = safeReason(result.buf);
    if (reason) payload.reason = reason;
    return res.status(result.status).json(payload);
  }

  res.setHeader('Content-Type', 'audio/mpeg');
  res.setHeader('Cache-Control', 'public, max-age=86400');
  return res.send(result.buf);
};
