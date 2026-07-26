# Digital Spectre — website

Static marketing site. No build step, no dependencies, no framework.

**Live:** https://www.digitalspectre.com

## Layout

```
/                    docs and notes — not served
  README.md          this file
  DEPLOY.md          deployment, DNS, pre-launch checklist
  CODE-NOTES.md      placeholders, design rationale, shared layer
  SECURITY-AUDIT.md  audit findings and residual risk
  TEST-REPORT.md     responsive test results

/docs                the site — publish this folder
  index.html         homepage
  404.html           error page
  site.css           shared design layer — edit tokens here
  site.js            shared behaviour
  CNAME              custom domain
  .nojekyll          disables Jekyll
  robots.txt
  sitemap.xml
  og-image.png       social preview card, 1200x630
  logo.svg           brand mark, inherits currentColor
  favicon.svg        tab icon, background baked in
  icon-192.png       app icons, referenced by the manifest
  icon-512.png
  apple-touch-icon.png
  site.webmanifest
  fonts/             self-hosted woff2 + OFL licences
  … 11 more pages

/tools               maintenance scripts — not served
  csp-hashes.py      regenerate the CSP script hashes after editing inline JS

/brand               masters — not served
  logo-lockup.svg    mark + wordmark, type converted to outlines
  avatar-512.png     square avatar for the GitHub organisation
  README.md          what each asset is for
```

The markdown files sit outside `/docs` deliberately. They list every unfinished
item on the site, so serving them publicly would hand a prospect the pre-launch
checklist.

## Pages

| Page | Purpose |
|---|---|
| `index.html` | Homepage |
| `platform.html` | Product — four surfaces, autonomy ladder |
| `solutions.html` | By role — security, operations, compliance |
| `sectors.html` | By sector — financial, healthcare, public, technology |
| `pricing.html` | Tiers and calculator |
| `how-we-work.html` | Engagement model |
| `trust.html` | Security, data handling, failure behaviour |
| `integrations.html` | What it watches and what it connects to |
| `about.html` | Positions and their cost |
| `contact.html` | Book a walkthrough |
| `privacy.html` | Privacy notice — **draft** |
| `terms.html` | Terms of service — **draft** |
| `404.html` | Error page |

## Deploying

**Settings → Pages → Build and deployment → Deploy from a branch**, then set the
folder to **`/docs`**.

Full instructions, DNS records and the pre-launch checklist are in `DEPLOY.md`.

## Editing

- **A design token** — `docs/site.css`, once, applies everywhere
- **A page needs to differ** — put the override in that page's inline `<style>`
- **Shared behaviour** — `docs/site.js`
- **Notes** — `CODE-NOTES.md`, not comments in the source. The shipped HTML,
  CSS and JavaScript deliberately carry none.

## Before going public

See the checklist at the end of `DEPLOY.md`. The short version: replace the
placeholder testimonial, confirm the published figures, get the two legal pages
reviewed, and wire the contact form to an endpoint. Brand assets are done —
`CODE-NOTES.md` explains how the mark is built if you ever need to redraw it.
