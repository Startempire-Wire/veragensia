# AGENTS.md — Veragensia Contributor and Agent Contract

> # 🚨 AUTHENTICATION HARD STOP — READ BEFORE ANY LOGIN
> **NEVER automate with a nonrenewable resource. NO recovery code automation—ever, for any provider.** Recovery codes and finite break-glass assets are operator-only and untouchable. Unknown renewability fails closed.
>
> **GitHub renewable routes:** existing `gh` CLI/API session → existing private browser session → approved PAT/OAuth token → GitHub App token → SSH/deploy key → device OAuth → UIAI Engine in a private ephemeral Veragensia browser using approved email/password plus renewable email OTP, TOTP, passkey/security key, or normal OAuth consent → provider support/manual operator recovery without recovery codes. One failed route is not exhaustion. Never use public `os.focusa.dev` for credentials.
>
> **Mandatory provider-auth preflight:** `bash tests/02-veragensia-nonrenewable-resource-policy-static-test.sh` must pass before any login, OAuth, credential recovery, or provider-auth mutation.

This file governs work in the `Startempire-Wire/veragensia` repository. It applies to human contributors and automated agents from the repository root downward. A more specific `AGENTS.md` may refine rules for a future subtree, but it must not weaken the security, authority, or evidence requirements here.

## 1. Product identity

- Product: **Veragensia**, the Focusa Agent OS.
- Short form and future CLI/package name: **Veragens**.
- Provisioned streamable instance: **Agent Cloud Computer**.
- Public build-in-public demo: `https://os.focusa.dev`.
- `lab.focusa.dev` is reserved for another project. Do not use it.
- Canonical repository: `Startempire-Wire/veragensia`. Do not create a parallel repository, hidden replacement implementation, or second source of truth.

Veragensia is an agent/human operating environment built from an upstream base, a Veragensia overlay, Focusa primitives, UIAI Engine, Chromium, and the Focusa Workforce extension. It is not a new kernel, a deep Omarchy fork, or an unaudited cloud-agent runtime.

Core principles:

> Surfaces are interchangeable; primitives are the platform.

> Focusa decides what a governed actor may do. Veragensia makes the machine behave as though that decision is real.

> Keyboard and mouse are optional peripherals in a full `voice_complete` Agent Computer.

> Ambient does not mean globally omniscient, always-recording, or globally authoritative.

Control-plane principle:

> Cloud coordinates. Node decides. Receipts prove. Private state stays local.

## 1.1 Agent communications + GitHub 2FA portability

- The immediate private communications use case is authorized completion of an active `github.com` login with a renewable SMS OTP so Focusa build/release work can proceed. It does not authorize ambient inbox, thread, notification, or phone access. Public `os.focusa.dev` remains credential-free and must never host the paired connector or OTP workflow.
- Connector/browser state belongs only in an encrypted private operator/customer trust context behind the Focusa credential/communications broker. Agents receive short-lived, revocable `read_otp`/`inject_otp` capabilities bound to provider, enrolled phone, expected sender/message class, active challenge, and expiry—not cookies, Google/Apple credentials, or unrestricted CDP/profile access. Prefer broker-side injection and keep OTP values out of model context and evidence.
- GitHub OTP is the first bounded slice, not the final product boundary. Preserve later customer-authorized SMS thread listing, bounded reads, sends, and events behind separate explicit capabilities; an OTP grant must never widen into ambient message access.
- Android/Google Messages may be the first connector, but Veragensia lifecycle, enrollment, encrypted-state, health, revoke/re-pair, teardown, and evidence contracts must use a versioned transport-neutral connector boundary. Do not bake Chromium or Android details into shared Focusa/Veragensia types.
- **iPhone/iOS is an urgent first-class target developed in parallel.** Select only Apple-supported and user-consented integration paths; never assume private iMessage/SMS APIs, jailbreaks, or weakened isolation. Require equivalent GitHub OTP scoping, customer ownership, restart durability, audit, revocation, portability, and real-device proof for Android and iPhone. Android-only delivery is an explicitly bounded bootstrap, not completion.
- Recovery codes and other finite break-glass artifacts remain permanently unavailable to agents regardless of release urgency.

## 2. Authority and conflict order

Use this precedence when instructions conflict:

1. Explicit operator direction and repository security requirements.
2. This `AGENTS.md`.
3. `docs/183-veragensia-public-agent-computer-security-and-lifecycle.md` for the live public demo.
4. `docs/182-veragensia-focusa-agent-os-spec.md` for product direction.
5. primitive-owning Docs 190–199 for their respective domains.
6. `docs/182b-veragensia-base-os-and-overlay-detailed-spec.md` for base/overlay boundaries.
7. `docs/182c-veragensia-fleet-scale-tailnet-spec.md` for fleet growth.
8. `README.md` and subtree documentation.
9. Existing implementation patterns, only when they do not conflict with the authorities above.

Status matters: Doc 183 is a **live operational contract**; Docs 182/182b/182c and 190–199 contain product/architecture direction with their own stated status. Do not silently turn an open question in a draft spec into permanent architecture, and do not describe a committed spec as shipped implementation.

If a required decision is absent, document the ambiguity and ask. Do not invent deployment targets, control planes, ports, credentials, pricing, licensing tiers, fleet topology, microphone authority, Foreman scope, Radar semantics, or mobile sync behavior.

## 3. Read before changing

Before modifying a relevant area, read the corresponding authority completely:

| Area | Required reading |
|---|---|
| Live demo, browser profiles, lifecycle, deployment, security | `docs/183-veragensia-public-agent-computer-security-and-lifecycle.md` |
| Product or UX architecture | `docs/182-veragensia-focusa-agent-os-spec.md` |
| Base image, overlay, themes, services, installer | `docs/182b-veragensia-base-os-and-overlay-detailed-spec.md` |
| Fleet, tailnet, spawning, headless workers | `docs/182c-veragensia-fleet-scale-tailnet-spec.md`, `docs/191-*` |
| Agent-first software, Agent Apps, resolver | `docs/190-*` |
| Telemetry/privacy/anti-exfiltration | `docs/192-*` |
| Linux capability enforcement, workload identity, sandboxing | `docs/193-*` |
| Secure Attention, takeover, desktop observation/control leases | `docs/194-*` |
| ResourceRef/runtime incarnation/state transfer | `docs/195-*` |
| Boot/platform trust, runtime attestation | `docs/196-*` |
| Voice/audio/full-duplex/no-keyboard operation | `docs/197-*`, Focusa Spec 181 |
| Native v0.1 vs full-profile interpretation | `docs/198-*` |
| Omarchy plugin + trusted audio/sync services + mobile/wearable Ambient Operator | `docs/199-*`, `docs/contracts/ambient-operator-convergence-map.v1.yaml`, Focusa Specs 182–184 |
| Browser/computer execution from voice/mobile/Radar/Foreman | UIAI Veragensia computer-control/voice binding + applicable UIAI contracts |
| Repository orientation | `README.md` |

Before edits:

1. Confirm the repository root and current branch.
2. Run `git status --short` and inspect existing diffs.
3. Treat unfamiliar changes as another contributor's work; do not overwrite them.
4. Check the relevant repository-local `br` item and its acceptance criteria. A linked GitHub issue is an external discussion or public reference, not a duplicate task record.
5. Keep the change limited to the requested step.

## 4. Repository map and ownership

- `overlay/` — the only Veragensia mutation layer applied over a stock base.
- `overlay/themes/` — branded visual assets and desktop theme material.
- `overlay/services/` — OS service definitions and service integration.
- `overlay/gui/` — native presentation components where appropriate.
- `overlay/omarchy/` — proposed stock-Omarchy adapter/install/plugin/session integration.
- `scripts/` — repository-managed lifecycle, browser, deployment, and evidence helpers.
- `ops/` — auditable operational templates, including least-privilege boundaries.
- `tests/` — static and behavioral regression tests.
- `docs/182*` — product, base/overlay, and fleet specifications.
- `docs/183-*` — live public Agent Computer security and lifecycle contract.
- `docs/190-*` through `199-*` — current Agent Computer software, cloud, telemetry, enforcement, control, resource, trust, voice and Ambient Operator architecture.
- `docs/contracts/ambient-operator-convergence-map.v1.yaml` — ownership/dependency/slice map; not task status.

Do not place durable implementation in `/tmp`, an operator home directory, a transient Focusa checkout, or an unmanaged live-host script. Temporary experiments must either be removed or promoted into this repository with tests and documentation.

## 5. Base and overlay invariants

- Keep Omarchy and webtop upstream code untouched.
- Implement Veragensia behavior as an overlay, package, service, plugin, or bounded integration.
- Do not deep-fork the base to simplify a short-term change.
- Fork or replace only an explicitly approved branding surface.
- Keep installers idempotent and non-destructive for their declared target.
- A repeated overlay application must converge rather than accumulate state.
- GUI surfaces consume daemon-owned truth; they do not become independent authorities.
- Read-only integration comes before mutation controls.
- Mutating agent actions require the applicable Focusa authorization and approval path.

### 5.1 Omarchy plugin boundary

A normal Omarchy/Quickshell plugin is a **presenter/operation-forwarder**, not an isolation or authority boundary.

Therefore:

- do not store credential values or broad secrets in plugin/QML state;
- do not make a plugin the Focusa reducer, Foreman/Radar state store, microphone authority, credential broker, EnforcementPlan compiler, or direct canonical database writer;
- use supported user plugin/config paths and validate manifests;
- do not modify package-owned Omarchy source under the upstream installation;
- keep trusted audio/sync/enforcement logic in separate bounded workloads/services;
- a visually trusted QML approval dialog is not hardened Secure Attention by itself.

### 5.2 Ambient ownership

- Focusa owns Project Foreman, Radar, Conversation and Ambient semantic primitives.
- Veragensia owns Linux/Omarchy/audio/sync/enforcement integration.
- UIAI owns browser/computer execution and proof.
- Wirebot/Context Core may own broader life/portfolio context in the Startempire reference deployment.
- phone/earbuds/wearables are paired surfaces and observation endpoints, never automatic application/architecture authority.

## 6. Trust classes

Every browser, desktop, audio, mobile-sync, or Agent App workflow must identify its trust class before credentials or privileged actions are considered.

### `public_demo`

`os.focusa.dev` is public, login-free, observable, and untrusted for privileged identity.

It must never retain:

- operator or customer identities;
- GitHub, AppVeyor, cloud, DNS, payment, or vault sessions;
- passwords, API keys, tokens, OTP seeds, recovery codes, cookies, or OAuth grants;
- personal browsing data or customer content;
- private Ambient Operator conversation/location streams.

The public profile is for demonstrations, synthetic data, public research, and governed product interaction only.

### `ephemeral_auth`

Privileged provider work belongs in a separate disposable browser profile/context or private node:

- use a separate loopback CDP endpoint;
- inject secrets through approved brokers or stdin-only private pipes;
- never place secret values in arguments, logs, screenshots, model-visible text, or repository files;
- destroy profile, process, and temporary helpers after use;
- prove the private endpoint closed and profile absent;
- prove the public profile remains free of sensitive-origin cookies.

Prefer an authenticated API-native action before launching a privileged browser. GitHub webhook inspection/redelivery is a proven provider-retrigger pattern.

### `private_operator`

A private operator/Ambient context must have explicit identity, authorization, retention, audit, revocation and paired-device contracts. Do not treat root, SSH, CDP, Docker, tailnet, Bluetooth, filesystem access, paired-phone status, or voice recognition as implicit permission.

**Transport capability is not authorization.**

### Platform trust class

Do not overclaim signed/measured/hardware-attested trust. Current stock Omarchy developer hardware defaults to the evidenced Doc-196 trust posture (normally `T1_DEVELOPER`) unless a stronger boot/attestation path is separately implemented and proven.

## 7. Secret and customer-data handling

- **Never automate with a nonrenewable resource.** Safe replenishment or reissuance must be proven before any agent, subprocess, browser workflow, or Veragensia node consumes, tests, rotates, invalidates, or spends a resource. Unknown renewability fails closed. Finite break-glass artifacts, one-time emergency credentials, irreversible quotas, and anything that cannot be replenished are operator-only and untouchable.
- **No recovery code automation—ever, for any provider.** Never retrieve, inspect, enumerate, parse, reveal, copy, inject, test, consume, request, rotate, or use a recovery code, and never ask the operator to spend one. Use an authorized session or renewable approved route; otherwise stop and report the blocker. This supersedes every historical workflow or fallback.
- **GitHub renewable-access ladder:** existing authenticated `gh` CLI/API session; existing private browser session; approved PAT/OAuth token; GitHub App installation token; authorized SSH/deploy key; GitHub device OAuth; UIAI Engine with a private ephemeral Veragensia browser using approved email/password plus renewable email OTP, authenticator/TOTP, passkey/security key, or normal OAuth consent; then provider support/operator-controlled manual recovery without recovery-code automation. Never use the public `os.focusa.dev` profile for credentials. Destroy private contexts and prove zero residue. One failed route never authorizes a recovery code; stop only after every applicable renewable route fails.
- Never print, paste, commit, snapshot, or narrate secret values.
- Retrieve only the exact required credential field from an approved manager.
- Use synthetic fixtures for mutation and destructive-path tests.
- Preserve signed authority history and customer records immutably.
- Redact receipts so they prove the action without carrying credentials or personal data.
- If a secret reaches a public or persistent surface, stop the exposure, report it, revoke/rotate as applicable, scrub storage, and record value-free evidence.
- Public demo data must be clearly synthetic and safe to reset.
- Raw conversation/audio, exact GPS and other high-sensitivity Ambient content follow their explicit privacy/retention contracts and are not generic telemetry.

## 8. Live-demo invariants

The public demo is intended to remain continuously available.

Required stable host paths and mounts are defined by Doc 183. Important invariants:

- the extension deploys from the stable `workforce-extension` parent, never a transient build mirror;
- the repository and extension are mounted through stable parent paths where inode replacement can occur;
- the demo daemon binds only to container loopback;
- the container has no Docker socket and no general host filesystem;
- the expected extension ID is verified, not guessed;
- persistent mode remains enabled unless the operator explicitly authorizes downtime;
- missing Chromium, CDP, manifest, service worker, extension ID, daemon health, or public HTTP health is a hard failure.

Expected status posture:

```text
container: running
connector: running
keeper: alive
chrome: healthy
extension: ready
demo_daemon: healthy
owner_drift: none
```

Do not weaken a hard gate into a warning to make a deployment appear green.

Doc 199 does not authorize adding private Ambient Operator credentials, phone context or meeting data to the public demo.

## 9. Permission and self-healing boundaries

Self-healing must be narrow and deterministic.

- Repair ownership only on the stable extension and demo-data scopes named in Doc 183.
- Never recursively `chown`, `chmod`, delete, or rebuild unrelated `/home/wirebot` content.
- Never use broad wildcard cleanup against user, customer, daemon, browser, conversation, sync-queue, or evidence data.
- Preserve live databases, audit ledgers, credentials, user files, and unknown state.
- Cleanup is limited to verified rebuildable staging, rollback, cache, and temporary artifacts.
- Keep at most the bounded rollback state defined by the deployment transaction.
- A stuck mobile/audio service does not justify deleting canonical Focusa conversation/work state.

## 10. Deployment contract

Repository state is the source of truth. A live fix is incomplete until it is mirrored here, tested, documented, committed, and pushed.

Canonical public-extension deployment is an atomic transaction:

1. Build with the pinned toolchain.
2. Stage under the stable parent.
3. compare local and remote manifest SHA-256 values;
4. retain one bounded rollback;
5. atomically promote the staged output;
6. invoke only the narrow audited root wrapper;
7. verify browser, extension, ownership, daemon, and public HTTP health;
8. restore rollback if activation fails.

Remote privilege is limited to `scripts/uiai-lab-remote-control` and the matching `ops/sudoers/` template. Do not grant arbitrary passwordless root or expand the wrapper without explicit review, tests, and rollback documentation.

Never deploy by manually copying selected files into live locations as a substitute for this transaction. Do not run live deployment commands without explicit operator authorization and a current spec/acceptance path.

Native Omarchy/Companion implementation uses its own target-specific transaction and acceptance gates; do not reuse the webtop public-demo transaction as proof of native readiness.

## 11. Failure handling

No silent failures.

- Do not discard meaningful stderr or use empty catches.
- Do not append `|| true` to required operations.
- Best-effort behavior is allowed only when explicitly non-critical and documented as such.
- Report the exact failing command, bounded error, and suspected cause.
- File an issue for real product, infrastructure, or workflow defects only when a public external reference is needed; canonical execution state remains in `br`.
- Include a concrete fix plan and acceptance criteria.
- If the canonical lifecycle or deployment mechanism breaks, fix that mechanism rather than inventing an unmanaged bypass.
- Mobile/audio/background suspension, stale sync, route changes and unavailable microphone are explicit runtime states, not silent fallbacks.

## 12. Testing and acceptance

Minimum checks for repository changes:

```bash
bash tests/01-veragensia-lab-lifecycle-static-test.sh
git diff --check
```

Additional requirements by scope:

- Shell changes: run `bash -n` on every modified shell script.
- Lifecycle changes: test missing-manifest, ownership drift, restart/recreation, extension readiness, and daemon restoration paths as applicable.
- Deployment changes: test staging, checksum mismatch, atomic promotion, bounded rollback, and failed-activation recovery.
- Sudoers changes: validate with `visudo -cf` before installation.
- Overlay changes: prove idempotency and that upstream base files remain untouched.
- Browser/security changes: prove context isolation, cleanup, closed private endpoints, zero public auth residue, and public health restoration.
- Product contracts: test producer and consumer behavior, cross-version compatibility, and live end-to-end delivery where applicable.
- **Omarchy plugin changes:** run `omarchy plugin validate` on the plugin in a qualified target environment; prove plugin unload/reload/rescan and no package-owned upstream modifications.
- **Trusted audio changes:** prove microphone/output endpoint inventory, headset route/profile changes, hardware/software mute posture where available, no ambient microphone grant to unrelated worker/browser/plugin, and safe behavior on Bluetooth disconnect.
- **Companion sync changes:** prove device pairing/revocation, encryption, sequence/replay defense, idempotency, offline queue restart, acknowledgement/reconciliation and stale-state labeling.
- **Foreman/Radar/Ambient changes:** prove exact Workstream identity, no cross-Workstream state bleed, no observation-to-authority shortcut, and no direct mobile writes into Focusa persistence.
- **Voice-complete changes:** run at least one representative workflow with keyboard/pointer absent or disabled and preserve utterance → operation → Evidence/Receipt lineage.
- **UIAI Ambient changes:** prove normal UIAI observation/control/verification path, control-lease fencing, and re-observation after human takeover.

Tests must use synthetic fixtures and leave zero residue. A green producer test does not prove a consumer received or enforced the contract.

## 13. Planning and specification proportionality

Use **`br` only** for repository-local task tracking. Do not introduce alternate command names in Veragensia documentation, scripts, or agent instructions.

- Maintain exactly one canonical task record for each unit of work.
- Do not duplicate the same backlog in `br`, GitHub issues, markdown checklists, or another tracker.
- When a public GitHub issue is useful, link it from the `br` item with `external-ref`; keep execution state and dependencies in `br`.
- Capture newly discovered gaps as concise `br` items with evidence and a clear outcome.
- Do not pre-create detailed specifications merely because a gap exists.
- The operator and planning agent decide whether related discoveries should be merged, deferred, closed, researched, or promoted into a detailed specification.
- Require a detailed specification when work introduces or materially changes architecture, trust boundaries, persistent data, public interfaces, privilege, deployment/rollback semantics, licensing, or cross-system contracts.
- Bounded documentation corrections, test additions, and implementation work under an existing exact contract may use acceptance criteria directly in the `br` item.
- A planning item closes when its decision or approved plan is durable; an implementation item closes only when its acceptance evidence is durable.

The stable implementation slices in Docs 182/190–199 and `docs/contracts/ambient-operator-convergence-map.v1.yaml` are **requirements/decomposition inputs, not task status**. Materialize them into `br`; never update the specs as a substitute for the task graph.

## 14. Documentation rules

- Update documentation in the same change when behavior or operating contracts change.
- New specifications, plans, guides, and notes use `<number>-<descriptive-name>.md`.
- Keep `README.md` concise; put operational detail in a numbered document.
- Mark documents as `draft`, `live operational contract`, `superseded`, or equivalent.
- Record acceptance criteria, rollback, and evidence steps for infrastructure changes.
- Preserve historical decisions; supersede them explicitly rather than rewriting history invisibly.
- Never copy private control-plane specifications or secrets into this public repository. Public docs may reference private spec numbers and bounded interfaces only.
- Historical proposal labels such as Radar `Spec 164` or Ambient Voice `135M` must not overwrite current Focusa numbering; use current Focusa Specs 182–184.

## 15. Change and Git discipline

- Work on the existing repository and intended branch; do not create a remote, fork, or branch without authorization.
- Make small, reviewable commits using Conventional Commits.
- Do not use destructive Git operations such as `reset --hard`, `clean`, or unapproved history rewriting.
- Do not overwrite unrelated or unrecognized work.
- Run required checks before committing.
- Push normal code/documentation changes to the intended remote before declaring them complete.
- Link the relevant issue when appropriate and leave a concise evidence-backed handoff.

The canonical tracker is a repository-local beads_rust workspace operated with `br`. If `.beads/` has not yet been initialized, do not create a parallel backlog elsewhere; initialize it once under operator authorization, then link any existing GitHub issue as an external reference.

## 16. Growth rules

Veragensia is expected to grow, but growth must preserve its contracts.

### New base targets

Add target-specific adapters behind the base/overlay contract. Do not let Chromebook, Omarchy, VM, container, mobile OS, or future platform details leak into every component.

### New services and GUI surfaces

Define stable, versioned IPC contracts. Keep daemon/node authority separate from presenters. Start read-only, then add governed mutation and approval behavior.

For Omarchy specifically, keep first-party trusted behavior behind service contracts; Quickshell plugins remain thin presenters/operation-forwarders.

### Audio and Ambient services

Trusted audio capture, Companion sync and owner-context projection remain independently scoped workloads. No broad same-UID microphone, phone-context, or precise-location authority.

### Fleet and tailnet

Keep daemons private, enrollment scoped, budgets bounded, and teardown explicit. Do not expose unauthenticated daemon ports or permit unbounded agent/LLM spend.

Tailscale/private networking may carry Companion bulk sync, but transport reachability is not Focusa application authority.

### Licensing

Premium behavior fails closed. Unknown, invalid, stale, or internal tiers receive no premium capability. The base desktop remains usable where the product spec requires it.

### Browser and provider automation

Model trust class, identity, scope, retention, cleanup, and evidence as first-class inputs. Prefer reusable UIAI capabilities over one-off CDP scripts, but do not claim a capability exists before it is implemented and proven.

### Mobile clients

Use supported Android/iOS APIs and model background/suspension restrictions honestly. A mobile app is a paired edge adapter, not a replacement Focusa daemon or Veragensia kernel.

### Repository structure

A future subtree may add its own `AGENTS.md` for specialized rules. It may tighten this contract, add platform-specific gates, or define local ownership. It may not weaken public-demo isolation, secret handling, immutable authority, least privilege, conversation/privacy boundaries, or evidence requirements.

## 17. Definition of done

A change is complete only when applicable items are true:

- requested scope implemented without unrelated expansion;
- authority and trust boundaries preserved;
- tests and syntax checks pass;
- rollback and failure paths are tested or documented;
- live behavior matches repository state;
- no credentials, personal data, temporary helpers, raw test conversation/location data, or test residue remain;
- documentation reflects current behavior;
- canonical `br` item updated with bounded evidence;
- changes committed and pushed;
- public demo health remains green when it is in scope.

Handoff should state:

1. exact files and commits;
2. tests and evidence run;
3. live deployment state, if any;
4. known blockers and open issues;
5. the next authorized step.
