---
industry: insurance-claims-intake
use_case: Verify the identity and correspondence of exact committed synthetic FNOL review artifacts
submission_type: scenario
claimed_tier: 3
threats:
  - audit-tampering
  - evidence-repudiation
---

# Public verification of committed FNOL review artifacts

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

Research candidate prepared for Mikhail Sergeev with AI-assisted drafting. The architecture, verifier and FNOL example below are assumed and unimplemented. Tier 3 is a proposed placement for the narrowly specified hypothetical mechanism, not an attained conformance tier, an Insurance Working Group submission or a result of PR182.

## Scenario

A claims operations analyst reviews an evidence packet associated with an AI-assisted first-notice-of-loss (FNOL) workflow. The proposed decision is whether to rely on a specific discrepancy calculation over a fixed, declared intake population and a fixed packet, or defer reliance and seek a supplement. It does not decide policy coverage, liability or payment, and does not establish that the declared population contains every real intake action.

The exact proposition is: **under the disclosed profile and trust premises, these supplied artifacts are the ones identified by the authenticated log commitments, and the reported discrepancies are reproducible from those exact inputs and matching rules.** The proposition concerns artifact identity, integrity and correspondence. A clean correspondence result would mean only that the selected obligations in the declared population are met by the committed packet under this profile.

### Assumed artifact and observation architecture

The local illustrative profile is `FNOL-COMMITTED-REVIEW-v1`. It is a proposed profile, not a normative Proof-of-Control schema or an implemented extension of PR182. It fixes the following artifacts before assessment:

| Artifact | Fixed contents and role |
|---|---|
| Population manifest **P** | A finite list of synthetic case/action/attempt identities and their declared record obligations, the source/session/epoch, intake interval, and a declaration of what the population purports to cover. P is not reconstructed from surviving packet records. Its declaration is not proof of capture completeness. |
| Packet manifest **E** | Every received record's distinct logical record ID, exact byte digest, referenced action/attempt/obligation, and signing-key reference. The exact record bytes and detached signature material are part of the proposed public synthetic input bundle. E fixes the received packet, not every record that might exist elsewhere. |
| Discrepancy result **R** | The digests of P, E, the profile, matching rules and verifier version, together with the deterministic correspondence findings. R does not contain or hash its own log inclusion proof. |
| Commitment and verification material | A domain-separated log leaf binds the digests of P, E and R, plus the profile, matching rules and verifier source. Authenticated tree heads, inclusion proofs, consistency proofs, monitor views and the declared key registry support a separate verification record. |

The proposed canonical manifest encoding is strict UTF-8 JSON with unique ASCII field names, lexicographically ordered object keys, no numeric literals, no insignificant whitespace and no final newline. Identifier and time values are ASCII strings. Each schema fixes array order explicitly: action/attempt/obligation identity for P, record ID for E, and finding category plus obligation/record identity for R. Identical input bytes must produce identical digests; an alternative serialization is a different artifact. The profile, algorithms, key identifiers and verification rules must themselves be versioned and bound in the commitment. This document specifies the design; it supplies no executable canonicalizer or verifier.

The hypothetical publisher commits those artifacts to a **public append-only transparency log**. The public verifier would obtain and verify inclusion proofs for the committed leaf and consistency proofs between the acquired authenticated tree heads. It would acquire authenticated views from two disclosed, independently controlled monitors and compare the heads and relevant views itself; it would not accept a monitor's signed “no conflict” conclusion in place of that comparison. The verification record would enumerate the actual acquired head/view identifiers, tree sizes, roots, proof digests, acquisition observations and completed comparisons.

For this synthetic scenario, the declared intake interval is ticks **[0, 300)** in synthetic review epoch `SYN-EPOCH-1`. P, E and R are assumed fixed and committed before tick **600**. The monitoring window is **[600, 900]**, and the verification cutoff is tick **900**. The selected view set consists of authenticated heads and relevant inclusion/consistency material obtained from the log and both monitors at the two endpoints, together with any additional views actually acquired within that window and listed in the record. Comparisons concern that finite disclosed set. They do not establish that every possible view was received, that no undisclosed fork existed, or that alteration would be detected after tick 900. These ticks describe a hypothetical schedule; a real implementation would need an explicit trusted clock/acquisition-time premise. Signed timestamps alone would not prove truthful event time.

The review-result commitment is deliberately not circular: R is the correspondence calculation over fixed P/E and rules. The later verification record identifies the proofs and views used to appraise that commitment at the cutoff. Neither a log receipt nor inclusion by itself establishes the truth of P or the recorded actions.

### Controllers and remaining dependencies

The following are named **hypothetical roles**, not assertions that real independent organizations or key custodians have been verified:

| Controller | Keys or authority controlled | What remains dependent on that controller |
|---|---|---|
| **P-owner**, the intake-population custodian | Population signing key `K-P`; selects the declared population and its scope | The signature authenticates P-owner's declaration. Truthful capture, source completeness and omission before declaration remain unestablished. |
| **R-owner**, the workflow record issuer | Record signing key `K-R`; creates record assertions | Record origin/authentication, not truthful action execution or effect. P-owner and R-owner may share control; no capture independence is inferred. |
| **Review publisher V** | Result signing key `K-V`; publishes P/E/R and the proposed verifier/rules | Attribution of the result. Correctness must be checked against the public fixed inputs/rules, not inferred from V's signature or reputation. |
| **Log operator L** | Log signing key `K-L`; storage, sequencing and proof service | Correct log operation and availability within the stated profile; inclusion does not prevent withholding or establish universal consistency. |
| **Monitor M1** and **monitor M2** | Separate monitor keys `K-M1` and `K-M2`; independently acquired and retained views | The architecture assumes distinct control from each other, L and the case operators. Actual ownership, key custody, selection and acquisition coverage would have to be disclosed and supported. Merely naming two services supplies none of that evidence. |

The proposed public key registry would pin the authorized keys, controller bindings and validity/revocation policy at the cutoff. Authentication depends on those bindings and on the signature/hash/proof mechanisms and verifier being sound. The compared-set result does not require pretending that every monitor sees every view. A stronger claim about detecting log equivocation would additionally require an honest monitor to obtain and make the relevant conflicting view available during the window; that acquisition premise is not established here. Monitoring or key-control collusion cannot erase an actual byte comparison of the disclosed views, but it can defeat an inference about views withheld from that set.

If a manifest or record fails its exact digest/signature check, the verifier would report that failure; it must not silently select replacement bytes. A conflicting authenticated same-size head or invalid consistency proof would be an integrity finding. Missing artifacts, unavailable proofs, unknown or revoked key bindings, an unavailable monitor, an uncompleted comparison or a monitoring lapse would prevent the selected verification profile from being established at the cutoff. The analyst would defer reliance and identify the missing premise, rather than report a clean packet or infer no bypass. A later supplement would preserve and reference the original assessment, not overwrite it. The mechanism does not promise availability, retention or future detection beyond its declared window.

### Filled, unexecuted correspondence example

All identifiers below are synthetic. P declares `SYN-CASE-1`, source/session/epoch `SYN-INTAKE` / `SYN-SESSION-1` / `SYN-EPOCH-1`, actions **A** and **B**, and attempt **1** for each. For this small local example, both attempts are declared to require exactly one logical **decision** record and one logical **dispatch** record. These are stipulated illustrative obligations; this example does not implement the full operation/attempt/phase procedure or show compliance with 7.1.2. A record's assertion of dispatch is not an observed endpoint effect.

Each obligation is keyed by `(case, source, session, epoch, action, attempt, phase)`. Each logical record has a distinct, nonreused `record_id` bound to that tuple. A retry has its own attempt ID and separately declared obligations. No retry is declared here. A record for an undeclared attempt would be unmatched, not an extra record for attempt 1. Re-presentation of the same record ID with identical bytes is recognized as redelivery and counted once; the same ID with different bytes is a conflict.

| Declared obligation | Logical records in E | Expected correspondence finding |
|---|---|---|
| A / attempt 1 / decision | none | Missing required record |
| A / attempt 1 / dispatch | none | Missing required record |
| B / attempt 1 / decision | `SYN-B-D-1`, `SYN-B-D-2` | Two distinct logical records for one obligation: excess record for that obligation |
| B / attempt 1 / dispatch | `SYN-B-X-1`, `SYN-B-X-2` | Two distinct logical records for one obligation: excess record for that obligation |

E therefore contains four distinct logical records against four declared obligations, but correspondence fails: two A obligations are missing and two B obligations each have an excess record. The two phases for B are **legitimate distinct lifecycle obligations**; a packet containing only `SYN-B-D-1` and `SYN-B-X-1` would have no excess-record finding for B. A second distinct record ID for the same B obligation creates the excess in the table; differing phase or retry identity alone does not. Whether excess records also conflict in payload is a separate finding.

R would record these missing/excess findings and their exact obligation/record identities, with no unmatched record in this stipulated packet. An outsider using the same committed inputs and published matching rules would be expected to reproduce that calculation. This is an expected result for a newly written, unexecuted FNOL illustration, not a measured outcome, a fourteenth PR182 case or an implementation of the proposed verifier. Log verification could establish the identities of these defective artifacts while the correspondence calculation correctly reports discrepancies.

## Claimed tier: Tier 3

**Hypothetical, conditional Tier 3 for exact committed-artifact integrity and publicly verifiable correspondence only.** This placement follows [current C8's explicit transparency-log example](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x10-C08-Verifiability-Tiers.md#cryptography-is-a-mechanism-not-a-tier): “A public, append-only transparency log with independent monitors.” C8 describes that example as retrospective rather than execution-stopping, and 8.1.6 distinguishes those mechanisms from operation-gating Tier 4.

This is not an unconditional theorem about all transparency deployments. C8 is explicitly a draft. Its open framing section says every admitted mechanism leaves residual trust and leaves the replacement Tier-2/Tier-3 framing and binary-threshold review unresolved. The roles, acquisition premises and limits above remain part of the claim; the scenario does not rely on the README's blanket statements about eliminated trust.

The architecture presupposes that the verifier source, matching rules, canonicalization profile, controller/key disclosure and entirely synthetic sample inputs would be published and usable without privileged credentials, with the relevant proofs/views available. That publication is **proposed, not performed**. No FNOL implementation or outsider verification run exists in this candidate, so C8.1.5's recorded verification demonstration and C8.1.8's published tooling are not claimed satisfied. The numeric frontmatter describes the hypothetical calibration scenario, not a deployed system or the tier of PR182's experiment.

## Why not one tier down?

**Why not Tier 2 for the selected requirement?** The analyst requires anyone to verify the committed artifact identities and reproduce the discrepancy calculation, without accepting an operator or auditor's replacement account on trust. An operator-signed replacement packet, a private Merkle root or an auditor's report alone does not meet that requirement. The assumed public log, authenticated proofs, disclosed acquired monitor views and public rules make that specific retrospective check available, while retaining their stated trust dependencies. They do not establish that the operator declared the true population.

**Reversibility and why not Tier 4.** The analyst can postpone evidentiary reliance and request a supplement. This review does not prevent workflow execution, undo a disclosed document or enforce a capability at an endpoint. It contains no “no proof, no write” execution gate; a withheld proof stops reliance on the review, not the underlying agent. Tier 4 is therefore not the proposed placement.

**Completeness.** The chosen finite artifact set is fixed, allowing an exact calculation over that set. The completeness of real action capture remains unestablished. If the decision instead requires proof that every real intake action was recorded, this Tier-3 architecture does not meet it; that broader requirement is not supplied by its title, tier or conclusion.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Hypothetical and conditional: identity/integrity of the exact committed P/E/R artifacts and public reproducibility of their correspondence calculation under the disclosed profile; not truth or completeness of population capture. |
| Privacy | not claimed | Only entirely synthetic sample data is proposed for publication. That choice is not a claimant-data privacy guarantee or a validated disclosure control. |
| Portability | not claimed | Public artifacts are proposed, but no operational portability predicate or implementation is assessed. |
| Authorization | not claimed | Neither signatures nor review commitments establish authorization of every realized action or effect. |
| Identity | not claimed | Key/controller bindings are explicit premises for this integrity claim, not an independently established real-world identity-domain claim. |
| Security | not claimed | No broader deployment-security predicate is assessed; the selected artifact-integrity claim is stated under Provenance. |

## Threats exercised

These tags identify exposure in the hypothetical workflow, not demonstrated mitigation.

| Threat | What it looks like here |
|---|---|
| `audit-tampering` | A party replaces a committed packet/result or supplies an incomplete declared-to-received correspondence. Exact commitment verification and the discrepancy calculation address different parts of that problem. Pre-declaration omission remains outside the integrity claim. |
| `evidence-repudiation` | A party disputes which exact declared population, received packet or calculated result was reviewed. The commitments bind the selected artifacts; they do not settle whether their underlying assertions describe real actions. |

## What Proof-of-Control does not verify here

- The truth of a loss, claimant account, population declaration or record assertion; claims-process adequacy, policy coverage, liability, valuation or underwriting.
- Capture of every real action, including portal, manual-import, retry or alternate-service paths not established by the declared population basis.
- Real-world no-bypass, endpoint enforcement, dispatch, delivery, storage mutation or another effect from a signature, log commitment or discrepancy calculation.
- Global log consistency from a finite compared view set, truthful wall-clock time from signed timestamps, or future availability/detection after the cutoff.
- The full operation/attempt/phase and record-identity procedure proposed in PR182; the local example selects only the explicit illustrative obligations above.
- Claimant-data privacy, insurer adoption, WG acceptance, membership, certification or independent external reproduction.

## Residual trust assumptions to disclose

P-owner and R-owner control what they declare. L controls its log service. M1/M2 control their keys, retained views and availability; independence and acquisition coverage are assumptions until supported. The verifier relies on the pinned key/controller and revocation registry, hash/signature/proof soundness, canonicalization and matching-rule correctness, exact version bindings, access to the selected artifacts and an explicit acquisition-time basis. The public verifier's availability would let others inspect and rerun its calculation; it would not prove that the code implements the intended policy correctly.

No TEE or runtime attestation is assumed, and no unspecified hardware root is used to fill a missing premise. The public PR182 campaign's local host records remain trusted harness records, and its population/observation/route premises remain synthetic or declared. They are not substitutes for this hypothetical log/monitor architecture.

## Notes / open questions

- **Hypothetical research candidate.** Implementation, publication of the proposed verification materials and recorded outsider verification remain separate steps.
- A real implementation would need evidenced controller identities, key custody, monitor selection/coverage, availability and clock premises, then published code/data and a recorded verification exercise. None is presented as already achieved. Do not publish claimant data or real case identifiers in the hypothetical demonstration artifacts.
- Preserve each cutoff assessment. Later evidence is a linked supplement or explicit revision with its own inputs and findings.
- Public evidence reused: [PR182's dated supplement at09d2e238](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/09d2e238bc9303b8d9f8442faba8c191d3832649/docs/proposals/coverage-reconciliation-evidence-2026-10-31.md) and its [unchanged original proposal](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/09d2e238bc9303b8d9f8442faba8c191d3832649/docs/proposals/coverage-reconciliation.md). Bjorn Vidar Hauge supplied the motivating restart/loss and alternate-path families; Mikhail Sergeev prepared the published finite-model work with AI assistance. This adaptation adds no execution result.
