const Stripe = require('stripe');

async function readRawBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).end('Method not allowed');

  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!webhookSecret) {
    console.error('[webhook] STRIPE_WEBHOOK_SECRET not configured');
    return res.status(500).json({ error: 'Server misconfigured' });
  }

  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
  const sig = req.headers['stripe-signature'];

  if (!sig) {
    console.error('[webhook] Missing stripe-signature header');
    return res.status(400).json({ error: 'Missing signature' });
  }

  let event;
  try {
    const rawBody = await readRawBody(req);
    event = stripe.webhooks.constructEvent(rawBody, sig, webhookSecret);
  } catch (err) {
    // Signature mismatch — not from Stripe
    console.error('[webhook] ❌ Signature failed:', err.message);
    return res.status(400).json({ error: `Webhook signature invalid: ${err.message}` });
  }

  // Respond 200 immediately — Stripe marks the webhook failed if we exceed 30s
  res.status(200).json({ received: true });

  // Process after responding so we never time out
  try {
    const type = event.type;
    const obj  = event.data.object;

    if (type === 'checkout.session.completed') {
      const usd   = ((obj.amount_total || 0) / 100).toFixed(2);
      const email = obj.customer_details?.email || '(no email)';
      const name  = obj.customer_details?.name  || '';
      const mode  = obj.mode === 'subscription' ? 'monthly' : 'one-time';
      console.log(`[donation] ✅ $${usd} ${mode} — ${name} <${email}> — ${obj.id}`);
    }

    else if (type === 'invoice.payment_succeeded') {
      // Recurring subscription renewal (not the first payment)
      if (obj.billing_reason === 'subscription_cycle') {
        const usd   = ((obj.amount_paid || 0) / 100).toFixed(2);
        const email = obj.customer_email || '(no email)';
        console.log(`[donation] 🔄 recurring $${usd}/mo — ${email} — ${obj.id}`);
      }
    }

    else if (type === 'customer.subscription.deleted') {
      const email = obj.customer_email || obj.id;
      console.log(`[donation] 🔕 subscription cancelled — ${email} — ${obj.id}`);
    }

    else if (type === 'checkout.session.expired') {
      console.log(`[donation] ⏱ session expired (no payment) — ${obj.id}`);
    }

    else if (type === 'charge.refunded') {
      const usd = ((obj.amount_refunded || 0) / 100).toFixed(2);
      console.log(`[donation] ↩️  refund $${usd} — charge:${obj.id}`);
    }

  } catch (err) {
    console.error('[webhook] Processing error after 200:', err.message);
  }
};
