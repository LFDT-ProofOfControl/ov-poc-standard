---
industry: agentic-commerce-payments
use_case: An autonomous agent pays suppliers machine-to-machine within a delegated cap, and a dispute later needs a record the facilitator cannot unilaterally rewrite or deny
submission_type: scenario
claimed_tier: 3
threats:
  - audit-tampering
  - evidence-repudiation
  - context-blind-authorization
---

# Verifying a Disputed Machine-to-Machine Payment Without the Facilitator's Cooperation

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A small business owner delegates a spending agent authority to pay a specific
supplier autonomously, up to a per-invoice cap, over a machine-to-machine
settlement flow (an HTTP 402-style payment request answered by the agent and
relayed through a payment facilitator). Weeks later the supplier disputes the
amount on one invoice, and separately the facilitator migrates its billing
database. The owner now needs to know, without taking either party's word for
it: did the agent's delegation actually permit that invoice, was the record
the facilitator is showing today the same one that existed at settlement
time, and could anyone — not just the facilitator — have caught it if it
were not?

## Claimed tier: Tier 3

This deployment anchors a content hash of the delegation record and of each
authorized-action record to a public, permissionless on-chain registry at
settlement time. Any outside party — the owner, the supplier, or an
auditor — can independently recompute that hash from the fields they each
hold and check it against a publicly queryable on-chain event, without an
account, a credential, or any cooperation from the facilitator. The parties
the claim's soundness rests on (the chain's own validators, not the
facilitator) are disclosed below rather than removed.

## Why not one tier down?

At Tier 2 the owner would be relying on the facilitator's own attestation, or
on a third-party auditor's periodic review, that the facilitator's internal
log is accurate. That is exactly the posture that fails the moment the
facilitator's database migration — or the facilitator itself — is the party
being disputed. The record the owner needs has to be checkable without the
facilitator's continued cooperation, goodwill, or even continued existence,
which is what moves this from Tier 2 to Tier 3: the facilitator's word is no
longer part of the proof.

Reversibility test: the payment has settled and the funds have moved by the
time a dispute surfaces; the harm cannot be undone by better logging after
the fact, only argued about with an unmovable record. Completeness test:
the owner can verify that a record they hold has not been altered since it
was anchored (Tier 3), but nothing here guarantees the owner was ever given
every record that should exist — an action taken off this flow entirely
would leave no gap to notice, which is exactly the limit Tier 4 would close
and this deployment does not reach (see below).

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | The delegation record and each authorized-action record are each a deterministic hash over a fixed field set. Recomputing that hash and checking it against the on-chain `Anchored(bytes32 indexed ref, address indexed anchoredBy, uint256 timestamp)` event emitted by a permissionless registry contract is open to anyone who holds the fields — no account with, or credential from, the facilitator is required. |
| Privacy | not claimed | The anchored value is a hash, not the underlying fields — but this deployment makes no disclosure-control claim about who is given the pre-image out of band. |
| Portability | not claimed | — |
| Authorization | 3 | The delegation chain (who granted the cap, to whom, and its revocation state) is itself a hash-linked structure. A third party can walk the chain and check whether a revocation record for the grant in question has itself been anchored, independent of what the facilitator's live system currently shows. |
| Identity | not claimed | The registry anchors a content hash, not an attested identity. Whatever signs the delegation and the action is a key the owner and agent control under their own key-management practice, outside this deployment's scope. |
| Security | not claimed | This deployment claims nothing about the agent's runtime environment, its hardware, or its resistance to compromise. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `audit-tampering` | If the facilitator's operational database were altered after settlement — by compromise, an internal actor, or an undocumented migration — the on-chain anchor is the fixed point no single party, including the facilitator, can quietly rewrite. The hash committed to at a given block does not move; a later value claiming to be "the same record" either matches it or does not. |
| `evidence-repudiation` | The facilitator cannot later deny that a specific delegation or action record existed with specific field values at a specific time, because the dispute does not turn on the facilitator's word: the owner or the supplier recomputes the same hash from the fields they each kept and checks it against the registry's publicly queryable event log, without the facilitator's participation. |
| `context-blind-authorization` | The cap was authorized for one supplier relationship. If the same delegation were used (or replayed) against a different, unauthorized context, the independently recomputable delegation-chain record shows which specific grant and revocation state was actually in force, rather than relying on the facilitator's account of which context applied. |

## What Proof-of-Control does not verify here

- Out of scope for `audit-tampering`: insider compromise at the silicon level. This deployment discloses no hardware attestation over the signing environment that produced the record (Security is "not claimed" above); that the signing key was not compromised before signing is a trust assumption, not a verified fact.
- Out of scope for `evidence-repudiation`: disputes about the meaning or significance of an action, rather than whether it occurred. The anchor proves a specific record existed with specific field values at a specific time. It says nothing about whether the amount, the counterparty, or the business purpose of that payment was legitimate or wise.
- Out of scope for `context-blind-authorization`: whether the authorized boundary itself was correctly defined. This deployment verifies that the delegation chain in force matches what is claimed; it does not verify that granting that cap in the first place was a sound decision.
- Specific to this deployment: anchoring happens after the action is recorded, not as a precondition of settlement — a payment can in principle complete in the brief window before its record is anchored, which is the gap that would need closing to reach Tier 4. The registry also anchors a hash, not the underlying record: a party who never received the underlying fields from the owner, the agent, or the facilitator has nothing locally to recompute against the anchored value, and cannot verify anything from the anchor alone. The anchor gives non-repudiation and tamper-evidence to a record someone already holds; it does not distribute that record.

## Residual trust assumptions to disclose

- The signing key(s) used to construct the delegation record and the action record are assumed uncompromised at the moment of signing. No hardware attestation over the signing environment is disclosed (see Security, above).
- The registry contract — a public, permissionless `anchor(bytes32 ref)` call emitting an `Anchored` event — is assumed to keep running and its event log to stay queryable. It is deployed at the same address via `CREATE2` across three public EVM chains (Base, Arbitrum One, and Ink), so a verifier is trusting the continued availability of at least one of those three, not any single operator or any single chain's continued existence.
- A verifier recomputing the hash is trusting that whoever handed them the underlying fields (owner, supplier, or facilitator) handed them the real fields, not a fabricated set that happens to hash to the value found on-chain. The anchor fixes a value in time; it does not vouch for who the pre-image actually came from.
- The delegation chain's revocation state is only as current as the last revocation record that was itself anchored. A revocation that was issued but never anchored is not yet verifiable by an outside party.

## Notes / open questions

This scenario is calibrated against a real, production, permissionless anchoring mechanism rather than against any specific disputed payment — named here because it costs nothing to name and lets a reviewer check it directly rather than take the description on faith. `AnchorRegistry` (`giskard09/giskard-payments`, `AnchorRegistry.sol`) is a single-function `anchor(bytes32 ref)` contract emitting `Anchored(bytes32 indexed ref, address indexed anchoredBy, uint256 timestamp)`, deployed via `CREATE2` at the identical address `0x49fEcA52bC634a9Ab773226D16619deC547794aa` on three public EVM chains — Base, Arbitrum One, and Ink — each independently source-verified on its own explorer, in active use anchoring machine-to-machine action records since mid-2026. Any reader can confirm the deployment and the event independently with a bare JSON-RPC call (`eth_getCode` at that address on each chain, or an `eth_getLogs` query for the `Anchored` topic), without trusting this document, the facilitator in the scenario above, or us. The dispute narrative itself remains a calibration device, not a report of an actual case.

Open question for the working group: [C7.2.2](../../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md#c72-the-contemporaneous-property) names an RFC 3161 timestamp authority, a transparency-log inclusion proof, or consensus time as acceptable anchoring sources. A permissionless smart-contract event log on a public chain, as used here, sits closest to "consensus time," but without a log-monitor role and without the per-record [RFC 6962](https://www.rfc-editor.org/rfc/rfc6962) inclusion-proof structure that [C7.3.4](../../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md#c73-the-tamper-evident-property) asks for. Is querying the event log for a given `ref` and confirming it was included in a finalized block sufficient to satisfy C7.3.4 on its own, or does Tier 3/4 conformance through this mechanism need an RFC-6962-style inclusion/consistency-proof structure layered on top of the chain's own finality — which would be a meaningfully larger build for any permissionless, no-operator anchoring design, not just this one?
