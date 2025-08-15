const formidable = require('formidable');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

module.exports.config = { api: { bodyParser: false } };

module.exports = async (req, res) => {
  // Basic Auth
  const auth = { login: "SasaBoss", password: "GIGACHAT@1231!" };
  const b64auth = (req.headers.authorization || '').split(' ')[1] || '';
  const [login, password] = Buffer.from(b64auth, 'base64').toString().split(':');
  if (login !== auth.login || password !== auth.password) {
    res.setHeader('WWW-Authenticate', 'Basic realm="Waybill"');
    res.status(401).send('Authentication required.');
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'POST only' });
    return;
  }

  const form = formidable({ multiples: false, keepExtensions: true });
  form.parse(req, (err, fields, files) => {
    if (err) {
      res.status(500).json({ error: String(err) });
      return;
    }
    const file = files.file;
    if (!file) {
      res.status(400).json({ error: 'No file uploaded' });
      return;
    }

    const inputPath = file.filepath;
    const outputPath = path.join('/tmp', 'waybill.xlsx');

    execFile('python3', ['process_invoice.py', inputPath, outputPath], { cwd: process.cwd() }, (error, stdout, stderr) => {
      if (error) {
        res.status(500).json({ error: stderr || error.message });
        return;
      }
      res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
      res.setHeader('Content-Disposition', 'attachment; filename="waybill.xlsx"');
      fs.createReadStream(outputPath).pipe(res);
    });
  });
};
