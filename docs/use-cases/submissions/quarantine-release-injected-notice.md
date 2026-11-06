---
industry: pharmaceutical-distribution
use_case: An AI quality agent at a drug wholesaler reads supplier and regulator notices and requests that quarantined lots be released or kept on hold.
business_impact: Recall costs, regulatory exposure and patient risk, with no record able to show that a person approved the release.
submission_type: scenario
claimed_tier: 4
threats:
  - prompt-injection
  - unsafe-actuation
  - approval-fatigue
  - identity-abuse
  - improper-output-handling
  - context-blind-authorization
  - evidence-repudiation
---

# Releasing Quarantined Drug Stock on an Injected Supplier Notice

> *Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.*

## Scenario

A US prescription-drug wholesaler quarantines a lot of an injectable after a trading partner flags it as possibly suspect. Its AI quality agent reads incoming supplier and regulator notices, matches them to held lots and drafts release or keep-hold requests. A release needs sign-off from a named QA pharmacist in the quality system. Once approved, the warehouse system makes the lot pickable, and it ships to pharmacies and hospitals the same day.

A supplier "all-clear" PDF carries hidden text saying the lot is cleared and the release is urgent. The agent drafts a release. The pharmacist, working through forty requests that afternoon, approves it from a summary. Or the agent, still holding her logged-in session, submits the approval itself. Either way the quality system records an approval under her authenticated identity, and the lot ships.

If the notice was fake, suspect product is with patients. The distributor's own logs can't answer the first question it will be asked: did a person approve this release?

## Claimed tier: Tier 4

The release triggers a physical effect that can't be undone, and Authorization and Identity carry the risk. The warehouse gateway must refuse the release unless it holds two things: an approval bound to this lot and this action, and an attestation from outside the quality system that a verified person completed a fresh liveness check for that approval, recorded in a public append-only ledger before the release.

## Why not one tier down?

**Reversibility.** Once cases leave the dock, finding the problem later means a recall, not a fix. Detection after the fact is not a remedy, so enforcement has to refuse the release rather than report it.

**Completeness.** At Tier 3, an approval the agent submitted through the pharmacist's session looks like any other record. At Tier 4 the release cannot run without the evidence, so a missing attestation means the release did not happen.

## Tier by domain

| Domain | Tier | Why |
| --- | --- | --- |
| Provenance | 3 | Which notice the agent read, with its digest and the sender's signature, is recorded, so an injected document can be traced. |
| Privacy | 2 | The approver's name need not reach trading partners; a pseudonymous attestation is enough. Low risk in this deployment. |
| Portability | 3 | Trading partners and an inspector check the release evidence outside the distributor's systems. |
| Authorization | 4 | The warehouse gateway refuses the release without approval evidence bound to the lot and the action. |
| Identity | 4 | The approval must come from a verified person, attested per approval outside the quality system, not inferred from a session. |
| Security | 2 | Document parsing runs isolated from the agent's tools; claimed at audit level only. |

## Threats exercised

| Threat | What it looks like here |
| --- | --- |
| `prompt-injection` | Hidden text in a supplier PDF tells the agent the lot is cleared. |
| `unsafe-actuation` | An approved release moves physical stock that ships the same day. |
| `approval-fatigue` | The pharmacist approves dozens of agent requests from summaries. |
| `identity-abuse` | The agent submits the approval through the pharmacist's live session. |
| `improper-output-handling` | The agent's draft reaches the quality system as if it were a reviewed decision. |
| `context-blind-authorization` | The release is checked against the agent's permissions, not against why the lot was held. |
| `evidence-repudiation` | Afterwards the pharmacist says she never approved it, and the logs can't settle it. |

## What Proof-of-Control does not verify here

- **The notice.** That the supplier notice was genuine, or that the lot is safe.
- **The decision.** That the pharmacist's judgment was right, or that she read the notice before approving.
- **The physical goods.** That the cases on the dock match the lot record.
- **The hold.** That the reason for the quarantine was entered correctly.
- **The liveness check.** That it was not defeated; that rests on the attester.
- **Validation.** Verification is not validation: the evidence shows the release stayed within its controls, not that the controls were adequate.

## Residual trust assumptions to disclose

- **The liveness attester** and the identity-verification process behind the person it attests.
- **The public ledger** and its monitors, and what happens if monitoring lapses.
- **The warehouse gateway** enforcing the check on every release path; any bypass voids Tier 4.
- **The supplier's signing keys** for the notices the agent reads.
- **The quality system** computing the digest of what it actually showed the pharmacist.

## Notes / open questions

- Whether one QA approval or a two-person rule applies is a policy choice the standard shouldn't fix.
- Suspect-product rules such as the US DSCSA inform the hold; this use case makes no claim about compliance with them.

Submitted by Vivian Chan - 5arz.com
