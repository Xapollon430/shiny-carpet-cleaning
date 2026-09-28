# Shiny Carpet Cleaning SEO runbook

Updated: September 29, 2026

## What is now in the rebuild

- A `/locations/` directory with 31 service-area pages covering the cities listed on the current Shiny website.
- Original copy for every service-area page. The pages describe coverage and never imply that Shiny has a physical office in every city.
- Nearby-city internal links calculated from each location's coordinates.
- Links from the homepage map, site navigation, and footer to the location directory.
- A unique title, description, canonical URL, Open Graph metadata, Twitter metadata, and index directive on every indexable HTML page.
- `LocalBusiness` and `WebSite` structured data on the homepage.
- `Service`, `BreadcrumbList`, and `FAQPage` structured data on each service-area page.
- `BlogPosting` structured data on the locally hosted articles.
- `sitemap.xml`, `robots.txt`, and a custom noindex 404 page.

## What the current live website does

The current WordPress site has 96 URLs in its page sitemap and 120 URLs in its post sitemap. Its useful SEO assets include:

- Individual pages for its core services.
- City pages for Northern Virginia, Maryland, and Washington, DC.
- Dedicated county pages and some service-and-city combinations.
- Pricing, package, promotion, reviews, gallery, contact, booking, and estimate pages.
- Title tags, descriptions, canonical URLs, Open Graph metadata, XML sitemaps, and robots rules.
- Organization, service, local business, breadcrumb, and FAQ structured data on some templates.
- Online booking through Housecall Pro and embedded lead forms through LeadConnector.

## What to carry into the rebuild

1. Keep the service and location information architecture.
2. Keep the direct Housecall Pro booking path.
3. Build a detailed page for every service that Shiny actually sells.
4. Keep real FAQs, preparation instructions, process details, and package information.
5. Keep verified reviews and recognizable third-party trust signals.
6. Keep current promotions only while they are valid.
7. Preserve every valuable old URL with a server-side 301 redirect.
8. Keep the three confirmed contact locations if the business still operates from all three.

## What not to copy

- Do not copy the old page text. Reusing it would preserve weak or duplicated copy and make the migration less useful.
- Do not create city pages that only swap the city name. Each location page needs useful local context, nearby coverage, real availability, and internal links.
- Do not claim an office in a city unless customers can visit or contact Shiny at that address.
- Do not copy old claims such as awards, certifications, pricing, allergy removal percentages, same-day availability, or guarantees until the business verifies them.
- Do not copy keyword-heavy titles or headings. The live carpet service page currently has two H1 elements, and some live titles are much longer than search results display well.
- Do not mark ordinary landing pages as `Article` or assign a fictional person as the author. The live schema does this on several non-article pages.
- Do not index thank-you, ad campaign, expired sale, template, or duplicate booking pages.

## First launch SEO work

### 1. Migration and indexing

- Approve the final production domain and canonical URL format.
- Export all WordPress URLs before the domain changes.
- Map every valuable old URL to its closest new page.
- Install server-side 301 redirects before changing DNS.
- Return 410 for expired pages that have no replacement and no links or traffic.
- Submit the new sitemap in Google Search Console and Bing Webmaster Tools.
- Inspect the homepage, service directory, location directory, top five service pages, and top ten blog URLs after launch.
- Monitor 404s and redirect chains every day for the first two weeks.

### 2. Measurement

- Install Google Tag Manager and GA4.
- Verify Google Search Console and Bing Webmaster Tools.
- Track estimate submissions, contact submissions, career submissions, booking clicks, phone clicks, email clicks, and map or directions clicks.
- Record the landing page, service, location, device, and campaign with every lead when the form system supports it.
- Use a call tracking number only if the provider can preserve Shiny's main number for local citations and Google Business Profile.

### 3. Local search

- Confirm the exact business name, main category, secondary categories, phone, hours, website, appointment URL, and service areas in Google Business Profile.
- Verify the Springfield, Alexandria, and Arlington addresses before showing all three as public locations.
- Keep name, address, and phone data consistent across Google, Bing, Apple Maps, Yelp, Facebook, BBB, Angi, Houzz, and major local directories.
- Add original crew, vehicle, equipment, and completed-work photos.
- Ask for reviews after completed jobs without offering incentives or filtering unhappy customers.
- Respond to every review with a short, specific answer.

### 4. Content and on-page work

- Build full pages for carpet, rug, upholstery, house, tile and grout, wood floor, mattress, pet stain and odor, window, power washing, water restoration, air duct, dryer vent, grout sealing, junk removal, carpet stretching, apartment, and commercial cleaning.
- Give each service page process details, inclusions, exclusions, preparation instructions, pricing factors, FAQs, real project photos, and a strong estimate action.
- Link relevant blog articles to their service page and link service pages back to useful articles.
- Review the imported blog archive for inaccurate advice, stale prices, weak sourcing, duplicate topics, and titles that say “2026” without a 2026 update.
- Merge overlapping articles rather than keeping several pages that answer the same search query.
- Add author and reviewer information only when a real person has reviewed the content.

### 5. Technical quality

- Compress the hero video and large gallery images, then test Core Web Vitals on mobile.
- Set long cache headers for versioned CSS, JavaScript, images, and video.
- Keep lazy loading below the fold and preload only the real largest content element.
- Validate structured data with Google's Rich Results Test and Schema.org Validator.
- Run a full crawl before launch and check status codes, canonical tags, headings, index rules, image alt text, orphan pages, and broken internal links.
- Test keyboard navigation, focus visibility, form labels, contrast, and reduced-motion behavior.

## Monthly SEO service

Complete this cycle every month and compare it with the previous month and the same month last year when enough history exists.

### Measurement and diagnosis

- Report organic clicks, impressions, average position, leads, booked appointments, phone calls, and conversion rate.
- Break performance down by service, location, landing page, device, and branded versus non-branded searches.
- Review Google Search Console indexing, page experience, manual actions, and query changes.
- Check Google Business Profile calls, website clicks, direction requests, photo views, and search terms.
- Identify the five largest gains, five largest losses, and the next actions for each.

### Content work

- Publish one useful article or substantial service-page addition based on actual query data and customer questions.
- Refresh at least two existing pages with better answers, photos, internal links, and verified facts.
- Improve one location page using real project details, neighborhood coverage, or customer questions from that area.
- Add internal links from new and high-authority pages to the service and location pages that need help.
- Remove, merge, redirect, or noindex content that competes with a stronger page for the same query.

### Local work

- Publish one Google Business Profile update using a real project, seasonal service, or verified offer.
- Add new real job photos with accurate captions.
- Respond to new reviews and flag reviews that violate platform rules.
- Check business hours, appointment links, service list, and contact information.
- Review citation accuracy quarterly and after any business information changes.

### Technical and conversion work

- Crawl the site for broken links, new 404s, accidental noindex tags, redirect chains, missing metadata, duplicate titles, and orphan pages.
- Test the estimate, contact, career, booking, phone, email, and directions actions.
- Review mobile Core Web Vitals and fix any page that moves into “poor.”
- Review form abandonment and the conversion rate of the top organic landing pages.
- Make one measurable conversion improvement when the data supports it.

### Monthly report deliverables

- One-page executive summary.
- Search and lead dashboard.
- Completed work with affected URLs.
- Problems found and fixed.
- Content published or refreshed.
- Prioritized work for the next month.

## Buttons and forms that still need production wiring

### Must connect before launch

1. **Homepage estimate form.** It currently validates in the browser and displays a placeholder success message. Send it to the approved CRM or form endpoint, add spam protection, and create an internal notification and customer confirmation.
2. **Contact form.** It currently displays a placeholder success message. Route it by topic or send it to the main customer service inbox and CRM.
3. **Career form.** It currently displays a placeholder success message and accepts a resume locally. Connect the file upload and application fields to the hiring destination.
4. **Form analytics.** Record successful submissions only after the server confirms delivery. Do not fire a conversion event on a button click alone.

### Already wired

- Header phone links use `tel:`.
- Email links use `mailto:`.
- Book online links open the existing Housecall Pro booking flow.
- Estimate links open the homepage estimate form.
- Navigation, footer, blog cards, gallery controls, blog filters, and mobile menus have destinations or local behavior.
- Homepage map markers link to their new service-area page.
- Location-page estimate, booking, service, phone, and nearby-area links are connected.
- Service cards intentionally flip on click to reveal their summary.

### Confirm before launch

- Confirm whether the three live-site addresses are active customer-facing locations.
- Confirm the final CRM or LeadConnector endpoints for the three forms.
- Confirm whether the privacy and terms pages will remain on WordPress or move into this rebuild.
- Confirm which promotions, packages, certifications, guarantees, awards, and social accounts are current.
- Confirm the analytics, Search Console, Tag Manager, and Google Business Profile account owners.
