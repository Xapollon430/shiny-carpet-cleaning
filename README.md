# Shiny Carpet Cleaning

Static website for Shiny Carpet Cleaning, including service, location, review, careers, blog, contact, and interactive 404 pages.

## Local preview

From this directory, run:

```bash
python3 -m http.server 4173 --directory dist
```

Then open `http://127.0.0.1:4173`.

## Deployment

Live site: https://shiny-carpet-cleaning.exe.xyz

The website runs on its own exe.dev VM. Node serves the static `dist` directory and processes quote, contact and careers forms through Resend. See [server/README.md](server/README.md) for deployment, configuration and logs.

```bash
SITE_URL=https://shiny-carpet-cleaning.exe.xyz python3 scripts/apply_seo.py
```

The GitHub repository is public. Keep secrets and customer submissions out of Git.
