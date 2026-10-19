# Crosswalk: IETF SCITT (RFC 9943) and RATS (RFC 9334)

| | |
| --- | --- |
| **Framework type** | IETF architectures: transparent digital supply chains (SCITT) and remote attestation (RATS) |
| **Corpus version** | RFC 9943, June 2026, Proposed Standard, with COSE Receipts in RFC 9942 · [access](https://www.rfc-editor.org/rfc/rfc9943) · RFC 9334, January 2023, Informational · [access](https://www.rfc-editor.org/rfc/rfc9334) · [corpus provenance](corpus/README.md) |
| **Relationship** | Interchange layer. SCITT and RATS define how an attested or registered statement travels between parties; Proof-of-Control defines what the evidence must establish about an agent's actions |
| **Coding status** | **[WG-INPUT NEEDED]** · qualitative only. No row-level coding; see [What is deliberately absent](#what-is-deliberately-absent) |

## The Relationship

Every framework currently coded in this directory is a control catalogue, a risk framework or a
regulation: each says what control an operator should have. SCITT and RATS sit at a different
layer. They say nothing about what a control boundary is, or what an agent action record should
contain. They define the roles and the wire formats by which a statement about an artifact
moves from the party that made it to a party that was not present when it was made.

That is the layer at which several C7 requirements are satisfied rather than merely described.
A Proof-of-Control implementer who has read RFC 9943 is holding the receipt format that C7.3.4
asks for. One who has read RFC 9334 is holding the vocabulary that separates the party that
appraises evidence from the party that acts on it, which is the separation the Tiers grade.

Neither is a route to a Proof-of-Control claim. Registering a statement with a Transparency
Service establishes that the statement was registered. It leaves open what the statement said,
whether it was generated at the action boundary, and whether the operator could have written it
by hand.

## Where SCITT reaches C7

| Requirement | SCITT construct | What it supplies, and what remains |
| --- | --- | --- |
| [C7.3.4](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) inclusion proof against an append-only tree | Receipt (RFC 9942) over the Transparency Service's Verifiable Data Structure | Supplies the proof form the requirement describes, obtainable by a verifier without the rest of the log. The content registered stays a Proof-of-Control obligation |
| C7.3.5 append-only consistency against previously published roots | The **Auditor** role, defined in RFC 9943 as a Relying Party that verifies the consistency and correctness of the append-only log | Names the role and the duty. The requirement's own discipline, comparing a recomputed root against the anchored value rather than a record count, stays with the implementer |
| C7.3.3 equivocation resistance | A Transparency Service holds an identity backed by a public key and publishes its trust anchors; Auditors and second Relying Parties can obtain the same roots | Gives the cross-verification the requirement offers as one option. RFC 9943 stops short of requiring a witness quorum |
| C7.6.6 external anchoring within a declared interval | Registration and receipt issuance | Fixes a point in a verifiable structure. The declared maximum interval, and the alert on a missed deadline, remain Proof-of-Control obligations |
| C7.7.1 to C7.7.3 schema, canonical serialization, explicit algorithm identifier | COSE_Sign1 envelopes and CBOR encoding | Carry explicit algorithm identifiers and a deterministic encoding, which is most of what C7.7.3 tests. The evidence claim set itself stays a Proof-of-Control schema |
| C7.4.1 trust-assumption disclosure | RFC 9943 requires a Transparency Service to publish its registration policies and trust anchors so they can be audited | A disclosure of the same shape, at the service level rather than the claim level |

## Where RATS reaches C1 and C8

RFC 9334 separates 7 roles. Three of them bear directly on this standard.

| Requirement area | RATS construct | Relationship |
| --- | --- | --- |
| [C1.1](../0.1/en/0x10-C01-Provenance.md) model and artifact provenance, C1.3 compute substrate provenance | Evidence from an Attester, Endorsements from an Endorser, Reference Values from a Reference Value Provider, appraised into Attestation Results | RATS supplies the vocabulary and the role separation for exactly the claims C1.3 makes about the substrate. It leaves the agent-specific content to this standard |
| [C8](../0.1/en/0x10-C08-Verifiability-Tiers.md) the Tiers, and the binary threshold | The split between **Verifier** and **Relying Party** | A Relying Party that acts on an Attestation Result is trusting the Verifier that produced it, which is the Tier 2 position stated in RATS terms. A Relying Party that verifies a receipt itself against a published root has no appraiser to trust, which is where Tier 3 begins. The 2 architectures name the same boundary from opposite sides, and neither grades it |

RATS has a widely implemented, 3 year old vocabulary for the distinction C8 was written to
grade. Adopting its terms where they fit would let a reader who knows RATS place the Tiers
without learning a second vocabulary.

## Proposed entry for the by-domain mapping

The Provenance row of the by-domain table in [README.md](README.md) is marked *working group to
complete*. RATS is the natural external alignment target for it, with SCITT as the transport for
the resulting statements.

## What is deliberately absent

**No row-level coding.** This crosswalk does not add a column to
[`coding_sheet.csv`](coding_sheet.csv), for 2 reasons the working group may wish to weigh before
one is added.

1. The coding sheet already carries 8 single-coder columns, and the
   [2026 review](../docs/reviews/mapping-review-2026-08.md) recorded 192 proposed changes and 96
   unauditable citations against them. A ninth single-coder column adds volume to a known
   weakness rather than reducing it.
2. The [rubric](rubric.md) is written for clause-to-requirement comparison. SCITT and RATS are
   architectures, and an architecture that defines a role rather than mandating a control codes
   awkwardly as Exact, Partial or None. Applying the rubric to them may need a note in the rubric
   first.

The recommendation is that the working group decide whether these 2 documents belong in the
quantitative sheet at all, and settle the rubric question, before 254 rows are coded.

## Contributor disclosure

Contributed by Certisyn, Inc., which has posted individual Internet-Drafts in this area,
including `draft-hillier-scitt-arp`. Every claim above rests on the published RFC text.
