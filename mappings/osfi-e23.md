# Crosswalk: OSFI Guideline E-23

| | |
| --- | --- |
| **Framework type** | Prudential guideline, Canada (Office of the Superintendent of Financial Institutions) |
| **Corpus version** | Guideline E-23, Model Risk Management (2027), published 11 September 2025, effective 1 May 2027. [Access](https://www.osfi-bsif.gc.ca/en/guidance/guidance-library/guideline-e-23-model-risk-management-2027) · [corpus provenance](corpus/README.md) |
| **Relationship** | Complementary. E-23 governs how an institution manages model risk; Proof-of-Control evidences what an agent did under the controls that process sets |
| **Coding status** | Draft seed coding, single coder. [Rubric](rubric.md) |

## The Relationship

E-23 applies to every federally regulated financial institution in Canada: banks, foreign bank branches, life insurance and fraternal companies, property and casualty companies, and trust and loan companies. It is principles-based and applies in proportion to each institution's size, strategy, risk profile and complexity. It covers AI/ML models explicitly.

Its subject is the institution's model risk management across the model lifecycle: design, review, approval, deployment, monitoring and decommission. Proof-of-Control's subject is the evidence of what an agent system did.

| | OSFI E-23 | Proof-of-Control |
| --- | --- | --- |
| Question answered | "Is model risk identified, rated and managed across the model lifecycle?" | "Did the AI system operate within its defined control boundaries, and can anyone verify that?" |
| Subject | The institution's models and its model risk management | The agent system's execution |
| Evidence | Model inventory, documentation, review assessments, approval decisions and monitoring results, held by the institution | Mechanism-generated, tamper-evident, contemporaneous execution evidence |
| Trust required | The institution and its reviewers | The mechanism and the parties it rests on (Tiers 3 and 4) |

### Where E-23 reaches an agent

E-23 does not use the word "agent". Four passages bring the models inside an agent system into its scope:

* **Section A.4 and footnote 1.** A model includes AI/ML methods, and an AI system "can be based on one or multiple models".
* **Principle 2.2** lists "level of autonomy" as a qualitative factor in the model risk rating.
* **Principle 3.4** lists "model modifications (including changes to algorithms, parameters, or supporting operational components)" among the events that prompt a model review.
* **Principle 3.6** asks for processes for "autonomous decision making, autonomous re-parametrization, and the elevated potential for model drift".

The strongest match in the coding below is 10.1.8. Principle 2.1 asks institutions to identify all models in use, including vendor and third-party models, and to keep an accurate, evergreen inventory. Proof-of-Control 10.1.8 asks for the declared inventory to be reconciled against automated discovery. E-23 does not require automated discovery, so the match is partial.

## Requirement-Level Mapping

<!-- BEGIN GENERATED MAPPING (tools/generate_crosswalks.py) -->

**Coverage: 11%** of the 127 Proof-of-Control requirements (0 exact matches, 14 partial matches, 113 not covered), computed per the [mapping rubric](rubric.md) from the row-level [coding sheet](coding_sheet.csv). *Draft seed coding — pending working-group validation.* To change this table, edit the coding sheet and run `python3 tools/generate_crosswalks.py`.

**How to read the Match column** ([full rubric](rubric.md)): **Exact** — the framework has a clause equivalent in scope and intent. **Partial** — the framework covers the topic, but not with Proof-of-Control's operator-independent evidence (or not at the same depth). **None** — the framework has no analogous provision. Where a section holds a mix, the badge shows the strongest match present and the **Covered** column shows how many of its requirements are matched at all — so a section reading *Partial 3/5* has two requirements this framework does not reach.

| Section | Reqs | Covered | Match | Closest framework clause(s) | Rationale |
| --- | :---: | :---: | :---: | --- | --- |
| [C1.1 Model and Artifact Provenance](../0.1/en/0x10-C01-Provenance.md) | 5 | 1/5 | Partial | Principle 3.5 | Principle 3.5 requires that integrating models into operational settings preserve their integrity and reliability; no load-time digest comparison against a signed manifest, and no per-comparison record. Not reached: 1.1.1, 1.1.3, 1.1.4, 1.1.5. |
| [C1.2 Input and Data Lineage](../0.1/en/0x10-C01-Provenance.md) | 4 | 2/4 | Partial | Principle 3.2 | Principle 3.2 requires controls on data cleansing and documented provenance of synthetic and proxy data; no hash-linked, append-only transformation log. Not reached: 1.2.1, 1.2.2. |
| [C1.3 Compute Substrate Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Appendix 1 records model dependencies at inventory level; no per-execution identification of the compute environment |
| [C1.4 Privacy-Preserving Provenance](../0.1/en/0x10-C01-Provenance.md) | 2 | 0/2 | None | — | Principle 3.2 requires model data to meet privacy requirements; provenance records holding digests instead of payloads not addressed |
| [C2.1 Data-Access Evidence](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | Per-operation data access records not addressed |
| [C2.2 Policy and Consent Enforcement](../0.1/en/0x10-C02-Privacy.md) | 5 | 0/5 | None | — | Principle 3.2 requires model data to be compliant with privacy requirements; no runtime consent evaluation |
| [C2.3 Privacy-Preserving Verification Mechanisms](../0.1/en/0x10-C02-Privacy.md) | 3 | 0/3 | None | — | Cryptographic privacy mechanisms not addressed |
| [C2.4 Evidence Handling for Protected Data](../0.1/en/0x10-C02-Privacy.md) | 2 | 0/2 | None | — | Minimized forms of protected data in retained evidence not addressed |
| [C3.1 Boundary-Crossing Evidence](../0.1/en/0x10-C03-Portability.md) | 2 | 0/2 | None | — | Boundary-crossing records not addressed |
| [C3.2 Cross-Environment Continuity](../0.1/en/0x10-C03-Portability.md) | 3 | 0/3 | None | — | Decommission keeps a retired model and its documentation for a set period; continued verifiability of evidence after a migration not addressed |
| [C4.1 Authority and Scope Enforcement](../0.1/en/0x10-C04-Authorization.md) | 8 | 4/8 | Partial | Appendix 1; Principle 2.3; Principle 2.3; Principle 3.6; Principle 2.3; Principle 3.5; D.2 Model decommission | Appendix 1 records approved uses and limitations, and Principle 2.3 sets limits or constraints on model usage by risk rating; no per-run record of granted permissions, scope and expiry. Not reached: 4.1.4, 4.1.5, 4.1.7, 4.1.8. |
| [C4.2 Delegation](../0.1/en/0x10-C04-Authorization.md) | 4 | 0/4 | None | — | Signed authorization tokens not addressed |
| [C5.1 Agent and Principal Binding](../0.1/en/0x10-C05-Identity.md) | 4 | 0/4 | None | — | Appendix 1 names a model owner, an accountable unit, not the principal for each action; per-action attribution not addressed |
| [C5.2 Inter-Agent Identity](../0.1/en/0x10-C05-Identity.md) | 2 | 0/2 | None | — | Inter-agent message signing not addressed |
| [C6.1 Execution Environment Integrity](../0.1/en/0x10-C06-Security.md) | 4 | 1/4 | Partial | Principle 3.6 | Principle 3.6 requires tracking and evaluating model usage; no per-invocation record of tool, arguments and result. Not reached: 6.1.1, 6.1.3, 6.1.4. |
| [C6.2 Isolation and Confidential Execution](../0.1/en/0x10-C06-Security.md) | 3 | 0/3 | None | — | Sandboxing of generated code not addressed |
| [C6.3 Cryptographic Key Lifecycle](../0.1/en/0x10-C06-Security.md) | 5 | 0/5 | None | — | Key management not addressed in E-23 |
| [C7.1 Generation at the Action Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | No interception gateway concept |
| [C7.2 The Contemporaneous Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 4 | 0/4 | None | — | Timing of record creation not addressed |
| [C7.3 The Tamper-Evident Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | Hash chaining of records not addressed. Principle 2.1 asks for an inventory subject to robust controls, which is not record integrity |
| [C7.4 The Transparent Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 1 | 0/1 | None | — | No disclosure of the parties and assumptions evidence rests on |
| [C7.5 The Determinism Boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 2 | 0/2 | None | — | Evidence schema content not addressed |
| [C7.6 Evidence Custody and Resilience](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 6 | 0/6 | None | — | Principle 3.6 contingency plans cover model unavailability and failure, not evidence-pipeline failures |
| [C7.7 The Interoperable Property](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md) | 5 | 0/5 | None | — | No evidence schema requirement |
| [C8.1 Tier Placement](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 8 | 0/8 | None | — | No grading of evidence by verifiability |
| [C8.2 Mechanism-to-Requirement Fit](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 2 | 0/2 | None | — | No mechanism-to-requirement fit rule |
| [C8.3 Chain Integrity and Self-Enforcement (Tier 4)](../0.1/en/0x10-C08-Verifiability-Tiers.md) | 5 | 0/5 | None | — | No self-enforcement concept |
| [C9.1 Locating Evidence on the System Surface](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | No stack-location requirement |
| [C9.2 Layer Coverage](../0.1/en/0x10-C09-System-Surface-MAESTRO.md) | 3 | 0/3 | None | — | Tamper-evident logging coverage not addressed |
| [C10.1 Conformance Claims](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 8 | 4/8 | Partial | Principle 3.4; Appendix 1; Appendix 1; D.2 Model rationale; Appendix 1; Principle 2.1 | Principle 3.4 requires review independent of development, by internal reviewers or objective third parties, and Appendix 1 records the model reviewer and approver; no published statement of an assurance stage. Not reached: 10.1.2, 10.1.3, 10.1.5, 10.1.7. |
| [C10.2 Trust-Assumption Disclosure](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 2 | 1/2 | Partial | Appendix 1; Principle 2.2 | Appendix 1 records model origin, developer and dependencies, and Principle 2.2 rates externally developed models on a standalone basis, so the parties a model relies on are named; no disclosure of the trust assumptions behind evidence. Not reached: 10.2.2. |
| [C10.3 Continuously Monitored Operation](../0.1/en/0x10-C10-Conformance-and-Disclosure.md) | 7 | 1/7 | Partial | A.4 Model; Principle 3.4 | An automated validator built on AI/ML is a model under A.4, so Principle 3.4 independent review of its performance applies; E-23 does not name structured-trace parsing. Not reached: 10.3.1, 10.3.2, 10.3.3, 10.3.4, 10.3.5, 10.3.6. |

### Gap Analysis (what this framework does not cover)

* **C1.1 Model and Artifact Provenance** — partially reached; no provision for 1.1.1, 1.1.3, 1.1.4, 1.1.5: Appendix 1 records model ID and version at inventory level; E-23 does not address what each execution record carries
* **C1.2 Input and Data Lineage** — partially reached; no provision for 1.2.1, 1.2.2: Principle 3.2 traceability covers data used to develop the model and Principle 3.6 tracks changes in input data in aggregate; neither records runtime inputs per action
* **C1.3 Compute Substrate Provenance** — Appendix 1 records model dependencies at inventory level; no per-execution identification of the compute environment
* **C1.4 Privacy-Preserving Provenance** — Principle 3.2 requires model data to meet privacy requirements; provenance records holding digests instead of payloads not addressed
* **C2.1 Data-Access Evidence** — Per-operation data access records not addressed
* **C2.2 Policy and Consent Enforcement** — Principle 3.2 requires model data to be compliant with privacy requirements; no runtime consent evaluation
* **C2.3 Privacy-Preserving Verification Mechanisms** — Cryptographic privacy mechanisms not addressed
* **C2.4 Evidence Handling for Protected Data** — Minimized forms of protected data in retained evidence not addressed
* **C3.1 Boundary-Crossing Evidence** — Boundary-crossing records not addressed
* **C3.2 Cross-Environment Continuity** — Decommission keeps a retired model and its documentation for a set period; continued verifiability of evidence after a migration not addressed
* **C4.1 Authority and Scope Enforcement** — partially reached; no provision for 4.1.4, 4.1.5, 4.1.7, 4.1.8: Validation of tool-call parameters not addressed
* **C4.2 Delegation** — Signed authorization tokens not addressed
* **C5.1 Agent and Principal Binding** — Appendix 1 names a model owner, an accountable unit, not the principal for each action; per-action attribution not addressed
* **C5.2 Inter-Agent Identity** — Inter-agent message signing not addressed
* **C6.1 Execution Environment Integrity** — partially reached; no provision for 6.1.1, 6.1.3, 6.1.4: Model approval accepts compensating mitigants and Principle 2.3 names controls for residual risk; no mapping of each declared control to an evidence source
* **C6.2 Isolation and Confidential Execution** — Sandboxing of generated code not addressed
* **C6.3 Cryptographic Key Lifecycle** — Key management not addressed in E-23
* **C7.1 Generation at the Action Boundary** — No interception gateway concept
* **C7.2 The Contemporaneous Property** — Timing of record creation not addressed
* **C7.3 The Tamper-Evident Property** — Hash chaining of records not addressed. Principle 2.1 asks for an inventory subject to robust controls, which is not record integrity
* **C7.4 The Transparent Property** — No disclosure of the parties and assumptions evidence rests on
* **C7.5 The Determinism Boundary** — Evidence schema content not addressed
* **C7.6 Evidence Custody and Resilience** — Principle 3.6 contingency plans cover model unavailability and failure, not evidence-pipeline failures
* **C7.7 The Interoperable Property** — No evidence schema requirement
* **C8.1 Tier Placement** — No grading of evidence by verifiability
* **C8.2 Mechanism-to-Requirement Fit** — No mechanism-to-requirement fit rule
* **C8.3 Chain Integrity and Self-Enforcement (Tier 4)** — No self-enforcement concept
* **C9.1 Locating Evidence on the System Surface** — No stack-location requirement
* **C9.2 Layer Coverage** — Tamper-evident logging coverage not addressed
* **C10.1 Conformance Claims** — partially reached; no provision for 10.1.2, 10.1.3, 10.1.5, 10.1.7: Declared domains and marketing limits not addressed
* **C10.2 Trust-Assumption Disclosure** — partially reached; no provision for 10.2.2: No category scheme for trust assumptions
* **C10.3 Continuously Monitored Operation** — partially reached; no provision for 10.3.1, 10.3.2, 10.3.3, 10.3.4, 10.3.5, 10.3.6: Tamper-evident evidence store not addressed

*Coding granularity is the individual requirement; the section rows above summarize the requirements beneath them. Where a section is coded uniformly the summary is exact, and where it is mixed the Covered column and the gap list name what is missing. Row-level detail is in the [coding sheet](coding_sheet.csv). This is seed coding by a single coder and has not yet had the second-coder pass the [rubric](rubric.md) requires.*

<!-- END GENERATED MAPPING -->

## Reverse Mapping (what E-23 requires that Proof-of-Control does not)

Proof-of-Control verifies adherence, not adequacy. Most of E-23 asks for judgments about whether a model is sound and fit for its purpose, which is validation and sits outside the standard.

| E-23 provision | What it requires | Why Proof-of-Control does not cover it |
| --- | --- | --- |
| Principle 1.1 | Senior management accountability, MRM resourcing, a multidisciplinary team | Organizational governance, not system evidence |
| Principle 1.2 | An MRM framework aligned to risk appetite, reviewed periodically, covering third-party models | Framework design, not system evidence |
| Principle 1.3 | Models used only where they are fit for their business purpose | A judgment of adequacy |
| Principle 2.2 | A model risk rating built on quantitative and qualitative factors | A risk judgment. Level of autonomy is a rating factor, not an evidence property |
| Principle 2.3 | Review, documentation, approval authority and monitoring intensity set by the rating | Process proportionality. The usage-limit part is partially reached (4.1.1 to 4.1.3) |
| Principle 3.1 | Lifecycle policies, independence and stakeholder accountabilities | Governance, not system evidence |
| Principle 3.2 | Development data that is accurate, representative, compliant, traceable and timely, with bias managed | Data quality is validation. Traceability is partially reached (1.2.3, 1.2.4) |
| Principle 3.3 | Development standards, documentation, explainability requirements and performance criteria | Outside the standard's scope |
| Principle 3.4 | Independent review of conceptual soundness and performance | Validation of the model, not verification of its execution |
| D.2 Model approval | An approval decision that affirms the risk rating and residual risk | An institutional decision |
| Principle 3.6 | Performance monitoring, drift thresholds and contingency plans | Model performance. Proof-of-Control evidence records execution facts, not quality (C7.5) |
| D.2 Model decommission | A disciplined retirement process, retention of the retired model, monitoring of downstream effects | Lifecycle process, not system evidence |
| Appendix 1 | Inventory fields such as risk rating, owner, reviewer, approver, review dates and monitoring status | Inventory content. The identification fields are partially reached (10.1.4) |

## What This Crosswalk Does Not Say

* A mapping identifies relevance. It does not establish compliance with E-23, and meeting a Proof-of-Control requirement does not satisfy an E-23 expectation.
* E-23 refers to other OSFI guidelines: B-10 for models and data from third-party vendors, and B-13 and E-21 for risk assessments before deployment. Those guidelines were not coded here.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
