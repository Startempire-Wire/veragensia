# 183 — Veragensia Public Agent Computer Security and Lifecycle

**Status:** live operational contract
**Live surface:** `https://os.focusa.dev`
**Related:** specs 182/182b/182c; WPUIAI/uiai-engine#102; Startempire-Wire/veragensia#1
**Tracking:** repository-local `br` items are canonical once initialized; linked GitHub issues are external references, not duplicate task records.

## 1. Goal

The public Veragensia demo is constantly available as a real agent computer and build-in-public product surface, while remaining isolated from operator/provider credentials and independent of transient Focusa build workspaces.

## 2. Trust boundary

`os.focusa.dev` is a **public-demo trust class**:

- never retain operator GitHub, AppVeyor, vault, cloud, payment, or personal sessions;
- never use the public profile as the default privileged-auth browser;
- privileged OAuth belongs in an ephemeral private browser context/node;
- if emergency auth occurs in the public desktop, stop public access first, scrub all auth storage, verify zero residue, then reopen;
- root/CDP access is transport capability, not authorization.

The container has no Docker socket and no general host filesystem. Host mounts are bounded:

- `/home/wirebot/webtop` → `/config` (desktop/browser state);
- `/home/wirebot/uiai-lab/workforce-extension` → `/extroot:ro`;
- `/home/wirebot/uiai-lab/veragensia-demo` → `/veragensia-demo`;
- `/home/wirebot/veragensia` → `/veragensia:ro`.

## 3. Stable extension deployment

The public extension must never mount the shared OVH Focusa build mirror. That mirror is intentionally synchronized with `rsync --delete` and can change between builds.

Canonical stable parent:

```text
/home/wirebot/uiai-lab/workforce-extension
└── dist/
```

Canonical deploy command on KH:

```text
uiai-lab-push
```

Transaction:

1. Build locally with the pinned Node runtime and `scripts/build.mjs`.
2. Rsync to `dist.stage.<pid>` on the stable OVH parent.
3. Compare local/remote manifest SHA-256.
4. Move current `dist` to one bounded rollback directory.
5. Atomically promote staged `dist`.
6. Invoke the narrow root lifecycle wrapper.
7. Verify Chromium CDP, exact extension ID, owner drift, demo daemon, and public HTTP 200.
8. Restore rollback if activation fails.

## 4. Lifecycle and self-healing

Canonical OVH owner: `/usr/local/bin/uiai-lab-live`.

Persistent mode is mandatory for the build-in-public demo:

```text
uiai-lab-live persist on
```

Keeper cadence: 30 seconds. It reconciles:

- container running;
- Cloudflare connector running;
- stable extension manifest present;
- stable extension and demo-data ownership = `wirebot:wirebot`;
- Chromium CDP healthy;
- expected extension loaded;
- in-container demo daemon healthy;
- public URL available.

`status` must expose:

```text
container: running
connector: running
keeper: alive
chrome: healthy
extension: ready
demo_daemon: healthy
owner_drift: none
ext_id: ohfbbkpacpcapicpgplnnmifmlnmjggj
```

Permission repair is exact-scope only. Never recursively chown unrelated `/home/wirebot` data.

## 5. Desktop-session-safe Chromium launch

A recreated webtop generates a new per-session DBus address. Launchers must derive `DBUS_SESSION_BUS_ADDRESS` from the active `plasmashell` process and set `XDG_RUNTIME_DIR=/config/.XDG` before running Chromium as `abc`.

Missing desktop environment, extension manifest, CDP, service worker, or expected extension ID is a hard failure—not an informational warning.

## 6. Demo daemon

The canonical released `/usr/local/bin/focusa-daemon` is copied into each recreated container. Persistent sample data lives at `/home/wirebot/uiai-lab/veragensia-demo` and mounts at `/veragensia-demo`.

Runtime:

```text
FOCUSA_BIND=127.0.0.1:8790
FOCUSA_DATA_DIR=/veragensia-demo/data
FOCUSA_TEST_MODE=1
```

Health: `http://127.0.0.1:8790/v1/health` from inside the container. The daemon never binds publicly.

## 7. Narrow remote authority

KH `uiai-lab-push` connects as `wirebot`. It cannot execute arbitrary root commands. OVH installs:

- `/usr/local/sbin/uiai-lab-remote-control`;
- `/etc/sudoers.d/uiai-lab-remote-control`.

Only `sync-activate` and `status` are accepted by the wrapper. Sudoers grants only that wrapper.

## 8. Private provider/OAuth procedure

Try API-native recovery first. Example: an exact GitHub push webhook can be redelivered through the authenticated repository-hooks API to retrigger AppVeyor without a browser login or a new commit.

When authenticated provider UI is still required, use a **separate ephemeral profile**:

1. Keep the public demo on its normal CDP/profile (currently `:9333`).
2. Launch a headless Chromium with a disposable profile and separate loopback CDP port (proven: `:9444`).
3. Inject vault values through stdin-only pipes; never command arguments, persistent files, logs, snapshots, or model-visible output.
4. Complete OAuth/provider action and capture value-free receipts.
5. Terminate only the private browser.
6. Destroy its profile and helper scripts.
7. Prove its CDP port closed and profile absent.
8. Prove the public profile has zero sensitive-origin cookies and full extension/daemon/public-HTTP health.

If separate context creation is unavailable, stop public access before using its profile, then scrub cookies, local/session storage, IndexedDB, login/web data, and history before reopening.

The proven 2026-08-28 flow used GitHub webhook redelivery to create exact-main AppVeyor build 113, then `rbw` password + one-use GitHub recovery code in an isolated profile to cancel superseded PR builds. The private port/profile were destroyed; public sensitive cookie count remained zero.

## 9. Security improvements still required

Tracked in WPUIAI/uiai-engine#102 and Veragensia#1:

- first-class external CDP attach/adopt;
- popup/OAuth target tracking;
- broker-bound recovery-code challenge resolution;
- verified `storage.scrub` operation;
- enforced `public_demo`, `ephemeral_auth`, and `private_operator` context classes;
- separate public view and governed private control paths;
- continuous alerting for extension/CDP/daemon/auth-residue drift;
- repo-managed installation of live scripts and sudoers templates.

## 10. Combination opportunities

- UIAI read/snapshot + Veragensia desktop + Focusa evidence receipt: semantic execution with human-visible proof.
- Tailnet browser mesh + private auth context: operator credentials remain on trusted nodes while public research stays on OVH.
- rbw/Aegis broker + CDP-bound secret fill: no secrets in transcripts.
- Focusa background jobs + provider browser transactions: durable build dispatch, browser receipt, and completion event.
- HyperFrames + browser evidence: turn verified UI flows into deterministic product demos.
- Stripe/commerce tools + private browser context: governed provider setup without exposing payment/admin sessions publicly.
