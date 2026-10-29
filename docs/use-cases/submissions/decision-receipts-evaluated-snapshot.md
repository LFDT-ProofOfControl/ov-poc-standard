---
industry: saas-customer-support
use_case: A decision model routes support tickets and releases downstream actions; every decision emits a signed receipt that serves as the evaluated snapshot for the action it releases
submission_type: scenario
claimed_tier: 3
threats:
  - evidence-repudiation
  - audit-tampering
  - context-blind-authorization
  - excessive-agency
  - approval-fatigue
---

# Decision receipts as evaluated snapshots: binding the decision record into Proof-of-Control evidence

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*
>
> *Worked from an open-source decision-receipt adapter over a Jev-shaped decision-model stub. The deployment is illustrative. Behaviors cited were checked against that stub on 2026-09-29.*

## Scenario

A SaaS operator routes inbound support tickets with a decision model — billing, support, or sales — and the routing releases downstream actions: refunds issued, account changes made, threads escalated. Decisions are high-volume and low-latency. A fraction are later disputed by customers or examined by auditors: *why was this refund denied, who approved this account change, what did the model actually decide?*

The operator wraps the decision function in a receipt adapter. Every decision emits one signed, hash-chained decision record: the options considered with their probabilities, the chosen option and its confidence, the authority declared for that decision class, the evidence references the decision relied on, and the policy tier the confidence maps to — routine (auto-act), supervised (act, flagged for sampling), or human-in-the-loop (gated until a named human records a disposition, appended as an override record naming the actor and the reason). When a released action passes the Proof-of-Control interception gateway, the decision record's digest is the evaluated-snapshot digest (C7.1.4b), and the gateway's before/during/after records and the decision record cross-reference by action ID. An auditor can traverse from any action to the decision that released it, and back.

## Claimed tier: Tier 3

The decision record exists to be believed by parties who do not trust the operator: a customer disputing an outcome, an external auditor, a regulator. That sets the tier. Verification tooling is published and open (an audit CLI that verifies the hash chain and signatures, then reports tier counts and flags — unreviewed human-tier decisions, low-confidence decisions acted on, evidence gaps), so anyone can verify without privileged access or the operator's cooperation.

## Why not one tier down?

At Tier 2 the evidence is signed, but verification runs through an assessor — and in this scenario the live disputes are *with the operator*. If the operator (or an assessor the operator engages and whose tooling needs the operator's key) is the only party who can check the record, then the failure mode that matters most — the operator rewriting or selectively presenting decision history after a dispute begins — stays open: an outsider cannot detect an omission in a log only the operator can verify. Tier 3 closes exactly that gap: mechanism-generated records, verifiable by outsiders with published tooling.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Every receipt carries the model ID and chains to the previous receipt for that agent; which model decided, and the full decision lineage, is third-party checkable. |
| Privacy | 2 | Raw inputs are never stored — only a hash of the input. An assessor can confirm a presented input matches its hash; the hash alone reveals nothing, but confirmation still requires the input to be presented. |
| Portability | not claimed | The receipt format is portable (append-only JSONL), but cross-organization portability semantics are not yet specified; the claim is reserved rather than implied. |
| Authorization | 3 | Authority is declared per decision class in policy, never inferred; confidence maps to routine / supervised / human-in-the-loop tiers, and human-tier decisions gate the action until a named human disposition is appended. |
| Identity | 2 | Receipts chain per agent identity; human override records name the human actor. Cryptographic binding of the agent's identity is the gateway's layer; the receipt binds to the identity the gateway attests. |
| Security | 2 | HMAC-SHA256 over canonical JSON plus the hash chain: tampering with one stored record invalidates its signature and breaks the next link (verified behavior). Asymmetric signing is the named upgrade path; symmetric-key custody is disclosed below as a residual assumption. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `evidence-repudiation` | After a customer dispute, the operator claims the model never made the decision, or made a different one. The signed chain fixes what was decided, when, at what confidence, and under whose authority. |
| `audit-tampering` | An insider edits the decision log before an audit. Editing one record invalidates its signature and breaks the chain at the next record; deletion truncates the chain detectably against the sequence IDs. |
| `context-blind-authorization` | A decision class permitted in one context (informational routing) releases an action in another (a refund). Declared per-class authority and tier gating bind each decision to the context its policy declared. |
| `excessive-agency` | The model acts on decision classes nobody authorized. A class with no policy entry has no declared authority and no tier; the audit flags it instead of the log silently absorbing it. |
| `approval-fatigue` | The human-in-the-loop queue becomes a rubber stamp. Overrides are individual, named, reasoned records — a reviewer who approves everything, instantly, leaves exactly that evidence. |

## What Proof-of-Control does not verify here

From the out-of-scope entries for the tagged threats:

- Whether the authorized boundary was correctly defined (`context-blind-authorization`).
- Whether the authority grant was too broad (`excessive-agency`).
- Insider compromise at the silicon level, disclosed through trust assumptions (`audit-tampering`).
- Disputes about the meaning or significance of an action, rather than whether it occurred (`evidence-repudiation`).
- The human fatigue and social engineering itself (`approval-fatigue`).

Specific to this deployment:

- Whether the model's stated probabilities are *calibrated*. The receipt records the confidence the model stated; it does not attest that the confidence was warranted.
- Whether the chosen option was *correct*. The record proves the decision happened as recorded — not that it was right.
- Whether the policy tiers and thresholds were set wisely. They are operator-declared, disclosed with the receipts, and open to challenge — but setting them is a governance act, not a verification result.

Verification is not validation. Proof-of-Control shows what this agent did and whether each released action stayed inside its controls. It does not judge whether a control was adequate, whether the decision was sound, or whether an effect settled outside the record.

## Residual trust assumptions to disclose

- **Signing-key custody.** The adapter signs with HMAC-SHA256; whoever holds the secret could, in principle, forge a chain from genesis. In this deployment the key is held off the serving host and rotated on suspicion. The durable fix — asymmetric (Ed25519) signatures, so verification needs no secret — is identified and not yet implemented in the adapter. This is the load-bearing assumption behind the Tier 2 placements for Identity and Security above.
- **Policy integrity.** The policy file (decision classes, thresholds, declared authorities) is operator-authored. Its content is disclosed alongside the receipts so auditors judge decisions under the rules as declared; its integrity at decision time is assumed, not proven.
- **Worked-implementation scope.** The implementation wraps a Jev-shaped model stub, not a production decision model; behaviors cited (tier assignment, override records, tamper cascade) were verified against the stub on 2026-09-29.
- **Clock trust.** Receipt timestamps are host-asserted. Anchoring chain heads to an external transparency log is future work, not a current claim.

## Notes / open questions

- This submission is the companion to our public comment on the evaluated-snapshot binding (C7.1.4), filed as an issue on this repository: if the working group prefers decision records as an informative companion rather than a normative binding, the same artifact serves either way.
- Open question for the working group: should the evaluated-snapshot binding name a minimum decision-record field set (options, confidence, declared authority, evidence references, human disposition — as the comment proposes), or remain mechanism-agnostic and let deployments declare their record semantics?
- The control this use case turns on — the gateway actually binding capability release to the decision record's digest — is wired in the scenario's execution path by construction (no digest, no release). A deployment that generates receipts *beside* the path rather than *in* it would not close the repudiation gap at any tier, and this submission does not claim it would.

— Submitted by HUMMBL (Reuben Bowlby, Agentic Systems Architect). The decision-receipt adapter is open source; we are glad to walk the working group through the mapping.
