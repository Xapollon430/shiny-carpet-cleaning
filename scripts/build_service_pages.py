#!/usr/bin/env python3
"""Build ad-ready service landing pages and refresh shared brand controls."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BOOK_URL = "https://book.housecallpro.com/book/Shiny-Carpet-Cleaning/66764a3c1a034ac0b96136517e678511"
PHONE_DISPLAY = "(703) 975-9099"
PHONE_LINK = "7039759099"


SERVICES = [
    {
        "slug": "house-cleaning",
        "name": "House cleaning",
        "image": "house-cleaning.webp",
        "hero": "Professional house cleaning across the DMV",
        "summary": "Reliable one-time and recurring cleaning for kitchens, bathrooms, bedrooms, and shared living spaces.",
        "details": "We build the visit around the rooms and surfaces that need attention, then work methodically through the home with products selected for the material at hand.",
        "benefits": ["One-time or recurring visits", "Room-by-room attention", "Clear scheduling and communication"],
    },
    {
        "slug": "carpet-cleaning",
        "name": "Carpet cleaning",
        "image": "carpet-cleaning.webp",
        "hero": "Professional carpet cleaning across the DMV",
        "summary": "Deep carpet cleaning that lifts embedded soil, allergens, spots, and residue while treating fibers with care.",
        "details": "Our technicians inspect the carpet, identify problem areas, pre-treat spots, and use professional extraction equipment to refresh high-traffic rooms and everyday living areas.",
        "benefits": ["Deep soil and spot removal", "Family and pet conscious products", "Professional hot water extraction"],
    },
    {
        "slug": "furniture-cleaning",
        "name": "Furniture cleaning",
        "image": "furniture-cleaning.webp",
        "hero": "Professional furniture cleaning across the DMV",
        "summary": "Fabric-conscious upholstery cleaning for sofas, sectionals, dining chairs, and other frequently used furniture.",
        "details": "We evaluate the fabric and condition before cleaning, then select a process designed to release soil, spots, and trapped odors without unnecessary saturation.",
        "benefits": ["Fabric-specific treatment", "Spot and soil removal", "Care for sofas, chairs, and sectionals"],
    },
    {
        "slug": "area-rug-cleaning",
        "name": "Area rug cleaning",
        "image": "area-rug-cleaning.webp",
        "hero": "Professional area rug cleaning across the DMV",
        "summary": "Fiber-conscious care that removes soil and odor while protecting the color, texture, and construction of your rugs.",
        "details": "Every rug begins with an inspection. We account for fiber type, backing, dyes, fringe, wear, and the stains that need attention before choosing a cleaning approach.",
        "benefits": ["Fiber and dye inspection", "Targeted stain treatment", "Careful cleaning for everyday and delicate rugs"],
    },
    {
        "slug": "mattress-cleaning",
        "name": "Mattress cleaning",
        "image": "mattress-cleaning.webp",
        "hero": "Professional mattress cleaning across the DMV",
        "summary": "Deep surface cleaning that helps remove dust, body oils, allergens, spots, and lingering odors.",
        "details": "Our mattress service focuses on the areas that collect everyday buildup while using controlled moisture and professional extraction appropriate for the material.",
        "benefits": ["Dust and allergen removal", "Spot and odor treatment", "Controlled-moisture cleaning"],
    },
    {
        "slug": "pet-stain-odor-removal",
        "name": "Pet stain and odor removal",
        "image": "pet-stain-odor.webp",
        "hero": "Pet stain and odor removal across the DMV",
        "summary": "Targeted treatment that addresses the source of pet accidents instead of covering odor with fragrance.",
        "details": "We inspect the affected carpet or upholstery, locate the areas that need treatment, and apply a process designed to break down contamination before extraction.",
        "benefits": ["Source-focused odor treatment", "Targeted stain care", "Available for carpets and upholstery"],
    },
    {
        "slug": "tile-grout-cleaning",
        "name": "Tile and grout cleaning",
        "image": "tile-grout.webp",
        "hero": "Professional tile and grout cleaning across the DMV",
        "summary": "Professional agitation and extraction for tile surfaces and porous grout lines in kitchens, bathrooms, and living areas.",
        "details": "We loosen embedded soil from the tile and grout, then use professional extraction to remove suspended grime and reveal a cleaner, more consistent finish.",
        "benefits": ["Deep grout-line cleaning", "Professional agitation and extraction", "Care for kitchens, bathrooms, and floors"],
    },
    {
        "slug": "wood-floor-services",
        "name": "Wood floor services",
        "image": "wood-floor.webp",
        "hero": "Professional wood floor cleaning across the DMV",
        "summary": "A dust-conscious cleaning process that removes residue and restores clarity to finished wood surfaces without sanding.",
        "details": "We inspect the finish, identify buildup and traffic patterns, and choose products and equipment intended for the floor’s existing protective coating.",
        "benefits": ["No-sanding maintenance option", "Residue and soil removal", "Process selected for finished wood"],
    },
    {
        "slug": "residential-carpet-cleaning",
        "name": "Residential carpet cleaning",
        "image": "residential-carpet.webp",
        "hero": "Residential carpet cleaning for DMV homes",
        "summary": "Whole-home carpet care tailored to fiber type, traffic levels, spots, pets, and the way your household uses each room.",
        "details": "From bedrooms and stairs to high-traffic family rooms, we plan the service around your home and use professional equipment to deliver a consistent clean.",
        "benefits": ["Whole-home service planning", "Traffic-lane and spot treatment", "Care tailored to active households"],
    },
    {
        "slug": "power-washing",
        "name": "Power washing",
        "image": "power-washing.webp",
        "hero": "Professional power washing across the DMV",
        "summary": "Controlled exterior cleaning for siding, patios, walkways, driveways, and other durable outdoor surfaces.",
        "details": "We match pressure and cleaning methods to the surface, working to remove dirt and organic buildup while avoiding unnecessary force.",
        "benefits": ["Surface-appropriate pressure", "Exterior dirt and buildup removal", "Service for homes and businesses"],
    },
    {
        "slug": "window-cleaning",
        "name": "Window cleaning",
        "image": "window-cleaning.webp",
        "hero": "Professional window cleaning across the DMV",
        "summary": "Interior and exterior glass cleaning that removes film, fingerprints, dust, and streaks for a clearer finish.",
        "details": "We clean the glass and focus on the buildup that interrupts natural light, with service options based on access and the condition of the windows.",
        "benefits": ["Interior and exterior options", "Film and streak removal", "Residential and commercial service"],
    },
    {
        "slug": "water-restoration",
        "name": "Water restoration",
        "image": "water-restoration.webp",
        "hero": "Water damage restoration across the DMV",
        "summary": "Rapid extraction and structural drying support after leaks, appliance failures, flooding, and other water emergencies.",
        "details": "Fast action helps limit secondary damage. We assess the affected areas, remove standing water where possible, and establish a drying plan for the property.",
        "benefits": ["Fast water extraction", "Professional drying equipment", "Clear assessment of affected areas"],
    },
]


def header_markup() -> str:
    return f'''<header class="site-header inner-header" data-site-header><div class="nav-shell">
    <a class="site-logo" href="/" aria-label="Shiny Carpet Cleaning home"><img class="brand-logo" src="/assets/brand/shiny-logo-full-reversed.svg" alt="Shiny Carpet Cleaning"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span></span><span></span><span class="sr-only">Open navigation</span></button>
    <nav class="primary-nav" id="primary-nav" aria-label="Primary navigation"><a class="nav-link" href="/services/">Our services</a><div class="nav-company"><button class="nav-link company-trigger" type="button" aria-expanded="false">Company <svg viewBox="0 0 12 8" aria-hidden="true"><path d="m1 1 5 5 5-5"/></svg></button><div class="nav-dropdown"><a href="/about/">About us</a><a href="/locations/">Service areas</a><a href="/careers/">Careers</a><a href="/blogs/">Blogs</a><a href="/reviews/">Reviews</a></div></div><a class="nav-link" href="/gallery/">Gallery</a><a class="nav-link" href="/contact/">Contact</a></nav>
    {actions_markup()}
  </div></header>'''


def actions_markup() -> str:
    return f'''<div class="header-actions" aria-label="Quick actions"><a class="header-action header-call" href="tel:{PHONE_LINK}"><span>Call now</span><strong>{PHONE_DISPLAY}</strong></a><a class="header-action header-book" href="{BOOK_URL}"><span>Book now</span></a></div>'''


def footer_markup() -> str:
    return f'''<footer class="site-footer" id="contact"><div class="footer-main"><div class="footer-brand"><img class="brand-logo footer-logo-horizontal" src="/assets/brand/shiny-logo-horizontal-reversed.svg" alt="Shiny Carpet Cleaning"><p>Family-run cleaning and restoration services for homes across the Greater DC Metro Area.</p></div><div class="footer-column"><h2>Contact</h2><a href="https://www.google.com/maps/search/?api=1&amp;query=7202+Lockport+Pl%2C+Lorton%2C+VA+22079">7202 Lockport Pl<br>Lorton, VA 22079</a><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a><a href="mailto:info@shinycarpetcleaning.com">info@shinycarpetcleaning.com</a></div><div class="footer-column"><h2>Hours</h2><p>Monday–Saturday<br>8:00am–6:00pm</p><a href="{BOOK_URL}">Book online</a><a href="/#form">Request an estimate</a></div><div class="footer-column"><h2>Company</h2><a href="/about/">About us</a><a href="/careers/">Careers</a><a href="/blogs/">Blogs</a><a href="/reviews/">Reviews</a><a href="/gallery/">Gallery</a><a href="/services/">Services</a><a href="/locations/">Service areas</a><a href="/contact/">Contact</a></div></div><div class="footer-bottom"><span class="footer-copyright"><img class="footer-symbol" src="/assets/brand/shiny-symbol.svg" alt="" aria-hidden="true"><span>© 2026 Shiny Carpet Cleaning. All rights reserved.</span></span></div></footer>'''


def service_page(service: dict) -> str:
    title = f"{service['name']} in the DMV — Shiny Carpet Cleaning"
    description = service["summary"]
    canonical = f"https://shiny-carpet-cleaning-va.netlify.app/services/{service['slug']}/"
    structured = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service["name"],
        "description": description,
        "provider": {"@type": "LocalBusiness", "name": "Shiny Carpet Cleaning", "telephone": "+1-703-975-9099"},
        "areaServed": ["Washington, DC", "Northern Virginia", "Maryland"],
        "url": canonical,
    }
    benefits = "".join(f"<li>{html.escape(item)}</li>" for item in service["benefits"])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(description)}"><link rel="stylesheet" href="/assets/site.css?v=125"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="website"><meta property="og:site_name" content="Shiny Carpet Cleaning"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://shiny-carpet-cleaning-va.netlify.app/assets/services/{service['image']}"><meta name="theme-color" content="#213B5C"><link rel="icon" href="/assets/shiny-favicon.png?v=1" type="image/png"><script type="application/ld+json">{json.dumps(structured)}</script></head>
<body class="inner-page service-detail-page">
  <a class="skip" href="#main">Skip to content</a>
  {header_markup()}
  <main id="main">
    <section class="service-landing-hero">
      <div class="service-landing-copy"><span class="eyebrow">Serving Northern Virginia, Maryland, and DC</span><h1>{html.escape(service['hero'])}</h1><p>{html.escape(service['summary'])}</p><ul class="service-trust-list">{benefits}</ul><div class="service-hero-actions"><a class="cta brand-primary" href="{BOOK_URL}">Book now</a><a class="cta brand-secondary" href="tel:{PHONE_LINK}">Call {PHONE_DISPLAY}</a></div></div>
      <div class="service-landing-photo"><img src="/assets/services/{service['image']}" alt="{html.escape(service['name'])} by Shiny Carpet Cleaning"></div>
    </section>
    <section class="service-overview"><div><span class="eyebrow">Professional care</span><h2>A clear plan for a deeper clean.</h2></div><div><p>{html.escape(service['details'])}</p><p>Tell us about the property, the surfaces, and any spots or concerns. We will help confirm the right service and schedule.</p></div></section>
  </main>
  {footer_markup()}
  <script src="/assets/site.js?v=55"></script>
</body></html>'''


def refresh_shared_headers():
    header_phone = re.compile(r'<a class="header-phone".*?</a>', re.S)
    logo = re.compile(r'<img class="brand-logo invert" src="[^\"]*shiny-logo\.png" alt="Shiny Carpet Cleaning">')
    for path in DIST.rglob("*.html"):
        if "/services/" in path.as_posix() and path.parent.name in {s["slug"] for s in SERVICES}:
            continue
        text = path.read_text()
        changed = logo.sub('<img class="brand-logo" src="/assets/brand/shiny-logo-full-reversed.svg" alt="Shiny Carpet Cleaning">', text)
        changed = header_phone.sub(actions_markup(), changed)
        changed = re.sub(r'/assets/site\.css\?v=\d+', '/assets/site.css?v=125', changed)
        changed = changed.replace('/assets/site.js?v=54', '/assets/site.js?v=55')
        if changed != text:
            path.write_text(changed)


def link_service_cards(path: Path):
    text = path.read_text()
    blocks = list(re.finditer(r'<button class="service-card reveal".*?</button>', text, re.S))
    if not blocks and text.count('<a class="service-card reveal"') == len(SERVICES):
        return
    if len(blocks) != len(SERVICES):
        raise RuntimeError(f"Expected {len(SERVICES)} service cards in {path}, found {len(blocks)}")
    pieces = []
    cursor = 0
    for match, service in zip(blocks, SERVICES):
        pieces.append(text[cursor:match.start()])
        block = match.group(0)
        block = re.sub(r'<button class="service-card reveal" type="button" aria-pressed="false"', f'<a class="service-card reveal" href="/services/{service["slug"]}/"', block, count=1)
        block = block[:-9] + '</a>'
        block = block.replace('Tap to close', 'Learn more')
        pieces.append(block)
        cursor = match.end()
    pieces.append(text[cursor:])
    path.write_text(''.join(pieces))


def refresh_sitemap():
    path = DIST / "sitemap.xml"
    text = path.read_text()
    rows = "\n".join(
        f'  <url><loc>https://shiny-carpet-cleaning-va.netlify.app/services/{service["slug"]}/</loc><lastmod>2026-10-08</lastmod><priority>0.9</priority></url>'
        for service in SERVICES
    )
    text = re.sub(
        r'\n  <url><loc>https://shiny-carpet-cleaning-va\.netlify\.app/services/(?!</loc>).*?</url>',
        '',
        text,
    )
    text = text.replace('\n</urlset>', f'\n{rows}\n</urlset>')
    path.write_text(text)


def main():
    refresh_shared_headers()
    for service in SERVICES:
        destination = DIST / "services" / service["slug"] / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(service_page(service))
    for page in (DIST / "index.html", DIST / "services" / "index.html"):
        link_service_cards(page)
    refresh_sitemap()


if __name__ == "__main__":
    main()
