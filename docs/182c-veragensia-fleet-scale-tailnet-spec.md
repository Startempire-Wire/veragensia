# 182c — Veragensia Fleet-Scale + Tailnet Mesh Spec

**Status:** DRAFT vision (2026-08-26). Companion to 182 / 182b; control plane = private spec 115.
**Planning:** capture gaps concisely in repository-local `br`; do not duplicate trackers or turn this draft vision into implementation before the operator and planning agent select the architecture.
**Vision:** spin up a fleet of Veragensia Agent Cloud Computers with a button in the Focusa UI —
e.g. ~85 instances × ~20 agents each running autonomous workflows — on the Tailscale mesh
(free tier = 100 nodes), each instance a tailnet node.

## Architecture
- **GUI Veragensia (few):** human-viewable webtop desktops (demos, operators). Heavy (~1–2 GB RAM each).
- **Headless workers (many):** UIAI Engine + Focusa daemon, no desktop — light; this is where
  ~20 agents/instance is feasible.
- **Tailnet mesh:** every instance joins Tailscale as its own node → addressable, encrypted,
  no port-forwarding; operator devices reach daemons over the mesh. (In-container `tailscaled`
  needs admin-minted authkeys.)
- **Orchestrator = Focusa control plane (115):** node registry, multi-node sync, device trust.
  The "button" = provision container → join tailnet → register node → launch silent sessions/work-loop.

## The button → provisioning flow
1. Focusa UI action `veragensia.spawn { kind: gui|headless, agents: N }`.
2. Orchestrator provisions a container (webtop for gui; headless image for workers) on a host with headroom.
3. Instance joins tailnet (authkey), registers as a Focusa node (heartbeat, tier).
4. Daemon starts; N silent sessions / work-loop agents launched, budgeted (engine governors).
5. Instance appears in the node registry; GUI ones stream via their tunnel/relay.

## Scale math (constraints that shape design)
- **RAM:** 85 GUI containers × ~1.5 GB ≈ 128 GB ≫ one OVH box (24 GB) → distribute across hosts,
  and prefer headless for the many.
- **LLM cost/quotas:** 1700 live agents = enormous spend + rate limits → the binding constraint.
  Needs a cost governor (engine budgets, spec 010) and per-fleet caps.
- **Tailscale free = 100 nodes** → fine to start; commercial fleet → paid mesh or spec-115 relay.

## Phases
- **P0 (now):** single GUI demo (os.focusa.dev) + in-container daemon. ✔
- **P1:** headless worker image + one-button single spawn (gui or headless).
- **P2:** tailnet-per-node join + node registry integration (115).
- **P3:** fleet spawn (N instances), LLM cost governor, scheduling across hosts.

## Acceptance (P1)
`veragensia.spawn` produces a running instance that registers as a node and (gui) streams, or
(headless) runs N budgeted agents; teardown on idle; no manual SSH.

## Non-goals
GUI desktop per headless worker; exposing daemons publicly unauthenticated; unbounded LLM spend.

## Open questions
- Authkey minting automation (Tailscale admin API token).
- Headless image base (minimal Chromium + engine + daemon, no DE).
- LLM governor policy + per-tier fleet caps (extend 115 pricing).
- Host fleet topology (multi-OVH / heterogenous) and scheduling.
