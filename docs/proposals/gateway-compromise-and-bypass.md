# Proposal: the Action Interception Gateway as a threat, compromise and bypass

*Date:* 2026-10-12 · *Status:* proposal only. No normative file is edited by this proposal.

*Submitted by:* Imran Siddique (@imran-siddique), in a personal capacity. I work on cMCP at
OPAQUE, which enforces MCP tool policy inside a TEE, so I build the component this proposal is
about.

*Targets:* Appendix C, C10.2, C10.3.2 (auditor evidence), README

*Origin:* [#78](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/78), logged in the
[public-comment register](../reviews/public-comment-register-2026-10.md) under Appendix D issues 3
and 5. The grading basis for G2 is from @vaverkamatous-rgb's measurements on that issue.

---

## The central finding

C7.1 puts an Action Interception Gateway inside every Proof-of-Control claim. 7.1.1 routes every
tool and effect invocation through it, with "no network or credential path to its tools that
bypasses the gateway". 7.1.3 makes it hold the action "until the *before* record is durably
written". 7.1.4 requires the effect channel to be mediated by one of three named options. All
three are Level 3, and C7's requirements "apply to every claim made in the domain chapters" C1
to C6, so meeting them is part of the minimum for any claim. C7's own control objective calls the component
"the enforcing mechanism".

Appendix C does not name it. A word-boundary search of `0x92-Appendix-C_Threat-Model.md` at
`93d0e28` returns zero matches for gateway, intercept, interception, mediation, bypass, custody
and enforcement. The coverage table has 32 rows and 12 of them use "gate" or "gates" as the verb
for the defence, so a substring search for "gate" reads as coverage when there is none.

The nearest row is "Audit tampering": "A compromised host rewrites the record", graded Full. A
compromised gateway rewrites nothing. It signs true records for the actions it admits and emits
nothing for the ones it hides. Every signature verifies, the chain is intact, and 7.6.2's
per-source sequence numbers stay contiguous, because the gateway is the source and numbers only
what it emits. The failure is omission, and a verifier that reads only the records that arrived
cannot see it.

Two normative passages already depend on the gateway not doing this:

* **"Evidence repudiation", graded Full:** "the operator cannot deny an action occurred". That
  holds for an action the gateway recorded. For an action it hid there is nothing to deny.
* **10.3.2, Level 4:** completeness is "demonstrated by reconciling gateway action counts against
  evidence-record counts". Both counts come from the gateway. A gateway that hides an action
  hides it from both, and the reconciliation shows zero unexplained difference.

CISO review F1 covered gateway failure, which became 7.6.1 and 7.6.3. Compromise and bypass are
not modelled anywhere in the threat model.

## Summary of proposed changes

| # | Where | Kind | Confidence |
| :--: | --- | --- | --- |
| G1 | Appendix C | New row: gateway compromise | Gap settled by reading; grade `[WG-INPUT NEEDED]` |
| G2 | Appendix C | New row: gateway bypass | Gap settled by reading; grading basis measured on #78; grade `[WG-INPUT NEEDED]` |
| G3 | Appendix C | Qualify the Full rating of "Evidence repudiation" and "Audit tampering" to recorded actions | Settled by reading; wording `[WG-INPUT NEEDED]` |
| G4 | New C10.2 row | Disclose who operates the gateway, separately from who holds the evidence keys | Judgement |
| G5 | C10.3.2, auditor evidence | Take the action count from a source that does not depend on the gateway | Defect settled by reading; wording is drafting |
| G6 | README | Restate the enforcement boundary | Editor |

**What this rests on.** The text of C7, C10 and Appendix C at `93d0e28`, read for this proposal,
and the measurements @vaverkamatous-rgb reported on #78 from a local implementation that observes
effects without going through the enforcement path. No attack was run against the reference
implementation for this proposal. Coverage grades and Levels are left to the working group.

**Relation to [#113](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/113).** Its L5
qualifies the same two Full rows on a different ground: algorithm breaks over the retention
period. The two qualifications compose, and G3 is written so that either can be adopted alone.

---

# G1: Appendix C, gateway compromise

**Where:** `0x92-Appendix-C_Threat-Model.md`, the landscape table and the coverage table, family
"Record integrity and resilience", after "Audit tampering". Appendix C is normative, so the wording
is the working group's; what follows is the input.

**Current text:** none; this is an addition.

**Proposed landscape row**

> `| Gateway compromise | The mediation point admits some actions without evidence, or signs evidence for a filtered subset of what it releases |`

**Proposed coverage row**

> `| Gateway compromise | Partial | Every record that arrives is verifiable and attributable to the gateway's attested identity (7.3.2); a failure of the evidence pipeline itself is recorded and fails closed (7.6.1, 7.6.3) | An action the gateway released and never recorded: the records that arrived carry no trace of it, and sequence continuity (7.6.2) is issued by the same component |`

**Why:** the gateway holds the signing keys of 7.3.2, sits in the path of every action at Level 3,
and at Level 4 refuses actions under 7.6.3. It is the component every other row's defence passes
through, and the threat model should say what happens when it is the adversary.

**Confidence:** that the row is absent is settled by the grep above. Partial is proposed because
the evidence still verifies what was recorded; `[WG-INPUT NEEDED]` on the grade.

---

# G2: Appendix C, gateway bypass

**Where:** as G1, after the gateway compromise row.

**Proposed landscape row**

> `| Gateway bypass | The agent reaches a tool or causes an effect by a path the gateway does not mediate |`

**Proposed coverage row**

> `| Gateway bypass | Partial | 7.1.1's auditor test attempts a direct tool call from the agent runtime; where a party that does not depend on the gateway enumerates a declared, closed effect space and reconciles it against the evidence, an unrecorded effect surfaces as a finding | An effect outside the declared effect space; a single lookup cannot tell an absent effect from an unreadable one, so a failed enumeration is reported as its own outcome and never as "no unrecorded effect" |`

**Why:** 7.1.1 forbids a bypass path and its auditor evidence tests for one at assessment time.
Nothing grades what the evidence shows when a path opens later. @vaverkamatous-rgb measured where
reconciliation against the tool side holds: a lookup at a named path answered "present" or
"could not establish", and a removed file and a permission-denied read gave the same answer.
Enumerating every regular file under a declared root, and refusing to answer if any part was
unreadable, did establish absence (301 files, matching `find` exactly). The same work found false
absence on a case-insensitive volume and FIFOs skipped without a signal. Those bounds are why the
grade is Partial and why the out-of-scope cell names a failed enumeration.

The failed-enumeration outcome is the same concern as
[#65](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/65) and
[#66](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/66): "could not evaluate" must
not read as "clean".

**Confidence:** absence of the row is settled by reading. The grading basis comes from one
machine, the local filesystem and a single injection run, as its author says; `[WG-INPUT NEEDED]`
on the grade and on whether "declared effect space" needs a definition in Appendix A.

---

# G3: Appendix C, qualify the two Full rows

**Current rows**

> `| Audit tampering | Full | Records are tamper-evident, generated by the mechanism at execution, not operator-narrated | Insider compromise at the silicon layer, disclosed via trust assumptions |`

> `| Evidence repudiation | Full | Cryptographic evidence is openly verifiable and non-repudiable; the operator cannot deny an action occurred | Disputes about the meaning or significance of an action, only whether it occurred |`

**Proposed rows**

> `| Audit tampering | Full, for recorded actions | Records are tamper-evident, generated by the mechanism at execution, not operator-narrated | Insider compromise at the silicon layer, disclosed via trust assumptions; omission by the gateway (see Gateway compromise) |`

> `| Evidence repudiation | Full, for recorded actions | Cryptographic evidence is openly verifiable and non-repudiable; the operator cannot deny a recorded action occurred | Disputes about the meaning or significance of an action, only whether it occurred; an action the gateway released without a record (see Gateway compromise, Gateway bypass) |`

**Why:** both Full grades are true of the records and are read as true of the actions. The middle
cell of "Evidence repudiation" already says "an action", so the qualification is a scope
correction rather than a downgrade.

**Confidence:** settled by reading; the wording is `[WG-INPUT NEEDED]`. If #113's L5 is adopted,
its qualification and this one sit in the same cell.

---

# G4: new C10.2 row, who operates the gateway

**Where:** `0x10-C10-Conformance-and-Disclosure.md`, C10.2 table, after the rows P01 and #113
propose. Numbered here as **10.2.6** on that basis.

**Proposed text** (new row)

> `| **10.2.6** | **Verify that** the disclosure names the party that operates each Action Interception Gateway (7.1.1) and the party that can change its configuration or code, separately from the custodian of the evidence keys (7.3.2), and states whether either is the operator of the agent. | 1 |`

**Auditor evidence:** 10.2.6: the gateway's deployment and change-control records against the
disclosure; a party with change rights over the gateway that the disclosure does not name is a
finding.

**Why:** 7.3.2 asks who holds the keys. A disclosure can answer that fully and say nothing about
who decides what the gateway admits, which is the question G1 turns on. Level 1 matches 10.2.1:
it is a disclosure, not a mechanism.

**Confidence:** **judgement call.** The gap is settled by reading C10.2; the Level and placement
are the working group's.

---

# G5: C10.3.2, an action count the gateway does not produce

**Current auditor evidence**

> 10.3.2: run the count reconciliation yourself over a sample window.

**Proposed auditor evidence**

> 10.3.2: run the count reconciliation yourself over a sample window, taking the action count from
> a source the gateway does not produce (the tool's or service's own request log, or egress
> records at the network boundary) and naming that source. A count read from the gateway is a
> consistency test of the gateway, not a completeness test.

**Why:** the requirement's text, "reconciling gateway action counts against evidence-record
counts", allows both sides of the reconciliation to come from one component. The requirement is
Level 4, the Tier at which the system is meant to enforce its own controls, so the count it rests
on should not come from the component being counted.

[#65](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/65) found that a declared
source which stops producing evidence is caught only by 10.3.2. That holds only when the action
count comes from somewhere other than the source that stopped.

**Confidence:** the defect is settled by reading; the wording is drafting. Whether the
requirement text itself should change is `[WG-INPUT NEEDED]`.

---

# G6: README, the enforcement boundary

**Current text** (README, "What Proof-of-Control is not")

> **Not runtime enforcement.** Enforcement (what an agent *may* do) is CSA AARM's half;
> Proof-of-Control is the evidence half (what it *did*, verifiable by others).

**Proposed text**

> **Not a policy engine.** Proof-of-Control does not define what an agent *may* do; that is the
> operator's policy, and CSA AARM's half. It does require one enforcement point (C7.1) whose own
> policy is narrow: no action is released until its evidence exists.

**Why:** C7.1.3 is enforcement. The draft AARM crosswalk in `mappings/csa-aarm.md`, marked "Draft
seed coding, single coder", records that AARM "places no ordering or durability requirement on
the receipt, so evidence emission is never a precondition of action release", and lists 7.1.3,
7.1.4 and 7.1.5 as not reached. On the crosswalk's own coding, the enforcement properties the
Tier 3 threshold depends on are the ones the other half does not supply. The README is
informative, so this is an editor's change.

---

# What I do not propose, and why

1. **No change to C7.1.** 7.1.1, 7.1.3 and 7.1.4 are right. The gap is that the threat model has
   not caught up with them.
2. **No requirement for a second gateway.** Running two mediation points to cross-verify each
   other is one design; enumeration of a declared effect space is another. G2 grades the outcome
   and leaves the design open.
3. **No Level for G1 to G3.** Appendix C carries coverage grades, not Levels.

# Knock-on edits implied but not drafted here

* **README**, "32 threats" in the Appendix C row of the table of contents, becomes 34 with G1 and
  G2, and the appendix's opening sentence needs a fourth source of threats.
* **`docs/use-cases/THREATS.md`** and the coverage block it feeds are generated; the generator
  needs the new rows rather than a hand edit.
* **`mappings/csa-aarm.md`**, "The Relationship" still says the mapping "contains exact matches
  precisely there (action interception, the runtime gateway)", while its own C7.1 row now codes
  Partial, 2 of 5.

# Sources

* `0.1/en/0x10-C07-Evidence-Generation-and-Properties.md`: control objective, 7.1.1 to 7.1.5,
  7.3.2, 7.6.1 to 7.6.3
* `0.1/en/0x10-C10-Conformance-and-Disclosure.md`: C10.2, 10.3.2
* `0.1/en/0x92-Appendix-C_Threat-Model.md`, at `93d0e28`
* `0.1/en/0x03-Using-Proof-of-Control.md`: the Level table
* `mappings/csa-aarm.md`: the C7.1 row and the C7.1 summary line
* [#78](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/78), including the
  2026-09-26 comment by @vaverkamatous-rgb
* [#113](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/113), L5
