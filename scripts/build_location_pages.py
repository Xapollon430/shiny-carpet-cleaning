#!/usr/bin/env python3
"""Build the location hub and local service-area pages."""

from __future__ import annotations

import html
import json
import os
import math
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE = os.environ.get("SITE_URL", "http://127.0.0.1:4173").rstrip("/")
BOOKING_URL = "https://book.housecallpro.com/book/Shiny-Carpet-Cleaning/66764a3c1a034ac0b96136517e678511"

LOCATIONS = [
    {"city": "Accokeek", "state": "MD", "lat": 38.6676, "lng": -77.0283, "setting": "homes near the Potomac, established neighborhoods, and busy family spaces"},
    {"city": "Aldie", "state": "VA", "lat": 38.9757, "lng": -77.6416, "setting": "newer communities, larger floor plans, and homes dealing with construction dust and daily foot traffic"},
    {"city": "Alexandria", "state": "VA", "lat": 38.8048, "lng": -77.0469, "setting": "historic homes, rowhouses, condos, apartments, and modern neighborhoods"},
    {"city": "Annandale", "state": "VA", "lat": 38.8304, "lng": -77.1964, "setting": "established homes, townhouses, apartments, and local businesses"},
    {"city": "Arlington", "state": "VA", "lat": 38.8816, "lng": -77.0910, "setting": "high-rise condos, apartments, townhouses, offices, and single-family homes"},
    {"city": "Ashburn", "state": "VA", "lat": 39.0438, "lng": -77.4874, "setting": "newer homes, large living spaces, active households, and pet-friendly communities"},
    {"city": "Bethesda", "state": "MD", "lat": 38.9847, "lng": -77.0947, "setting": "condos, established homes, renovated interiors, and professional offices"},
    {"city": "Bowie", "state": "MD", "lat": 39.0068, "lng": -76.7791, "setting": "family homes, townhouses, finished basements, and high-traffic living areas"},
    {"city": "Bristow", "state": "VA", "lat": 38.7226, "lng": -77.5361, "setting": "family homes, basements, pet households, and newer communities"},
    {"city": "Centreville", "state": "VA", "lat": 38.8404, "lng": -77.4289, "setting": "townhomes, single-family homes, apartments, and active family spaces"},
    {"city": "Chantilly", "state": "VA", "lat": 38.8943, "lng": -77.4311, "setting": "homes, offices, retail spaces, and interiors exposed to daily commuter traffic"},
    {"city": "Columbia", "state": "MD", "lat": 39.2037, "lng": -76.8610, "setting": "planned neighborhoods, townhomes, apartments, and commercial spaces"},
    {"city": "Dumfries", "state": "VA", "lat": 38.5676, "lng": -77.3280, "setting": "townhomes, family houses, apartments, and high-use rooms"},
    {"city": "Fairfax", "state": "VA", "lat": 38.8462, "lng": -77.3064, "setting": "single-family homes, townhouses, apartments, and professional spaces"},
    {"city": "Falls Church", "state": "VA", "lat": 38.8823, "lng": -77.1711, "setting": "older homes, renovated properties, condos, and compact city living"},
    {"city": "Gainesville", "state": "VA", "lat": 38.7957, "lng": -77.6139, "setting": "newer neighborhoods, larger family homes, basements, and pet households"},
    {"city": "Gaithersburg", "state": "MD", "lat": 39.1434, "lng": -77.2014, "setting": "townhomes, condos, single-family homes, and local workplaces"},
    {"city": "Germantown", "state": "MD", "lat": 39.1732, "lng": -77.2717, "setting": "apartments, townhouses, family homes, and busy shared spaces"},
    {"city": "Glen Burnie", "state": "MD", "lat": 39.1626, "lng": -76.6247, "setting": "established homes, apartments, townhouses, and neighborhood businesses"},
    {"city": "Indian Head", "state": "MD", "lat": 38.6001, "lng": -77.1622, "setting": "family homes, smaller communities, and rooms affected by outdoor moisture and daily use"},
    {"city": "Laurel", "state": "MD", "lat": 39.0993, "lng": -76.8483, "setting": "apartments, townhomes, single-family houses, and commercial properties"},
    {"city": "Leesburg", "state": "VA", "lat": 39.1157, "lng": -77.5636, "setting": "historic properties, newer communities, large homes, and local businesses"},
    {"city": "Manassas", "state": "VA", "lat": 38.7509, "lng": -77.4753, "setting": "older homes, townhouses, apartments, offices, and retail spaces"},
    {"city": "Potomac", "state": "MD", "lat": 39.0182, "lng": -77.2086, "setting": "larger homes, delicate rugs, finished basements, and high-use family rooms"},
    {"city": "Silver Spring", "state": "MD", "lat": 38.9907, "lng": -77.0261, "setting": "apartments, condos, townhomes, older houses, and busy commercial spaces"},
    {"city": "Springfield", "state": "VA", "lat": 38.7893, "lng": -77.1872, "setting": "family homes, townhouses, apartments, offices, and the neighborhoods around our Fullerton Road office"},
    {"city": "Stafford", "state": "VA", "lat": 38.4221, "lng": -77.4083, "setting": "family homes, finished basements, pet households, and high-traffic rooms"},
    {"city": "Upper Marlboro", "state": "MD", "lat": 38.8159, "lng": -76.7497, "setting": "single-family homes, townhouses, larger properties, and community spaces"},
    {"city": "Waldorf", "state": "MD", "lat": 38.6246, "lng": -76.9391, "setting": "family homes, townhouses, apartments, and well-used living spaces"},
    {"city": "Warrenton", "state": "VA", "lat": 38.7135, "lng": -77.7953, "setting": "historic homes, rural properties, newer neighborhoods, and local businesses"},
    {"city": "Washington", "state": "DC", "lat": 38.9072, "lng": -77.0369, "setting": "rowhouses, apartments, condos, offices, and properties with tight access or shared entryways"},
]

STATE_NAMES = {"VA": "Virginia", "MD": "Maryland", "DC": "Washington, DC"}

SERVICES = [
    ("Carpet cleaning", "Hot water extraction for traffic lanes, spots, and embedded soil.", "/assets/services/carpet-cleaning.webp"),
    ("Area rug cleaning", "Fiber-conscious care for everyday rugs and delicate materials.", "/assets/services/area-rug-cleaning.webp"),
    ("Upholstery cleaning", "Fabric-safe cleaning for sofas, chairs, sectionals, and other furniture.", "/assets/services/furniture-cleaning.webp"),
    ("Tile and grout cleaning", "Professional agitation and extraction for tile and porous grout lines.", "/assets/services/tile-grout.webp"),
    ("Pet stain and odor removal", "Targeted treatment that reaches the source of pet accidents.", "/assets/services/pet-stain-odor.webp"),
    ("House cleaning", "One-time and recurring help for kitchens, bathrooms, and living spaces.", "/assets/services/house-cleaning.webp"),
]


def slug(location: dict) -> str:
    return f"{location['city'].lower().replace(' ', '-')}-{location['state'].lower()}"


def distance(a: dict, b: dict) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 3959 * 2 * math.asin(math.sqrt(h))


def header(active: str = "") -> str:
    current = ' aria-current="page"' if active == "locations" else ""
    return f'''<header class="site-header inner-header" data-site-header><div class="nav-shell">
    <a class="site-logo" href="/" aria-label="Shiny Carpet Cleaning home"><img class="brand-logo invert" src="/assets/shiny-logo.png" alt="Shiny Carpet Cleaning"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span></span><span></span><span class="sr-only">Open navigation</span></button>
    <nav class="primary-nav" id="primary-nav" aria-label="Primary navigation"><a class="nav-link" href="/services/">Our services</a><div class="nav-company"><button class="nav-link company-trigger" type="button" aria-expanded="false">Company <svg viewBox="0 0 12 8" aria-hidden="true"><path d="m1 1 5 5 5-5"/></svg></button><div class="nav-dropdown"><a href="/about/">About us</a><a href="/locations/"{current}>Locations</a><a href="/careers/">Careers</a><a href="/blogs/">Blogs</a><a href="/reviews/">Reviews</a></div></div><a class="nav-link" href="/gallery/">Gallery</a><a class="nav-link" href="/contact/">Contact</a></nav>
    <a class="header-phone" href="tel:7039759099"><svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 26 26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg><span>(703) 975-9099</span></a>
  </div></header>'''


def footer() -> str:
    return f'''<footer class="site-footer" id="contact"><div class="footer-main"><div class="footer-brand"><img class="brand-logo invert" src="/assets/shiny-logo.png" alt="Shiny Carpet Cleaning"><p>Family-run cleaning and restoration services for homes across the Greater DC Metro Area.</p></div><div class="footer-column"><h2>Contact</h2><a href="https://maps.app.goo.gl/76dYgTyyS3PcNsuc6">7627B Fullerton Rd.<br>Suite B<br>Springfield, VA 22153</a><a href="tel:7039759099">(703) 975-9099</a><a href="mailto:info@shinycarpetcleaning.com">info@shinycarpetcleaning.com</a></div><div class="footer-column"><h2>Hours</h2><p>Monday–Saturday<br>8:00am–6:00pm</p><a href="{BOOKING_URL}">Book online</a><a href="/#form">Request an estimate</a></div><div class="footer-column"><h2>Company</h2><a href="/about/">About us</a><a href="/careers/">Careers</a><a href="/blogs/">Blogs</a><a href="/reviews/">Reviews</a><a href="/gallery/">Gallery</a><a href="/services/">Services</a><a href="/locations/">Locations</a><a href="/contact/">Contact</a></div></div><div class="footer-bottom"><span>© 2026 Shiny Carpet Cleaning. All rights reserved.</span></div></footer>'''


def service_cards() -> str:
    return "".join(
        f'''<a class="location-service-card reveal" href="/services/"><img src="{image}" alt="" loading="lazy"><span><strong>{name}</strong><small>{copy}</small></span></a>'''
        for name, copy, image in SERVICES
    )


def location_schema(location: dict, nearby: list[dict]) -> str:
    city, state, page_slug = location["city"], location["state"], slug(location)
    page_url = f"{SITE}/locations/{page_slug}/"
    faqs = [
        (f"Does Shiny Carpet Cleaning serve all of {city}?", f"We schedule cleaning throughout {city} and nearby communities. Share your street address when requesting an estimate so the team can confirm route availability for your property."),
        (f"What cleaning services are available in {city}?", "Service availability includes carpet, area rug, upholstery, tile and grout, pet stain and odor, house cleaning, and other specialty cleaning. The team will confirm the right service for your surfaces."),
        ("How do I get an estimate?", "Use the online estimate form or call (703) 975-9099. Include the service, property address, and rooms or items that need attention."),
        ("Can I book online?", "Yes. Online booking shows available appointment times. For unusual materials, water damage, or several services in one visit, request an estimate first."),
    ]
    graph = [
        {
            "@type": "Service",
            "@id": page_url + "#service",
            "name": f"Professional cleaning services in {city}, {state}",
            "serviceType": "Carpet and specialty cleaning",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": {"@type": "City", "name": f"{city}, {state}"},
            "url": page_url,
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Locations", "item": f"{SITE}/locations/"},
                {"@type": "ListItem", "position": 3, "name": f"{city}, {state}", "item": page_url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
                for question, answer in faqs
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def location_page(location: dict) -> str:
    city, state = location["city"], location["state"]
    page_slug = slug(location)
    state_name = STATE_NAMES[state]
    nearby = sorted((item for item in LOCATIONS if item is not location), key=lambda item: distance(location, item))[:5]
    nearby_links = "".join(f'<a href="/locations/{slug(item)}/">{item["city"]}, {item["state"]}<span>↗</span></a>' for item in nearby)
    office_note = "Shiny’s Springfield office is located on Fullerton Road." if city == "Springfield" else "Shiny routes local crews from the Springfield area throughout the DMV."
    title = f"Carpet Cleaning in {city}, {state} | Shiny Carpet Cleaning"
    description = f"Professional carpet, rug, upholstery, tile, and house cleaning in {city}, {state}. Request an estimate from Shiny Carpet Cleaning."
    schema = location_schema(location, nearby)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(description)}"><link rel="stylesheet" href="/assets/site.css?v=99"><script type="application/ld+json">{schema}</script></head>
<body class="inner-page location-page">
  <a class="skip" href="#main">Skip to content</a>
  {header("locations")}
  <main id="main">
    <section class="location-hero">
      <div class="location-hero-copy"><span class="eyebrow">Serving {html.escape(city)} and nearby communities</span><h1>Professional carpet cleaning in {html.escape(city)}, {state}</h1><p>Local cleaning for {html.escape(location['setting'])}. Tell us what needs attention and we’ll help you choose the right service.</p><div class="location-actions"><a class="cta location-estimate" href="/#form">Get an estimate <span aria-hidden="true">↗</span></a><a class="cta location-book" href="{BOOKING_URL}">Book online</a></div></div>
      <div class="location-hero-photo"><img src="/assets/about/real-carpet-cleaning-hero.webp" alt="Professional carpet cleaning in a residential home"></div>
    </section>
    <section class="location-intro"><div><span class="eyebrow">Local service, surface-specific care</span><h2>Cleaning help for homes and businesses across {html.escape(city)}.</h2></div><div><p>Shiny Carpet Cleaning has served the Greater DC area since 2006. Our crews match the cleaning method to the material, soil level, access, and way each room is used.</p><p>{html.escape(office_note)} Appointments in {html.escape(city)} are scheduled by route, so sharing your address and preferred timing helps us confirm availability.</p></div></section>
    <section class="location-services" aria-labelledby="location-services-title"><div class="location-section-heading"><span class="eyebrow">Services available</span><h2 id="location-services-title">Care for the surfaces you use every day.</h2><a href="/services/">View every service</a></div><div class="location-services-grid">{service_cards()}</div></section>
    <section class="location-faq"><div class="location-section-heading"><span class="eyebrow">Common questions</span><h2>Planning a cleaning in {html.escape(city)}.</h2></div><div class="location-faq-list"><details><summary>Do you serve all of {html.escape(city)}?</summary><p>We schedule cleaning throughout {html.escape(city)} and nearby communities. Share your street address when requesting an estimate so the team can confirm route availability for your property.</p></details><details><summary>What services are available?</summary><p>Service availability includes carpet, area rug, upholstery, tile and grout, pet stain and odor, house cleaning, and other specialty cleaning. The team will confirm the right service for your surfaces.</p></details><details><summary>How do I get an estimate?</summary><p>Use the online estimate form or call <a href="tel:7039759099">(703) 975-9099</a>. Include the service, property address, and rooms or items that need attention.</p></details><details><summary>Can I book online?</summary><p>Yes. Online booking shows available appointment times. For unusual materials, water damage, or several services in one visit, request an estimate first.</p></details></div></section>
    <section class="nearby-locations"><div><span class="eyebrow">Nearby service areas</span><h2>Cleaning across {html.escape(state_name)} and the DMV.</h2></div><div class="nearby-location-links">{nearby_links}<a href="/locations/">All service areas<span>↗</span></a></div></section>
  </main>
  {footer()}
  <script src="/assets/site.js?v=52"></script>
</body></html>'''


def hub_page() -> str:
    groups = []
    for state in ("VA", "MD", "DC"):
        cards = "".join(
            f'<a class="location-card reveal" href="/locations/{slug(item)}/"><span>{item["city"]}</span><small>{item["state"]}</small><b aria-hidden="true">↗</b></a>'
            for item in LOCATIONS if item["state"] == state
        )
        groups.append(f'<section class="location-state-group"><div><span class="eyebrow">{STATE_NAMES[state]}</span><h2>{"Virginia service areas" if state == "VA" else "Maryland service areas" if state == "MD" else "District of Columbia"}</h2></div><div class="location-state-content"><div class="location-card-grid">{cards}</div></div></section>')
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Shiny Carpet Cleaning service areas",
        "url": f"{SITE}/locations/",
        "about": {"@id": f"{SITE}/#business"},
        "hasPart": [{"@type": "WebPage", "name": f"{item['city']}, {item['state']}", "url": f"{SITE}/locations/{slug(item)}/"} for item in LOCATIONS],
    }, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Service Areas | Shiny Carpet Cleaning</title><meta name="description" content="Find Shiny Carpet Cleaning service areas across Northern Virginia, Maryland, and Washington, DC."><link rel="stylesheet" href="/assets/site.css?v=99"><script type="application/ld+json">{schema}</script></head>
<body class="inner-page locations-page"><a class="skip" href="#main">Skip to content</a>{header("locations")}<main id="main"><section class="inner-hero locations-hero"><h1>Our locations</h1></section><section class="locations-directory">{''.join(groups)}</section></main>{footer()}<script src="/assets/site.js?v=52"></script></body></html>'''


def write_redirects() -> None:
    """Preserve the location URLs used by the current WordPress site."""
    rows = []
    for location in LOCATIONS:
        city_slug = location["city"].lower().replace(" ", "-")
        if location["state"] == "VA":
            old = f"/locations/virginia/{city_slug}/"
        elif location["state"] == "MD":
            old = f"/locations/maryland/{city_slug}/"
        else:
            old = "/locations/washington-dc/"
        new = f"/locations/{slug(location)}/"
        if old != new:
            rows.append((old, new, "legacy WordPress location URL"))
    extras = [
        ("/carpet-cleaning-in-dc/", "/locations/washington-dc/", "legacy DC landing page"),
        ("/carpet-cleaning-in-montgomery-county-maryland/", "/locations/", "legacy county landing page"),
        ("/residential-and-commercial-carpet-cleaning-arlington-va/", "/locations/arlington-va/", "legacy Arlington landing page"),
        ("/carpet-cleaning/", "/services/", "legacy service page"),
        ("/area-rug-cleaning/", "/services/", "legacy service page"),
        ("/furniture-cleaning/", "/services/", "legacy service page"),
        ("/upholstery-cleaning-services/", "/services/", "legacy service page"),
        ("/pet-stain-odor-removing/", "/services/", "legacy service page"),
        ("/mattress-cleaning/", "/services/", "legacy service page"),
        ("/wood-floor-cleaning/", "/services/", "legacy service page"),
        ("/tile-and-grout-cleaning/", "/services/", "legacy service page"),
        ("/water-restoration-services/", "/services/", "legacy service page"),
        ("/commercial-carpet-cleaning-services/", "/services/", "legacy service page"),
        ("/residential-carpet-cleaning-services/", "/services/", "legacy service page"),
        ("/disinfection-service/", "/services/", "legacy service page"),
        ("/get-free-estimate/", "/#form", "legacy estimate page"),
        ("/2022-update-on-mattress-cleaning-cost-is-it-worth-it/", "/blogs/update-on-mattress-cleaning-cost-is-it-worth-it/", "legacy article page"),
    ]
    upholstery_cities = ["washington-dc", "springfield-va", "manassas-va", "falls-church-va", "fairfax-va", "chantilly-va", "bowie-md", "bethesda-md", "arlington-va", "annandale-va", "alexandria-va"]
    for name in upholstery_cities:
        extras.append((f"/furniture-and-upholstery-cleaning-in-{name}/", f"/locations/{name}/", "legacy service and city landing page"))
    rows.extend(extras)
    (DIST / "_redirects").write_text("\n".join(f"{old} {new} 301" for old, new, _ in rows) + "\n")
    seo_dir = ROOT / "seo"
    seo_dir.mkdir(exist_ok=True)
    csv = ["source,target,status,reason"] + [f'"{old}","{new}",301,"{reason}"' for old, new, reason in rows]
    (seo_dir / "redirects.csv").write_text("\n".join(csv) + "\n")


def main() -> None:
    base = DIST / "locations"
    base.mkdir(parents=True, exist_ok=True)
    location_slugs = {slug(item) for item in LOCATIONS}
    for directory in base.iterdir():
        if directory.is_dir() and directory.name not in location_slugs:
            shutil.rmtree(directory)
    (base / "index.html").write_text(hub_page())
    for location in LOCATIONS:
        directory = base / slug(location)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "index.html").write_text(location_page(location))
    write_redirects()
    print(f"Built {len(LOCATIONS)} location pages and the location directory.")


if __name__ == "__main__":
    main()
