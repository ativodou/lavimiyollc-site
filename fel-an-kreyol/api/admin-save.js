export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { password, entries } = req.body || {};

  if (!password || password !== process.env.ADMIN_PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (!Array.isArray(entries)) {
    return res.status(400).json({ error: 'Invalid entries' });
  }

  const token = process.env.GITHUB_TOKEN;
  const owner = 'ativodou';
  const repo  = 'lavimiyollc-site';
  const path  = 'fel-an-kreyol/data/diksyone.json';

  if (!token) return res.status(500).json({ error: 'GITHUB_TOKEN not set' });

  // Get current file SHA (required for update)
  const getRes = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
  });

  if (!getRes.ok && getRes.status !== 404) {
    const err = await getRes.text();
    console.error('[admin-save] GitHub GET error:', err);
    return res.status(502).json({ error: 'Could not read file from GitHub.' });
  }

  const current = getRes.ok ? await getRes.json() : null;
  const sha = current?.sha;

  const content = Buffer.from(JSON.stringify(entries, null, 2)).toString('base64');

  const putBody = {
    message: `diksyone: admin update (${entries.length} entries)`,
    content,
    ...(sha ? { sha } : {}),
  };

  const putRes = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${path}`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'Content-Type': 'application/json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    body: JSON.stringify(putBody),
  });

  if (!putRes.ok) {
    const err = await putRes.text();
    console.error('[admin-save] GitHub PUT error:', err);
    return res.status(502).json({ error: 'Could not save to GitHub.' });
  }

  return res.status(200).json({ ok: true, count: entries.length });
}
