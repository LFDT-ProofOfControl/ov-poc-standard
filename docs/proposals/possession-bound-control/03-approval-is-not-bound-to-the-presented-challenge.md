# Gap: C4.1.6 records an approval that may not be the challenge the human answered

**Status:** proposal. Issue text for the Authorization group.
**Targets:** C4.1.6. Threat slugs `approval-fatigue`, `prompt-injection`.
**Pattern:** challenge-bound approval. **Instance:** ENI6MA PassPlus.

## The problem the draft allows

C4.1.6 asks for the approver's authenticated identity, the exact content presented, the decision, and a timestamp. An implementation stores those four fields and passes. Nothing checks that the content presented and the action later released are the same bytes, or the same digest, or even the same kind of object.

Two failures follow.

The interface shows a payment of 20 and the stored "content" is a payment of 20,000. The approver id is real. The timestamp is real. The decision is yes. The field named content does not match the screen. The auditor note says to confirm that the presented content matches what was executed. The requirement text does not say how those two representations are compared, so a deployment compares a sentence to a sentence by eye and ships.

A prompt injection changes the tool call after the human has approved a different call, or instead of the human. The threat vocabulary says Proof-of-Control gates and records the out-of-bounds action and does not detect the injection. That gate has no purchase if the approval record is not bound to the action digest. The injection stays in scope as an unblocked effect. The draft calls the approval present.

`approval-fatigue` has the same shape. The standard cannot remove fatigue. It can require that the bytes the human answered are the bytes the capability authorizes. Without that, fatigue and substitution look identical in the log: a yes, a name, a time.

## The pattern that closes it

The human answers a challenge. The challenge has a digest. The response has a digest. The capability that releases an effect cites both, and cites the canonical digest of the effect. Level 3 for that effect requires one of these:

- the challenge digest equals the action digest, or
- a published function maps the bytes the human was shown to the action digest, and the auditor recomputes it.

If the screen shows a sentence and the capability covers tool-call bytes, and no published function relates them, the record is a displayed-content note under C4.1.6 and is not authorization for the tool call. This is P02's representation injectivity applied to the approval surface. P02 measured it on commercial APIs. The same split exists between a sentence and a canonical tool invocation.

The pattern does not claim the human understood the sentence. It claims the response the checker accepted was a response to a named challenge, and that the release cited that challenge.

## What PassPlus runs

The clients bind the response to the challenge the guest issued.

- The challenge output carries planes (`eni6ma.challenge.v2` on the web path).
- Validate submits those planes' challenge together with the bearings.
- The guest accepts or rejects the pair.
- iOS maps pad input to bearings and does not grant on the practice verifier.

A human who answers a different painting than the one in the challenge fails the guest. That is the pattern, on the ceremony surface.

## What PassPlus does not run

The clients do not compute a digest over a downstream tool invocation, and they do not show a payment sentence whose bytes are the challenge. Screen binding for an agent effect is the requirement. The ceremony shows binding between painted planes and bearings. Extending that binding to a tool call is the gateway work in gap 04. An assessor who treats a successful ceremony as authorization for an unseen tool call is making the mistake this gap exists to forbid.

## Requirement sketch

Amend the C4.1.6 auditor note:

> Where the approval is a possession protocol, collect the challenge digest and the response digest. Confirm both sit inside the signature of the possession record and inside any capability that released the action. If the presented bytes and the action bytes differ, collect the published mapping and recompute it. A missing mapping is a finding against this requirement for any claim that the approval authorized the action.

**4.1.9, Level 2.** Verify that a test which presents challenge A to the human and submits a capability for action B is rejected, and that the rejection record names both digests.

**Auditor evidence.** The A/B test. One production sample where the auditor recomputes the mapping, or confirms the digests are equal.
