#!/usr/bin/env python3
"""Check indexable generated pages for regressions found in the SEO audit."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import argparse

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals, self.descriptions, self.h1 = [], [], 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href'))
        if tag == 'meta' and attrs.get('name') == 'description':
            self.descriptions.append(attrs.get('content', ''))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site-url', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / 'dist'
    descriptions = []
    for path in root.rglob('*.html'):
        if path.name in {'404.html', 'retired.html'}:
            continue
        source = path.read_text()
        page = Page()
        page.feed(source)
        route = '/' + path.relative_to(root).as_posix().removesuffix('index.html')
        assert page.canonicals == [args.site_url.rstrip('/') + route], (route, page.canonicals)
        assert page.h1 == 1, (route, 'H1 count', page.h1)
        assert len(page.descriptions) == 1 and page.descriptions[0], (route, 'description')
        assert 'shiny-carpet-cleaning-va.netlify.app' not in source, (route, 'retired host')
        descriptions.extend(page.descriptions)
    assert not [text for text, count in Counter(descriptions).items() if count > 1], 'Duplicate descriptions'
    print(f'PASS: {len(descriptions)} pages: one canonical, one H1, unique descriptions, no retired host.')

if __name__ == '__main__':
    main()
