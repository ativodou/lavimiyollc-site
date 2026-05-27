module.exports = async function handler(req, res) {
  const token = process.env.GITHUB_TOKEN;
  const owner = 'ativodou';
  const repo  = 'lavimiyollc-site';
  const path  = 'fel-an-kreyol/data/diksyone.json';

  try {
    const headers = { Accept: 'application/vnd.github.raw+json' };
    if (token) headers.Authorization = `Bearer ${token}`;

    const r = await fetch(
      `https://api.github.com/repos/${owner}/${repo}/contents/${path}`,
      { headers }
    );

    if (!r.ok) throw new Error(`GitHub ${r.status}`);

    const data = await r.json();
    res.setHeader('Cache-Control', 'public, max-age=30, stale-while-revalidate=60');
    res.setHeader('Content-Type', 'application/json');
    return res.status(200).json(data);
  } catch (err) {
    console.error('[diksyone]', err.message);
    return res.status(502).json({ error: err.message });
  }
};
