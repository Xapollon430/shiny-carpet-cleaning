# Shiny on exe.dev

Personal account: xapollon430@gmail.com
VM and public URL: https://shiny-carpet-cleaning.exe.xyz
Application: /home/exedev/shiny
Service: shiny.service on localhost:8000, automatic startup and restart
Secrets: /etc/shiny.env, root only
Private form records: /var/lib/shiny

Node 22 serves dist and sends the three forms through Resend. Résumés are emailed as attachments and never served publicly. Includes field validation, honeypot, rate limits and origin checks. VM storage is not an offsite backup.

Deploy from site/:

```sh
python3 scripts/build_migration.py
SITE_URL=https://shiny-carpet-cleaning.exe.xyz python3 scripts/apply_seo.py
COPYFILE_DISABLE=1 tar --no-xattrs -czf /tmp/shiny-deploy.tar.gz dist emails server
scp /tmp/shiny-deploy.tar.gz shiny-carpet-cleaning.exe.xyz:/home/exedev/shiny-deploy.tar.gz
ssh shiny-carpet-cleaning.exe.xyz 'tar -xzf /home/exedev/shiny-deploy.tar.gz -C /home/exedev/shiny && sudo systemctl restart shiny'
```

Logs: ssh shiny-carpet-cleaning.exe.xyz 'sudo journalctl -u shiny -n 30 --no-pager'

Netlify has been removed. The seven historical submissions were archived privately on the VM at /var/lib/shiny/netlify-archive.json. No custom-domain DNS changes. Update SITE_URL, SEO metadata and service environment together when adding a domain.

Migration rules live in seo/redirects.csv. Rebuild them with scripts/build_migration.py. The audited original URL inventory is seo/legacy-url-inventory.csv. Verify a running server with python3 scripts/check_migration.py --base-url=https://shiny-carpet-cleaning.exe.xyz. Retired campaign/confirmation/template URLs return HTTP 410 with noindex; unrelated unknown paths still return 404.
