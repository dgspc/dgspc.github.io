# Test report

Headless Chromium 131, 13 pages × 3 viewports = **39 runs**.

| Viewport | Size | Touch |
|---|---|---|
| Mobile | 375 × 812 | yes |
| Tablet | 768 × 1024 | yes |
| Desktop | 1440 × 900 | no |

Each run loads the page, scrolls the full height to trigger every
`IntersectionObserver`, then measures the rendered result.

## Result: 39 / 39 pass

| Check | Mobile | Tablet | Desktop |
|---|---|---|---|
| Horizontal overflow | pass | pass | pass |
| JS errors and 404s | pass | pass | pass |
| Scroll reveals fire | pass | pass | pass |
| Tap targets ≥ 40px | pass | pass | pass |
| Nav collapse | pass | pass | pass |

**Nav behaviour** — desktop shows the five links and hides the burger; mobile
and tablet do the reverse. The 404 has no burger by design, which the test
records rather than flags.

**Overflow** — measured on element bounding boxes rather than
`document.scrollWidth`, because `body` sets `overflow-x: hidden` and would have
masked a real overflow. Elements that do extend past the viewport (the marquee
track, the radar canvas) were confirmed to sit inside an `overflow: hidden`
ancestor: 39 on mobile, 37 on tablet, 29 on desktop, all correctly clipped.

## What the test found and what was fixed

Touch targets below 40px on mobile and tablet:

| Control | Was | Now |
|---|---|---|
| Burger menu, all 12 pages with a nav | 34px | 44px |
| Fail open / fail closed toggle, `trust.html` | 31px | 44px |
| Category filters, `integrations.html` | 39px | 44px |
| Lens tabs, `solutions.html` | 40px | 44px |
| Tier buttons, `pricing.html` | — | 44px |

These passed WCAG 2.2 AA (2.5.8 wants 24px) but fell short of AAA and of the
Apple and Android guidance of 44 and 48px. Cheap to fix, so fixed.

The media query is `(pointer:coarse),(max-width:960px)`. Coarse pointer alone
misses touch laptops that report a fine primary pointer; the width clause
catches those. Desktop rendering is unaffected.

## Layout reflow verified

Grid column counts measured directly from computed style:

| Component | Mobile | Tablet | Desktop |
|---|---|---|---|
| Homepage hero | 1 | 1 | 2 |
| Homepage console | 1 | 2 | 2 |
| Sectors comparison table | 1 | 1 | 5 |
| Pricing tiers | 1 | 1 | 3 |
| Trust failure matrix | 1 | 1 | 4 |
| Autonomy ladder rung | 1 | 1 | 3 |
| Contact form and brief | 1 | 1 | 2 |
| Integrations grid | 1 | 2 | 3 |
| Legal document layout | 1 | 1 | 2 |

The sectors table is the one worth noting: it is emitted column-major and uses
`grid-auto-flow: column` on desktop, so the same markup reads as a five-column
table on desktop and as four stacked per-sector cards on mobile.

## Not covered

- Real iOS Safari and Android Chrome. Chromium 131 is a good proxy but not a
  substitute, particularly for Safari's handling of `100vh` and sticky headers.
- Fonts. The sandbox blocks Google Fonts, so all 39 runs rendered on the system
  fallback stack. Layout held, which is itself a useful result — but check the
  real typeface once deployed.
- Screen readers and keyboard-only navigation.
- Lighthouse performance scoring.

## Reproducing

```bash
cd dist && python3 -m http.server 8899 &
node responsive-test.js
```
