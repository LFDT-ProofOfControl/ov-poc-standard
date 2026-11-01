# AARM source and rationale review for the C7/C10 mapping

Author: **Mikhail Sergeev**. Prepared with AI assistance as a nonblind source review. The existing codings were visible. This is an informative proposal for source and rationale review, not a completed independent-human coding study, canonical correction, conformance assessment or coverage result.

## Scope and source views

This note addresses the 45 existing `CSA_AARM` rows in C7/C10 of the [coding sheet](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/mappings/coding_sheet.csv) at `54a7bc67140b39c9107216cd390dd47c1d42946d`. The [row companion](aarm-source-rationale-2026-10-31-rows.json) preserves each baseline label, both proposed source-view labels, the missing subduties, the rationale, explicit alternatives and an indexed source excerpt. No canonical CSV, generated crosswalk, coverage table or chart is changed. No new aggregate coverage figure is proposed.

- **P — primary:** [aarm.dev/spec](https://aarm.dev/spec), labelled v1.0, February 2026, captured 2026-10-31 at 22:34:12.040843 UTC. Author: Herman Errico; Cloud Security Alliance Technical Working Group; CC BY 4.0. Raw HTML SHA-256: `93072c4244287e984bc24e394d1d271c52a380f3ef857a06d701fdfdf1ebe598`.
- **C — primary plus companion:** the same primary text plus the separately captured [conformance/testing page](https://aarm.dev/conformance), 2026-10-31 at 22:35:47.897441 UTC. No version/date label was observed. Raw HTML SHA-256: `d293d128492431ebbd90e86134c4cb56039b632508cff707952d14c5e754f4e8`.

The companion is relevant to a present-day statement about AARM testing. Its undated contents are not silently treated as historical v1.0 text, and this review does not establish what an earlier coder could access. The primary specification points to a testing protocol; identity with a separately published archival protocol edition remains unverified. The referenced receipt schema was not separately obtained or version-identified. Its unseen contents remain **unavailable/unassessed**, not No Match.

## Concrete source and rationale corrections

[PR85](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/85) already replaced generic labels with actual R1/R4/R5 identifiers and corrected part of the AARM coding. This note builds on that baseline and does not repeat its completed changes. In particular:

1. **Recording order and mediation (7.1.3, 7.1.4).** The primary abstract explicitly places recording before execution; R1 requires interception with no bypass. These support a partial timing/mediation analogy. They do not specify the durable-write gate or attested effect-channel binding required by the Proof-of-Control rows. PM is proposed in both views, with the narrower NM reading retained as an alternative. The [rubric](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/54a7bc67140b39c9107216cd390dd47c1d42946d/mappings/rubric.md) allows a general control to partially match a more specific mechanism.
2. **Identity, signatures and key custody (7.3.2).** Primary R6 cryptographically binds a receipt to agent identity, which does not itself prescribe a signing-key architecture. Primary NM is proposed, with the broader cryptographic-control PM reading retained. The companion explicitly tests offline receipt signatures and tampering (`CT_R5_2`, `CT_R5_3`), supporting companion PM. Neither view supplies operator/agent isolation of the generating mechanism's signing keys.
3. **Actual companion tests need credit.** `CT_R1_3` tests failure when the AARM system is unavailable, supporting a partial fail-closed analogue for 7.6.3 in C; it is not an evidence-store recovery test. `CT_R5_1` includes policy version/hash per schema, and `CT_R8_1` checks correct-schema telemetry. A broad claim that AARM has no such testing would omit the inspected companion. A missing schema is not evidence that those displayed tests are absent.
4. **Receipt integrity has a limited subject.** Tamper detection does not by itself supply anti-equivocation, per-source omission detection, external root anchoring, retention, canonical serialization or algorithm-identifier rules. Each row below identifies the actual inspected source and the remaining duty; the conclusion is bounded to that source set.
5. **C10 analogies remain contestable.** An evidence package is not a prescribed conformance-statement field set (10.1.4); a verification capability is not a scheduled operating validator (10.3.3); one working-group package review is not recurring pipeline reassessment (10.3.5). The broader PM alternatives remain explicit in the companion data rather than being erased by those distinctions.

## Row proposals

`B` is the existing baseline label; `P` and `C` are scoped proposals, not replacement entries. EM/PM/NM use the existing rubric. Source keys are local lookup labels in the companion data, not new AARM requirement identifiers. A listed source for NM is the nearest inspected clause, not a statement that it requires the missing control.

| Proof-of-Control row | Baseline | P | C | Inspected source keys (P / C) | Source/rationale proposal |
|---|---|---|---|---|---|
| 7.1.1 | PM | PM | PM | R1 | Mandatory pre-execution interception is the same general control; Proof-of-Control specifies its architecture. |
| 7.1.2 | PM | PM | PM | R5, R6 / R5, R6, CT_R5_2 | Per-action receipts and identity binding partially cover action evidence without matching every phase duty. |
| 7.1.3 | NM | PM | PM | ABSTRACT, R5 | Explicit recording before execution is a partial timing control; absence of the durable-write gate prevents EM, not PM. |
| 7.1.4 | NM | PM | PM | R1, ARCH61 | Mandatory interception/control-plane mediation is a partial control; Proof-of-Control adds specific attested effect bindings. |
| 7.1.5 | NM | NM | NM | CONFORMANCE | Core/Extended eligibility is a different claim regime, not this evidence/mechanism-dependent restriction. |
| 7.2.1 | PM | PM | PM | ABSTRACT, R5 | Pre-execution recording and receipt timestamps overlap contemporaneous evidence, without the transaction mechanism. |
| 7.2.2 | PM | NM | NM | R5 | A timestamp field is not an external time-anchoring control; keep the temporal-evidence PM alternative visible. |
| 7.2.3 | NM | NM | NM | ARCH_NEUTRAL, ARCH63 | An implementation architecture description does not impose measurement freshness. |
| 7.2.4 | NM | NM | NM | R6 | Agent identity binding does not bind that key to a hardware measurement. |
| 7.3.1 | PM | PM | PM | R5 / R5, CT_R5_2, CT_R5_3 | Receipt tamper evidence is a general integrity control; missing history mechanisms limit the match to PM. |
| 7.3.2 | PM | NM | PM | R6, R5 / CT_R5_2, CT_R5_3 | Primary: identity binding does not prescribe a signing-key architecture, so NM remains the reasoned alternative. Companion: explicit receipt signatures provide a partial signing control; custody isolation is still absent. |
| 7.3.3 | PM | NM | NM | R5 / R5, CT_R5_3 | Detecting altered receipts is not a history anti-equivocation duty; the two properties must not be inferred from one another. |
| 7.3.4 | NM | NM | NM | R5 / R5, CT_R5_2 | Receipt verification does not require proving membership in a committed log. |
| 7.3.5 | NM | NM | NM | R5 / R5, CT_R5_3 | Tamper evidence does not impose consistency between published histories. |
| 7.4.1 | NM | NM | NM | ARCH_NEUTRAL, ARCH62, ARCH64 | Acknowledged architecture trade-offs are not a disclosure obligation. |
| 7.5.1 | NM | NM | NM | R5, R2, R3 | Receipt fields and intent-aware policy do not impose this semantic boundary on every field. |
| 7.5.2 | NM | NM | NM | CONFORMANCE | Generic conformance-package review is not this specific public-claims control. |
| 7.6.1 | PM | NM | NM | R4, R5 / CT_R1_3 | Authorization outcomes or fail-closed outage handling do not provide logging-system failure observability. |
| 7.6.2 | PM | NM | NM | R5 / R5, CT_R5_3 | Receipt modification checks do not establish omission detection. |
| 7.6.3 | PM | NM | PM | R1, R4, R5 / CT_R1_3 | Primary: no explicit evidence-failure behavior. Companion: AARM-unavailability fail-closed test supplies a partial control, though not the evidence-store mechanism. |
| 7.6.4 | PM | PM | PM | R9, R5 | Per-action least privilege (SHOULD; required for Extended) and agent-action receipts are a limited access-control analogue. |
| 7.6.5 | PM | NM | NM | R5, CONFORMANCE | Receipt creation and conformance review do not prescribe retention. |
| 7.6.6 | PM | NM | NM | R5 | A signed/timestamped receipt does not supply external anchoring. |
| 7.7.1 | PM | PM | PM | R5, R8 / CT_R5_1, CT_R8_1 | Receipt fields and standard telemetry/schema tests partially cover structured evidence. Unprovided schema contents remain unassessed. |
| 7.7.2 | NM | NM | NM | R5, R6, R8 / CT_R5_1, CT_R5_2 | Format and signature requirements do not specify canonicalization. No judgement is made about the unavailable referenced schema. |
| 7.7.3 | NM | NM | NM | R6 / CT_R5_2 | Signature validation does not impose this algorithm-selection/metadata rule. |
| 7.7.4 | NM | NM | NM | CONFORMANCE_STEPS / CT_R5_3, CT_R8_1 | Actual tamper/schema tests are acknowledged, but canonical-form conformance is a different test object; breadth remains contestable. |
| 7.7.5 | NM | NM | NM | R5, R8 / CT_R5_1 | Receipt fields and interoperability do not decide ambiguous parser behavior. |
| 10.1.1 | PM | PM | PM | CONFORMANCE, CONFORMANCE_STEPS | Conformance claims and evidence review are analogous general controls, without Proof-of-Control's named stages. |
| 10.1.2 | PM | NM | NM | CONFORMANCE, CONFORMANCE_STEPS | Core/Extended eligibility does not impose that domain/marketing boundary; a broad PM analogy remains open. |
| 10.1.3 | PM | PM | PM | CONFORMANCE, CONFORMANCE_STEPS | Evidence compiled for each requirement partially covers claim-to-evidence traceability. |
| 10.1.4 | PM | NM | NM | CONFORMANCE, CONFORMANCE_STEPS | Evidence-package existence is not a prescribed statement field set; keep the broad-package PM alternative. |
| 10.1.5 | PM | NM | NM | CONFORMANCE | The specification's own metadata is not a duty on an implementation claim. |
| 10.1.6 | PM | NM | NM | R1, CONFORMANCE | Universal action interception does not prescribe documentary scope/exclusion declarations; the broader scope analogy remains open. |
| 10.1.7 | PM | NM | NM | R8, CONFORMANCE / CT_R8_1 | Action telemetry and conformance statements are different artifacts. |
| 10.1.8 | PM | NM | NM | R8 / CT_R8_1 | Observability export does not impose deployment discovery reconciliation. |
| 10.2.1 | NM | NM | NM | ARCH_NEUTRAL, ARCH62, ARCH64 | Architecture trust commentary is not the required disclosure. |
| 10.2.2 | NM | NM | NM | ARCH_NEUTRAL, ARCH62, ARCH64 | Named trust trade-offs do not impose comparable disclosure tags. |
| 10.3.1 | PM | PM | PM | R5 / R5, CT_R5_2, CT_R5_3 | Receipt integrity is a partial evidence-integrity control despite missing store/history duties. |
| 10.3.2 | PM | PM | PM | R1, R5 | Universal interception and receipts partially cover all-action evidence generation without the prescribed reconciliation. |
| 10.3.3 | PM | NM | NM | R5 / R5, CT_R5_2, CT_R5_3 | Verification capability and conformance tests do not require an operating scheduled validator; the broad PM analogy remains visible. |
| 10.3.4 | PM | NM | NM | R7, R8 / CT_R7_1, CT_R8_1 | Intent-drift alerts and telemetry concern different events from evidence-pipeline assurance. |
| 10.3.5 | PM | NM | NM | CONFORMANCE, CONFORMANCE_STEPS | One TWG package review is not recurring reassessment; the generic-assurance PM alternative remains open. |
| 10.3.6 | PM | NM | NM | R1, R5 | All-action receipt intent does not impose a metric-publication duty; retain the broad coverage-topic alternative. |
| 10.3.7 | PM | NM | NM | CONFORMANCE_STEPS, R8 / CT_R5_1, CT_R8_1 | Generic conformance/schema tests assess a different subject; retain the broad testing analogy as an alternative. |

The companion contains the full missing-duty and alternative text for every row, including the primary-only 7.3.2 alternative, the C10 borderline readings and the breadth judgement at 7.7.4. No row is promoted from unavailable evidence to a negative finding.

## Review boundary

The requested review is whether the quoted sources and the stated scope justify each rationale and proposed alternative. Source facts and coding judgements are separate. This note does not establish the adequacy of a real implementation, the truth of an execution claim or equivalence between the frameworks' conformance regimes.

The required independent-human coding, blinding, reliability and adjudication process has not been completed by this assisted review. The existing assisted reverse analysis also does not replace that study; a C7/C10-only comparison must not be described as absence from all Proof-of-Control requirements. No coverage percentage, aggregate label count, agreement statistic or new experiment is reported here. No canonical update is requested in this carrier.
