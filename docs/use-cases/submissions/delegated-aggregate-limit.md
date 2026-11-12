---
industry: procurement
use_case: Orchestrator agent delegates supply ordering to sub-agents under one aggregate spending limit
business_impact: Orders that each pass local policy together exceed the principal's limit, and no party's records show it
submission_type: scenario
claimed_tier: 4
threats:
  - context-blind-authorization
  - excessive-agency
  - identity-abuse
  - insecure-inter-agent-comms
  - unbounded-consumption
  - trust-opacity
---

# Sub-Agents Exceeding an Aggregate Limit That No Single Hop Violates

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

An enterprise authorizes an orchestrator agent to place supply orders up to an
aggregate limit. The orchestrator delegates tasks to three sub-agents: research,
negotiation, and execution.

Each sub-agent operates within its local scope. The execution agent places
three separate orders, each below the per-order limit, and together they exceed
the aggregate limit. No alert fires, because no hop violates local policy. No
party has a global view of the delegation chain, and the operator's own logs
show complete compliance.

What is at stake is committed spend. An order accepted by a vendor is an
obligation the enterprise now carries, and the party that needs to know whether
the limit held, whether an auditor, a regulator or an insurer, has only the
operator's account of it.

## Claimed tier: Tier 4

The control that matters here is a sum across branches of a delegation chain,
and the action it governs creates an obligation as soon as it runs. Tier 4 is
the tier at which an order cannot be placed without producing evidence, and an
order whose evidence does not verify is refused.

Reaching it requires that the evidence artifact of each sub-agent
cryptographically binds its delegated authority to the parent grant, and that
each order is bound to the portion of the aggregate it consumes. Committed
consumption plus remaining reserved capacity has to stay within the principal's
limit across every branch, the same capacity cannot authorize two orders, and
an order stays blocked when the consumption state cannot be established. The
verification runs before the order is sent, against the original principal's limit
rather than against the hop's local scope.

## Why not one tier down?

At Tier 3 an external verifier can reconstruct the chain from the records it
holds and see that the three orders sum past the limit. Two things are wrong
with stopping there.

**Reversibility.** The verifier sees the breach after the third order has been
accepted. Detection is not a remedy for a commitment already made to a vendor.
The case for Tier 4 is that the third order has to be refused rather than
reported.

**Completeness.** At Tier 3 the records held are unaltered, and nothing
guarantees they are all the records. An aggregate is only as good as its
operands: one order placed off-record makes the verified sum wrong while every
record still verifies. At Tier 4 an order cannot execute without producing
evidence, so the absence of a record means the order was not placed, and the
sum is a sum over everything.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | The lineage of authority, from the principal's grant through the orchestrator to each sub-agent, has to be reconstructable by an external verifier without privileged access to the operator's system |
| Privacy | not claimed | The scenario turns on spending authority; no personal data is in the path described |
| Portability | not claimed | One operator and one platform; no claim is made about evidence surviving a move across vendors or environments |
| Authorization | 4 | The aggregate limit is the load-bearing control. Each order must be bound to the capacity it consumes and refused when the sum across all delegation branches would pass the principal's limit |
| Identity | 3 | Each order has to be attributable to the agent that placed it and to the principal whose grant it draws on, in a form anyone can verify |
| Security | 3 | The integrity of the chain itself: a hop's evidence that does not bind to its parent grant, or a chain with a missing link, has to be detectable by the verifier |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `context-blind-authorization` | Each order is an in-scope call for the execution agent. It is wrong only in the context of the two orders before it, which the local verification does not see |
| `excessive-agency` | The execution agent can commit more in total than the share of the principal's limit its task needs, because its scope is expressed per order |
| `identity-abuse` | A sub-agent acts on authority derived through two hops. Without a verifiable delegation chain, nothing distinguishes authority the principal granted from authority a hop assumed |
| `insecure-inter-agent-comms` | The delegations from orchestrator to sub-agents are agent-to-agent messages. If they are not bound to signed identities, the chain cannot be reconstructed from them |
| `unbounded-consumption` | The aggregate limit is a budget cap. Spend runs past it in increments that each look permitted |
| `trust-opacity` | A reader of the operator's compliant logs cannot tell what they would have to trust for those logs to mean the limit held |

## What Proof-of-Control does not verify here

- **Whether the aggregate limit was well-defined.** Proof-of-Control shows that
  the orders stayed within the limit the principal granted. It does not show
  that the limit was the right number, or that it was drawn around the right
  set of orders.
- **Whether the grant was too broad.** That the execution agent held authority
  to commit the whole aggregate is visible in the chain. Nothing in the
  evidence says it should have held less.
- **Whether the per-vendor concentration policy was correctly instrumented.**
  A policy stated in documentation and never placed in the execution path
  produces no evidence either way. See the notes below and the closing section
  of THREATS.md.
- **Whether the orders were commercially sensible.** An in-bounds order at a
  bad price, or for the wrong quantity, is an in-bounds order.
- **Credential theft or social engineering at the human level.** A principal
  who was deceived into issuing the grant, or whose credential was taken,
  produces a chain that verifies.
- **The cost of evidence at each boundary.** Latency added by verifying the
  chain before every order is an engineering trade-off outside the claim.
- **Whether the vendor fulfilled the order.** The evidence covers the order
  being placed within authority. Delivery, invoicing and settlement are effects
  in the outside world.
- **Eliminating trust.** The standard requires that residual trust be
  disclosed, as below. It does not require that there be none.

That is validation, not verification.

## Residual trust assumptions to disclose

- **Hop-to-hop signatures.** Each hop in the chain trusts the previous hop's
  signature. The disclosure states how many independent parties would have to
  collude to forge or suppress evidence; the scenario assumes a collusion
  threshold of 0 where each hop can be verified on its own, by anyone. Where a
  hop cannot, the disclosure has to say so and give the number for that hop.
- **Root of credential issuance.** Whoever issues the principal's credential
  and the agents' credentials. If one enterprise identity provider issues all
  of them, it is the single root and the disclosure names it.
- **The consumption state.** The aggregate is enforced against a record of
  capacity already committed and reserved. A reader trusts that this state is
  authoritative, that restoring saved state cannot make consumed capacity
  available again, and that two branches cannot draw on the same capacity.
- **The gate.** At Tier 4 a reader trusts that the path that sends an order to
  a vendor cannot be reached except through that verification. Any second path, such
  as a manual override or a vendor portal session, is outside the claim and
  has to be named.
- **Freshness and revocation.** How quickly a revoked or narrowed grant reaches
  sub-agents already holding a delegation under it, and what they can commit
  in that window.
- **The attestation chain,** with its version, if the claim that a given agent
  instance placed an order rests on hardware or platform attestation, and any
  point where two attestations are assumed to describe the same machine.
- **Monitors of any transparency log** that holds the evidence, and what a
  verifier can conclude if they lapse.

## Notes / open questions

- The scenario also contains a control that no tier reaches. If the per-vendor
  concentration limit exists in documentation and was never instrumented,
  nothing is violated, because nothing enforces it, and no evidence is
  produced. Silence is indistinguishable from compliance. Raising the tier of
  the aggregate-limit claim does not touch this; the conformance criteria have
  to name the mechanism for each claimed control.
- Reasonable people may place Identity at Tier 4 rather than Tier 3, on the
  argument that the gate cannot enforce an aggregate across a chain it has not
  verified, so identity binding is enforced at serving time whether or not it
  is claimed. It is left at Tier 3 here because the scenario's failure is one
  of authorization: every agent in it is who it says it is.
- A Tier 3 placement is defensible where orders can be cancelled without cost
  inside a known window, since detection would then be a remedy. The claim
  here assumes an accepted order is a commitment.
- Open question: how the principal's limit is divided across branches. A fixed
  split refuses orders a different split would have allowed. A shared pool
  needs the consumption state to be consistent across branches at the moment
  each order is verified.
- Open question: the per-order limit and the aggregate limit are two
  boundaries on one action. The scenario treats only the aggregate as
  load-bearing.
- Adapted from the example in Section 9 of the working draft, "An example of
  the lack of Proof-of-Control in practice", and brought to the v2 template.
