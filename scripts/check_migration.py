#!/usr/bin/env python3
"""Check every audited legacy URL and migration rule against an HTTP server."""
from __future__ import annotations
import argparse
import collections
import concurrent.futures
import csv
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request,build_opener,HTTPRedirectHandler

ROOT=Path(__file__).resolve().parents[1]
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',required=True);args=parser.parse_args();base=args.base_url.rstrip('/')
    rules={r['source']:r for r in csv.DictReader((ROOT/'seo/redirects.csv').open())}
    inventory=list(csv.DictReader((ROOT/'seo/legacy-url-inventory.csv').open()))
    def fetch(route,method='HEAD'):
        try:response=build_opener(NoRedirect).open(Request(base+route,method=method),timeout=30)
        except HTTPError as response:
            return response.code,dict(response.headers),response.read() if method=='GET' else b''
        return response.status,dict(response.headers),response.read() if method=='GET' else b''
    def check(source):
        rule=rules.get(source);expected=int(rule['status']) if rule else 200
        status,headers,_=fetch(source)
        assert status==expected,(source,status,expected)
        if expected==301:
            assert headers.get('Location')==rule['target'],(source,headers.get('Location'),rule['target'])
            if rule['target'].startswith('/'):
                final,_,_=fetch(rule['target'].split('#')[0]);assert final==200,(source,'bad final target',final)
        elif expected==410:
            assert headers.get('X-Robots-Tag')=='noindex',(source,'retired page is indexable')
        return expected
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(check,sorted(set(rules)|{r['path'] for r in inventory})))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        legacy=list(pool.map(check,[r['path'] for r in inventory]))
    # Slash variants and attribution query strings must survive the migration.
    assert fetch('/carpet-cleaning-cost')[1]['Location']=='/blogs/carpet-cleaning-cost/'
    assert fetch('/carpet-cleaning-cost/?utm_source=migration-test')[1]['Location']=='/blogs/carpet-cleaning-cost/?utm_source=migration-test'
    assert fetch('/get-free-estimate/?utm_source=migration-test')[1]['Location']=='/?utm_source=migration-test#form'
    assert fetch('/book/?utm_source=migration-test')[1]['Location'].endswith('?utm_source=migration-test')
    assert fetch('/?utm_source=migration-test')[0]==200
    assert fetch('/migration-check-unknown-route/')[0]==404
    _,_,retired=fetch('/thank-you/','GET');assert b'noindex' in retired and b'no longer available' in retired
    _,_,sitemap=fetch('/sitemap.xml','GET');assert b'retired.html' not in sitemap
    print(f'PASS: all {len(inventory)} audited old URLs: {dict(collections.Counter(legacy))}')
    print(f'PASS: all {len(rules)} explicit rules and their internal destinations, slash variants, query preservation, retirement/noindex, sitemap exclusions and unknown-route 404.')

if __name__=='__main__':main()
