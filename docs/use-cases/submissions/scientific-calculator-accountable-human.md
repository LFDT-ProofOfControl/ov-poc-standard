---
industry: scientific-research
use_case: A research agent prepares a portfolio-risk worksheet under a human officer's research-only grant before the institution changes providers.
submission_type: scenario
claimed_tier: 3
threats:
  - context-blind-authorization
  - excessive-agency
  - audit-tampering
  - evidence-repudiation
  - trust-opacity
---

# A research agent calculates portfolio risk under an accountable human

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

An institution's research officer authorizes an agent to prepare a monthly
portfolio-risk worksheet. The officer grants research access to a fixed input
version, a named calculator version and an internal review destination. The
agent calculates compounded net asset value and maximum drawdown, then returns
its worksheet for review. The grant permits neither market orders nor external
publication. No client records are used in this example.

The officer later leaves and the institution changes providers. A successor
needs to determine which calculation was authorized, whether its inputs changed
and whether the result can still be recomputed. A signed result alone does not
answer those questions: the evidence must bind the institution, the officer's
current role, the delegated agent and the exact invocation.

## Claimed tier: Tier 3

Tier 3 is the evidence bar proposed for this hypothetical deployment, rather
than a claim about an existing calculator or an assessed implementation.
The successor must be able to verify retained invocation records and recompute
the declared arithmetic without relying on the former provider's account.
That requires authenticated grants, method and input digests, contemporaneous
execution evidence and an externally witnessed integrity commitment whose
signing and monitoring dependencies are disclosed. An operator's signature
plus a reproducible formula does not by itself establish this tier.

The evidence distinguishes the requested calculation, the policy decision,
the dispatched artifact and the returned result. A provider handoff preserves
the old verification material and links the old and new evidence chains.
Neither a digest nor an inclusion receipt establishes that every action was
captured.

## Why not one tier down?

At Tier 2 the successor must accept a provider's or auditor's account of which
inputs and permissions applied. That dependency is the disputed fact when the
provider has changed. Tier 3 requires exportable evidence and disclosed
mechanisms that permit verification without that account.

This task produces a correctable internal worksheet from synthetic data.
It does not claim that an absent record establishes an absent action, or that
all execution paths are mediated. A market order or private-data disclosure
would introduce different consequences and require its own tier assessment;
those effects are outside this scenario.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Evidence binds the method, inputs and invoked artifact; retained inputs permit recomputation. |
| Privacy | not claimed | The public fixture contains synthetic returns and no personal or client data. |
| Portability | 3 | The successor can export and verify the bundle after changing providers. |
| Authorization | 3 | The current human role, bounded delegation and invocation decision can be verified against disclosed authority sources. |
| Identity | 3 | Records separately bind the institution, accountable officer and agent, with disclosed issuer and status dependencies. |
| Security | not claimed | The arithmetic fixture establishes neither environment integrity nor complete mediation. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `context-blind-authorization` | The approved method runs against a later, unapproved input version. |
| `excessive-agency` | The agent attempts an order or external publication under its research-only grant. |
| `audit-tampering` | The former provider substitutes an input or result in retained records. |
| `evidence-repudiation` | The former officer denies authorizing the recorded invocation. |
| `trust-opacity` | The exported bundle omits the issuer, anchor, monitor or verifier dependencies. |

## What Proof-of-Control does not verify here

- Whether the institution granted a sensible scope or selected a sound strategy.
- Whether source market observations are accurate, a scientific method is valid,
  a forecast is reliable or an investment is suitable.
- Whether a transaction settled or a legal interest changed hands.
- Every unrecorded action, uncompromised hardware or the elimination of residual trust.

The declared arithmetic is separately testable. Starting with 100 abstract NAV
units and three synthetic monthly simple returns of +1%, -2% and +3%, with no
cash flows, fees or taxes, compounding gives 101, 98.98 and 101.9494. Maximum
drawdown is 2%, measured from the running peak including the opening value.
There is no intermediate rounding. The [public vector](../fixtures/scientific-calculator.json)
uses decimal strings; the [reference calculation](../fixtures/verify_scientific_calculator.py)
compares decimal and exact rational arithmetic. These are two arithmetic
implementations in one contribution, not an independent assessment of authority
or a historical fund backtest.

## Residual trust assumptions to disclose

- The institution's role register, credential issuers, key custody and the
  status/freshness policy used at the invocation time.
- The calculator artifact, canonical serialization, units, rounding policy,
  input retention and permitted disclosure destination.
- The external integrity anchor, witness or monitor set, their independence
  from the operator, verification material and behavior when freshness or
  monitoring is unavailable.
- The binding from a dispatched invocation to its execution record. A host
  statement about that binding remains a trust dependency unless the declared
  mechanism establishes it.
- The custody and availability of the verification bundle after provider exit.

## Notes / open questions

Proposed refusal vectors include an expired role, changed input digest,
replayed approval, wrong output recipient and an attempted order under the
research-only grant. Only the arithmetic vector accompanies this submission;
these authority and continuity vectors still need an implementation and
assessment. A tier label cannot replace those mechanisms.

An execution record should distinguish the source observation date, invocation
time, evidence-generation time and later verification time. A delayed replay
must not disguise itself as evidence generated during the original execution.

TitleChain/M5 uses x401 for its exact-action authorization profile and x402 for
applicable value-transfer controls. These are implementation terms rather than
adopted Advanced AI Society requirements. A payment receipt cannot supply
permission, title or an institution's appointment. The research-only worksheet
has no settlement step.

Submitted by Pamela Norton, TitleChain Foundation. M5Scientific calculator
research motivates this example; no M5 account, proprietary algorithm or
commercial service is required to reproduce the vector. The contribution is
informative under the repository's Apache License 2.0 and changes no normative
requirement.
