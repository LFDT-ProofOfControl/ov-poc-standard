---
industry: software-engineering
use_case: A worker agent writes a change, a reviewer agent reviews it, the worker corrects it once and the reviewer re-reviews it; the "corrected and accepted" outcome must rest on the right review of the right result.
submission_type: scenario
claimed_tier: 3
threats:
  - context-blind-authorization
  - insecure-inter-agent-comms
  - excessive-agency
  - unbounded-consumption
---

# Reviewed correction loop between two agents

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

Lena maintains a small library. She gives two AI agents one signed, bounded mandate
for one task: fix a parsing function so that durations above a limit raise an error.
The mandate fixes the plan in advance: hop 1, agent A writes the change; hop 2, agent
B reviews it; hop 3, A corrects it if B asked for changes; hop 4, B re-reviews the
correction. There is no hop 5. The mandate also fixes a cost cap per hop, a cap on the
number of handoffs, a cap on the number of attempts, and an expiry. An independent
receiver, not either agent, moves each package from one hop to the next, decides
whether the next hop may start, and records what it did.

Lena will merge the change only if the loop ends as "corrected and accepted". So the
decision that matters is the reviewer's verdict at hop 4, and the question an auditor
asks afterwards is narrow: was that ACCEPT given by the reviewer, at hop 4, in this
session, for the result the worker produced at hop 3?

The ways this goes wrong are all valid-looking records in the wrong place: B's ACCEPT
from another session, or from hop 2, presented at hop 4; a hop-4 verdict that names
the hop-1 result instead of the corrected one; a review package whose worker output
was changed after it was collected; a record issued for one invocation and admitted
for another; an attempt past the cap or a hop the plan does not name, started because
a verdict seemed to invite it. Each is an individually well-formed record in a composed path, which is the case
4.1.7 describes. A controlled offline demonstration of this loop exists (a producer-run
test set of positive cells and refusal cells with mutation checks and stand-ins for
the model turns; producer-run only, not independently reproduced, no deployment). It
informs the threat list below; the tier argument does not rest on it, and it is not
evidence that any system meets Tier 3.

## Claimed tier: Tier 3

The claim Lena and an auditor rely on is "the change that was merged is the change the
reviewer accepted at the last hop of this session". Anyone holding the records must be
able to verify, without trusting the operator or either agent, that each review record
names the digest of the result it judged, the hop it belongs to and the session or
invocation it was issued for, and that each of those equals what the receiver expected
at that point. That is Tier 3: the records are verifiable and their binding to the
context is verifiable, with the receiver's honesty disclosed rather than removed.

This is the tier the scenario argues the deployment needs. Whether a particular
implementation meets the Tier 3 requirements, in particular how much a verifier still
has to trust the producer of the records, has to be assessed separately against the
standard. This submission makes no such assessment for any system, including the
demonstration mentioned above.

## Why not one tier down?

At Tier 2 a third party vouches that the review process exists and was followed. That
cannot distinguish an ACCEPT given for the corrected result from an ACCEPT given in an
earlier hop or another session for a different result: both are genuine reviewer
outputs, and the attestation is about the process, not about which result a verdict
was bound to. The failure the use case cannot tolerate is a correct-looking "corrected
and accepted" outcome built from a verdict about something else. Once the change is
merged and released, that is detected late, and possibly only after users depend on it.

Tier 4 would add that a hop cannot launch at all without producing its evidence, so a
missing hop-4 record would mean hop 4 did not run. Lena does not need that guarantee to
decide whether to merge, because she merges only on a present, verifiable ACCEPT, but
see the notes.

## Tier by domain

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Each hop's output and each review must be attributable to the agent and hop that produced it, verifiably. |
| Privacy | not claimed | The task carries no personal data. |
| Portability | not claimed | Both agents run under one receiver; nothing moves between providers. |
| Authorization | 3 | Admission of each hop must be verifiable against the mandate's plan, caps and the expected context, including that a review verdict cannot extend the plan. |
| Identity | 3 | Worker and reviewer roles must be bound to signed identities so that the worker cannot present at a reviewer hop. |
| Security | 2 | Integrity of the packages moved between hops is needed; a stronger isolation claim is not what the merge decision turns on. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `context-blind-authorization` | A genuine review record from another session, another hop or another invocation is presented where a different one is expected, and every verification that ignores the context passes. |
| `insecure-inter-agent-comms` | The package from worker to reviewer, or the verdict from reviewer back, is altered or swapped between collection and use: changed output, a review of the wrong result, a link naming the wrong source hop. |
| `excessive-agency` | A verdict is taken as permission to go further than the mandate: a fifth hop, a further correction round, or the worker acting in the reviewer role. |
| `unbounded-consumption` | Attempts or handoffs continue past the mandate's caps because each individual step looks allowed. |

## What Proof-of-Control does not verify here

- Whether the reviewer's verdict is right. A verifiable ACCEPT bound to the right result
  at the right hop says the review happened as recorded; it does not say the code is
  correct. A relying party should read content correctness as not assessed.
- Whether the mandate's plan, caps and acceptance criteria were adequate for the task.
- Whether the merged change behaves correctly in production.
- For `context-blind-authorization`: whether the authorization policy itself was right.
- For `unbounded-consumption`: availability defense; a cap set in the mandate can gate,
  but choosing the cap is outside the claim.
- That the two agents are distinct in any sense beyond their signed identities, for
  example that they do not share a model, a prompt or an operator.

## Residual trust assumptions to disclose

- The receiver: it holds the expected context for each hop (session, hop, invocation,
  expected result digest) and is trusted to state it truthfully; a receiver that lies
  about the expected context defeats the binding.
- The signing root of the mandate and of the agents' identities, and its revocation
  path.
- The clock used for expiry, and that receiver and verifier read it in the same domain.
- That the result digest named in a review covers every file the reviewer saw; a
  digest over a manifest is only as complete as the manifest.

## Notes / open questions

- The schema at the time of writing has no claim that names the session, invocation or
  audience a record was issued for, and none that names the result or step a review or
  approval judged. Without one, the binding in this scenario lives outside the evidence
  token, in the receiver's own records. Is a context-binding claim, compared by the
  verifier with the relying party's expected context, in scope for 4.1.7, or for 7.1.4
  (where single use is defined)?
- 4.1.8 says advisory output must not raise authorization state. A reviewer's ACCEPT is
  such an output. A concrete auditor test for this use case: present a review record of
  another step or another result and confirm it is refused, and confirm that no verdict
  value starts a hop the mandate does not name.
- Order of refusal matters: a record for the wrong context should be refused before any
  launch, and the refusal should not consume the record, so that the same record is
  still usable in its own context. Whether the standard should say so is open.
- The loop has several distinct end states (accepted without correction; corrected but
  not re-reviewed; corrected and accepted; failed after correction; not complete). The
  token's verdict values are policy decisions and do not represent an outcome; this
  relates to the question in issue #66.
