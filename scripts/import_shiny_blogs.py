#!/usr/bin/env python3
"""Import the public Shiny WordPress archive into the static local site."""

from __future__ import annotations

import html
import io
import json
import re
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BLOG_ROOT = DIST / "blogs"
IMAGE_ROOT = DIST / "assets" / "blog" / "archive"
API = "https://shinycarpetcleaning.com/wp-json/wp/v2/posts?per_page=100&page={page}&_embed=1"
USER_AGENT = "Mozilla/5.0 Shiny static archive importer"
ALLOWED = {"p", "h2", "h3", "h4", "ul", "ol", "li", "strong", "b", "em", "i", "blockquote", "a", "br"}


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.load(response)


class ArticleSanitizer(HTMLParser):
    def __init__(self, local_slugs: set[str]):
        super().__init__(convert_charrefs=True)
        self.local_slugs = local_slugs
        self.out: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "iframe", "form", "noscript"}:
            self.skip_depth += 1
            return
        if self.skip_depth or tag not in ALLOWED:
            return
        if tag == "a":
            href = dict(attrs).get("href", "")
            match = re.match(r"https?://(?:www\.)?shinycarpetcleaning\.com/([^/?#]+)/?", href)
            if match and match.group(1) in self.local_slugs:
                href = f"/blogs/{match.group(1)}/"
            elif href.startswith("javascript:"):
                href = "#"
            self.out.append(f'<a href="{html.escape(href, quote=True)}">')
        elif tag == "br":
            self.out.append("<br>")
        else:
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "iframe", "form", "noscript"}:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if not self.skip_depth and tag in ALLOWED and tag != "br":
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip_depth:
            self.out.append(html.escape(data))

    def get_html(self):
        return re.sub(r"\s+", " ", "".join(self.out)).replace("> ", ">").replace(" </", "</").strip()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(value))).strip()


def post_terms(post: dict) -> tuple[str, str]:
    terms = post.get("_embedded", {}).get("wp:term", [])
    categories = next((group for group in terms if group and group[0].get("taxonomy") == "category"), [])
    category = next((item for item in categories if item.get("slug") != "uncategorized"), categories[0] if categories else None)
    return (category or {}).get("name", "Cleaning advice"), (category or {}).get("slug", "cleaning-advice")


def featured_url(post: dict) -> str | None:
    media = post.get("_embedded", {}).get("wp:featuredmedia", [])
    return media[0].get("source_url") if media else None


def download_image(post: dict) -> tuple[str, str | None]:
    slug = post["slug"]
    url = featured_url(post)
    if not url:
        return slug, None
    target = IMAGE_ROOT / f"{slug}.webp"
    if target.exists():
        return slug, f"/assets/blog/archive/{target.name}"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=35) as response:
            raw = response.read()
        with Image.open(io.BytesIO(raw)) as image:
            image = image.convert("RGB")
            image.thumbnail((1280, 900), Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=82, method=6)
        return slug, f"/assets/blog/archive/{target.name}"
    except Exception as exc:
        print(f"image skipped for {slug}: {exc}")
        return slug, None


HEADER = '''<header class="site-header inner-header is-scrolled" data-site-header><div class="nav-shell">
  <a class="site-logo" href="/" aria-label="Shiny Carpet Cleaning home"><img class="brand-logo invert" src="/assets/shiny-logo.png" alt="Shiny Carpet Cleaning"></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span></span><span></span><span class="sr-only">Open navigation</span></button>
  <nav class="primary-nav" id="primary-nav" aria-label="Primary navigation"><a class="nav-link" href="/services/">Our services</a><div class="nav-company"><button class="nav-link company-trigger" type="button" aria-expanded="false">Company <svg viewBox="0 0 12 8" aria-hidden="true"><path d="m1 1 5 5 5-5"/></svg></button><div class="nav-dropdown"><a href="/about/">About us</a><a href="/locations/">Locations</a><a href="/careers/">Careers</a><a href="/blogs/">Blogs</a></div></div><a class="nav-link" href="/gallery/">Gallery</a><a class="nav-link" href="/contact/">Contact</a></nav>
  <a class="header-phone" href="tel:7039759099"><svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 26 26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg><span>(703) 975-9099</span></a>
</div></header>'''

FOOTER = '''<footer class="site-footer" id="contact"><div class="footer-main">
  <div class="footer-brand"><img class="brand-logo invert" src="/assets/shiny-logo.png" alt="Shiny Carpet Cleaning"><p>Family-run cleaning and restoration services for homes across the Greater DC Metro Area.</p></div>
  <div class="footer-column"><h2>Contact</h2><a href="https://maps.app.goo.gl/76dYgTyyS3PcNsuc6">7627B Fullerton Rd.<br>Suite B<br>Springfield, VA 22153</a><a href="tel:7039759099">(703) 975-9099</a><a href="mailto:info@shinycarpetcleaning.com">info@shinycarpetcleaning.com</a></div>
  <div class="footer-column"><h2>Hours</h2><p>Monday–Saturday<br>8:00am–6:00pm</p><a href="https://book.housecallpro.com/book/Shiny-Carpet-Cleaning/66764a3c1a034ac0b96136517e678511">Book online</a><a href="/#form">Request an estimate</a></div>
  <div class="footer-column"><h2>Company</h2><a href="/about/">About us</a><a href="/careers/">Careers</a><a href="/blogs/">Blogs</a><a href="/gallery/">Gallery</a></div>
</div><div class="footer-bottom"><span>© 2026 Shiny Carpet Cleaning. All rights reserved.</span></div></footer>'''


def document(title: str, description: str, body: str, body_class: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — Shiny Carpet Cleaning</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="stylesheet" href="/assets/site.css?v=45"></head><body class="inner-page {body_class}">{HEADER}<main id="main">{body}</main>{FOOTER}<script src="/assets/site.js?v=45"></script></body></html>'''


def card(post: dict, image: str | None) -> str:
    title = clean_text(post["title"]["rendered"])
    name, slug = post_terms(post)
    date = datetime.fromisoformat(post["date"]).strftime("%b %d, %Y")
    iso = post["date"][:10]
    image = image or "/assets/services/carpet-cleaning.webp"
    url = f'/blogs/{post["slug"]}/'
    return f'''<article class="resource-card reveal" data-blog-card data-category="{html.escape(slug)}" data-date="{iso}"><a class="resource-image" href="{url}"><img src="{image}" alt="" loading="lazy"></a><div class="resource-copy"><div class="resource-meta"><span>{html.escape(name)}</span><time datetime="{iso}">{date}</time></div><h2><a href="{url}">{html.escape(title)}</a></h2></div></article>'''


def featured(post: dict, image: str | None, wide: bool) -> str:
    title = clean_text(post["title"]["rendered"])
    excerpt = clean_text(post["excerpt"]["rendered"])
    name, _ = post_terms(post)
    iso = post["date"][:10]
    date = datetime.fromisoformat(post["date"]).strftime("%b %d, %Y")
    image = image or "/assets/services/carpet-cleaning.webp"
    cls = " featured-wide" if wide else ""
    return f'''<a class="featured-story{cls}" href="/blogs/{post['slug']}/"><div class="featured-image"><img src="{image}" alt="" loading="eager"></div><div class="featured-copy"><div class="featured-meta"><span>{html.escape(name)}</span><time datetime="{iso}">{date}</time></div><h2>{html.escape(title)}</h2><p>{html.escape(excerpt[:220])}</p><b>Read article <i>↗</i></b></div></a>'''


def main():
    posts = []
    page = 1
    while True:
        batch = fetch_json(API.format(page=page))
        posts.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    posts.sort(key=lambda post: post["date"], reverse=True)
    IMAGE_ROOT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=10) as pool:
        images = dict(pool.map(download_image, posts))

    categories: dict[str, str] = {}
    for post in posts:
        name, slug = post_terms(post)
        categories.setdefault(slug, name)

    filter_options = ''.join(f'<option value="{html.escape(slug)}">{html.escape(name)}</option>' for slug, name in categories.items())
    filter_buttons = ''.join(f'<button type="button" data-blog-filter="{html.escape(slug)}" aria-pressed="false">{html.escape(name)}</button>' for slug, name in categories.items())
    body = f'''<section class="learn-hero"><div class="learn-hero-copy"><h1>Check out our blogs</h1></div></section>
<section class="resources-section" id="resources"><div class="mobile-blog-filters"><label><span class="sr-only">Filter articles by topic</span><select data-blog-filter-select><option value="all">All topics</option>{filter_options}</select></label><label><span class="sr-only">Sort articles</span><select data-blog-sort-select><option value="newest">Newest first</option><option value="oldest">Oldest first</option></select></label></div><div class="resources-layout"><aside class="blog-filter-panel" aria-label="Filter articles"><div class="filter-group"><span class="filter-label">Sort by</span><button class="is-active" type="button" data-blog-sort="newest" aria-pressed="true">Newest</button><button type="button" data-blog-sort="oldest" aria-pressed="false">Oldest</button></div><div class="filter-group"><span class="filter-label">Topic</span><button class="is-active" type="button" data-blog-filter="all" aria-pressed="true">All</button>{filter_buttons}</div></aside><div class="resource-grid" data-blog-grid>{''.join(card(post, images.get(post['slug'])) for post in posts)}</div></div></section>'''
    (BLOG_ROOT / "index.html").write_text(document("Cleaning Guides & Advice", "Practical cleaning guides, cost explainers, and home-care advice from Shiny Carpet Cleaning.", body, "blog-page"))

    slugs = {post["slug"] for post in posts}
    for post in posts:
        title = clean_text(post["title"]["rendered"])
        excerpt = clean_text(post["excerpt"]["rendered"])
        name, _ = post_terms(post)
        iso = post["date"][:10]
        date = datetime.fromisoformat(post["date"]).strftime("%B %d, %Y")
        sanitizer = ArticleSanitizer(slugs)
        sanitizer.feed(post["content"]["rendered"])
        hero_image = images.get(post["slug"])
        media = f'<img class="article-hero-image" src="{hero_image}" alt="" loading="eager">' if hero_image else ""
        article = f'''<article class="article-page"><header class="article-hero"><a class="article-back" href="/blogs/">← All articles</a><span>{html.escape(name)}</span><h1>{html.escape(title)}</h1><time datetime="{iso}">{date}</time>{media}</header><div class="article-layout"><div class="article-content">{sanitizer.get_html()}</div><aside class="article-aside"><strong>Need a professional clean?</strong><p>Tell us what needs attention and get a free estimate from the Shiny team.</p><a href="/#form">Get estimate ↗</a></aside></div></article>'''
        target = BLOG_ROOT / post["slug"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(document(title, excerpt[:155], article, "article-body"))

    print(f"Imported {len(posts)} posts across {len(categories)} categories")


if __name__ == "__main__":
    main()
