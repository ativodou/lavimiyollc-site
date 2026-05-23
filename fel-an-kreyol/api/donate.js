const Stripe = require('stripe');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
    const { amount, mode, successUrl, cancelUrl } = req.body;

    if (!amount || amount < 1) return res.status(400).json({ error: 'Invalid amount' });

    const origin = req.headers.origin || 'https://felankreyol.org';
    const productName = mode === 'subscription'
      ? `Don anyèl — Fèl an Kreyòl Inc.`
      : `Don — Fèl an Kreyòl Inc.`;

    const sessionParams = {
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'usd',
          product_data: {
            name: productName,
            description: 'Edike Ayiti — chak dola = liv pou timoun yo',
          },
          unit_amount: Math.round(amount * 100),
          ...(mode === 'subscription' ? { recurring: { interval: 'month' } } : {}),
        },
        quantity: 1,
      }],
      mode: mode === 'subscription' ? 'subscription' : 'payment',
      success_url: successUrl || `${origin}/success`,
      cancel_url: cancelUrl || origin,
      custom_text: {
        submit: { message: '🙏 Mèsi pou sipò ou. Fèl an Kreyòl Inc. se yon òganizasyon san bi likratif.' },
      },
    };

    const session = await stripe.checkout.sessions.create(sessionParams);
    res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('[donate]', err.message);
    res.status(500).json({ error: err.message });
  }
};
