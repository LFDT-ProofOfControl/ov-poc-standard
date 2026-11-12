# Contribution pack: possession-bound control

**Status:** proposed collateral. Nothing in `0.1/en/` is changed by these files.
**Pattern source:** ENI6MA PassPlus, the on-device ceremony and sealed enrollment described in the PassPlus architecture note of 2026-10-02.
**What this pack is not:** a request to adopt ENI6MA software, keys, guest binaries, or a product name as part of the standard. The standard stays technology-neutral. These documents name holes in the current requirements, name the pattern that closes each hole, and then show how PassPlus already runs that pattern so the working group can see the pattern is implementable.

The document to contribute is [WHITE-PAPER-FULL.md](WHITE-PAPER-FULL.md), by Frank Dylan Rosario, Dr. Lin Wang, and Dr. Octavia Sulea. It stands alone. It cites the Proof-of-Control requirement files, names the chain of holes, and separates external attack surfaces from agent attack surfaces. It does not cite other manuscripts. [WHITE-PAPER.md](WHITE-PAPER.md) is the short cover note.

## Read in this order

| Document | Hole it files | Draft targets |
| --- | --- | --- |
| [WHITE-PAPER-FULL.md](WHITE-PAPER-FULL.md) | Full paper: identity checks a copied credential and the agent itself can pass, with requirement citations and bibliography | C5, C4, C2, C6, C7, C8, Appendices B and D |
| [WHITE-PAPER.md](WHITE-PAPER.md) | Short cover note of the same hole | C5, C4, C7, C8, Appendix B |
| [WHITE-PAPER-ONESHOT-OSCILLATION.md](WHITE-PAPER-ONESHOT-OSCILLATION.md) | The durable token is the architecture's fatal error. Each gap names that token. The repair is a per-act proof: one-shot on each interactive step, oscillation as the same proof between two service processes. | C4, C5, C7, C8 |
| [WHITE-PAPER-STACK-OBSOLETE.md](WHITE-PAPER-STACK-OBSOLETE.md) | When an agent runs on that per-act proof, the Standard's token stack (C5 through C10 and Appendix B) grades an object the burn has already finished with. | C1–C10, Appendix B |
| [WHITE-PAPER-ACADEMIC-REVIEW.md](WHITE-PAPER-ACADEMIC-REVIEW.md) | The draft is broken at issuance. Later controls rename the same reusable secret. Expiry, scope, gateway, attestation, and tier are patches on presentation. | C4, C5, C7, C8 |
| [WHITE-PAPER-ACADEMIC-REVIEW-PLAIN.md](WHITE-PAPER-ACADEMIC-REVIEW-PLAIN.md) | Same review. Each example is definition, context, record, and result. Figurative sentence forms are replaced with the fields and operations they were naming. | C4, C5, C7, C8 |
| [WHITE-PAPER-STANDARD-FAULTS.md](WHITE-PAPER-STANDARD-FAULTS.md) | Standalone fault record of the draft. Swim lanes, numbered walk-throughs, `<! ERROR En !>` tags, attack paragraphs, glossary, and a map from draft sections to error numbers. No external system is cited. | C2, C4, C5, C7, C8, Appendix B, THREATS.md |
| [DEFINITIONS.md](DEFINITIONS.md) | Appendix A has no terms for the pattern, and issue 7 uses "ceremony" for a setup ceremony. | Appendix A, issue 7 |
| [01-bearer-credential-does-not-show-possession.md](01-bearer-credential-does-not-show-possession.md) | C5.1.2 and C5.1.3 are satisfied by a stolen bearer token. | C5.1 |
| [02-unlinkable-profile-withholds-the-wrong-field.md](02-unlinkable-profile-withholds-the-wrong-field.md) | P05 suspends the principal. The hole is the witness, not the principal. | C5, issue 2, P05 |
| [03-approval-is-not-bound-to-the-presented-challenge.md](03-approval-is-not-bound-to-the-presented-challenge.md) | C4.1.6 records a decision. It does not bind that decision to the bytes the human answered. | C4.1.6, `approval-fatigue`, `prompt-injection` |
| [04-release-does-not-require-a-possession-capability.md](04-release-does-not-require-a-possession-capability.md) | C7.1.4 binds a snapshot. Nothing requires that snapshot to cite a fresh human possession check. | C7.1.4, C7.1.5, C4.1.3, C4.1.5 |
| [05-operator-boolean-is-not-open-verification.md](05-operator-boolean-is-not-open-verification.md) | A local `validated: true` is graded as if an outsider had checked it. | C8, issue 6, C7.5 |
| [06-signing-key-rules-do-not-fit-a-witness.md](06-signing-key-rules-do-not-fit-a-witness.md) | C6.3's HSM rules, applied to a human witness, either reject the pattern or launder it into a signing key. | C6.3, C6.3.5, C2.4.1 |
| [07-inventory-has-no-possession-row.md](07-inventory-has-no-possession-row.md) | Appendix B will file this pattern as a ZKP or a TEE report. It is neither. | Appendix B |

Use case, in the corpus the validator already checks:

- [`../../use-cases/submissions/possession-before-irreversible-effect.md`](../../use-cases/submissions/possession-before-irreversible-effect.md)

## Collateral the draft does not yet have

Each row is a deliverable this pack asks the working group to add. PassPlus is the instance that shows the row is fillable. The instance is not the requirement.

| Missing collateral | Why the draft fails without it | PassPlus instance |
| --- | --- | --- |
| Glossary entries in [DEFINITIONS.md](DEFINITIONS.md) | Issue 7's word "ceremony" collides with a possession protocol. Assessors will mix a trusted setup with a human challenge. | The product calls the interaction a ceremony. The contribution renames the pattern so the draft's word stays put. |
| Identity profile token `possession-bound` | C5.1.1 plus P05 offer only "name the principal" or "suspend the principal." | Handle and device enrollment stay. The secret configuration is sealed, not copied into the evidence record. |
| Signed fields: challenge digest, response digest, checker digest, nonce id | Two implementations can both "do a challenge" and hash different bytes. C7.7 already says that breaks binding. | Web challenge argv carries `tau` and `nonce`. Validate consumes bearings. iOS calls `challengeV2` then `validate`. |
| Negative schema vectors | No vector rejects a record that contains the witness, a reused nonce, or a response digest outside the signature. | The response witness `eni6ma.proof.v1` omits the secret, the permutation, the offsets, epsilon, and pi. |
| Auditor note on C4.1.6 | An approver id plus a boolean can be stored against content the approver was not shown. | Bearings are the response to the planes the challenge presented. |
| C7.1.4 binding rule | The capability can bind a tool snapshot and still be issued with no possession check. | Not wired. The clients do not sit in front of an agent tool gateway. The pattern says the capability must cite the possession record. |
| Disclosure categories | Issue 7's list has Hardware, Mathematical, Ceremony, Vendor, Implementation, Distributed. A human-held witness and a pinned wasm checker have no cell. | The checker is a pinned `wasm32-wasip1` guest. The witness is held on the device until E6PS seal. |
| Appendix B row | See gap 07. | Device-local checker: emerging. Outsider recomputation of the transcript: not what the shipping clients export. |
| Use case for `prompt-injection` | Coverage index: that slug has no story. The injection is out of scope. The release it tries to cause is in scope. | The use case is the story. The clients demonstrate the check, not the payment halt. |
| Separated quantum disclosures | A hybrid seal margin will be offered as if it satisfied C6.3.5. | E6PS v2 is X25519 plus ML-KEM-768 for enrollment confidentiality. That is not an evidence-signature scheme. |

## How to file

One issue per gap file. The white paper is the cover note, linked from each issue. The use case is its own pull request: copy is already in `docs/use-cases/submissions/`, and `python3 tools/validate_use_cases.py` should be run on that file before the pull request. Do not open a pull request that edits `0.1/en/` until the Identity and Authorization groups pick the profile token.

Normative text, if the groups adopt it, uses the requirement sketches inside each gap file. Those sketches name artifacts. They do not name a vendor.

## License boundary

Discussion text and pattern definitions are what this pack contributes. Parameter-level construction of the witness alphabet stays out of the repository until the contributor decides, on purpose, how that construction sits under the Apache 2.0 patent grant. The holes can be stated without those parameters.
