# 198 — Veragensia Foundation Integration and Native v0.1 Scope Guard Addendum

**Status:** DRAFT canonical product-direction addendum, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Amends/clarifies:** Docs 182b, 186, 187 and 188 where their constrained native-preview wording could otherwise be mistaken for the complete Agent Computer architecture.
**Foundation dependencies:** Docs 190–197 and Focusa Spec 181.

## 1. Purpose

The native Chromebook v0.1 contracts intentionally define the smallest real governed cycle that can be proven on constrained/reclaimed hardware.

Since those documents were written, Veragensia's canonical full Agent Computer architecture has become more explicit about two foundational requirements:

1. **Machine enforcement:** Focusa semantic authority must compile into actual Veragensia execution restrictions through Docs 193–196.
2. **Voice-native human interaction:** keyboard and mouse are optional peripherals in a full `voice_complete` profile under Doc 197 / Focusa Spec 181.

This addendum prevents the constrained v0.1 implementation from becoming accidental precedent against those full-product laws.

## 2. Conflict rule

When Docs 182b/186/187/188 describe a smaller preview surface and Docs 182/190–197 describe the full Agent Computer architecture:

```text
v0.1 documents
    define the immediate constrained implementation/release gate

Docs 182 + 190–197
    define the canonical full-product architecture
```

The smaller v0.1 scope is an explicit omission profile, not an architectural rejection.

## 3. Canonical full-profile composition

Any wording in older v0.1 docs listing a smaller set of full-profile defaults is superseded by:

```text
Focusa daemon/core
Focusa Desktop
Pi + Focusa Pi extension
UIAI Engine + Cockpit/browser/computer surfaces
Veragensia enforcement/control substrate
Voice/Conversation service bound to Focusa Spec 181
Veragensia native shell/session integration
```

## 4. Enforcement amendment

The v0.1 statement that an unsandboxed plugin, same UID, process label or systemd scope is not sufficient isolation remains correct and is strengthened by Doc 193.

The future governed runner MUST converge on:

```text
Focusa AuthorityDecision / CapabilityGrant
→ Veragensia EnforcementPlan
→ ExecutionPrincipal + WorkloadIdentity
→ verified machine isolation
→ dispatch
```

For the immediate v0.1 acceptance gate, one real isolated run is sufficient only if its actual containment is described honestly. If the implementation does not yet satisfy the general Doc-193 EnforcementPlan/WorkloadIdentity architecture, it MUST be labeled a bounded preview mechanism rather than canonical full-profile enforcement.

No v0.1 test may use same-user ambient `$HOME`, unrestricted session D-Bus, keyring, accessibility, microphone, compositor/input or network access and call that equivalent to the full enforcement substrate.

## 5. Resource/runtime identity amendment

The v0.1 bridge's `bridge_epoch` is an early local freshness primitive. Full-product identity follows Doc 195:

- ResourceRef + revision instead of path-as-identity;
- RuntimeIncarnation instead of PID/socket/window identity persistence;
- replica/write fencing for local/cloud work;
- explicit preserved/rebound/invalidated/unknown state across restart/restore.

A future v0.1 implementation SHOULD align its bridge epoch/run identifiers with those semantics where practical, but the initial proof need not implement the entire distributed resource model before it can prove one bounded native cycle.

## 6. Trusted human control amendment

The compact Work panel's stop/pause affordances are not the final human-control architecture.

The full product uses Doc 194:

```text
Secure Attention
+ Focusa Intervention
+ ComputerControlLease generation/fencing
+ DesktopObservation
+ OperatorDeltaReceipt
+ mandatory re-observation
```

The v0.1 stop gate remains useful proof of owned-run cancellation. It MUST NOT be described as proof of full desktop Agent Assist/takeover safety until Doc-194 controls are implemented.

## 7. Voice-native amendment

The existing v0.1 documents emphasize pointer/keyboard accessibility because they predate the voice-native constitutional requirement.

They are amended as follows:

> Keyboard/pointer support remains required compatibility/accessibility behavior. It is no longer the canonical assumption about how the owner must operate Veragensia.

A full `voice_complete` Agent Computer must pass Doc 197 with keyboard/pointer absent or disabled through a representative complete workflow.

### Immediate v0.1 posture

Voice is **not automatically added to the existing G00–G13 release gates** merely by publishing this addendum. Doing so would falsely convert a bounded first-device proof into a much larger unimplemented release.

Instead:

- native v0.1 MUST NOT claim `voice_complete`;
- native v0.1 UI/contracts MUST avoid architectural choices that make later voice parity impossible;
- all native operations SHOULD be exposed through canonical structured Focusa/Veragensia operations rather than QML-only click handlers so voice can project the same operations later;
- any approval/stop/navigation API introduced for v0.1 must be usable by future nonvisual/voice surfaces;
- a post-v0.1 full-profile gate MUST include Doc-197 voice-complete acceptance.

## 8. Microphone privacy amendment

Older docs correctly prohibit default ambient microphone capture by agent workloads.

That rule remains. Doc 197 introduces a narrower distinction:

```text
ordinary agent / Agent App microphone access
    default denied

trusted attested Voice/Conversation capture service
    may receive explicitly configured microphone capability
    under Focusa Spec 181 / Veragensia Docs 193,196,197
```

Voice-first does not mean every agent process gets microphone access.

## 9. Low-resource hardware and voice

Voice architecture must work on constrained hardware through profile placement rather than forcing every speech model on-device.

Possible posture:

```text
local low-latency capture / VAD / mute / stop / secure control
+
local or remote ASR/TTS according to profile/privacy/network/resource policy
+
Focusa canonical Conversation Ledger / operation path
```

A remote speech provider is an adapter, not conversation or authority owner.

## 10. Platform trust amendment

Exact-device bring-up in Doc 187 now also establishes an initial Doc-196 platform trust class.

A reclaimed Chromebook may validly be `T1_DEVELOPER` after owner-controlled firmware/OS/software verification while stronger trust classes remain unavailable.

Do not reject useful development hardware merely because hardware attestation is unavailable; do not represent it as stronger than proven.

## 11. Release vocabulary

Use these distinctions:

```text
native_v0.1_ready
    immediate Docs 186/187/188 evidence passes

foundation_ready
    Docs 193–196 enforcement/control/identity/trust implemented and evidenced

voice_complete
    Focusa Spec 181 + Veragensia Doc 197 acceptance passes

full_agent_computer_profile_ready
    canonical full composition and applicable 190–197 gates pass
```

One status MUST NOT be substituted for another.

## 12. Implementation dependency direction

The intended path is:

```text
bounded native v0.1 proof
→ general machine-enforcement substrate
→ stable resource/runtime identity + secure attention/control
→ trusted platform/runtime attestation
→ canonical full-profile composition
→ voice-complete interaction
→ Elastic Agent Computing at broader scale
```

Work may overlap when evidence supports it. This order is not a calendar commitment.

## 13. Final principle

> The first Chromebook proves Veragensia can inhabit a real small computer. It does not get to define the limits of what the Agent Computer ultimately is.
