# Brand assets

Masters. Nothing in this folder is served — `/docs` is the published folder.

| File | Use |
|---|---|
| `logo-lockup.svg` | Mark plus wordmark, horizontal. Type is converted to outlines, so it renders correctly without Bricolage Grotesque installed. For the repository README, decks, press and email signatures. |
| `avatar-512.png` | Square avatar for the GitHub organisation, and anywhere else that wants a single image with the background included. |

The web assets live in `/docs`: `logo.svg` (mark alone, inherits
`currentColor`), `favicon.svg`, `icon-192.png`, `icon-512.png`,
`apple-touch-icon.png` and `og-image.png`.

## Using it

**Colour.** The mark is one colour. Phosphor `#F4F6F7` on void `#08090A`, or
void on phosphor. Nothing else — no gradient, no outline, no second colour in
the bands. The offset pair already carries the idea; tinting one of them
flattens it.

**Clear space.** One bar width on every side — about 44% of the mark's height.

**Minimum size.** 16px tall. Below that the corner wedges close up; use
`favicon.svg`, which is drawn with a tighter margin for exactly this reason.

**Don't** rotate it, stretch it to fill a square, add a drop shadow, or
reproduce it over a photograph or a busy field. It is built on two fixed
angles and a vertical rail; anything that disturbs those reads as a mistake.

Construction is documented in `../CODE-NOTES.md`.
