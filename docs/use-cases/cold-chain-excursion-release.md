---
industry: pharmaceutical-distribution
use_case: An AI quality agent at a drug distributor reviews temperature excursions on cold-chain shipments and recommends whether affected stock can still be sold.
business_impact: Patients receive product that may have lost potency, with recall costs and regulatory exposure, and no record able to show what data the release relied on or that a person approved it.
submission_type: scenario
claimed_tier: 4
threats: [rag-weakness, misinformation, unsafe-actuation, approval-fatigue, context-blind-authorization, evidence-repudiation]
---

# Releasing Insulin After a Temperature Excursion on the Wrong Stability Data

*Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.*

## Scenario

A distributor receives a tote of insulin pens whose temperature log shows six hours above the labeled range in transit. Its AI quality agent looks up the manufacturer's stability data for permitted time out of refrigeration, compares it with the excursion and drafts a disposition: release, or hold for destruction.

The retrieval step returns the stability document for a different insulin product with a longer allowance. The agent concludes the excursion is within limits and drafts "release". A QA pharmacist approves it from the agent's summary, which says "excursion within manufacturer allowance". The pens go back into saleable stock and ship to pharmacies that afternoon.

When a pharmacy reports a complaint, the distributor can't show which temperature data and which stability document the release relied on. It also can't show that a person, rather than an agent using her session, approved it.

## Claimed tier: Tier 4

The release puts product in patients' hands and can't be undone. The release gateway must refuse to return the stock to saleable status unless it holds:

1. the temperature record captured with the unit or tote by a logger outside the agent's control;
2. the digest of the stability document the agent relied on, identified by product;
3. an attestation from outside the quality system that a verified person completed a fresh liveness check for this release, bound to the digests of 1 and 2 and to the lots released, recorded in a public append-only ledger before the release.

## Why not one tier down?

**Reversibility.** Once pens reach patients, finding the error means a recall and possible harm, not a correction. The release must be refused, not reported.

**Retrieval is the weak point.** At Tier 3 an outsider can later see that the wrong document was used. At Tier 4, binding the approval to the document's digest puts the document in front of the approver, and the gateway can check that its product matches the lot.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 4 | The temperature record and the stability document are bound to the release by digest; a release citing a document for a different product is refused. |
| Privacy | 2 | The approver's name need not reach pharmacies; a pseudonymous attestation is enough. |
| Portability | 3 | A pharmacy, manufacturer or inspector checks the release evidence outside the distributor's systems. |
| Authorization | 4 | The gateway refuses a release without approval bound to the lots, the temperature record and the stability data. |
| Identity | 4 | The approval must come from a verified person, attested per approval, not inferred from a session. |
| Security | 2 | Loggers and the gateway are tamper-evident; claimed at audit level only. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| rag-weakness | Retrieval returns another product's stability document. |
| misinformation | The agent states the excursion is within allowance. |
| unsafe-actuation | An approved release puts possibly degraded product back into saleable stock. |
| approval-fatigue | The pharmacist approves from a one-line summary. |
| context-blind-authorization | The release is checked against the agent's permissions, not against which product the data was for. |
| evidence-repudiation | Afterwards, no record shows what the release relied on or who approved it. |

## What Proof-of-Control does not verify here

- **The product.** That the pens are still potent. That is a stability question, not an evidence question.
- **The logger.** That the temperature record is accurate; that rests on the logger and its calibration.
- **The stability data.** That the manufacturer's document is correct, only that the release relied on the document for this product.
- **The decision.** That the pharmacist's judgment was right, or that she read the document.
- **The liveness check.** That it was not defeated; that rests on the attester.

## Residual trust assumptions to disclose

- **The temperature loggers** travelling with the units, their calibration and signing keys.
- **The source of stability data** and how documents are identified by product.
- **The liveness attester** and the identity-verification process behind it.
- **The public ledger** and its monitors.
- **The release gateway** enforcing the check on every release path; any bypass voids Tier 4.

## Notes / open questions

- Whether an excursion release needs one QA approval or two is a policy choice the standard shouldn't fix.
- Good distribution practice and labeled storage conditions inform the hold; this use case makes no claim about compliance with them.

Submitted by Vivian Chan - 5arz.com
