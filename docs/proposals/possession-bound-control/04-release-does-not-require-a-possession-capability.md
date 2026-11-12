# Gap: the gateway can release an effect that never cited a possession check

**Status:** proposal. Issue text for the Authorization group and for C7.
**Targets:** C7.1.4, C7.1.5, C4.1.3, C4.1.5, C4.2.
**Pattern:** possession capability. **Instance:** ENI6MA PassPlus, possession half only.

## The problem the draft allows

C7.1.4 requires the effect channel to be mediated in the same trust boundary as policy evaluation, by one of three options. Option (b) is a single-use capability bound to the evaluated snapshot digest and the target resource. C7.1.5 says a system that evidences evaluation and does not mediate the effect may claim Tier 1 or Tier 2 only. C4.1.3 requires out-of-scope actions to be blocked at the gateway, not flagged. C4.1.5 requires per-task credentials and forbids a standing broad credential at runtime.

A system can meet all four with capabilities that never cite a human possession check. That is correct for action classes with no human in the loop. It is a hole wherever the conformance statement says a human must have answered before release. The statement can say it in a policy PDF. C7.1.5's own lesson is that a control asserted outside the execution path produces no evidence either way. The draft does not require the possession citation inside option (b), so the PDF and the capability can disagree and the capability still verifies.

P02 tightens a different gap: the snapshot digest may not determine the endpoint's effect. This gap sits one step earlier. Even a perfect endpoint binding authorizes whatever snapshot was signed. If that snapshot was never the output of a possession check, the endpoint faithfully performs an action nobody holding the witness accepted.

## The pattern that closes it

For an action class mapped to `possession-bound` in the conformance statement:

- The gateway releases the effect only when a capability verifies.
- The capability's signed body includes the possession-record digest and the canonical action digest.
- The nonce in the possession record is unconsumed. Consumption is written before release.
- A second presentation is a rejection record with both digests.
- The witness is not copied into the capability.
- Delegation hops after the first carry the capability. They do not carry the witness. A later hop requires a new human challenge only when that hop's action class says so. Scope intersection (C4.2.3) still applies. A possession check is not a blank delegation.

C7.1.4 does not need a fourth mediation option. Option (b) gains a required input when the profile says so.

## What PassPlus runs

The fail-closed half of the check, on the device:

- No local session unless `validated` is true.
- A nonce already stored and consumed is not a successful consume on the Authority path: consume requires a nonce from reserve, inside `expires_at`, not yet consumed.
- The 900-second local session observed in one iOS test is a standing grant for that window. C4.1.5 would record it as a residual standing credential, not as proof that no standing credential exists. The pattern's capability is single-use. The session is a different artifact. The contribution names both so an assessor does not accept the session as the capability.

## What PassPlus does not run

There is no Action Interception Gateway in the PassPlus clients. A ceremony acceptance does not refuse a payment, a file write, or an agent message. Web, extension, and iOS do not call reserve or consume. The pattern fixes the draft by making the citation mandatory. PassPlus is the existence proof of the check the citation would point at. It is not an existence proof of the halt.

Where `handle-app` does call consume, the body is `{nonce, proof_ok}` and the Authority does not re-run the guest. That call is not the capability in this gap. A bit from the caller is the operator boolean, treated in gap 05.

## Requirement sketch

**7.1.6, Level 3.** Verify that, for each action class the conformance statement maps to `possession-bound`, the gateway's release path verifies a single-use capability citing that class's possession record and the canonical action digest, and that a test release without the capability does not reach the tool.

**Auditor evidence.** The substitution test already written for C7.1.4: snapshot A presented, action B dispatched, B refused. Plus a third arm: snapshot A with a bearer token and no possession-record digest, refused. Confirm the tool was not invoked in either arm. A system with no such action class marks this requirement not applicable and cannot claim human possession for any release.
