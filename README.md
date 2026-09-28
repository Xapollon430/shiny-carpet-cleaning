# Shiny Carpet Cleaning

Static website for Shiny Carpet Cleaning, including service, location, review, careers, blog, contact, and interactive 404 pages.

## Local preview

From this directory, run:

```bash
python3 -m http.server 4173 --directory dist
```

Then open `http://127.0.0.1:4173`.

## Deployment

The site is configured for Netlify with `dist` as the publish directory. Quote, contact, and career forms use Netlify Forms.

Set `SITE_URL` when regenerating production metadata:

```bash
SITE_URL=https://example.netlify.app python3 scripts/apply_seo.py
python3 scripts/prepare_launch.py
```
