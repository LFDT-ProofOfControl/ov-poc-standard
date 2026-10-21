# Crosswalk: IETF Internet-Drafts for Agent Action Evidence

**Framework type:** Evidence formats (fourteen individual-submission Internet-Drafts built on
SCITT and COSE)
**Relationship:** Candidate evidence formats. The drafts define records that a Proof-of-Control
claim could carry its evidence in. They do not grade evidence, and using them places a claim at
no Tier.

## The Relationship

Proof-of-Control says what the evidence must show. These drafts define the bytes for part of
that evidence: a signed record of one agent action, refusals and blocks included; a producer-run
append-only log whose checkpoints other parties verify; canonicalization and digest
declarations; selective disclosure; records exchanged across an organizational boundary; a way
to ask a counterparty for evidence; the model, runtime and hardware facts behind an action, each
labelled with how it was obtained; and a join from a record to the OpenTelemetry trace that
observed the same action.

For each requirement, the tables below name the draft section that defines a field or rule an
implementation could use as evidence, and say where no draft does. "Maps to" means the format
can carry the evidence. It does not mean that a deployment using the format meets the
requirement: that turns on the deployment's gateway, keys, witnesses and claim register.

Mapped against Working Draft v0.1, October 30, 2026, at commit `93d0e28` (chapters C1 to C10 in
`0.1/en/`, and the claim set in `schema/`), and against each Internet-Draft at the posted
revision below. Section numbers are those revisions'.

## The Drafts

| Cited as | Internet-Draft | Authors | Rev, date | What it defines |
| --- | --- | --- | --- | --- |
| AAC | [draft-mih-scitt-agent-action-capsule](https://datatracker.ietf.org/doc/draft-mih-scitt-agent-action-capsule/05/) | S. Mih | -05, 2026-09-26 | The Agent Action Capsule: a digest-committed record of one agent action and its disposition, a COSE_Sign1 Producer Envelope, and SCITT registration |
| SD | [draft-mih-scitt-agent-action-capsule-sel-disc](https://datatracker.ietf.org/doc/draft-mih-scitt-agent-action-capsule-sel-disc/00/) | S. Mih | -00, 2026-06-19 | Per-field selective disclosure for Capsule payloads: salted-hash commitments and decoy digests |
| DE | [draft-mih-agent-disclosure-envelope](https://datatracker.ietf.org/doc/draft-mih-agent-disclosure-envelope/00/) | S. Mih | -00, 2026-09-26 | Revealing the content behind a digest-only field without changing the Capsule |
| Bundle | [draft-mih-zhang-agent-disclosure-bundle](https://datatracker.ietf.org/doc/draft-mih-zhang-agent-disclosure-bundle/01/) | S. Mih, Y. Zhang | -01, 2026-10-19 | A portable container of Capsules with declared citation closure and separately reported completeness claims |
| CPB | [draft-mih-sokolov-scitt-payload-binding](https://datatracker.ietf.org/doc/draft-mih-sokolov-scitt-payload-binding/05/) | S. Mih, A. Sokolov | -05, 2026-09-11 | A canonicalization algorithm registry, derived identifiers, typed digest references, statement-to-Receipt binding |
| CLL | [draft-mih-scitt-checkpointed-local-log](https://datatracker.ietf.org/doc/draft-mih-scitt-checkpointed-local-log/02/) | S. Mih | -02, 2026-10-13 | A producer-run append-only log (Merkle Mountain Range) with signed checkpoints that other parties verify for consistency |
| Bilateral | [draft-mih-agent-bilateral-attestation](https://datatracker.ietf.org/doc/draft-mih-agent-bilateral-attestation/02/) | S. Mih | -02, 2026-09-13 | Request and action attestations exchanged across an organizational boundary |
| Settlement | [draft-mih-agent-settlement-records](https://datatracker.ietf.org/doc/draft-mih-agent-settlement-records/00/) | S. Mih | -00, 2026-10-01 | Two-party payment records: each leg sealed by the party that observed it; agreement derived by the verifier |
| Request | [draft-mih-agent-evidence-request](https://datatracker.ietf.org/doc/draft-mih-agent-evidence-request/00/) | S. Mih | -00, 2026-09-26 | Asking for evidence: exactly one of an artifact, a signed refusal with a reason, or a recorded absence |
| Store | [draft-mih-agent-evidence-layer](https://datatracker.ietf.org/doc/draft-mih-agent-evidence-layer/00/) | S. Mih | -00, 2026-10-03 | What a local evidence store provides: record model, typed links, retention states, commitment interface |
| Composition | [draft-mih-sato-agent-accountability-composition](https://datatracker.ietf.org/doc/draft-mih-sato-agent-accountability-composition/01/) | S. Mih, T. Sato, I. Schrock, S. Bu, A. Sokolov | -01, 2026-08-16 | Joining authorization, human-authorization, action and runtime-audit records on a shared action digest |
| Method | [draft-mih-agent-accountability-conformance](https://datatracker.ietf.org/doc/draft-mih-agent-accountability-conformance/00/) | S. Mih | -00, 2026-07-31 | A deterministic verification method for single records and compositions, with a test-vector discipline |
| Runtime | [draft-palanisamy-scitt-aac-runtime](https://datatracker.ietf.org/doc/draft-palanisamy-scitt-aac-runtime/00/) | G. Palanisamy, S. Mih | -00, 2026-10-02 | The Capsule's `model_attestation` block: model, weights, serving-runtime, agent-runtime and hardware claims, each with a declared source, and citation of a foreign attestation record |
| OTel | [draft-palanisamy-scitt-aac-otel](https://datatracker.ietf.org/doc/draft-palanisamy-scitt-aac-otel/00/) | G. Palanisamy, S. Mih | -00, 2026-10-02 | Carrying OpenTelemetry trace and span context in a Capsule, and the Capsule's identifier on the span, with an allow-list of GenAI semantic-convention attributes |

Dates are those on the posted text. None of the fourteen is a working-group document.

## Tier Placement Caveat

A format has no Tier; a claim does ([C8.1](../0.1/en/0x10-C08-Verifiability-Tiers.md)). What the
drafts offer the trust analysis of C8.1.2 is a plain statement of what each record does and does
not establish.

* A Capsule signed only by its producer (AAC Section 5.4, `attestation_mode: "self_attested"`)
  is an operator-signed record. C8 places that at Tier 2.
* Registering a record with a SCITT Transparency Service (AAC Section 3.3) returns a Receipt:
  evidence of inclusion in that service's log, and of time only when the Receipt carries a signed
  time claim (CLL Section 4.5). A Receipt is not a consistency proof (Store Section 8).
* CLL checkpoints registered under a Consistency Registration Policy at Transparency Services the
  producer does not operate (CLL Section 4.4, items 2 and 3, and Section 4.5) are the drafts' route
  toward a Tier 3 claim. Whether a deployment gets there depends on who those Transparency Service
  operators are; C8.1.2 requires naming them, and C8.1.3 places a log whose root one party controls
  at Tier 2. "Consistency Registration Policy" is the CLL's own term (Section 1.1): a SCITT
  Registration Policy that admits a checkpoint only if it is consistent with the last checkpoint
  that service registered for the same log. The CLL defines no witness role (Section 1.2).
* Runtime labels each model, runtime and hardware fact with how it was obtained (self-reported,
  provider-reported, OS-reported, computed or attested), and a verifier never reports a fact above
  its label (Runtime Sections 2, 3.1.1 and 7). A fact is attested only through a cited attestation
  record that the record issuer's own verifier accepts (Runtime Section 4.5).
* Nothing in the drafts gates execution on proof validity. They do not reach Tier 4 (C8.3).

The drafts state the same limit C8 states for Tier 3. A CLL whose checkpoints are registered under
a Consistency Registration Policy establishes order,
contemporaneity and completeness of what was committed; it establishes nothing about the truth of
any entry, and not that the log is the producer's only log (CLL Section 7). A signature and a
Receipt attest record bytes and timing, not the honesty of the runtime that wrote them (AAC
Section 13, CPB Section 12.5). That is the signing-time versus runtime distinction of C8.2.2.

## The Mapping

### C1 Provenance

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 1.1.1 | Runtime Section 3.1: `weights_digest` over the weight file as loaded (scope `file`, source `computed`) or over in-memory tensors (scope `tensors`, admitted only as `attested`), with `model_id`, `quantization` and `decoding`. Runtime Section 4.1: `runtime_digest` of the serving binary, with a `measurement_class`. AAC Section 5.2: `epoch_id` rotates when the model version changes, and the epoch-boundary Capsule (Section 5.2.2) carries the block. AAC Section 5.3: the `inference_completion` effect binds request and completion digests at the serving boundary | A `computed` weights digest can be recomputed by anyone holding the file; that this file served the request is still the producer's statement unless a cited attestation record binds the same value (Runtime Sections 3.1.1 and 4.5). `model_id` alone is a self-reported name, and no field establishes which arithmetic ran, so quantization is never reported as verified (Runtime Sections 3.1.1 and 9) |
| 1.1.2 to 1.1.5 | None | No signed-manifest comparison, model signature chain, admission control or supply-chain attestation. Runtime Section 4.5 cites an attestation record by digest but defines no attestation format |
| 1.2.1, 1.2.2 | AAC Section 5.5.5: typed digest references from a Capsule to the records it acted on or responded to. DE Section 1: digests of the agent's input and output | Presence by digest, asserted by the producer; input integrity is composed upstream (AAC Section 13) |
| 1.2.3 | CLL is payload-neutral (Section 1); digests of transformation records could be its entries | No transformation record is defined |
| 1.3.1, 1.3.2 | Runtime Section 4.2: the agent's execution environment (`runtime_env`, framework, sandbox, invoked tool version). Runtime Section 4.4: platform and accelerator. Runtime Section 4.5: a hardware or platform attestation record cited by typed digest reference and verified by its issuer's verifier, which lifts a field to `attested` only when it binds an equal value. AAC Section 5.5.6: a `ran_under` citation to a record of the runtime environment. Composition Section 6.4.3: an action digest bound into a TPM quote | Without a verified attestation record, hardware is OS-reported at best and the agent runtime is self-reported (Runtime Sections 4.4 and 7). Stable device identifiers never enter the record (Runtime Section 4.4), so host identity is not recorded. The TPM binding was exercised on a virtual TPM and establishes no hardware root (Composition Section 6.4.7) |
| 1.4.1, 1.4.2 | AAC Section 14.1: each field is classed clear-safe, digest-only or never-enters before admission. SD Sections 4 and 6; DE Section 5 | |

### C2 Privacy

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 2.1.1, 2.1.3 | AAC Section 5.3: the Effect Record's request and response digests. Store Section 6.2: disclosure records state what was revealed and what was suppressed | No data-store identifier or operation type; used versus disclosed is not a Capsule field |
| 2.1.2, 2.4.1 | AAC Sections 14.1 and 14.2: digest-only and never-enters classes, admission by allow-list | Digests of low-entropy values are recoverable by dictionary attack (CPB Section 12.2) |
| 2.2.1 to 2.2.5 | AAC Section 8.1: a Constraint Record carries the result of each deterministic evaluation, denials included, and can bind the evidence it evaluated by an optional `evidence_digest` | No consent, purpose, residency or licence vocabulary |
| 2.3.1 | SD Sections 4.2, 4.3 and 6; DE Section 5.1; Request Section 8 (derivation-scoped disclosure) | Commitments and selective disclosure only; no zero-knowledge proof |
| 2.3.2 | AAC Section 3.3: registration with a Transparency Service | No consent record type |
| 2.3.3 | None | No verifiable computation |
| 2.4.2 | CLL Section 2, item 2: erasing content leaves its committed digest in the log. Store Section 6.1: retention states AVAILABLE, PARTIAL, WITHHELD, DELETED, LEGAL_HOLD; WITHHELD is never reported as DELETED | |

### C3 Portability

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 3.1.1, 3.1.2 | Bilateral Sections 4 and 5: request and action attestations across an organizational boundary, the constraint set pinned by digest, a result for every constraint. Settlement Sections 3 and 9: each side seals only what it observed, and the verifier derives agreement. Store Section 10: per-pairing reconciliation states (MATCHED, A_ONLY, B_ONLY, CONFLICTING, INSUFFICIENT, UNRESOLVED) | Organizational boundaries only; no jurisdiction or compute-boundary field. Bilateral wire encodings are not yet fixed (Section 4) |
| 3.2.1 | CPB Sections 4 and 12.6: registry entries are immutable and name their hash, and evidence is renewed before an algorithm weakens. AAC Section 5.4.2: cross-algorithm re-anchoring | |
| 3.2.2 | AAC Section 5.2.2: an epoch-boundary Capsule chains to the last Capsule of the prior epoch. CLL Section 2, item 3: a key rotation is an entry, signed under the outgoing key, naming the incoming one | Both link within one producer's stream. Across producers the drafts offer citation (AAC Section 5.5.5), not a signed linking record |
| 3.2.3 | SD (per-recipient disclosure); Request Section 8 | No per-jurisdiction disclosure rules |

Request (Section 4, the three outcomes; Section 9, retention commitments) and Bundle (Sections 3,
4 and 9: one object, offline or hosted) are how evidence moves between parties. They bear on
[Appendix D](../0.1/en/0x93-Appendix-D_Open-Issues.md) issues 3 and 5 as input, not as an answer.

### C4 Authorization

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 4.1.1 | AAC Section 5.5: `disposition.authority`, an opaque reference. AAC Section 5.3: typed digest references to external authorization records. Composition Section 6.1 (CAN) | No draft defines a public form of the grant itself (permission set, scope, expiry). A capability-envelope format for it is planned and not yet drafted |
| 4.1.2, 4.1.3 | AAC Section 5.5 (decision, `verdict_class`), Section 8.1 (Constraint Records, each flagged for whether it gated the decision) and Section 5.5.3 (a Capsule on every verdict, blocked and denied included) | The record shows a decision; where it was enforced is a C7.1 matter |
| 4.1.4 | AAC Section 5.3 (`request_digest`); a schema validation can be a Constraint Record (Section 8.1) | No binding to a registered tool schema |
| 4.1.5 | None | |
| 4.1.6 | AAC Section 5.5: `human_disposed` is true only when a human acted, and requires `approver: "human"`. AAC Section 5.5.4: deferral and resolution as chained Capsules. Composition Section 6.2 (WHO): a named human's signature over the canonical bytes of the action, with VERIFIED kept apart from ACCEPTED | AAC records that a human acted, not who |
| 4.1.7, 4.1.8 | AAC Section 5.5.4 (chain) records order | No path-aware evaluation; nothing on trust transfer into approval state |
| 4.2.1 to 4.2.4 | Bilateral Section 4: the requester's attestation binds it to the request's terms | No delegation-chain format, scope intersection or zero-knowledge presentation |

### C5 Identity

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 5.1.1 | AAC Section 5.1: `operator` (the accountable tenant) and `developer` (agent identity and version). Store Section 4: `principal_ref` | Strings and opaque references. AAC Section 14.1 keeps end-user identity out of the record by design |
| 5.1.2 | AAC Section 3.2: the verifier returns the authenticated key; whether that key is authorized is the caller's policy | Key control is not authority (Store Section 11) |
| 5.1.3 | Composition Section 6.2 (WHO) | Human authorization of an action, not a delegation token per tool call |
| 5.1.4 | None | |
| 5.2.1, 5.2.2 | Bilateral Section 4; Settlement Section 3 (one key per side; a shared key is reported as sealer conflation) | Binding keys to organizations is inherited, not solved (Bilateral Section 11.1) |

### C6 Security

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 6.1.1 | AAC Section 8: Constraint Records refer to the producer's manifest; Class 2 verification (Section 8.2) uses it | The manifest is private, and its discovery is out of scope (Section 8) |
| 6.1.2 | AAC Section 5.3 (effect type, status, request and response digests), Section 5.1 (timestamp), Section 5.5.3 (every verdict) | A record does not show that every invocation was recorded (see C10.3.2) |
| 6.1.3, 6.2.2 | Runtime Section 4.1: `measurement_class` names how the serving binary was measured, `tee_measured` included. Runtime Section 4.5: a TEE or platform attestation record cited by digest and verified by its issuer's verifier. Composition Section 6.4.3 (TPM quote binding) | No comparison against golden reference values. The Runtime draft reports that only `self_measured` and `os_measured` are produced by shipping code today, and `tee_measured` has a record shape and a verifier (Section 4.1). The TPM binding was exercised on a virtual TPM |
| 6.2.1 | Runtime Section 4.2: `sandbox_type` recorded per action | Self-reported unless a source says otherwise, and a verifier infers no confinement strength from it (Runtime Section 7). No record of escape attempts |
| 6.2.3 | None | No hardware gate |
| 6.3.1, 6.3.3 | None | No key custody or compromise procedure. Bilateral Section 11.8 asks for key validity as of anchored time and leaves revocation to the identity scheme |
| 6.3.2 | CLL Section 2, item 3 | |
| 6.3.4 | AAC Section 3.1 (algorithm in the protected header); CPB Section 4 (named algorithms; a new hash is a new entry); CLL Section 4 | The AAC Producer Envelope fixes Ed25519; moving off it takes a profile revision. CLL defines checkpoints for MMR_SHA256 logs only (CLL Section 9) |
| 6.3.5 | CPB Section 12.6; AAC Section 5.4.2 | No post-quantum algorithm is registered |

### C7 Evidence Generation and Properties

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 7.1.1, 7.1.3 | None | The drafts define the record, not the gateway: no process separation, no write-before-forward |
| 7.1.2 | AAC Section 5.3: effect status `planned`, `dispatched`, `confirmed`, in Capsules linked by chain relations (Section 5.5.4) and correlation fields (Section 3.4) | Not required at three points per action |
| 7.1.4, 7.1.5 | AAC Section 5.3: `confirmed` requires a digest of the observed response, and `effect_attestation` records whether a gate observed the effect or a runtime reported it. AAC Section 5.4: `effect_mode` is rederived by the verifier and never graded up | Observed and bound, not world state (AAC Section 13). No action-bound single-use capability, so option (b) has no format |
| 7.2.1 | AAC Section 5.4.3: an imported historical record declares itself `backfilled`. CLL Section 2, item 1: append at production time | Record timestamps are producer-attested (AAC Section 5.4.3) |
| 7.2.2 | AAC Section 3.3 (Receipt); CLL Section 4.5 | Time only where the Receipt carries a signed time claim |
| 7.2.3, 7.2.4 | None | |
| 7.3.1 | AAC Section 5.5.4 (chain block); CLL Sections 1, 3 and 4 (Merkle Mountain Range) | |
| 7.3.2 | None | Key custody is out of scope |
| 7.3.3 | CLL Section 4.4, items 2 and 3, and Section 4.5: a Transparency Service applying a Consistency Registration Policy registers a checkpoint only if it extends the last one it registered, and a Transparency Service the producer runs is a replica. Request Section 5: the artifact served depends on the subject and the anchor, not on who asks | |
| 7.3.4 | CLL Section 6 (inclusion); AAC Section 3.3 (Receipt); Bundle Section 6 (per-record membership; an endpoint proof does not stand in for it) | |
| 7.3.5 | CLL Section 4.4, item 2, and Section 6 (consistency); Store Section 8 | |
| 7.4.1 | See C10.2 | |
| 7.5.1, 7.5.2 | Method Section 4 (the determinism boundary); AAC Section 8.1 (each result comes from a deterministic predicate, and no model is re-prompted to verify one); Store Section 4.1 (`epistemic_type`, set at commit and never upgraded) | |
| 7.6.1 | None | |
| 7.6.2 | CLL Section 6 (range completeness); Bundle Section 4 (a cited record is supplied or listed as missing, never dropped) | Bounds omission within the committed log, not action taken off it (CLL Section 7). Bundle Section 8 gives one digest over an enumerated set and defines an Ed25519 countersignature over it; that counts toward the signed manifest the 7.6.2 auditor note accepts only when the signer is a party other than the producer, since Section 8 renders a self-countersignature as not independent |
| 7.6.3 | None | Tier 4 |
| 7.6.4 | Store Section 6.2 (disclosure records) | Records acts of disclosure, not every read |
| 7.6.5 | AAC Section 5.5.6 (retention declarations); Request Section 9 (retention commitments); Store Section 6.1 | |
| 7.6.6 | CLL Section 4.4, items 1 and 4: a declared maximum interval between checkpoints makes a missed one detectable, and nothing after the last registered checkpoint is represented as covered by one | |
| 7.7.1 | AAC Section 5 (field tables) | |
| 7.7.2 | CPB Sections 4.1 and 5; AAC Section 5.1 (`canonicalization_id` is `jcs`); Settlement Section 6 (amounts as an integer and a scale) | |
| 7.7.3 | CPB Section 4 (a payload class declares one algorithm, and verifiers do not infer it), Section 6.2, Section 7 (unknown VDS identifiers are rejected) | |
| 7.7.4 | CPB Section 14.1 (each registration names public positive and negative vectors; locations in Section 14.1.1); Method Section 5 (a must-fail vector must be refused, with a mutation probe for each category); Composition Section 8 | The cross-slot vector pack is a candidate, not yet frozen (Composition Section 8.1) |
| 7.7.5 | CPB Section 8.3 (a duplicate key makes the reference Malformed; first-wins and last-wins are prohibited); Bundle Section 3 (no duplicate Capsule IDs) | CPB Section 4.1 does not itself state duplicate-member handling for JSON payloads |

### C8 Verifiability Tiers

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 8.1.2 | AAC Sections 5.4 and 5.4.1 (attestation, ledger, effect and cross-party grades, rederived by the verifier, with overclaims reported); Composition Section 7; Store Section 3 (self-attested, witnessed, countersigned) | Inputs to the trust analysis, not Tiers |
| 8.1.5, 8.1.8 | AAC Sections 6 and 7: Class 1 verification needs only the record's bytes. Open-source verifiers are listed below | |
| 8.2.2 | AAC Section 13; CPB Section 12.5 | |
| 8.3.1 to 8.3.5 | None | Bilateral Section 4 gates execution on a verified request at the performing party, but that gate is the operator's and may degrade by policy (Section 7). C8.3.5 asks for enforcement outside operator control |

### C9 System Surface (MAESTRO)

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 9.1.1 to 9.1.3 | None | No draft records a MAESTRO Layer; the claim register does |
| 9.2.1 | CLL; AAC Section 5.5.4 | |
| 9.2.2 | OTel Sections 3, 3.1 and 4: a Capsule names the trace and span that observed its action, with fixed resource and GenAI attributes (service, operation, agent and tool names), and the span carries the Capsule identifier back. Runtime Sections 4.1 and 4.2 keep the serving runtime and the agent's own runtime apart | Correlation, not placement: the span is the same producer's telemetry, and a report counts it as no independent corroboration (OTel Sections 5 and 7). Which Layer the evidence came from is still the claim register's statement |
| 9.2.3 | Bundle Sections 4 and 8 (citation closure; one digest over the bundle); Method Section 8 | |

A claim using these formats would most often locate the logs (CLL, AAC chains) at Layer 5 and the
cross-party records (Bilateral, Settlement, Request) at Layer 7.

### C10 Conformance and Trust-Assumption Disclosure

| Requirement | Candidate evidence format | Limit |
| --- | --- | --- |
| 10.1.1 to 10.1.8 | None. Method Section 3 covers verification of records (binding, per-slot, composition), not an organization's statement | No template for a Self-Declared or Third-Party Assessed statement |
| 10.2.1, 10.2.2 | Material for a disclosure, not a format: Bundle Section 6 (three completeness claims reported separately, and `checkpoint_unverified` where no witness signature was verified) and Section 10 (producer self-report labelled as such); CLL Section 4.4, item 3 (named Transparency Services); Store Section 4.1 | No category set ([Appendix D](../0.1/en/0x93-Appendix-D_Open-Issues.md), issue 7) |
| 10.3.1 | CLL | |
| 10.3.2 | AAC Section 5.5.3 (a Capsule on every verdict) | A producer rule; the count reconciliation is not defined |
| 10.3.3 | AAC Sections 6 and 7; Method Section 4 | |
| 10.3.4 to 10.3.7 | None | |

### The Evidence Claim Set

The claim set in [`schema/`](../schema/README.md) allocates three claim keys (-70014 to -70016).
Each touches one of these formats, so each has a row. The rows map claims, not requirements.

| Claim | Candidate evidence format | Limit |
| --- | --- | --- |
| `merkle_root` (-70014), `tree_size` (-70015) | AAC Section 3.3: a Receipt from a Transparency Service whose verifiable data structure is an RFC 9162 Merkle tree carries an inclusion proof, with the tree size it is taken against, to a root the service signs. The verifier reads which structure applies from the Receipt's protected header (CPB Section 7) | CPB is agnostic about the structure (Section 7), so this holds only where the service uses an RFC 9162 tree. A CLL checkpoint commits a Merkle Mountain Range (CLL Sections 4 and 4.1): its `commitment` and `log_size` are not an RFC 6962 tree head and do not belong in these two claims |
| `dispatched_snapshot_hash` (-70016) | AAC Section 5.3: a Capsule with effect status `dispatched` carries the `request_digest` of what was sent, and chains (Section 5.5.4) to the Capsules before it for the same action. The evidence a check evaluated can be bound by an optional `evidence_digest` in its Constraint Record (Section 8.1) | AAC has no MODIFY verdict and no field that marks a dispatched action as a modification of the evaluated one: the difference shows only when a verifier compares the two digests. `request_digest` is SHOULD, not MUST, at `dispatched` |

## What the Drafts Do Not Cover

* **Tier 4.** No fail-closed gate, no halt on violation, nothing enforced outside the operator's
  control (C6.2.3, C7.6.3, C8.3). Runtime can cite a TEE attestation record, and the one hardware
  binding a draft defines, a TPM quote, was exercised on a virtual TPM; neither gates execution.
* **Verified agent or principal identity.** Operator, developer and principal are strings or
  opaque references; whether a key belongs to anyone is the relying party's policy (C5.1.2 to
  C5.1.4, C5.2.2).
* **The authority granted, in public form.** AAC carries an opaque reference to it. A
  capability-envelope format is planned and not yet drafted (C4.1.1, C4.1.5, C4.2, C7.1.4
  option (b)).
* **Model provenance beyond the producer's word, unless attested.** Runtime makes each model and
  runtime fact carry its source, and a weights digest the producer computed can be recomputed from
  the file. That the file served the request stays the producer's statement until a cited
  attestation record binds it, and nothing shows which arithmetic ran (Runtime Section 9). There is
  no manifest comparison, signature chain or lineage (C1.1.2 to C1.1.5, C1.2.4).
* **Zero-knowledge proofs.** Privacy rests on digests, salted-hash commitments and selective
  disclosure (C2.3.1, C2.3.3, C4.2.4).
* **Statement and disclosure templates.** Nothing for a Self-Declared or Third-Party Assessed
  conformance statement, and no trust-assumption categories (C10.1, C10.2.2).
* Also absent: consent and purpose vocabularies (C2.2), jurisdiction and compute boundaries
  (C3.1.1, C3.2.3), path-aware authorization (C4.1.7, C4.1.8), gateway architecture (C7.1.1,
  C7.1.3), key custody (C6.3.1, C7.3.2) and a MAESTRO Layer field (C9.1; OTel correlates a record
  with the trace that observed it, which helps place it, but names no Layer). Bundle reserves a
  countersignature slot whose verification is future work (Bundle Section 8).

## Implementations

Open-source implementations exist for five of the drafts. This crosswalk maps the drafts, not
them.

* [agent-action-capsule](https://github.com/action-state-group/agent-action-capsule): reference
  code in Python, Go, Rust and TypeScript, and test vectors, for AAC.
* [capsule-emit](https://github.com/action-state-group/capsule-emit): a producer of Capsules. It
  writes the Runtime block, and an OpenTelemetry span exporter in it writes the OTel block
  (Runtime Section 11, OTel Section 8).
* [Mesh-LLM capsules](https://github.com/Mesh-LLM/capsules): a producer at the inference boundary
  of a peer-to-peer model-serving network, which writes the Runtime block's serving-runtime
  measurement (Runtime Section 11).
* [checkpointed-local-log](https://github.com/action-state-group/checkpointed-local-log): a CLL
  library, with checkpoint and Merkle Mountain Range test vectors.

CPB's test vectors are at the locations its Section 14.1.1 names.

## Status

> **[DRAFT]** Mapped by an author of the drafts, as a single coder. A second reading, ideally by
> someone who did not write them, is the most useful review. Section numbers are pinned to the
> revisions above and will move with later ones.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
