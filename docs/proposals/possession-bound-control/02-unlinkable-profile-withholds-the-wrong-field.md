# Gap: the unlinkable profile withholds the principal, and this pattern withholds the witness

**Status:** proposal. Issue text for the Identity group, beside P05 and Appendix D issue 2.
**Targets:** C5, `docs/proposals/P05-unlinkable-identity.md`, Appendix D issue 2.
**Pattern:** possession-bound profile. **Instance:** ENI6MA PassPlus.

## The problem the draft allows

Issue 2 asks whether verifiable-but-unlinkable identity is an implementer-selectable option. P05 is right about the defect it found: C5.1.1 and the evidence schema require `agent_id` and `initiating_user`, so a design that must not carry a persistent principal cannot meet Level 1, and making those fields optional hides a pipeline failure inside a privacy feature.

P05's remedy suspends C5.1.1 and substitutes a session pseudonym. That is coherent for the examples in issue 4 where the relying party must not learn a stable principal: price negotiation, whistleblowing, shielded research sharing.

It is the wrong remedy for a different design that issue 2 currently has no bucket for. In that design the relying party must learn which enrolled principal acted, and must not learn the witness. Suspend the principal and accountability of the enrolled human disappears. Keep C5.1.1 as "put the credential material in the record" and the witness leaks into the log. The draft, plus P05, offers those two buckets only.

## The pattern that closes it

Add a third profile token, `possession-bound`, inside the signed record.

| Profile | Principal reference | Witness in the record |
| --- | --- | --- |
| `identified` | required | credential identifiers as C5.1 writes them today |
| `unlinkable` | suspended, per P05, with P05's substitute requirements | not the point of that profile |
| `possession-bound` | required | forbidden |

An unknown token is rejected. A missing profile means `identified`, so current vectors keep their meaning. A `possession-bound` record that omits the principal reference fails. A `possession-bound` record that contains the witness fails. Suspension is never inferred from a missing field.

P05's profile machinery is the right machinery: the token is signed, the conformance statement maps each action class to one profile, and the claim register lists substitutions. This gap adds a column. It does not weaken P05's refusal to make `agent_id` optional.

## What PassPlus runs

The instance sits in the third column.

- The principal reference is the handle and the device enrollment, not a secret string.
- The witness stays on the device until seal.
- The Authority does not store plaintext Encoding A or `secret_units`.
- Public grade rows store a SHA-256, not module bytes.
- The checker result is a boolean plus, where the response witness is produced, bearings and a proof hash. Bearings are the response. They are not the witness. A profile definition has to say that, or an assessor will delete the response and keep a boolean that nobody can recompute, or will keep the secret configuration and call it the response.

## What PassPlus does not run

PassPlus does not implement P05 unlinkability, and this gap does not ask it to. The handle is a stable local principal. Parties that later receive a possession record learn that reference. Parties that receive only a sealed `.e6` learn the ciphertext and the hashes. The profile says which of those artifacts is the evidence record. The product today produces both, for different recipients. The evidence record for Proof-of-Control is the possession record, not the seal.

## Requirement sketch

**5.0.1, Level 1.** Verify that every evidence record declares `identified`, `unlinkable`, or `possession-bound` inside the signed bytes, and that an unknown token is rejected.

**5.0.4, Level 1.** Verify that a `possession-bound` record includes a principal reference and excludes the witness, and that sample records which drop the reference or include the witness fail validation.

**Auditor evidence.** Three fixtures: identified, possession-bound, unknown token. The possession-bound fixture's body contains no witness field. Alter the profile token under a valid signature and confirm the signature check fails.
