const forms = {
  'quote-request': {
    subject: 'New Cleaning Request Received',
    intro: 'We have received a new cleaning request:',
    fields: [['name', 'Name'], ['email', 'Email'], ['phone', 'Phone'], ['zip', 'Zip Code'], ['service', 'Request'], ['details', 'House details and cleaning notes']],
    followup: 'Kindly reach out to the prospect at your earliest convenience to discuss their needs.',
    action: 'Call the Customer',
  },
  'contact-message': {
    subject: 'New Contact Message Received',
    intro: 'We have received a new contact message:',
    fields: [['name', 'Name'], ['email', 'Email'], ['phone', 'Phone'], ['topic', 'Topic'], ['message', 'Message']],
    followup: 'Kindly reach out to the customer at your earliest convenience to answer their message.',
    action: 'Call the Customer',
  },
  'career-application': {
    subject: 'New Career Application Received',
    intro: 'We have received a new career application:',
    fields: [['name', 'Name'], ['email', 'Email'], ['phone', 'Phone'], ['position', 'Position'], ['location', 'Preferred location'], ['experience', 'Years of related experience'], ['availability', 'Availability'], ['message', 'Why they would be a strong fit'], ['resume', 'Resume']],
    followup: 'Please review the application and reach out to the applicant to discuss the next steps.',
    action: 'Call the Applicant',
  },
};
const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const emailAddress = value => /^[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+$/.test(String(value)) ? String(value) : '';
function renderEmail(formName, data, siteUrl = 'https://shiny-carpet-cleaning-va.netlify.app') {
  if (data.resume && typeof data.resume === 'object') data = { ...data, resume: data.resume.url };
  const form = forms[formName];
  if (!form) throw new Error('Unknown Shiny form');
  const site = new URL(siteUrl);
  if (!['https:', 'http:'].includes(site.protocol)) throw new Error('Invalid site URL');
  const phone = String(data.phone || '').replace(/[^+\d]/g, '');
  const email = emailAddress(data.email);
  const fields = form.fields.filter(([key]) => data[key] !== undefined && data[key] !== null && data[key] !== '').map(([key, label]) => {
    const value = String(data[key]);
    let rendered = escape(value).replace(/\r?\n/g, '<br>');
    const href = key === 'email' && email ? `mailto:${email}` : key === 'phone' && phone ? `tel:${phone}` : '';
    if (href) rendered = `<a href="${escape(href)}" style="color:#1556a6">${rendered}</a>`;
    if (key === 'resume') {
      try {
        const url = new URL(value);
        if (url.protocol === 'https:') rendered = `<a href="${escape(url.href)}" style="color:#1556a6">View resume</a>`;
      } catch {}
    }
    return `<div style="margin-bottom:6px;overflow-wrap:anywhere"><strong>${label}:</strong> ${rendered}</div>`;
  }).join('');
  const actionHref = phone ? `tel:${phone}` : email ? `mailto:${email}` : '';
  const actionLabel = phone ? form.action : 'Reply by Email';
  const action = actionHref ? `<table role="presentation" align="center" cellspacing="0" cellpadding="0" style="margin:24px auto"><tr><td bgcolor="#22b676" style="border-radius:10px;text-align:center"><a href="${escape(actionHref)}" style="display:inline-block;padding:12px 25px;background:#22b676;border-radius:10px;color:#fff;font:bold 16px Arial,sans-serif;text-decoration:none">${actionLabel}</a></td></tr></table>` : '';
  const subject = `${form.subject}: ${String(data.name || 'Website visitor').replace(/[\r\n]/g, ' ')}`;
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(subject)}</title></head><body style="margin:0;padding:24px 12px;background:#eaf0f6;font-family:Arial,Helvetica,sans-serif;color:#222"><table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr><td align="center"><table role="presentation" width="600" cellspacing="0" cellpadding="0" style="width:100%;max-width:600px;background:#fff"><tr><td align="center" style="padding:30px 24px"><img src="${escape(new URL('/assets/brand/shiny-logo-full.png', site).href)}" width="200" alt="Shiny Carpet Cleaning" style="display:block;width:200px;max-width:100%;height:auto;border:0"></td></tr><tr><td style="padding:12px 28px 28px;font-size:16px;line-height:1.5"><p style="margin:0 0 20px">${form.intro}</p>${fields}<p style="margin:24px 0 0">${form.followup}</p>${action}<p style="margin:24px 0 0">Thank you,<br>Shiny Carpet Cleaning</p></td></tr></table></td></tr></table></body></html>`;
  const text = [form.intro, '', ...form.fields.filter(([key]) => data[key] !== undefined && data[key] !== null && data[key] !== '').map(([key,label]) => `${label}: ${data[key]}`), '', form.followup, '', 'Thank you,', 'Shiny Carpet Cleaning'].join('\n');
  return { subject, html, text, replyTo: email || undefined };
}
module.exports = { renderEmail };
