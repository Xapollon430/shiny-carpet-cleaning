#!/usr/bin/env python3
"""Build preserved legacy pages and compile the reviewed URL migration rules."""
from __future__ import annotations
import csv
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'

def main():
    pages = json.loads((ROOT / 'seo/legacy-pages.json').read_text())
    rules = list(csv.DictReader((ROOT / 'seo/redirects.csv').open()))
    mapping = {r['source']: r for r in rules}
    assert len(mapping) == len(rules), 'Duplicate migration source'
    template = (DIST / 'about/index.html').read_text()
    header = re.search(r'<header\b.*?</header>', template, re.S).group()
    footer = re.search(r'<footer\b.*?</footer>', template, re.S).group()
    def document(title, description, body, noindex=False):
        return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — Shiny Carpet Cleaning</title><meta name="description" content="{html.escape(description,quote=True)}">{'<meta name="robots" content="noindex,follow">' if noindex else ''}<link rel="stylesheet" href="/assets/site.css?v=190"></head><body class="inner-page migration-page"><a class="skip" href="#main">Skip to content</a>{header}<main id="main"><section class="migration-content"><h1>{html.escape(title)}</h1><div class="migration-prose">{body}</div></section></main>{footer}<script src="/assets/site.js?v=55"></script></body></html>'''
    for page in pages:
        target = DIST / page['route'].strip('/') / 'index.html'
        target.parent.mkdir(parents=True,exist_ok=True)
        body = page['body']
        if page.get('type') == 'service':
            body += '<div class="service-hero-actions"><a class="cta brand-primary" href="/#form">Request an estimate</a><a class="cta brand-secondary" href="tel:7039759099">Call now</a></div>'
        target.write_text(document(page['title'],page['description'],body))
    (DIST / 'retired.html').write_text(document('This page is no longer available','Find current cleaning services and request an estimate.','<p>This page is no longer available.</p><p>For current services, availability and pricing, <a href="/#form">request an estimate</a> or <a href="/services/">browse our services</a>.</p>',True))
    # Link the restored specialty pages without changing the main twelve-card grid.
    target = DIST / 'services/index.html'
    source = re.sub(r'\s*<!-- MIGRATION:SERVICES -->.*?<!-- /MIGRATION:SERVICES -->','',target.read_text(),flags=re.S)
    links = ''.join(f'<li><a href="{p["route"]}">{html.escape(p["title"])}</a></li>' for p in pages if p.get('type') == 'service')
    source = source.replace('</main>',f'<!-- MIGRATION:SERVICES --><section class="migration-additional"><h2>Additional services</h2><ul>{links}</ul></section><!-- /MIGRATION:SERVICES --></main>')
    target.write_text(source)
    # Keep published internal links on their final local destination rather than the old host.
    for path in DIST.rglob('*.html'):
        source = path.read_text()
        def rewrite(match):
            href=html.unescape(match.group(2)); u=urlsplit(href)
            if u.netloc and u.netloc not in ('shinycarpetcleaning.com','www.shinycarpetcleaning.com','shiny-carpet-cleaning.exe.xyz'): return match.group()
            if not u.netloc and not href.startswith('/'): return match.group()
            route=u.path or '/'; rule=mapping.get(route)
            if rule and int(rule['status']) == 301: result=rule['target']
            elif (DIST / route.strip('/') / 'index.html').exists(): result=route
            else: return match.group()
            target=urlsplit(result)
            query='&'.join(part for part in (target.query,u.query) if part)
            result=urlunsplit((target.scheme,target.netloc,target.path,query,target.fragment or u.fragment))
            return 'href='+match.group(1)+html.escape(result,quote=True)+match.group(1)
        # Articles can contain old relative routes as well as absolute links.
        def retire_link(match):
            href=html.unescape(match.group(2)); u=urlsplit(href)
            if u.netloc and u.netloc not in ('shinycarpetcleaning.com','www.shinycarpetcleaning.com','shiny-carpet-cleaning.exe.xyz'):
                return match.group()
            rule=mapping.get(u.path)
            return match.group(3) if rule and int(rule['status']) == 410 else match.group()
        source=re.sub(r'<a\b[^>]*href=(["\'])([^"\']*)\1[^>]*>(.*?)</a>',retire_link,source,flags=re.S)
        source=re.sub(r'href=(["\'])([^"\']*)\1',rewrite,source)
        if 'footer-policy-links' not in source:
            source=source.replace('</div></footer>','<span class="footer-policy-links"><a href="/pricing/">Pricing</a><a href="/privacy-policy/">Privacy</a><a href="/terms-and-conditions/">Terms</a></span></div></footer>')
        source=re.sub(r'/assets/site\.css\?v=\d+','/assets/site.css?v=190',source)
        path.write_text(source)
    for rule in rules:
        status=int(rule['status']); assert status in (301,410), rule
        if status == 301 and rule['target'].startswith('/'):
            route=urlsplit(rule['target']).path
            assert route not in mapping, f'Redirect chain: {rule}'
            assert (DIST / route.strip('/') / 'index.html').exists(), f'Missing target: {rule}'
    (DIST / '_redirects').write_text(''.join(f"{r['source']} {r['target']} {r['status']}\n" for r in rules))
    print(f'Built {len(pages)} preserved pages and {len(rules)} reviewed URL rules.')

if __name__ == '__main__': main()
