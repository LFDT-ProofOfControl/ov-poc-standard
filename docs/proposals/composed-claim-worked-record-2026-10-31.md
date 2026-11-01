# A worked assessor record for composed claims under C8.1.7 (#174) — 31 October 2026

Status: **proposed informative companion; not adopted standard text.**

- **Date.** 31 October 2026.
- **Author and disclosure.** Mikhail Sergeev, author of [#174](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/174); prepared with AI assistance. The worked record is hypothetical, and T1–T5 are proposed and unexecuted. It has not been verified against any running system.
- **What it is.** An informative companion to #174. It is not an adopted or proposed normative row, and it claims no adoption.
- **Source base.** Upstream master `54a7bc67140b39c9107216cd390dd47c1d42946d`; sources and capture limits are listed in section 6. References to source state describe that captured context.
- **Publication scope.** Supporting GitHub material, separate from [PR182](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/182). This is not a timely final standard comment or evidence of an extended 30 October comment deadline.

## 1. What already exists, and what this adds

The concept is already public. This candidate does not rediscover it.

| Source | What it already provides |
|---|---|
| C8 8.1.2, 8.1.7, 8.2.1 | A register entry, a trust analysis and a mechanism-to-fact mapping for each claim. A vendor-rooted attestation reaches Tier 3 only when composed with independent anchoring, and the vendor assumption stays on the disclosure. |
| P01 P7, P11, P12 | Anchoring adds log-operator non-equivocation with a detection window, plus ledger fidelity. It makes *the history publicly auditable while the measurement still rests on the same chain*. Shared dependencies and composition assumptions are disclosed. P01's findings are tool results on five self-authored deployment descriptions, not observations of this hypothetical deployment. |
| #174 body | The exact proposition; the predicate per component, against which parties; bindings; shared dependencies; falsify versus suppress; the limitation resolved. A proposed C8.1 row and a synthetic false-measurement test. |
| #174 comment 6502860323, after Bjørn Vidar Hauge's comment 6500255112 | The predicates required, which were checked, outcomes, scope and what remains not assessed. Successful, failed, unavailable and unevaluable are distinguished. Two proposed fixed-log variants. |
| #162 (David McKibbin) and Bjørn Vidar Hauge's reply | Verifiability is not sufficiency. Evidence outcomes stay separate from ALLOW/DENY. Uncertainty is never upgraded to pass. |
| PR #142 (StevenMih, dated register note, open at source capture) | Established and Assumed lists. Each assumed party records who selected it and whether its dishonesty is publicly detectable. |
| #114 and comment 6505930949 | Integrity and anchoring are reported separately. A block served without a verifiable proof rests on the party serving it. |
| #123 | Group keys by operator before counting sources. |

**Scope of the novelty statement.** Among the pinned sources inspected for this candidate (listed in section 6), none shows a *filled* record: one composed claim carried end to end through the #174 procedure, with each test tied to the field it exercises. The overlap search was keyword-bounded, so this statement covers only those sources.

This candidate supplies:

- (a) one worked record;
- (b) a per-adversary reading under a single capability model;
- (c) the expected record for each existing proposed test;
- (d) two further proposed tests, T4 and T5.

## 2. The worked record

The example is hypothetical and describes no real deployment:

- A vendor-rooted TEE attestation report R is committed to a public transparency log L.
- The verifier appraises R at appraisal time t_a.
- The verifier itself obtains and compares authenticated views of L, from identified sources W1 and W2, up to observation cutoff τ.

### 2.1 Component observations

Each row is a computation or observation by the verifier. None is a proposition about the producing environment or about the future.

| ID | Observation | Evidence supplied | Trusted dependencies (assumed, not verified here) |
|---|---|---|---|
| Q1a | R's signature chains to vendor root V through collateral valid at t_a, and R's report data binds the verifier's fresh challenge | R; collateral; challenge | V; collateral service; the hardware measurement mechanism |
| Q1b | The measurement field of R equals reference value M (byte or value equality only) | R; M | None for the equality itself |
| Q1c | Reference-authority appraisal under the stated policy: M was published by RVP, and RVP's authority as reference publisher for this claim is established, under the policy the record names, from available authoritative material | M; RVP publication and authority material; the named policy | The named policy and the authority material it relies on. This appraisal does not establish that M denotes good or intended software; that remains a separate premise of PB |
| Q2 | digest d of R is a leaf of L at signed tree head S2 | Inclusion proof; signed head S2 | Binding of LO's head-signing key to LO |
| Q3 | S2 is an append-only extension of S1 | Consistency proof; signed heads S1 and S2 | As for Q2 |
| Q4 | Identified view comparison. The verifier obtained the view set {H_W1, H_W2}: LO-signed tree heads of L covering S1..S2, one obtained from W1 and one from W2, each before τ. It verified each head under LO's key and computed consistency between them and with S1 and S2. The completed comparison found no conflict. | The obtained heads, their source identities and acquisition times; the consistency proofs used | Acquisition: each head was actually obtained from the named source before τ. Binding: each head verifies under LO's key for L, and each source identity is authenticated. Coverage, needed only for the broader inference in 2.2: the set includes the views served to the relevant relying parties |
| Q5 | Authenticated time assertion: a time t, signed by LO and bound to d, is present in the receipt | Signed receipt | Binding of LO's signing key to LO, as for Q2 |
| Q6 | R and its proofs remain retrievable after τ (availability and retention) | — | Not assessed in this record |

### 2.2 Propositions

A register entry under 8.1.7 must say which of these propositions it grades.

**PB (environment).** The environment that produced R ran the software denoted by M when R was generated. This is a conditional inference from Q1a, Q1b and Q1c. It holds only under these premises:

- V and the collateral service are honest and uncompromised;
- the hardware measured correctly;
- M denotes the intended software; this is not established by Q1c's authority appraisal;
- the measurement-to-software mapping is discriminating enough for the inference drawn;
- the challenge binding links R to this appraisal session.

Q1b alone is an observed value equality and establishes nothing about the environment.

**PA-obs (history as observed).** A fixed conjunction:

- (i) R, with digest d, is included in L at S2 (Q2);
- (ii) S2 extends S1 (Q3);
- (iii) in the identified view set {H_W1, H_W2}, obtained and compared by the verifier up to τ, no conflicting view of L over S1..S2 appeared (Q4).

Conjunct (iii) concerns that set and that cutoff only, not all possible views.

**PA-reach (broader inference, not part of PA-obs).** No conflicting head of L over S1..S2 was served to any relevant relying party up to τ. This is conditionally supported only if the Q4 coverage premise is accepted. A compared source cannot detect a view it never receives.

**PA-time.** R existed no later than t. This is a truthful-bound proposition, distinct from Q5. It is conditionally supported only if all of these premises are accepted:

- LO's clock was correct;
- LO was honest about t;
- t is bound to d (Q5).

Otherwise PA-time is not established. The authenticated assertion itself remains the observation Q5.

**PA-future (conditional detectability).** A later alteration of committed history would become visible. Alteration here means a later signed head that does not extend S2, or one under which d is no longer a leaf. This requires all of:

- views continue to be obtained and compared after τ;
- their acquisition and coverage premises continue to hold;
- comparison happens within the disclosed window w (P01 P7).

Withholding R or its proofs from a requester is a different matter. It is availability (Q6), not an alteration of committed history.

Evidence through S2 and τ cannot establish PA-future. The record lists it as a premise set only.

**PC (composite).** The conjunction of PB and PA-obs, with PA-time optional.

### 2.3 Outcomes and supported conclusions

The outcome vocabulary follows #162 and the #174 reply: verified, failed, unavailable, unevaluable, not assessed.

| ID | Outcome | Scope | Reason |
|---|---|---|---|
| Q1a | verified | R; collateral at t_a; relative to V | Chain, collateral and challenge binding verify |
| Q1b | verified | Observed equality only | Field equals M |
| Q1c | verified | RVP's authority for this claim, under the stated policy | Authority material obtained and appraised under that policy |
| Q2 | verified | S2 only | Inclusion proof verifies against S2 |
| Q3 | verified | S1→S2 only | Consistency proof verifies |
| Q4 | verified | {H_W1, H_W2}; S1..S2; up to τ | Heads obtained and verified under LO's key; completed comparison found no conflict |
| Q5 | verified | The authenticated assertion only | LO's signature over t and d verifies |
| Q6 | not assessed | — | Outside this record's scope |

Supported conclusions:

- **PB:** conditionally supported, given the PB premises. It is not supported against V, the collateral service or RVP, because the premises assume those parties honest.
- **PA-obs:** supported, scoped to S1, S2, the identified view set and cutoff τ, under the capability model in 2.4.
- **PA-reach:** conditionally supported if the coverage premise is accepted, and not established otherwise.
- **Q5:** the authenticated time assertion by LO is verified.
- **PA-time:** conditionally supported if the time premises are accepted, and not established otherwise.
- **PA-future:** not established. Its premises are listed in 2.7.
- **PC:** conditionally supported when the PB premises hold and PA-obs holds in its stated scope. Lack of unconditional support does not make PC false. Against any party able to defeat one necessary conjunct (2.4), PC is unsupported. The Tier for PC remains open (2.6).

### 2.4 One capability model

**Capabilities per evidence item:**

- *forge:* produce false evidence that verifies;
- *suppress:* prevent production or publication;
- *withhold:* refuse to serve existing evidence later.

**The rule, applied per exact proposition.** This follows the claim-relative test in #174.

- **Atomic proposition, one route:** unsupported against party X when X can make that route's evidence verify while the proposition is false.
- **Atomic proposition, redundant routes:** unsupported against X only when X can defeat every route.
  - Routes count as redundant only if each one independently supports the same proposition with the same scope.
  - Complementary inputs to one observation are not redundant routes. For example, the signed heads and the acquisition and comparison of views that together make up Q4 are complementary.
- **Conjunction such as PC or PA-obs:** unsupported against X when X can defeat any one necessary conjunct.
  - V can forge the report behind PB. PC is therefore unsupported against V, even though the anchor faithfully preserves the false report.
- **Shared dependency** is a separate question from the truth of a conjunction. Components that one party controls do not count as separate routes against that party.

**Selection is not control.** That a party selected another is recorded, but it is not itself evidence of control. Effective control is either stipulated (as in T4) or evidenced. Otherwise it is recorded as *not established*.

| Party | Trusted dependency for | Can forge | Can suppress or withhold | Resisted by this record? |
|---|---|---|---|---|
| V, collateral service | PB | Q1a, and so PB | — | No. Assumed honest for PB. PB and PC are unsupported against them |
| RVP | PB | M and its authority material (Q1c) | — | No. Assumed honest for PB. PB and PC are unsupported against RVP |
| LO | Meaning of the Q2, Q3, Q4 and Q5 signatures | Conflicting heads (equivocation); a false t | Withhold inclusion; withhold proofs after τ (Q6) | Equivocation is exposed only if conflicting heads appear in the compared set (Q4). A head served only to parties outside that set is not detected, so PA-reach rests on the coverage premise. False t: not resisted, so PA-time stays premise-dependent. Withholding: availability, not assessed |
| W1, W2 | Acquisition and coverage of Q4: they relay the heads LO served them | Cannot forge an LO-signed head | Not relay, or relay selectively | Selective relay can keep a conflict out of the set. PA-obs remains a statement about the set actually obtained; PA-reach depends on coverage |
| Operator | — | Through any party it effectively controls | Withhold R from L; act off-record | Depends on control (below) |
| Toolchain B (hypothetical shared case) | Q1 verifier and log verifier | Both | — | Q1 and Q2 to Q4 do not count separately against B. PB, PA-obs and PC are all unsupported against B |

The rule gives one consequence per case:

- **Operator effectively controls LO; W1 and W2 are not controlled.** The comparison of the disclosed set stands, and PA-obs holds for that set. LO could still have served a conflicting head to a party whose view is not in the set. Neither W1 nor W2 detects a view it never receives, so PA-reach remains conditional on the coverage premise.
- **Operator effectively controls LO and both compared sources.**
  - The byte comparison of the disclosed set still exists and is recorded as computed. PA-obs, as a statement about that set, is not removed by the control.
  - The acquisition and coverage premises cannot be relied on against the operator, because it controls what the sources hold and relay. PA-reach is therefore unsupported against the operator.
  - The anchor is not credited, against the operator, with resolving unseen alteration.
  - For other parties, assess each necessary conjunct under the same capability model and stated premises. No support against V, the collateral service or RVP follows for PB or PC.
- **Operator selected the sources; control not established.** The results are unchanged, and the register records the selection. Whether operator selection disqualifies the anchor as independent for Tier purposes is the open C8 question. `[WG-INPUT NEEDED]`

### 2.5 Shared dependencies

P01 P11 discloses a shared party once and marks it shared. This record adds the consequence of that sharing, using the 2.4 rule. A shared dependency removes separate-route credit against that party. It is not converted into a number.

### 2.6 Tier reasoning

The record does not output a composite Tier. It supplies the per-proposition inputs that the 8.1.2 recomputation needs.

1. A Tier is registered for a named proposition, not for the mechanism bundle.
2. For PB, the anchor is credited with nothing. For PA-obs, the anchor is credited with three things, under the 2.4 conditions:
   - authenticated inclusion at S2;
   - append-only consistency from S1 to S2;
   - no conflict in the identified view set compared through τ.

   Credit for resolving unseen alteration by the operator requires PA-reach, and so the coverage premise. Detection of later alteration of committed history rests on the PA-future premises. Withholding is availability (Q6), and the anchor is not credited with it.
3. PC is conditionally supported. Whether a register may assign Tier 3 to PC, while PB rests on V, is for the working group to decide. The C8 note leaves the Tier 2/Tier 3 test open. `[WG-INPUT NEEDED]` This record makes the choice visible and does not resolve it.
4. The Tier is not computed as a minimum, maximum, mean, independent-key count or weakest outcome. The #174 body disclaims a component minimum, and P01 rejects a universal trust ranking.

### 2.7 Explicit premises not established by the record

- **PB:**
  - V and the collateral service are honest;
  - the hardware measures correctly;
  - M denotes the intended software;
  - the measurement-to-software mapping is discriminating enough for the inference drawn;
  - the challenge binding holds.
- **Q4 and PA-reach:**
  - acquisition of each head from the named source before τ;
  - authentic bindings of the heads and source identities;
  - for PA-reach, coverage of the views served to relevant relying parties.
- **PA-time:** LO's clock is correct; LO is honest about t; t is bound to d.
- **PA-future:** views continue to be obtained and compared after τ under the same premises, within the disclosed window.
- **Availability:** R and its proofs remain retrievable (Q6, not assessed).
- **Completeness:** the operator submitted every report. Tier 3 does not give completeness (C8, *What a Tier 3 claim does not give you*).
- **No external effects:** Q1a to Q6 establish nothing about any external effect of the environment's actions. P02 keeps request binding separate from effect binding.

## 3. Expected records for the proposed tests (none executed)

**Baseline.** Unless a case says otherwise, the evidence and outcomes for Q1a, Q1b, Q1c and Q2 to Q5 are those of 2.3, and Q6 remains not assessed.

**Pass and fail.** Pass means the published verifier and the register produce the expected record. Fail means one outcome category is reported as another, or a log result fills a measurement, view, time or environment field.

| Case | Origin | Setup | Expected record | Fails if |
|---|---|---|---|---|
| T1 | #174 body | A test root admitted by the verification configuration issues R with a deliberately false measurement. R is anchored. S1, S2 and a consistency proof are obtained. | Q1a verified *relative to the test root*, which is listed as a trusted dependency. Q1b is the observed equality as issued. Q2 and Q3 verified; Q4 as in the baseline. Q5: the authenticated assertion is verified, but PA-time is not established unless the time premises are accepted. PA-obs is supported in scope. PB is recorded as conditional on the test root and is not established for the actual environment. | PB or PC is reported as established by Q1b or Q2 to Q5, or Q5 is reported as a truthful bound |
| T2 | #174 reply, variant 1; Bjørn Vidar Hauge's comment | Material required for the measurement appraisal is withheld | Q1a, Q1b or Q1c unavailable, with a reason. Q2 and Q3 verified. PB is not established from the available evidence. This is not evidence that the measurement is false. | Q1 is reported verified or failed |
| T3 | #174 reply, variant 2 | The material is present, but RVP's authority for this claim cannot be established under the stated policy | Q1b verified, as observed equality only. Q1c unevaluable, with a reason. PB not established. Two contrasts follow. | Q1b is reported unevaluable; Q1c is reported verified or failed; a policy rejection is reported as a false environment; or a value inequality is reported as refuting software identity without the discriminating-mapping premise |

**T3 contrasts.**

- *Q1b failed:* a completed comparison finds the measurement differs from M. This counts as evidence against PB only when Q1a and Q1c are accepted *and* the measurement-to-reference mapping is sufficiently discriminating for that inference. Otherwise it records only that the values differ.
- *Q1c failed:* a completed appraisal rejects RVP under the stated policy. This is a policy outcome on admissibility. It leaves PB not established under that policy and does not show that the environment ran other software.

| Case | Origin | Setup | Expected record | Fails if |
|---|---|---|---|---|
| T4 | New in this candidate | The baseline, plus a stipulation that the operator has effective control of LO and of both compared sources W1 and W2. Selection alone is not used. | See the T4 record below | The comparison of the disclosed set is reported as absent; PA-reach or the unseen-alteration credit is granted against the operator; support against other parties is asserted without assessing each conjunct; or a variant infers control from selection without a stipulation |
| T5 | New in this candidate | Only S2 and its inclusion proof are supplied; the S1 head and the heads from W1 and W2 that Q3 and Q4 require are absent | Q2 verified, so inclusion of d at S2 is supported on its own. Q3 unavailable (reason: the S1 signed head was not supplied). Q4 unavailable (reason: no authenticated heads from W1 or W2 were obtained). The fixed proposition PA-obs is *not established*. A narrower proposition, if registered, carries its own name, for example *PA-incl: d is a leaf of L at S2*. Had the S1 head and the source heads been supplied but the comparison not run, Q3 and Q4 would be *not assessed*. | Q3 or Q4 is inferred from Q2, PA-obs is reported as supported, or unavailable and not assessed are reported interchangeably |

**T4 expected record.**

- Q2 to Q4 are recorded as computed, and the comparison of the disclosed set {H_W1, H_W2} remains recorded.
- PA-obs, scoped to that set, is not removed by the control.
- The acquisition and coverage premises cannot be relied on against the operator. PA-reach is therefore unsupported against the operator, and the anchor is not credited, against the operator, with resolving unseen alteration.
- For other parties, assess each necessary conjunct under the same capability model and stated premises. No support against V, the collateral service or RVP follows for PB or PC.

T4 and T5 are proposed and not executed. Neither depends on a hardware compromise. Like T1, both exercise the reporting boundary.

## 4. Proposed text (informative auditor evidence)

This follows the P01 shape.

- **Where.** This dated informative companion, `docs/proposals/composed-claim-worked-record-2026-10-31.md`, illustrates the auditor-evidence note of the row proposed in #174, as extended by the #174 reply.
- **Current text.** None in the standard. The #174 row and reply are public comments, not adopted text.
- **Proposed text.** *For one sampled composed claim, confirm that the register record lists:*
  - *the exact proposition graded;*
  - *each component observation, with outcome, scope and reason, distinguishing verified, failed, unavailable, unevaluable and not assessed;*
  - *the trusted dependencies of each conditional inference, separately from the adversaries the record resists;*
  - *for any view comparison, the identified authenticated view set, its sources, the cutoff, and the acquisition, binding and coverage premises;*
  - *the basis of any time claim, distinguishing an authenticated assertion from a truthful bound;*
  - *for each proposition, the parties against which it is unsupported because they can defeat a necessary conjunct, or every route that independently supports the same proposition and scope;*
  - *availability, recorded separately from integrity.*

  *Exercise cases T1 to T5.*
- **Why.** An assessor can close out a filled record and its negative cases against an artifact, which is what the CONTRIBUTING auditability rule asks for.
- **Confidence.**
  - The record shape and T1 to T3: drafting on public reasoning.
  - T4 and T5: proposed.
  - The Tier for PC: `[WG-INPUT NEEDED]`.

## 5. Deliberately not proposed

- **No composite-Tier formula.** P02's weakest-of-four verdict in its proposed 4.3.1 is for endpoint EB1–EB4 classification only.
- **No endpoint or effect claim** (P02).
- **No relying-party sufficiency judgement** (#162).
- **No decision on #149**, and no restatement of the Tier 2/Tier 3 test.
- **No normative row, manifest schema or rename.** Trust-minimized stays.
- **No new experiment.** No claim of working-group acceptance, and no claim that a supplement after the 30 October comment date meets that date.

## 6. Sources, attribution and reading limits

This dated companion builds on Mikhail Sergeev's #174 body and reply, David McKibbin's #162 and Bjørn Vidar Hauge's replies, and the existing C8, P01 and P02 texts of the Proof-of-Control project. The related-source table above credits StevenMih's PR142; #114 is by Nirinasoa Rajaona (`e-lemur`), its later reply is by `FantasticoFox`, and #123 is by `GravitOpenNetwork`. These sources remain their authors' contributions. AI assistance in preparing this companion does not constitute independent validation.

The source capture was collected on 31 October 2026 at 22:12:23.187Z. Repository files below are pinned to `54a7bc67140b39c9107216cd390dd47c1d42946d`. Issue, comment and PR records are mutable: their listed `updated_at` values and captured-text digests identify the inspected versions and do not make the current pages immutable. Digests are SHA-256 of the captured UTF-8 source representations, not raw HTTP response bytes.

| Captured source | Reference or last update | SHA-256 |
|---|---|---|
| [C8.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/0.1/en/0x10-C08-Verifiability-Tiers.md) | `54a7bc67140b39c9107216cd390dd47c1d42946d` | `9f63ee9e6bb84e2ea8fce96ca6ac2f9c42b753a6749e9af377d7c71d21016f56` |
| [P01.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/docs/proposals/P01-trust-calculus-tiers.md) | `54a7bc67140b39c9107216cd390dd47c1d42946d` | `0fcd2d64913d5202e224ae28a1415d4d4deea4c2f3dccaf1e043a336e8afd1d3` |
| [P02.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/docs/proposals/P02-effect-binding.md) | `54a7bc67140b39c9107216cd390dd47c1d42946d` | `ae1843aad4a99bedd70aa155be614e7631aebed9191e0acc3b7ea4e36c347ac1` |
| [proposals-README.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/docs/proposals/README.md) | `54a7bc67140b39c9107216cd390dd47c1d42946d` | `1d6b9efa2d74ff8fd76065f4e01305c42c4817819e83b816c8fc44534d258770` |
| [CONTRIBUTING.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/CONTRIBUTING.md) | `54a7bc67140b39c9107216cd390dd47c1d42946d` | `94a0c5de85a2f2143ec00cdb83a35c041d17d16bbcb9363108b814f8f9a80844` |
| [CLAUDE.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/CLAUDE.md) | `54a7bc67140b39c9107216cd390dd47c1d42946d` | `a688285e221293eb895bbe78fa632c08b1015d9f2e0b67cdd10d481f231cda1a` |
| [README.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/README.md) | `54a7bc67140b39c9107216cd390dd47c1d42946d` | `10fcc7f74c18d6c74781282183d7075a0b93bf91585e2baf420bf5e6323a3d83` |
| [issue-162.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/162) | `updated_at=2026-10-29T15:01:48Z` | `e244314419675f2acd89a44ae84a35717d320b2e82bd715b6d42ae62ff0d9e13` |
| [issue-162-comment-6500262155.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/162#issuecomment-6500262155) | `updated_at=2026-10-29T15:01:48Z` | `97b8995e00d7781deb114ea709d8836f24d234c28ef84fb410a31204c29adbca` |
| [issue-174.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/174) | `updated_at=2026-10-29T16:49:04Z` | `4b96509e52be425ec737bbede2b629bb7d063d814a3104a608e55aef7b103357` |
| [issue-174-comment-6500255112.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/174#issuecomment-6500255112) | `updated_at=2026-10-29T15:01:32Z` | `bba0ec909c18917fc46d386a45f2f72cb84f2bccf0508cde22a0f7f4ac4d8ad8` |
| [issue-174-comment-6502860323.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/174#issuecomment-6502860323) | `updated_at=2026-10-29T16:49:04Z` | `8d1b69debe02384251ef26c3779859f3137778cc5a5ccf08e02d28db4efe1300` |
| [pr-142.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/142) | `updated_at=2026-10-21T00:19:30Z;head=cd33b2d20884600c3a15e2677abaaef2c320a646` | `066b8444456385bdb3677c71bc50dc8ce9f4b2535264298b45e88670c55b14b3` |
| [issue-114.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/114) | `updated_at=2026-10-29T19:29:08Z` | `da60dc272e98426e8202b278c7497840da6ce49f7554d8e38e3a6c54fdee1739` |
| [issue-114-comment-6505930949.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/114#issuecomment-6505930949) | `updated_at=2026-10-29T19:29:08Z` | `126ab0efc89ccb1c17d1c82501954b0be6eee60312f278bd53cfe66f7d463290` |
| [issue-123.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/123) | `updated_at=2026-10-15T09:19:33Z` | `4018f6756305b7ae7141644c17f65a7f1327fba977e94ecb6e75ad73fa35e3e7` |
| [issue-149.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/149) | `updated_at=2026-10-21T20:30:55Z` | `8893561d7da8b00c1172b5caa246ffbe053f0995c18708ca5c020bcfd52f707f` |
| [issue-140.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/140) | `updated_at=2026-10-21T13:02:22Z` | `c069731c8d594da2b3e0a664ab55b5389354d7f89bc647185a018bb9a486ecb3` |
| [issue-140-comment-6314717255.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/140#issuecomment-6314717255) | `updated_at=2026-10-21T11:23:52Z` | `a47b9abefc038b6f7b36b77226f53f0bff54070e4dc487de9e8fb9528052f874` |
| [issue-140-comment-6316353024.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/140#issuecomment-6316353024) | `updated_at=2026-10-21T12:48:27Z` | `11257e21718964af63e800d4b212eb2d6f8b04b69557b42da5e5771e9ed2405c` |
| [issue-140-comment-6316721666.md](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/140#issuecomment-6316721666) | `updated_at=2026-10-21T13:02:22Z` | `d7c4ac64dd4eaf7fb98d156a25090c0a82bbc117fadb422111a522aafbb4e9b9` |

The remaining-delta statement is confined to these inspected sources and the bounded overlap inventory. The composition-keyword search was not exhaustive. The bodies of #122 and #126 were not read; no non-overlap conclusion is drawn from their titles alone. #140 concerned reversibility/action-class evidence and is not resolved by this record. No current exclusivity or ownership claim follows from the bounded search.

The illustrative outcomes in section 2 and expected records in section 3 are not execution results. All T1–T5 remain proposed and unexecuted. The composite Tier remains open for working-group disposition. No result from the separate PR182 coverage-reconciliation material is imported into this record.
