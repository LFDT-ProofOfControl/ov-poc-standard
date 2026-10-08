# Proposal: legal-entity agents under an accountable human

*Date:* 2026-10-08 · *Status:* proposal only. No normative file is edited by this proposal.

*Submitted by:* Pamela Norton — TitleChain Foundation (founding team, Proof-of-Control initiative)

*Related:* [Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md) issues 1, 2 and 3;
[use case: a cooperative's selling agent](../use-cases/legal-entity-agent-accountable-human.md);
published as TitleChain Foundation RFC 0002 (draft) with a machine-readable crosswalk of all
127 v0.1 requirements: <https://github.com/TitleChain-Foundation/icsn-standards/pull/82>

*Disclosure of interest:* the submitter has commercial interests in an implementation (M5)
that this proposal could favor, and will follow the working group's recusal practice on any
decision that would directly favor it. No requirement below names or depends on that
implementation.

---

## Finding

5.1.1 asks that every action resolve to "a named principal." For most deployments the principal
is a legal entity, which acts only through a person who holds role authority for it. Recording
the entity alone loses who exercised authority; recording the person alone loses on whose
behalf. When that person leaves, or keys rotate, or the agent changes provider, the evidence
has to keep answering both questions. The [use case](../use-cases/legal-entity-agent-accountable-human.md)
walks through one small business where all three happen.

## Answers to open issues

- **Issue 1 (Identity vs. Authorization).** Agree with the working-group lean, made concrete:
  Identity supplies three authenticated parties (agent, legal entity, accountable human with role
  authority); Authorization evaluates the signed chain between them. LE1 below.
- **Issue 2 (anonymity and pseudonymity).** Pseudonymity as an implementer-selectable option:
  relying parties see a stable pseudonym and evidence of a valid entity delegation; the link back
  to the entity and person stays in a store the principal controls, with disclosure conditions
  declared under C10.2 and each disclosure recorded. LE3 below.
- **Issue 3 (evidence continuity).** The principal can export a verification bundle and verify it
  offline without the original operator, and a provider move writes a signed linking record.
  LE4 below.

## Proposed requirements

Twenty-two requirements in the standard's format and Level scheme. Each names the v0.1
requirements it extends; none changes existing text. All need working-group ratification.

### LE1 Three-party principal binding

*Extends C5.1 and C4.2. Answers Appendix D issue 1: Identity supplies the three
authenticated parties; Authorization evaluates the chain between them.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE1.1** | **Verify that** every execution record carries the agent instance identifier, the legal-entity principal identifier, the accountable human of record's identifier, and a reference to the role authority linking that human to the entity. | 1 | 5.1.1 |
| **LE1.2** | **Verify that** before a grant is issued, the accountable human's role authority for the entity is validated as current for the scope granted, and the validation result is written to the execution record. | 2 | 4.1.1, 5.1.2 |
| **LE1.3** | **Verify that** the delegation chain runs human → entity role → agent, that each hop carries the delegator's signature, and that the agent's scope is the intersection of the human's role authority and the entity's grant. | 2 | 4.2.2, 4.2.3 |
| **LE1.4** | **Verify that** no record names an agent as the originating principal or as the accountable human, and that an agent cannot issue a delegation exceeding the authority it was granted. | 1 | 4.2.3 |
| **LE1.5** | **Verify that** the accountable human or the entity can revoke an agent's authority at any time without the consent of the agent or its provider, that revocation is recorded, and that it applies to every subsequent action. | 2 | 4.1.2 |
| **LE1.6** | **Verify that** when the accountable human's role authority ends, every grant they issued is revoked or reaffirmed by a successor within a declared interval, with records linking the predecessor and successor grants. | 2 | 4.2.2 |

**Auditor evidence:** LE1.1 — sampled records resolve to an agent, an entity, and a person with
role authority. LE1.2 — a grant record preceded by a role-authority validation, and one rejected
grant from an expired role. LE1.3 — walk one chain from agent to person to entity. LE1.4 — search
records for agents in principal fields; attempt an over-scope sub-delegation in test. LE1.5 —
revoke in test and confirm the next action is refused. LE1.6 — end a role in test and confirm
grants are revoked or reaffirmed within the interval.

### LE2 Identity survives key change

*Extends C5.1.2 and C6.3.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE2.1** | **Verify that** rotating or migrating the key of an agent, accountable human, or entity leaves its identifier unchanged, and that a signed record links the predecessor and successor keys. | 2 | 6.3.2 |
| **LE2.2** | **Verify that** possession of a compromised key cannot by itself transfer title or control, change an entity role, or create a delegation, and that recovery requires approval records from the accountable human and the entity. | 2 | 6.3.3 |
| **LE2.3** | **Verify that** verification results distinguish evidence valid at event time, evidence produced under an algorithm since deprecated, and evidence signed by a key compromised after the event, and that deprecated evidence remains verifiable. | 2 | 6.3.4, 6.3.5 |

**Auditor evidence:** LE2.1 — a rotation record and an unchanged identifier across it. LE2.2 —
attempt a title or role change with a stolen test key and confirm refusal. LE2.3 — verify one
record before and after deprecating its algorithm.

### LE3 Pseudonymous, accountable agents

*Answers Appendix D issue 2 as an implementer-selectable option.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE3.1** | **Verify that**, where pseudonymity is selected, relying parties receive a stable pseudonymous subject identifier together with evidence of a valid delegation from a verified entity (for example a zero-knowledge or selective-disclosure presentation), and never the entity's or human's identifiers. | 3 | 4.2.4 |
| **LE3.2** | **Verify that** the link from pseudonym to entity and accountable human is held in the principal-controlled store, that the conditions for disclosing it are listed in the trust-assumption disclosure, and that each disclosure is recorded. | 2 | 10.2.1 |
| **LE3.3** | **Verify that** any reputation or risk score about a pseudonymous subject is computed by a method published under LE5 and is disclosed with the evidence records it rests on. | 2 | 7.5.1 |

**Auditor evidence:** LE3.1 — validate one presentation without learning the entity. LE3.2 — the
disclosure-conditions entry and a recorded test disclosure. LE3.3 — recompute one score from its
cited evidence with the published method.

### LE4 Principal-controlled evidence and exit

*Extends C1.4, C2.4, and C3. Answers Appendix D issue 3.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE4.1** | **Verify that** protected source records remain in the principal-controlled store and that evidence shared with operators or relying parties carries only identifiers, digests, or commitments. | 2 | 1.4.1, 2.1.2, 2.4.1 |
| **LE4.2** | **Verify that** the principal can export a complete verification bundle (evidence, public keys and reference values, verifier version, and computation manifest) and verify it offline without the original operator. | 2 | 3.2.1, 8.1.5 |
| **LE4.3** | **Verify that** moving the agent or its evidence to a new provider writes a signed linking record joining the last record of the old chain to the first record of the new one. | 3 | 3.2.2 |

**Auditor evidence:** LE4.1 — scan shared evidence for protected content. LE4.2 — verify an
exported bundle on an offline machine. LE4.3 — walk one linking record across a migration.

### LE5 Deterministic, published computation

*Extends C7.2, C7.7, and C10.1.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE5.1** | **Verify that** every value an evidence record computes (a fee, split, score, or deadline) is defined in a published, machine-readable computation manifest with formula, units, and rounding, and that each record cites the digest of the manifest and of every parameter file used. | 2 | 7.7.1, 10.1.5 |
| **LE5.2** | **Verify that** a time-triggered event is timestamped at the deadline it fires on rather than when it was processed, so that replaying the same history produces byte-identical records. | 2 | 7.2.1 |
| **LE5.3** | **Verify that** the canonical serialization admits only number forms that every supported language represents identically and rejects all others. | 2 | 7.7.2, 7.7.4 |
| **LE5.4** | **Verify that** each manifest computation has at least two separate implementations held to one set of published vectors, including negative vectors. | 3 | 7.7.4 |

**Auditor evidence:** LE5.1 — recompute one record's values from the cited manifest and confirm
the digests. LE5.2 — process the same history at two different times and compare records.
LE5.3 — submit an out-of-range integer and a non-finite number and confirm rejection. LE5.4 —
run both implementations against the vectors.

### LE6 Consequential actions

*Extends C4.1.6 and C7.3.*

| # | Description | Level | Extends |
| :---: | --- | :---: | --- |
| **LE6.1** | **Verify that** actions changing title or control state, entity roles, or delegations, or moving value above a declared threshold, require an approval record from the accountable human, and that an agent's approval is never accepted in its place. | 2 | 4.1.6 |
| **LE6.2** | **Verify that** value-moving actions settle through a reversible hold with published release, refund, and dispute rules; that a refund reverses the hold rather than recovering funds from payees; and that the hold's event log is hash-chained. | 2 | 7.3.1 |
| **LE6.3** | **Verify that** every automated response (a policy denial, a deadline refund, a release) records the rule that produced it and the party entitled to trigger it. | 1 | 4.1.2 |

**Auditor evidence:** LE6.1 — attempt a role change approved only by an agent and confirm
refusal. LE6.2 — refund a held transaction in test and confirm no payee was debited. LE6.3 —
sampled automated events name their rule and trigger.

## Not proposed

- No change to the four Tiers, the conformance stages, or the evidence schema.
- No new mechanism is made normative; examples (zero-knowledge or selective-disclosure
  presentations, linking records) are illustrative.
- LE5 (computation manifest) and LE6.2 (reversible settlement hold) may fit better as an
  informative profile than as core requirements; the working group may prefer that placement.
