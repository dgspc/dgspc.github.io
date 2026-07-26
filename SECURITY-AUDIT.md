# Security audit

Static site, no backend. Audited by static analysis plus live exploitation
attempts in headless Chromium 131 against a server configured to behave like
GitHub Pages.

**Verdict: safe to publish**, with two residual items noted at the end.

## Attack surface

There is almost none, and that is the main finding. No backend, no database,
no authentication, no cookies, no storage APIs, no npm dependencies shipped,
no user-generated content. The whole site is 13 static documents, one
stylesheet and one script.

| Sink | Count | Fed by |
|---|---|---|
| `innerHTML` | 12 | Hardcoded arrays only — verified each one |
| `eval`, `new Function`, `document.write`, `outerHTML`, `insertAdjacentHTML` | 0 | — |
| `localStorage`, `sessionStorage`, `document.cookie`, `indexedDB` | 0 | — |
| `javascript:` URLs | 0 | — |

External input enters in exactly one place: `404.html` reads
`window.location`. That value is written with `textContent` and a text node,
never as markup.

## Live exploitation attempts

Eight reflected-XSS payloads fired at the 404 handler — raw and URL-encoded
tags, script injection, SVG onload, attribute breakout, `javascript:` scheme,
and query and fragment variants.

**Result: zero code execution, zero dialogs, zero injected nodes.** Every
payload rendered as inert, URL-encoded text.

## Fixed during the audit

**Content Security Policy** added to all 13 pages. Blocks scripts, frames and
connections from any other origin, and disallows `<object>`, `<embed>` and
form submission entirely.

```
default-src 'self'; base-uri 'none'; object-src 'none';
script-src 'self' 'unsafe-inline';
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
font-src https://fonts.gstatic.com; img-src 'self' data:;
connect-src 'self'; form-action 'none'; upgrade-insecure-requests
```

`'unsafe-inline'` is required because the page styles and scripts are inline.
When the contact form is wired to a CRM, add that origin to `connect-src`.

**Latent injection removed.** `privacy.html` and `terms.html` built their
contents list by taking `textContent` from each heading and re-inserting it as
`innerHTML`. Author-controlled, so not exploitable, but a heading containing
`<` would have broken the page. Now built with `createElement` and
`textContent`.

**Placeholder email.** The contact form showed `sam@company.com` as its
placeholder. `company.com` is a real registered domain; changed to
`example.com`, which RFC 2606 reserves for exactly this.

**Repository restructured.** `DEPLOY.md`, `CODE-NOTES.md` and
`TEST-REPORT.md` were inside the published folder, so they would have been
readable at `/DEPLOY.md`. Between them they list every unfinished item on the
site — placeholder testimonial, unconfirmed figures, unreviewed legal pages.
The site now lives in `docs/` and the notes stay at the repository root.

**Privacy policy corrected.** It described cookies, an analytics package and a
consent mechanism, none of which exist. It also omitted Google Fonts, which is
the only third party the site contacts. Publishing an inaccurate privacy notice
is a poor look for any company and a worse one for a company selling
governance software.

## Residual risk

**1. `style-src 'unsafe-inline'`.**

The site uses 17 inline `style=""` attributes. CSP hashes cover `<style>`
elements but not style attributes, so this directive cannot be tightened
without either rewriting those 17 into classes or adding `'unsafe-hashes'`,
which is weaker than it sounds. The practical risk is low — CSS injection
needs an HTML injection point first, and there isn't one.

**2. Clickjacking.**

`frame-ancestors` is ignored in a `<meta>` CSP — it only works as a real
header, and GitHub Pages cannot set headers. The site has no authenticated
actions or state-changing controls, so the practical risk is close to zero.
If you want it closed, put Cloudflare in front and add `X-Frame-Options` and
`frame-ancestors` there.

**3. Header-only protections are unavailable.**

`X-Content-Type-Options`, `Strict-Transport-Security` and `Permissions-Policy`
have no `<meta>` equivalent. `Referrer-Policy` does, and is now set.
GitHub Pages sends HSTS on `github.io`; on a custom domain it depends on
Enforce HTTPS being ticked.

## Checked and clear

- No credentials, API keys or tokens anywhere in the source
- No `target="_blank"` without `rel`, so no tabnabbing
- No mixed content — every external reference is HTTPS
- No source maps, `.git`, backup or editor files in the bundle
- No comments in the shipped HTML, CSS or JavaScript
- `contact@digitalspectre.com` is the only address published, and it is
  intentional
- The contact form transmits nothing today; `collect()` assembles a payload
  but no endpoint is wired
- Fonts are self-hosted from `/docs/fonts`. No request leaves the origin on
  any page, and the CSP (`font-src 'self'`, no `fonts.googleapis.com` in
  `style-src`) enforces it. This closed the GDPR exposure that used to be the
  leading finding here — see `CODE-NOTES.md` section 6
- `script-src` no longer carries `'unsafe-inline'`. Each page pins the SHA-256
  hash of its own inline script instead, so injected script cannot run. Regenerate
  with `python3 tools/csp-hashes.py` after editing any inline `<script>`, and
  verify with `--check`
- `Referrer-Policy: strict-origin-when-cross-origin` is set via `<meta>` on all
  13 pages

## Re-verified after hardening

**Injection.** 32 payloads — 12 each against `location.pathname` and
`location.search` on the 404 route resolver, 8 against the contact form fields
and select values. Payloads covered raw and encoded `<script>`, `<img
onerror>`, `<svg onload>`, `<iframe srcdoc>`, `javascript:` URLs, attribute
breakouts and tag breakouts. **No execution, no injected nodes, no CSP
violations.** The 404 resolver is the only code that reads the URL and it
builds its output with `createTextNode` throughout.

**CSP enforcement, proven rather than assumed.** With the hardened policy in
place, a script element appended at runtime and an `onerror` attribute injected
via `innerHTML` were both refused by the browser, with two CSP violations
logged. All 13 pages' own inline scripts still execute, and normal browsing
produces zero violations.

**Static scan.** No credentials or key material. No `eval`, `new Function`,
`document.write`, `insertAdjacentHTML`, `srcdoc` or `javascript:` URLs. No
inline event handlers. No `localStorage`, `sessionStorage`, `document.cookie`
or `indexedDB`. No `target="_blank"` without `rel`. No external references of
any kind — the page loads six files, all same-origin.

**The 10 `innerHTML` assignments** were reviewed individually. Every one is
fed from a literal, a static lookup table or `Date`; none is reachable from
user input. The two that handle URL-derived data clear with `innerHTML = ''`
and then append text nodes.

**Accessibility.** All 13 pages pass WCAG AA contrast, heading order is
unbroken, every image has `alt`, every form control has a label, and no link
or button is missing an accessible name.
