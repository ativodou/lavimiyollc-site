module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { amount } = req.body; // HTG
    if (!amount || parseFloat(amount) < 1) return res.status(400).json({ error: 'Invalid amount' });

    const base = process.env.MONCASH_ENV === 'sandbox'
      ? 'https://sandbox.moncashbutton.digicelgroup.com'
      : 'https://moncashbutton.digicelgroup.com';

    const credentials = Buffer.from(
      `${process.env.MONCASH_CLIENT_ID}:${process.env.MONCASH_CLIENT_SECRET}`
    ).toString('base64');

    // 1 — Get access token
    const tokenRes = await fetch(
      `${base}/Api/v1/oauth/token?grant_type=client_credentials&scope=read,write`,
      {
        method: 'POST',
        headers: {
          Authorization: `Basic ${credentials}`,
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
      }
    );
    if (!tokenRes.ok) throw new Error(`MonCash auth ${tokenRes.status}`);
    const { access_token } = await tokenRes.json();

    // 2 — Create payment order
    const orderId = `felkr-${Date.now()}`;
    const payRes = await fetch(`${base}/Api/v1/CreatePayment`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${access_token}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ amount: parseFloat(amount), orderId }),
    });
    if (!payRes.ok) throw new Error(`MonCash payment ${payRes.status}`);
    const { payment_token } = await payRes.json();

    const url = `${base}/Moncash-middleware/Payment/Startpayment?token=${payment_token.token}`;
    res.status(200).json({ url });
  } catch (err) {
    console.error('[moncash]', err.message);
    res.status(500).json({ error: err.message });
  }
};
