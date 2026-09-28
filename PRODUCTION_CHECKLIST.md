# Shiny Website Production Checklist
Use this checklist before deploying the new website.

## Forms and lead delivery

- [ ] Connect the homepage estimate form to the client’s CRM or LeadConnector endpoint.
- [ ] Connect the dedicated contact form to the correct inbox or CRM pipeline.
- [ ] Connect the careers application form to the hiring inbox or applicant system.
- [ ] Add secure resume-file upload storage and delivery.
- [ ] Replace the current placeholder success messages with confirmed submission results.
- [ ] Add submission-error states and retry guidance.
- [ ] Test every form on desktop and mobile.
- [ ] Confirm that form submissions create the correct notifications and CRM records.
- [ ] Add spam protection that does not block legitimate leads.

## Booking and promotions

- [ ] Confirm the Housecall Pro booking URL with the client.
- [ ] Configure the `WANDER10` code as a valid 10% promotion in the booking or payment system.
- [ ] Define the discount’s expiration date, exclusions, and maximum value.
- [ ] Test the code from the 404 game through the complete booking process.

## Analytics and search

- [ ] Install the client’s GA4 property.
- [ ] Track estimate submissions, contact submissions, job applications, phone clicks, email clicks, and booking clicks as events.
- [ ] Mark the appropriate GA4 events as conversions.
- [ ] Verify Google Search Console ownership for the production domain.
- [ ] Submit `https://shinycarpetcleaning.com/sitemap.xml` in Search Console.
- [ ] Confirm that `robots.txt`, canonical URLs, structured data, and Open Graph images use the production domain.
- [ ] Connect Bing Webmaster Tools if the client wants broader reporting.
- [ ] Record baseline rankings, organic traffic, conversions, and indexed-page totals before launch.

## Business information

- [ ] Confirm the official business name, phone number, email address, primary address, and opening hours.
- [ ] Confirm whether customers are served at the Springfield address or whether the address should be hidden as a service-area business.
- [ ] Confirm every city currently listed in the service-area directory.
- [ ] Confirm that the seven priority location pages represent real operating markets.
- [ ] Add final team names, job titles, biographies, and approved photographs.
- [ ] Replace all temporary team photographs.
- [ ] Verify the final review count and supported review platforms.

## Content and legal

- [ ] Review all imported blog articles for outdated pricing, services, addresses, promotions, and contact details.
- [ ] Confirm that all website photographs are owned by Shiny or properly licensed.
- [ ] Add approved privacy-policy and terms pages locally instead of depending on old-site URLs.
- [ ] Confirm consent language for calls, email, and SMS follow-up.
- [ ] Add any required promotion terms for `WANDER10`.
- [ ] Proofread all pages with the client before launch.

## Hosting and migration

- [ ] Confirm the production hosting provider and deployment process.
- [ ] Confirm that the host supports the rules in `dist/_redirects`; convert them to the host’s format when necessary.
- [ ] Test every redirect in `seo/redirects.csv` on the production environment.
- [ ] Configure HTTPS and redirect HTTP traffic to HTTPS.
- [ ] Choose one canonical hostname and redirect the other version consistently (`www` or non-`www`).
- [ ] Confirm that unknown URLs display the custom 404 game while returning HTTP 404.
- [ ] Preserve the existing domain’s DNS, email records, and third-party verification records during launch.
- [ ] Create a complete backup of the current production website before changing DNS or hosting.

## Final quality checks

- [ ] Crawl the production site for broken links, redirect chains, missing titles, missing descriptions, and duplicate canonicals.
- [ ] Validate structured data with Google’s Rich Results Test.
- [ ] Test homepage, services, about, careers, gallery, blogs, contact, locations, location pages, and the 404 game.
- [ ] Test current Chrome, Safari, Firefox, Edge, iPhone, Android, tablet, and common desktop widths.
- [ ] Test keyboard navigation, focus visibility, form labels, image alternative text, and color contrast.
- [ ] Check Core Web Vitals and optimize oversized images or scripts.
- [ ] Verify that all telephone, email, booking, map, navigation, and CTA links point to the intended destination.
- [ ] Confirm that the production sitemap contains only pages intended for indexing.

## Immediately after launch

- [ ] Submit the sitemap and request indexing for the homepage, service page, location directory, and priority location pages.
- [ ] Check Search Console indexing and crawl reports daily during the first week.
- [ ] Test real form and booking conversions from a separate device.
- [ ] Monitor analytics, server errors, broken URLs, and redirect traffic.
- [ ] Confirm that old high-traffic URLs redirect to the correct new pages.
- [ ] Record the launch date and baseline metrics in the monthly SEO report.

## Monthly SEO work

- [ ] Review Search Console queries, clicks, impressions, average position, and indexing issues.
- [ ] Review GA4 organic traffic, calls, forms, bookings, and conversion rate.
- [ ] Improve pages with high impressions and low click-through rates.
- [ ] Update one important service, location, or blog page with useful first-hand information.
- [ ] Add real project photographs and locally relevant customer proof.
- [ ] Check local rankings and Google Business Profile performance.
- [ ] Reply to reviews and keep business details accurate.
- [ ] Audit broken links, redirects, sitemap status, structured data, and Core Web Vitals.
- [ ] Create a short report listing completed work, results, issues, and next month’s priorities.
