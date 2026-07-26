# Deploying to GitHub Pages

Static site, no build step. Push the files and enable Pages.

**Repository layout**

```
/                 DEPLOY.md, CODE-NOTES.md, TEST-REPORT.md   <- never served
/docs             the site itself                            <- publish this
```

The three markdown files sit at the repository root deliberately. They list
every unfinished item on the site, so serving them publicly would hand a
prospect your pre-launch checklist. Publishing from `/docs` keeps them private
while leaving them in version control.

## Files to publish

| File | Purpose |
|---|---|
| `index.html` | Homepage. **Must** be named this — Pages serves it at the root |
| `404.html` | Error page. Picked up automatically, returns a real 404 status |
| `.nojekyll` | Turns off Jekyll processing. Faster, and avoids surprises with any file starting with `_` |
| `CNAME` | Custom domain. Currently `www.digitalspectre.com` — edit or delete |
| `CODE-NOTES.md` | Developer notes, placeholders and design rationale |
| `site.css` | Shared design layer — tokens, nav, footer, type. **Edit tokens here** |
| `site.js` | Shared behaviour — sticky nav, scroll reveals, mobile menu |
| `logo.svg`, `favicon.svg` | Brand mark, and the tab icon with its background baked in |
| `icon-192.png`, `icon-512.png` | App icons, referenced by the manifest |
| `apple-touch-icon.png` | Home-screen icon for iOS, 180x180 |
| `site.webmanifest` | Name, theme colour and icon set for installed use |
| `og-image.png` | Social preview card, 1200x630 |
| `robots.txt`, `sitemap.xml` | Search engine directives |
| 11 other `.html` files | The rest of the site |

## Do not publish

`spectre-hero-options.html` and `spectre-hero-network.html` are design review
artefacts, not part of the site. Nothing links to them, but if they're in the
published folder they'll be publicly reachable and indexable. Delete them or
keep them on a branch that isn't published.

## Setup

1. Push everything to the repository
2. **Settings → Pages → Build and deployment**, source *Deploy from a branch*
3. Pick your branch and set the folder to **`/docs`**
4. Wait for the first deploy, then check the URL

## Custom domain

The `CNAME` file sets the domain. Pair it with DNS:

| Record | Host | Value |
|---|---|---|
| `CNAME` | `www` | `<username>.github.io` |
| `A` | `@` | `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` |
| `AAAA` | `@` | `2606:50c0:8000::153`, `8001::153`, `8002::153`, `8003::153` |

Then tick **Enforce HTTPS** in Settings → Pages once the certificate issues.
Verify the apex IPs against GitHub's current documentation before you commit —
they change occasionally.

If you aren't using a custom domain yet, delete `CNAME`.

## Verify after deploying

```bash
# should print 404, not 200
curl -I https://www.digitalspectre.com/this-page-does-not-exist

# should print 200
curl -I https://www.digitalspectre.com/
```

A 200 on the first command means the error page is being served as a normal
page. See the note at the top of `404.html` for why that matters.

## Where the developer notes went

The shipped HTML, CSS and JavaScript carry **no comments**. Everything that was
a comment — placeholder instructions, deployment notes, design rationale — is in
**`CODE-NOTES.md`**. Read that before editing anything, and add new notes there
rather than back into the source.

## How the CSS and JS are organised

Every page loads `site.css` and `site.js` first, then its own inline
`<style>` and `<script>`. Anything inline therefore wins over the shared
layer, which is how a page overrides a shared rule.

- **Changing a design token** — edit `site.css`, once, and it applies everywhere
- **A page needs to differ** — put the override in that page's inline `<style>`,
  under the `overrides of the shared layer` comment
- **Page-specific behaviour** stays in that page's inline `<script>`

Three pages carry deliberate overrides: `index.html` runs a slightly larger
type and spacing scale, and `privacy.html` / `terms.html` use a document
layout with no film grain.

## Things that bite on GitHub Pages

- **Case sensitivity.** Paths are case-sensitive. Keep filenames lowercase.
  `Platform.html` and `platform.html` are different files.
- **No server config.** No `.htaccess`, no redirect rules, no custom headers.
  If you need a redirect, use a small HTML file with a `meta refresh` and a
  `rel="canonical"` link.
- **Relative paths only.** Every link and asset reference on this site is
  relative, so it works at both `username.github.io` and
  `username.github.io/repo-name/`. Don't introduce root-absolute paths like
  `/favicon.svg` — they break on project sites.
- **Fonts are self-hosted** from `/docs/fonts` as subsetted variable woff2,
  so the site makes no third-party requests. GitHub Pages serves `.woff2` as
  `font/woff2` with no configuration. The preload links carry `crossorigin`
  because font fetches are CORS-mode even from the same origin — drop it and
  the file downloads twice.

## Before you make the repository public

- [x] Brand assets — mark, favicon, app icons, manifest and social card are
      in place, and the inline lockup on all 13 pages uses the real mark
- [ ] Replace the placeholder testimonial on `index.html` with an approved
      customer quote and attribution
- [ ] Confirm the published figures against current measurements: latency,
      availability, termination window, self-host option, penetration testing
      cadence, sub-processor count
- [ ] Legal review of `privacy.html` and `terms.html`, then remove the draft
      banner **and** the `noindex` meta tag from each. Both pages now open with a
      notice stating the company is fictional — keep it until the site describes a
      real business, and if it ever does, the invented testimonial and figures have
      to go at the same time
- [ ] Fill in the registered address and company number in `privacy.html`
- [ ] Set governing law and jurisdiction in `terms.html`
- [ ] Confirm the team and funding statements on `about.html`
- [ ] Wire the contact form to a real endpoint — see the `collect()` function
      in `contact.html`
- [ ] Decide the repository licence. The site's own code has none, which means
      all rights reserved by default — fine for a company site, but GitHub will
      show "no licence". The fonts in `docs/fonts` are SIL OFL and carry their
      own `*-OFL.txt`; make sure a repo-wide licence doesn't imply it covers them
- [x] Contrast — `--smoke` is now `#878F96`: 6.07:1 on the page background,
      5.81:1 on `--carbon`, 4.52:1 on `--ash`. Every text style on all 13 pages
      clears WCAG AA. The token is text-only, so nothing moved
- [x] Heading order — every `<h4>` label is now `<h3 class="hlab">` and the three
      `<h1>` to `<h3>` jumps are `<h2>`. Verified pixel-identical across 13 pages
      at two viewports
- [ ] Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools
- [ ] Check the social card renders — paste a URL into Slack or LinkedIn.
      `og:image` is an absolute URL pointing at `www.digitalspectre.com`, so it
      only resolves once that domain is live. Change it if you publish
      elsewhere — crawlers won't follow a relative path.
