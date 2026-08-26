# Runbook — point veragensia.com → os.focusa.dev

**Trigger:** operator purchases `veragensia.com`. Until then this is a ready-to-run plan (no-op).
**Goal:** brand domain redirects to the live OS demo; canonical marketing domain later.

## Steps (once owned)
1. **Add zone to Cloudflare:** `cf` / CF dashboard → add `veragensia.com`, switch NS at registrar.
2. **Redirect rule** (Cloudflare Redirect Rules, proxied):
   - Match: `http.host in {"veragensia.com" "www.veragensia.com"}`
   - Action: **dynamic** redirect → `concat("https://os.focusa.dev", http.request.uri.path)`
   - Status: 301 (permanent) once stable; 302 while iterating.
3. **Verify:** `curl -sI https://veragensia.com | grep -i location` → `os.focusa.dev`.
4. **Record:** add `veragensia.com` to README + KB 13 as canonical brand domain.

## Notes
- Keep `os.focusa.dev` as the live app host; `veragensia.com` is brand/marketing + redirect for now.
- If registrar offers free forwarding and CF onboarding is slow, use registrar 302 as a stopgap.
