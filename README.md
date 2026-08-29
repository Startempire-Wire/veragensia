# Veragensia — the Focusa Agent OS

> *ver-* (truth) + *agens* (the actor) + *-ia* (realm) — **"the realm of the true agent."**

Veragensia is an **agent/human operating environment**: a real Linux desktop where governed agents and
people work side by side. It is the product surface of the Focusa primitives, lifted from
*browser-extension ↔ daemon* to *OS services ↔ OS GUI*.

**Live build-in-public demo / agent playground:** <https://os.focusa.dev>

## Composition

```
┌──────────────────────────────────────────────────────────────┐
│  Custom Focusa GUI (QML shell, waybar modules, branded theme) │
├──────────────────────────────────────────────────────────────┤
│  System-wide Focusa layer (daemon svc, IPC, approvals,        │
│  credentials, pairing, work-loop scheduler, audit, notify)    │
├──────────────────────────────────────────────────────────────┤
│  UIAI Engine (agent browser: verbs, budgets, fleet, events)   │
├──────────────────────────────────────────────────────────────┤
│  Omarchy base (Arch + Hyprland) — kept upstream-untouched     │
└──────────────────────────────────────────────────────────────┘
```

- **Base:** [Omarchy](https://github.com/basecamp/omarchy) (MIT), consumed as an overlay — no deep fork.
- **Focusa primitives:** re-homed, not rebuilt (daemon, worksets, silent sessions, `can()`, approvals,
  credentials broker, device pairing, work loop, roles, widgets/wall, SSE, audit).
- **UIAI Engine:** the agent's browser and perception layer.
- **Browser + Focusa Workforce extension** ship preinstalled on every install (a native surface).

An **Agent Cloud Computer** is a provisioned, streamable Veragensia instance — the client-setup offer.

## Architecture principle
*Surfaces are interchangeable; primitives are the platform.* The browser extension, the desktop,
mobile, and cloud runtimes are all windows into the same daemon-owned truth. Companion control plane:
Focusa Cloud (private spec 115) — *cloud coordinates, node decides, receipts prove, private state stays local.*

## This repo
- `overlay/` — the Focusa layer installed **on top of** stock Omarchy (theme, services, GUI).
- `scripts/` — lab lifecycle, atomic deployment, browser launcher, narrow remote control, and screenshot tooling.
- `ops/sudoers/` — least-privilege deployment templates for the live lab.
- `docs/182-…` — product/base/fleet specs (mirrors of public Focusa spec 182).
- `docs/183-veragensia-public-agent-computer-security-and-lifecycle.md` — constant-availability, stable-sync, self-healing, and public/private browser trust contract.

## Run the lab (proving ground)
```bash
scripts/uiai-lab-live up            # container + extension chromium + tunnel + keeper
scripts/uiai-lab-live persist on    # always-on demo (off = idle teardown)
scripts/uiai-lab-push               # atomic stable deploy + reload + end-to-end verification
```

The public demo is a `public_demo` trust class: operator/provider credentials must use a private ephemeral browser context and must never persist in the public profile. See docs/183.

## Status
Build-in-public. Phase 0 (live webtop demo) operational at os.focusa.dev. Phases 1–4 per docs/182.

## License
TBD (Omarchy base is MIT; Focusa primitives are source-available). See open questions in docs/182.
