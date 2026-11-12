# Gap: the draft can grade a local boolean as open verification

**Status:** proposal. Issue text for C8 and Appendix D issue 6.
**Targets:** C8, C7.1.5, C7.5, issue 6 (binary threshold), C8 open item 2 (human authority and Tier 4).
**Pattern:** outsider recomputation versus operator boolean. **Instance:** ENI6MA PassPlus.

## The problem the draft allows

Tier 3 is trust-minimized. After P01, that does not mean the trusted party has been removed. It means the mechanism's soundness and the parties it depends on are disclosed, and an outsider can check the evidence. Dishonesty that never becomes publicly detectable does not cross the line the binary question is using.

A possession checker that returns `validated: true` on the claimant's device produces a bit. Anyone who trusts the device trusts the bit. Anyone who does not trust the device has nothing to recompute. The bit is an attestation of a local decision. That is Tier 2 when a signature lets an assessor see that this device emitted this bit, and Tier 1 when the operator simply asserts it. It is not Tier 3.

C8 open item 2 asks whether required human authorization belongs in the Tier 4 root-of-trust cell. Putting the human there makes Tier 4 mean "trust this person," which is the structure P01 forced the tier table to stop claiming. The fail-closed halt can be a Tier 4 property of the gateway: the effect does not leave if the capability is absent. The human remains a disclosed party who can be coerced and who can answer a challenge the screen did not bind. Those facts are C10.2 disclosures. They are not a root that makes the boolean open.

Issue 6 asks for formal definitions and for impossibility results. This gap is a small one the review can adopt without waiting for the whole impossibility program. Outsider verification of an operator boolean, with no other inputs, is not open verification. Outsider verification of a transcript against a published commitment, a published challenge, and a published response is a different proposition. The draft should say they are different, or implementers will export the bit.

C7.5 reinforces the limit. The bit does not show that the model was right, that the human understood the downstream effect, or that an external system settled the action.

## The pattern that closes it

Grade the two artifacts separately, in the same conformance claim.

| Artifact | What an outsider does | Level |
| --- | --- | --- |
| Operator boolean, unsigned | Trusts the operator's statement | 1 |
| Operator boolean, signed by the device | Checks the signature, still trusts the device to have run the checker | 2 |
| Transcript: commitment, challenge, response, checker digest | Recomputes acceptance. The boolean is not an input. | 3 |
| Gateway halt when the capability is absent | Observes that the effect does not occur | 4 for the halt only |

A claim that attaches Tier 3 to the first or second row fails. A claim that attaches Tier 4 to the human, rather than to the halt, fails.

## What PassPlus runs

The instance is the second row, and in places the first.

- The clients treat guest JSON `validated: true`, or a zero exit, as the ceremony outcome.
- The checker and the claimant share the device.
- iOS Release `encryptAndSave` does not start a URLSession. The result stays local.
- On the Authority path, consume stores `proof_ok` from the caller. The Authority does not re-run the child. If the field is absent, the value used is true. That default is an operator boolean with a fail-open default. It is a concrete reason the standard should reject "the caller said yes" as a Tier 3 possession record. It is also a limit of that API, stated here so the pattern is not confused with it.

The guest is re-runnable. Re-running it on the same device still trusts the device. Re-running it requires the witness or a commitment the published checker can use. The architecture page shows the on-device witness. It does not show a published outsider verifier.

## What the pattern specifies beyond the clients

Publish the commitment, the challenge, the response, and the checker digest. Publish a verifier. Acceptance ignores `validated`. Until that export exists, PassPlus possession evidence stays at Level 2, and any Proof-of-Control claim for the clients stays no.

The useful fact for issue 6 is that the same product sits on both sides of a definition. The bit is what it ships. The transcript is what the pattern needs for Tier 3. A standard that has only one slot called "the check passed" will put the bit in the transcript's slot.

## Requirement sketch

**8.1.9, Level 1.** Verify that the conformance claim states, for each possession check, which of the four rows above the artifact occupies, and that a sampled artifact matches the row.

**Auditor evidence.** Take one production record. Attempt the outsider recomputation with the published verifier. If the verifier needs the operator boolean or a call back to the operator, the row is not the transcript row. Record the actual row. A claim text that says Tier 3 for that record is a finding.
