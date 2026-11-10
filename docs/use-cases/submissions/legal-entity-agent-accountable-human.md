---
industry: small-business-commerce
use_case: A resale cooperative's selling agent lists, sells, and settles members' pre-owned goods under authority granted by an officer who later leaves.
submission_type: scenario
claimed_tier: 3
threats:
  - identity-abuse
  - excessive-agency
  - context-blind-authorization
  - approval-fatigue
  - audit-tampering
  - evidence-repudiation
  - trust-opacity
---

# A cooperative's selling agent, an accountable officer, and a change of hands

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A small resale cooperative sells its members' pre-owned clothing online. Its selling agent
lists items, accepts offers, issues refunds, and releases payment to members once delivery is
confirmed. The cooperative is the principal, but it acts through a person: its operations
officer configured the agent and issued its grant under a board-approved role. Payments are
held until delivery is confirmed and then released.

Three months later the officer leaves. Afterwards a member disputes a refund the agent issued,
a buyer claims an item was misdescribed, and the cooperative moves its agent to a cheaper
provider. Each question turns on evidence: was the refund within the agent's authority, who
was accountable for that authority on that date, and does the record survive the move to the
new provider?

## Claimed tier: Tier 3

Every party to a dispute here has a reason to doubt the cooperative's own logs: the departed
officer, the member, the buyer, and the old provider. Tier 3 lets each of them verify the
evidence from published material without trusting the operator: the grant and its scope, the
officer's role authority on the grant date, each refund decision, and the payment hold's event
history.

## Why not one tier down?

At Tier 2 the evidence rests on the operator's or provider's attestation. After the officer
leaves and the provider changes, the parties most likely to dispute the record are the ones
asked to trust it, and the old provider is no longer a party to anything. Settlement harm here
can be undone while payment is held, so the use case does not need Tier 4's fail-closed
gating; it does need a record that survives the change of people and provider.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | not claimed | The agent's model and listing inputs are not in dispute in this scenario. |
| Privacy | 2 | Member and buyer details stay in the cooperative's own store; shared evidence carries identifiers and digests only. |
| Portability | 3 | The record must verify after the move to a new provider, through a signed linking record. |
| Authorization | 3 | Each refund and release must be shown to fall within the grant, evaluated at execution time. |
| Identity | 3 | Each action must resolve to the agent, the cooperative, and the officer accountable on that date, through a signed chain. |
| Security | 2 | Key custody and rotation must not change who the cooperative or officer is. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `identity-abuse` | After leaving, the officer's still-valid credential is used to widen the agent's grant. |
| `excessive-agency` | The agent can issue refunds of any size, though the grant intended a cap. |
| `context-blind-authorization` | A refund that is in scope is issued after the item was already released to the member. |
| `approval-fatigue` | The officer approves batches of high-value refunds the agent queued without reading them. |
| `audit-tampering` | The old provider's logs are lost or rewritten after the cooperative leaves. |
| `evidence-repudiation` | The departed officer denies having granted refund authority. |
| `trust-opacity` | The new provider's evidence rests on assumptions the cooperative cannot see. |

## What Proof-of-Control does not verify here

- Whether the board was right to give the officer that role, or whether the grant's scope was
  sensible.
- Whether an item really matched its listing; Proof-of-Control shows the claim and the
  decision, not the garment.
- Whether a released payment actually reached the member's bank.
- Credential theft or social engineering of the officer, which is out of scope for
  `identity-abuse`.

## Residual trust assumptions to disclose

- The cooperative's governance records are the root for who held the officer role and when.
- The issuers of the officer's and agent's credentials, and their revocation policy.
- The old and new providers' signing keys, and the key that signs the linking record between
  their evidence chains.
- The timestamp or transparency-log anchor used for both chains, and its monitors.

## Notes / open questions

- The draft resolves every action to "a named principal" (5.1.1). Here that needs three
  identifiers: the agent, the cooperative, and the officer accountable at grant time. This bears
  on Appendix D issue 1.
- When the officer leaves, the grants they issued should be revoked or reaffirmed by a successor
  within a declared interval. The draft has no requirement for this.
- A buyer-facing pseudonym for the cooperative, linkable under declared conditions, would answer
  Appendix D issue 2 for small sellers that do not want to expose members.
- Holding payment until delivery is confirmed lets a refund reverse the hold instead of
  recovering money from payees; the hold's event log should be hash-chained (7.3.1).
- A profile proposing requirements for these points is described in
  [`docs/proposals/titlechain-legal-entity-agent-profile.md`](../proposals/titlechain-legal-entity-agent-profile.md).
