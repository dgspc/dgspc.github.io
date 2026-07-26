"""Harden the CSP.

script-src 'unsafe-inline' is the one directive that meaningfully weakens this
policy: with it, any injected <script> runs. Each page has exactly one inline
script and no inline event handlers, so the directive can be replaced with a
SHA-256 hash of that script's contents.

style-src keeps 'unsafe-inline' — the site uses 17 inline style="" attributes
and CSP hashes do not cover attributes.

Re-run this after editing any inline <script>, or that page's script stops
executing.
"""
import base64, hashlib, re, sys
from pathlib import Path

DOCS = Path("/home/claude/site/docs")
CHECK = "--check" in sys.argv

SCRIPT = re.compile(r"<script>(.*?)</script>", re.S)
CSP = re.compile(r'(Content-Security-Policy" content=")([^"]+)(")')
REFERRER = '<meta name="referrer" content="strict-origin-when-cross-origin">\n'

stale, done = [], []
for f in sorted(DOCS.glob("*.html")):
    t = f.read_text()
    bodies = SCRIPT.findall(t)
    if len(bodies) != 1:
        print(f"!! {f.name}: expected 1 inline script, found {len(bodies)}")
        continue
    digest = base64.b64encode(hashlib.sha256(bodies[0].encode()).digest()).decode()
    token = f"'sha256-{digest}'"

    m = CSP.search(t)
    policy = m.group(2)
    new_policy = re.sub(r"script-src [^;]+",
                        f"script-src 'self' {token}", policy)

    if CHECK:
        if token not in policy:
            stale.append(f.name)
        continue

    t = t[:m.start(2)] + new_policy + t[m.end(2):]

    if 'name="referrer"' not in t:
        anchor = '<meta name="viewport"'
        i = t.index(anchor)
        t = t[:i] + REFERRER + t[i:]

    f.write_text(t)
    done.append((f.name, digest[:12]))

if CHECK:
    print("pages whose CSP hash no longer matches their inline script:",
          stale or "none — all current")
    sys.exit(1 if stale else 0)

for name, d in done:
    print(f"  {name:20} sha256-{d}…")
print(f"\n{len(done)} pages hardened: script-src 'unsafe-inline' removed, "
      "referrer policy added")
