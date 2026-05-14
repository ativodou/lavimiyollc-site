const SANDBOX = process.env.MONCASH_ENV !== 'production';
const BASE_URL = SANDBOX
  ? 'https://sandbox.moncashbutton.digicelgroup.com/Api'
  : 'https://moncashbutton.digicelgroup.com/Api';
const REDIRECT_BASE = SANDBOX
  ? 'https://sandbox.moncashbutton.digicelgroup.com/Moncash-middleware/Payment/Redirect'
  : 'https://moncashbutton.digicelgroup.com/Moncash-middleware/Payment/Redirect';

const HTG_RATE = 132; // USD → HTG approximate rate

async function getToken() {
  const creds = Buffer.from(
    `${process.env.MONCASH_CLIENT_ID}:${process.env.MONCASH_CLIENT_SECRET}`
  ).toString('base64');
  const res = await fetch(`${BASE_URL}/oauth/token`, {
    method: 'POST',
    headers: {
      Authorization: `Basic ${creds}`,
      'Content-Type': 'application/x-www-form-urlencoded',
      Accept: 'application/json',
    },
    body: 'grant_type=client_credentials&scope=read,write',
  });
  const data = await res.json();
  if (!data.access_token) throw new Error('MonCash auth failed: ' + JSON.stringify(data));
  return data.access_token;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { items } = req.body;
    if (!Array.isArray(items) || !items.length) {
      return res.status(400).json({ error: 'No items provided' });
    }

    const totalUSD = items.reduce((s, i) => s + i.price * i.qty, 0);
    const totalHTG = Math.round(totalUSD * HTG_RATE);
    const orderId = 'LM-' + Date.now();

    const token = await getToken();

    const payRes = await fetch(`${BASE_URL}/v1/CreatePayment`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ amount: totalHTG, orderId }),
    });

    const payData = await payRes.json();
    if (!payData.payment_token?.token) {
      return res.status(500).json({ error: 'MonCash payment creation failed', detail: payData });
    }

    res.status(200).json({ url: `${REDIRECT_BASE}?token=${payData.payment_token.token}` });
  } catch (err) {
    console.error('[moncash]', err.message);
    res.status(500).json({ error: err.message });
  }
};
