# Shiny static website handoff

Publish the CONTENTS of `dist/` at the root of the business website, not under `/dist/` or a subfolder. No npm install, framework, build step, database, WordPress, Node server or Resend account is required to display the pages. A web server/static host is required; opening files directly is not a deployment.

The archive is prepared for https://shinycarpetcleaning.com. Confirm the final hostname before launch. For another hostname, rebuild with `handoff/build_static.py --site-url https://chosen-host --output /destination` in the source project, or update all canonical links, JSON-LD IDs/URLs, social images and sitemap/robots URLs in the delivered files. Do not leave preview-domain canonicals in production.

## Receiving-team setup

| Item | Included behavior | Receiving-team responsibility |
|---|---|---|
| Pages, styles, scripts, photos, SVG animation, gallery, blog archive | Static files in dist | Serve with correct MIME types, HTTPS, trailing-slash directory URLs and real 404 responses. |
| Quote/contact/careers forms | Frontend fields and validation; disabled submission until endpoints are configured | Set the three POST URLs in assets/handoff-config.js. Implement email delivery, validation, spam/rate limits, privacy/storage and error handling. Never put an email API key in browser JS. |
| Career resumes | Browser file input | Backend must accept multipart upload with resume and form fields. Limit size/types; do not expose uploads publicly. Current backend limits are 5 MB, PDF/DOC/DOCX. |
| Booking | Existing Housecall Pro booking URL | Confirm Shiny controls this booking account and that appointments reach the business. No booking API key is in the site. |
| Live reviews page | Existing Elfsight app ID and elfsightcdn.com script | Confirm Shiny controls the widget/subscription, permitted domain and review source accounts. The static homepage review quotes are separate content. |
| Service-area map | Leaflet 1.9.4 from unpkg.com; Esri World Street Map tiles | External network access is required. Preserve map attribution; maintain the library/tile provider or replace it. |
| Fonts | Google Fonts: Manrope and Instrument Serif | External network access is required; self-host if preferred, preserving the fonts' licenses. |
| Old URL migration | dist/_redirects plus migration/redirects.csv and inventory | Translate/apply 223 explicit rules in the chosen host. _redirects is not universal. Preserve 301 status, query strings and fragment destinations; return 410 plus noindex for retired routes. All internal redirect destinations must return 200. |
| Sitemap / robots / structured data / social metadata | Included for target domain | Keep crawlable URLs indexable; submit sitemap and verify canonicals after domain switch. |
| Search Console / Analytics / Business Profile | No new analytics collection configured | Request access to existing business properties, keep history and add consent/conversion measurement as appropriate. Presence of prior-site tags is not proof of collection. |
| Domain/email DNS | Not included | Keep domain ownership with Shiny. Coordinate website DNS and TLS with the provider; preserve existing mail DNS records. Domain transfer is not required merely to change web hosting. |

## Form endpoint contract

Quote and contact send application/x-www-form-urlencoded; careers sends multipart/form-data. All send `form-name` and `bot-field` as well as the visible fields. Return a non-2xx response on any failure; return 2xx only after accepting the submission for actual delivery. The frontend shows success on any 2xx, so do not return a fallback HTML page for an unhandled POST. Use same-origin endpoints or configure CORS explicitly.

Required quote fields: name, email, phone, zip, service; optional details; consent is required in the browser. Required contact fields: name, email, message. Required career fields: name, email, phone, position, location, availability, message, resume; optional experience.

## Not included

Git repository/history, developer account details, SSH access, production environment files, email-service credentials, server code, customer submissions/resumes, old Netlify archives, screenshots, audit reports and local tooling are excluded. No form or inbox-delivery claim applies to this static-only archive. Original development/build sources and the existing Node/Resend backend can be transferred separately if requested.

## Before acceptance

Check desktop/mobile layout, every primary route, service map, review widget, booking, all three form submissions including inbox and resume delivery, redirect CSV behavior, unknown-route 404, robots/sitemap/canonicals and domain HTTPS. Recheck performance after deployment: the benchmark report measures exe.dev, not the receiving provider.

Included photos, logo variations, fonts, library and widget integrations remain subject to their respective ownership and license terms. The receiving team should confirm the business's asset rights and subscriptions.
