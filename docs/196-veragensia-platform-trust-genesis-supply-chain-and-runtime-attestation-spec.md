# 196 — Veragensia Platform Trust, Genesis, Software Supply Chain, and Runtime Attestation

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Dependencies:** Docs 193–195; Focusa architecture-authority cryptographic model, node identity, entitlement, Runtime Constitution, temporal authority; UIAI entitlement/runtime identity; upstream Linux/boot/package trust mechanisms.

## 1. Decision

An Agent Computer needs a defined answer to:

> Why should Focusa, the owner, or another Agent Computer trust that this machine is actually running the software/policy it claims to be running?

Trust starts before the agent process.

```text
platform / boot posture
        ↓
owner enrollment
        ↓
node identity
        ↓
Veragensia trusted substrate
        ↓
Focusa / UIAI / Pi / first-party surface verification
        ↓
workload identity + runtime attestation
        ↓
capability eligibility
```

Not every machine must have identical hardware trust. The posture must be explicit and capabilities can depend on it.

## 2. Foundational laws

1. **First boot is a security/authority genesis event.** Do not silently inherit product authority from a generic Linux installation.
2. **Platform trust and user authority are separate.** Secure Boot does not decide what the human wants.
3. **Software signature is not runtime authority.** A correctly signed binary still needs a grant.
4. **Source/repository identity is not runtime attestation.** A Git commit is not proof the running process matches it.
5. **Node identity, workload identity and runtime attestation are separate.**
6. **Mutable runtime posture does not change stable owner/agent principal identity.**
7. **Trust posture is graded and explicit.** Unsupported hardware can remain useful without pretending to provide stronger attestation.
8. **Critical first-party components are verified as a set.** Focusa, Veragensia, UIAI, Pi integration, policy bundle and Agent App resolver compatibility are not independently assumed compatible.
9. **Application descriptors are not self-authenticating.** Agentability/capability claims bind to software/image/descriptors and observed evidence.
10. **Updates can invalidate compatibility and attestation.** Upgrade means re-evaluate, not preserve green state by inertia.
11. **Rollback cannot silently revive revoked software/policy.**
12. **Time-sensitive trust uses Focusa Temporal Authority semantics.**
13. **Attestation is evidence for policy, not architecture authority.**

## 3. Platform trust classes

Initial portable classes:

```text
T0_UNVERIFIED
    boot/runtime integrity not established

T1_DEVELOPER
    pinned/checksummed software and owner-controlled machine; no hardware measured trust required

T2_SIGNED_BOOT
    verified boot chain/signature policy established

T3_MEASURED_BOOT
    boot/runtime measurements available and policy-evaluated

T4_HARDWARE_ATTESTED
    hardware-backed device identity/measurement acceptable to policy
```

The exact implementation may vary by hardware/platform.

A recycled Chromebook may legitimately operate at `T1_DEVELOPER` while a production financial Agent Computer requires a stronger class.

## 4. Genesis sequence

A new Agent Computer SHOULD progress through:

```text
platform inspect
→ establish trust class
→ owner enrollment
→ create/restore node identity
→ verify Veragensia substrate
→ verify Focusa runtime and contracts
→ verify UIAI runtime/contracts
→ verify Pi/reference harness package where present
→ verify policy/constitution bundles
→ install capability resolver/app catalog trust roots
→ perform private pairing
→ generate genesis receipt
→ become eligible for profile capabilities
```

No stage implies the next one passed.

## 5. Owner enrollment

Owner enrollment binds the machine to the deployment's Canonical Owner Principal without copying the owner's private architectural signing key onto ordinary runtime nodes unless an explicit key-custody design allows it.

It records:

- owner principal ref;
- deployment/tenant ref;
- node identity;
- trust class;
- enrollment authority/signature;
- revocation/recovery path;
- timestamp/temporal confidence;
- privacy/trust profile.

## 6. Node identity

Reuse the existing Focusa durable node identity where it owns product-node semantics.

Veragensia may project additional platform measurements but MUST NOT mint a conflicting second node identity for the same Focusa enrollment domain.

Node identity does not prove software posture by itself.

## 7. `RuntimeAttestation`

```yaml
schema: veragensia.runtime_attestation.v1
runtime_attestation_id:
node_identity_ref:
runtime_incarnation_ref:
platform_trust_class:
boot_measurement_ref:
os_release_ref:
kernel_ref:
veragensia_release_ref:
veragensia_digest:
focusa_release_ref:
focusa_digest:
uiai_release_ref:
uiai_digest:
pi_package_ref:
pi_package_digest:
runtime_constitution_ref:
policy_bundle_digest:
agent_app_registry_digest:
enforcement_compiler_digest:
measured_at:
attestor_ref:
fresh_until:
signature_ref:
```

Absent components are explicit, not omitted ambiguously.

## 8. Workload attestation

Doc 193 WorkloadIdentity references a runtime attestation or derived workload measurement.

A privileged broker checks:

```text
stable workload identity
+ code/image digest
+ policy digest
+ node/runtime trust posture
+ fresh capability grant
```

before accepting a consequential request.

## 9. Software supply-chain binding

Every first-party and Agent App component considered trusted for governed operation should have:

- source/release provenance;
- content digest;
- signature/verification status where supported;
- expected publisher/authority;
- declared schema/protocol compatibility;
- SBOM/provenance where available and useful;
- revocation status;
- update channel;
- rollback compatibility.

A package being present in a repository or distro does not make it an approved Agent Computer component automatically.

## 10. Agent App descriptor attestation

Doc 190 Agent App descriptors bind:

```yaml
software_digest_ref:
descriptor_digest:
capability_schema_digest:
agentability_claim:
agentability_evidence_refs: []
compatibility_refs: []
publisher_ref:
signature_ref:
```

Agentability class is not accepted solely from vendor/self-description.

Veragensia may lower an application's effective Agentability/trust when runtime evidence contradicts its declared surface.

## 11. First-party compatibility bundle

A full Agent Computer release/profile should pin a compatibility set:

```yaml
schema: veragensia.first_party_compatibility_bundle.v1
veragensia:
focusa:
focusa_desktop:
pi_focusa_extension:
uiai_engine:
uiai_cockpit:
operation_registry_digest:
contract_bundle_digests: []
minimum_platform_trust:
known_incompatible: []
```

A healthy individual process does not prove bundle compatibility.

## 12. Update transition

Before update:

```text
verify signed/pinned candidate
→ resolve compatibility
→ preview affected capabilities
→ preserve rollback state
→ install atomically where applicable
→ re-attest runtime
→ re-run capability/enforcement checks
→ enable upgraded capabilities
```

If new runtime attestation fails, do not preserve old trust/capability claims merely because the process starts.

## 13. Rollback and revocation

Rollback is allowed only to a release/policy set that remains:

- trusted;
- compatible with persisted state;
- not revoked;
- supported by current authority policy.

A known-vulnerable or revoked version cannot become trusted again because an OS snapshot restored it.

## 14. Secure/Measured Boot relationship

Veragensia may use platform mechanisms such as signed boot chains, TPM-backed measurements and hardware-bound encrypted credentials where available.

The architecture does not require a single vendor-specific mechanism.

The trust result is represented as a typed posture with evidence rather than a boolean `secure=true`.

## 15. Disk and local data protection

Trust profiles should declare at-rest posture for:

- Focusa state;
- Conversation Ledger/audio;
- browser/private profiles;
- credential broker state;
- Agent App data;
- cached Evidence/artifacts.

Hardware-backed encryption MAY be required for higher trust classes.

Unlocking storage grants access to data according to OS credentials but does not grant agent capability automatically.

## 16. Cloud Agent Computer trust

Cloud nodes require the same logical model:

```text
provider/host evidence
→ node identity
→ runtime incarnation
→ image/software measurements
→ workload identity
→ capability eligibility
```

Provider control-plane claims are evidence inputs, not Focusa authority.

A resumed/recreated Cloud Agent Computer receives a fresh runtime incarnation and re-attestation.

## 17. Voice trust relationship

Voice-complete profiles depend on trusted audio/control services.

The microphone capture service, speech renderer, transcript store and secure-attention service each carry workload/runtime identity. A fake Agent App cannot claim to be the trusted Focusa/Veragensia voice merely by producing audio that sounds the same.

Synthetic voice similarity is presentation, never cryptographic identity.

## 18. Genesis Receipt

```yaml
schema: veragensia.genesis_receipt.v1
agent_computer_ref:
owner_enrollment_ref:
node_identity_ref:
platform_trust_class:
runtime_attestation_ref:
compatibility_bundle_ref:
profile_ref:
capabilities_enabled: []
capabilities_blocked: []
created_at:
evidence_refs: []
```

## 19. Acceptance invariants

A trusted-profile implementation proves:

1. changed first-party binary/image digest changes runtime attestation;
2. incompatible bundle does not report ready;
3. untrusted Agent App descriptor cannot self-promote to A4;
4. revoked runtime version cannot regain trust through rollback alone;
5. cloud recreate/restore advances runtime incarnation and re-attests;
6. workload identity mismatch blocks privileged brokers;
7. stable owner/agent identity does not change merely because software upgrades;
8. lower-trust hardware is labeled honestly rather than denied useful local operation universally;
9. trusted voice/control workloads are distinguishable from ordinary applications.

## 20. Final principle

> An Agent Computer must know not only who is asking and what they are allowed to do, but what machine and software is actually doing it.
