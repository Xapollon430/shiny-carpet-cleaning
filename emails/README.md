# Shiny form notifications

The existing Netlify forms store submissions and trigger `netlify/functions/submission-created.js`. The function sends the matching HTML and plain-text templates through Resend. The recipient is fixed to Xapollon430@gmail.com; replies go to the person who submitted the form.

Set these server-side variables in Netlify. Use the Functions scope if your plan supports explicit scopes; the free plan uses the standard environment settings. Never reference these variables in frontend code:

- `RESEND_API_KEY`: a Resend sending API key. Keep it out of frontend files and Git.
- `SHINY_EMAIL_FROM`: `Shiny Carpet Cleaning <notifications@YOUR_VERIFIED_DOMAIN>`.

For testing before domain verification, Resend's `onboarding@resend.dev` sender can send to the email address belonging to the Resend account. That account must use Xapollon430@gmail.com for our requested tests.

Deploy the function alongside the site, then submit a clearly marked test through each actual form. Check both Netlify's saved submissions and the three delivered HTML emails. Test the career form with a disposable test resume. The resume URL is included in the notification.

Once all three deliveries are confirmed, disable the three default Netlify email notifications to avoid duplicates. Keep them enabled until custom delivery is verified.

Preview templates locally with `node scripts/preview_form_emails.cjs`. No server, framework, or Resend SDK needs to be installed.
