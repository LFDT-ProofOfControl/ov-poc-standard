# Definitions the draft does not have

**Status:** proposal for Appendix A and for issue 7. Not normative.
**Pattern source:** ENI6MA PassPlus. The terms below are the pattern. PassPlus is one running instance, named so the working group can see the terms are inhabited. The terms do not require that instance.

Issue 7 uses **ceremony** for a cryptographic setup whose participants are trusted to have generated parameters honestly. PassPlus uses the same word for a person answering a fresh challenge. Those are different roots of trust. This list keeps the draft's word and adds the missing ones.

## Terms

**Possession witness.** The secret configuration a prover uses to answer a challenge. It is an input. It is not an evidence-signing key, not a bearer token, and not an output of the check. In PassPlus the witness is the enrollment secret. It stays on the device until it is sealed. The Authority does not store it in plaintext.

**Possession protocol.** An interaction in which a verifier selects a fresh challenge, a prover returns a response computed from a possession witness, and a checker accepts or rejects. The shipping PassPlus clients run this on device: challenge, then validate, against a `wasm32-wasip1` guest. Web and extension pass `tau` and `nonce` into the challenge. The iOS client calls `challengeV2`, then `validate`, and writes a local session only when `validated` is true.

**Checker.** The component that accepts or rejects a response for a challenge. In PassPlus the checker is the pinned guest. A checker digest is the identity of that component. A pin is a provenance fact. It becomes a hardware attestation only when an attestation report covers that digest and an outsider compares the report to a published value (C6.1.3, C6.1.4).

**Possession record.** The evidence artifact of one run: principal reference, challenge digest, response digest, checker digest, nonce identifier, and the checker's decision. The witness is absent. PassPlus can produce the inputs of this record (challenge, bearings, guest, nonce, boolean). It does not yet serialize them as a Proof-of-Control claim.

**Possession-bound profile.** An identity profile in which the evidence record keeps a principal reference and omits the witness. This is the profile C5 does not have. It is not P05's unlinkable profile. Unlinkable withholds the principal. Possession-bound withholds the witness.

**Challenge-bound approval.** A human approval record in which the signed bytes include the digest of the challenge the human answered and the digest of the response, and those digests are the same digests cited by any later capability. C4.1.6 records the approver, the content presented, the decision, and a timestamp. It does not require the presented content and the authorized action to be the same digest.

**Possession capability.** A single-use authorization artifact under C7.1.4(b) whose signed body includes the possession-record digest and the canonical digest of the evaluated action. The gateway releases the effect only when the capability verifies and the nonce is unconsumed. PassPlus does not issue this capability and does not stand in front of an agent tool gateway. The definition is the hole. The on-device check is the part the clients already run.

**Evidence-signing key.** The key that signs possession records and capabilities. C6.3 applies to it: hardware-backed generation, rotation, compromise procedure, algorithm identifier, and a post-quantum or hybrid signature when retention outlives the classical scheme.

**Enrollment seal.** A confidentiality wrapper for a possession witness moving to a recipient who is allowed to open it. PassPlus uses E6PS v2: X25519 plus ML-KEM-768, BLAKE3, XChaCha20-Poly1305, inside an `.e6`. The seal's quantum margin is a margin on confidentiality of enrollment. It is not C6.3.5's margin on unforgeability of evidence signatures.

**Operator boolean.** A decision bit emitted by a checker the claimant operates. PassPlus clients treat `validated: true` as the ceremony outcome. That bit shows the checker ran on that device. It is open verification only when a party who does not operate the checker recomputes the decision from published artifacts, and the bit is not an input to that recomputation.

**Setup ceremony.** The draft's existing term. Parameter generation for a cryptographic construction, trusted or trustless as C8 specifies. Not a possession protocol.

## Disclosure categories issue 7 does not list

Add these beside Hardware, Mathematical, Ceremony, Vendor, Implementation, and Distributed. Do not overload Ceremony.

| Category | What is disclosed | PassPlus instance |
| --- | --- | --- |
| Human-held witness | A person can produce responses and can be coerced. The protocol does not remove that party. | The human answers the painted challenge. |
| Pinned checker | Verification depends on a named checker digest and on the runtime that executed it. | Pinned wasm guest, WASI profile, on-device execution. |
| Seal recipient | A named party can open the enrollment seal. | Factory recipient key. Plaintext is not what the Authority stores. |

## Words this contribution refuses

**Prove**, except for a cryptographic proof or the name Proof-of-Control. A possession check shows a response matched a challenge under a checker.

**Independent verification** as a tier name. Tier 3's name in this draft is Trust-minimized.

**Ceremony** inside new requirement text, for the human protocol. Use possession protocol. The product's own documentation can keep its word. The standard should not inherit the collision.
