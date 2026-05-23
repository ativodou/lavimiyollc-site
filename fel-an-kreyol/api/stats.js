const Stripe = require('stripe');
const https = require('https');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=600');

  // Diagnostic: test raw connectivity to Stripe
  const keyPrefix = (process.env.STRIPE_SECRET_KEY || '').slice(0, 8);
  let rawTest = 'pending';
  try {
    const r = await fetch('https://api.stripe.com/v1/balance', {
      headers: { Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}` },
    });
    rawTest = `fetch_ok:${r.status}`;
  } catch (e) {
    rawTest = `fetch_err:${e.message}`;
  }

  if (req.url && req.url.includes('diag')) {
    return res.status(200).json({ keyPrefix, rawTest, node: process.version });
  }

  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
    let totalCents = 0;
    let startingAfter;

    // Page through all successful, non-refunded charges
    do {
      const batch = await stripe.charges.list({
        limit: 100,
        ...(startingAfter ? { starting_after: startingAfter } : {}),
      });

      for (const charge of batch.data) {
        if (charge.paid && !charge.refunded && charge.currency === 'usd') {
          totalCents += charge.amount;
        }
      }

      startingAfter = batch.has_more ? batch.data[batch.data.length - 1].id : null;
    } while (startingAfter);

    res.status(200).json({
      funds_usd: Math.round(totalCents / 100),
      books_delivered: parseInt(process.env.BOOKS_DELIVERED || '0', 10),
    });
  } catch (err) {
    console.error('[stats]', err.message);
    res.status(500).json({ error: err.message });
  }
};
