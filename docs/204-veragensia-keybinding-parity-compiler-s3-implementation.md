# 204 — Veragensia keybinding parity compiler (V201-S3) implementation

- **Status:** implemented (demo proving-ground slice)
- **Spec authority:** `docs/201-veragensia-semantic-os-operation-keybinding-and-voxtype-integration-spec.md` §4 (keybinding projection/parity), §4.2 (classification gate), §14 V201-S3, §15 invariants 2 and 8
- **Date:** 2026-09-09
- **Scope:** read-only compilation of live bindings into a classified projection. Never executes bindings, never mutates the desktop, never grants authority.

## 1. What exists

| Artifact | Role |
|---|---|
| `scripts/veragens-keymap-parity.py` | The compiler: correlates S1 live bindings with S2 operations, applies the classification gate, renders docs/201 §4-style chords, detects drift |
| `config/keybinding-projection.json` | Projection rules: dispatcher + optional argument-sha256 → operation id, with a source class |
| `scripts/veragens` | `keymap inspect --json --inventory <S1-report> [--rules] [--baseline]` |
| `tests/10-veragensia-keymap-parity-test.py` | Contract tests: gate behavior, chord style, invariants 2 and 8, CLI end-to-end |

## 2. How correlation works (and why it is chord-independent)

Projection rules match a binding's **dispatcher** plus, optionally, its
**argument digest** — never the chord. This implements docs/201 §15
invariant 2: remapping a hotkey does not change the semantic operation
identity. Argument-digest rules are environment-scoped (the demo's terminal
rule binds to the exact exec argument digest only); dispatcher-only rules
(`killactive`, `fullscreen`, `exit`) apply wherever those dispatchers exist.
Native Omarchy qualification adds its own rules derived from the live
Omarchy keymap; the rule file is data, extensible without code change.

## 3. Classification gate (docs/201 §4.2)

Every live binding receives exactly one classification:
`semantic_operation` (matched a rule), `application_internal` (non-semantic
dispatcher such as `exec` without a matching digest rule),
`text_input`/`hardware_firmware`/`unsupported_platform` (reserved classes
for richer sources), or `unmapped_gap` — recorded as a release defect
(`unmapped_gap_is_release_defect: true`) with its own count. Exit status
stays 0: the report is the deliverable, the counts are the signal.

## 4. Drift detection (docs/201 §15 invariant 8)

`--baseline <prior-report>` diffs the current projection against a stored
one by binding identity (binding_ref = sha256 of the binding tuple) and
emits `projection_drift` with added/removed/changed lists. A changed Omarchy
keymap therefore surfaces as explicit drift instead of silently breaking
agent control. Changed = operation_ref or classification moved.

## 5. Live verification (demo proving ground)

```bash
veragens keymap inspect --json --inventory <S1 report>
# classified: 4 | unmapped_gap: 0
#   SUPER + RETURN -> semantic_operation system.app.launch.terminal
#   SUPER + Q      -> semantic_operation system.window.close
#   SUPER + F      -> semantic_operation system.window.fullscreen
#   SUPER + SHIFT + Q -> semantic_operation system.session.exit
```

The full S1→S3→S2 chain runs inside the demo container against the mounted
repo; native acceptance (full Omarchy keymap coverage) completes on
qualified hardware per docs/200a T1A.

## 6. What this slice deliberately does not do

- No execution, no hotkey generation, no keymap mutation (S4 owns execution;
  §4.3 keeps generated hotkeys optional and non-load-bearing).
- No claim that the demo's four rules generalize to native Omarchy: the
  native keymap (~283 upstream commands in the S1 baseline) will produce
  `unmapped_gap` records until its rules are added at qualification — that
  is the compiler doing its defect-surfacing job, not a failure of it.
