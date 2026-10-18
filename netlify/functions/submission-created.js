const { renderEmail } = require('../../emails/render.cjs');
const supportedForms = new Set(['quote-request', 'contact-message', 'career-application']);

// Netlify invokes this event function after verifying and storing a form submission.
exports.handler = async (event) => {
  const { payload } = JSON.parse(event.body);
  const formName = payload.form_name;
  if (!supportedForms.has(formName)) return { statusCode: 204 };
  if (!payload.id) throw new Error('Missing Netlify submission ID');
  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.SHINY_EMAIL_FROM;
  if (!apiKey || !from) throw new Error('Configure RESEND_API_KEY and SHINY_EMAIL_FROM in Netlify');

  const email = renderEmail(formName, payload.data, process.env.URL || 'https://shiny-carpet-cleaning-va.netlify.app');
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Idempotency-Key': `shiny-submission-${payload.id}`,
    },
    body: JSON.stringify({
      from,
      to: ['xapollon430@gmail.com'],
      subject: email.subject,
      html: email.html,
      text: email.text,
      reply_to: email.replyTo,
    }),
    signal: AbortSignal.timeout(10000),
  });
  if (!response.ok) throw new Error(`Resend rejected notification with HTTP ${response.status}`);
  const sent = await response.json();
  console.log(`Shiny ${formName} notification sent: ${sent.id}`);
  return { statusCode: 200, body: JSON.stringify({ id: sent.id }) };
};
