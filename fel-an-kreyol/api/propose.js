export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { mot, kat, def, egz, non, 'imèl': imel } = req.body || {};

  if (!mot || !kat || !def) {
    return res.status(400).json({ error: 'Mo, kategori, ak definisyon obligatwa.' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'Email service not configured.' });
  }

  const html = `
<h2 style="font-family:Georgia,serif;color:#142D70;">Nouvo pwopoziyon mo — Diksyonè Nasyonal</h2>
<table style="border-collapse:collapse;width:100%;font-family:Georgia,serif;font-size:15px;">
  <tr><td style="padding:8px 12px;background:#EEF2FB;font-weight:700;width:130px;">Mo</td><td style="padding:8px 12px;border-bottom:1px solid #E5E0D8;font-size:18px;font-weight:700;color:#142D70;">${mot}</td></tr>
  <tr><td style="padding:8px 12px;background:#EEF2FB;font-weight:700;">Kategori</td><td style="padding:8px 12px;border-bottom:1px solid #E5E0D8;">${kat}</td></tr>
  <tr><td style="padding:8px 12px;background:#EEF2FB;font-weight:700;">Definisyon</td><td style="padding:8px 12px;border-bottom:1px solid #E5E0D8;">${def}</td></tr>
  ${egz ? `<tr><td style="padding:8px 12px;background:#EEF2FB;font-weight:700;">Egzanp</td><td style="padding:8px 12px;border-bottom:1px solid #E5E0D8;font-style:italic;">« ${egz} »</td></tr>` : ''}
  ${non ? `<tr><td style="padding:8px 12px;background:#EEF2FB;font-weight:700;">Non</td><td style="padding:8px 12px;border-bottom:1px solid #E5E0D8;">${non}</td></tr>` : ''}
  ${imel ? `<tr><td style="padding:8px 12px;background:#EEF2FB;font-weight:700;">Imèl</td><td style="padding:8px 12px;">${imel}</td></tr>` : ''}
</table>
<p style="margin-top:20px;font-family:Georgia,serif;font-size:13px;color:#6B7280;">Soumèt via diksyone.felankreyol.org · ${new Date().toLocaleString('fr-FR', { timeZone: 'America/New_York' })}</p>
`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Diksyonè Nasyonal <diksyone@felankreyol.org>',
        to: ['anbyanssa@gmail.com'],
        subject: `Nouvo mo pwopoze: « ${mot} »`,
        html,
        reply_to: imel || undefined,
      }),
    });

    if (!r.ok) {
      const err = await r.text();
      console.error('[propose] Resend error:', err);
      return res.status(502).json({ error: 'Email delivery failed.' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[propose] error:', err);
    return res.status(500).json({ error: 'Internal error.' });
  }
}
