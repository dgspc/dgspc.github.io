# Code notes

Everything that used to live as a comment inside the HTML, CSS and JavaScript.
Moved here so the shipped source carries no developer-facing instructions.

Three reasons this matters: view-source is public, placeholder notes tend to
outlive the placeholders, and instructions buried in thirteen files get missed.

---

## 1. Placeholders to replace

### Contact form endpoint

**Where:** `contact.html`

NOTE FOR IMPLEMENTATION Deliberately not a <form> element — submission is handled in JS so the page never navigates away. To wire this up, POST the payload assembled in collect() to your CRM or an endpoint of your choosing, and keep the client-side validation as a first pass only.

### Legal draft banners

**Where:** `privacy.html` and `terms.html`

DRAFT BANNER · reader-facing notice. Delete this block AND the noindex meta tag in <head> once legal has signed off.

---

## 2. Deployment

The note that used to sit at the top of `404.html`.

```
============================================================
     DEPLOYMENT NOTE · GITHUB PAGES
     ============================================================
     Good news: GitHub Pages needs no configuration for this file.
     A 404.html at the root of the published branch or folder is
     picked up automatically and served with a genuine HTTP 404
     status, on both user sites and project sites. Nothing to add.

     VERIFY ANYWAY · should print 404, not 200
       curl -I https://your-domain.com/this-page-does-not-exist

     WHY IT MATTERS
       If a host ever serves this content with a 200 status you have
       a "soft 404". The visitor sees the right page, but every
       machine reading the site is told the URL is valid, and four
       things break silently at once:
         1. Search engines index it, so you accumulate thin
            near duplicate pages competing with the real ones.
         2. Search Console stops reporting broken links, because
            as far as it can tell nothing is broken.
         3. Analytics logs ordinary pageviews, so you never find
            out which of your own internal links are dead.
         4. Uptime and link checkers go quiet for the same reason.
       Nobody gets an alert, which is why it survives launch.

     GITHUB PAGES SPECIFICS
       · Paths are case sensitive. Keep filenames lowercase.
       · Every link on this site is relative, so it works whether
         you publish to username.github.io or to a project site at
         username.github.io/repo-name/.
       · The suggestion logic below matches on the last path
         segment, so a /repo-name/ prefix does not confuse it.
       · Jekyll runs by default. The .nojekyll file at the root
         turns it off, which is faster and avoids surprises with
         any file or folder whose name starts with an underscore.
       · There is no server side redirect support. If you need one,
         use a small HTML file with a meta refresh plus a canonical
         link, not a JavaScript redirect.

     IF YOU MOVE HOST LATER
       nginx    error_page 404 /404.html;
       Apache   ErrorDocument 404 /404.html
       Netlify, Cloudflare Pages, Vercel  automatic at the root
       S3 alone returns 200. Put CloudFront in front and map 404
       to /404.html with a 404 response code.
       Watch for catch all SPA rewrites, such as /* to /index.html
       with status 200. They silently override all of the above.

     ALSO
       Do not redirect unknown URLs to the homepage. That is a soft
       404 with worse UX on top: the visitor loses the address they
       typed and gets no clue what went wrong.
     ============================================================
```

---

## 3. Shared layer

### `site.css`

============================================================ DIGITAL SPECTRE — SHARED LAYER Tokens, reset, ambient field, type scale, buttons, nav, reveals, section heads and footer. Loaded by every page before its own inline styles, so any page can override. Edit design tokens HERE, not in a page. ============================================================

### `site.js`

============================================================ DIGITAL SPECTRE — SHARED BEHAVIOUR Sticky nav, scroll reveals, mobile menu. Every block is guarded, so this file is safe to load on any page including ones without a sticky nav or a burger (404). Page-specific behaviour stays inline on each page. ============================================================

Every page loads `site.css` and `site.js` first, then its own inline `<style>`
and `<script>`. Inline therefore wins, which is how a page overrides a shared
rule. Change a design token in `site.css` and it applies everywhere.

Deliberate overrides: `index.html` runs a slightly larger type and spacing
scale; `privacy.html` and `terms.html` use a document layout with no film grain.

---

## 4. Design rationale, page by page

Why each page is built the way it is — originally the header comment in each
`<style>` block, plus notes on the non-obvious decisions.

### `index.html` — Homepage

- THE CONSOLE A sweep passes over the fleet; whatever it touches reports into the feed. Feed rows are caused by the radar, not faked alongside it. ============================================================

### `platform.html` — Platform

- AUTONOMY LADDER Three meters per rung. Agent reach and required controls climb together; human grip on each individual action falls away. That opposition is the argument the section makes. ============================================================

### `solutions.html` — Solutions

- THREE LENSES Auto-advances so the argument lands without a click, but any interaction hands control over and the rotation stops. ============================================================

### `sectors.html` — Sectors

- COMPARISON TABLE Built from data so the desktop grid and the stacked mobile cards can never drift apart. ============================================================

- Emitted column by column: [corner + row labels], then each sector's header followed by its own five values. Desktop reads it as a table via grid-auto-flow:column; mobile reads it as four stacked cards.

### `pricing.html` — Pricing

- CALCULATOR Volume ladder is a flat rate per band, not a marginal one — simpler to reason about, and it never produces the situation where adding one agent costs more than adding ten. ============================================================

- Flat bands invert at the boundaries: 25 agents at $59 costs more than 26 at $47. So we cap at whatever the cheapest larger deployment would cost. Nobody ever pays more for supervising less.

### `how-we-work.html` — How we work

- HANDOVER CHART 3 = leading, 0 = not involved. Spectre falls, the client's engineers rise, and security spikes at step two where the rules are written. ============================================================

### `trust.html` — Trust

- FAILURE MATRIX Same four scenarios, two postures. Cells marked `stop` are where an agent is deliberately prevented from acting — the cost of fail-closed, shown rather than glossed over. ============================================================

### `integrations.html` — Integrations

- DIRECTORY kind: 'watched'  = seen as a tool call, no setup 'conn'     = a connector we build and maintain ============================================================

### `contact.html` — Contact

- LIVE BRIEF Team decides who shows up; fleet size decides what's worth showing. Both feed the same four rows. ============================================================

- VALIDATION + SUBMIT ============================================================

### `privacy.html` — Privacy

- these document pages have never carried the film grain — remove this line if you'd rather they matched the marketing pages

### `terms.html` — Terms

- these document pages have never carried the film grain — remove this line if you'd rather they matched the marketing pages

### `404.html` — 404

- GitHub Pages project sites are served from /repo-name/, so the pathname carries a prefix that isn't part of what the visitor asked for. Show the full path, but match on the last segment only.

---

## 5. Rebuilding this file

These notes were extracted from the source, not written separately. If you add
a comment to a page it will not appear here automatically — put it in this file
instead, and keep the shipped source clean.

---

## 5. The mark

Two offset parallel forms — the ghost and the solid, the same shape caught
twice. It is the afterimage idea the rest of the site is built on, which is
why the hero headline uses the same device in motion.

**Construction.** Every straight edge in the mark is vertical, horizontal, or
sits on one of two ruled angles:

| | ratio | used for |
|---|---|---|
| band | 7 across : 5 down | the two diagonal bars, the lower corner wedge |
| bevel | 5 across : 4 up | the cut tips of both bars, the upper corner wedge |

Drawn on a 96 x 100 grid. Left rail at `x=0`, outer edge at `x=96`. Bar width
is 42 units. The one soft detail is the outer corner where the upper bar meets
the right edge — a single curve in an otherwise hard-edged mark. Keep it.

**Where it lives.** The mark is inlined in the nav and footer lockup on all 13
pages so it inherits `currentColor` and costs no extra request. `logo.svg` is
the same geometry as a standalone file, for anything outside the site.

**If you redraw it,** change `logo.svg`, `favicon.svg`, the two PNG icons and
the 25 inline copies together, or the set drifts apart. The inline copies are
byte-identical, so a find-and-replace across `/docs/*.html` does it.

**Clear space** is the width of one bar — 42 grid units, or roughly 44% of the
mark's height — on every side. Below about 16px the corner wedges start to
disappear; use the favicon artwork there, which carries a tighter margin.

---

## 6. Typefaces

Self-hosted from `/docs/fonts`, declared at the top of `site.css`. Nothing is
requested from Google Fonts or any other third party — `privacy.html` says so
in as many words, and the CSP (`font-src 'self'`) enforces it.

| File | Axes kept | Size |
|---|---|---|
| `bricolage-grotesque.woff2` | `opsz` 12–96, `wght` 400–800 | 156K |
| `inter-tight.woff2` | `wght` 400–600 | 77K |
| `martian-mono.woff2` | `wght` 300–500 | 44K |

All three are subsetted to Latin plus the marks the copy uses. That includes
`U+2192` — the arrow in the buttons and in the console feed sits outside
Google's `latin` subset, so it used to fall back to a system glyph and now
doesn't.

**Optical sizing** is two thirds of the display face's weight. It is worth
keeping: that file runs from 17.5px in the nav to 84px in the hero, and the
`opsz` axis is what stops the large sizes looking loose. Pinning it drops the
file to 80K if you ever need the bytes back.

**The mono face is declared `font-weight:500`, not `300 500`.** Google served
Martian Mono as two static faces, 300 and 500, so every mono element on the
site — including the ones that never set a weight and inherit 400 — resolved
to 500. Pinning the descriptor reproduces that exactly. Widen it to `300 500`
if you want the lighter weight available, but check the small grey labels
afterwards: they get about 4% lighter.

**Preload** covers the display and body faces only, because those set the
first paint. `crossorigin` is required even though the files are same-origin —
font fetches are CORS-mode, and without it the browser downloads each file
twice.

Licences sit next to the fonts as `*-OFL.txt`. All three are SIL Open Font
License, which permits self-hosting and requires the licence to travel with
the files.

---

## 7. Heading levels

Small mono labels — footer columns, `WHAT YOU KEEP`, `AGENTS WE SEE` and the rest —
are `<h3 class="hlab">`. They were `<h4>` sitting directly under an `<h2>`, which is a
skipped level.

Two traps if you touch this. `h3` carries `line-height:1.16` where `h4` inherited
`1.02`, and several pages set `max-width` on `h3` for real section headings
(`.sect h3`, `.role h3`, `.surface h3`, `.q h3` and others). Every `.hlab` rule
therefore opens with `line-height:1.02;max-width:none;` to hold the old rendering.
Drop either and the labels wrap.

`trust.html` already had a class called `lab`, which is why these are `hlab`.

---

## 8. The mid grey

`--smoke` is `#878F96`, not the `#71787E` it started as. The original was 4.45:1
against `--void` — under the 4.5:1 WCAG AA floor for normal text — and 3.31:1
against `--ash`. It sets footer copy, every mono label, timestamps, `.dim`
paragraphs and the console chrome, so it was the single cause of every contrast
failure on the site.

`#878F96` holds the same hue and clears AA on all three surfaces: 6.07 on
`--void`, 5.81 on `--carbon`, 4.52 on `--ash`.

It is defined in five places — `site.css` plus the inline `:root` in `404.html`,
`index.html`, `privacy.html` and `terms.html`. Change one and you get four pages
disagreeing with the other nine. The token is only ever used as a text colour,
never a background, border or fill, so adjusting it cannot move anything.

---

## 9. The CSP is hash-pinned

`script-src` does not carry `'unsafe-inline'`. Each page pins the SHA-256 hash
of its own inline `<script>` instead, which is why the policy differs slightly
from page to page — that is deliberate, not drift.

**Edit an inline `<script>` and that page's script stops running.** The hash no
longer matches and the browser refuses it, silently apart from a console
message. Regenerate after any such edit:

```bash
python3 tools/csp-hashes.py            # rewrite the hashes
python3 tools/csp-hashes.py --check    # non-zero exit if any page is stale
```

The `--check` form is what you want in CI or a pre-commit hook.

`style-src` still carries `'unsafe-inline'` and has to: the site uses 17 inline
`style=""` attributes, and CSP hashes cover `<style>` elements but not
attributes. Rewriting those 17 into classes would let you drop it.

This only works because no page uses inline event handlers (`onclick=` and
friends). If you add one it will not fire, and the fix is a listener in the
inline script rather than loosening the policy.
