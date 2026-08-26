# 182b — Veragensia Base OS + Overlay Detailed Spec

**Status:** DRAFT (2026-08-26). Companion to `182-veragensia-focusa-agent-os-spec.md`.
**Repo:** Startempire-Wire/veragensia · live proving ground `https://os.focusa.dev`.
**Convention:** base = upstream-untouched; overlay = the only Focusa mutation surface.

---

## Part A — Base OS

### A.1 Definition
The base is a bootable/streamable Linux desktop that provides: a compositor/DE, a real Chromium,
the Selkies/KasmVNC streaming stack, and a place to mount the overlay + extension. Two tracks:
- **Track 1 (now, streamable):** LinuxServer **webtop** (ubuntu-kde) in Docker — container-hardened, streams via Selkies. This is what os.focusa.dev runs.
- **Track 2 (Phase 1, product):** **Omarchy** (Arch + Hyprland, MIT) — the branded, opinionated base.

### A.2 Base responsibilities (both tracks)
- Boot a Wayland/Hyprland (or KDE/X) session headlessly.
- Run Chromium with `--remote-debugging-port` (CDP) for discovery/screenshots.
- Provide the streaming endpoint (Selkies websockets) for human view.
- Expose a stable mount point for the overlay + extension (`/extroot`, overlay dir).
- Stay **login-free** for the demo (no CUSTOM_USER/PASSWORD); production access via spec-115 relay.

### A.3 Container/boot contract (Track 1)
- Mounts: `/config` (state), parent extension dir → `/extroot:ro`, overlay dir → `/overlay:ro`.
- Boot order: DE up → apply overlay (theme/services) → launch Chromium with extension → open startpage (CDP) → tunnel connector up.
- CDP on `127.0.0.1:9333`; extension ID is path-derived from `/extroot/dist`.

**Accept (base):** container boots headless; Chromium + CDP reachable; Selkies stream viewable; `/extroot/dist` and `/overlay` resolve fresh after rebuilds (parent mounts).

### A.4 Omarchy base (Track 2)
- Consume Omarchy as base image/install; do **not** patch upstream.
- Hyprland compositor; QML GUI stack available for the overlay.
- Unattended install support → build a Veragensia image (ISO or container).

**Accept (Omarchy base):** stock Omarchy boots; overlay applies cleanly on top (see Part B); no upstream file modified.

---

## Part B — Overlay (the Focusa layer)

### B.1 Definition
`overlay/` is the only Focusa mutation surface. It installs **on top of** the base and provides
branding + system services + GUI. It must be applicable to a stock base with a single idempotent step.

### B.2 Components
- **`overlay/themes/`** — Veragensia Hyprland theme: palette, logo, cursor, splash; waybar styling.
- **`overlay/services/`** — systemd units: `veragens-daemon` (Focusa daemon), `veragens-engine` (UIAI Engine), `veragens-ipc` (bus), `veragens-notify`, `veragens-audit`.
- **`overlay/gui/`** — QML Focusa shell: start page / wall / command panel as native desktop surfaces; waybar modules for live state (mission, agent activity, approvals, budget).

### B.3 System-wide Focusa layer (services ↔ primitives)
Each Focusa primitive becomes a system service with a stable IPC contract (read-only first):
daemon (authority), worksets/workstreams, silent sessions, `can(principal,capability,context)`,
approvals, credentials broker, device pairing, work-loop scheduler, roles, widgets/wall, SSE bus, audit.

### B.4 Apply mechanism
- Single idempotent installer: `overlay/install.sh` (or package) that copies themes, installs units, enables services, and reloads the compositor. No upstream patches.
- Re-runnable; detects base track (webtop vs Omarchy) and adapts paths.

**Accept (overlay):** on a stock base, `overlay/install.sh` yields a branded session; daemon + engine services healthy; waybar shows live daemon state from a fixture; re-run is idempotent.

### B.5 GUI contracts
- GUI consumes daemon state over the IPC bus read-only; mutations require approval prompts.
- waybar modules subscribe to the SSE bus; render mission/agent/approval/budget.
- QML shell renders start/wall/command natively; can embed an agent-view (Engine artifact-ref).

**Accept (GUI):** a budget pause surfaces as an OS notification; an agent action triggers an approval prompt; shell renders start page natively.

---

## Part C — Integration & sequencing
- Base (A) first, then overlay (B) applied on top; demo runs Track 1 + overlay now; product is Track 2 + overlay.
- Daemon + Engine (B.3) are what make os.focusa.dev a live agent playground.
- Licensing gates premium overlay surfaces (spec 115/118); base desktop usable unentitled.

## Non-goals
- Patching Omarchy/webtop upstream; vendoring Focusa daemon or Engine (consumed, not copied);
  real-time GUI streaming from Cloudflare containers.
