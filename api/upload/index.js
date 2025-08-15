const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  try {
    // Read multipart form
    const chunks = [];
    req.on('data', d => chunks.push(d));
    await new Promise(r => req.on('end', r));
    const contentType = req.headers['content-type'] || '';
    if (!contentType.startsWith('multipart/form-data')) {
      return res.status(400).json({ error: 'Expect multipart/form-data' });
    }
    // Parse multipart manually (simple; Vercel parses automatically in real env or use formidable)
    // Here, to keep template simple, we write raw body to temp and let python script read it using werkzeug/formidable? 
    // Instead, simpler: rely on Vercel default body parsing OFF and use 'formidable'.
    return res.status(400).json({ error: 'Please install formidable in real deployment.' });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
};
module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'POST only' });
  }

  // Заглушка: пока что просто отдаём JSON-ответ
  res.status(200).json({
    message: 'Файл получен! Здесь будет обработка PDF → Excel.'
  });
};
