# Proposal: coverage reconciliation in C10.3.2 and C10.3.6 (from issue #173)

**Date:** 2026-10-29 · **Source:** `ov-poc-standard` master `93d0e282fc177d5df741de4cdd6a0d0dacf1955a`. The changes below tighten the current requirements: new assessor cases are proposed requirement changes, not an editorial clarification.

## The central finding

10.3.2 asks the auditor to "reconcile gateway action counts against evidence-record counts". Equal totals establish a cardinality relation, not that each in-scope action has the records it owes. The fix is to reconcile **obligations**, not counts. Expected obligations come from the standard's requirements as operationalized by a declared model, applied to an identified population of actions; they are not derived solely from the evidence records that survived. Otherwise, as Christopher Filkins put it, an implementation can make missing evidence disappear by deriving its expectations from the incomplete evidence.

---

**Source of the findings**

* [#173](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173) — the count counterexample and the per-(action, phase) reconciliation.
* [Addendum on the phase vocabulary](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173#issuecomment-6502874578) — `interception_point` has no value for 7.1.2's "during"; a required phase the format cannot express is one format finding, not one missing record per action; `docs/proposals/tooling-findings.md` §5.
* Christopher Filkins, [first reply](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173#issuecomment-6501456428) (operation / attempt / phase; unresolved outcomes; later evidence as a supplement) and [second reply](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173#issuecomment-6509031753) (obligations declared rather than inferred from surviving records; versioned phase vocabulary and trigger rules; undetermined triggering reported as such). Related: [#161](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/161).
* [Reply in #173](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173#issuecomment-6508003310) — matching unit, window close, later evidence.
* Joshua Waldrep, comment in the [public-comment Google Doc](https://docs.google.com/document/d/1EiiGDwLXvMxoSHp3Ru56AhR2u9gNd-6Fjs_CKZ4kU-w/edit) on "before, during, and after tool invocation" (21 October 2026): a call denied before dispatch has no tool execution to record, and the denial record should distinguish it from a dispatched call whose execution evidence is missing.
* [#176](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/176) — a compensating-duplicate regression against the reference implementation.

**Targets:** `0.1/en/0x10-C10-Conformance-and-Disclosure.md` — requirements 10.3.2 and 10.3.6, the 10.3.2 auditor-evidence entry, and a shared definition placed where both can use it (placement is a working-group decision, see D1).

---

## The evidence base, and its limits

* **Checked (count arithmetic):** the two windows in #173 — one action without records and another's written twice as distinct records; one action with three records of the same phase — keep the totals of a control window and fail a per-(action, phase) comparison. Shown by the snippet in #173; re-run with a before/after-only profile in the addendum. The snippet has no record identifiers and does not distinguish redelivery of one logical record from creation of distinct records.
* **Checked (reference verifier, narrower):** #176 runs a compensating duplicate against the reference implementation at `93d0e28` in its one-record-per-action profile. The count comparison balances; `Verifier.verify_chain` rejects the presentation in this case through sequence continuity (7.6.2). This compares count arithmetic with the full verifier; it is not an isolated ablation of 7.6.2, since the chain-link check remains. A truncated tail with no anchor still verifies.
* **Not executed:** the classification proposed here (obligation model, obligation states, record-identity policy) has not been run on any case, including case 2.
* **Not established:** that a working-group task exists for this change; how the working group will settle 7.1.2's phase semantics, the interception-point vocabulary (#81) or Appendix D issue 8.

---

## Terms used below

* **Population:** the in-scope actions of the window, under the action classes the conformance statement defines (10.1.6). The **population source** is where the list of actions comes from (for example the gateway's record of intercepted actions); its **completeness basis** is why that list is taken to contain every in-scope action (for example 7.1.1's no-bypass demonstration), or a statement that this is not established.
* **Obligation model:** a declared, versioned statement of the record phases and of the rules that determine when each record becomes required. It operationalizes the applicable requirements (today 7.1.2's three linked, independently signed records for an intercepted action) and any approved profile; it cannot remove an obligation those requirements impose.
* **Obligation state:** *triggered*, *not triggered* (with the rule that justifies it), or *undetermined* (the evidence cannot establish whether the trigger occurred). Properly identified evidence may be used to evaluate a trigger; the absence of a record is not itself evidence that its obligation was not triggered.
* **Matching unit:** (operation, delivery attempt, phase). A retry is a new attempt with its own obligations.
* **Record-identity policy:** a declared rule for when two received records are the same logical record (for example, same record identifier and same signed content). A **recognized redelivery** is the same logical record received again. **Duplicate or conflicting records** are distinct logical records that claim the same obligation. Neither satisfies another attempt's or phase's obligation.
* **Outcome state:** an action's effect may be established or unresolved at the window's close. Outcome state and obligation state are separate; an unresolved outcome does not waive an obligation already triggered (for example at dispatch).
* **Format finding:** a required phase that the record format cannot express. It is reported once with its affected scope; it does not authorize omitting the phase and is not counted as one missing record per action.

---

## Summary of proposed changes

| # | Where | Change |
|---|---|---|
| S | Shared definition (placement: D1) | Obligation model, population basis, obligation states, record-identity policy, findings, assessment record and supplements |
| C1 | 10.3.2 (Level 4) | All-action coverage is demonstrated only by a reconciliation with no findings and no unresolved outcomes at the cutoff, over a population whose completeness basis is established |
| C2 | 10.3.2 auditor evidence | Replace "run the count reconciliation" with reconciliation over a sample window and constructed windows |
| C3 | 10.3.6 (Level 3) | Keep the in-scope denominator; define the numerator; publish findings, and label a population-limited figure as such |

---

# S — shared definition

**Where:** a short normative paragraph applying to 10.3.2 and 10.3.6. Because Levels are cumulative and 10.3.6 is Level 3 while 10.3.2 is Level 4, the definition must be usable at Level 3 without requiring the Level 4 demonstration. Suggested placement: the C10.3 lead-in. Placement is decision D1.

**Proposed text**

> Coverage of an audit window is assessed against an identified population of in-scope actions (10.1.6) and a declared, versioned obligation model that operationalizes the applicable requirements, including 7.1.2, and any approved profile; the model cannot remove an obligation those requirements impose. The claim states the population source and its completeness basis, or states that completeness of the population is not established. For each action and delivery attempt, each obligation is classified as triggered, not triggered (with the justifying rule) or undetermined; expected obligations are not derived solely from the evidence records present. Each triggered obligation is met by exactly one logical record under the declared record-identity policy, or is missing, or has duplicate or conflicting records; a record that meets no obligation is unmatched; a required phase the record format cannot express is a format finding with its affected scope. A record for one attempt or phase does not meet an obligation of another. An action whose outcome is unresolved at the window's close remains in the population, and obligations it has already triggered still apply. Each window's assessment records its cutoff, the population and inputs assessed, and the version of the obligation model and of the assessment; evidence that arrives later, and any correction, is recorded as a linked supplement or an explicitly versioned revision that identifies what changed, without overwriting the original assessment.

**Why:** both requirements need the same notion of what a covered action is. Defining it once keeps the Level 3 metric and the Level 4 demonstration consistent without making the metric depend on passing the demonstration.

**Confidence:** the need is **read from the source** (10.3.6's numerator is undefined); the wording is a **judgement call**.

---

# C1 — 10.3.2

**Current text**

> `| **10.3.2** | **Verify that** evidence generation covers every in-scope action rather than a sample — demonstrated by reconciling gateway action counts against evidence-record counts over an audit window, with zero unexplained difference. | 4 |`

**Proposed text**

> `| **10.3.2** | **Verify that** evidence generation covers every in-scope action rather than a sample — demonstrated by reconciliation over an audit window under the coverage definition of C10.3, with an established completeness basis for the population and with no missing records for triggered obligations, no duplicate or conflicting records, no unmatched records, no undetermined obligations, no format findings and no unresolved outcomes at the cutoff. A recognized redelivery under the declared record-identity policy is not a finding. A reconciliation that correctly reports findings does not demonstrate coverage for that window. A comparison of totals alone does not demonstrate this requirement. | 4 |`

**Why:** the current demonstration can pass a window in which an action has no records (#173). Replacing it with a list of classifications alone would leave success undefined; the proposed rule states it. Unknowns cannot establish coverage. Cadence, incident response and suspension stay with Appendix D issue 8.

**Confidence:** the defect is **shown by a checked counterexample** in the stated profile. The replacement rule is a **judgement call**; it depends on D2 and D3.

---

# C2 — 10.3.2 auditor evidence

**Current text, verbatim:** "10.3.2 — run the count reconciliation yourself over a sample window."

**Proposed replacement:** "10.3.2 — the population source and completeness basis, the obligation model and its version, and the record-identity policy; then run the reconciliation yourself over a sample window and over constructed windows covering at least: one action without its required records while another action with the same required phase set has a distinct duplicate for each required phase, keeping the totals of a control window; one action whose records all carry the same phase, keeping the same totals; a retry, and a redelivery of one record that the declared policy recognizes; unresolved actions both with all already-required records present and with a record already triggered at dispatch missing; an action whose trigger cannot be determined; and later evidence for a closed window. Confirm each finding is reported in its own category, that a recognized redelivery is not reported as a duplicate, that the original window's assessment is preserved, and that the 10.3.6 figure does not count an action with any finding or an unresolved outcome at the cutoff as covered. An unresolved outcome alone is not a missing-record finding."

**Why:** a reconciliation run only on a clean window cannot show that it detects anything.

**Confidence:** **judgement call** on the case list; this adds assessor obligations.

---

# C3 — 10.3.6

**Current text**

> `| **10.3.6** | **Verify that** proof coverage — evidence-covered in-scope actions divided by total in-scope actions — is computed on a defined schedule and published with the claim, so coverage decay is visible rather than silent. | 3 |`

**Proposed text**

> `| **10.3.6** | **Verify that** proof coverage — evidence-covered in-scope actions divided by total in-scope actions — is computed on a defined schedule and published with the claim, so coverage decay is visible rather than silent. Under the coverage definition of C10.3, an action is evidence-covered when its outcome is resolved at the cutoff, every obligation it triggered in the window is met and it has no finding; repeated records do not increase the count. The published figure states its population source and completeness basis, and is published with the counts of missing records for triggered obligations, duplicate or conflicting records, unmatched records, undetermined obligations, format findings and unresolved outcomes. Where the completeness of the population is not established, the figure is labelled as coverage of the identified population and is not presented as coverage of all in-scope actions. | 3 |`

**Why:** the current numerator has no definition; a deployment computing it from record totals publishes 100 percent for the #173 windows. Keeping "total in-scope actions" as the denominator, and labelling a population-limited figure, prevents a metric over recorded actions from being presented as coverage of all in-scope actions when unrecorded or bypassed actions have not been ruled out. A computed partial-coverage figure is distinct from the all-action demonstration in 10.3.2.

**Confidence:** the gap is **read from the source**; the definition is a **judgement call** tied to S.

---

## Proposed cases

Record-identity policy used in these cases: same record identifier and same signed content = one logical record.

| Case | Window | Expected classification | Status |
|---|---|---|---|
| 1 | Complete population basis established; all outcomes resolved, all obligation states determined, one logical record per triggered obligation and no findings | clean control; covered | proposed |
| 2 | A and B have the same required phase set; all of A's required records are absent, while B has a distinct extra logical record for each required phase; totals equal a control window | A: missing; B: duplicate or conflicting; neither covered | count arithmetic **checked** (#173 snippet); reference-verifier rejection **checked** in #176's one-record profile; this classification **not executed** |
| 3 | Attempt 2 after a lost response, with its own records; one record of attempt 1 received twice with the same identifier and content | attempt 2 judged on its own records; recognized redelivery, no finding; attempt 1 judged on its own records | proposed |
| 4a | Dispatched, outcome unresolved at close; all already-triggered obligations met, other obligation states determined and no findings | outcome unresolved; not covered; no missing-record finding merely because the outcome is unresolved | proposed |
| 4b | Dispatched, outcome unresolved at close; the record due at dispatch is missing | outcome unresolved; dispatch obligation triggered and missing; not covered | proposed |
| 5 | The evidence cannot establish whether a trigger occurred | obligation undetermined, with reason; not covered; not treated as not required | proposed |
| 6 | A receipt for case 4b's action arrives in the next window | window 1 assessment unchanged; linked supplement states what the new evidence establishes | proposed |

Equal totals apply only to case 2 and to the same-phase window of C2. A required phase the format cannot express is a format finding (S), not one missing record per action.

---

## Limits

* **Population.** Reconciliation against the gateway's record shows correspondence within that population. Whether every in-scope action entered it is 7.1.1's question, and the gateway as the single source of both totals is the subject of #78 and #148. C3 therefore asks for the completeness basis to be stated, not assumed.
* **Dispatch is not effect.** A record due at dispatch shows the request was released, not that the effect occurred (`tooling-findings.md` §5; 7.1.4–7.1.5).
* **Cases are proposed.** Only the count arithmetic of case 2 and the narrower #176 regression were run.

---

## Mature prior practice

Financial-statement auditing separates completeness from occurrence ([PCAOB AS 1105](https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105), paragraph .11). [AS 2315](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2315), paragraph .17, makes the related point that sampling the recorded items cannot detect omissions from that population; the source must include the items that might have been omitted. This proposal follows the same logic: expected obligations come from an identified population and declared rules, not from the evidence records. No new primitive is claimed. The analogy does not establish a formal equivalence to the agent protocol and does not require organisational independence in every case.

---

## What this does not propose

* No change to 7.1.2, the schema or the interception-point vocabulary; the obligation model operationalizes them and leaves #81 open.
* No resolution of Appendix D issue 8 (cadence, incident handling, suspension). The findings in S are offered as the detection outputs its third question needs.
* No new tier or Level change; the Level allocation is decision D1.

## Open decisions for the working group

* **D1.** Where the shared definition sits so that 10.3.6 (Level 3) can use it without the Level 4 demonstration: the C10.3 lead-in, a new row, or a profile.
* **D2.** Which phase vocabulary the obligation model refers to once #81 and 7.1.2's "during" are settled, and whether trigger rules belong in the conformance claim, the disclosure (C10.2) or an approved profile.
* **D3.** What completeness basis for the population is acceptable at each Level.
* **D4.** How long an outcome may stay unresolved before Appendix D issue 8's incident handling applies.
