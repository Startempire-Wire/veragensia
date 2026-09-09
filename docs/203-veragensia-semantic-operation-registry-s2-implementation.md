# 203 — Veragensia semantic operation registry (V201-S2) implementation

- **Status:** implemented (first slice)
- **Spec authority:** `docs/201-veragensia-semantic-os-operation-keybinding-and-voxtype-integration-spec.md` §3 (SystemOperationDescriptor) and §14 V201-S2
- **Date:** 2026-09-09
- **Scope:** the registry and its read-only projections. Execution (invoke/batch) is V201-S4 and is deliberately absent.

## 1. What exists

| Artifact | Role |
|---|---|
| `config/system-operations.json` | The registry: catalog envelope `veragensia.system_operation_catalog.v1` + descriptors `veragensia.system_operation.v1` (16 operations) |
| `scripts/veragens-operations.py` | Loader/validator + bounded projections (`catalog()`, `describe()`, `family_coverage()`); raises `RegistryError` on any contract violation |
| `scripts/veragens` | `operation list --json` and `operation describe <id> --json` (exit 2 + typed error envelope for unknown ids) |
| `tests/09-veragensia-system-operation-registry-test.py` | Contract tests: validation, id uniqueness, family coverage, authority posture, CLI projections, no-invoke guarantee |

## 2. Descriptor contract (from docs/201 §3, enforced)

Every descriptor carries exactly the spec keys: `schema`, `operation_id`
(`system.<family>[.<name>]`), `version`, `owner_runtime`, `category`, `human`
(label + hotkeys), `voice` (1–8 examples), `parameters.schema_ref`,
`preconditions`, `execution` (preferred/fallback adapters within the spec enum
+ an opaque `command_template_ref`), `risk` (consequence_class
low/medium/high + reversibility), and `result` (schema_ref +
evidence_policy_ref). `command_template_ref` values are execution-template
keys resolved by S4 — never inline commands.

## 3. Authority posture (a design rule, tested)

Every `medium`/`high` consequence operation declares
`preconditions.authority_ref_required: true` — currently: `system.window.close`,
`system.display.reload_configuration`, `system.session.exit`,
`system.capture.screenshot`, `system.clipboard.paste_history`,
`system.agent.select_foreman`, `system.dictation.toggle`. Low-risk reversible
operations (workspace navigation, focus movement) stay authority-free.
The descriptor advertises the requirement; the applicable gates still decide.

## 4. Family coverage (docs/201 §14 V201-S2)

All nine first families have ≥1 descriptor: workspace/navigation (2),
window placement/state (3), app launch/close/focus (2), audio/Bluetooth (2),
display/power (2), capture/clipboard (2), notification/history (1),
agent launch/selection (1), dictation/listening control (1).
`family_coverage()` is the release diagnostic — a family with zero
descriptors fails the test.

## 5. What this slice deliberately does not do

- No `invoke`/`batch`/`keymap inspect` subcommands (V201-S4; the CLI help
  test asserts their absence until then).
- No adapter execution, no hotkey generation, no Focusa/voice projection
  (V201-S5). Voice consumption of the same registry is the T2 boundary.
- No claim of runtime availability: whether `omarchy_cli` or a native service
  exists in the live environment is V201-S1 inventory + runtime evidence, not
  registry truth.

## 6. Verification

```bash
python3 scripts/veragens-operations.py --validate   # 16 operations, 9/9 families
python3 tests/09-veragensia-system-operation-registry-test.py
./scripts/veragens operation list --json
./scripts/veragens operation describe system.workspace.activate --json
```

## 7. Next slices

- **V201-S3** keybinding parity compiler: correlate V201-S1 live bindings
  (argument-hashed) with these operation ids; classify every binding
  (docs/201 §4.2 classification gate); surface `unmapped_gap` as a defect.
- **V201-S4** direct execution: adapter wiring, `invoke`/`batch`, owner
  interruption fencing (§15 invariant 5), exact-target verification (§15.6).
