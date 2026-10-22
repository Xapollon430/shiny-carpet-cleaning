#!/usr/bin/env python3
"""Build a static-only vendor handoff; never include Git history or server secrets."""
from pathlib import Path
import argparse,csv,hashlib,json,re,shutil,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--site-url',default='https://shinycarpetcleaning.com')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    site=args.site_url.rstrip('/')
    if not re.fullmatch(r'https://[A-Za-z0-9.-]+',site):
        parser.error('--site-url must be an HTTPS origin without a path')
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='shiny-handoff-') as temp:
        package=Path(temp)/'shiny-static-handoff';dist=package/'dist'
        shutil.copytree(ROOT/'dist',dist,ignore=shutil.ignore_patterns('.DS_Store','*.pyc','__pycache__'))
        for path in dist.rglob('*'):
            if path.is_file() and path.suffix in {'.html','.js','.css','.xml','.txt'}:
                source=path.read_text()
                source=source.replace('https://shiny-carpet-cleaning.exe.xyz',site)
                if path.suffix=='.html':
                    source=re.sub(r' data-netlify(?:-honeypot)?="[^"]*"','',source)
                    source=source.replace('<script src="/assets/site.js', '<script src="/assets/handoff-config.js"></script><script src="/assets/site.js')
                path.write_text(source)
        config='''// Set same-origin POST endpoints before publishing the forms.
// Keep API keys on the receiving server, never in this file.
window.SHINY_FORM_ENDPOINTS = {
  "quote-request": "",
  "contact-message": "",
  "career-application": ""
};
'''
        (dist/'assets/handoff-config.js').write_text(config)
        js=dist/'assets/site.js';source=js.read_text()
        marker="    if (status) status.textContent = 'Sending…';"
        assert source.count(marker)==1,'Form integration changed; review handoff adapter'
        source=source.replace(marker,'''    const endpoint = window.SHINY_FORM_ENDPOINTS?.[form.name];
    if (!endpoint) {
      if (status) status.textContent = 'Please call (703) 975-9099 to contact the Shiny team.';
      return;
    }
'''+marker)
        assert "fetch(form.action || '/', request)" in source
        js.write_text(source.replace("fetch(form.action || '/', request)","fetch(endpoint, request)"))
        migration=package/'migration';migration.mkdir()
        for name in ['redirects.csv','legacy-url-inventory.csv']:
            shutil.copyfile(ROOT/'seo'/name,migration/name)
        shutil.copyfile(ROOT/'handoff/README.md',package/'README.md')
        (package/'TARGET-DOMAIN.txt').write_text(f'{site}\nDomain-specific canonicals, structured data, social metadata and sitemap use this origin.\n')
        textfiles=[x for x in dist.rglob('*') if x.is_file() and x.suffix in {'.html','.js','.css','.xml','.txt'}]
        for path in textfiles:
            text=path.read_text()
            for forbidden in ['xapollon430@gmail.com','shiny-carpet-cleaning.exe.xyz','shiny-carpet-cleaning-va.netlify.app','RESEND_API_KEY','/Users/vehbikaraagac']:
                assert forbidden not in text,(path,forbidden)
        files=[x for x in package.rglob('*') if x.is_file()]
        manifest={str(x.relative_to(package)):hashlib.sha256(x.read_bytes()).hexdigest() for x in files}
        (package/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2))
        destination=output/'shiny-static-handoff.zip'
        with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as archive:
            for path in package.rglob('*'):
                if path.is_file():archive.write(path,str(path.relative_to(package.parent)))
        print(f'{destination}\n{len(files)} files; {destination.stat().st_size/1e6:.1f} MB. No backend or credentials included.')

if __name__=='__main__':main()
