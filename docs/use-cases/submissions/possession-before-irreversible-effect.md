---
industry: payments
use_case: A payment agent releases an irreversible transfer only after a fresh human possession check bound to that transfer
submission_type: scenario
claimed_tier: 4
threats:
  - prompt-injection
  - identity-abuse
  - excessive-agency
  - approval-fatigue
  - evidence-repudiation
---

# Possession check before an irreversible transfer

> Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.

## Scenario

A person authorizes a personal agent to pay a named beneficiary a stated amount.
The agent holds a payment tool. An injected instruction tells the agent to pay
a different beneficiary a larger amount. The gateway holds the tool call. The
call proceeds only when a possession protocol accepts for a challenge whose
digest is the canonical payment, and the nonce is then consumed. A second
presentation of the same capability is refused and the refusal is recorded.
The person enrolled earlier under a stable principal reference. The witness
used to answer the challenge is not in the evidence record. The payment
network's settlement, if the gateway releases the call, is outside the record.

## Claimed tier: Tier 4

The risky domain is authorization of an irreversible transfer. Tier 4 here
means the gateway does not release the payment tool unless the possession
capability verifies, so a missing or replayed check is a refused call rather
than a later finding. Identity of the possession transcript is Tier 3 in the
domain table: an outsider recomputes acceptance from the commitment, the
challenge, and the response, and the operator's boolean is not an input.
The overall tier follows the irreversible release, not the average of the
domains.

## Why not one tier down?

At Tier 3 an assessor can recompute the possession transcript and can see
that a capability was absent or rebound. The transfer has already settled.
The person cannot unpay the beneficiary the injection named. Reversibility
fails, so detection after release is not the control this case is calibrating.
Completeness fails the same way at Tier 3: an agent that can reach the
payment tool without passing the gateway produces no possession record, and
the absence of a record does not show the payment did not happen. Tier 4
closes that arm only for the tool path the gateway mediates. A side path
the gateway does not mediate is disclosed as residual, not graded as Tier 4.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 2 | The checker is identified by a published digest. A supply-chain signature chain on that checker is not required to refuse the payment. |
| Privacy | 3 | The evidence record carries digests and the principal reference. The witness stays out of the record, and an outsider checks the transcript without receiving the witness. |
| Portability | not claimed | The case does not move the agent across a trust domain. |
| Authorization | 4 | The gateway refuses the payment tool when the single-use capability is missing, rebound, or already consumed. |
| Identity | 3 | The possession-bound profile keeps the principal reference and withholds the witness. An outsider recomputes the check. A copied bearer token with no fresh possession record is refused. |
| Security | 2 | The checker runs as a named sandbox with a recorded configuration. Hardware attestation of that sandbox is not the control that refuses the payment. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `prompt-injection` | Injected text names a different beneficiary and a larger amount. The gateway still demands a capability for the canonical payment the human answered. |
| `identity-abuse` | A copied payment token is presented without a fresh accepted possession record for this nonce. |
| `excessive-agency` | The agent can call the payment tool for any beneficiary it can name. The release path accepts only the digested payment. |
| `approval-fatigue` | The screen and the tool call can diverge. The capability cites the challenge digest and the action digest, and a missing mapping refuses release. |
| `evidence-repudiation` | The operator cannot substitute a later story for the signed possession record and the refusal or release record. |

## What Proof-of-Control does not verify here

The injection string itself is out of scope. The case records the action the
injection tried to release and whether the gateway refused it.

Whether the enrolled principal is the legal account holder, beyond the
principal reference and the disclosed enrollment, is out of scope.

Whether the amount and the beneficiary were a wise payment is out of scope.
A possession check of a payment the human did intend still releases that
payment.

Whether the human was coerced, or answered a screen whose pixels are not
covered by the challenge digest, is residual trust. If no published function
binds the sentence on the screen to the canonical payment bytes, the approval
does not authorize the tool call.

Whether the payment network settled, reversed, or paid a different account
than the canonical request named is out of scope. Message binding is not
endpoint effect binding. An endpoint that applies a server-side default
beneficiary is outside this claim unless that endpoint meets the effect-binding
conditions the standard is separately considering.

Credential theft at the human layer, including a person tricked into answering
a challenge for a payment they did not mean, is only partly in scope. The
record shows which challenge was answered. It does not show the person's
understanding.

A standing session left open after the check is not this capability. If the
deployment also issues a time-bounded session, that session is a separate
grant and is disclosed. It is not evidence that no standing credential exists.

## Residual trust assumptions to disclose

The human can be coerced. The protocol does not remove that party.

The checker digest must match the published checker. The runtime that
executed the checker is a pinned-checker assumption, not a hardware quote,
unless a separate attestation says so.

The evidence-signing key has its own custody, rotation, and compromise
procedure. The possession witness is not that key. Compromise of the witness
is re-enrollment. Compromise of the signing key re-grades the records that
key signed.

The enrollment seal, if the witness was moved to a recipient, names that
recipient. A party who can open the seal is disclosed. The seal's
encapsulation algorithm is not the evidence signature's algorithm.

The nonce store and the gateway are assumed to be the only path to the
payment tool. A tool credential reachable around the gateway is a failed
mediation, not a residual to accept silently.

Monitors on any transparency log that anchors the release records, and the
consequence of a lapsed monitor, are disclosed with the log. This scenario
does not remove that assumption.

## Notes / open questions

This scenario is the pattern. It is not a conformance claim for any shipping
client. The on-device half of the pattern, a fresh challenge, a response, a
pinned wasm checker, a local grant only on acceptance, and a witness that is
sealed rather than stored in plaintext by the enrollment authority, is what
ENI6MA PassPlus runs. Those clients do not stand in front of a payment tool,
and they do not export an outsider verifier that ignores the local boolean.
The Tier 4 cell in this file is the gateway the standard currently fails to
require, not a halt those clients perform.

A local boolean signed by the device, with no outsider recomputation, would
place Identity at Tier 2 and would pull the overall claim off Tier 4, because
the capability would cite an artifact the payee cannot recompute. That
downgrade is the point of the companion note on operator booleans.

`prompt-injection` had no worked use case in the coverage index when this
story was added. The tag means the deployment is exposed to injection. It
does not mean the possession check detects malicious text.
