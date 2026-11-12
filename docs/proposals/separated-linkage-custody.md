# Proposal: separated linkage custody for unlinkable identity binding

*Date:* 2026-11-12 · *Status:* proposal only. No normative file is edited by this proposal.

*Submitted by:* Mitchell Travers, agentprivacy. Interest: research on privacy architecture for
agents acting on behalf of people. No conformance claim; no product named.

*Related:* [`P05-unlinkable-identity.md`](P05-unlinkable-identity.md) · issue #107 ·
[Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md) issue 2 · the C5.2
`[WG-INPUT NEEDED]` note. Also filed as a public comment in the Google Doc, on "Anonymity and
pseudonymity" in Section 4.

---

## Finding

P05 gives the Unlinkable profile a mechanism (C5.0), a schema discriminator, and measurement
requirements. It places accountability in C5.3, threshold escrow, which its own §15 marks
`[MODELLED — NOT IMPLEMENTABLE TODAY]`. Issue #107 places the link from pseudonym to principal in
"a store the principal controls", with the disclosure conditions declared under C10.2.

That leaves the profile without an accountability route that can be built and assessed today.
#107's placement is the right one, but "the principal controls the store" is an assertion unless
the standard says what must be kept apart from what, and how an assessor tests it.

The answer proposed here is separation on the principal's side:

* a **holder** keeps the principal's identity and the links from pseudonym to principal, and
  decides what each action may use;
* an **acting agent** executes toward relying parties, carrying only a pseudonym, a delegation
  proof, and the inputs the holder released for that action.

The relying party and the operator never receive the link. The acting agent never holds it.
Accountability is the holder's signed, session-scoped disclosure under declared conditions: the
same accountability a named principal is under today, made explicit, and buildable with
per-session keys and ordinary signatures.

## Proposed text: new C5.4 Separated Linkage Custody (Unlinkable profile)

Numbering is provisional. C5.3 and 5.1.5 to 5.1.8 are taken by P05, and 5.1.6 is also proposed
in #165.

> ## C5.4 Separated Linkage Custody
>
> Under the Unlinkable profile, the link from pseudonym to principal exists, is held on the
> principal's side, and is kept out of reach of the component that acts.
>
> | # | Description | Level |
> | :--------: | --- | :---: |
> | **5.4.1** | **Verify that** the component holding the principal's identity and the pseudonym-to-principal links (the holder) is separate from the component that executes actions toward relying parties (the acting agent), and that the acting agent's execution environment cannot read the link store. | 2 |
> | **5.4.2** | **Verify that** the acting agent receives only inputs the holder released for the action, and that each release is recorded on the holder side with the session and delegation token it served. | 2 |
> | **5.4.3** | **Verify that** each delegation token is issued under its own pseudonym, so that the pseudonyms of two sessions by the same principal are not linkable from the evidence alone. | 2 |
> | **5.4.4** | **Verify that** disclosure of a link is scope-bound: the holder can issue a signed statement binding the pseudonym of a named session to the principal, and that statement yields nothing that links any other session. Each disclosure is recorded to an append-only log, as in P05's proposed 5.3.4. | 3 |
> | **5.4.5** | **Verify that** the conditions under which the holder will disclose, and the party able to compel it, are stated in the C10.2 trust-assumption disclosure. | 1 |
> | **5.4.6** | **Verify that** the claim lists every channel a relying party or operator observes under the Unlinkable profile, states the leakage assessed for each, and assesses linkability over the channels jointly, or justifies the independence that a per-channel assessment assumes. | 3 |
> | **5.4.7** | **Verify that** the linkability assessment names the adversary class it was made against (the background information assumed available to a relying party or operator) and is repeated on a defined schedule, so that a claim made under the Unlinkable profile carries the date of the assessment it rests on. | 3 |
>
> **Auditor evidence:** 5.4.1 — custody configuration; from the acting environment in test,
> attempt to read the link store (should fail) and record the attempt. 5.4.2 — sample an action;
> match its inputs to a holder release record. 5.4.3 — compare pseudonyms across two sampled
> sessions by one test principal; confirm no shared identifier or key. 5.4.4 — request one
> disclosure in test; verify the signature; confirm the other session's pseudonym is not
> derivable from it; find the log entry. 5.4.5 — read the disclosure. 5.4.6 — the channel list
> and the joint assessment, or the stated independence argument. 5.4.7 — the named adversary
> class, the assessment date, and the schedule; confirm the latest assessment falls within it.

**The trust assumption, stated plainly.** C5.4 trusts the holder to honour a valid disclosure
demand. It does not by itself reach Tier 3. It removes the operator and the relying party from
the set of parties trusted with *who the principal is*, and replaces an assertion ("we do not
look") with a separation an assessor can test. Where threshold escrow (P05 C5.3) becomes
implementable, it can sit on top of C5.4 for Tier 3 accountability; C5.4 does not depend on it.

## Why 5.4.6 and 5.4.7

P05 measures the anonymity set (change 6) and the composed-path cost (change 7). Two further
points bear on how a relying party's view is assessed.

**Channels combine.** A relying party sees several channels at once: the pseudonym, timing,
action content, network metadata, and the delegation proof. Bounding each channel separately and
summing gives a valid upper bound only when the channels are conditionally independent given the
principal and no single observer combines them. Timing and content are routinely correlated, and
correlated channels can reveal more together than their sum. The separation in 5.4.1 and 5.4.2 is
what makes independence plausible to begin with: an acting agent that never sees the principal's
identity cannot leak it into content or timing.

**The assessment ages.** Leakage is assessed against an adversary's background information
(linkage corpora, side information), and that background grows after the evidence is emitted.
The records do not change; what can be inferred from them does. An unlinkability assessment is
therefore a statement about a named adversary class at a point in time, not a permanent property
of the records, and a claim should carry its date.

## Answers to P05 §14 open questions 1, 2 and 6

* **Q1, a third pseudonymous-but-linkable profile.** Yes. A stable pseudonym per relying party
  (pairwise identifiers, for example `did:peer`) is deployable today and covers most of the
  motivating cases in Appendix D issue 4. 5.4.1, 5.4.2, 5.4.5, 5.4.6 and 5.4.7 apply to it
  unchanged; 5.4.3 does not.
* **Q2, what a session is.** One delegation token. That aligns the pseudonym (5.4.3), the
  disclosure scope (5.4.4), the opening warrant in P05's 5.3.3, and the expiry already required
  by C5.1.3, so one boundary serves all four.
* **Q6, C5.2.2 under the profile.** Suspend it until anonymous group attestation is
  implementable, as P05 §15 itself suggests. Under C5.4 the receiving party can still validate
  message integrity against the session pseudonym's key, so C5.2.1 holds; what it cannot do is
  validate the sender's organisation, and the claim should say so under C10.2.

## Open questions for the working group

| # | Question | Where it bites |
| :--: | --- | --- |
| 1 | `[WG-INPUT NEEDED]` Does C5.4 stand as its own section, or fold into P05's C5.0 as the accountability route for the Unlinkable profile alongside C5.3? | placement |
| 2 | `[WG-INPUT NEEDED]` Should the holder and the acting agent be required to run under different operators, or only in separated environments under one operator? The first is stronger and harder to deploy. | 5.4.1 |
| 3 | `[WG-INPUT NEEDED]` What schedule for 5.4.7: fixed (for example yearly), or tied to the Continuously Monitored stage? | 5.4.7, Appendix D issue 8 |

## What this proposal does not do

It does not change the Tier rules, propose an escrow scheme, or require a particular credential
format. It does not claim C5.4 reaches Tier 3. It proposes requirements an assessor can close out
against an artifact today.
