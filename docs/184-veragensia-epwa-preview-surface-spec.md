# 184 — Veragensia EPWA Preview Surface Specification

## Purpose
Expose a browser-previewable Evidence PWA presentation surface at `https://os.focusa.dev/evidence/` without claiming that static demo content is canonical evidence.

## Exact implementation allowlist
- `preview/evidence/index.html`
- `preview/evidence/styles.css`
- `preview/evidence/app.js`
- `scripts/uiai-lab-live`

## Contract
- Nginx webtop serves the dependency-free preview at `/evidence/`; lifecycle sync copies only this allowlisted directory from the read-only `/veragensia` mount.
- Preview visibly labels itself `Preview fixture — not canonical evidence`; no fake verification, completion, settlement, or provider claims.
- UI demonstrates packet cards, thumbnail framing, ID + descriptor, source/capture metadata, trust posture, expandable provenance, responsive light/dark presentation, and degraded/unavailable state.
- No external fonts, libraries, credentials, private paths, or mutable packet storage.
- Runtime packet links remain placeholders until canonical UIAI API routing is mounted.
- `uiai-lab-live` syncs preview on create and reload; failure is surfaced and lifecycle activation fails closed.

## Acceptance
- `/evidence/` returns HTTP 200 from the public demo after lifecycle reload.
- 375/768/1024/1440 screenshots show no horizontal overflow.
- Browser diagnostics have no new errors.
- Existing root desktop route and extension mounts remain unchanged.

## Rollback
Remove the preview sync call and `preview/evidence/`; the desktop shell remains available.
