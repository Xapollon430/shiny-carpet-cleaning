# Shiny form notifications

The exe.dev service in `server/server.cjs` validates quote, contact and career submissions, saves private submission records, and sends the HTML/plain-text templates from `render.cjs` through Resend. Career résumés are attached to email and are not public links.

Server-only configuration in `/etc/shiny.env`:

- RESEND_API_KEY
- SHINY_EMAIL_FROM
- SHINY_EMAIL_TO
- SITE_URL

Current sender: onboarding@resend.dev. Current test recipient: xapollon430@gmail.com. Before client launch, verify a Shiny sender domain in Resend and configure the approved business recipient. The test sender is restricted to the Resend account owner.

All three exe.dev migration tests arrived in the Gmail inbox on October 20, 2026, including the career résumé attachment.

Preview templates with `node scripts/preview_form_emails.cjs`.
