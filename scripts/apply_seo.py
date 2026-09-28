#!/usr/bin/env python3
"""Apply shared SEO metadata and rebuild crawl files for the static site."""

from __future__ import annotations

import html
import json
import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE = os.environ.get("SITE_URL", "http://127.0.0.1:4173").rstrip("/")
DEFAULT_IMAGE = f"{SITE}/assets/about/real-carpet-cleaning-hero.webp"
TODAY = date.today().isoformat()
HOME_FAQS = [
    (
        "How long does it take carpets to dry after professional cleaning?",
        "Most carpets feel dry in 2 to 4 hours and reach a complete dry in about 6 to 8 hours. Airflow, humidity, and carpet thickness can affect the timing.",
    ),
    (
        "What should I do before the cleaning team arrives?",
        "Please remove small and fragile items from the rooms being cleaned. The Shiny team can handle the larger furniture that needs to be moved for the service.",
    ),
    (
        "Are your cleaning products safe for pets?",
        "Yes. Shiny uses eco-friendly cleaning products that are safe for pets.",
    ),
    (
        "How often should carpets be professionally cleaned?",
        "Shiny recommends professional carpet cleaning every 6 to 12 months. Homes with pets or heavy foot traffic may need service more often.",
    ),
]


def route_for(path: Path) -> str:
    relative = path.relative_to(DIST).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[: -len("index.html")]
    return "/" + relative


def text_value(source: str, pattern: str, fallback: str) -> str:
    match = re.search(pattern, source, re.I | re.S)
    if not match:
        return fallback
    value = re.sub(r"<[^>]+>", " ", match.group(1))
    return " ".join(html.unescape(value).split())


def absolute_asset(src: str | None) -> str:
    if not src:
        return DEFAULT_IMAGE
    if src.startswith("http"):
        return src
    return SITE + "/" + src.lstrip("/")


def meta_block(title: str, description: str, url: str, image: str, page_type: str) -> str:
    esc = html.escape
    return f'''<!-- SEO:META -->
  <link rel="canonical" href="{esc(url)}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta property="og:locale" content="en_US">
  <meta property="og:type" content="{page_type}">
  <meta property="og:site_name" content="Shiny Carpet Cleaning">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{esc(image)}">
  <meta property="og:image:alt" content="Shiny Carpet Cleaning professional cleaning service">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{esc(image)}">
  <meta name="theme-color" content="#07131f">
  <link rel="icon" href="/assets/shiny-favicon.png?v=1" type="image/png">
<!-- /SEO:META -->'''


def breadcrumb_schema(route: str, title: str) -> dict:
    parts = [part for part in route.strip("/").split("/") if part]
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    if route.startswith("/blogs/") and route != "/blogs/":
        items.append({"@type": "ListItem", "position": 2, "name": "Cleaning guides", "item": SITE + "/blogs/"})
        items.append({"@type": "ListItem", "position": 3, "name": title.replace(" — Shiny Carpet Cleaning", ""), "item": SITE + route})
    elif parts:
        items.append({"@type": "ListItem", "position": 2, "name": title.replace(" — Shiny Carpet Cleaning", "").replace(" | Shiny Carpet Cleaning", ""), "item": SITE + route})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def structured_block(path: Path, source: str, route: str, title: str, description: str, image: str) -> str:
    if route.startswith("/locations/"):
        return ""
    graph: list[dict] = []
    if route == "/":
        graph.extend([
            {
                "@type": ["LocalBusiness", "ProfessionalService"],
                "@id": SITE + "/#business",
                "name": "Shiny Carpet Cleaning",
                "url": SITE + "/",
                "logo": SITE + "/assets/shiny-logo.png",
                "image": image,
                "telephone": "+1-703-975-9099",
                "email": "info@shinycarpetcleaning.com",
                "priceRange": "$$",
                "foundingDate": "2006",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "7627B Fullerton Rd., Suite B",
                    "addressLocality": "Springfield",
                    "addressRegion": "VA",
                    "postalCode": "22153",
                    "addressCountry": "US",
                },
                "geo": {"@type": "GeoCoordinates", "latitude": 38.7893, "longitude": -77.1872},
                "openingHoursSpecification": [{
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "opens": "08:00",
                    "closes": "18:00",
                }],
                "areaServed": ["Washington, DC", "Northern Virginia", "Maryland"],
                "contactPoint": {"@type": "ContactPoint", "telephone": "+1-703-975-9099", "contactType": "customer service"},
            },
            {"@type": "WebSite", "@id": SITE + "/#website", "name": "Shiny Carpet Cleaning", "url": SITE + "/", "publisher": {"@id": SITE + "/#business"}},
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in HOME_FAQS
                ],
            },
        ])
    else:
        graph.append(breadcrumb_schema(route, title))
    if "article-body" in source:
        published = text_value(source, r'<time[^>]+datetime=["\']([^"\']+)', "")
        graph.append({
            "@type": "BlogPosting",
            "headline": title.replace(" — Shiny Carpet Cleaning", ""),
            "description": description,
            "datePublished": published,
            "dateModified": published,
            "mainEntityOfPage": SITE + route,
            "image": image,
            "author": {"@type": "Organization", "name": "Shiny Carpet Cleaning"},
            "publisher": {"@id": SITE + "/#business"},
        })
    if not graph:
        return ""
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<!-- SEO:STRUCTURED --><script type="application/ld+json">{payload}</script><!-- /SEO:STRUCTURED -->'


def apply_to_page(path: Path) -> None:
    source = path.read_text()
    route = route_for(path)
    title = text_value(source, r"<title>(.*?)</title>", "Shiny Carpet Cleaning")
    if "article-body" in source:
        title = text_value(source, r"<h1[^>]*>(.*?)</h1>", title.replace(" — Shiny Carpet Cleaning", ""))
        source = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", source, count=1, flags=re.I | re.S)
    description = text_value(source, r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', "Professional cleaning services across DC, Maryland, and Virginia.")
    hero_match = re.search(r'class=["\'][^"\']*(?:article-hero-image|about-hero-image)[^"\']*["\'][^>]+src=["\']([^"\']+)', source, re.I)
    image = absolute_asset(hero_match.group(1) if hero_match else None)
    url = SITE + route
    page_type = "article" if "article-body" in source else "website"
    source = re.sub(r'\s*<!-- SEO:META -->.*?<!-- /SEO:META -->', '', source, flags=re.S)
    source = re.sub(r'\s*<!-- SEO:STRUCTURED -->.*?<!-- /SEO:STRUCTURED -->', '', source, flags=re.S)
    meta = meta_block(title, description, url, image, page_type)
    structured = structured_block(path, source, route, title, description, image)
    source = source.replace("</head>", f"{meta}{structured}</head>", 1)
    path.write_text(source)


def write_sitemap(paths: list[Path]) -> None:
    rows = []
    for path in sorted(paths, key=route_for):
        route = route_for(path)
        if route == "/404.html":
            continue
        source = path.read_text(errors="ignore")
        published_match = re.search(r'<time[^>]+datetime=["\'](\d{4}-\d{2}-\d{2})', source, re.I)
        lastmod = published_match.group(1) if "article-body" in source and published_match else TODAY
        priority = "1.0" if route == "/" else "0.9" if route in ("/services/", "/locations/", "/contact/") else "0.8" if route.startswith("/locations/") else "0.6" if route.startswith("/blogs/") else "0.7"
        rows.append(f"  <url><loc>{SITE}{route}</loc><lastmod>{lastmod}</lastmod><priority>{priority}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    (DIST / "sitemap.xml").write_text(xml)


def write_robots() -> None:
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def main() -> None:
    pages = list(DIST.rglob("*.html"))
    for page in pages:
        if page.name == "404.html":
            continue
        apply_to_page(page)
    write_sitemap(pages)
    write_robots()
    print(f"Applied SEO metadata to {len(pages)} pages and rebuilt sitemap.xml and robots.txt.")


if __name__ == "__main__":
    main()
