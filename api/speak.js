const https = require('https');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'API key not configured' });

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch(e) { return res.status(400).json({ error: 'Invalid JSON' }); }
  }
  const text = body && body.text;
  if (!text) return res.status(400).json({ error: 'text required' });

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
          res.status(r11.statusCode).json({ error: buf.toString() });
        } else {
          res.setHeader('Content-Type', 'audio/mpeg');
          res.setHeader('Cache-Control', 'public, max-age=86400');
          res.send(buf);
        }
        resolve();
      });
    });
    r.on('error', function(e) { res.status(500).json({ error: e.message }); resolve(); });
    r.write(postData);
    r.end();
  });
};
