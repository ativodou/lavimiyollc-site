// number of books
const Stripe = require('stripe');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
    const { items, successUrl, cancelUrl } = req.body;

    if (!Array.isArray(items) || !items.length) {
      return res.status(400).json({ error: 'No items provided' });
    }

    const line_items = items.map(item => ({
      price_data: {
        currency: 'usd',
        product_data: { name: item.name },
        unit_amount: Math.round(item.price * 100),
      },
      quantity: item.qty,
    }));

    const isDigital = items.every(i => i.digital);

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items,
      mode: 'payment',
      ...(isDigital ? {} : {
        shipping_address_collection: {
          allowed_countries: ['US', 'CA', 'FR', 'HT', 'GB', 'DE', 'ES', 'IT', 'BE', 'CH'],
        },
      }),
      success_url: successUrl || `${req.headers.origin}/success`,
      cancel_url: cancelUrl || req.headers.origin,
    });

    res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('[checkout]', err.message);
    res.status(500).json({ error: err.message });
  }
};
