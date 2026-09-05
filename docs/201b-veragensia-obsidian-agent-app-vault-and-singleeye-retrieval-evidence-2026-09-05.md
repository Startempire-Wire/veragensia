# 201B — Obsidian Agent App, Startempire Vault, and SingleEye Retrieval Evidence

**Status:** dated integration/retrieval evidence, 2026-09-05.  
**Companions:** Doc 190 Agent-First Software, Doc 201 semantic OS operations, Focusa durable-knowledge/integration docs, Focusa Spec 53 pairing.  
**Rule:** verified source findings are separated from unresolved historical-vault material.

## 1. Current Obsidian is materially agent-operable

Current official Obsidian documentation exposes an **Obsidian CLI** capable of controlling the running desktop application.

Relevant capabilities include:

```text
obsidian commands
obsidian hotkeys
obsidian command id=<command-id>
obsidian search query=...
obsidian read
obsidian create
obsidian append / prepend
obsidian move / rename / delete
obsidian tasks
obsidian tags
obsidian backlinks / links
obsidian base:query
obsidian devtools / dev:screenshot / eval
```

The CLI can target exact vaults and files.

Sources:

- <https://obsidian.md/help/cli>
- <https://obsidian.md/cli>

### Architecture consequence

For an Agent Computer, Obsidian SHOULD be treated as a structured Agent App where this CLI version is available.

Preferred route:

```text
Focusa/Veragensia capability
→ Obsidian CLI / vault operation
→ resulting file/app state
→ Evidence/Receipt as applicable
```

not:

```text
launch Obsidian
→ synthesize hotkeys/mouse for every operation
```

The Omarchy `Super + Shift + O` binding remains a human launch projection only.

## 2. Obsidian Headless

Current official Obsidian documentation also provides **Obsidian Headless** in open beta for server-side Obsidian service/sync operations without the desktop app.

Source: <https://obsidian.md/help/headless>

Potential Agent Computer value:

- remote vault synchronization;
- server/private-node vault replicas;
- backups;
- automation;
- agent access without granting the whole desktop session.

Any credential/sync integration still follows normal Veragensia/Focusa credential, ResourceRef, replica, and authority rules.

## 3. Existing Startempire Obsidian vault architecture found in connected GitHub

Current connected Focusa integration documentation records this deployed/reference relationship:

```text
Operator / Obsidian on Mac
        ↓ git sync
Obsidian vault on VPS
        ↓ sync-vault-wiki
Wiki.js
```

The same integration docs describe Wiki.js as receiving a **one-way sync from the Obsidian vault**.

The historical enrichment design references the vault path:

```text
/data/wirebot/obsidian
```

and historical-vault extraction from Markdown files.

Relevant connected-repository documents:

```text
Startempire-Wire/focusa/docs/INTEGRATION_SPEC.md
Startempire-Wire/focusa/docs/UNIFIED_ORGANISM_SPEC.md
Startempire-Wire/focusa/docs/WIKI_ENRICH_NIGHTLY_SPEC.md
```

### Boundary

Those GitHub documents describe the vault and sync pipeline. The actual `/data/wirebot/obsidian` Markdown contents are not stored in the connected GitHub repositories currently visible through the GitHub connector.

Therefore repo documentation proves **the vault connection exists**, but does not by itself provide the contents of every vault note.

## 4. Knowledge ownership

Existing Focusa organism/integration material distinguishes durable reviewed knowledge in the Wiki.js/Obsidian domain from Focusa's active cognitive/work state.

Preserve that distinction:

```text
Obsidian / reviewed knowledge
    durable owner knowledge artifacts

Focusa
    scoped active cognition, Workpoints, authority, evidence, project runtime

Conversation Ledger
    attributable interaction provenance
```

An agent may read/propose updates to vault knowledge under authorization, but the existence of a Markdown note does not silently override current Focusa Workpoint/authority or architecture provenance rules.

## 5. Agent App capability direction

Candidate Obsidian capabilities for the Veragensia Agent App catalog:

```text
obsidian.vault.list
obsidian.vault.search
obsidian.note.read
obsidian.note.create
obsidian.note.append
obsidian.note.edit
obsidian.note.move
obsidian.note.delete
obsidian.link.inspect
obsidian.command.invoke
obsidian.hotkeys.inspect
obsidian.base.query
obsidian.dev.inspect
```

Exact operations should be generated from installed Obsidian CLI/version capability discovery rather than frozen from this evidence file.

## 6. `SingleEye` retrieval result

Searches performed through connected GitHub scopes included:

```text
SingleEye
singleeye
Single Eye
```

across relevant Startempire-Wire, WPUIAI, Philoveracity, and `verioussmith` repository scopes.

### Result

No user-owned current default-branch GitHub file containing the intended **SingleEye** vault note was found.

Global GitHub results for unrelated public projects with identifiers named `SingleEye` were rejected as irrelevant.

The most likely explanation consistent with the connected architecture is:

```text
SingleEye exists/existed inside the external Obsidian vault
/data/wirebot/obsidian
```

whose connection is documented by GitHub but whose actual Markdown contents are not exposed by the current GitHub connector.

This is a **retrieval gap**, not evidence that the note does not exist.

## 7. Pairing reconciliation rule for future SingleEye recovery

When SingleEye is recovered, pairing/device ideas MUST first be reconciled against current Focusa pairing ownership:

- `docs/53-focusa-device-pairing-spec.md`;
- pairing wizard/repair companions;
- Spec 184 Ambient Operator pairing;
- Veragensia Doc 199 Companion identity/sync;
- Doc 196 platform/workload identity and attestation.

SingleEye ideas may improve or extend:

```text
physical-presence proof
visual/QR pairing UX
nearby discovery
public-key/device offer exchange
human-mediated trust transfer
multi-device handoff
wearable/phone/Agent Computer pairing
re-pair/revocation
```

but MUST NOT become a second device-token ledger or independent trust authority without an explicit owner-authorized supersession.

## 8. Retrieval acceptance for SingleEye

Do not describe SingleEye integration as completed until an authorized source copy is recovered and the following are recorded:

```text
exact note/path
source vault/revision or content digest
author/provenance if available
date/context
pairing ideas extracted verbatim/bounded
conflicts with current Spec 53/184/199 identified
accepted ideas promoted by Verious Smith III
```

Until then, references to “SingleEye pairing ideas” remain a known historical-input gap.
