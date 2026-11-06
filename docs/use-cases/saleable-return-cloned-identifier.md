---
industry: pharmaceutical-distribution
use_case: An AI returns agent at a drug wholesaler verifies returned units and decides whether they go back into saleable stock.
business_impact: Counterfeit product re-enters the supply chain under a genuine serial number, with patient risk, recall costs and regulatory exposure, and no record able to show what was checked or who approved it.
submission_type: scenario
claimed_tier: 4
threats: [unsafe-actuation, improper-output-handling, context-blind-authorization, approval-fatigue, evidence-repudiation]
---

# Restocking a Returned Unit Whose Identifier Was Copied

*Illustrative, hypothetical scenario for calibration. Not necessarily indicative of any specific organization's current state.*

## Scenario

Under DSCSA, a wholesaler must verify the product identifier of a returned unit before reselling it. A distributor's AI returns agent scans each returned bottle's 2D barcode, sends the identifier to the manufacturer's verification service, and drafts "restock" when the response says the identifier is valid. A returns supervisor approves restocks in batches.

A pharmacy returns a bottle that is counterfeit. Its label carries a genuine serial number copied from a real bottle, so the verification service confirms it. The agent drafts "restock". The supervisor approves the batch, and the bottle goes back into saleable stock and ships the next day.

When the genuine bottle with the same serial number turns up elsewhere, the distributor's record shows only that an identifier was verified. It can't show that this physical bottle was checked, or that a person approved putting it back on the shelf.

## Claimed tier: Tier 4

Restocking puts a unit back into the supply chain and can't be undone once it ships. The restock gateway must refuse a restock unless it holds:

1. a check of the physical unit, read by equipment outside the agent's control, using an identifier bound to the unit that a copied label can't reproduce;
2. the verification response for that identifier;
3. an attestation from outside the returns system that a verified person completed a fresh liveness check for this restock, bound to the digests of 1 and 2, recorded in a public append-only ledger before the restock.

## Why not one tier down?

**Data is not the unit.** A verification response shows that a serial number exists and is valid, not that the bottle in hand is the one it was issued for. At Tier 3 an outsider can later see the duplicate. At Tier 4 the restock can't run without a check of the unit itself.

**Batch approval hides the unit.** Binding the approval to each unit's check means the approver signs off on what was found for that bottle, not on a count.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 4 | The physical check and the verification response are bound to the restock by digest. |
| Privacy | 2 | The approver's name need not reach trading partners; a pseudonymous attestation is enough. |
| Portability | 3 | The manufacturer and an inspector check the restock evidence outside the distributor's systems. |
| Authorization | 4 | The gateway refuses a restock without approval bound to the unit and its checks. |
| Identity | 4 | The approval must come from a verified person, attested per approval, not inferred from a session. |
| Security | 2 | Readers and the gateway are tamper-evident; claimed at audit level only. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| unsafe-actuation | An approved restock puts a counterfeit unit back into saleable stock. |
| improper-output-handling | A "valid identifier" response is treated as proof the unit is genuine. |
| context-blind-authorization | The restock is checked against the agent's permissions, not against what was checked on the unit. |
| approval-fatigue | The supervisor approves restocks in batches. |
| evidence-repudiation | Afterwards, the record can't show which bottle was checked or who approved it. |

## What Proof-of-Control does not verify here

- **The unit's contents.** That the product inside is genuine and unadulterated, only that the unit's identifier wasn't copied.
- **The physical identifier.** That it can't be defeated; that rests on its design and is disclosed.
- **The verification service.** That its data is correct.
- **The decision.** That the supervisor's judgment was right.
- **Validation.** The evidence shows the restock stayed within its controls, not that the controls were adequate.

## Residual trust assumptions to disclose

- **The physical identifier** on each unit and the readers that check it.
- **The verification service** and its response signing.
- **The liveness attester** and the identity-verification process behind it.
- **The public ledger** and its monitors.
- **The restock gateway** enforcing the check on every restock path; any bypass voids Tier 4.

## Notes / open questions

- For units without a physical identifier, should the standard allow Tier 3 with a disclosed gap?
- This use case makes no claim about compliance with DSCSA saleable-returns rules.

Submitted by Vivian Chan - 5arz.com
