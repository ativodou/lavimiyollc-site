module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  const key = process.env.STRIPE_SECRET_KEY || '';
  const keyOk = key.startsWith('sk_test_') || key.startsWith('sk_live_');
  const keyLen = key.length;

  let result = 'pending';
  try {
    const r = await fetch('https://api.stripe.com/v1/balance', {
      method: 'GET',
      headers: { Authorization: `Bearer ${key}` },
    });
    const body = await r.json();
    result = { status: r.status, object: body.object, error: body.error };
  } catch (e) {
    result = { fetchError: e.message };
  }

  res.status(200).json({ node: process.version, keyOk, keyLen, result });
};
